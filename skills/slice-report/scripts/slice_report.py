#!/usr/bin/env python3
"""slice_report.py - the same labelling metrics, cut by slices of the data.

Reads the gold file and the prediction file (JSONL, shared id) and groups the items by one or more
fields of the gold file: language, source, difficulty, a length bucket, or "has this gold label".

    python slice_report.py gold.jsonl pred.jsonl --by meta.lang --by meta.difficulty
    python slice_report.py gold.jsonl pred.jsonl --length text            # buckets of text length
    python slice_report.py gold.jsonl pred.jsonl --by-label               # one slice per gold label
    python slice_report.py gold.jsonl pred.jsonl --by meta.lang --format json --out slices.json

For every slice: number of items, micro F1 with a bootstrap interval (shown as – when the slice has no
gold label, where F1 says nothing), exact-match rate with a Wilson interval, misses among its labelled
items and false alarms among its unlabelled items, and the difference between the slice and all other
items with a bootstrap interval: in micro F1 when both sides have gold labels, otherwise in exact-match
rate (the report names the measure). A slice is marked "worse" or "better" only when that interval
excludes 0, and "too few" when it has fewer than --min-n items (default 20), where no verdict is given.

Python 3.9+, standard library only. Exit code 0: report written; 2: the input could not be read.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

Z95 = 1.959963984540054


def read_jsonl(path: str) -> list[dict]:
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}: line {n} is not valid JSON ({e.msg})")
    return rows


def dig(row: dict, field: str):
    cur = row
    for part in field.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def as_set(value) -> frozenset:
    if isinstance(value, str):
        return frozenset([value]) if value.strip() else frozenset()
    if isinstance(value, (list, tuple)) and all(isinstance(v, str) for v in value):
        return frozenset(v for v in value if v.strip())
    return frozenset()


def wilson(k: int, n: int, z: float = Z95):
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [max(0.0, centre - half), min(1.0, centre + half)]


def micro_f1(rows: list[tuple]) -> float | None:
    """Micro F1 of (tp, fp, fn) rows; None when the rows hold no gold label (F1 is not meaningful there)."""
    tp = sum(r[0] for r in rows)
    fp = sum(r[1] for r in rows)
    fn = sum(r[2] for r in rows)
    if tp + fn == 0:
        return None
    return 2 * tp / (2 * tp + fp + fn)


def exact_rate(rows: list[tuple]) -> float | None:
    return sum(1 for r in rows if r[1] == 0 and r[2] == 0) / len(rows) if rows else None


def percentile(values: list[float], q: float) -> float:
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def interval(values: list) -> list[float] | None:
    vals = [v for v in values if v is not None]
    if not vals or len(vals) < 0.9 * len(values):
        return None
    return [percentile(vals, 0.025), percentile(vals, 0.975)]


def length_buckets(lengths: list[int], k: int = 3) -> list[tuple[int, int]]:
    """k buckets with roughly equal numbers of items; returns inclusive (low, high) bounds."""
    s = sorted(lengths)
    if not s:
        return []
    cuts = sorted({s[min(len(s) - 1, (len(s) * j) // k)] for j in range(1, k)})
    bounds, low = [], s[0]
    for c in cuts:
        if c - 1 >= low:
            bounds.append((low, c - 1))
            low = c
    bounds.append((low, s[-1]))
    return bounds


def bucket_name(n: int, bounds: list[tuple[int, int]]) -> str:
    for lo, hi in bounds:
        if lo <= n <= hi:
            return f"{lo}–{hi} chars"
    return "other"


def slice_stats(items: list[dict], members: list[int], boot: int, rng: random.Random, min_n: int) -> dict:
    """items: dicts with counts (tp, fp, fn), exact, has_gold, has_pred. members: indices in the slice."""
    inside = [items[i] for i in members]
    member_set = set(members)
    outside = [it for i, it in enumerate(items) if i not in member_set]
    rows_in = [it["c"] for it in inside]
    rows_out = [it["c"] for it in outside]
    n = len(inside)
    exact = sum(1 for it in inside if it["exact"])
    f_in, f_out = micro_f1(rows_in), micro_f1(rows_out)
    measure = "micro F1" if f_in is not None and f_out is not None else "exact match"
    stat = micro_f1 if measure == "micro F1" else exact_rate
    s_in, s_out = stat(rows_in), stat(rows_out)
    out = {"n": n, "micro_f1": f_in, "exact_match": {"k": exact, "n": n, "rate": exact / n if n else None, "ci": wilson(exact, n)},
           "rest_n": len(outside), "rest_micro_f1": f_out, "measure": measure,
           "diff": None if s_in is None or s_out is None else s_in - s_out}
    labelled = [it for it in inside if it["has_gold"]]
    unlabelled = [it for it in inside if not it["has_gold"]]
    if labelled:
        miss = sum(1 for it in labelled if not it["has_pred"])
        out["miss"] = {"k": miss, "n": len(labelled), "rate": miss / len(labelled), "ci": wilson(miss, len(labelled))}
    if unlabelled:
        alarm = sum(1 for it in unlabelled if it["has_pred"])
        out["false_alarm"] = {"k": alarm, "n": len(unlabelled), "rate": alarm / len(unlabelled), "ci": wilson(alarm, len(unlabelled))}
    f_boot, d_boot = [], []
    if boot > 0 and n:
        for _ in range(boot):
            a = [rows_in[rng.randrange(n)] for _ in range(n)]
            f_boot.append(micro_f1(a))
            if rows_out:
                b = [rows_out[rng.randrange(len(rows_out))] for _ in range(len(rows_out))]
                sa, sb = stat(a), stat(b)
                d_boot.append(None if sa is None or sb is None else sa - sb)
    out["micro_f1_ci"] = interval(f_boot) if f_boot else None
    out["diff_ci"] = interval(d_boot) if d_boot else None
    if n < min_n:
        out["verdict"] = "too few"
    elif out["diff_ci"] and out["diff_ci"][1] < 0:
        out["verdict"] = "worse"
    elif out["diff_ci"] and out["diff_ci"][0] > 0:
        out["verdict"] = "better"
    else:
        out["verdict"] = "no measured difference"
    return out


def build(gold_rows: list[dict], pred_rows: list[dict], by: list[str], length_field: str | None, by_label: bool,
          id_field: str = "id", gold_field: str = "labels", pred_field: str = "labels", boot: int = 1000,
          seed: int = 20261118, min_n: int = 20, n_buckets: int = 3) -> dict:
    pred = {dig(r, id_field): as_set(dig(r, pred_field)) for r in pred_rows}
    items = []
    for r in gold_rows:
        g = as_set(dig(r, gold_field))
        p = pred.get(dig(r, id_field), frozenset())
        items.append({"row": r, "gold": g, "c": (len(g & p), len(p - g), len(g - p)), "exact": g == p,
                      "has_gold": bool(g), "has_pred": bool(p)})
    rng = random.Random(seed)
    overall = {"n": len(items), "micro_f1": micro_f1([it["c"] for it in items]),
               "exact_match_rate": sum(1 for it in items if it["exact"]) / len(items) if items else None}
    groups = []
    for field in by:
        values: dict[str, list[int]] = {}
        for i, it in enumerate(items):
            v = dig(it["row"], field)
            if isinstance(v, list):
                keys = [str(x) for x in v] or ["(none)"]
            else:
                keys = ["(missing)" if v is None else str(v)]
            for k in keys:
                values.setdefault(k, []).append(i)
        groups.append((field, values))
    if length_field:
        lengths = [len(str(dig(it["row"], length_field) or "")) for it in items]
        bounds = length_buckets(lengths, n_buckets)
        values = {}
        for i, n in enumerate(lengths):
            values.setdefault(bucket_name(n, bounds), []).append(i)
        ordered = {bucket_name(lo, bounds): values[bucket_name(lo, bounds)] for lo, _ in bounds if bucket_name(lo, bounds) in values}
        groups.append((f"length of {length_field}", ordered))
    if by_label:
        values = {}
        for i, it in enumerate(items):
            for l in (sorted(it["gold"]) or ["(no gold label)"]):
                values.setdefault(l, []).append(i)
        groups.append(("gold label", dict(sorted(values.items()))))
    out = {"overall": overall, "min_n": min_n, "bootstrap": {"resamples": boot, "seed": seed}, "groups": []}
    for field, values in groups:
        out["groups"].append({"field": field,
                              "slices": [{"value": v, **slice_stats(items, members, boot, rng, min_n)} for v, members in values.items()]})
    return out


def pct(x, d=1) -> str:
    return "–" if x is None else f"{100 * x:.{d}f}%"


def num(x) -> str:
    return "–" if x is None else f"{x:.3f}"


def to_markdown(rep: dict) -> str:
    o = rep["overall"]
    lines = [f"**Slices of {o['n']} items.** Overall micro F1 {num(o['micro_f1'])}, exact match {pct(o['exact_match_rate'])}.", ""]
    for g in rep["groups"]:
        lines += [f"### By {g['field']}", "",
                  "| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |", "|---|---|---|---|---|---|---|---|"]
        for s in g["slices"]:
            ci = s.get("micro_f1_ci")
            f1 = num(s["micro_f1"]) + (f" [{ci[0]:.2f}–{ci[1]:.2f}]" if ci else "")
            em = s["exact_match"]
            emt = f"{em['k']}/{em['n']} ({pct(em['rate'])})"
            miss = f"{s['miss']['k']}/{s['miss']['n']}" if "miss" in s else "–"
            fa = f"{s['false_alarm']['k']}/{s['false_alarm']['n']}" if "false_alarm" in s else "–"
            dci = s.get("diff_ci")
            diff = "–" if s["diff"] is None else f"{s['diff']:+.3f}" + (f" [{dci[0]:+.2f} to {dci[1]:+.2f}]" if dci else "")
            if s["diff"] is not None and s.get("measure") == "exact match":
                diff += " (exact match)"
            lines.append(f"| {s['value']} | {s['n']} | {f1} | {emt} | {miss} | {fa} | {diff} | {s['verdict']} |")
        lines.append("")
    lines.append(f"\"Against the rest\" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has "
                 f"no gold label, F1 is not defined and the exact-match rate is compared instead. "
                 f"A slice is called worse or better only when the interval excludes 0; slices under {rep['min_n']} items get no verdict.")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Labelling metrics by slice.")
    ap.add_argument("gold")
    ap.add_argument("pred")
    ap.add_argument("--by", action="append", default=[], metavar="FIELD", help="a field of the gold file, e.g. meta.lang (repeatable)")
    ap.add_argument("--length", metavar="FIELD", help="bucket items by the length of this text field")
    ap.add_argument("--buckets", type=int, default=3)
    ap.add_argument("--by-label", action="store_true", help="one slice per gold label")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--gold-field", default="labels")
    ap.add_argument("--pred-field", default="labels")
    ap.add_argument("--min-n", type=int, default=20)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261118)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if not (a.by or a.length or a.by_label):
        print("error: give at least one of --by FIELD, --length FIELD, --by-label", file=sys.stderr)
        return 2
    try:
        rep = build(read_jsonl(a.gold), read_jsonl(a.pred), a.by, a.length, a.by_label, a.id_field, a.gold_field,
                    a.pred_field, a.boot, a.seed, a.min_n, a.buckets)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    text = json.dumps(rep, ensure_ascii=False, indent=1) + "\n" if a.format == "json" else to_markdown(rep)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
