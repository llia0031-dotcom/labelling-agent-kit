"""Builds the data the report and the viewer read, from the result files only.

    python tools/report_data.py                      # main + revision (+ rca), the published results
    python tools/report_data.py --main dev1           # a development view of another experiment

Writes
  viewer/data.js      window.LAK = {...}: arms, per-label tables, confusion, slices, failures with root causes,
                      the revision comparison, costs
  eval/numbers.md     every table the evaluation report cites, as markdown (the evidence-check source)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lak.task import get_task  # noqa: E402

RES = ROOT / "results"
ARM_NAMES = {
    "prompt-short": {"zh": "短提示词", "en": "Short prompt"},
    "prompt-rules": {"zh": "整本规则进提示词", "en": "Rulebook in prompt"},
    "agent": {"zh": "Agent：查规则", "en": "Agent: rules"},
    "agent-cases": {"zh": "Agent：查规则和案例", "en": "Agent: rules + cases"},
    "agent-cases-check": {"zh": "Agent：查规则、案例，再自查", "en": "Agent: rules + cases + self-check"},
    "agent-cases-synthetic": {"zh": "Agent：合成案例", "en": "Agent: synthetic cases"},
    "agent-cases-mixed": {"zh": "Agent：真实、合成各半", "en": "Agent: half real, half synthetic"},
}
TASK_NAMES = {"ad_policy": {"zh": "广告政策标签", "en": "Ad policy labels"}, "asap": {"zh": "餐厅点评方面（ASAP）", "en": "Restaurant review aspects (ASAP)"}}
CAUSE_NAMES = {"prompt_defect": {"zh": "提示词缺陷", "en": "Prompt defect"}, "model_capability": {"zh": "模型能力", "en": "Model capability"},
               "rule_conflict": {"zh": "规则冲突", "en": "Rule conflict"}, "sample_distribution": {"zh": "样本分布", "en": "Sample distribution"},
               "label_ambiguity": {"zh": "标签歧义", "en": "Label ambiguity"}, "split": {"zh": "两次归因不一致", "en": "Split"}}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def r4(x):
    return None if x is None else round(x, 4)


def arm_name(arm_id: str, versions: bool = False) -> dict:
    base = arm_id[:-3] if arm_id.endswith("-v2") else arm_id
    name = ARM_NAMES.get(base, {"zh": base, "en": base})
    if not versions:
        return name
    v2 = arm_id.endswith("-v2")
    return {"zh": name["zh"] + ("（第二版）" if v2 else "（第一版）"), "en": name["en"] + (" (v2)" if v2 else " (v1)")}


def arm_row(arm_id: str, u: dict, versions: bool = False) -> dict:
    m, o = u["metrics"], u["ops"]
    d = m.get("decision")
    return {"id": arm_id, "name": arm_name(arm_id, versions),
            "micro": {"f1": r4(m["micro"]["f1"]), "ci": m["micro"]["f1_ci"] and [r4(x) for x in m["micro"]["f1_ci"]],
                      "p": r4(m["micro"]["precision"]), "r": r4(m["micro"]["recall"])},
            "macro": {"f1": r4(m["macro"]["f1"]), "ci": m["macro"]["f1_ci"] and [r4(x) for x in m["macro"]["f1_ci"]]},
            "exact": {"k": m["exact_match"]["k"], "n": m["exact_match"]["n"]},
            "miss": d and {"k": d["miss"]["k"], "n": d["miss"]["n"]}, "fa": d and {"k": d["false_alarm"]["k"], "n": d["false_alarm"]["n"]},
            "cost_per_1k": round(1000 * o["cost_per_item_usd"], 3), "calls": o["calls_per_item"], "tools": o["tool_calls_per_item"],
            "failed": o["failed"], "gate": o["rule_gate_fired"], "repair": o["repair_fired"],
            "check_changed": o["check_changed_items"], "check_items": o["check_items"],
            "labels": [{"label": r["label"], "support": r["support"], "tp": r["tp"], "fp": r["fp"], "fn": r["fn"],
                        "p": r4(r["precision"]), "p_ci": r["precision_ci"] and [r4(x) for x in r["precision_ci"]],
                        "r": r4(r["recall"]), "r_ci": r["recall_ci"] and [r4(x) for x in r["recall_ci"]], "f1": r4(r["f1"])}
                       for r in m["per_label"] if r["support"] or r["predicted"]],
            "confusion": {"rows": u["confusion"]["row_names"], "cols": u["confusion"]["column_names"], "m": u["confusion"]["matrix"],
                          "kinds": u["confusion"]["item_kinds"], "top": u["confusion"]["top_pairs"][:8]},
            "slices": [{"field": g["field"], "slices": [{"value": s["value"], "n": s["n"], "f1": r4(s["micro_f1"]),
                                                         "ci": s.get("micro_f1_ci") and [r4(x) for x in s["micro_f1_ci"]],
                                                         "diff": r4(s["diff"]), "verdict": s["verdict"], "measure": s.get("measure"),
                                                         "exact": s["exact_match"]["k"], "miss": s.get("miss"), "fa": s.get("false_alarm")}
                                                        for s in g["slices"]]} for g in u["slices"]["groups"]]}


def failures(rca: dict, task, zh: dict | None = None) -> list[dict]:
    by_item: dict = {}
    zh = zh or {}
    for n, d in enumerate(rca["decisions"]):
        it = by_item.setdefault(d["item_id"], {"id": d["item_id"], "text": d["text"], "gold": d["gold"], "pred": d["pred"],
                                               "meta": d.get("meta", {}), "decisions": []})
        p = d.get("pass1") or {}
        t = zh.get(str(n), {})
        it["decisions"].append({"label": d["label"], "kind": d["kind"], "cause": d["cause"], "agreed": d["agreed"],
                                "why": p.get("why", ""), "fix": p.get("fix", ""),
                                "why_zh": t.get("why") or "", "fix_zh": t.get("fix") or "", "evidence": d.get("evidence"),
                                "stable": d["same_error_arms"] == d["other_arms"] and d["other_arms"] > 0})
    return list(by_item.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", default="main")
    ap.add_argument("--revision", default="revision")
    ap.add_argument("--set", default="test_a")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    an = load(RES / a.main / "analysis.json")
    if not an:
        print(f"no results/{a.main}/analysis.json")
        return 1
    rev = load(RES / a.revision / "analysis.json")
    data = {"experiment": a.main, "tasks": []}
    for tname, sets in an["tasks"].items():
        set_name = a.set if a.set in sets else next(iter(sets))
        task = get_task(tname)
        units = sets[set_name]
        t = {"id": tname, "name": TASK_NAMES[tname], "set": set_name, "items": next(iter(units.values()))["metrics"]["n_items"],
             "arms": [arm_row(k, u) for k, u in units.items()],
             "comparisons": [{"id": c.get("id"), "a": c["a"], "b": c["b"], "verdict": c.get("verdict", "NOT RUN"),
                              "diff": c["result"] and r4(c["result"]["micro_f1"]["diff"]),
                              "ci": c["result"] and c["result"]["micro_f1"]["diff_ci"] and [r4(x) for x in c["result"]["micro_f1"]["diff_ci"]]}
                             for c in an.get("comparisons", []) if c["task"] == tname],
             "failures": [], "rca": None, "revision": None}
        for f in sorted((RES / a.main / "rca").glob(f"{tname}-{set_name}-*.json")) if (RES / a.main / "rca").exists() else []:
            if f.name.endswith(".zh.json"):
                continue
            r = load(f)
            t["rca"] = r["summary"]
            t["failures"] = failures(r, task, load(f.with_name(f.stem + ".zh.json")))
        if rev and tname in rev["tasks"]:
            t["revision"] = {s: [arm_row(k, u, versions=True) for k, u in arms.items()] for s, arms in rev["tasks"][tname].items()}
            t["revision_comparisons"] = [{"id": c.get("id"), "set": c["set"], "a": c["a"], "b": c["b"], "verdict": c.get("verdict"),
                                          "diff": c["result"] and r4(c["result"]["micro_f1"]["diff"]),
                                          "ci": c["result"] and c["result"]["micro_f1"]["diff_ci"] and [r4(x) for x in c["result"]["micro_f1"]["diff_ci"]],
                                          "a_only": c["result"] and c["result"]["exact_match"]["a_only_right"],
                                          "b_only": c["result"] and c["result"]["exact_match"]["b_only_right"]}
                                         for c in rev.get("comparisons", []) if c["task"] == tname]
        data["tasks"].append(t)
    data["causes"] = CAUSE_NAMES
    (ROOT / "viewer").mkdir(exist_ok=True)
    (ROOT / "viewer" / "data.js").write_text("window.LAK = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
                                             encoding="utf-8", newline="\n")
    print(f"viewer/data.js: {len(data['tasks'])} tasks from results/{a.main}" + (f" and results/{a.revision}" if rev else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
