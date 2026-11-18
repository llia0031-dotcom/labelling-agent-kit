"""Analysis of one experiment: metrics, confusion, slices, operations and paired comparisons.

    python -m lak.analyze experiments/main.json

Reads results/<name>/<task>/<set>/<arm>.jsonl (written by lak.run) and writes
  results/<name>/analysis.json   everything below, for the report and the viewer
  results/<name>/ANALYSIS.md     the same as tables

All numbers come from the skill scripts (label-metrics, confusion-report, slice-report), so the agent's
evaluation uses exactly the code it ships to other projects.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .task import ROOT, get_task, skill_module

lm = skill_module("label-metrics", "label_metrics.py")
cr = skill_module("confusion-report", "confusion_report.py")
sr = skill_module("slice-report", "slice_report.py")

RESULTS = ROOT / "results"
BOOT = 2000
SEED = 20261118


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def ops(recs: list[dict]) -> dict:
    n = len(recs)
    ok = [r for r in recs if r["ok"]]
    def share(pred) -> float:
        return round(sum(1 for r in recs if pred(r)) / n, 4) if n else 0.0
    tool_names = sorted({t["name"] for r in recs for t in r["tool_calls"]})
    check = [r["branches"]["check"] for r in ok if r["branches"].get("check")]
    ev = [v for r in ok for v in (r.get("evidence_ok") or {}).values()]
    usage = {k: sum(r["usage"].get(k, 0) for r in recs) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}
    return {
        "items": n, "answered": len(ok), "failed": n - len(ok),
        "errors": sorted({str(r["error"])[:80] for r in recs if not r["ok"]}),
        "calls_per_item": round(sum(r["calls"] for r in recs) / n, 3) if n else 0,
        "tool_rounds_per_item": round(sum(r["tool_rounds"] for r in recs) / n, 3) if n else 0,
        "tool_calls_per_item": round(sum(len(r["tool_calls"]) for r in recs) / n, 3) if n else 0,
        "items_using_tool": {t: share(lambda r, t=t: any(c["name"] == t for c in r["tool_calls"])) for t in tool_names},
        "rule_gate_fired": sum(1 for r in recs if r["branches"].get("rule_gate")),
        "repair_fired": sum(1 for r in recs if r["branches"].get("repair")),
        "check_items": len(check),
        "check_changed_items": sum(1 for c in check if c.get("added") or c.get("dropped")),
        "check_added_labels": sum(len(c.get("added", [])) for c in check),
        "check_dropped_labels": sum(len(c.get("dropped", [])) for c in check),
        "check_hinted_labels": sum(len(c.get("hinted", [])) for c in check),
        "evidence_exact": {"k": sum(ev), "n": len(ev)},
        "cost_usd": round(sum(r["cost_usd"] for r in recs), 6),
        "cost_per_item_usd": round(sum(r["cost_usd"] for r in recs) / n, 7) if n else 0,
        "tokens": usage,
    }


def analyse_unit(task, set_name: str, recs: list[dict], labels: list[str]) -> dict:
    items = {r["id"]: r for r in task.items(set_name)}
    order = [r["item_id"] for r in recs]
    gold = [frozenset(items[i]["labels"]) for i in order]
    pred = [frozenset(r["labels"]) if r["ok"] else frozenset() for r in recs]
    metrics = lm.summarise(gold, pred, labels, BOOT, SEED)
    gold_rows = [items[i] for i in order]
    pred_rows = [{"id": r["item_id"], "labels": r["labels"] if r["ok"] else []} for r in recs]
    conf = cr.build(gold_rows, pred_rows, labels, top=15, examples=6)
    cfg = task.config
    slices = sr.build(gold_rows, pred_rows, cfg.get("slices", []), cfg.get("length_field"), True, boot=1000, seed=SEED, min_n=20)
    return {"metrics": metrics, "confusion": conf, "slices": slices, "ops": ops(recs)}


def run(exp_path: Path) -> dict:
    exp = json.loads(Path(exp_path).read_text(encoding="utf-8"))
    base = RESULTS / exp["name"]
    out = {"experiment": exp["name"], "tasks": {}, "comparisons": []}
    preds: dict = {}
    for run_ in exp["runs"]:
        tname, set_name = run_["task"], run_["set"]
        for spec in run_["arms"]:
            arm_id = spec.get("id", spec["arm"])
            f = base / tname / set_name / f"{arm_id}.jsonl"
            if not f.exists():
                continue
            task = get_task(tname, spec.get("rules_file", "rules.json"))
            labels = get_task(tname).all_labels
            recs = read_jsonl(f)
            unit = analyse_unit(task, set_name, recs, labels)
            out["tasks"].setdefault(tname, {}).setdefault(set_name, {})[arm_id] = unit
            items = {r["id"]: r for r in task.items(set_name)}
            preds[(tname, set_name, arm_id)] = {r["item_id"]: (frozenset(r["labels"]) if r["ok"] else frozenset()) for r in recs}
            preds[(tname, set_name, "_gold")] = {i: frozenset(items[i]["labels"]) for i in items}
    base.mkdir(parents=True, exist_ok=True)
    for c in exp.get("comparisons", []):
        key_a, key_b = (c["task"], c["set"], c["a"]), (c["task"], c["set"], c["b"])
        if key_a not in preds or key_b not in preds:
            out["comparisons"].append({**c, "result": None, "note": "NOT RUN"})
            continue
        gold_map = preds[(c["task"], c["set"], "_gold")]
        ids = [i for i in preds[key_a] if i in preds[key_b]]
        res = lm.compare([gold_map[i] for i in ids], [preds[key_a][i] for i in ids], [preds[key_b][i] for i in ids],
                         get_task(c["task"]).all_labels, BOOT, SEED)
        lo_hi = res["micro_f1"]["diff_ci"]
        verdict = "no measured difference"
        if lo_hi and lo_hi[0] > 0:
            verdict = "B better"
        elif lo_hi and lo_hi[1] < 0:
            verdict = "B worse"
        out["comparisons"].append({**c, "result": res, "verdict": verdict})
    (base / "analysis.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    (base / "ANALYSIS.md").write_text(markdown(out), encoding="utf-8", newline="\n")
    return out


def f3(x) -> str:
    return "–" if x is None else f"{x:.3f}"


def ci2(ci) -> str:
    return "" if not ci else f" [{ci[0]:.2f}–{ci[1]:.2f}]"


def markdown(a: dict) -> str:
    lines = [f"# Analysis: {a['experiment']}", ""]
    for tname, sets in a["tasks"].items():
        for set_name, arms in sets.items():
            lines += [f"## {tname} / {set_name}", "",
                      "| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |",
                      "|---|---|---|---|---|---|---|---|---|---|---|"]
            for arm_id, u in arms.items():
                m, o = u["metrics"], u["ops"]
                d = m.get("decision")
                miss = f"{d['miss']['k']}/{d['miss']['n']}" if d else "–"
                fa = f"{d['false_alarm']['k']}/{d['false_alarm']['n']}" if d else "–"
                em = m["exact_match"]
                lines.append(f"| {arm_id} | {m['n_items']} | {f3(m['micro']['f1'])}{ci2(m['micro']['f1_ci'])} | {f3(m['macro']['f1'])}{ci2(m['macro']['f1_ci'])} | "
                             f"{em['k']}/{em['n']} | {miss} | {fa} | {o['calls_per_item']:.2f} | {o['tool_calls_per_item']:.2f} | "
                             f"{1000 * o['cost_per_item_usd']:.2f} | {o['failed']} |")
            lines.append("")
    if a["comparisons"]:
        lines += comparison_lines(a)
    lines += ["", "# Details per arm", ""]
    for tname, sets in a["tasks"].items():
        for set_name, arms in sets.items():
            for arm_id, u in arms.items():
                lines += [f"## {tname} / {set_name} / {arm_id}", ""]
                lines.append(lm.to_markdown(u["metrics"], None, f"{tname} / {set_name} / {arm_id}"))
                o = u["ops"]
                lines += [f"Operations: {o['answered']}/{o['items']} answered; {o['calls_per_item']:.2f} calls and "
                          f"{o['tool_calls_per_item']:.2f} tool calls per item; rule gate {o['rule_gate_fired']}, quote repair {o['repair_fired']}, "
                          f"self-check changed {o['check_changed_items']} of {o['check_items']} items "
                          f"(+{o['check_added_labels']} / −{o['check_dropped_labels']} labels); exact quotes {o['evidence_exact']['k']}/{o['evidence_exact']['n']}; "
                          f"cost ${o['cost_usd']:.4f} (${1000 * o['cost_per_item_usd']:.3f} per 1,000 items)."
                          + (" Items on which each tool was called: " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in o["items_using_tool"].items()) + "." if o["items_using_tool"] else ""), ""]
                conf = u["confusion"]
                k = conf["item_kinds"]
                lines += [f"Confusion: exact {k['exact']}, under-labelled {k['under-labelled']}, over-labelled {k['over-labelled']}, swapped {k['swapped']}.", "",
                          "| Gold | Predicted | Count | Kind |", "|---|---|---|---|"]
                lines += [f"| {p['gold']} | {p['predicted']} | {p['count']} | {p['kind']} |" for p in conf["top_pairs"][:10]]
                lines += ["", sr.to_markdown(u["slices"]), ""]
    return "\n".join(lines) + "\n"


def comparison_lines(a: dict) -> list[str]:
    lines = []
    if a["comparisons"]:
        lines += ["## Comparisons (B − A, micro F1, paired bootstrap 95%)", "", "| Id | Task / set | A | B | Δ micro F1 | Δ macro F1 | McNemar p (exact match) | Verdict |", "|---|---|---|---|---|---|---|---|"]
        for c in a["comparisons"]:
            r = c.get("result")
            if not r:
                lines.append(f"| {c.get('id', '')} | {c['task']} / {c['set']} | {c['a']} | {c['b']} | NOT RUN | | | |")
                continue
            mi, ma = r["micro_f1"], r["macro_f1"]
            p = r["exact_match"]["mcnemar_exact_p"]
            lines.append(f"| {c.get('id', '')} | {c['task']} / {c['set']} | {c['a']} | {c['b']} | {mi['diff']:+.3f}{_ci_signed(mi['diff_ci'])} | "
                         f"{ma['diff']:+.3f}{_ci_signed(ma['diff_ci'])} | {'–' if p is None else f'{p:.3f}'} | {c['verdict']} |")
    return lines + [""]


def _ci_signed(ci) -> str:
    return "" if not ci else f" [{ci[0]:+.3f}, {ci[1]:+.3f}]"


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = run(Path((argv or sys.argv[1:])[0]))
    print(markdown(a))
    return 0


if __name__ == "__main__":
    sys.exit(main())
