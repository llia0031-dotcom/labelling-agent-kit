# Tutorial: find what a weak label is mistaken for

Files in `examples/`: `gold.jsonl` (86 ads, labels fixed when each ad was written) and `pred_short.jsonl` (labels from a short prompt). `label-metrics` showed that this run gives ABSOLUTE too freely. Output below copied from a real run.

```bash
python scripts/confusion_report.py examples/gold.jsonl examples/pred_short.jsonl --top 6
```

```text
**Confusion over 86 items.** Exact 67, under-labelled 6, over-labelled 13, swapped 0.

| gold \ predicted | ABSOLUTE | ... | GUARANTEE | ... | (no predicted label) |
| **ABSOLUTE**     | 10       |     | ·         |     | 2 |
| **DISPARAGE**    | 1        |     | ·         |     | 4 |
| **GUARANTEE**    | 6        |     | 14        |     | · |
| **(no gold label)** | 2     |     | ·         |     | 35 |

| Gold | Predicted | Count | Kind | Example ids |
| GUARANTEE | ABSOLUTE | 6 | confused | en-d12, syn-val-047, syn-val-048, syn-val-055, syn-val-059 |
| DISPARAGE | (no predicted label) | 4 | missed | syn-val-045, syn-val-046, syn-val-050, syn-val-057 |
| (no gold label) | ABSOLUTE | 2 | added to an unlabelled item | syn-val-008, zh-d11 |
```

## Read it

1. **GUARANTEE → ABSOLUTE, 6 times, "confused".** Every one of these items was right about GUARANTEE (diagonal 14 of 14) and also got ABSOLUTE. The ads promise a result in strong words ("100% pass rate", "绝对没问题"). The rule boundary is: a promised outcome is GUARANTEE; ABSOLUTE is only for superlatives and rank. Fix: a boundary sentence between the two labels, which the rulebook has (`label-rules between ABSOLUTE GUARANTEE`); the short prompt does not show it.
2. **DISPARAGE → (no predicted label), 4 misses.** Open the ids: three run down rivals without naming one ("the entry-level earphones they usually use", "another brand of earphones", "cheap so-called sunscreens"). Fix: an *applies when* entry for unnamed rivals. Check the gold first: these four are synthetic validation ads, and the fourth (syn-val-046) disparages nothing.
3. **(no gold label) → ABSOLUTE, 2 false alarms.** zh-d11 states a sales rank limited to a time and a platform with its source (a fact the SAMR guide exempts). Fix: the exemption is in the rulebook's *does not apply* list.

Each confused pair names the items to keep as a regression set: after the fix, those ids should flip and nothing else should.
