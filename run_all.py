"""One command for the whole evaluation.

    python run_all.py --offline        # rebuild every result from the stored answers, then run the tests (no key, no cost)
    python run_all.py                  # the same, sending only the requests whose answers are not stored (Message Batches)
    python run_all.py --stages accept,main,analyze

Stages, in order:
  accept    data acceptance checks on every item set and case library      results/ACCEPTANCE.md
  dev       the two development runs, re-analysed from their stored records results/dev1/, results/dev2/
  main      the preregistered arms on test A                               results/main/
  rca       root-cause analysis of the best v1 arm of each task            results/main/rca/
  revision  v2 against the best v1 arm on test B, and v2 on test A          results/revision/
  report    costs, the numbers the report cites, data for the viewer,   results/COSTS.md, eval/numbers.md, viewer/data.js,
            then the evidence check of the report and the READMEs        eval/claims.json, eval/claims_check.json
  tests     the offline tests

The API key is read from the file named by EVAL_ENV_FILE (a line ANTHROPIC_API_KEY=...), never from the shell.
Every stage skips work whose answers are stored, so an interrupted run can be started again.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

STAGES = ["accept", "dev", "main", "rca", "revision", "report", "tests"]
BUDGET = {"main": 1.6, "rca": 0.4, "revision": 1.2}


def best_arm(analysis: dict, task: str, set_name: str, arms: list[str]) -> str:
    """Highest micro F1; on a tie, the cheaper arm (the preregistered rule)."""
    units = analysis["tasks"][task][set_name]
    cands = [(units[a]["metrics"]["micro"]["f1"] or 0.0, -units[a]["ops"]["cost_per_item_usd"], a) for a in arms if a in units]
    return max(cands)[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use stored answers only; fail if one is missing")
    ap.add_argument("--stages", default=",".join(STAGES))
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    mode = "offline" if a.offline else "batch"
    stages = [s for s in a.stages.split(",") if s]
    from lak import accept, analyze, rca, run

    if "accept" in stages:
        rep = accept.run()
        bad = [f"{f['task']}/{f['set']}" for f in rep["files"] if not f["accepted"]]
        print(f"[accept] {len(rep['files'])} files, not accepted: {bad or 'none'}")
        if bad:
            return 1
    if "dev" in stages:
        # the development runs are re-analysed from their stored records; dev1 used an earlier design that the
        # current code no longer builds, so its requests are not replayed
        for name in ("dev1", "dev2"):
            if (ROOT / "results" / name).exists():
                analyze.run(ROOT / "experiments" / f"{name}.json")
        print("[dev] results/dev1/ANALYSIS.md, results/dev2/ANALYSIS.md")
    main_exp = ROOT / "experiments" / "main.json"
    if "main" in stages:
        run.run(main_exp, mode, BUDGET["main"])
        analyze.run(main_exp)
        print("[main] done: results/main/ANALYSIS.md")
    if "rca" in stages:
        an = json.loads((ROOT / "results" / "main" / "analysis.json").read_text(encoding="utf-8"))
        v1_arms = ["prompt-short", "prompt-rules", "agent", "agent-cases", "agent-cases-check"]
        for task in ("ad_policy", "asap"):
            arm = best_arm(an, task, "test_a", v1_arms)
            out = rca.run(main_exp, task, "test_a", arm, mode, BUDGET["rca"] / 2)
            print(f"[rca] {task}: best v1 arm {arm}; {out['summary']['decisions']} wrong decisions; {out['summary']['by_cause']}")
    rev_exp = ROOT / "experiments" / "revision.json"
    if "revision" in stages and rev_exp.exists():
        run.run(rev_exp, mode, BUDGET["revision"])
        analyze.run(rev_exp)
        print("[revision] done: results/revision/ANALYSIS.md")
    if "report" in stages:
        steps = [["first_turn.py", name] for name in ("dev1", "dev2", "main")
                 if any((ROOT / "results" / name / f).exists() for f in ("responses.jsonl", "responses.jsonl.gz"))]
        steps += [["translate_rca.py"], ["costs.py"], ["report_numbers.py"], ["report_data.py"], ["check_claims.py"]]
        for step in steps:
            r = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "tools" / step[0]), *step[1:]], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            if r.returncode:
                print(r.stdout[-2000:], r.stderr[-2000:])
                return r.returncode
        print("[report] eval/numbers.md, results/COSTS.md, viewer/data.js rebuilt; every number in the report and the READMEs found in the result files (eval/claims_check.json)")
    if "tests" in stages:
        r = subprocess.run([sys.executable, "-X", "utf8", "-B", "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
