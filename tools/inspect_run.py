"""Prints a quick look at one experiment's records: per arm, tool use, tokens, cost and gold vs predicted.

    python tools/inspect_run.py smoke [--items]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lak.task import get_task  # noqa: E402


def main() -> None:
    name = sys.argv[1]
    show_items = "--items" in sys.argv
    base = ROOT / "results" / name
    sys.stdout.reconfigure(encoding="utf-8")
    for task_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        task = get_task(task_dir.name)
        for set_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            gold = {r["id"]: set(r["labels"]) for r in task.items(set_dir.name)}
            for f in sorted(set_dir.glob("*.jsonl")):
                if f.name.endswith(".pred.jsonl"):
                    continue
                recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
                n = len(recs)
                tp = fp = fn = exact = 0
                for r in recs:
                    g, p = gold[r["item_id"]], set(r["labels"])
                    tp += len(g & p); fp += len(p - g); fn += len(g - p); exact += g == p
                inp = sum(r["usage"]["input_tokens"] + r["usage"]["cache_read_input_tokens"] + r["usage"]["cache_creation_input_tokens"] for r in recs) / n
                out = sum(r["usage"]["output_tokens"] for r in recs) / n
                tools = sum(len(r["tool_calls"]) for r in recs) / n
                print(f"{task_dir.name:10} {set_dir.name:7} {f.stem:18} n={n} exact={exact} tp={tp} fp={fp} fn={fn} "
                      f"calls/item={sum(r['calls'] for r in recs) / n:.1f} tools/item={tools:.1f} in={inp:.0f} out={out:.0f} "
                      f"$/item={sum(r['cost_usd'] for r in recs) / n:.5f} failed={sum(1 for r in recs if not r['ok'])}")
                if show_items:
                    for r in recs:
                        g, p = gold[r["item_id"]], set(r["labels"])
                        mark = "OK " if g == p else "XX "
                        tc = ",".join(f"{t['name']}({json.dumps(t['input'], ensure_ascii=False)[:60]})" for t in r["tool_calls"])
                        print(f"   {mark}{r['item_id']}: gold={sorted(g)} pred={sorted(p)} miss={sorted(g - p)} extra={sorted(p - g)} "
                              f"br={json.dumps(r['branches'], ensure_ascii=False)[:120]} tools=[{tc[:200]}] err={r['error']}")


if __name__ == "__main__":
    main()
