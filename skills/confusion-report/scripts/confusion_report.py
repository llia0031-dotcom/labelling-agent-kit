#!/usr/bin/env python3
"""confusion_report.py - which labels get confused with which, for multi-label (or single-label) labelling.

An ordinary confusion matrix needs one gold label and one predicted label per item. With several labels
per item it is not defined, so this script builds the multi-label confusion matrix (MLCM) of Heydarian,
Doyle and Samavi, "MLCM: Multi-Label Confusion Matrix", IEEE Access 10 (2022). The matrix has one extra
row, "no gold label", and one extra column, "no predicted label". For an item with gold set T and
predicted set P:

  every label in both T and P     counts on the diagonal
  T empty                         each predicted label counts in the "no gold label" row
  P misses labels, adds none      each missed label counts in the "no predicted label" column
  P adds labels, misses none      each added label counts against every gold label of the item
  P misses some and adds some     each added label counts against every missed label

With one label per item this is the ordinary confusion matrix.

    python confusion_report.py gold.jsonl pred.jsonl
    python confusion_report.py gold.jsonl pred.jsonl --top 15 --format json --out confusion.json

Also reported: how many items are exact, under-labelled (missed only), over-labelled (added only) or
swapped (both), and the most frequent confused pairs with the ids of the items behind them.

Python 3.9+, standard library only. Exit code 0: report written; 2: the input could not be read.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

NO_GOLD = "(no gold label)"
NO_PRED = "(no predicted label)"


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


def kind_of(gold: frozenset, pred: frozenset) -> str:
    if gold == pred:
        return "exact"
    missed, added = gold - pred, pred - gold
    if missed and added:
        return "swapped"
    return "under-labelled" if missed else "over-labelled"


def mlcm(ids: list, gold: list[frozenset], pred: list[frozenset], labels: list[str]) -> dict:
    """Returns the (L+1) x (L+1) matrix (rows gold, columns predicted) and the item ids behind each cell."""
    L = len(labels)
    idx = {l: k for k, l in enumerate(labels)}
    m = [[0] * (L + 1) for _ in range(L + 1)]
    cells: dict[tuple[int, int], list] = {}

    def add(r: int, c: int, item_id) -> None:
        m[r][c] += 1
        cells.setdefault((r, c), []).append(item_id)

    for i, g, p in zip(ids, gold, pred):
        g = frozenset(l for l in g if l in idx)
        p = frozenset(l for l in p if l in idx)
        if not g:
            if not p:
                add(L, L, i)
            for l in sorted(p):
                add(L, idx[l], i)
            continue
        for l in sorted(g & p):
            add(idx[l], idx[l], i)
        missed, added = sorted(g - p), sorted(p - g)
        if not added:
            for l in missed:
                add(idx[l], L, i)
        elif not missed:
            for t in sorted(g):
                for a in added:
                    add(idx[t], idx[a], i)
        else:
            for t in missed:
                for a in added:
                    add(idx[t], idx[a], i)
    return {"matrix": m, "cells": cells}


def build(gold_rows: list[dict], pred_rows: list[dict], labels: list[str] | None = None, id_field: str = "id",
          gold_field: str = "labels", pred_field: str = "labels", top: int = 10, examples: int = 5) -> dict:
    pred_by_id = {dig(r, id_field): as_set(dig(r, pred_field)) for r in pred_rows}
    ids = [dig(r, id_field) for r in gold_rows]
    gold = [as_set(dig(r, gold_field)) for r in gold_rows]
    pred = [pred_by_id.get(i, frozenset()) for i in ids]
    if not labels:
        seen = set()
        for s in gold + pred:
            seen |= s
        labels = sorted(seen)
    res = mlcm(ids, gold, pred, labels)
    m, cells, L = res["matrix"], res["cells"], len(labels)
    names = labels + [NO_GOLD]
    cols = labels + [NO_PRED]
    kinds = {"exact": 0, "under-labelled": 0, "over-labelled": 0, "swapped": 0}
    for g, p in zip(gold, pred):
        kinds[kind_of(g, p)] += 1
    pairs = []
    for (r, c), who in cells.items():
        if r == c:
            continue
        pairs.append({"gold": names[r], "predicted": cols[c], "count": len(who), "ids": who[:examples],
                      "kind": "missed" if c == L else ("added to an unlabelled item" if r == L else "confused")})
    pairs.sort(key=lambda x: (-x["count"], x["gold"], x["predicted"]))
    per_label = []
    for k, l in enumerate(labels):
        row_total = sum(m[k])
        wrong = [(cols[c], m[k][c]) for c in range(L + 1) if c != k and m[k][c]]
        wrong.sort(key=lambda x: -x[1])
        col_wrong = [(names[r], m[r][k]) for r in range(L + 1) if r != k and m[r][k]]
        col_wrong.sort(key=lambda x: -x[1])
        per_label.append({"label": l, "row_total": row_total, "correct": m[k][k],
                          "row_share_correct": m[k][k] / row_total if row_total else None,
                          "gold_here_predicted_as": wrong[:3], "predicted_here_gold_was": col_wrong[:3]})
    return {"n_items": len(ids), "labels": labels, "row_names": names, "column_names": cols, "matrix": m,
            "item_kinds": kinds, "top_pairs": pairs[:top], "per_label": per_label,
            "method": "MLCM (Heydarian, Doyle, Samavi 2022): rows are gold labels, columns are predicted labels"}


def to_markdown(rep: dict) -> str:
    k = rep["item_kinds"]
    lines = [f"**Confusion over {rep['n_items']} items.** Exact {k['exact']}, under-labelled {k['under-labelled']}, "
             f"over-labelled {k['over-labelled']}, swapped {k['swapped']}.", "",
             "Rows are gold labels, columns are predicted labels (multi-label confusion matrix, MLCM).", ""]
    cols = rep["column_names"]
    lines.append("| gold \\ predicted | " + " | ".join(cols) + " |")
    lines.append("|---" * (len(cols) + 1) + "|")
    for name, row in zip(rep["row_names"], rep["matrix"]):
        lines.append(f"| **{name}** | " + " | ".join("·" if v == 0 else str(v) for v in row) + " |")
    lines += ["", "### Most frequent confusions", "", "| Gold | Predicted | Count | Kind | Example ids |", "|---|---|---|---|---|"]
    for p in rep["top_pairs"]:
        lines.append(f"| {p['gold']} | {p['predicted']} | {p['count']} | {p['kind']} | {', '.join(map(str, p['ids']))} |")
    if not rep["top_pairs"]:
        lines.append("| – | – | 0 | – | – |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Multi-label confusion matrix and the most frequent confusions.")
    ap.add_argument("gold")
    ap.add_argument("pred")
    ap.add_argument("--labels", help="comma-separated label list, in the order to show (default: every label seen)")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--gold-field", default="labels")
    ap.add_argument("--pred-field", default="labels")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--examples", type=int, default=5, help="item ids listed per confused pair")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    labels = [x.strip() for x in a.labels.split(",") if x.strip()] if a.labels else None
    try:
        rep = build(read_jsonl(a.gold), read_jsonl(a.pred), labels, a.id_field, a.gold_field, a.pred_field, a.top, a.examples)
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
