"""Builds the ASAP task files from the public dataset.

ASAP (Bu et al., NAACL 2021) is a set of 46,730 restaurant reviews from Dianping, each labelled by the
dataset's annotators for 18 aspect categories. It is published by Meituan-Dianping under Apache-2.0:
https://github.com/Meituan-Dianping/asap . The labelling task here: which of the 18 aspects does a
review mention? (The dataset's polarity value is kept as metadata; "-2" means not mentioned.)

    python tasks/asap/build.py download     # fetch train.csv, dev.csv, test.csv into $LAK_DATA/asap
    python tasks/asap/build.py sample       # write the frozen samples (fixed seed)
    python tasks/asap/build.py cues         # per-label cue phrases from the training split -> cues.json
    python tasks/asap/build.py stats        # label shares in the full splits and in the samples

Samples (seed 20261118, drawn without replacement from a shuffled id list):
    items_dev.jsonl      120 reviews from the official dev split      development and tuning
    items_test_a.jsonl   200 reviews from the official test split     all arms; failures are analysed
    items_test_b.jsonl   200 other reviews from the official test split   untouched until the revised version
    cases_real.jsonl     600 reviews from the official train split    the case library
Near-duplicate reviews (character 8-gram Jaccard >= 0.3) are then kept in one set: the later set's item
moves to the earlier set (dev, test A, test B), see tasks/keep_together.py.
Only these samples are kept in the repository; the full dataset is not redistributed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import random
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from keep_together import keep_together  # noqa: E402
DATA = Path(os.environ.get("LAK_DATA") or (ROOT / "data")) / "asap"
BASE = "https://raw.githubusercontent.com/Meituan-Dianping/asap/master/data/"
SHA256 = {
    "train.csv": "30912f5e2a866a4c0f654ec3461215f008b8b90d208f2c410f03369f43655de9",
    "dev.csv": "54efc8f6bc26d63a9f87e3418cd68e47f2eb13a19085e85abe63f3eafafe2b44",
    "test.csv": "217dd27c1d5699067952474e40824935d56ecf8b5047950d6da3d1222976a2bd",
}
SEED = 20261118
SIZES = {"dev": 120, "test_a": 200, "test_b": 200, "cases_real": 600}
# label order follows the paper's Table 1
LABELS = ["Food#Taste", "Food#Appearance", "Food#Portion", "Food#Recommend",
          "Price#Level", "Price#Cost_effective", "Price#Discount",
          "Location#Downtown", "Location#Transportation", "Location#Easy_to_find",
          "Service#Queue", "Service#Hospitality", "Service#Parking", "Service#Timely",
          "Ambience#Decoration", "Ambience#Noise", "Ambience#Space", "Ambience#Sanitary"]


def download() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for name, want in SHA256.items():
        path = DATA / name
        if not path.exists():
            print(f"downloading {name}")
            urllib.request.urlretrieve(BASE + name, path)
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{name}: {'ok' if got == want else 'CHANGED'} sha256 {got[:16]}")
        if got != want:
            raise SystemExit(f"{name} differs from the file this project was built on")


def read_split(name: str) -> list[dict]:
    path = DATA / f"{name}.csv"
    if not path.exists():
        raise SystemExit(f"{path} not found. Run: python tasks/asap/build.py download")
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            # line breaks are stored as the two characters backslash + n, sometimes after an extra backslash
            text = r["review"].replace("\\\\n", "\n").replace("\\n", "\n").replace("\\\n", "\n")
            text = re.sub(r"\\+r", "", text)              # stored carriage returns
            text = re.sub(r"\\+t", " ", text)             # stored tabs
            text = re.sub(r"\\{2,}", "", text)            # leftover runs of backslashes
            text = re.sub(r"[ \t\xa0]{3,}", "  ", text)
            text = re.sub(r"\n{2,}", "\n", text).strip()
            polarity = {a: int(r[a]) for a in LABELS if r[a].strip() != "-2"}
            stars = float(r["star"])
            k = len(polarity)
            rows.append({"id": f"asap-{name}-{r['id']}", "text": text, "labels": [a for a in LABELS if a in polarity],
                         "meta": {"lang": "zh", "source": f"asap/{name}", "stars": stars, "n_chars": len(text),
                                  "stars_band": "1-3 stars" if stars < 4 else "4-5 stars",
                                  "n_labels_band": "1-4 labels" if k <= 4 else ("5-7 labels" if k <= 7 else "8+ labels"),
                                  "has_neutral": "has a neutral mention" if 0 in polarity.values() else "no neutral mention",
                                  "polarity": polarity}})
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


def sample() -> None:
    rng = random.Random(SEED)
    plan = {"dev": [("dev", "items_dev.jsonl")], "test": [("test_a", "items_test_a.jsonl"), ("test_b", "items_test_b.jsonl")],
            "train": [("cases_real", "cases_real.jsonl")]}
    chunks, files = {}, {}
    for split, parts in plan.items():
        rows = sorted(read_split(split), key=lambda r: r["id"])
        rng.shuffle(rows)
        start = 0
        for key, fname in parts:
            chunks[key] = rows[start:start + SIZES[key]]
            files[key] = fname
            start += SIZES[key]
    sets = {k: chunks[k] for k in ("dev", "test_a", "test_b")}
    for item_id, src, dst in keep_together(sets):
        print(f"moved {item_id} from {src} to {dst} (near duplicate of an item there)")
    chunks.update(sets)
    for key, chunk in chunks.items():
        for r in chunk:
            r["meta"]["set"] = key
        if key == "cases_real":
            chunk = [{"id": r["id"], "text": r["text"], "labels": r["labels"], "source": "real"} for r in chunk]
        write_jsonl(HERE / files[key], chunk)
        print(f"{files[key]}: {len(chunk)} items, {sum(len(r['labels']) for r in chunk) / len(chunk):.2f} labels per item")


NGRAM = re.compile(r"[一-鿿]+")


def grams(text: str) -> set[str]:
    out = set()
    for run in NGRAM.findall(text):
        for n in (2, 3, 4):
            out.update(run[i:i + n] for i in range(len(run) - n + 1))
    return out


def cues(top: int = 12, min_count: int = 150) -> None:
    """For each label: phrases far more frequent in training reviews that carry it, with how often a review
    containing the phrase carries the label (precision of the cue) and how many labelled reviews contain it."""
    rows = read_split("train")
    n = len(rows)
    doc_grams = [grams(r["text"]) for r in rows]
    df = Counter(g for gs in doc_grams for g in gs)
    out = {}
    for label in LABELS:
        has = [label in r["labels"] for r in rows]
        n_pos = sum(has)
        pos = Counter(g for gs, h in zip(doc_grams, has) if h for g in gs)
        scored = []
        for g, c in df.items():
            if c < min_count:
                continue
            a = pos.get(g, 0)
            b = c - a
            lo = math.log((a + 0.5) / (n_pos - a + 0.5)) - math.log((b + 0.5) / (n - n_pos - b + 0.5))
            scored.append((lo, g, a, c))
        scored.sort(reverse=True)
        picked = []
        for lo, g, a, c in scored:
            if any(g in p["phrase"] or p["phrase"] in g for p in picked):
                continue
            picked.append({"phrase": g, "reviews_with_phrase": c, "of_which_labelled": a, "precision": round(a / c, 3),
                           "share_of_labelled_reviews": round(a / n_pos, 3)})
            if len(picked) >= top:
                break
        out[label] = {"labelled_reviews": n_pos, "share": round(n_pos / n, 3), "cues": picked}
    (HERE / "cues.json").write_text(json.dumps({"split": "train", "reviews": n, "min_count": min_count, "labels": out},
                                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for label, v in out.items():
        print(label, f"{v['share']:.3f}", " ".join(f"{c['phrase']}({c['precision']:.2f})" for c in v["cues"][:8]))


def stats() -> None:
    out = {}
    for split in ("train", "dev", "test"):
        rows = read_split(split)
        out[f"full_{split}"] = _stats(rows)
    for fname in ("items_dev.jsonl", "items_test_a.jsonl", "items_test_b.jsonl", "cases_real.jsonl"):
        rows = [json.loads(l) for l in (HERE / fname).read_text(encoding="utf-8").splitlines() if l.strip()]
        out[fname] = _stats(rows)
    (HERE / "stats.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for k, v in out.items():
        print(k, v["n"], v["labels_per_item"], v["median_chars"])


def _stats(rows: list[dict]) -> dict:
    n = len(rows)
    lens = sorted(len(r["text"]) for r in rows)
    c = Counter(l for r in rows for l in r["labels"])
    return {"n": n, "labels_per_item": round(sum(len(r["labels"]) for r in rows) / n, 2), "median_chars": lens[n // 2],
            "label_share": {l: round(c[l] / n, 3) for l in LABELS}}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"download": download, "sample": sample, "cues": cues, "stats": stats}.get(cmd, lambda: print(__doc__))()
