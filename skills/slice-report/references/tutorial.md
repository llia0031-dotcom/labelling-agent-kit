# Tutorial: is the labeller weaker on one kind of item?

Files in `examples/`: `gold.jsonl` (86 ads with `meta.lang`, `meta.source` and `meta.difficulty`: violating, look-alike or plain) and `pred_short.jsonl`. Output below copied from a real run.

```bash
python scripts/slice_report.py examples/gold.jsonl examples/pred_short.jsonl --by meta.difficulty --by meta.lang
```

```text
### By meta.difficulty
| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
| violating  | 45 | 0.866 [0.81–0.92] | 32/45 (71.1%) | 4/45 | – | -0.143 [-0.32 to +0.04] (exact match) | no measured difference |
| look-alike | 27 | –                 | 22/27 (81.5%) | –    | 5/27 | +0.052 [-0.13 to +0.22] (exact match) | no measured difference |
| plain      | 14 | –                 | 13/14 (92.9%) | –    | 1/14 | +0.179 [-0.01 to +0.33] (exact match) | too few |

### By meta.lang
| en | 39 | 0.905 [0.80–0.98] | 35/39 (89.7%) | 1/20 | 2/19 | +0.151 [+0.02 to +0.29] | better |
| zh | 47 | 0.754 [0.65–0.85] | 32/47 (68.1%) | 3/25 | 4/22 | -0.151 [-0.28 to -0.01] | worse |
```

## Read it

1. **Chinese ads are measurably worse** (micro F1 0.151 lower than English, interval −0.28 to −0.01). Before blaming the language, cut by label: the Chinese label set has DATA and FLAG, the English one WEIGHT and BEFORE_AFTER. The confusion matrix of the Chinese items shows the largest group of their 15 wrong label decisions: 5 GUARANTEE ads also given ABSOLUTE, then 4 missed DISPARAGE.
2. **Look-alikes** have no gold label, so F1 is not defined there ("–") and the slice is compared on exact match; the false-alarm count is the number to watch: 5 of 27 look-alike ads got a label.
3. **Plain ads** (14) are under the minimum of 20 items: no verdict, read the items instead.
4. Difficulty slices with no measured difference do not mean the labeller is equally good on them: the intervals are wide at this size.

Slices of the input (language, source, length) tell you where a labeller is safe to deploy; slices defined by the gold labels (difficulty, number of labels) explain errors.
