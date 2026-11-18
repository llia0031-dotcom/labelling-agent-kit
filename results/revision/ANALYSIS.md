# Analysis: revision

## ad_policy / test_b

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| agent-cases-check | 118 | 0.971 [0.94–0.99] | 0.971 [0.93–1.00] | 114/118 | 0/61 | 2/57 | 2.89 | 0.53 | 0.52 | 0 |
| agent-cases-check-v2 | 118 | 0.993 [0.98–1.00] | 0.989 [0.95–1.00] | 117/118 | 0/61 | 1/57 | 2.96 | 0.61 | 0.56 | 0 |

## ad_policy / test_a

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| agent-cases-check | 119 | 0.971 [0.94–0.99] | 0.967 [0.92–1.00] | 115/119 | 1/67 | 0/52 | 2.96 | 0.55 | 0.53 | 0 |
| agent-cases-check-v2 | 119 | 0.986 [0.96–1.00] | 0.980 [0.94–1.00] | 117/119 | 0/67 | 2/52 | 2.91 | 0.45 | 0.54 | 0 |

## asap / test_b

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| agent-cases-check | 199 | 0.834 [0.82–0.85] | 0.799 [0.77–0.82] | 37/199 | – | – | 3.41 | 0.26 | 1.60 | 0 |
| agent-cases-check-v2 | 199 | 0.852 [0.83–0.87] | 0.821 [0.80–0.84] | 43/199 | – | – | 3.29 | 0.08 | 1.62 | 0 |

## asap / test_a

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| agent-cases-check | 201 | 0.824 [0.80–0.84] | 0.789 [0.76–0.81] | 36/201 | 0/199 | 0/2 | 3.40 | 0.26 | 1.59 | 0 |
| agent-cases-check-v2 | 201 | 0.841 [0.82–0.86] | 0.812 [0.79–0.83] | 36/201 | 0/199 | 0/2 | 3.26 | 0.04 | 1.64 | 0 |

## Comparisons (B − A, micro F1, paired bootstrap 95%)

| Id | Task / set | A | B | Δ micro F1 | Δ macro F1 | McNemar p (exact match) | Verdict |
|---|---|---|---|---|---|---|---|
| H6-ad | ad_policy / test_b | agent-cases-check | agent-cases-check-v2 | +0.021 [+0.000, +0.048] | +0.018 [+0.000, +0.047] | 0.250 | no measured difference |
| H6-asap | asap / test_b | agent-cases-check | agent-cases-check-v2 | +0.018 [+0.005, +0.031] | +0.022 [+0.006, +0.039] | 0.377 | B better |
| R-ad | ad_policy / test_a | agent-cases-check | agent-cases-check-v2 | +0.014 [-0.018, +0.048] | +0.014 [-0.044, +0.069] | 0.688 | no measured difference |
| R-asap | asap / test_a | agent-cases-check | agent-cases-check-v2 | +0.017 [+0.003, +0.031] | +0.023 [+0.007, +0.040] | 1.000 | B better |


# Details per arm

## ad_policy / test_b / agent-cases-check

**ad_policy / test_b / agent-cases-check: 118 items, 9 labels.** Micro F1 0.971 [0.94–0.99], macro F1 0.971 [0.93–1.00], exact match 114/118 (96.6%) [92–99].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 17 | 17 | 17 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| MEDICAL | 11 | 11 | 11 | 0 | 0 | 100.0% [74–100] | 100.0% [74–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 15 | 17 | 15 | 2 | 0 | 88.2% [66–97] | 100.0% [80–100] | 0.938 [0.82–1.00] |
| DISPARAGE | 6 | 6 | 6 | 0 | 0 | 100.0% [61–100] | 100.0% [61–100] | 1.000 [1.00–1.00] |
| DATA | 6 | 6 | 6 | 0 | 0 | 100.0% [61–100] | 100.0% [61–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 6 | 7 | 6 | 1 | 0 | 85.7% [49–97] | 100.0% [61–100] | 0.923 [0.67–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 7 | 8 | 7 | 1 | 0 | 87.5% [53–98] | 100.0% [65–100] | 0.933 [0.73–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 68 | 72 | 68 | 4 | 0 | 94.4% | 100.0% | 0.971 [0.94–0.99] |

Miss rate (a labelled item predicted with no label): 0/61 (0.0%) [0–6]. False-alarm rate (an unlabelled item given a label): 2/57 (3.5%) [1–12].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 118/118 answered; 2.89 calls and 0.53 tool calls per item; rule gate 53, quote repair 0, self-check changed 4 of 118 items (+1 / −3 labels); exact quotes 72/72; cost $0.0618 ($0.524 per 1,000 items). Items on which each tool was called: get_label_rules 42%, phrase_stats 3%, search_cases 7%.

Confusion: exact 114, under-labelled 0, over-labelled 4, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| WEIGHT | GUARANTEE | 2 | confused |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |
| (no gold label) | WEIGHT | 1 | added to an unlabelled item |

**Slices of 118 items.** Overall micro F1 0.971, exact match 96.6%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 59 | 0.944 [0.88–0.99] | 55/59 (93.2%) | 0/32 | 2/27 | -0.056 [-0.12 to -0.01] | worse |
| zh | 59 | 1.000 [1.00–1.00] | 59/59 (100.0%) | 0/29 | 0/30 | +0.056 [+0.01 to +0.12] | better |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 11 | 0.933 [0.73–1.00] | 10/11 (90.9%) | 0/6 | 1/5 | -0.043 [-0.25 to +0.05] | too few |
| written-lookalike | 12 | 0.889 [0.67–1.00] | 11/12 (91.7%) | 0/4 | 0/8 | -0.088 [-0.29 to +0.04] | too few |
| written | 48 | 0.966 [0.91–1.00] | 46/48 (95.8%) | 0/26 | 1/22 | -0.010 [-0.07 to +0.04] | no measured difference |
| video-words | 47 | 1.000 [1.00–1.00] | 47/47 (100.0%) | 0/25 | 0/22 | +0.049 [+0.01 to +0.10] | better |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 61 | 0.986 [0.96–1.00] | 59/61 (96.7%) | 0/61 | – | +0.002 [-0.07 to +0.07] (exact match) | no measured difference |
| look-alike | 41 | – | 41/41 (100.0%) | – | 0/41 | +0.052 [+0.01 to +0.10] (exact match) | better |
| plain | 16 | – | 14/16 (87.5%) | – | 2/16 | -0.105 [-0.29 to +0.03] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 22–49 chars | 39 | 1.000 [1.00–1.00] | 39/39 (100.0%) | 0/18 | 0/21 | +0.040 [+0.01 to +0.09] | better |
| 50–82 chars | 38 | 0.939 [0.86–1.00] | 35/38 (92.1%) | 0/21 | 2/17 | -0.050 [-0.14 to +0.01] | no measured difference |
| 83–315 chars | 41 | 0.980 [0.94–1.00] | 40/41 (97.6%) | 0/22 | 0/19 | +0.014 [-0.04 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 57 | – | 55/57 (96.5%) | – | 2/57 | -0.002 [-0.07 to +0.07] (exact match) | no measured difference |
| ABSOLUTE | 17 | 1.000 [1.00–1.00] | 17/17 (100.0%) | 0/17 | – | +0.039 [+0.01 to +0.08] | too few |
| ALCOHOL | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.031 [+0.01 to +0.06] | too few |
| DATA | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.033 [+0.01 to +0.07] | too few |
| DISPARAGE | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.032 [+0.01 to +0.06] | too few |
| GUARANTEE | 15 | 1.000 [1.00–1.00] | 15/15 (100.0%) | 0/15 | – | +0.038 [+0.01 to +0.08] | too few |
| MEDICAL | 11 | 1.000 [1.00–1.00] | 11/11 (100.0%) | 0/11 | – | +0.035 [+0.01 to +0.07] | too few |
| WEIGHT | 7 | 0.889 [0.76–1.00] | 5/7 (71.4%) | 0/7 | – | -0.095 [-0.22 to +0.02] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_b / agent-cases-check-v2

**ad_policy / test_b / agent-cases-check-v2: 118 items, 9 labels.** Micro F1 0.993 [0.98–1.00], macro F1 0.989 [0.95–1.00], exact match 117/118 (99.2%) [95–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 17 | 17 | 17 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| MEDICAL | 11 | 11 | 11 | 0 | 0 | 100.0% [74–100] | 100.0% [74–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 15 | 15 | 15 | 0 | 0 | 100.0% [80–100] | 100.0% [80–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 6 | 6 | 6 | 0 | 0 | 100.0% [61–100] | 100.0% [61–100] | 1.000 [1.00–1.00] |
| DATA | 6 | 6 | 6 | 0 | 0 | 100.0% [61–100] | 100.0% [61–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 6 | 7 | 6 | 1 | 0 | 85.7% [49–97] | 100.0% [61–100] | 0.923 [0.67–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 68 | 69 | 68 | 1 | 0 | 98.6% | 100.0% | 0.993 [0.98–1.00] |

Miss rate (a labelled item predicted with no label): 0/61 (0.0%) [0–6]. False-alarm rate (an unlabelled item given a label): 1/57 (1.8%) [0–9].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 118/118 answered; 2.96 calls and 0.61 tool calls per item; rule gate 52, quote repair 2, self-check changed 1 of 118 items (+0 / −1 labels); exact quotes 69/69; cost $0.0657 ($0.556 per 1,000 items). Items on which each tool was called: get_label_rules 49%, phrase_stats 1%, search_cases 10%.

Confusion: exact 117, under-labelled 0, over-labelled 1, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |

**Slices of 118 items.** Overall micro F1 0.993, exact match 99.2%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 59 | 0.986 [0.95–1.00] | 58/59 (98.3%) | 0/32 | 1/27 | -0.014 [-0.05 to +0.00] | no measured difference |
| zh | 59 | 1.000 [1.00–1.00] | 59/59 (100.0%) | 0/29 | 0/30 | +0.014 [+0.00 to +0.05] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 11 | 1.000 [1.00–1.00] | 11/11 (100.0%) | 0/6 | 0/5 | +0.008 [+0.00 to +0.03] | too few |
| written-lookalike | 12 | 1.000 [1.00–1.00] | 12/12 (100.0%) | 0/4 | 0/8 | +0.008 [+0.00 to +0.03] | too few |
| written | 48 | 0.982 [0.94–1.00] | 47/48 (97.9%) | 0/26 | 1/22 | -0.018 [-0.06 to +0.00] | no measured difference |
| video-words | 47 | 1.000 [1.00–1.00] | 47/47 (100.0%) | 0/25 | 0/22 | +0.013 [+0.00 to +0.04] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 61 | 1.000 [1.00–1.00] | 61/61 (100.0%) | 0/61 | – | +0.018 [+0.00 to +0.05] (exact match) | no measured difference |
| look-alike | 41 | – | 41/41 (100.0%) | – | 0/41 | +0.013 [+0.00 to +0.04] (exact match) | no measured difference |
| plain | 16 | – | 15/16 (93.8%) | – | 1/16 | -0.062 [-0.19 to +0.00] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 22–49 chars | 39 | 1.000 [1.00–1.00] | 39/39 (100.0%) | 0/18 | 0/21 | +0.010 [+0.00 to +0.04] | no measured difference |
| 50–82 chars | 38 | 0.979 [0.92–1.00] | 37/38 (97.4%) | 0/21 | 1/17 | -0.021 [-0.08 to +0.00] | no measured difference |
| 83–315 chars | 41 | 1.000 [1.00–1.00] | 41/41 (100.0%) | 0/22 | 0/19 | +0.011 [+0.00 to +0.04] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 57 | – | 56/57 (98.2%) | – | 1/57 | -0.018 [-0.05 to +0.00] (exact match) | no measured difference |
| ABSOLUTE | 17 | 1.000 [1.00–1.00] | 17/17 (100.0%) | 0/17 | – | +0.010 [+0.00 to +0.03] | too few |
| ALCOHOL | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.008 [+0.00 to +0.03] | too few |
| DATA | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.009 [+0.00 to +0.03] | too few |
| DISPARAGE | 6 | 1.000 [1.00–1.00] | 6/6 (100.0%) | 0/6 | – | +0.008 [+0.00 to +0.03] | too few |
| GUARANTEE | 15 | 1.000 [1.00–1.00] | 15/15 (100.0%) | 0/15 | – | +0.010 [+0.00 to +0.03] | too few |
| MEDICAL | 11 | 1.000 [1.00–1.00] | 11/11 (100.0%) | 0/11 | – | +0.009 [+0.00 to +0.03] | too few |
| WEIGHT | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.008 [+0.00 to +0.03] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_a / agent-cases-check

**ad_policy / test_a / agent-cases-check: 119 items, 9 labels.** Micro F1 0.971 [0.94–0.99], macro F1 0.967 [0.92–1.00], exact match 115/119 (96.6%) [92–99].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 10 | 10 | 0 | 0 | 100.0% [72–100] | 100.0% [72–100] | 1.000 [1.00–1.00] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 16 | 14 | 2 | 0 | 87.5% [64–97] | 100.0% [78–100] | 0.933 [0.81–1.00] |
| DISPARAGE | 9 | 9 | 9 | 0 | 0 | 100.0% [70–100] | 100.0% [70–100] | 1.000 [1.00–1.00] |
| DATA | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| ALCOHOL | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 5 | 5 | 0 | 0 | 100.0% [57–100] | 100.0% [57–100] | 1.000 [1.00–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 70 | 70 | 68 | 2 | 2 | 97.1% | 97.1% | 0.971 [0.94–0.99] |

Miss rate (a labelled item predicted with no label): 1/67 (1.5%) [0–8]. False-alarm rate (an unlabelled item given a label): 0/52 (0.0%) [0–7].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 2.96 calls and 0.55 tool calls per item; rule gate 58, quote repair 1, self-check changed 5 of 119 items (+1 / −5 labels); exact quotes 70/70; cost $0.0634 ($0.533 per 1,000 items). Items on which each tool was called: get_label_rules 43%, phrase_stats 3%, search_cases 5%.

Confusion: exact 115, under-labelled 2, over-labelled 2, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DATA | (no predicted label) | 2 | missed |
| WEIGHT | GUARANTEE | 2 | confused |

**Slices of 119 items.** Overall micro F1 0.971, exact match 96.6%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.972 [0.93–1.00] | 58/60 (96.7%) | 0/35 | 0/25 | +0.002 [-0.05 to +0.06] | no measured difference |
| zh | 59 | 0.971 [0.92–1.00] | 57/59 (96.6%) | 1/32 | 0/27 | -0.002 [-0.06 to +0.05] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 0.941 [0.83–1.00] | 12/13 (92.3%) | 0/8 | 0/5 | -0.034 [-0.14 to +0.05] | too few |
| written-lookalike | 12 | 1.000 [1.00–1.00] | 12/12 (100.0%) | 0/6 | 0/6 | +0.032 [+0.01 to +0.06] | too few |
| written | 48 | 0.983 [0.94–1.00] | 47/48 (97.9%) | 0/28 | 0/20 | +0.020 [-0.03 to +0.07] | no measured difference |
| video-words | 46 | 0.960 [0.90–1.00] | 44/46 (95.7%) | 1/25 | 0/21 | -0.018 [-0.09 to +0.04] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 0.971 [0.94–0.99] | 63/67 (94.0%) | 1/67 | – | -0.060 [-0.12 to -0.01] (exact match) | worse |
| plain | 20 | – | 20/20 (100.0%) | – | 0/20 | +0.040 [+0.01 to +0.08] (exact match) | better |
| look-alike | 32 | – | 32/32 (100.0%) | – | 0/32 | +0.046 [+0.01 to +0.09] (exact match) | better |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 0.979 [0.94–1.00] | 38/39 (97.4%) | 0/22 | 0/17 | +0.011 [-0.04 to +0.06] | no measured difference |
| 49–85 chars | 40 | 0.950 [0.87–1.00] | 38/40 (95.0%) | 1/19 | 0/21 | -0.030 [-0.12 to +0.03] | no measured difference |
| 86–299 chars | 40 | 0.981 [0.94–1.00] | 39/40 (97.5%) | 0/26 | 0/14 | +0.016 [-0.04 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 52/52 (100.0%) | – | 0/52 | +0.060 [+0.01 to +0.12] (exact match) | better |
| ABSOLUTE | 10 | 0.957 [0.87–1.00] | 9/10 (90.0%) | 0/10 | – | -0.018 [-0.11 to +0.05] | too few |
| ALCOHOL | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.032 [+0.00 to +0.07] | too few |
| DATA | 7 | 0.889 [0.67–1.00] | 5/7 (71.4%) | 1/7 | – | -0.095 [-0.30 to +0.02] | too few |
| DISPARAGE | 9 | 1.000 [1.00–1.00] | 9/9 (100.0%) | 0/9 | – | +0.033 [+0.01 to +0.07] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.036 [+0.01 to +0.07] | too few |
| MEDICAL | 18 | 1.000 [1.00–1.00] | 18/18 (100.0%) | 0/18 | – | +0.038 [+0.01 to +0.08] | too few |
| WEIGHT | 5 | 0.833 [0.71–1.00] | 3/5 (60.0%) | 0/5 | – | -0.151 [-0.28 to +0.02] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_a / agent-cases-check-v2

**ad_policy / test_a / agent-cases-check-v2: 119 items, 9 labels.** Micro F1 0.986 [0.96–1.00], macro F1 0.980 [0.94–1.00], exact match 117/119 (98.3%) [94–100].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 11 | 10 | 1 | 0 | 90.9% [62–98] | 100.0% [72–100] | 0.952 [0.82–1.00] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 9 | 9 | 9 | 0 | 0 | 100.0% [70–100] | 100.0% [70–100] | 1.000 [1.00–1.00] |
| DATA | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 70 | 72 | 70 | 2 | 0 | 97.2% | 100.0% | 0.986 [0.96–1.00] |

Miss rate (a labelled item predicted with no label): 0/67 (0.0%) [0–5]. False-alarm rate (an unlabelled item given a label): 2/52 (3.8%) [1–13].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 2.91 calls and 0.45 tool calls per item; rule gate 63, quote repair 0, self-check changed 1 of 119 items (+1 / −0 labels); exact quotes 72/72; cost $0.0638 ($0.536 per 1,000 items). Items on which each tool was called: get_label_rules 38%, phrase_stats 2%, search_cases 5%.

Confusion: exact 117, under-labelled 0, over-labelled 2, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| (no gold label) | WEIGHT | 1 | added to an unlabelled item |

**Slices of 119 items.** Overall micro F1 0.986, exact match 98.3%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.972 [0.93–1.00] | 58/60 (96.7%) | 0/35 | 2/25 | -0.028 [-0.07 to +0.00] | no measured difference |
| zh | 59 | 1.000 [1.00–1.00] | 59/59 (100.0%) | 0/32 | 0/27 | +0.028 [+0.00 to +0.07] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 1.000 [1.00–1.00] | 13/13 (100.0%) | 0/8 | 0/5 | +0.016 [+0.00 to +0.04] | too few |
| written-lookalike | 12 | 1.000 [1.00–1.00] | 12/12 (100.0%) | 0/6 | 0/6 | +0.016 [+0.00 to +0.04] | too few |
| written | 48 | 0.983 [0.94–1.00] | 47/48 (97.9%) | 0/28 | 1/20 | -0.005 [-0.05 to +0.04] | no measured difference |
| video-words | 46 | 0.980 [0.93–1.00] | 45/46 (97.8%) | 0/25 | 1/21 | -0.009 [-0.06 to +0.03] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 1.000 [1.00–1.00] | 67/67 (100.0%) | 0/67 | – | +0.038 [+0.00 to +0.10] (exact match) | no measured difference |
| plain | 20 | – | 19/20 (95.0%) | – | 1/20 | -0.040 [-0.15 to +0.03] (exact match) | no measured difference |
| look-alike | 32 | – | 31/32 (96.9%) | – | 1/32 | -0.020 [-0.08 to +0.03] (exact match) | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 1.000 [1.00–1.00] | 39/39 (100.0%) | 0/22 | 0/17 | +0.021 [+0.00 to +0.06] | no measured difference |
| 49–85 chars | 40 | 0.976 [0.92–1.00] | 39/40 (97.5%) | 0/19 | 1/21 | -0.014 [-0.08 to +0.03] | no measured difference |
| 86–299 chars | 40 | 0.981 [0.94–1.00] | 39/40 (97.5%) | 0/26 | 1/14 | -0.008 [-0.06 to +0.03] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 50/52 (96.2%) | – | 2/52 | -0.038 [-0.10 to +0.00] (exact match) | no measured difference |
| ABSOLUTE | 10 | 1.000 [1.00–1.00] | 10/10 (100.0%) | 0/10 | – | +0.017 [+0.00 to +0.04] | too few |
| ALCOHOL | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.016 [+0.00 to +0.04] | too few |
| DATA | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.016 [+0.00 to +0.04] | too few |
| DISPARAGE | 9 | 1.000 [1.00–1.00] | 9/9 (100.0%) | 0/9 | – | +0.016 [+0.00 to +0.04] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.018 [+0.00 to +0.05] | too few |
| MEDICAL | 18 | 1.000 [1.00–1.00] | 18/18 (100.0%) | 0/18 | – | +0.019 [+0.00 to +0.05] | too few |
| WEIGHT | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.015 [+0.00 to +0.04] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_b / agent-cases-check

**asap / test_b / agent-cases-check: 199 items, 18 labels.** Micro F1 0.834 [0.82–0.85], macro F1 0.799 [0.77–0.82], exact match 37/199 (18.6%) [14–25].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 191 | 196 | 189 | 7 | 2 | 96.4% [93–98] | 99.0% [96–100] | 0.977 [0.96–0.99] |
| Food#Appearance | 47 | 40 | 32 | 8 | 15 | 80.0% [65–90] | 68.1% [54–80] | 0.736 [0.62–0.84] |
| Food#Portion | 86 | 79 | 68 | 11 | 18 | 86.1% [77–92] | 79.1% [69–86] | 0.824 [0.76–0.88] |
| Food#Recommend | 45 | 43 | 36 | 7 | 9 | 83.7% [70–92] | 80.0% [66–89] | 0.818 [0.72–0.90] |
| Price#Level | 97 | 75 | 67 | 8 | 30 | 89.3% [80–94] | 69.1% [59–77] | 0.779 [0.70–0.84] |
| Price#Cost_effective | 39 | 62 | 36 | 26 | 3 | 58.1% [46–70] | 92.3% [80–97] | 0.713 [0.61–0.80] |
| Price#Discount | 63 | 50 | 41 | 9 | 22 | 82.0% [69–90] | 65.1% [53–76] | 0.726 [0.62–0.81] |
| Location#Downtown | 36 | 18 | 15 | 3 | 21 | 83.3% [61–94] | 41.7% [27–58] | 0.556 [0.38–0.70] |
| Location#Transportation | 37 | 27 | 27 | 0 | 10 | 100.0% [88–100] | 73.0% [57–85] | 0.844 [0.73–0.93] |
| Location#Easy_to_find | 42 | 38 | 33 | 5 | 9 | 86.8% [73–94] | 78.6% [64–88] | 0.825 [0.72–0.90] |
| Service#Queue | 27 | 30 | 21 | 9 | 6 | 70.0% [52–83] | 77.8% [59–89] | 0.737 [0.59–0.85] |
| Service#Hospitality | 104 | 106 | 96 | 10 | 8 | 90.6% [83–95] | 92.3% [86–96] | 0.914 [0.87–0.95] |
| Service#Parking | 16 | 15 | 14 | 1 | 2 | 93.3% [70–99] | 87.5% [64–97] | 0.903 [0.77–1.00] |
| Service#Timely | 28 | 30 | 24 | 6 | 4 | 80.0% [63–90] | 85.7% [69–94] | 0.828 [0.71–0.92] |
| Ambience#Decoration | 84 | 84 | 79 | 5 | 5 | 94.0% [87–97] | 94.0% [87–97] | 0.940 [0.90–0.97] |
| Ambience#Noise | 50 | 40 | 32 | 8 | 18 | 80.0% [65–90] | 64.0% [50–76] | 0.711 [0.59–0.80] |
| Ambience#Space | 61 | 59 | 48 | 11 | 13 | 81.4% [70–89] | 78.7% [67–87] | 0.800 [0.71–0.87] |
| Ambience#Sanitary | 62 | 55 | 44 | 11 | 18 | 80.0% [68–88] | 71.0% [59–81] | 0.752 [0.66–0.83] |
| **micro** | 1115 | 1047 | 902 | 145 | 213 | 86.2% | 80.9% | 0.834 [0.82–0.85] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 199/199 answered; 3.41 calls and 0.26 tool calls per item; rule gate 197, quote repair 33, self-check changed 60 of 199 items (+45 / −29 labels); exact quotes 1045/1047; cost $0.3192 ($1.604 per 1,000 items). Items on which each tool was called: get_label_rules 26%, search_cases 0%.

Confusion: exact 37, under-labelled 57, over-labelled 53, swapped 52.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | (no predicted label) | 16 | missed |
| Price#Discount | (no predicted label) | 15 | missed |
| Location#Downtown | (no predicted label) | 14 | missed |
| Food#Portion | (no predicted label) | 12 | missed |
| Ambience#Noise | (no predicted label) | 11 | missed |
| Ambience#Sanitary | (no predicted label) | 11 | missed |
| Price#Level | Price#Cost_effective | 10 | confused |
| Food#Taste | Price#Cost_effective | 9 | confused |
| Ambience#Sanitary | Price#Cost_effective | 8 | confused |
| Food#Appearance | (no predicted label) | 8 | missed |

**Slices of 199 items.** Overall micro F1 0.834, exact match 18.6%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 163 | 0.824 [0.80–0.84] | 28/163 (17.2%) | 0/163 | – | -0.058 [-0.09 to -0.02] | worse |
| 1-3 stars | 36 | 0.881 [0.85–0.91] | 9/36 (25.0%) | 0/36 | – | +0.058 [+0.02 to +0.09] | better |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 83 | 0.849 [0.83–0.87] | 14/83 (16.9%) | 0/83 | – | +0.026 [-0.01 to +0.06] | no measured difference |
| 1-4 labels | 76 | 0.807 [0.77–0.84] | 20/76 (26.3%) | 0/76 | – | -0.036 [-0.08 to +0.00] | no measured difference |
| 8+ labels | 40 | 0.835 [0.80–0.87] | 3/40 (7.5%) | 0/40 | – | +0.000 [-0.04 to +0.04] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 143 | 0.851 [0.83–0.87] | 31/143 (21.7%) | 0/143 | – | +0.063 [+0.02 to +0.11] | better |
| no neutral mention | 56 | 0.788 [0.75–0.82] | 6/56 (10.7%) | 0/56 | – | -0.063 [-0.10 to -0.02] | worse |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 57–236 chars | 64 | 0.820 [0.78–0.85] | 18/64 (28.1%) | 0/64 | – | -0.020 [-0.06 to +0.02] | no measured difference |
| 237–319 chars | 68 | 0.829 [0.80–0.86] | 10/68 (14.7%) | 0/68 | – | -0.008 [-0.05 to +0.03] | no measured difference |
| 320–846 chars | 67 | 0.851 [0.83–0.87] | 9/67 (13.4%) | 0/67 | – | +0.026 [-0.01 to +0.06] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 84 | 0.838 [0.81–0.86] | 12/84 (14.3%) | 0/84 | – | +0.009 [-0.03 to +0.04] | no measured difference |
| Ambience#Noise | 50 | 0.831 [0.80–0.87] | 6/50 (12.0%) | 0/50 | – | -0.005 [-0.04 to +0.03] | no measured difference |
| Ambience#Sanitary | 62 | 0.833 [0.80–0.86] | 10/62 (16.1%) | 0/62 | – | -0.002 [-0.04 to +0.03] | no measured difference |
| Ambience#Space | 61 | 0.838 [0.81–0.87] | 9/61 (14.8%) | 0/61 | – | +0.006 [-0.04 to +0.04] | no measured difference |
| Food#Appearance | 47 | 0.824 [0.79–0.86] | 7/47 (14.9%) | 0/47 | – | -0.014 [-0.05 to +0.02] | no measured difference |
| Food#Portion | 86 | 0.841 [0.82–0.86] | 10/86 (11.6%) | 0/86 | – | +0.012 [-0.02 to +0.05] | no measured difference |
| Food#Recommend | 45 | 0.831 [0.80–0.86] | 5/45 (11.1%) | 0/45 | – | -0.005 [-0.04 to +0.03] | no measured difference |
| Food#Taste | 191 | 0.836 [0.82–0.85] | 36/191 (18.8%) | 0/191 | – | +0.057 [-0.06 to +0.18] | no measured difference |
| Location#Downtown | 36 | 0.798 [0.76–0.83] | 4/36 (11.1%) | 0/36 | – | -0.048 [-0.09 to -0.01] | worse |
| Location#Easy_to_find | 42 | 0.825 [0.79–0.86] | 5/42 (11.9%) | 0/42 | – | -0.013 [-0.06 to +0.03] | no measured difference |
| Location#Transportation | 37 | 0.815 [0.78–0.85] | 4/37 (10.8%) | 0/37 | – | -0.025 [-0.07 to +0.02] | no measured difference |
| Price#Cost_effective | 39 | 0.868 [0.83–0.90] | 6/39 (15.4%) | 0/39 | – | +0.044 [+0.01 to +0.08] | better |
| Price#Discount | 63 | 0.829 [0.80–0.86] | 9/63 (14.3%) | 0/63 | – | -0.009 [-0.05 to +0.02] | no measured difference |
| Price#Level | 97 | 0.840 [0.82–0.86] | 12/97 (12.4%) | 0/97 | – | +0.012 [-0.02 to +0.05] | no measured difference |
| Service#Hospitality | 104 | 0.843 [0.82–0.86] | 17/104 (16.3%) | 0/104 | – | +0.020 [-0.02 to +0.06] | no measured difference |
| Service#Parking | 16 | 0.857 [0.81–0.90] | 2/16 (12.5%) | 0/16 | – | +0.025 [-0.03 to +0.08] | too few |
| Service#Queue | 27 | 0.799 [0.75–0.85] | 4/27 (14.8%) | 0/27 | – | -0.042 [-0.09 to +0.01] | no measured difference |
| Service#Timely | 28 | 0.867 [0.83–0.91] | 5/28 (17.9%) | 0/28 | – | +0.039 [-0.00 to +0.08] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_b / agent-cases-check-v2

**asap / test_b / agent-cases-check-v2: 199 items, 18 labels.** Micro F1 0.852 [0.83–0.87], macro F1 0.821 [0.80–0.84], exact match 43/199 (21.6%) [16–28].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 191 | 197 | 189 | 8 | 2 | 95.9% [92–98] | 99.0% [96–100] | 0.974 [0.96–0.99] |
| Food#Appearance | 47 | 39 | 31 | 8 | 16 | 79.5% [64–89] | 66.0% [52–78] | 0.721 [0.60–0.82] |
| Food#Portion | 86 | 82 | 69 | 13 | 17 | 84.1% [75–90] | 80.2% [71–87] | 0.821 [0.76–0.88] |
| Food#Recommend | 45 | 47 | 36 | 11 | 9 | 76.6% [63–86] | 80.0% [66–89] | 0.783 [0.68–0.87] |
| Price#Level | 97 | 96 | 86 | 10 | 11 | 89.6% [82–94] | 88.7% [81–94] | 0.891 [0.84–0.94] |
| Price#Cost_effective | 39 | 59 | 33 | 26 | 6 | 55.9% [43–68] | 84.6% [70–93] | 0.673 [0.56–0.77] |
| Price#Discount | 63 | 83 | 61 | 22 | 2 | 73.5% [63–82] | 96.8% [89–99] | 0.836 [0.77–0.90] |
| Location#Downtown | 36 | 36 | 24 | 12 | 12 | 66.7% [50–80] | 66.7% [50–80] | 0.667 [0.52–0.78] |
| Location#Transportation | 37 | 31 | 28 | 3 | 9 | 90.3% [75–97] | 75.7% [60–87] | 0.824 [0.71–0.91] |
| Location#Easy_to_find | 42 | 38 | 34 | 4 | 8 | 89.5% [76–96] | 81.0% [67–90] | 0.850 [0.76–0.92] |
| Service#Queue | 27 | 32 | 22 | 10 | 5 | 68.8% [51–82] | 81.5% [63–92] | 0.746 [0.60–0.86] |
| Service#Hospitality | 104 | 111 | 100 | 11 | 4 | 90.1% [83–94] | 96.2% [91–98] | 0.930 [0.89–0.96] |
| Service#Parking | 16 | 15 | 14 | 1 | 2 | 93.3% [70–99] | 87.5% [64–97] | 0.903 [0.77–1.00] |
| Service#Timely | 28 | 33 | 27 | 6 | 1 | 81.8% [66–91] | 96.4% [82–99] | 0.885 [0.79–0.96] |
| Ambience#Decoration | 84 | 88 | 80 | 8 | 4 | 90.9% [83–95] | 95.2% [88–98] | 0.930 [0.89–0.97] |
| Ambience#Noise | 50 | 50 | 38 | 12 | 12 | 76.0% [63–86] | 76.0% [63–86] | 0.760 [0.65–0.84] |
| Ambience#Space | 61 | 68 | 52 | 16 | 9 | 76.5% [65–85] | 85.2% [74–92] | 0.806 [0.72–0.88] |
| Ambience#Sanitary | 62 | 64 | 49 | 15 | 13 | 76.6% [65–85] | 79.0% [67–87] | 0.778 [0.69–0.85] |
| **micro** | 1115 | 1169 | 973 | 196 | 142 | 83.2% | 87.3% | 0.852 [0.83–0.87] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 199/199 answered; 3.29 calls and 0.08 tool calls per item; rule gate 198, quote repair 44, self-check changed 43 of 199 items (+44 / −14 labels); exact quotes 1164/1169; cost $0.3229 ($1.623 per 1,000 items). Items on which each tool was called: get_label_rules 8%.

Confusion: exact 43, under-labelled 37, over-labelled 76, swapped 43.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Price#Discount | 17 | confused |
| Food#Taste | Price#Cost_effective | 14 | confused |
| Food#Taste | Ambience#Space | 12 | confused |
| Price#Level | Price#Cost_effective | 12 | confused |
| Price#Level | Price#Discount | 12 | confused |
| Food#Portion | (no predicted label) | 10 | missed |
| Food#Portion | Price#Cost_effective | 10 | confused |
| Food#Taste | Ambience#Sanitary | 10 | confused |
| Service#Hospitality | Price#Cost_effective | 10 | confused |
| Ambience#Decoration | Price#Cost_effective | 9 | confused |

**Slices of 199 items.** Overall micro F1 0.852, exact match 21.6%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 163 | 0.846 [0.83–0.86] | 33/163 (20.2%) | 0/163 | – | -0.034 [-0.07 to +0.01] | no measured difference |
| 1-3 stars | 36 | 0.879 [0.84–0.91] | 10/36 (27.8%) | 0/36 | – | +0.034 [-0.01 to +0.07] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 83 | 0.861 [0.84–0.88] | 18/83 (21.7%) | 0/83 | – | +0.016 [-0.02 to +0.05] | no measured difference |
| 1-4 labels | 76 | 0.812 [0.77–0.84] | 18/76 (23.7%) | 0/76 | – | -0.052 [-0.10 to -0.01] | worse |
| 8+ labels | 40 | 0.869 [0.84–0.90] | 7/40 (17.5%) | 0/40 | – | +0.025 [-0.01 to +0.06] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 143 | 0.873 [0.85–0.89] | 37/143 (25.9%) | 0/143 | – | +0.081 [+0.04 to +0.12] | better |
| no neutral mention | 56 | 0.792 [0.76–0.83] | 6/56 (10.7%) | 0/56 | – | -0.081 [-0.12 to -0.04] | worse |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 57–236 chars | 64 | 0.826 [0.79–0.86] | 15/64 (23.4%) | 0/64 | – | -0.036 [-0.07 to +0.00] | no measured difference |
| 237–319 chars | 68 | 0.868 [0.83–0.90] | 16/68 (23.5%) | 0/68 | – | +0.023 [-0.02 to +0.06] | no measured difference |
| 320–846 chars | 67 | 0.859 [0.83–0.88] | 12/67 (17.9%) | 0/67 | – | +0.010 [-0.02 to +0.04] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 84 | 0.863 [0.84–0.89] | 20/84 (23.8%) | 0/84 | – | +0.024 [-0.01 to +0.06] | no measured difference |
| Ambience#Noise | 50 | 0.862 [0.83–0.89] | 11/50 (22.0%) | 0/50 | – | +0.016 [-0.02 to +0.06] | no measured difference |
| Ambience#Sanitary | 62 | 0.864 [0.84–0.90] | 17/62 (27.4%) | 0/62 | – | +0.021 [-0.01 to +0.06] | no measured difference |
| Ambience#Space | 61 | 0.866 [0.83–0.89] | 14/61 (23.0%) | 0/61 | – | +0.025 [-0.01 to +0.06] | no measured difference |
| Food#Appearance | 47 | 0.845 [0.81–0.88] | 8/47 (17.0%) | 0/47 | – | -0.010 [-0.05 to +0.03] | no measured difference |
| Food#Portion | 86 | 0.869 [0.84–0.89] | 17/86 (19.8%) | 0/86 | – | +0.033 [-0.00 to +0.07] | no measured difference |
| Food#Recommend | 45 | 0.862 [0.83–0.89] | 9/45 (20.0%) | 0/45 | – | +0.014 [-0.02 to +0.05] | no measured difference |
| Food#Taste | 191 | 0.856 [0.84–0.87] | 43/191 (22.5%) | 0/191 | – | +0.099 [-0.00 to +0.20] | no measured difference |
| Location#Downtown | 36 | 0.824 [0.78–0.86] | 3/36 (8.3%) | 0/36 | – | -0.036 [-0.08 to +0.01] | no measured difference |
| Location#Easy_to_find | 42 | 0.834 [0.80–0.87] | 5/42 (11.9%) | 0/42 | – | -0.024 [-0.06 to +0.02] | no measured difference |
| Location#Transportation | 37 | 0.827 [0.79–0.87] | 6/37 (16.2%) | 0/37 | – | -0.033 [-0.08 to +0.01] | no measured difference |
| Price#Cost_effective | 39 | 0.887 [0.85–0.92] | 9/39 (23.1%) | 0/39 | – | +0.045 [+0.01 to +0.08] | better |
| Price#Discount | 63 | 0.874 [0.84–0.90] | 12/63 (19.0%) | 0/63 | – | +0.033 [-0.00 to +0.07] | no measured difference |
| Price#Level | 97 | 0.866 [0.84–0.89] | 21/97 (21.6%) | 0/97 | – | +0.030 [-0.00 to +0.06] | no measured difference |
| Service#Hospitality | 104 | 0.863 [0.84–0.88] | 22/104 (21.2%) | 0/104 | – | +0.028 [-0.01 to +0.07] | no measured difference |
| Service#Parking | 16 | 0.867 [0.82–0.91] | 2/16 (12.5%) | 0/16 | – | +0.017 [-0.03 to +0.06] | too few |
| Service#Queue | 27 | 0.824 [0.77–0.87] | 3/27 (11.1%) | 0/27 | – | -0.033 [-0.09 to +0.02] | no measured difference |
| Service#Timely | 28 | 0.874 [0.83–0.91] | 8/28 (28.6%) | 0/28 | – | +0.027 [-0.02 to +0.07] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / agent-cases-check

**asap / test_a / agent-cases-check: 201 items, 18 labels.** Micro F1 0.824 [0.80–0.84], macro F1 0.789 [0.76–0.81], exact match 36/201 (17.9%) [13–24].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 190 | 189 | 1 | 1 | 99.5% [97–100] | 99.5% [97–100] | 0.995 [0.99–1.00] |
| Food#Appearance | 54 | 39 | 29 | 10 | 25 | 74.4% [59–85] | 53.7% [41–66] | 0.624 [0.49–0.73] |
| Food#Portion | 88 | 76 | 61 | 15 | 27 | 80.3% [70–88] | 69.3% [59–78] | 0.744 [0.66–0.81] |
| Food#Recommend | 32 | 40 | 24 | 16 | 8 | 60.0% [45–74] | 75.0% [58–87] | 0.667 [0.53–0.78] |
| Price#Level | 94 | 64 | 56 | 8 | 38 | 87.5% [77–94] | 59.6% [49–69] | 0.709 [0.62–0.79] |
| Price#Cost_effective | 41 | 72 | 40 | 32 | 1 | 55.6% [44–66] | 97.6% [87–100] | 0.708 [0.60–0.79] |
| Price#Discount | 73 | 56 | 49 | 7 | 24 | 87.5% [76–94] | 67.1% [56–77] | 0.760 [0.67–0.84] |
| Location#Downtown | 39 | 20 | 16 | 4 | 23 | 80.0% [58–92] | 41.0% [27–57] | 0.542 [0.38–0.69] |
| Location#Transportation | 52 | 43 | 39 | 4 | 13 | 90.7% [78–96] | 75.0% [62–85] | 0.821 [0.73–0.90] |
| Location#Easy_to_find | 47 | 41 | 36 | 5 | 11 | 87.8% [74–95] | 76.6% [63–86] | 0.818 [0.72–0.90] |
| Service#Queue | 35 | 37 | 30 | 7 | 5 | 81.1% [66–91] | 85.7% [71–94] | 0.833 [0.72–0.92] |
| Service#Hospitality | 111 | 107 | 98 | 9 | 13 | 91.6% [85–96] | 88.3% [81–93] | 0.899 [0.85–0.94] |
| Service#Parking | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| Service#Timely | 28 | 30 | 23 | 7 | 5 | 76.7% [59–88] | 82.1% [64–92] | 0.793 [0.65–0.89] |
| Ambience#Decoration | 90 | 91 | 80 | 11 | 10 | 87.9% [80–93] | 88.9% [81–94] | 0.884 [0.83–0.93] |
| Ambience#Noise | 64 | 55 | 50 | 5 | 14 | 90.9% [80–96] | 78.1% [67–86] | 0.840 [0.76–0.90] |
| Ambience#Space | 76 | 77 | 65 | 12 | 11 | 84.4% [75–91] | 85.5% [76–92] | 0.850 [0.79–0.91] |
| Ambience#Sanitary | 71 | 66 | 58 | 8 | 13 | 87.9% [78–94] | 81.7% [71–89] | 0.847 [0.77–0.90] |
| **micro** | 1197 | 1115 | 953 | 162 | 244 | 85.5% | 79.6% | 0.824 [0.80–0.84] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 3.40 calls and 0.26 tool calls per item; rule gate 200, quote repair 28, self-check changed 75 of 201 items (+66 / −43 labels); exact quotes 1115/1115; cost $0.3203 ($1.594 per 1,000 items). Items on which each tool was called: get_label_rules 26%.

Confusion: exact 36, under-labelled 69, over-labelled 37, swapped 59.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Portion | (no predicted label) | 17 | missed |
| Price#Discount | (no predicted label) | 16 | missed |
| Price#Level | (no predicted label) | 16 | missed |
| Price#Level | Price#Cost_effective | 15 | confused |
| Food#Appearance | (no predicted label) | 14 | missed |
| Food#Taste | Price#Cost_effective | 10 | confused |
| Service#Hospitality | Price#Cost_effective | 10 | confused |
| Ambience#Sanitary | (no predicted label) | 9 | missed |
| Location#Downtown | (no predicted label) | 9 | missed |
| Ambience#Space | (no predicted label) | 8 | missed |

**Slices of 201 items.** Overall micro F1 0.824, exact match 17.9%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.797 [0.75–0.84] | 5/37 (13.5%) | 0/37 | – | -0.033 [-0.09 to +0.02] | no measured difference |
| 4-5 stars | 164 | 0.831 [0.81–0.85] | 31/164 (18.9%) | 0/162 | 0/2 | +0.033 [-0.01 to +0.08] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.837 [0.81–0.87] | 4/56 (7.1%) | 0/56 | – | +0.022 [-0.02 to +0.06] | no measured difference |
| 5-7 labels | 79 | 0.828 [0.80–0.86] | 16/79 (20.3%) | 0/79 | – | +0.006 [-0.03 to +0.04] | no measured difference |
| 1-4 labels | 66 | 0.786 [0.74–0.83] | 16/66 (24.2%) | 0/64 | 0/2 | -0.047 [-0.10 to +0.00] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.826 [0.80–0.85] | 27/148 (18.2%) | 0/148 | – | +0.006 [-0.03 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.820 [0.78–0.85] | 9/53 (17.0%) | 0/51 | 0/2 | -0.006 [-0.05 to +0.04] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.846 [0.81–0.88] | 18/67 (26.9%) | 0/65 | 0/2 | +0.031 [-0.01 to +0.07] | no measured difference |
| 236–314 chars | 67 | 0.787 [0.75–0.82] | 9/67 (13.4%) | 0/67 | – | -0.055 [-0.10 to -0.01] | worse |
| 315–946 chars | 67 | 0.839 [0.81–0.87] | 9/67 (13.4%) | 0/67 | – | +0.024 [-0.02 to +0.06] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.829 [+0.77 to +0.88] (exact match) | too few |
| Ambience#Decoration | 90 | 0.845 [0.82–0.87] | 13/90 (14.4%) | 0/90 | – | +0.049 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.840 [0.81–0.87] | 8/64 (12.5%) | 0/64 | – | +0.029 [-0.01 to +0.07] | no measured difference |
| Ambience#Sanitary | 71 | 0.854 [0.82–0.88] | 11/71 (15.5%) | 0/71 | – | +0.055 [+0.02 to +0.09] | better |
| Ambience#Space | 76 | 0.848 [0.82–0.87] | 10/76 (13.2%) | 0/76 | – | +0.048 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.811 [0.78–0.84] | 6/54 (11.1%) | 0/54 | – | -0.019 [-0.06 to +0.02] | no measured difference |
| Food#Portion | 88 | 0.827 [0.80–0.85] | 13/88 (14.8%) | 0/88 | – | +0.004 [-0.03 to +0.04] | no measured difference |
| Food#Recommend | 32 | 0.850 [0.81–0.89] | 4/32 (12.5%) | 0/32 | – | +0.031 [-0.01 to +0.07] | no measured difference |
| Food#Taste | 190 | 0.826 [0.81–0.85] | 32/190 (16.8%) | 0/190 | – | +0.046 [-0.07 to +0.21] | no measured difference |
| Location#Downtown | 39 | 0.795 [0.75–0.83] | 4/39 (10.3%) | 0/39 | – | -0.039 [-0.09 to +0.01] | no measured difference |
| Location#Easy_to_find | 47 | 0.835 [0.80–0.87] | 6/47 (12.8%) | 0/47 | – | +0.016 [-0.03 to +0.06] | no measured difference |
| Location#Transportation | 52 | 0.815 [0.78–0.85] | 5/52 (9.6%) | 0/52 | – | -0.013 [-0.06 to +0.03] | no measured difference |
| Price#Cost_effective | 41 | 0.832 [0.79–0.87] | 6/41 (14.6%) | 0/41 | – | +0.010 [-0.04 to +0.05] | no measured difference |
| Price#Discount | 73 | 0.828 [0.80–0.86] | 8/73 (11.0%) | 0/73 | – | +0.007 [-0.03 to +0.05] | no measured difference |
| Price#Level | 94 | 0.802 [0.77–0.83] | 14/94 (14.9%) | 0/94 | – | -0.047 [-0.09 to -0.01] | worse |
| Service#Hospitality | 111 | 0.837 [0.81–0.86] | 18/111 (16.2%) | 0/111 | – | +0.036 [-0.00 to +0.08] | no measured difference |
| Service#Parking | 12 | 0.792 [0.69–0.89] | 2/12 (16.7%) | 0/12 | – | -0.035 [-0.13 to +0.06] | too few |
| Service#Queue | 35 | 0.817 [0.77–0.85] | 5/35 (14.3%) | 0/35 | – | -0.010 [-0.06 to +0.03] | no measured difference |
| Service#Timely | 28 | 0.788 [0.74–0.84] | 2/28 (7.1%) | 0/28 | – | -0.044 [-0.10 to +0.01] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / agent-cases-check-v2

**asap / test_a / agent-cases-check-v2: 201 items, 18 labels.** Micro F1 0.841 [0.82–0.86], macro F1 0.812 [0.79–0.83], exact match 36/201 (17.9%) [13–24].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 194 | 189 | 5 | 1 | 97.4% [94–99] | 99.5% [97–100] | 0.984 [0.97–0.99] |
| Food#Appearance | 54 | 39 | 28 | 11 | 26 | 71.8% [56–83] | 51.9% [39–65] | 0.602 [0.48–0.71] |
| Food#Portion | 88 | 81 | 61 | 20 | 27 | 75.3% [65–83] | 69.3% [59–78] | 0.722 [0.64–0.79] |
| Food#Recommend | 32 | 42 | 25 | 17 | 7 | 59.5% [44–73] | 78.1% [61–89] | 0.676 [0.54–0.79] |
| Price#Level | 94 | 98 | 80 | 18 | 14 | 81.6% [73–88] | 85.1% [77–91] | 0.833 [0.77–0.89] |
| Price#Cost_effective | 41 | 65 | 36 | 29 | 5 | 55.4% [43–67] | 87.8% [74–95] | 0.679 [0.57–0.77] |
| Price#Discount | 73 | 88 | 72 | 16 | 1 | 81.8% [72–88] | 98.6% [93–100] | 0.894 [0.84–0.94] |
| Location#Downtown | 39 | 44 | 28 | 16 | 11 | 63.6% [49–76] | 71.8% [56–83] | 0.675 [0.55–0.79] |
| Location#Transportation | 52 | 48 | 43 | 5 | 9 | 89.6% [78–95] | 82.7% [70–91] | 0.860 [0.78–0.93] |
| Location#Easy_to_find | 47 | 40 | 33 | 7 | 14 | 82.5% [68–91] | 70.2% [56–81] | 0.759 [0.65–0.85] |
| Service#Queue | 35 | 41 | 32 | 9 | 3 | 78.0% [63–88] | 91.4% [78–97] | 0.842 [0.74–0.92] |
| Service#Hospitality | 111 | 113 | 102 | 11 | 9 | 90.3% [83–94] | 91.9% [85–96] | 0.911 [0.87–0.95] |
| Service#Parking | 12 | 12 | 11 | 1 | 1 | 91.7% [65–99] | 91.7% [65–99] | 0.917 [0.77–1.00] |
| Service#Timely | 28 | 34 | 25 | 9 | 3 | 73.5% [57–85] | 89.3% [73–96] | 0.806 [0.68–0.90] |
| Ambience#Decoration | 90 | 95 | 83 | 12 | 7 | 87.4% [79–93] | 92.2% [85–96] | 0.897 [0.85–0.94] |
| Ambience#Noise | 64 | 63 | 56 | 7 | 8 | 88.9% [79–95] | 87.5% [77–94] | 0.882 [0.81–0.94] |
| Ambience#Space | 76 | 85 | 66 | 19 | 10 | 77.6% [68–85] | 86.8% [77–93] | 0.820 [0.75–0.88] |
| Ambience#Sanitary | 71 | 77 | 63 | 14 | 8 | 81.8% [72–89] | 88.7% [79–94] | 0.851 [0.78–0.91] |
| **micro** | 1197 | 1259 | 1033 | 226 | 164 | 82.0% | 86.3% | 0.841 [0.82–0.86] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 3.26 calls and 0.04 tool calls per item; rule gate 199, quote repair 48, self-check changed 46 of 201 items (+46 / −17 labels); exact quotes 1257/1259; cost $0.3296 ($1.640 per 1,000 items). Items on which each tool was called: get_label_rules 3%.

Confusion: exact 36, under-labelled 42, over-labelled 64, swapped 59.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Price#Cost_effective | 15 | confused |
| Food#Taste | Food#Portion | 13 | confused |
| Food#Appearance | (no predicted label) | 12 | missed |
| Price#Level | Price#Cost_effective | 11 | confused |
| Service#Hospitality | Price#Cost_effective | 11 | confused |
| Ambience#Decoration | Price#Cost_effective | 9 | confused |
| Food#Portion | (no predicted label) | 9 | missed |
| Food#Portion | Price#Cost_effective | 9 | confused |
| Ambience#Space | (no predicted label) | 8 | missed |
| Food#Taste | Food#Appearance | 8 | confused |

**Slices of 201 items.** Overall micro F1 0.841, exact match 17.9%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.834 [0.80–0.87] | 4/37 (10.8%) | 0/37 | – | -0.009 [-0.05 to +0.03] | no measured difference |
| 4-5 stars | 164 | 0.843 [0.82–0.87] | 32/164 (19.5%) | 0/162 | 0/2 | +0.009 [-0.03 to +0.05] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.878 [0.85–0.90] | 9/56 (16.1%) | 0/56 | – | +0.063 [+0.03 to +0.10] | better |
| 5-7 labels | 79 | 0.838 [0.81–0.86] | 12/79 (15.2%) | 0/79 | – | -0.006 [-0.04 to +0.03] | no measured difference |
| 1-4 labels | 66 | 0.767 [0.73–0.81] | 15/66 (22.7%) | 0/64 | 0/2 | -0.091 [-0.13 to -0.05] | worse |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.850 [0.83–0.87] | 27/148 (18.2%) | 0/148 | – | +0.041 [-0.00 to +0.09] | no measured difference |
| no neutral mention | 53 | 0.810 [0.77–0.85] | 9/53 (17.0%) | 0/51 | 0/2 | -0.041 [-0.09 to +0.00] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.857 [0.82–0.89] | 20/67 (29.9%) | 0/65 | 0/2 | +0.022 [-0.02 to +0.06] | no measured difference |
| 236–314 chars | 67 | 0.813 [0.78–0.84] | 6/67 (9.0%) | 0/67 | – | -0.042 [-0.08 to -0.01] | worse |
| 315–946 chars | 67 | 0.854 [0.82–0.88] | 10/67 (14.9%) | 0/67 | – | +0.020 [-0.02 to +0.06] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.829 [+0.77 to +0.88] (exact match) | too few |
| Ambience#Decoration | 90 | 0.873 [0.85–0.89] | 16/90 (17.8%) | 0/90 | – | +0.074 [+0.04 to +0.11] | better |
| Ambience#Noise | 64 | 0.875 [0.85–0.90] | 12/64 (18.8%) | 0/64 | – | +0.062 [+0.02 to +0.09] | better |
| Ambience#Sanitary | 71 | 0.886 [0.86–0.91] | 15/71 (21.1%) | 0/71 | – | +0.082 [+0.05 to +0.11] | better |
| Ambience#Space | 76 | 0.875 [0.85–0.90] | 15/76 (19.7%) | 0/76 | – | +0.068 [+0.04 to +0.10] | better |
| Food#Appearance | 54 | 0.819 [0.78–0.85] | 3/54 (5.6%) | 0/54 | – | -0.032 [-0.07 to +0.01] | no measured difference |
| Food#Portion | 88 | 0.841 [0.82–0.86] | 8/88 (9.1%) | 0/88 | – | -0.001 [-0.04 to +0.03] | no measured difference |
| Food#Recommend | 32 | 0.869 [0.83–0.91] | 6/32 (18.8%) | 0/32 | – | +0.034 [-0.01 to +0.08] | no measured difference |
| Food#Taste | 190 | 0.846 [0.83–0.86] | 33/190 (17.4%) | 0/190 | – | +0.117 [+0.01 to +0.25] | better |
| Location#Downtown | 39 | 0.841 [0.81–0.87] | 4/39 (10.3%) | 0/39 | – | +0.000 [-0.04 to +0.04] | no measured difference |
| Location#Easy_to_find | 47 | 0.870 [0.84–0.90] | 9/47 (19.1%) | 0/47 | – | +0.041 [+0.01 to +0.08] | better |
| Location#Transportation | 52 | 0.847 [0.81–0.88] | 7/52 (13.5%) | 0/52 | – | +0.008 [-0.03 to +0.05] | no measured difference |
| Price#Cost_effective | 41 | 0.877 [0.85–0.91] | 8/41 (19.5%) | 0/41 | – | +0.048 [+0.01 to +0.08] | better |
| Price#Discount | 73 | 0.871 [0.84–0.89] | 12/73 (16.4%) | 0/73 | – | +0.053 [+0.02 to +0.09] | better |
| Price#Level | 94 | 0.837 [0.81–0.86] | 15/94 (16.0%) | 0/94 | – | -0.008 [-0.04 to +0.03] | no measured difference |
| Service#Hospitality | 111 | 0.854 [0.83–0.88] | 20/111 (18.0%) | 0/111 | – | +0.036 [+0.00 to +0.07] | better |
| Service#Parking | 12 | 0.856 [0.79–0.91] | 1/12 (8.3%) | 0/12 | – | +0.016 [-0.05 to +0.07] | too few |
| Service#Queue | 35 | 0.843 [0.80–0.88] | 4/35 (11.4%) | 0/35 | – | +0.002 [-0.04 to +0.04] | no measured difference |
| Service#Timely | 28 | 0.822 [0.77–0.87] | 1/28 (3.6%) | 0/28 | – | -0.024 [-0.08 to +0.03] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


