"""Data acceptance checks: the rules in DATA_ACCEPTANCE.md, run on every item set and case library.

    python -m lak.accept                 # all tasks -> results/acceptance.json and results/ACCEPTANCE.md

Each check is blocking (the file is not used until it passes) or a warning (reported with the numbers).
Reference for length and label share: the task's real data (ASAP: the real case library drawn from the
training split; ad policy: the written test ads), so a synthetic library is compared with real data.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from .task import ROOT, dig, get_task, label_rules, read_jsonl

CJK = re.compile(r"[一-鿿]")
THRESHOLDS = {"near_dup_jaccard": 0.6, "near_dup_share": 0.01, "leak_jaccard": 0.3, "length_within": 0.95,
              "label_share_diff": 0.10, "cue_precision": 0.95, "cue_conflict_share": 0.05}


def grams(text: str, n: int) -> set[str]:
    t = re.sub(r"\s+", "", text.lower())
    return {t[i:i + n] for i in range(max(1, len(t) - n + 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def is_chinese(text: str) -> bool:
    return len(CJK.findall(text)) >= 0.3 * len(re.sub(r"\s", "", text))


def lang_of(row: dict) -> str | None:
    return dig(row, "meta.lang") or row.get("lang")


def pct(values: list[int], q: float) -> int:
    s = sorted(values)
    return s[min(len(s) - 1, int(q * (len(s) - 1)))]


def check(rows: list[dict], task, reference: list[dict] | None, tests: dict[str, list[dict]], cues: dict | None) -> dict:
    out = {"rows": len(rows), "checks": []}

    def add(code: str, name: str, blocking: bool, passed: bool, detail: str, examples=None) -> None:
        out["checks"].append({"code": code, "name": name, "blocking": blocking, "passed": passed, "detail": detail,
                              "examples": (examples or [])[:5]})

    if not rows:
        add("A1", "schema: unique id, text, label list", True, False, "the file has no rows")
        out["blocking_failed"], out["warnings"], out["accepted"] = ["A1"], [], False
        return out
    ids = [r.get("id") for r in rows]
    bad_schema =[r.get("id") for r in rows if not r.get("id") or not isinstance(r.get("text"), str) or not r["text"].strip()
                  or not isinstance(r.get("labels"), list) or not all(isinstance(x, str) for x in r["labels"])]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    add("A1", "schema: unique id, text, label list", True, not bad_schema and not dup_ids,
        f"{len(bad_schema)} malformed rows, {len(dup_ids)} duplicate ids", bad_schema + dup_ids)

    book = task.book
    known = {l["id"]: l for l in book["labels"]}
    unknown, out_of_scope = [], []
    for r in rows:
        for l in r.get("labels", []):
            if l not in known:
                unknown.append(r["id"])
            elif not label_rules.in_scope(known[l], lang_of(r) if task.config.get("scope_field") else None):
                out_of_scope.append(r["id"])
    add("A2", "labels exist in the rulebook and fit the item's scope", True, not unknown and not out_of_scope,
        f"{len(unknown)} rows with unknown labels, {len(out_of_scope)} with a label outside the item's scope", unknown + out_of_scope)

    empties = [r["id"] for r in rows if not r.get("labels")]
    allowed = book.get("empty_allowed", True)
    add("A3", "empty-label rows only where the rulebook allows them", True, allowed or not empties,
        f"{len(empties)} rows without a label; rulebook {'allows' if allowed else 'does not allow'} them")

    default_lang = task.config.get("rule_lang")
    wrong_lang = [r["id"] for r in rows if (lang_of(r) or default_lang) in ("zh", "en")
                  and is_chinese(r["text"]) != ((lang_of(r) or default_lang) == "zh")]
    add("A4", "text is in the stated language", True, not wrong_lang, f"{len(wrong_lang)} rows in another language", wrong_lang)

    texts = [" ".join(r["text"].split()) for r in rows]
    exact = [i for i, c in Counter(texts).items() if c > 1]
    g5 = [grams(t, 5) for t in texts]
    near = set()
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if jaccard(g5[i], g5[j]) >= THRESHOLDS["near_dup_jaccard"]:
                near.add(rows[j]["id"])
    share = len(near) / len(rows) if rows else 0
    add("A5", "no exact duplicates; near duplicates at most 1%", True, not exact and share <= THRESHOLDS["near_dup_share"],
        f"{len(exact)} exact duplicate texts; {len(near)} near duplicates ({100 * share:.1f}%, character 5-gram Jaccard >= 0.6)", sorted(near))

    leaks = []
    for name, test_rows in tests.items():
        t8 = [(t["id"], grams(t["text"], 8)) for t in test_rows]
        for r in rows:
            g8 = grams(r["text"], 8)
            for tid, tg in t8:
                if tid != r["id"] and jaccard(g8, tg) >= THRESHOLDS["leak_jaccard"]:
                    leaks.append(f"{r['id']}~{name}:{tid}")
    add("A6", "no overlap with the frozen test sets", True, not leaks,
        f"{len(leaks)} pairs with character 8-gram Jaccard >= 0.3 against {', '.join(tests) or 'no test set'}", leaks)

    missing_src = [r["id"] for r in rows if not (dig(r, "meta.source") or r.get("source"))]
    add("A7", "every row states where it comes from", True, not missing_src, f"{len(missing_src)} rows without a source", missing_src)

    if reference:
        lens = [len(r["text"]) for r in reference]
        lo, hi = pct(lens, 0.01), pct(lens, 0.99)
        inside = sum(1 for r in rows if lo <= len(r["text"]) <= hi) / len(rows)
        add("A8", "length within the real data's 1st-99th percentile for 95% of rows", False, inside >= THRESHOLDS["length_within"],
            f"{100 * inside:.1f}% within {lo}-{hi} characters")
        ref_share = {l: sum(1 for r in reference if l in r["labels"]) / len(reference) for l in known}
        own = {l: sum(1 for r in rows if l in r["labels"]) / len(rows) for l in known}
        diffs = sorted(((abs(own[l] - ref_share[l]), l) for l in known), reverse=True)
        add("A9", "each label's share within 10 points of the real data", False, diffs[0][0] <= THRESHOLDS["label_share_diff"],
            "largest gaps: " + ", ".join(f"{l} {100 * own[l]:.0f}% vs {100 * ref_share[l]:.0f}%" for _, l in diffs[:3]))
    if cues:
        strong = {l: [c["phrase"] for c in v["cues"] if c["precision"] >= THRESHOLDS["cue_precision"]] for l, v in cues.items()}
        conflict = []
        for r in rows:
            hit = [l for l, ps in strong.items() if l not in r["labels"] and any(p in r["text"] for p in ps)]
            if hit:
                conflict.append(f"{r['id']}:{'/'.join(hit)}")
        share = len(conflict) / len(rows)
        add("A10", "strong cue of a label that the row does not carry in at most 5% of rows", False, share <= THRESHOLDS["cue_conflict_share"],
            f"{len(conflict)} rows ({100 * share:.1f}%) contain a phrase whose training-split precision for a missing label is >= 0.95", conflict)
    out["blocking_failed"] = [c["code"] for c in out["checks"] if c["blocking"] and not c["passed"]]
    out["warnings"] = [c["code"] for c in out["checks"] if not c["blocking"] and not c["passed"]]
    out["accepted"] = not out["blocking_failed"]
    return out


def run() -> dict:
    report = {"thresholds": THRESHOLDS, "files": []}
    for tname in sorted(d.name for d in (ROOT / "tasks").iterdir() if (d / "task.json").exists()):
        task = get_task(tname)
        cfg = task.config
        sets = {k: task.items(k) for k in cfg["sets"]}
        cues_path = task.dir / "cues.json"
        cues = json.loads(cues_path.read_text(encoding="utf-8"))["labels"] if cues_path.exists() else None
        # real reference data: the task's real case library if it has one, else its test items
        real = cfg["case_libraries"].get("real")
        reference = read_jsonl(task.dir / real) if isinstance(real, str) else [r for k in ("test_a", "test_b") for r in sets.get(k, [])]
        files = [(k, f, sets[k]) for k, f in cfg["sets"].items()]
        for lib, spec in cfg["case_libraries"].items():
            if isinstance(spec, str) and (task.dir / spec).exists():
                files.append((f"cases:{lib}", spec, read_jsonl(task.dir / spec)))
        for kind, fname, rows in files:
            tests = {k: v for k, v in sets.items() if k in ("test_a", "test_b") and k != kind}
            if kind == "test_a":
                tests = {"test_b": sets["test_b"], "dev": sets["dev"]}
            elif kind == "test_b":
                tests = {"test_a": sets["test_a"], "dev": sets["dev"]}
            res = check(rows, task, reference if kind.startswith("cases") or kind == "dev" else None, tests,
                        cues if kind.startswith("cases") or tname == "asap" else None)
            report["files"].append({"task": tname, "set": kind, "file": fname, **res})
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "results" / "ACCEPTANCE.md").write_text(markdown(report), encoding="utf-8", newline="\n")
    return report


def markdown(rep: dict) -> str:
    lines = ["# Data acceptance", "", "Rules and thresholds: DATA_ACCEPTANCE.md. B = blocking, W = warning.", ""]
    for f in rep["files"]:
        verdict = "accepted" if f["accepted"] else "NOT accepted (" + ", ".join(f["blocking_failed"]) + ")"
        lines += [f"## {f['task']} / {f['set']} ({f['file']}, {f['rows']} rows): {verdict}", "", "| Check | | Result | Detail |", "|---|---|---|---|"]
        for c in f["checks"]:
            lines.append(f"| {c['code']} {c['name']} | {'B' if c['blocking'] else 'W'} | {'pass' if c['passed'] else 'FAIL' if c['blocking'] else 'warn'} | {c['detail']} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r = run()
    for f in r["files"]:
        print(f"{f['task']:10} {f['set']:16} {f['rows']:4} accepted={f['accepted']} blocking_failed={f['blocking_failed']} warnings={f['warnings']}")
