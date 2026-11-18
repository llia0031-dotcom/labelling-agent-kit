"""Root-cause analysis (RCA) of the failures of one arm.

    python -m lak.rca experiments/main.json --task asap --set test_a --arm agent-cases-check --mode batch

A failure is one wrong label decision: a label given that is not in the gold set (false positive) or a
gold label not given (false negative). For each one the code first collects signals:

  same_error_arms   how many of the other arms on the same items made the same wrong decision
  rule_read         whether the agent read this label's rule before answering
  considered        for a miss: whether the agent listed the label as considered and rejected, and why
  evidence          for a false positive: the quote the agent gave
  check             whether the self-check turn added or dropped this label
  case_share        how the case library labels items containing the agent's quote (false positive) or the
                    strongest cue phrase in the item (miss): the share of those cases carrying the label
  cue               (when the task has cues.json) a strong cue phrase of the label that occurs in the item
  gold_polarity     (ASAP) the dataset's sentiment value for a missed aspect; 0 means a neutral, mild mention

Then every item with failures is sent twice, independently, with the item, the gold and predicted labels,
the rules involved and the signals, and each decision is classified into one of five causes with a reason
and a suggested fix. The second pass lists the causes in reverse order. A decision counts as classified
when both passes agree; otherwise it is reported as split. Output: results/<exp>/rca/<task>-<set>-<arm>.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from . import llm
from .task import ROOT, get_task, read_jsonl

CAUSES = {
    "prompt_defect": "the instructions or the agent's flow led it astray: it skipped a rule it needed, misread what the task asks, "
                     "or the self-check changed a right answer",
    "model_capability": "the rule covers the case and was available, but the model misread the text or reasoned wrongly",
    "rule_conflict": "the rulebook is silent, unclear or contradicts itself on this case, or two rules both seem to fit",
    "sample_distribution": "the item is unusual for the task (very long, off-topic, mixed content, rare label) or unlike the cases",
    "label_ambiguity": "the gold decision itself is debatable: careful labellers could disagree, or the gold looks incomplete or "
                       "inconsistent with the dataset's own conventions",
}
ORDER = list(CAUSES)


def signals(task, item: dict, rec: dict, others: dict[str, dict], cases_lib: str | None) -> list[dict]:
    gold, pred = set(item["labels"]), set(rec["labels"]) if rec["ok"] else set()
    ans = rec.get("answer") or {"labels": [], "rejected": []}
    evid = {l["id"]: l["evidence"] for l in ans["labels"]}
    rejected = {r.get("id"): r.get("reason", "") for r in ans.get("rejected", [])}
    check = rec["branches"].get("check") or {}
    cues = {}
    cues_path = task.dir / "cues.json"
    if cues_path.exists():
        cues = json.loads(cues_path.read_text(encoding="utf-8"))["labels"]
    index = task.case_index(cases_lib, task.scope(item))
    out = []
    for kind, labels in (("false_positive", sorted(pred - gold)), ("miss", sorted(gold - pred))):
        for l in labels:
            same = sum(1 for o in others.values() if (l in o and kind == "false_positive") or (l not in o and kind == "miss"))
            s = {"label": l, "kind": kind, "same_error_arms": same, "other_arms": len(others),
                 "rule_read": l in set(rec.get("rules_read") or []) or l in (rec["branches"].get("rule_gate") or [])}
            phrase = None
            if kind == "false_positive":
                s["evidence"] = evid.get(l, "")
                phrase = (evid.get(l) or "")[:12]
            else:
                s["considered"] = l in rejected
                if l in rejected:
                    s["rejected_reason"] = rejected[l]
                for c in (cues.get(l, {}).get("cues") or []):
                    if c["phrase"] in item["text"]:
                        s["cue"] = {"phrase": c["phrase"], "training_precision": c["precision"]}
                        phrase = c["phrase"]
                        break
                pol = (item.get("meta") or {}).get("polarity", {}).get(l)
                if pol is not None:
                    s["gold_polarity"] = pol
            if check:
                if l in check.get("added", []):
                    s["check"] = "added by the self-check"
                elif l in check.get("dropped", []):
                    s["check"] = "dropped by the self-check"
            if phrase:
                from .task import case_search
                st = case_search.phrase_stats(index.cases, phrase, examples=0)
                if st["cases_with_phrase"]:
                    share = next((x["share"] for x in st["label_shares"] if x["label"] == l), 0.0)
                    s["case_share"] = {"phrase": phrase, "cases": st["cases_with_phrase"], "share_with_label": share}
            s["label_share_in_cases"] = round(sum(1 for c in index.cases if l in c["labels"]) / max(1, len(index.cases)), 3)
            out.append(s)
    return out


SYSTEM = """You analyse why a content-labelling agent got some label decisions wrong. For each wrong decision, pick exactly one root cause:
{causes}

Use the signals: an error that every other arm also made points away from the prompt and toward the rule, the data or the gold label; a rule that was never read points to the flow; a quote that does not support the label, or an obvious mention that was missed although the rule was read, points to the model; a case library that mostly labels such wording the other way points to the gold or the rule. Judge the gold label on the item's own words and the dataset's conventions in the rules, not on what you would prefer.

For each decision give the cause, one sentence on why, and one concrete fix (a rule edit, a prompt edit, more cases of a kind, or "none: document as ambiguous")."""


def cause_list(reverse: bool) -> str:
    keys = ORDER[::-1] if reverse else ORDER
    return "\n".join(f"- {k}: {CAUSES[k]}" for k in keys)


def rca_schema() -> dict:
    return {"type": "object", "properties": {"decisions": {"type": "array", "items": {"type": "object", "properties": {
        "label": {"type": "string"}, "kind": {"type": "string", "enum": ["false_positive", "miss"]},
        "cause": {"type": "string", "enum": ORDER}, "why": {"type": "string"}, "fix": {"type": "string"}},
        "required": ["label", "kind", "cause", "why", "fix"], "additionalProperties": False}}},
        "required": ["decisions"], "additionalProperties": False}


def request(task, item: dict, rec: dict, sig: list[dict], reverse: bool) -> dict:
    labels = sorted({s["label"] for s in sig})
    ans = rec.get("answer") or {"labels": []}
    given = "; ".join(f"{l['id']} (\"{l['evidence']}\", {l['confidence']})" for l in ans["labels"]) or "none"
    user = (f"Task: {task.config['title']}. {task.config['description']}\n\n<item>\n{item['text']}\n</item>\n\n"
            f"Gold labels: {', '.join(sorted(item['labels'])) or 'none'}\nAgent's labels: {given}\n\n"
            f"Wrong decisions with signals:\n{json.dumps(sig, ensure_ascii=False, indent=1)}\n\n"
            f"Rules of the labels involved:\n{task.rules_text(item, labels)}")
    return {"system": SYSTEM.format(causes=cause_list(reverse)), "messages": [{"role": "user", "content": user}],
            "output_config": {"format": {"type": "json_schema", "schema": rca_schema()}}}


def job(task, item, rec, sig, reverse):
    resp = yield request(task, item, rec, sig, reverse)
    data, why = llm.final_json(resp)
    cost = llm.cost_of(resp["usage"], resp.get("pricing", "batch")) if "usage" in resp else 0.0
    return {"data": data, "error": why, "cost_usd": cost}


def run(exp_path: Path, task_name: str, set_name: str, arm_id: str, mode: str, budget: float | None = 0.4) -> dict:
    exp = json.loads(Path(exp_path).read_text(encoding="utf-8"))
    base = ROOT / "results" / exp["name"]
    spec = next(a for r in exp["runs"] if r["task"] == task_name and r["set"] == set_name for a in r["arms"] if a.get("id", a["arm"]) == arm_id)
    task = get_task(task_name, spec.get("rules_file", "rules.json"))
    items = {r["id"]: r for r in task.items(set_name)}
    recs = {r["item_id"]: r for r in read_jsonl(base / task_name / set_name / f"{arm_id}.jsonl")}
    other_ids = [a.get("id", a["arm"]) for r in exp["runs"] if r["task"] == task_name and r["set"] == set_name for a in r["arms"]
                 if a.get("id", a["arm"]) != arm_id and (base / task_name / set_name / f"{a.get('id', a['arm'])}.jsonl").exists()]
    others = {o: {r["item_id"]: set(r["labels"]) if r["ok"] else set() for r in read_jsonl(base / task_name / set_name / f"{o}.jsonl")} for o in other_ids}
    sigs = {}
    for iid, rec in recs.items():
        s = signals(task, items[iid], rec, {o: others[o].get(iid, set()) for o in others}, spec.get("cases"))
        if s:
            sigs[iid] = s
    engine = llm.Engine(base / "rca" / "responses.jsonl", mode=mode, budget_usd=budget)
    jobs = {}
    for iid, s in sigs.items():
        for p, rev in (("p1", False), ("p2", True)):
            jobs[f"rca|{task_name}|{set_name}|{arm_id}|{iid}|{p}"] = job(task, items[iid], recs[iid], s, rev)
    done = engine.run(jobs)
    rows, cost = [], 0.0
    for iid, s in sigs.items():
        r1, r2 = done[f"rca|{task_name}|{set_name}|{arm_id}|{iid}|p1"], done[f"rca|{task_name}|{set_name}|{arm_id}|{iid}|p2"]
        cost += r1["cost_usd"] + r2["cost_usd"]
        d1 = {(d["label"], d["kind"]): d for d in ((r1["data"] or {}).get("decisions") or [])}
        d2 = {(d["label"], d["kind"]): d for d in ((r2["data"] or {}).get("decisions") or [])}
        for sig in s:
            key = (sig["label"], sig["kind"])
            a, b = d1.get(key), d2.get(key)
            row = {"item_id": iid, **sig, "text": items[iid]["text"], "gold": items[iid]["labels"], "pred": recs[iid]["labels"],
                   "meta": {k: v for k, v in (items[iid].get("meta") or {}).items() if k != "polarity"},
                   "pass1": a, "pass2": b}
            if a and b and a["cause"] == b["cause"]:
                row["cause"], row["agreed"] = a["cause"], True
            else:
                row["cause"], row["agreed"] = "split", False
            rows.append(row)
    n = len(rows)
    agreed = [r for r in rows if r["agreed"]]
    summary = {
        "task": task_name, "set": set_name, "arm": arm_id, "items_with_failures": len(sigs), "decisions": n,
        "agreement": {"k": len(agreed), "n": n},
        "by_cause": dict(Counter(r["cause"] for r in rows).most_common()),
        "by_kind_and_cause": {k: dict(Counter(r["cause"] for r in rows if r["kind"] == k).most_common()) for k in ("false_positive", "miss")},
        "by_label": {l: dict(Counter(r["cause"] for r in rows if r["label"] == l).most_common())
                     for l, _ in Counter(r["label"] for r in rows).most_common()},
        "stable_errors": sum(1 for r in rows if r["same_error_arms"] == r["other_arms"]),
        "cost_usd": round(cost, 6),
    }
    out = {"summary": summary, "decisions": rows}
    (base / "rca").mkdir(parents=True, exist_ok=True)
    stem = f"{task_name}-{set_name}-{arm_id}"
    (base / "rca" / f"{stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    (base / "rca" / f"{stem}.md").write_text(markdown(out), encoding="utf-8", newline="\n")
    return out


def markdown(out: dict) -> str:
    s = out["summary"]
    rows = out["decisions"]
    lines = [f"# Root causes: {s['task']} / {s['set']} / {s['arm']}", "",
             f"{s['decisions']} wrong label decisions on {s['items_with_failures']} items; the two independent passes agree on "
             f"{s['agreement']['k']} of {s['agreement']['n']}. {s['stable_errors']} of the decisions were also wrong in every other arm. "
             f"Cost ${s['cost_usd']:.4f}.", "",
             "| Cause | All | False positives | Misses |", "|---|---|---|---|"]
    for cause in ORDER + ["split"]:
        n = s["by_cause"].get(cause, 0)
        fp = s["by_kind_and_cause"]["false_positive"].get(cause, 0)
        fn = s["by_kind_and_cause"]["miss"].get(cause, 0)
        lines.append(f"| {cause} | {n} | {fp} | {fn} |")
    pairs = Counter(tuple(sorted([str((r.get("pass1") or {}).get("cause")), str((r.get("pass2") or {}).get("cause"))]))
                    for r in rows if not r["agreed"])
    if pairs:
        lines += ["", "## Split decisions: the two causes given", "", "| First | Second | Decisions |", "|---|---|---|"]
        lines += [f"| {a} | {b} | {n} |" for (a, b), n in pairs.most_common()]
    lines += ["", "## By label", "", "| Label | Decisions | " + " | ".join(ORDER + ["split"]) + " |", "|---" * (len(ORDER) + 3) + "|"]
    for label, counts in s["by_label"].items():
        total = sum(counts.values())
        lines.append(f"| {label} | {total} | " + " | ".join(str(counts.get(c, 0)) for c in ORDER + ["split"]) + " |")
    lines += ["", "## Suggested fixes (first pass), grouped by cause", ""]
    for cause in ORDER:
        fixes = [r["pass1"]["fix"] for r in rows if r["cause"] == cause and r.get("pass1")]
        if fixes:
            lines.append(f"### {cause} ({len(fixes)})")
            lines += [f"- {r['label']} ({r['kind'].replace('_', ' ')}, {r['item_id']}): {r['pass1']['fix']}" for r in rows if r["cause"] == cause and r.get("pass1")][:25]
            lines.append("")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment")
    ap.add_argument("--task", required=True)
    ap.add_argument("--set", required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--mode", default="offline", choices=["batch", "direct", "offline"])
    ap.add_argument("--budget", type=float, default=0.4)
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    out = run(Path(a.experiment), a.task, a.set, a.arm, a.mode, a.budget)
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
