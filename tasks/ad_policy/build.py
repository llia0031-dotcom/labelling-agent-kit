"""Builds the ad-policy task files from Policy Model Lab's public data (same author, MIT).

Source files (data_public/ of https://github.com/llia0031-dotcom/policy-model-lab):
  text_tests.jsonl   264 ad texts with labels fixed when each ad was written: Grounded Review's public
                     items (dev, test, hard, memory) and the caption plus on-screen words of the 96 video ads
  synth_train.jsonl  1,529 synthetic ads (labels set in each generation request, filtered against the test items)
  synth_val.jsonl    191 synthetic ads from held-out product and style buckets

    python tasks/ad_policy/build.py [--src PATH_TO_data_public]     (default: $LAK_POLICY_LAB_DATA or data/policy-model-lab)

Writes (seed 20261118):
  items_dev.jsonl     the 24 Grounded Review dev items, two video items that were opened while checking the
                      file format, and 60 synthetic validation ads: development and tuning
  items_test_a.jsonl  119 of the other 238 written ads: all arms; failures are analysed
  items_test_b.jsonl  the other 119: untouched until the revised version
  cases_synth.jsonl   600 synthetic training ads: the case library
Test A and B are split within each stratum (source x language x whether the ad has a label). Near-duplicate
ads (character 8-gram Jaccard >= 0.3, data acceptance check A6) are then kept in one set: the later set's
item moves to the earlier set (dev, test A, test B), see tasks/keep_together.py.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from keep_together import keep_together  # noqa: E402
# the three files from https://github.com/llia0031-dotcom/policy-model-lab/tree/main/data_public
DEFAULT_SRC = Path(os.environ.get("LAK_POLICY_LAB_DATA") or (HERE.parents[1] / "data" / "policy-model-lab"))
SEED = 20261118
SEEN = {"zv-01", "zv-02"}          # opened while checking the file format: kept out of the test sets
SOURCE = {"gr-dev": "written", "gr-test": "written", "gr-hard": "written-hard", "gr-memory": "written-lookalike", "video-text": "video-words"}


def read(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


def item(r: dict, set_name: str) -> dict:
    if "split" in r:
        diff = "violating" if r["gold"] else ("look-alike" if r["trap"] else "plain")
        src = SOURCE[r["split"]]
    else:
        diff = "violating" if r["gold"] else ("look-alike" if r["kind"] == "TRAP" else "plain")
        src = "synthetic"
    return {"id": r.get("id") or f"syn-{r['sid']}", "text": r["text"], "labels": sorted(r["gold"]),
            "meta": {"lang": r["lang"], "source": src, "difficulty": diff, "n_chars": len(r["text"]), "set": set_name}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(DEFAULT_SRC))
    a = ap.parse_args()
    src = Path(a.src)
    tests = read(src / "text_tests.jsonl")
    rng = random.Random(SEED)

    dev = [item(r, "dev") for r in tests if r["split"] == "gr-dev" or r["id"] in SEEN]
    val = read(src / "synth_val.jsonl")
    by = defaultdict(list)
    for r in sorted(val, key=lambda r: r["sid"]):
        by[(r["lang"], bool(r["gold"]), r["kind"] == "TRAP")].append(r)
    picked = []
    for key in sorted(by):                                   # 60 in proportion to the strata
        rng.shuffle(by[key])
        picked += by[key][:max(1, round(60 * len(by[key]) / len(val)))]
    picked = picked[:60]
    for n, r in enumerate(picked):
        r["id"] = f"syn-val-{n:03d}"
    dev += [item(r, "dev") for r in picked]

    rest = [r for r in tests if r["split"] != "gr-dev" and r["id"] not in SEEN]
    strata = defaultdict(list)
    for r in sorted(rest, key=lambda r: r["id"]):
        strata[(r["split"], r["lang"], bool(r["gold"]))].append(r)
    a_set, b_set = [], []
    flip = 0
    for key in sorted(strata):
        rows = strata[key]
        rng.shuffle(rows)
        half = len(rows) // 2
        if len(rows) % 2:                                    # odd strata alternate the extra item between A and B
            half += flip
            flip = 1 - flip
        a_set += rows[:half]
        b_set += rows[half:]
    test_a = [item(r, "test_a") for r in sorted(a_set, key=lambda r: r["id"])]
    test_b = [item(r, "test_b") for r in sorted(b_set, key=lambda r: r["id"])]
    sets = {"dev": dev, "test_a": test_a, "test_b": test_b}
    for item_id, frm, dst in keep_together(sets):
        print(f"moved {item_id} from {frm} to {dst} (near duplicate of an item there)")
    for k, rows in sets.items():
        for r in rows:
            r["meta"]["set"] = k
    dev, test_a, test_b = sets["dev"], sets["test_a"], sets["test_b"]

    train = sorted(read(src / "synth_train.jsonl"), key=lambda r: r["sid"])
    rng.shuffle(train)
    cases = [{"id": f"case-{n:04d}", "text": r["text"], "labels": sorted(r["gold"]), "lang": r["lang"], "source": "synthetic"}
             for n, r in enumerate(train[:600])]

    for name, rows in (("items_dev.jsonl", dev), ("items_test_a.jsonl", test_a), ("items_test_b.jsonl", test_b), ("cases_synth.jsonl", cases)):
        write(HERE / name, rows)
        langs = Counter(r.get("lang") or r["meta"]["lang"] for r in rows)
        labelled = sum(1 for r in rows if r["labels"])
        print(f"{name}: {len(rows)} ({dict(langs)}), {labelled} with a label, {len(rows) - labelled} without")
    print("test A by source:", Counter(r["meta"]["source"] for r in test_a), "difficulty:", Counter(r["meta"]["difficulty"] for r in test_a))
    print("test B by source:", Counter(r["meta"]["source"] for r in test_b), "difficulty:", Counter(r["meta"]["difficulty"] for r in test_b))
    print("labels A:", sorted(Counter(l for r in test_a for l in r["labels"]).items()))
    print("labels B:", sorted(Counter(l for r in test_b for l in r["labels"]).items()))


if __name__ == "__main__":
    main()
