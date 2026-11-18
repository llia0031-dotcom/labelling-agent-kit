"""Adds up what every stored model answer cost, from its own token usage and pricing (batch or standard).

    python tools/costs.py        # -> results/COSTS.md and results/costs.json

Each results/<run>/responses.jsonl holds one line per answer received; the cost of a line is its tokens at
claude-haiku-5-5's list price (input $0.10, output $0.50 per million tokens; cache writes 1.25x and reads
0.1x the input price), halved for answers that came through the Message Batches API.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lak.llm import cost_of, store_lines  # noqa: E402

PURPOSE = {
    "smoke": "first check of the flow on dev (direct calls)",
    "dev1": "development on dev, first agent design",
    "dev2": "development on dev, retrieval step and tuning",
    "synth-asap": "700 synthetic reviews for the case-library comparison",
    "main": "preregistered arms on test A",
    "main/rca": "root-cause classification, two passes",
    "main/rca (translation)": "Chinese text of the root-cause reasons, for the Chinese viewer",
    "revision": "v1 and v2 on test B, v2 on test A",
}


def main() -> int:
    rows = []
    names = ("responses.jsonl", "responses.jsonl.gz", "translate.jsonl", "translate.jsonl.gz")
    found = {Path(str(f)[:-3]) if f.suffix == ".gz" else f for f in (ROOT / "results").rglob("*.jsonl*") if f.name in names}
    seen: set = set()
    # a run that reuses another run's answers ("reuse" in its experiment file) stores copies of them; each answer is
    # charged once, in the store where it first appears (main is read before revision)
    order = sorted(found, key=lambda f: (f.parent.name == "revision", str(f)))
    for f in order:
        run = f.parent.relative_to(ROOT / "results").as_posix() + (" (translation)" if f.name == "translate.jsonl" else "")
        n = batch = copied = 0
        cost = 0.0
        tok = {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
        for line in store_lines(f):
            if not line.strip():
                continue
            e = json.loads(line)
            # a copy is the very same answer (same request, same batch, same content); the same request sent again
            # in another run is a new answer and was paid for again
            ident = (e["key"], e["hash"], json.dumps(e["response"], sort_keys=True))
            if ident in seen:
                copied += 1
                continue
            seen.add(ident)
            r = e["response"]
            n += 1
            batch += r.get("pricing") == "batch"
            cost += cost_of(r["usage"], r.get("pricing", "batch"))
            for k in tok:
                tok[k] += r["usage"].get(k, 0)
        rows.append({"run": run, "purpose": PURPOSE.get(run, ""), "answers": n, "batch_answers": batch, "copied": copied, "cost_usd": round(cost, 4), **tok})
    total = round(sum(r["cost_usd"] for r in rows), 4)
    (ROOT / "results" / "costs.json").write_text(json.dumps({"runs": rows, "total_usd": total}, indent=1) + "\n", encoding="utf-8", newline="\n")
    lines = ["# Model costs", "", "Summed from the token usage stored with every answer (claude-haiku-5-5 list price; Message Batches answers at half price).", "",
             "| Run | Purpose | Answers | Via batch | Copied from another run, not charged again | Input tokens | Output tokens | USD |", "|---|---|---|---|---|---|---|---|"]
    rows.sort(key=lambda r: r["run"])
    for r in rows:
        lines.append(f"| {r['run']} | {r['purpose']} | {r['answers']:,} | {r['batch_answers']:,} | {r['copied']:,} | "
                     f"{r['input_tokens'] + r['cache_creation_input_tokens'] + r['cache_read_input_tokens']:,} | {r['output_tokens']:,} | {r['cost_usd']:.4f} |")
    lines.append(f"| **total** | | {sum(r['answers'] for r in rows):,} | {sum(r['batch_answers'] for r in rows):,} | {sum(r['copied'] for r in rows):,} | | | **{total:.4f}** |")
    (ROOT / "results" / "COSTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
