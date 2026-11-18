# Tutorial: score two prompts and decide whether the second is better

Files in `examples/`: `gold.jsonl` (86 ads in Chinese and English, labels fixed when each ad was written), `pred_short.jsonl` (labels from a short prompt with only the label list) and `pred_rules.jsonl` (the same prompt with the whole rulebook added). Outputs below are copied from real runs.

## 1. Score one run

```bash
python scripts/label_metrics.py examples/gold.jsonl examples/pred_short.jsonl
```

```text
**Label metrics: 86 items, 8 labels.** Micro F1 0.816 [0.74–0.88], ... exact match 67/86 (77.9%) [68–85].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
| ABSOLUTE | 12 | 19 | 10 | 9 | 2 | 52.6% [32–73] | 83.3% [55–95] | 0.645 [0.42–0.83] |
| DISPARAGE | 8 | 5 | 4 | 1 | 4 | 80.0% [38–96] | 50.0% [22–78] | 0.615 [0.20–0.89] |
...
Miss rate ...: 4/45 (8.9%) [4–21]. False-alarm rate ...: 6/41 (14.6%) [7–28].
```

Read it per label. ABSOLUTE is given too freely (precision 52.6%: 9 of its 19 uses are wrong); DISPARAGE is missed (recall 50.0%: 4 of 8). The intervals are wide because the supports are small: 8 gold items for DISPARAGE.

## 2. Compare with the second prompt on the same items

```bash
python scripts/label_metrics.py examples/gold.jsonl examples/pred_short.jsonl --compare examples/pred_rules.jsonl
```

```text
| Measure | A | B | Difference (B − A) |
| Micro F1 | 0.816 | 0.905 | +0.090 [+0.029 to +0.157] |
| Macro F1 | 0.871 | 0.925 | +0.055 [-0.014 to +0.137] |

Exact match: only A right on 1 item, only B right on 12, both right on 66, both wrong on 7; exact McNemar p = 0.003.
```

- **Micro F1**: the interval of the difference is above 0, so the rulebook prompt is measurably better overall.
- **Macro F1**: the interval includes 0. Write "no measured difference in macro F1", not "slightly better".
- **McNemar**: 12 items only B got exactly right against 1 for A.

The per-label table under it shows where the gain comes from: ABSOLUTE F1 0.645 → 0.800 (false positives 9 → 3, the rulebook's "does not apply" entries at work).

## 3. Next steps

- Which labels does ABSOLUTE get confused with? → `confusion-report` on the same files.
- Is the short prompt worse on Chinese ads or on look-alikes? → `slice-report --by meta.lang --by meta.difficulty`.
