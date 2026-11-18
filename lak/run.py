"""Runs one experiment: every task x item set x arm in experiments/<name>.json.

    python -m lak.run experiments/main.json --mode batch --budget 1.5
    python -m lak.run experiments/main.json --mode offline          # rebuild from the stored answers

An experiment file:
    {"name": "main", "frozen": {"tasks/ad_policy/rules.json": "<sha12>", "prompts/v1.json": "<sha12>", ...},
     "runs": [{"task": "ad_policy", "set": "test_a", "arms": [{"arm": "prompt-short"}, {"arm": "agent", "id": "agent"}]}]}

"frozen" lists the fingerprints of the task files the preregistration fixed; a run refuses to start when
a file has changed. "reuse": ["main"] lets a run take identical requests' answers from another run's store. Answers are stored in results/<name>/responses.jsonl, one record per item and arm in
results/<name>/<task>/<set>/<arm>.jsonl, and the predictions in the same folder as <arm>.pred.jsonl.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import llm
from .agent import arm_from, label_job
from .task import ROOT, get_task, sha12

RESULTS = ROOT / "results"


def check_frozen(exp: dict) -> list[str]:
    """Compares the fingerprints listed under "frozen" (paths relative to the project folder) with the files."""
    problems = []
    for rel, want in (exp.get("frozen") or {}).items():
        path = ROOT / rel
        got = sha12(path) if path.exists() else "missing"
        if got != want:
            problems.append(f"{rel}: {got} (preregistered {want})")
    return problems


def freeze_list(task_names: list[str], prompt_versions: list[str]) -> dict:
    """The fingerprints a preregistration fixes: every task file the runs read, and the prompt files."""
    out = {}
    for t in task_names:
        task = get_task(t)
        for f, h in task.fingerprints().items():
            out[f"tasks/{t}/{f}"] = h
    for v in prompt_versions:
        out[f"prompts/{v}.json"] = sha12(ROOT / "prompts" / f"{v}.json")
    return out


def plan(exp: dict, only_task: str | None = None) -> list[dict]:
    out = []
    for run in exp["runs"]:
        if only_task and run["task"] != only_task:
            continue
        for spec in run["arms"]:
            arm = arm_from(spec)
            task = get_task(run["task"], arm.rules_file)
            items = task.items(run["set"])
            if run.get("limit"):
                items = items[: run["limit"]]
            out.append({"task": task, "set": run["set"], "arm": arm, "items": items})
    return out


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


def run(exp_path: Path, mode: str = "offline", budget: float | None = None, only_task: str | None = None,
        fake=None, log=print, poll: float = 20.0) -> dict:
    exp = json.loads(Path(exp_path).read_text(encoding="utf-8"))
    problems = check_frozen(exp)
    if problems:
        raise SystemExit("frozen files changed since the preregistration:\n  " + "\n  ".join(problems))
    out_dir = RESULTS / exp["name"]
    reuse = [RESULTS / name / "responses.jsonl" for name in exp.get("reuse", [])]
    engine = llm.Engine(out_dir / "responses.jsonl", mode=mode, fake=fake, log=log, budget_usd=budget, poll_seconds=poll, reuse=reuse)
    units = plan(exp, only_task)
    jobs, where = {}, {}
    for u in units:
        for it in u["items"]:
            key = f"{u['task'].name}|{u['set']}|{u['arm'].id}|{it['id']}"
            jobs[key] = label_job(u["task"], it, u["arm"])
            where[key] = u
    log(f"{exp['name']}: {len(units)} task x set x arm units, {len(jobs)} item runs, mode {mode}")
    t0 = time.time()
    done = engine.run(jobs)
    summary = {"experiment": exp["name"], "mode": mode, "units": []}
    for u in units:
        recs = [done[f"{u['task'].name}|{u['set']}|{u['arm'].id}|{it['id']}"] for it in u["items"]]
        base = out_dir / u["task"].name / u["set"]
        write_jsonl(base / f"{u['arm'].id}.jsonl", recs)
        write_jsonl(base / f"{u['arm'].id}.pred.jsonl", [{"id": r["item_id"], "labels": r["labels"] if r["ok"] else None} for r in recs])
        summary["units"].append({"task": u["task"].name, "set": u["set"], "arm": u["arm"].id, "items": len(recs),
                                 "failed": sum(1 for r in recs if not r["ok"]),
                                 "calls": sum(r["calls"] for r in recs),
                                 "cost_usd": round(sum(r["cost_usd"] for r in recs), 5)})
    summary["cost_usd"] = round(sum(x["cost_usd"] for x in summary["units"]), 5)
    summary["answers_sent_this_run"] = engine.sent
    summary["answers_reused"] = engine.reused
    summary["batches_this_run"] = engine.batches
    summary["minutes"] = round((time.time() - t0) / 60, 1)
    (out_dir / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    log(f"done: cost of stored answers ${summary['cost_usd']:.4f}; sent {engine.sent} new requests (${engine.spent:.4f}), reused {engine.reused}")
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment")
    ap.add_argument("--mode", choices=["batch", "direct", "offline"], default="offline")
    ap.add_argument("--budget", type=float, help="stop sending once this much (USD) was spent in this run")
    ap.add_argument("--task")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    run(Path(a.experiment), a.mode, a.budget, a.task)
    return 0


if __name__ == "__main__":
    sys.exit(main())
