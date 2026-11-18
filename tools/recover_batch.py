"""Rebuilds the batch journal of an experiment whose first round was sent but not recorded.

    python tools/recover_batch.py experiments/dev1.json --list            # recent batches on the account
    python tools/recover_batch.py experiments/dev1.json --batch msgbatch_...  # write the journal for that batch

The first round's requests are rebuilt exactly as lak.run builds them (same order, so custom ids r0, r1, ...
map to the same requests). The batch is used only if its request count matches; nothing is sent.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lak import llm  # noqa: E402
from lak.agent import label_job  # noqa: E402
from lak.run import RESULTS, plan  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--batch")
    a = ap.parse_args()
    c = llm.client()
    if a.list:
        for n, b in enumerate(c.messages.batches.list(limit=8)):
            if n >= 8:
                break
            rc = b.request_counts
            print(b.id, b.created_at, b.processing_status, "requests:", rc.processing + rc.succeeded + rc.errored + rc.canceled + rc.expired)
        return 0
    exp = json.loads(Path(a.experiment).read_text(encoding="utf-8"))
    engine = llm.Engine(RESULTS / exp["name"] / "responses.jsonl", mode="offline", log=lambda *_: None)
    jobs = {}
    for u in plan(exp):
        for it in u["items"]:
            jobs[f"{u['task'].name}|{u['set']}|{u['arm'].id}|{it['id']}"] = label_job(u["task"], it, u["arm"])
    first = {}
    for name, gen in jobs.items():
        params = engine.params(next(gen))
        first[name] = (f"{name}#1", llm.request_hash(params))
    b = c.messages.batches.retrieve(a.batch)
    rc = b.request_counts
    total = rc.processing + rc.succeeded + rc.errored + rc.canceled + rc.expired
    if total != len(first):
        print(f"batch has {total} requests, the first round has {len(first)}: not the same batch")
        return 1
    names = list(first)
    entry = {"batch": a.batch, "requests": {f"r{n}": list(first[name]) for n, name in enumerate(names)}}
    with engine.journal.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"journal written: {len(names)} requests -> {a.batch} ({b.processing_status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
