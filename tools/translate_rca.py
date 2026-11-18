"""Chinese versions of the root-cause explanations, for the Chinese results viewer only.

The root-cause step writes its reasons and suggested fixes in English. The Chinese viewer shows them in Chinese,
so this step translates the first pass's "why" and "fix" of every decision, 20 decisions per request, through the
Message Batches API (claude-haiku-5-5). Label ids, Chinese quotes and code stay as they are. The counts and
causes are not touched; the English originals stay in the root-cause files.

    python tools/translate_rca.py --mode batch      # results/main/rca/<task>-<set>-<arm>.zh.json
    python tools/translate_rca.py                   # offline: rebuild from the stored answers
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lak import llm  # noqa: E402

RCA = ROOT / "results" / "main" / "rca"
CHUNK = 20
SYSTEM = ("Translate each entry's \"why\" and \"fix\" into concise, natural simplified Chinese for a results page. Keep label ids "
          "(such as Price#Level or Ambience#Noise), cause names, quoted Chinese text, numbers and code exactly as they are. Do not add or "
          "drop content. Answer with JSON: {\"items\": [{\"i\": <the entry's i>, \"why\": \"...\", \"fix\": \"...\"}]}.")
SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "i": {"type": "integer"}, "why": {"type": "string"}, "fix": {"type": "string"}}, "required": ["i", "why", "fix"], "additionalProperties": False}}},
    "required": ["items"], "additionalProperties": False}


def job(entries: list[dict]):
    resp = yield {"system": SYSTEM, "messages": [{"role": "user", "content": json.dumps(entries, ensure_ascii=False)}],
                  "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}}}
    data, why = llm.final_json(resp)
    cost = llm.cost_of(resp["usage"], resp.get("pricing", "batch")) if "usage" in resp else 0.0
    return {"items": (data or {}).get("items", []), "error": why, "cost_usd": cost}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="offline", choices=["batch", "direct", "offline"])
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    engine = llm.Engine(RCA / "translate.jsonl", mode=a.mode, budget_usd=0.1)
    files = sorted(p for p in RCA.glob("*.json") if not p.name.endswith(".zh.json"))
    jobs, plan = {}, {}
    for f in files:
        rows = json.loads(f.read_text(encoding="utf-8"))["decisions"]
        entries = [{"i": n, "why": (r.get("pass1") or {}).get("why", ""), "fix": (r.get("pass1") or {}).get("fix", "")} for n, r in enumerate(rows)]
        for k in range(0, len(entries), CHUNK):
            key = f"zh|{f.stem}|{k}"
            jobs[key] = job(entries[k:k + CHUNK])
            plan[key] = (f, entries[k:k + CHUNK])
    done = engine.run(jobs)
    out: dict = {}
    cost = 0.0

    def collect(done_jobs, plan_map):
        nonlocal cost
        for key, res in done_jobs.items():
            f, entries = plan_map[key]
            cost += res["cost_usd"]
            got = {x["i"]: x for x in res["items"]}
            for e in entries:
                if got.get(e["i"], {}).get("why"):
                    out.setdefault(f, {})[e["i"]] = {"why": got[e["i"]]["why"], "fix": got[e["i"]].get("fix", "")}
                else:
                    out.setdefault(f, {}).setdefault(e["i"], {"why": "", "fix": ""})

    collect(done, plan)
    # a long chunk can be cut off; the entries left without a translation go again, 5 per request, then one by one
    for tag, size in (("zh2", 5), ("zh3", 1)):
        jobs2, plan2 = {}, {}
        for f, entries in plan.values():
            missing = [e for e in entries if not out.get(f, {}).get(e["i"], {}).get("why")]
            for k in range(0, len(missing), size):
                key = f"{tag}|{f.stem}|{missing[k]['i']}"
                jobs2[key] = job(missing[k:k + size])
                plan2[key] = (f, missing[k:k + size])
        if jobs2:
            collect(engine.run(jobs2), plan2)
    for f, m in out.items():
        missing = sum(1 for v in m.values() if not v["why"])
        (RCA / f"{f.stem}.zh.json").write_text(json.dumps({str(k): v for k, v in sorted(m.items())}, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")
        print(f"{f.stem}.zh.json: {len(m)} decisions, {missing} without a translation")
    print(f"cost ${cost:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
