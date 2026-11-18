---
name: label-metrics
description: Scores a labelling run against gold labels - precision, recall and F1 for every label with 95% intervals, micro and macro F1, exact-match rate, and miss and false-alarm rates - and compares two runs on the same items with a paired test. Use it whenever someone wants to know how good a classifier, labelling agent, moderation model or annotation batch is, or whether a new prompt or model version is really better - for example "score these predictions", "precision and recall per label", "compute F1 for my labelling agent", "is version B better than version A", "标注结果算一下 P/R/F1", "每个标签的准确率召回率", "两版提示词哪个好". Works for multi-label and single-label tasks. A bundled script does the counting and the statistics so the numbers are exact and reproducible; the agent reads them and says what they mean.
metadata:
  version: "0.1.0"
---

# Label metrics

A single accuracy number hides where a labeller fails. Score every label separately, put an interval on every rate, and only call a difference real when its interval excludes zero. The bundled script does the arithmetic; your job is to read it honestly.

## Inputs

Two JSONL files with one line per item and a shared `id`:

```json
{"id": "ad-017", "labels": ["ABSOLUTE", "DATA"]}
```

- **Gold**: the reference labels (from the dataset, or fixed when the item was written).
- **Predictions**: what the run produced. An empty list means "no label applies".
- Other fields are ignored; `--gold-field`, `--pred-field` and `--id-field` read other names, and `meta.lang` style paths work.

If the user has a CSV or a spreadsheet, convert it to this shape first.

## Run the script

```bash
python <this-skill-folder>/scripts/label_metrics.py gold.jsonl pred.jsonl
python <this-skill-folder>/scripts/label_metrics.py gold.jsonl pred_a.jsonl --compare pred_b.jsonl
```

Python 3.9+, standard library only. `--format json` gives every number; `--labels A,B,C` fixes the label list and order (labels never predicted still appear); `--boot 0` skips the bootstrap for speed. Exit code 0: report written; 2: an input could not be read.

What it computes (definitions in `references/metrics.md`):

- per label: TP, FP, FN, precision and recall with Wilson 95% intervals, F1 with a bootstrap interval over items
- micro F1 (every label decision counts once), macro F1 (every label counts once), exact match, Hamming loss
- when some items have no gold label: miss rate (a labelled item left empty) and false-alarm rate (an unlabelled item given a label)
- `--compare`: the paired difference in micro and macro F1 with a bootstrap interval, and an exact McNemar test on exact match

Items with no prediction line, or a prediction without a label list, count as "no label" and are listed under the table. Report them: a run that fails silently looks better than it is.

## Read the result

1. **Lead with the measure that matches the decision.** Micro F1 for overall quality when frequent labels matter most; macro F1 when rare labels matter as much; miss and false-alarm rates for moderation, where the two errors cost different things.
2. **Name the weakest labels**, with their support. A label with 5 gold items and recall 40% is 2 of 5: say so, and say the interval is wide.
3. **Precision or recall?** Low precision = the label is given too freely (look at false positives); low recall = it is missed (look at misses). Hand the next step to `confusion-report` (which labels it is confused with) or `slice-report` (where it fails).
4. **Comparisons**: B is better only when the interval of the difference is above zero. If it includes zero, write "no measured difference", not "slightly better". With McNemar, report how many items only A got right and only B got right.

## Report

The shape, with the numbers of the example in `references/tutorial.md` (86 ads, a short prompt against the same prompt with the rulebook):

```markdown
**Short prompt on 86 ads: micro F1 0.816 [0.74–0.88]. Two labels are weak: ABSOLUTE is given too freely (precision 52.6%, 10 of 19) and DISPARAGE is missed (recall 50.0%, 4 of 8; small support, wide interval).**

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 19 | 10 | 9 | 2 | 52.6% [32–73] | 83.3% [55–95] | 0.645 [0.42–0.83] |

With the rulebook on the same items: micro F1 +0.090 [+0.029 to +0.157], a measured improvement; macro F1 +0.055 [-0.014 to +0.137], no measured difference. Only the rulebook prompt exact on 12 items, only the short prompt on 1 (McNemar p = 0.003).
```

Never round a rate into a stronger claim, never drop a label from the table because it looks bad, and keep the item count next to every percentage.
