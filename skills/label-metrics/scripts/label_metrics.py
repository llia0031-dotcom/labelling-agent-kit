#!/usr/bin/env python3
"""label_metrics.py - precision, recall and F1 per label for a labelling run, with intervals.

Reads two JSONL files that share an id: the gold labels and the predicted labels. Each line holds an id
and a list of labels (an empty list means "no label applies"). Works for multi-label and single-label tasks.

    python label_metrics.py gold.jsonl pred.jsonl
    python label_metrics.py gold.jsonl pred.jsonl --compare pred_b.jsonl     # two runs on the same items
    python label_metrics.py gold.jsonl pred.jsonl --format json --out metrics.json

What it reports
  per label   TP, FP, FN, precision and recall with Wilson 95% intervals, F1 with a bootstrap interval
  overall     micro and macro F1 (bootstrap intervals), exact-match rate (Wilson), Hamming loss
  decision    when some items have no gold label: miss rate (a labelled item predicted as empty) and
              false-alarm rate (an unlabelled item given a label), both with Wilson intervals
  --compare   the same for a second run, the paired difference in micro and macro F1 (paired bootstrap)
              and an exact McNemar test on exact-match

Python 3.9+, standard library only. Exit code 0: report written; 2: the input could not be read.
The numbers are tested against scikit-learn and statsmodels (see tests/ in the repository).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

Z95 = 1.959963984540054


# ---------- reading ----------

def read_jsonl(path: str) -> list[dict]:
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}: line {n} is not valid JSON ({e.msg})")
    return rows


def dig(row: dict, field: str):
    """Reads a field; "meta.lang" reads row["meta"]["lang"]."""
    cur = row
    for part in field.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def label_set(value) -> frozenset | None:
    """A list of labels, a single label, or None when the value is missing or not a label list."""
    if value is None:
        return None
    if isinstance(value, str):
        return frozenset([value]) if value.strip() else frozenset()
    if isinstance(value, (list, tuple)):
        if not all(isinstance(v, str) for v in value):
            return None
        return frozenset(v for v in value if v.strip())
    return None


def load_pairs(gold_path: str, pred_path: str, id_field: str = "id", gold_field: str = "labels",
               pred_field: str = "labels") -> dict:
    """Aligns the two files on id. A gold item with no usable prediction counts as an empty prediction
    and is listed under 'missing' (no line) or 'unparsed' (a line without a label list)."""
    gold_rows, pred_rows = read_jsonl(gold_path), read_jsonl(pred_path)
    gold, order = {}, []
    for r in gold_rows:
        i = dig(r, id_field)
        s = label_set(dig(r, gold_field))
        if i is None or s is None:
            raise ValueError(f"{gold_path}: every line needs '{id_field}' and a label list in '{gold_field}'")
        if i in gold:
            raise ValueError(f"{gold_path}: duplicate id {i!r}")
        gold[i] = s
        order.append(i)
    pred, unparsed, extra, seen = {}, [], [], set()
    for r in pred_rows:
        i = dig(r, id_field)
        if i in seen:
            raise ValueError(f"{pred_path}: duplicate id {i!r}")
        seen.add(i)
        if i not in gold:
            extra.append(i)
            continue
        s = label_set(dig(r, pred_field))
        if s is None:
            unparsed.append(i)
            s = frozenset()
        pred[i] = s
    missing = [i for i in order if i not in pred]
    for i in missing:
        pred[i] = frozenset()
    return {"ids": order, "gold": [gold[i] for i in order], "pred": [pred[i] for i in order],
            "missing": missing, "unparsed": unparsed, "not_in_gold": extra}


# ---------- statistics ----------

def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float] | None:
    """Wilson score interval for k successes out of n."""
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def ratio(k: int, n: int) -> float | None:
    return k / n if n else None


def f1_of(tp: int, fp: int, fn: int) -> float | None:
    d = 2 * tp + fp + fn
    return 2 * tp / d if d else None


def label_list(gold: list, pred: list, labels: list[str] | None = None) -> list[str]:
    if labels:
        return list(labels)
    seen = set()
    for s in gold:
        seen |= s
    for s in pred:
        seen |= s
    return sorted(seen)


def item_vectors(gold: list, pred: list, labels: list[str]) -> list[tuple]:
    """Per item: (tp, fp, fn) index tuples over the label list, and whether the sets are equal."""
    idx = {l: k for k, l in enumerate(labels)}
    out = []
    for g, p in zip(gold, pred):
        tp = tuple(idx[l] for l in g & p if l in idx)
        fp = tuple(idx[l] for l in p - g if l in idx)
        fn = tuple(idx[l] for l in g - p if l in idx)
        out.append((tp, fp, fn, g == p))
    return out


def tally(vectors: list[tuple], n_labels: int, rows=None) -> tuple[list, list, list]:
    tp, fp, fn = [0] * n_labels, [0] * n_labels, [0] * n_labels
    for r in (range(len(vectors)) if rows is None else rows):
        a, b, c, _ = vectors[r]
        for k in a:
            tp[k] += 1
        for k in b:
            fp[k] += 1
        for k in c:
            fn[k] += 1
    return tp, fp, fn


def micro_macro(tp: list, fp: list, fn: list) -> tuple[float | None, float | None]:
    """Micro F1 over all labels; macro F1 over the labels present in the gold set (support > 0), so two runs on
    the same items are always averaged over the same labels. A false positive on a label absent from the gold
    set still counts in micro F1 and in the per-label table."""
    micro = f1_of(sum(tp), sum(fp), sum(fn))
    per = [f1_of(a, b, c) for a, b, c in zip(tp, fp, fn) if a + c > 0]
    macro = sum(per) / len(per) if per else None
    return micro, macro


def percentile(values: list[float], q: float) -> float:
    """Linear-interpolation percentile (the default of numpy.percentile)."""
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def interval(values: list[float | None]) -> list[float] | None:
    vals = [v for v in values if v is not None]
    if len(vals) < 0.9 * len(values) or not vals:   # undefined in more than 10% of the resamples
        return None
    return [percentile(vals, 0.025), percentile(vals, 0.975)]


def bootstrap(vectors: list[tuple], n_labels: int, boot: int, seed: int) -> dict:
    """Percentile bootstrap over items for micro F1, macro F1 and each label's F1."""
    if boot <= 0 or not vectors:
        return {"micro": None, "macro": None, "labels": [None] * n_labels}
    rng = random.Random(seed)
    n = len(vectors)
    micro, macro, per = [], [], [[] for _ in range(n_labels)]
    for _ in range(boot):
        rows = [rng.randrange(n) for _ in range(n)]
        tp, fp, fn = tally(vectors, n_labels, rows)
        mi, ma = micro_macro(tp, fp, fn)
        micro.append(mi)
        macro.append(ma)
        for k in range(n_labels):
            per[k].append(f1_of(tp[k], fp[k], fn[k]))
    return {"micro": interval(micro), "macro": interval(macro), "labels": [interval(v) for v in per]}


def summarise(gold: list, pred: list, labels: list[str] | None = None, boot: int = 2000, seed: int = 20261118) -> dict:
    labels = label_list(gold, pred, labels)
    n, L = len(gold), len(labels)
    vectors = item_vectors(gold, pred, labels)
    tp, fp, fn = tally(vectors, L)
    bs = bootstrap(vectors, L, boot, seed)
    per = []
    for k, l in enumerate(labels):
        per.append({
            "label": l, "support": tp[k] + fn[k], "predicted": tp[k] + fp[k], "tp": tp[k], "fp": fp[k], "fn": fn[k],
            "tn": n - tp[k] - fp[k] - fn[k],
            "precision": ratio(tp[k], tp[k] + fp[k]), "precision_ci": _ci(wilson(tp[k], tp[k] + fp[k])),
            "recall": ratio(tp[k], tp[k] + fn[k]), "recall_ci": _ci(wilson(tp[k], tp[k] + fn[k])),
            "f1": f1_of(tp[k], fp[k], fn[k]), "f1_ci": bs["labels"][k],
        })
    micro, macro = micro_macro(tp, fp, fn)
    exact = sum(1 for v in vectors if v[3])
    out = {
        "n_items": n, "labels": labels,
        "per_label": per,
        "micro": {"precision": ratio(sum(tp), sum(tp) + sum(fp)), "recall": ratio(sum(tp), sum(tp) + sum(fn)),
                  "f1": micro, "f1_ci": bs["micro"], "tp": sum(tp), "fp": sum(fp), "fn": sum(fn)},
        "macro": {"f1": macro, "f1_ci": bs["macro"],
                  "labels_counted": sum(1 for a, c in zip(tp, fn) if a + c > 0)},
        "exact_match": {"k": exact, "n": n, "rate": ratio(exact, n), "ci": _ci(wilson(exact, n))},
        "hamming_loss": (sum(fp) + sum(fn)) / (n * L) if n and L else None,
        "bootstrap": {"resamples": boot, "seed": seed} if boot > 0 else None,
    }
    with_gold = [(g, p) for g, p in zip(gold, pred) if g]
    without = [(g, p) for g, p in zip(gold, pred) if not g]
    if with_gold and without:
        missed = sum(1 for g, p in with_gold if not p)
        alarms = sum(1 for g, p in without if p)
        out["decision"] = {
            "labelled_items": len(with_gold), "unlabelled_items": len(without),
            "miss": {"k": missed, "n": len(with_gold), "rate": ratio(missed, len(with_gold)), "ci": _ci(wilson(missed, len(with_gold)))},
            "false_alarm": {"k": alarms, "n": len(without), "rate": ratio(alarms, len(without)), "ci": _ci(wilson(alarms, len(without)))},
        }
    return out


def _ci(pair) -> list[float] | None:
    return [pair[0], pair[1]] if pair else None


# ---------- comparing two runs on the same items ----------

def binom_two_sided(b: int, c: int) -> float | None:
    """Exact McNemar p-value: a two-sided binomial test of b against b + c with p = 0.5."""
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def compare(gold: list, pred_a: list, pred_b: list, labels: list[str] | None = None, boot: int = 2000,
            seed: int = 20261118) -> dict:
    """Paired comparison of run B against run A on the same items (differences are B minus A)."""
    union = [a | b for a, b in zip(pred_a, pred_b)]
    labels = label_list(gold, union, labels)
    L, n = len(labels), len(gold)
    va, vb = item_vectors(gold, pred_a, labels), item_vectors(gold, pred_b, labels)
    a_only = sum(1 for x, y in zip(va, vb) if x[3] and not y[3])   # A exact, B not
    b_only = sum(1 for x, y in zip(va, vb) if y[3] and not x[3])
    ma, mb = micro_macro(*tally(va, L)), micro_macro(*tally(vb, L))
    d_micro, d_macro = [], []
    if boot > 0 and n:
        rng = random.Random(seed)
        for _ in range(boot):
            rows = [rng.randrange(n) for _ in range(n)]
            xa, xb = micro_macro(*tally(va, L, rows)), micro_macro(*tally(vb, L, rows))
            d_micro.append(None if xa[0] is None or xb[0] is None else xb[0] - xa[0])
            d_macro.append(None if xa[1] is None or xb[1] is None else xb[1] - xa[1])
    per = []
    ta, tb = tally(va, L), tally(vb, L)
    for k, l in enumerate(labels):
        fa, fb = f1_of(ta[0][k], ta[1][k], ta[2][k]), f1_of(tb[0][k], tb[1][k], tb[2][k])
        per.append({"label": l, "f1_a": fa, "f1_b": fb, "diff": None if fa is None or fb is None else fb - fa})
    return {
        "n_items": n,
        "micro_f1": {"a": ma[0], "b": mb[0], "diff": _sub(mb[0], ma[0]), "diff_ci": interval(d_micro) if d_micro else None},
        "macro_f1": {"a": ma[1], "b": mb[1], "diff": _sub(mb[1], ma[1]), "diff_ci": interval(d_macro) if d_macro else None},
        "exact_match": {"a_only_right": a_only, "b_only_right": b_only, "both_right": sum(1 for x, y in zip(va, vb) if x[3] and y[3]),
                        "both_wrong": sum(1 for x, y in zip(va, vb) if not x[3] and not y[3]),
                        "mcnemar_exact_p": binom_two_sided(a_only, b_only)},
        "per_label": per,
        "bootstrap": {"resamples": boot, "seed": seed} if boot > 0 else None,
    }


def _sub(b, a):
    return None if a is None or b is None else b - a


# ---------- output ----------

def pct(x: float | None, digits: int = 1) -> str:
    return "–" if x is None else f"{100 * x:.{digits}f}%"


def num(x: float | None) -> str:
    return "–" if x is None else f"{x:.3f}"


def rng_pct(ci) -> str:
    return "" if not ci else f" [{100 * ci[0]:.0f}–{100 * ci[1]:.0f}]"


def rng_num(ci) -> str:
    return "" if not ci else f" [{ci[0]:.2f}–{ci[1]:.2f}]"


def to_markdown(s: dict, notes: dict | None = None, title: str = "Label metrics") -> str:
    lines = [f"**{title}: {s['n_items']} items, {len(s['labels'])} labels.** "
             f"Micro F1 {num(s['micro']['f1'])}{rng_num(s['micro']['f1_ci'])}, "
             f"macro F1 {num(s['macro']['f1'])}{rng_num(s['macro']['f1_ci'])}, "
             f"exact match {s['exact_match']['k']}/{s['exact_match']['n']} ({pct(s['exact_match']['rate'])}){rng_pct(s['exact_match']['ci'])}.", ""]
    lines += ["| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |", "|---|---|---|---|---|---|---|---|---|"]
    for r in s["per_label"]:
        lines.append(f"| {r['label']} | {r['support']} | {r['predicted']} | {r['tp']} | {r['fp']} | {r['fn']} | "
                     f"{pct(r['precision'])}{rng_pct(r['precision_ci'])} | {pct(r['recall'])}{rng_pct(r['recall_ci'])} | "
                     f"{num(r['f1'])}{rng_num(r['f1_ci'])} |")
    m = s["micro"]
    lines.append(f"| **micro** | {m['tp'] + m['fn']} | {m['tp'] + m['fp']} | {m['tp']} | {m['fp']} | {m['fn']} | "
                 f"{pct(m['precision'])} | {pct(m['recall'])} | {num(m['f1'])}{rng_num(m['f1_ci'])} |")
    if "decision" in s:
        d = s["decision"]
        lines += ["", f"Miss rate (a labelled item predicted with no label): {d['miss']['k']}/{d['miss']['n']} "
                      f"({pct(d['miss']['rate'])}){rng_pct(d['miss']['ci'])}. "
                      f"False-alarm rate (an unlabelled item given a label): {d['false_alarm']['k']}/{d['false_alarm']['n']} "
                      f"({pct(d['false_alarm']['rate'])}){rng_pct(d['false_alarm']['ci'])}."]
    lines += ["", "Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1."]
    if notes:
        for key, text in (("missing", "gold items without a prediction line (counted as no label)"),
                          ("unparsed", "predictions without a label list (counted as no label)"),
                          ("not_in_gold", "prediction ids that are not in the gold file (ignored)")):
            if notes.get(key):
                shown = ", ".join(map(str, notes[key][:10])) + (" ..." if len(notes[key]) > 10 else "")
                lines.append(f"- {len(notes[key])} {text}: {shown}")
    return "\n".join(lines) + "\n"


def compare_markdown(c: dict, name_a: str = "A", name_b: str = "B") -> str:
    mi, ma, e = c["micro_f1"], c["macro_f1"], c["exact_match"]
    lines = [f"**{name_b} against {name_a} on the same {c['n_items']} items.**", "",
             f"| Measure | {name_a} | {name_b} | Difference ({name_b} − {name_a}) |", "|---|---|---|---|",
             f"| Micro F1 | {num(mi['a'])} | {num(mi['b'])} | {_signed(mi['diff'])}{rng_signed(mi['diff_ci'])} |",
             f"| Macro F1 | {num(ma['a'])} | {num(ma['b'])} | {_signed(ma['diff'])}{rng_signed(ma['diff_ci'])} |", "",
             f"Exact match: only {name_a} right on {e['a_only_right']} {_items(e['a_only_right'])}, only {name_b} right on {e['b_only_right']}, "
             f"both right on {e['both_right']}, both wrong on {e['both_wrong']}; exact McNemar p = "
             f"{'–' if e['mcnemar_exact_p'] is None else format(e['mcnemar_exact_p'], '.3f')}.", "",
             f"| Label | F1 {name_a} | F1 {name_b} | Difference |", "|---|---|---|---|"]
    for r in c["per_label"]:
        lines.append(f"| {r['label']} | {num(r['f1_a'])} | {num(r['f1_b'])} | {_signed(r['diff'])} |")
    lines += ["", "A difference whose interval includes 0 is not a measured difference."]
    return "\n".join(lines) + "\n"


def _items(n: int) -> str:
    return "item" if n == 1 else "items"


def _signed(x) -> str:
    return "–" if x is None else f"{x:+.3f}"


def rng_signed(ci) -> str:
    return "" if not ci else f" [{ci[0]:+.3f} to {ci[1]:+.3f}]"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Precision, recall and F1 per label, with intervals.")
    ap.add_argument("gold")
    ap.add_argument("pred")
    ap.add_argument("--compare", metavar="PRED_B", help="a second prediction file on the same items")
    ap.add_argument("--labels", help="comma-separated label list (default: every label seen in either file)")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--gold-field", default="labels")
    ap.add_argument("--pred-field", default="labels")
    ap.add_argument("--boot", type=int, default=2000, help="bootstrap resamples for F1 intervals (0 = none)")
    ap.add_argument("--seed", type=int, default=20261118)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--out", help="write the report to this file instead of the screen")
    a = ap.parse_args(argv)
    labels = [x.strip() for x in a.labels.split(",") if x.strip()] if a.labels else None
    try:
        d = load_pairs(a.gold, a.pred, a.id_field, a.gold_field, a.pred_field)
        if a.compare and labels is None:
            d_b = load_pairs(a.gold, a.compare, a.id_field, a.gold_field, a.pred_field)
            labels = label_list(d["gold"], [x | y for x, y in zip(d["pred"], d_b["pred"])])
        result = {"run": summarise(d["gold"], d["pred"], labels, a.boot, a.seed),
                  "notes": {k: d[k] for k in ("missing", "unparsed", "not_in_gold")}}
        if a.compare:
            d2 = load_pairs(a.gold, a.compare, a.id_field, a.gold_field, a.pred_field)
            result["run_b"] = summarise(d2["gold"], d2["pred"], labels, a.boot, a.seed)
            result["notes_b"] = {k: d2[k] for k in ("missing", "unparsed", "not_in_gold")}
            result["comparison"] = compare(d["gold"], d["pred"], d2["pred"], labels, a.boot, a.seed)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        text = json.dumps(result, ensure_ascii=False, indent=1) + "\n"
    else:
        text = to_markdown(result["run"], result["notes"], "Run A" if a.compare else "Label metrics")
        if a.compare:
            text += "\n" + to_markdown(result["run_b"], result["notes_b"], "Run B") + "\n" + compare_markdown(result["comparison"])
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
