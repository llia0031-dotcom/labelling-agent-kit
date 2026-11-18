"""The labelling agent: one generic flow, configured per arm, filled in per task.

Flow for one item (code decides every branch; the model decides the labels):

  1. LABEL      The model reads the item and the label catalogue. Case arms: the code first retrieves the
                most similar labelled cases (BM25 on the item text) and puts them in the first message.
                Agent arms may call tools:
                  get_label_rules  the rule of one or more labels (applies / does not apply / boundaries)
                  compare_labels   the boundary and precedence rules for a pair of labels
                  search_cases     labelled cases that resemble a query (BM25)
                  phrase_stats     how the cases that contain a phrase were labelled
                After MAX_ROUNDS tool rounds the model must answer.
  2. VALIDATE   Unknown label ids and labels outside the item's scope are dropped. Agent arms, at most once
                each: labels given without their rule having been read get their rules sent (the rule gate);
                a quote that is not the item's own words gets one turn to fix it or drop the label.
  3. CHECK      (check arms only) One more turn: confirm each label against its rule, decide the unsure
                ones, and look at labels whose keywords occur in the item but were not given.
  4. RESULT     Labels, evidence, confidence, the tool calls, the branches taken and the token usage.

A job is a generator for llm.Engine: it yields request parameters and receives each answer, so many
items and arms share each Message Batch.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from dataclasses import dataclass, field

from . import llm
from .task import Task

MAX_ROUNDS = 5


@dataclass(frozen=True)
class Arm:
    id: str                       # name used in results, e.g. "agent-cases"
    rules: str = "catalogue"      # "catalogue" (one line per label) or "full" (the whole rulebook in the prompt)
    tools: tuple = ()             # subset of ("rules", "cases")
    check: bool = False           # the self-check turn
    cases: str | None = None      # case library name; None = the task's default
    prompt: str = "v1"            # instruction version
    rules_file: str = "rules.json"
    effort: str | None = None     # overrides the engine's effort for this arm (a tuning parameter)

    @property
    def repair(self) -> bool:     # the quote-repair turn belongs to the agent arms
        return bool(self.tools)


ARMS = {
    "prompt-short": Arm("prompt-short"),
    "prompt-rules": Arm("prompt-rules", rules="full"),
    "agent": Arm("agent", tools=("rules",)),
    "agent-cases": Arm("agent-cases", tools=("rules", "cases")),
    "agent-cases-check": Arm("agent-cases-check", tools=("rules", "cases"), check=True),
}


def arm_from(spec: dict) -> Arm:
    base = ARMS[spec["arm"]]
    return Arm(spec.get("id", base.id), base.rules, base.tools, base.check, spec.get("cases", base.cases),
               spec.get("prompt", base.prompt), spec.get("rules_file", base.rules_file), spec.get("effort"))


# ---------------- prompts ----------------

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


class _Prompts(dict):
    """Instruction versions, read from prompts/<version>.json the first time they are used."""

    def __missing__(self, version: str) -> dict:
        path = PROMPT_DIR / f"{version}.json"
        if not path.exists():
            raise KeyError(f"no prompt version {version!r} (looked for {path})")
        self[version] = json.loads(path.read_text(encoding="utf-8"))
        return self[version]


PROMPTS = _Prompts()


def tool_defs(arm: Arm, labels: list[str]) -> list[dict]:
    out = []
    if "rules" in arm.tools:
        out += [
            {"name": "get_label_rules", "description": "The rule of one or more labels: definition, when it applies, when it does not, and its boundaries with other labels.",
             "input_schema": {"type": "object", "properties": {"labels": {"type": "array", "items": {"type": "string", "enum": labels}, "minItems": 1}},
                              "required": ["labels"], "additionalProperties": False}},
            {"name": "compare_labels", "description": "The boundary and precedence rules between two labels that might both fit.",
             "input_schema": {"type": "object", "properties": {"a": {"type": "string", "enum": labels}, "b": {"type": "string", "enum": labels}},
                              "required": ["a", "b"], "additionalProperties": False}},
        ]
    if "cases" in arm.tools:
        out += [
            {"name": "search_cases", "description": "Labelled cases that resemble the query (keyword search). Optionally only cases that carry one label.",
             "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "label": {"type": "string", "enum": labels},
                                                               "k": {"type": "integer", "minimum": 1, "maximum": 8}},
                              "required": ["query"], "additionalProperties": False}},
            {"name": "phrase_stats", "description": "How the cases that contain an exact phrase were labelled: the share of them carrying each label.",
             "input_schema": {"type": "object", "properties": {"phrase": {"type": "string"}}, "required": ["phrase"], "additionalProperties": False}},
        ]
    return out


def schema(labels: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "labels": {"type": "array", "items": {"type": "object", "properties": {
                "id": {"type": "string", "enum": labels}, "evidence": {"type": "string"},
                "confidence": {"type": "string", "enum": ["sure", "unsure"]}},
                "required": ["id", "evidence", "confidence"], "additionalProperties": False}},
            "rejected": {"type": "array", "items": {"type": "object", "properties": {
                "id": {"type": "string", "enum": labels}, "reason": {"type": "string"}},
                "required": ["id", "reason"], "additionalProperties": False}},
        },
        "required": ["labels", "rejected"], "additionalProperties": False,
    }


def system_prompt(task: Task, item: dict, arm: Arm) -> str:
    p = PROMPTS[arm.prompt]
    c = task.config
    fmt = {"noun": c["item_noun"], "title": c["title"], "description": c["description"]}
    parts = [p["intro"].format(**fmt), "", "Labels for this " + c["item_noun"] + ":", task.catalogue(item)]
    general = task.general_rules(item)
    if general:
        parts += ["", "General rules:"] + [f"- {g}" for g in general]
    if arm.rules == "full":
        parts += ["", "The full rulebook:", "", task.full_rulebook(item)]
    steps = (p["work_tools"] + (p["work_cases"] if "cases" in arm.tools else []) + p["work_end"]) if arm.tools else p["work_no_tools"]
    parts += ["", "How to work:"] + [f"{n}. {s.format(**fmt)}" for n, s in enumerate(steps, 1)]
    parts += ["", p["answer"].format(**fmt)]
    return "\n".join(parts)


def user_prompt(task: Task, item: dict, arm: Arm | None = None) -> str:
    noun = task.config["item_noun"]
    text = f"Label this {noun}.\n\n<{noun}>\n{item['text']}\n</{noun}>"
    if arm is not None and "cases" in arm.tools:
        p = PROMPTS[arm.prompt]
        cases = task.prefetch_cases(item, arm.cases)
        text += "\n\n" + p["cases_intro"].format(noun=noun) + "\n" + cases
    return text


# ---------------- checks ----------------

def norm(s: str) -> str:
    s = s.replace("\\n", "\n")
    s = re.sub(r"[\s　]+", "", s)
    return s.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "，": ",", "：": ":", "！": "!", "？": "?", "；": ";", "（": "(", "）": ")"}))


def quote_ok(quote: str, text: str) -> bool:
    """A quote is the item's own words if each piece (split at ellipses) occurs in the text, ignoring
    whitespace, full-width punctuation and letter case."""
    pieces = [x for x in re.split(r"\.\.\.|…|⋯", quote) if norm(x)]
    t = norm(text).lower()
    return bool(pieces) and all(norm(x).lower() in t for x in pieces)


def clean(data: dict, allowed: list[str]) -> dict:
    seen, labels, dropped = set(), [], []
    for l in data.get("labels", []) if isinstance(data, dict) else []:
        lid = l.get("id") if isinstance(l, dict) else None
        if lid in allowed and lid not in seen:
            seen.add(lid)
            labels.append({"id": lid, "evidence": str(l.get("evidence", "")), "confidence": l.get("confidence", "sure")})
        elif lid not in seen:
            dropped.append(lid)
    rejected = [r for r in (data.get("rejected", []) if isinstance(data, dict) else []) if isinstance(r, dict)]
    return {"labels": labels, "rejected": rejected, "dropped_unknown": dropped}


# ---------------- the job ----------------

def label_job(task: Task, item: dict, arm: Arm):
    p = PROMPTS[arm.prompt]
    noun = task.config["item_noun"]
    allowed = task.labels_for(item)
    tools = tool_defs(arm, allowed)
    sys_text = system_prompt(task, item, arm)
    messages: list[dict] = [{"role": "user", "content": user_prompt(task, item, arm)}]
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
    rec = {"item_id": item["id"], "arm": arm.id, "prompt": arm.prompt, "cases": arm.cases, "rules_file": arm.rules_file,
           "labels": [], "answer": None, "ok": False, "error": None, "calls": 0, "tool_rounds": 0, "tool_calls": [],
           "branches": {"rule_gate": None, "repair": None, "check": None}, "stages": [], "cost_usd": 0.0}
    rounds, stage, repaired, gated = 0, "label", False, False
    rule_reads: set[str] = set()
    while True:
        req = {"system": [{"type": "text", "text": sys_text, "cache_control": {"type": "ephemeral"}}], "messages": list(messages),
               "output_config": {"format": {"type": "json_schema", "schema": schema(allowed)}}}
        if arm.effort:
            req["output_config"]["effort"] = arm.effort
        if tools:
            req["tools"] = tools
            if rounds >= MAX_ROUNDS:
                req["tool_choice"] = {"type": "none"}
        resp = yield req
        rec["calls"] += 1
        if "error" in resp:
            rec["error"] = resp["error"]
            break
        for k in usage:
            usage[k] += resp["usage"].get(k, 0)
        rec["cost_usd"] += llm.cost_of(resp["usage"], resp.get("pricing", "batch"))
        messages.append({"role": "assistant", "content": resp["content"]})
        if resp.get("stop_reason") == "tool_use" and tools:
            rounds += 1
            results = []
            for b in llm.tool_uses(resp):
                out, is_err = run_tool(task, item, arm, b["name"], b.get("input") or {})
                if b["name"] == "get_label_rules" and not is_err:
                    rule_reads.update(b["input"].get("labels", []))
                rec["tool_calls"].append({"stage": stage, "name": b["name"], "input": b.get("input"), "chars": len(out), "is_error": is_err})
                results.append({"type": "tool_result", "tool_use_id": b["id"], "content": out, "is_error": is_err})
            messages.append({"role": "user", "content": results})
            continue
        data, why = llm.final_json(resp)
        if data is None:
            rec["error"] = why
            break
        ans = clean(data, allowed)
        rec["stages"].append({"stage": stage, "labels": [l["id"] for l in ans["labels"]],
                              "unsure": [l["id"] for l in ans["labels"] if l["confidence"] == "unsure"]})
        unread = [l["id"] for l in ans["labels"] if l["id"] not in rule_reads]
        if unread and "rules" in arm.tools and not gated:
            gated = True
            rule_reads.update(unread)
            rec["branches"]["rule_gate"] = unread
            messages.append({"role": "user", "content": p["gate"].format(labels=", ".join(unread), rules=task.rules_text(item, unread))})
            continue
        bad = [l for l in ans["labels"] if not quote_ok(l["evidence"], item["text"])]
        if bad and arm.repair and not repaired:
            repaired = True
            rec["branches"]["repair"] = [l["id"] for l in bad]
            listing = "; ".join(f'{l["id"]}: "{l["evidence"]}"' for l in bad)
            messages.append({"role": "user", "content": p["repair"].format(noun=noun, bad=listing)})
            continue
        if arm.check and stage == "label":
            stage = "check"
            given = {l["id"] for l in ans["labels"]}
            hinted = [h for h in task.keyword_hits(item) if h["id"] not in given]
            hints = p["hints"].format(noun=noun, labels=", ".join(f"{h['id']} ({', '.join(map(str, h['keywords'][:3]))})" for h in hinted)) if hinted else ""
            rec["branches"]["check"] = {"hinted": [h["id"] for h in hinted], "before": sorted(given)}
            messages.append({"role": "user", "content": p["check"].format(noun=noun, hints=hints)})
            continue
        rec["answer"] = ans
        rec["labels"] = sorted(l["id"] for l in ans["labels"])
        rec["evidence_ok"] = {l["id"]: quote_ok(l["evidence"], item["text"]) for l in ans["labels"]}
        rec["rules_read"] = sorted(rule_reads)
        rec["ok"] = True
        if arm.check and rec["branches"]["check"]:
            before = set(rec["branches"]["check"]["before"])
            rec["branches"]["check"]["added"] = sorted(set(rec["labels"]) - before)
            rec["branches"]["check"]["dropped"] = sorted(before - set(rec["labels"]))
        break
    rec["tool_rounds"] = rounds
    rec["usage"] = usage
    rec["cost_usd"] = round(rec["cost_usd"], 7)
    return rec


def run_tool(task: Task, item: dict, arm: Arm, name: str, args: dict) -> tuple[str, bool]:
    try:
        if name == "get_label_rules" and "rules" in arm.tools:
            return task.rules_text(item, list(args.get("labels", []))), False
        if name == "compare_labels" and "rules" in arm.tools:
            return task.compare(item, args.get("a", ""), args.get("b", "")), False
        if name == "search_cases" and "cases" in arm.tools:
            return task.search_cases(item, arm.cases, str(args.get("query", "")), int(args.get("k", 5) or 5), args.get("label")), False
        if name == "phrase_stats" and "cases" in arm.tools:
            return task.phrase_stats(item, arm.cases, str(args.get("phrase", ""))), False
        return f"Unknown tool {name}.", True
    except Exception as e:  # a broken tool call is reported back to the model, not raised
        return f"Tool error: {type(e).__name__}: {e}", True
