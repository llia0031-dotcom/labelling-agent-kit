# Analysis: smoke

## ad_policy / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 4 | 0.857 [0.67–1.00] | 0.889 [0.50–1.00] | 3/4 | 0/3 | 0/1 | 1.00 | 0.00 | 0.34 | 0 |
| prompt-rules | 4 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 4/4 | 0/3 | 0/1 | 1.00 | 0.00 | 0.72 | 0 |
| agent | 4 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 4/4 | 0/3 | 0/1 | 1.00 | 0.00 | 0.45 | 0 |
| agent-cases | 4 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 4/4 | 0/3 | 0/1 | 1.00 | 0.00 | 0.53 | 0 |
| agent-cases-check | 4 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 4/4 | 0/3 | 0/1 | 2.75 | 1.00 | 0.76 | 0 |

## asap / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 3 | 0.757 [0.55–0.86] | 0.633 [0.38–0.75] | 0/3 | – | – | 1.00 | 0.00 | 0.72 | 0 |
| prompt-rules | 3 | 0.737 [0.55–0.82] | 0.596 [0.38–0.69] | 0/3 | – | – | 1.00 | 0.00 | 0.98 | 0 |
| agent | 3 | 0.757 [0.55–0.86] | 0.633 [0.38–0.75] | 0/3 | – | – | 1.00 | 0.00 | 0.98 | 0 |
| agent-cases | 3 | 0.700 [0.55–0.80] | 0.596 [0.38–0.67] | 0/3 | – | – | 1.33 | 0.00 | 1.13 | 0 |
| agent-cases-check | 3 | 0.737 [0.60–0.82] | 0.623 [0.43–0.69] | 0/3 | – | – | 3.33 | 1.00 | 2.54 | 0 |

## Comparisons (B − A, micro F1, paired bootstrap 95%)

| Id | Task / set | A | B | Δ micro F1 | Δ macro F1 | McNemar p (exact match) | Verdict |
|---|---|---|---|---|---|---|---|
| T1 | ad_policy / dev | prompt-short | agent | +0.143 [+0.000, +0.333] | +0.111 [+0.000, +0.500] | 1.000 | no measured difference |
| T2 | asap / dev | prompt-short | nope | NOT RUN | | | |


# Details per arm

## ad_policy / dev / prompt-short

**ad_policy / dev / prompt-short: 4 items, 9 labels.** Micro F1 0.857 [0.67–1.00], macro F1 0.889 [0.50–1.00], exact match 3/4 (75.0%) [30–95].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| MEDICAL | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| GUARANTEE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| DISPARAGE | 0 | 0 | 0 | 0 | 0 | – | – | – |
| DATA | 0 | 0 | 0 | 0 | 0 | – | – | – |
| ALCOHOL | 0 | 0 | 0 | 0 | 0 | – | – | – |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 0 | 0 | 0 | 0 | 0 | – | – | – |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 3 | 4 | 3 | 1 | 0 | 75.0% | 100.0% | 0.857 [0.67–1.00] |

Miss rate (a labelled item predicted with no label): 0/3 (0.0%) [0–56]. False-alarm rate (an unlabelled item given a label): 0/1 (0.0%) [0–79].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 4/4 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 4/4; cost $0.0014 ($0.342 per 1,000 items).

Confusion: exact 3, under-labelled 0, over-labelled 1, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| GUARANTEE | ABSOLUTE | 1 | confused |

**Slices of 4 items.** Overall micro F1 0.857, exact match 75.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 4 | 0.857 [0.67–1.00] | 3/4 (75.0%) | 0/3 | 0/1 | – | too few |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 4 | 0.857 [0.67–1.00] | 3/4 (75.0%) | 0/3 | 0/1 | – | too few |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 3 | 0.857 [0.67–1.00] | 2/3 (66.7%) | – | – | – | too few |
| look-alike | 1 | – | 1/1 (100.0%) | – | – | – | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–24 chars | 1 | 0.667 [0.67–0.67] | 0/1 (0.0%) | – | – | -0.333 [-0.33 to -0.33] | too few |
| 25–26 chars | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.333 [+0.33 to +0.33] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 1 | – | 1/1 (100.0%) | – | – | – | too few |
| ABSOLUTE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.200 [+0.00 to +0.33] | too few |
| GUARANTEE | 1 | 0.667 [0.67–0.67] | 0/1 (0.0%) | – | – | -0.333 [-0.33 to -0.33] | too few |
| MEDICAL | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.200 [+0.00 to +0.33] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / prompt-rules

**ad_policy / dev / prompt-rules: 4 items, 9 labels.** Micro F1 1.000 [1.00–1.00], macro F1 1.000 [1.00–1.00], exact match 4/4 (100.0%) [51–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| MEDICAL | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| GUARANTEE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| DISPARAGE | 0 | 0 | 0 | 0 | 0 | – | – | – |
| DATA | 0 | 0 | 0 | 0 | 0 | – | – | – |
| ALCOHOL | 0 | 0 | 0 | 0 | 0 | – | – | – |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 0 | 0 | 0 | 0 | 0 | – | – | – |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 3 | 3 | 3 | 0 | 0 | 100.0% | 100.0% | 1.000 [1.00–1.00] |

Miss rate (a labelled item predicted with no label): 0/3 (0.0%) [0–56]. False-alarm rate (an unlabelled item given a label): 0/1 (0.0%) [0–79].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 4/4 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 3/3; cost $0.0029 ($0.720 per 1,000 items).

Confusion: exact 4, under-labelled 0, over-labelled 0, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|

**Slices of 4 items.** Overall micro F1 1.000, exact match 100.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | – | – | – | too few |
| look-alike | 1 | – | 1/1 (100.0%) | – | – | – | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–24 chars | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| 25–26 chars | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.000 [+0.00 to +0.00] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 1 | – | 1/1 (100.0%) | – | – | – | too few |
| ABSOLUTE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| GUARANTEE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| MEDICAL | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent

**ad_policy / dev / agent: 4 items, 9 labels.** Micro F1 1.000 [1.00–1.00], macro F1 1.000 [1.00–1.00], exact match 4/4 (100.0%) [51–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| MEDICAL | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| GUARANTEE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| DISPARAGE | 0 | 0 | 0 | 0 | 0 | – | – | – |
| DATA | 0 | 0 | 0 | 0 | 0 | – | – | – |
| ALCOHOL | 0 | 0 | 0 | 0 | 0 | – | – | – |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 0 | 0 | 0 | 0 | 0 | – | – | – |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 3 | 3 | 3 | 0 | 0 | 100.0% | 100.0% | 1.000 [1.00–1.00] |

Miss rate (a labelled item predicted with no label): 0/3 (0.0%) [0–56]. False-alarm rate (an unlabelled item given a label): 0/1 (0.0%) [0–79].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 4/4 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 3/3; cost $0.0018 ($0.452 per 1,000 items).

Confusion: exact 4, under-labelled 0, over-labelled 0, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|

**Slices of 4 items.** Overall micro F1 1.000, exact match 100.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | – | – | – | too few |
| look-alike | 1 | – | 1/1 (100.0%) | – | – | – | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–24 chars | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| 25–26 chars | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.000 [+0.00 to +0.00] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 1 | – | 1/1 (100.0%) | – | – | – | too few |
| ABSOLUTE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| GUARANTEE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| MEDICAL | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases

**ad_policy / dev / agent-cases: 4 items, 9 labels.** Micro F1 1.000 [1.00–1.00], macro F1 1.000 [1.00–1.00], exact match 4/4 (100.0%) [51–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| MEDICAL | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| GUARANTEE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| DISPARAGE | 0 | 0 | 0 | 0 | 0 | – | – | – |
| DATA | 0 | 0 | 0 | 0 | 0 | – | – | – |
| ALCOHOL | 0 | 0 | 0 | 0 | 0 | – | – | – |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 0 | 0 | 0 | 0 | 0 | – | – | – |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 3 | 3 | 3 | 0 | 0 | 100.0% | 100.0% | 1.000 [1.00–1.00] |

Miss rate (a labelled item predicted with no label): 0/3 (0.0%) [0–56]. False-alarm rate (an unlabelled item given a label): 0/1 (0.0%) [0–79].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 4/4 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 3/3; cost $0.0021 ($0.526 per 1,000 items).

Confusion: exact 4, under-labelled 0, over-labelled 0, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|

**Slices of 4 items.** Overall micro F1 1.000, exact match 100.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | – | – | – | too few |
| look-alike | 1 | – | 1/1 (100.0%) | – | – | – | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–24 chars | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| 25–26 chars | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.000 [+0.00 to +0.00] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 1 | – | 1/1 (100.0%) | – | – | – | too few |
| ABSOLUTE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| GUARANTEE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| MEDICAL | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases-check

**ad_policy / dev / agent-cases-check: 4 items, 9 labels.** Micro F1 1.000 [1.00–1.00], macro F1 1.000 [1.00–1.00], exact match 4/4 (100.0%) [51–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| MEDICAL | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| GUARANTEE | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| DISPARAGE | 0 | 0 | 0 | 0 | 0 | – | – | – |
| DATA | 0 | 0 | 0 | 0 | 0 | – | – | – |
| ALCOHOL | 0 | 0 | 0 | 0 | 0 | – | – | – |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 0 | 0 | 0 | 0 | 0 | – | – | – |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 3 | 3 | 3 | 0 | 0 | 100.0% | 100.0% | 1.000 [1.00–1.00] |

Miss rate (a labelled item predicted with no label): 0/3 (0.0%) [0–56]. False-alarm rate (an unlabelled item given a label): 0/1 (0.0%) [0–79].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 4/4 answered; 2.75 calls and 1.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 4 items (+0 / −0 labels); exact quotes 3/3; cost $0.0030 ($0.756 per 1,000 items).

Confusion: exact 4, under-labelled 0, over-labelled 0, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|

**Slices of 4 items.** Overall micro F1 1.000, exact match 100.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/3 | 0/1 | – | too few |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | – | – | – | too few |
| look-alike | 1 | – | 1/1 (100.0%) | – | – | – | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–24 chars | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| 25–26 chars | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.000 [+0.00 to +0.00] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 1 | – | 1/1 (100.0%) | – | – | – | too few |
| ABSOLUTE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| GUARANTEE | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |
| MEDICAL | 1 | 1.000 [1.00–1.00] | 1/1 (100.0%) | – | – | +0.000 [+0.00 to +0.00] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-short

**asap / dev / prompt-short: 3 items, 18 labels.** Micro F1 0.757 [0.55–0.86], macro F1 0.633 [0.38–0.75], exact match 0/3 (0.0%) [0–56].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Food#Appearance | 1 | 1 | 0 | 1 | 1 | 0.0% [0–79] | 0.0% [0–79] | 0.000 [0.00–0.00] |
| Food#Portion | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Food#Recommend | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Price#Level | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Price#Cost_effective | 2 | 3 | 2 | 1 | 0 | 66.7% [21–94] | 100.0% [34–100] | 0.800 [0.00–1.00] |
| Price#Discount | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Downtown | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Location#Transportation | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Easy_to_find | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Service#Queue | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Hospitality | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Service#Parking | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Timely | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Decoration | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Ambience#Noise | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Space | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Sanitary | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| **micro** | 17 | 20 | 14 | 6 | 3 | 70.0% | 82.4% | 0.757 [0.55–0.86] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 3/3 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 20/20; cost $0.0021 ($0.715 per 1,000 items).

Confusion: exact 0, under-labelled 1, over-labelled 1, swapped 1.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Appearance | (no predicted label) | 1 | missed |
| Food#Taste | Ambience#Decoration | 1 | confused |
| Food#Taste | Ambience#Space | 1 | confused |
| Food#Taste | Food#Appearance | 1 | confused |
| Food#Taste | Food#Recommend | 1 | confused |
| Food#Taste | Price#Cost_effective | 1 | confused |
| Location#Downtown | Service#Hospitality | 1 | confused |
| Location#Easy_to_find | Service#Hospitality | 1 | confused |
| Price#Level | Ambience#Decoration | 1 | confused |
| Price#Level | Ambience#Space | 1 | confused |

**Slices of 3 items.** Overall micro F1 0.757, exact match 0.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 4-5 stars | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.232 [-0.31 to -0.06] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 1-4 labels | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.232 [-0.31 to -0.06] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 2 | 0.846 [0.80–0.86] | 0/2 (0.0%) | – | – | +0.301 [+0.25 to +0.31] | too few |
| no neutral mention | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 450–573 chars | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 574–584 chars | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.050 [-0.06 to +0.25] | too few |
| 585–585 chars | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Ambience#Sanitary | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Appearance | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.050 [-0.06 to +0.25] | too few |
| Food#Portion | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Recommend | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Taste | 3 | 0.757 [0.55–0.86] | 0/3 (0.0%) | – | – | – | too few |
| Location#Downtown | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Location#Easy_to_find | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Location#Transportation | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Price#Cost_effective | 2 | 0.846 [0.80–0.86] | 0/2 (0.0%) | – | – | +0.301 [+0.25 to +0.31] | too few |
| Price#Discount | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Price#Level | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |
| Service#Parking | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Service#Queue | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-rules

**asap / dev / prompt-rules: 3 items, 18 labels.** Micro F1 0.737 [0.55–0.82], macro F1 0.596 [0.38–0.69], exact match 0/3 (0.0%) [0–56].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Food#Appearance | 1 | 1 | 0 | 1 | 1 | 0.0% [0–79] | 0.0% [0–79] | 0.000 [0.00–0.00] |
| Food#Portion | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Food#Recommend | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Price#Level | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Price#Cost_effective | 2 | 3 | 2 | 1 | 0 | 66.7% [21–94] | 100.0% [34–100] | 0.800 [0.00–1.00] |
| Price#Discount | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Downtown | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Location#Transportation | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Easy_to_find | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Service#Queue | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Hospitality | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Service#Parking | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Timely | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Decoration | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Ambience#Noise | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Space | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Sanitary | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| **micro** | 17 | 21 | 14 | 7 | 3 | 66.7% | 82.4% | 0.737 [0.55–0.82] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 3/3 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 21/21; cost $0.0029 ($0.979 per 1,000 items).

Confusion: exact 0, under-labelled 1, over-labelled 1, swapped 1.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Appearance | (no predicted label) | 1 | missed |
| Food#Taste | Ambience#Decoration | 1 | confused |
| Food#Taste | Ambience#Space | 1 | confused |
| Food#Taste | Food#Appearance | 1 | confused |
| Food#Taste | Food#Recommend | 1 | confused |
| Food#Taste | Price#Cost_effective | 1 | confused |
| Location#Downtown | Service#Hospitality | 1 | confused |
| Location#Downtown | Service#Timely | 1 | confused |
| Location#Easy_to_find | Service#Hospitality | 1 | confused |
| Location#Easy_to_find | Service#Timely | 1 | confused |

**Slices of 3 items.** Overall micro F1 0.737, exact match 0.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| 4-5 stars | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.193 [-0.27 to -0.02] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| 1-4 labels | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.193 [-0.27 to -0.02] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 2 | 0.815 [0.80–0.82] | 0/2 (0.0%) | – | – | +0.269 [+0.25 to +0.27] | too few |
| no neutral mention | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.269 [-0.27 to -0.25] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 450–573 chars | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| 574–584 chars | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.073 [-0.02 to +0.25] | too few |
| 585–585 chars | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.269 [-0.27 to -0.25] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Ambience#Sanitary | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Food#Appearance | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.073 [-0.02 to +0.25] | too few |
| Food#Portion | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Food#Recommend | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Food#Taste | 3 | 0.737 [0.55–0.82] | 0/3 (0.0%) | – | – | – | too few |
| Location#Downtown | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Location#Easy_to_find | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Location#Transportation | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Price#Cost_effective | 2 | 0.815 [0.80–0.82] | 0/2 (0.0%) | – | – | +0.269 [+0.25 to +0.27] | too few |
| Price#Discount | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Price#Level | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.269 [-0.27 to -0.25] | too few |
| Service#Parking | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.02 to +0.27] | too few |
| Service#Queue | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.269 [-0.27 to -0.25] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent

**asap / dev / agent: 3 items, 18 labels.** Micro F1 0.757 [0.55–0.86], macro F1 0.633 [0.38–0.75], exact match 0/3 (0.0%) [0–56].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Food#Appearance | 1 | 1 | 0 | 1 | 1 | 0.0% [0–79] | 0.0% [0–79] | 0.000 [0.00–0.00] |
| Food#Portion | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Food#Recommend | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Price#Level | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Price#Cost_effective | 2 | 3 | 2 | 1 | 0 | 66.7% [21–94] | 100.0% [34–100] | 0.800 [0.00–1.00] |
| Price#Discount | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Downtown | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Location#Transportation | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Easy_to_find | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Service#Queue | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Hospitality | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Service#Parking | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Timely | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Decoration | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Ambience#Noise | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Space | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Sanitary | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| **micro** | 17 | 20 | 14 | 6 | 3 | 70.0% | 82.4% | 0.757 [0.55–0.86] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 3/3 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 20/20; cost $0.0029 ($0.976 per 1,000 items).

Confusion: exact 0, under-labelled 1, over-labelled 1, swapped 1.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Appearance | (no predicted label) | 1 | missed |
| Food#Taste | Ambience#Decoration | 1 | confused |
| Food#Taste | Ambience#Space | 1 | confused |
| Food#Taste | Food#Appearance | 1 | confused |
| Food#Taste | Food#Recommend | 1 | confused |
| Food#Taste | Price#Cost_effective | 1 | confused |
| Location#Downtown | Service#Hospitality | 1 | confused |
| Location#Easy_to_find | Service#Hospitality | 1 | confused |
| Price#Level | Ambience#Decoration | 1 | confused |
| Price#Level | Ambience#Space | 1 | confused |

**Slices of 3 items.** Overall micro F1 0.757, exact match 0.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 4-5 stars | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.232 [-0.31 to -0.06] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 1-4 labels | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.232 [-0.31 to -0.06] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 2 | 0.846 [0.80–0.86] | 0/2 (0.0%) | – | – | +0.301 [+0.25 to +0.31] | too few |
| no neutral mention | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 450–573 chars | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| 574–584 chars | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.050 [-0.06 to +0.25] | too few |
| 585–585 chars | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Ambience#Sanitary | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Appearance | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.050 [-0.06 to +0.25] | too few |
| Food#Portion | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Recommend | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Food#Taste | 3 | 0.757 [0.55–0.86] | 0/3 (0.0%) | – | – | – | too few |
| Location#Downtown | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Location#Easy_to_find | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Location#Transportation | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Price#Cost_effective | 2 | 0.846 [0.80–0.86] | 0/2 (0.0%) | – | – | +0.301 [+0.25 to +0.31] | too few |
| Price#Discount | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Price#Level | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |
| Service#Parking | 1 | 0.857 [0.86–0.86] | 0/1 (0.0%) | – | – | +0.232 [+0.06 to +0.31] | too few |
| Service#Queue | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.301 [-0.31 to -0.25] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases

**asap / dev / agent-cases: 3 items, 18 labels.** Micro F1 0.700 [0.55–0.80], macro F1 0.596 [0.38–0.67], exact match 0/3 (0.0%) [0–56].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Food#Appearance | 1 | 2 | 0 | 2 | 1 | 0.0% [0–66] | 0.0% [0–79] | 0.000 [0.00–0.00] |
| Food#Portion | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Food#Recommend | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Price#Level | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Price#Cost_effective | 2 | 3 | 2 | 1 | 0 | 66.7% [21–94] | 100.0% [34–100] | 0.800 [0.00–1.00] |
| Price#Discount | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Downtown | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Location#Transportation | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Easy_to_find | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Service#Queue | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Hospitality | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Service#Parking | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Timely | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Decoration | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Ambience#Noise | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Space | 0 | 2 | 0 | 2 | 0 | 0.0% [0–66] | – | 0.000 [0.00–0.00] |
| Ambience#Sanitary | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| **micro** | 17 | 23 | 14 | 9 | 3 | 60.9% | 82.4% | 0.700 [0.55–0.80] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 3/3 answered; 1.33 calls and 0.00 tool calls per item; rule gate 0, quote repair 1, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 23/23; cost $0.0034 ($1.129 per 1,000 items).

Confusion: exact 0, under-labelled 1, over-labelled 1, swapped 1.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Appearance | (no predicted label) | 1 | missed |
| Food#Taste | Ambience#Decoration | 1 | confused |
| Food#Taste | Ambience#Space | 1 | confused |
| Food#Taste | Food#Appearance | 1 | confused |
| Food#Taste | Food#Recommend | 1 | confused |
| Food#Taste | Price#Cost_effective | 1 | confused |
| Location#Downtown | Ambience#Space | 1 | confused |
| Location#Downtown | Food#Appearance | 1 | confused |
| Location#Downtown | Service#Hospitality | 1 | confused |
| Location#Downtown | Service#Timely | 1 | confused |

**Slices of 3 items.** Overall micro F1 0.700, exact match 0.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| 4-5 stars | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.125 [-0.20 to +0.05] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| 1-4 labels | 2 | 0.625 [0.55–0.80] | 0/2 (0.0%) | – | – | -0.125 [-0.20 to +0.05] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 2 | 0.759 [0.75–0.80] | 0/2 (0.0%) | – | – | +0.213 [+0.20 to +0.25] | too few |
| no neutral mention | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.213 [-0.25 to -0.20] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 450–573 chars | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| 574–584 chars | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.114 [+0.05 to +0.25] | too few |
| 585–585 chars | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.213 [-0.25 to -0.20] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Ambience#Sanitary | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Food#Appearance | 1 | 0.800 [0.80–0.80] | 0/1 (0.0%) | – | – | +0.114 [+0.05 to +0.25] | too few |
| Food#Portion | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Food#Recommend | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Food#Taste | 3 | 0.700 [0.55–0.80] | 0/3 (0.0%) | – | – | – | too few |
| Location#Downtown | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Location#Easy_to_find | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Location#Transportation | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Price#Cost_effective | 2 | 0.759 [0.75–0.80] | 0/2 (0.0%) | – | – | +0.213 [+0.20 to +0.25] | too few |
| Price#Discount | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Price#Level | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.213 [-0.25 to -0.20] | too few |
| Service#Parking | 1 | 0.750 [0.75–0.75] | 0/1 (0.0%) | – | – | +0.125 [-0.05 to +0.20] | too few |
| Service#Queue | 1 | 0.545 [0.55–0.55] | 0/1 (0.0%) | – | – | -0.213 [-0.25 to -0.20] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases-check

**asap / dev / agent-cases-check: 3 items, 18 labels.** Micro F1 0.737 [0.60–0.82], macro F1 0.623 [0.43–0.69], exact match 0/3 (0.0%) [0–56].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Food#Appearance | 1 | 1 | 0 | 1 | 1 | 0.0% [0–79] | 0.0% [0–79] | 0.000 [0.00–0.00] |
| Food#Portion | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Food#Recommend | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Price#Level | 1 | 3 | 1 | 2 | 0 | 33.3% [6–79] | 100.0% [21–100] | 0.500 [0.00–1.00] |
| Price#Cost_effective | 2 | 3 | 2 | 1 | 0 | 66.7% [21–94] | 100.0% [34–100] | 0.800 [0.00–1.00] |
| Price#Discount | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Downtown | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| Location#Transportation | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Location#Easy_to_find | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Queue | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Hospitality | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Service#Parking | 1 | 1 | 1 | 0 | 0 | 100.0% [21–100] | 100.0% [21–100] | 1.000 |
| Service#Timely | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Decoration | 1 | 2 | 1 | 1 | 0 | 50.0% [9–91] | 100.0% [21–100] | 0.667 [0.00–1.00] |
| Ambience#Noise | 0 | 0 | 0 | 0 | 0 | – | – | – |
| Ambience#Space | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| Ambience#Sanitary | 1 | 0 | 0 | 0 | 1 | – | 0.0% [0–79] | 0.000 |
| **micro** | 17 | 21 | 14 | 7 | 3 | 66.7% | 82.4% | 0.737 [0.60–0.82] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 3/3 answered; 3.33 calls and 1.00 tool calls per item; rule gate 0, quote repair 1, self-check changed 3 of 3 items (+3 / −4 labels); exact quotes 21/21; cost $0.0076 ($2.541 per 1,000 items).

Confusion: exact 0, under-labelled 0, over-labelled 1, swapped 2.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Ambience#Sanitary | Price#Level | 1 | confused |
| Ambience#Sanitary | Service#Hospitality | 1 | confused |
| Food#Appearance | Price#Level | 1 | confused |
| Food#Taste | Ambience#Decoration | 1 | confused |
| Food#Taste | Ambience#Space | 1 | confused |
| Food#Taste | Food#Appearance | 1 | confused |
| Food#Taste | Price#Cost_effective | 1 | confused |
| Location#Downtown | Price#Level | 1 | confused |
| Location#Downtown | Service#Hospitality | 1 | confused |
| Price#Level | Ambience#Decoration | 1 | confused |

**Slices of 3 items.** Overall micro F1 0.737, exact match 0.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| 4-5 stars | 2 | 0.625 [0.60–0.67] | 0/2 (0.0%) | – | – | -0.193 [-0.22 to -0.15] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| 1-4 labels | 2 | 0.625 [0.60–0.67] | 0/2 (0.0%) | – | – | -0.193 [-0.22 to -0.15] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 2 | 0.786 [0.67–0.82] | 0/2 (0.0%) | – | – | +0.186 [+0.07 to +0.22] | too few |
| no neutral mention | 1 | 0.600 [0.60–0.60] | 0/1 (0.0%) | – | – | -0.186 [-0.22 to -0.07] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 450–573 chars | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| 574–584 chars | 1 | 0.667 [0.67–0.67] | 0/1 (0.0%) | – | – | -0.083 [-0.15 to +0.07] | too few |
| 585–585 chars | 1 | 0.600 [0.60–0.60] | 0/1 (0.0%) | – | – | -0.186 [-0.22 to -0.07] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Ambience#Sanitary | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Food#Appearance | 1 | 0.667 [0.67–0.67] | 0/1 (0.0%) | – | – | -0.083 [-0.15 to +0.07] | too few |
| Food#Portion | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Food#Recommend | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Food#Taste | 3 | 0.737 [0.60–0.82] | 0/3 (0.0%) | – | – | – | too few |
| Location#Downtown | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Location#Easy_to_find | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Location#Transportation | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Price#Cost_effective | 2 | 0.786 [0.67–0.82] | 0/2 (0.0%) | – | – | +0.186 [+0.07 to +0.22] | too few |
| Price#Discount | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Price#Level | 1 | 0.600 [0.60–0.60] | 0/1 (0.0%) | – | – | -0.186 [-0.22 to -0.07] | too few |
| Service#Parking | 1 | 0.818 [0.82–0.82] | 0/1 (0.0%) | – | – | +0.193 [+0.15 to +0.22] | too few |
| Service#Queue | 1 | 0.600 [0.60–0.60] | 0/1 (0.0%) | – | – | -0.186 [-0.22 to -0.07] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


