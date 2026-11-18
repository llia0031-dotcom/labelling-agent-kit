# Analysis: dev2

## ad_policy / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 87 | 0.832 [0.76–0.90] | 0.889 [0.79–0.94] | 70/87 | 4/45 | 4/42 | 1.00 | 0.00 | 0.09 | 0 |
| prompt-rules | 87 | 0.917 [0.85–0.97] | 0.938 [0.87–0.98] | 79/87 | 3/45 | 2/42 | 1.00 | 0.00 | 0.11 | 0 |
| agent | 87 | 0.898 [0.83–0.95] | 0.904 [0.81–0.96] | 77/87 | 3/45 | 5/42 | 1.86 | 0.81 | 0.24 | 0 |
| agent-cases | 87 | 0.905 [0.84–0.96] | 0.909 [0.82–0.96] | 78/87 | 4/45 | 3/42 | 1.62 | 0.26 | 0.26 | 0 |
| agent-cases-check | 87 | 0.913 [0.84–0.97] | 0.921 [0.83–0.97] | 80/87 | 5/45 | 2/42 | 2.88 | 0.53 | 0.52 | 0 |
| agent-cases-check-medium | 87 | 0.915 [0.84–0.97] | 0.925 [0.84–0.97] | 80/87 | 4/45 | 3/42 | 3.08 | 1.14 | 0.62 | 0 |

## asap / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 60 | 0.736 [0.71–0.76] | 0.689 [0.64–0.72] | 1/60 | – | – | 1.00 | 0.00 | 0.20 | 0 |
| prompt-rules | 60 | 0.799 [0.76–0.83] | 0.767 [0.72–0.80] | 4/60 | – | – | 1.00 | 0.00 | 0.26 | 0 |
| agent | 60 | 0.841 [0.81–0.87] | 0.791 [0.74–0.83] | 10/60 | – | – | 2.20 | 0.37 | 0.77 | 0 |
| agent-cases | 60 | 0.827 [0.79–0.86] | 0.780 [0.73–0.82] | 11/60 | – | – | 2.20 | 0.00 | 0.96 | 0 |
| agent-cases-check | 60 | 0.844 [0.81–0.87] | 0.795 [0.75–0.83] | 10/60 | – | – | 3.45 | 0.32 | 1.63 | 0 |
| agent-cases-check-medium | 60 | 0.863 [0.83–0.89] | 0.823 [0.78–0.86] | 12/60 | – | – | 3.83 | 0.72 | 1.88 | 0 |
| agent-cases-synthetic | 60 | 0.832 [0.80–0.86] | 0.778 [0.73–0.81] | 10/60 | – | – | 2.15 | 0.02 | 0.93 | 0 |

## Comparisons (B − A, micro F1, paired bootstrap 95%)

| Id | Task / set | A | B | Δ micro F1 | Δ macro F1 | McNemar p (exact match) | Verdict |
|---|---|---|---|---|---|---|---|
| d-ad-1 | ad_policy / dev | prompt-short | agent | +0.066 [+0.002, +0.127] | +0.016 [-0.052, +0.087] | 0.118 | B better |
| d-ad-2 | ad_policy / dev | agent | agent-cases | +0.007 [-0.036, +0.054] | +0.004 [-0.045, +0.053] | 1.000 | no measured difference |
| d-ad-3 | ad_policy / dev | agent-cases | agent-cases-check | +0.008 [-0.029, +0.046] | +0.012 [-0.041, +0.074] | 0.500 | no measured difference |
| d-ad-e | ad_policy / dev | agent-cases-check | agent-cases-check-medium | +0.002 [-0.029, +0.034] | +0.004 [-0.037, +0.050] | 1.000 | no measured difference |
| d-asap-1 | asap / dev | prompt-short | agent | +0.105 [+0.073, +0.136] | +0.102 [+0.065, +0.136] | 0.004 | B better |
| d-asap-2 | asap / dev | agent | agent-cases | -0.015 [-0.032, +0.001] | -0.011 [-0.036, +0.017] | 1.000 | no measured difference |
| d-asap-3 | asap / dev | agent-cases | agent-cases-check | +0.018 [-0.002, +0.039] | +0.015 [-0.015, +0.047] | 1.000 | no measured difference |
| d-asap-e | asap / dev | agent-cases-check | agent-cases-check-medium | +0.019 [+0.001, +0.037] | +0.028 [-0.002, +0.060] | 0.727 | B better |
| d-asap-s | asap / dev | agent-cases-synthetic | agent-cases | -0.006 [-0.027, +0.014] | +0.002 [-0.025, +0.031] | 1.000 | no measured difference |


# Details per arm

## ad_policy / dev / prompt-short

**ad_policy / dev / prompt-short: 87 items, 9 labels.** Micro F1 0.832 [0.76–0.90], macro F1 0.889 [0.79–0.94], exact match 70/87 (80.5%) [71–87].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 19 | 10 | 9 | 2 | 52.6% [32–73] | 83.3% [55–95] | 0.645 [0.38–0.82] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 4 | 4 | 0 | 4 | 100.0% [51–100] | 50.0% [22–78] | 0.667 [0.22–0.94] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| **micro** | 48 | 53 | 42 | 11 | 6 | 79.2% | 87.5% | 0.832 [0.76–0.90] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 4/42 (9.5%) [4–22].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 53/53; cost $0.0076 ($0.087 per 1,000 items).

Confusion: exact 70, under-labelled 6, over-labelled 11, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| GUARANTEE | ABSOLUTE | 6 | confused |
| DISPARAGE | (no predicted label) | 4 | missed |
| (no gold label) | ABSOLUTE | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |
| (no gold label) | BEFORE_AFTER | 1 | added to an unlabelled item |
| MEDICAL | ABSOLUTE | 1 | confused |

**Slices of 87 items.** Overall micro F1 0.832, exact match 80.5%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.905 [0.81–0.98] | 36/40 (90.0%) | 1/20 | 2/20 | +0.125 [-0.02 to +0.25] | no measured difference |
| zh | 47 | 0.780 [0.68–0.86] | 34/47 (72.3%) | 3/25 | 2/22 | -0.125 [-0.25 to +0.00] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 0.833 [0.72–0.93] | 18/24 (75.0%) | 0/15 | 2/9 | +0.003 [-0.13 to +0.13] | no measured difference |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.175 [+0.11 to +0.24] | too few |
| synthetic | 60 | 0.820 [0.72–0.90] | 49/60 (81.7%) | 4/28 | 2/32 | -0.030 [-0.17 to +0.10] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.866 [0.81–0.93] | 32/45 (71.1%) | 4/45 | – | -0.194 [-0.35 to -0.04] (exact match) | worse |
| look-alike | 27 | – | 24/27 (88.9%) | – | 3/27 | +0.122 [-0.04 to +0.27] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.156 [-0.02 to +0.31] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 0.857 [0.77–0.95] | 24/29 (82.8%) | 0/15 | 0/14 | +0.039 [-0.07 to +0.17] | no measured difference |
| 56–92 chars | 29 | 0.757 [0.61–0.88] | 20/29 (69.0%) | 3/16 | 3/13 | -0.118 [-0.29 to +0.02] | no measured difference |
| 93–177 chars | 29 | 0.897 [0.76–1.00] | 26/29 (89.7%) | 1/14 | 1/15 | +0.091 [-0.06 to +0.24] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 38/42 (90.5%) | – | 4/42 | +0.194 [+0.01 to +0.35] (exact match) | better |
| ABSOLUTE | 12 | 0.889 [0.77–1.00] | 9/12 (75.0%) | 1/12 | – | +0.078 [-0.07 to +0.22] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.187 [+0.12 to +0.26] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.179 [+0.11 to +0.25] | too few |
| DISPARAGE | 8 | 0.706 [0.40–0.89] | 3/8 (37.5%) | 3/8 | – | -0.151 [-0.48 to +0.04] | too few |
| GUARANTEE | 14 | 0.824 [0.74–0.90] | 8/14 (57.1%) | 0/14 | – | -0.012 [-0.13 to +0.12] | too few |
| MEDICAL | 4 | 0.889 [0.73–1.00] | 3/4 (75.0%) | 0/4 | – | +0.063 [-0.10 to +0.23] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.175 [+0.11 to +0.25] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / prompt-rules

**ad_policy / dev / prompt-rules: 87 items, 9 labels.** Micro F1 0.917 [0.85–0.97], macro F1 0.938 [0.87–0.98], exact match 79/87 (90.8%) [83–95].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 13 | 10 | 3 | 2 | 76.9% [50–92] | 83.3% [55–95] | 0.800 [0.57–0.95] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 6 | 6 | 0 | 2 | 100.0% [61–100] | 75.0% [41–93] | 0.857 [0.57–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 48 | 44 | 4 | 4 | 91.7% | 91.7% | 0.917 [0.85–0.97] |

Miss rate (a labelled item predicted with no label): 3/45 (6.7%) [2–18]. False-alarm rate (an unlabelled item given a label): 2/42 (4.8%) [1–16].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 48/48; cost $0.0092 ($0.106 per 1,000 items).

Confusion: exact 79, under-labelled 4, over-labelled 4, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| ABSOLUTE | (no predicted label) | 2 | missed |
| DISPARAGE | (no predicted label) | 2 | missed |
| GUARANTEE | ABSOLUTE | 2 | confused |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |

**Slices of 87 items.** Overall micro F1 0.917, exact match 90.8%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.927 [0.83–1.00] | 37/40 (92.5%) | 1/20 | 2/20 | +0.018 [-0.10 to +0.13] | no measured difference |
| zh | 47 | 0.909 [0.83–0.98] | 42/47 (89.4%) | 2/25 | 0/22 | -0.018 [-0.12 to +0.11] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.121 [+0.05 to +0.21] | better |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.087 [+0.03 to +0.15] | too few |
| synthetic | 60 | 0.871 [0.78–0.94] | 52/60 (86.7%) | 3/28 | 2/32 | -0.129 [-0.22 to -0.06] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.936 [0.89–0.98] | 39/45 (86.7%) | 3/45 | – | -0.086 [-0.20 to +0.03] (exact match) | no measured difference |
| look-alike | 27 | – | 26/27 (96.3%) | – | 1/27 | +0.080 [-0.03 to +0.18] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.031 [-0.12 to +0.15] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 0.968 [0.90–1.00] | 28/29 (96.6%) | 0/15 | 0/14 | +0.075 [-0.03 to +0.18] | no measured difference |
| 56–92 chars | 29 | 0.889 [0.78–0.98] | 25/29 (86.2%) | 2/16 | 0/13 | -0.044 [-0.17 to +0.06] | no measured difference |
| 93–177 chars | 29 | 0.897 [0.74–1.00] | 26/29 (89.7%) | 1/14 | 2/15 | -0.029 [-0.20 to +0.10] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 40/42 (95.2%) | – | 2/42 | +0.086 [-0.03 to +0.20] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.929 [0.81–1.00] | 10/12 (83.3%) | 1/12 | – | +0.017 [-0.11 to +0.13] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.093 [+0.04 to +0.15] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.089 [+0.03 to +0.15] | too few |
| DISPARAGE | 8 | 0.842 [0.57–0.96] | 5/8 (62.5%) | 2/8 | – | -0.093 [-0.35 to +0.06] | too few |
| GUARANTEE | 14 | 0.933 [0.85–1.00] | 12/14 (85.7%) | 0/14 | – | +0.024 [-0.08 to +0.14] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.091 [+0.04 to +0.15] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.087 [+0.04 to +0.15] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent

**ad_policy / dev / agent: 87 items, 9 labels.** Micro F1 0.898 [0.83–0.95], macro F1 0.904 [0.81–0.96], exact match 77/87 (88.5%) [80–94].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 5 | 4 | 1 | 0 | 80.0% [38–96] | 100.0% [51–100] | 0.889 [0.50–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 6 | 6 | 0 | 2 | 100.0% [61–100] | 75.0% [41–93] | 0.857 [0.57–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 9 | 5 | 4 | 0 | 55.6% [27–81] | 100.0% [57–100] | 0.714 [0.33–0.95] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 50 | 44 | 6 | 4 | 88.0% | 91.7% | 0.898 [0.83–0.95] |

Miss rate (a labelled item predicted with no label): 3/45 (6.7%) [2–18]. False-alarm rate (an unlabelled item given a label): 5/42 (11.9%) [5–25].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 1.86 calls and 0.81 tool calls per item; rule gate 5, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 50/50; cost $0.0206 ($0.237 per 1,000 items). Items on which each tool was called: get_label_rules 80%.

Confusion: exact 77, under-labelled 4, over-labelled 6, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ALCOHOL | 4 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| DISPARAGE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| GUARANTEE | MEDICAL | 1 | confused |

**Slices of 87 items.** Overall micro F1 0.898, exact match 88.5%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.884 [0.78–0.97] | 35/40 (87.5%) | 1/20 | 3/20 | -0.025 [-0.15 to +0.12] | no measured difference |
| zh | 47 | 0.909 [0.82–0.98] | 42/47 (89.4%) | 2/25 | 2/22 | +0.025 [-0.11 to +0.16] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.147 [+0.07 to +0.25] | better |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.106 [+0.05 to +0.17] | too few |
| synthetic | 60 | 0.844 [0.73–0.93] | 50/60 (83.3%) | 3/28 | 5/32 | -0.156 [-0.27 to -0.07] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.946 [0.90–0.99] | 40/45 (88.9%) | 3/45 | – | +0.008 [-0.13 to +0.15] (exact match) | no measured difference |
| look-alike | 27 | – | 23/27 (85.2%) | – | 4/27 | -0.048 [-0.20 to +0.10] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.058 [-0.09 to +0.18] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 1.000 [1.00–1.00] | 29/29 (100.0%) | 0/15 | 0/14 | +0.147 [+0.07 to +0.25] | better |
| 56–92 chars | 29 | 0.865 [0.73–0.97] | 24/29 (82.8%) | 2/16 | 2/13 | -0.053 [-0.19 to +0.07] | no measured difference |
| 93–177 chars | 29 | 0.839 [0.67–0.96] | 24/29 (82.8%) | 1/14 | 3/15 | -0.087 [-0.27 to +0.05] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 37/42 (88.1%) | – | 5/42 | -0.008 [-0.15 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.929 [0.81–1.00] | 10/12 (83.3%) | 1/12 | – | +0.043 [-0.09 to +0.16] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.114 [+0.05 to +0.19] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.109 [+0.05 to +0.18] | too few |
| DISPARAGE | 8 | 0.842 [0.57–0.96] | 5/8 (62.5%) | 2/8 | – | -0.069 [-0.32 to +0.09] | too few |
| GUARANTEE | 14 | 0.966 [0.90–1.00] | 13/14 (92.9%) | 0/14 | – | +0.096 [-0.01 to +0.20] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.111 [+0.05 to +0.19] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.106 [+0.05 to +0.17] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases

**ad_policy / dev / agent-cases: 87 items, 9 labels.** Micro F1 0.905 [0.84–0.96], macro F1 0.909 [0.82–0.96], exact match 78/87 (89.7%) [81–94].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 5 | 4 | 1 | 0 | 80.0% [38–96] | 100.0% [51–100] | 0.889 [0.50–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 5 | 0 | 3 | 100.0% [57–100] | 62.5% [31–86] | 0.769 [0.40–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 7 | 5 | 2 | 0 | 71.4% [36–92] | 100.0% [57–100] | 0.833 [0.50–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 47 | 43 | 4 | 5 | 91.5% | 89.6% | 0.905 [0.84–0.96] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 3/42 (7.1%) [2–19].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 1.62 calls and 0.26 tool calls per item; rule gate 35, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 47/47; cost $0.0227 ($0.261 per 1,000 items). Items on which each tool was called: get_label_rules 22%, search_cases 5%.

Confusion: exact 78, under-labelled 5, over-labelled 4, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DISPARAGE | (no predicted label) | 3 | missed |
| (no gold label) | ALCOHOL | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| GUARANTEE | MEDICAL | 1 | confused |

**Slices of 87 items.** Overall micro F1 0.905, exact match 89.7%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.905 [0.80–0.98] | 36/40 (90.0%) | 1/20 | 2/20 | -0.001 [-0.13 to +0.12] | no measured difference |
| zh | 47 | 0.906 [0.81–0.98] | 42/47 (89.4%) | 3/25 | 1/22 | +0.001 [-0.13 to +0.12] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.138 [+0.06 to +0.24] | better |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.099 [+0.04 to +0.16] | too few |
| synthetic | 60 | 0.852 [0.74–0.94] | 51/60 (85.0%) | 4/28 | 3/32 | -0.148 [-0.26 to -0.06] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.935 [0.88–0.98] | 39/45 (86.7%) | 4/45 | – | -0.062 [-0.18 to +0.06] (exact match) | no measured difference |
| look-alike | 27 | – | 25/27 (92.6%) | – | 2/27 | +0.043 [-0.09 to +0.17] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.044 [-0.10 to +0.17] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 0.968 [0.89–1.00] | 28/29 (96.6%) | 0/15 | 1/14 | +0.093 [-0.02 to +0.20] | no measured difference |
| 56–92 chars | 29 | 0.882 [0.76–0.97] | 25/29 (86.2%) | 3/16 | 0/13 | -0.036 [-0.18 to +0.08] | no measured difference |
| 93–177 chars | 29 | 0.867 [0.71–0.97] | 25/29 (86.2%) | 1/14 | 2/15 | -0.056 [-0.23 to +0.08] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 39/42 (92.9%) | – | 3/42 | +0.062 [-0.07 to +0.18] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.929 [0.81–1.00] | 10/12 (83.3%) | 1/12 | – | +0.033 [-0.09 to +0.15] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.106 [+0.04 to +0.18] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.101 [+0.04 to +0.17] | too few |
| DISPARAGE | 8 | 0.778 [0.46–0.96] | 4/8 (50.0%) | 3/8 | – | -0.157 [-0.48 to +0.01] | too few |
| GUARANTEE | 14 | 0.966 [0.90–1.00] | 13/14 (92.9%) | 0/14 | – | +0.087 [-0.01 to +0.19] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.103 [+0.05 to +0.17] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.099 [+0.04 to +0.16] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases-check

**ad_policy / dev / agent-cases-check: 87 items, 9 labels.** Micro F1 0.913 [0.84–0.97], macro F1 0.921 [0.83–0.97], exact match 80/87 (92.0%) [84–96].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 4 | 4 | 0 | 4 | 100.0% [51–100] | 50.0% [22–78] | 0.667 [0.25–0.92] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 44 | 42 | 2 | 6 | 95.5% | 87.5% | 0.913 [0.84–0.97] |

Miss rate (a labelled item predicted with no label): 5/45 (11.1%) [5–23]. False-alarm rate (an unlabelled item given a label): 2/42 (4.8%) [1–16].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 2.88 calls and 0.53 tool calls per item; rule gate 37, quote repair 1, self-check changed 2 of 87 items (+0 / −2 labels); exact quotes 44/44; cost $0.0454 ($0.521 per 1,000 items). Items on which each tool was called: get_label_rules 44%, phrase_stats 1%, search_cases 5%.

Confusion: exact 80, under-labelled 5, over-labelled 2, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DISPARAGE | (no predicted label) | 4 | missed |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |

**Slices of 87 items.** Overall micro F1 0.913, exact match 92.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.927 [0.83–1.00] | 37/40 (92.5%) | 1/20 | 2/20 | +0.025 [-0.11 to +0.16] | no measured difference |
| zh | 47 | 0.902 [0.78–0.98] | 43/47 (91.5%) | 4/25 | 0/22 | -0.025 [-0.17 to +0.10] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.129 [+0.05 to +0.25] | better |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.091 [+0.03 to +0.17] | too few |
| synthetic | 60 | 0.862 [0.73–0.95] | 53/60 (88.3%) | 5/28 | 2/32 | -0.138 [-0.27 to -0.05] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.933 [0.86–0.99] | 40/45 (88.9%) | 5/45 | – | -0.063 [-0.18 to +0.05] (exact match) | no measured difference |
| look-alike | 27 | – | 26/27 (96.3%) | – | 1/27 | +0.063 [-0.04 to +0.17] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.017 [-0.13 to +0.14] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 1.000 [1.00–1.00] | 29/29 (100.0%) | 0/15 | 0/14 | +0.129 [+0.04 to +0.25] | better |
| 56–92 chars | 29 | 0.848 [0.67–0.97] | 25/29 (86.2%) | 4/16 | 0/13 | -0.101 [-0.29 to +0.04] | no measured difference |
| 93–177 chars | 29 | 0.897 [0.74–1.00] | 26/29 (89.7%) | 1/14 | 2/15 | -0.024 [-0.20 to +0.11] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 40/42 (95.2%) | – | 2/42 | +0.063 [-0.05 to +0.18] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.69–1.00] | 10/12 (83.3%) | 2/12 | – | -0.034 [-0.24 to +0.11] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.098 [+0.03 to +0.18] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.093 [+0.03 to +0.18] | too few |
| DISPARAGE | 8 | 0.706 [0.31–0.92] | 4/8 (50.0%) | 4/8 | – | -0.254 [-0.68 to -0.02] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.125 [+0.04 to +0.23] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.095 [+0.03 to +0.17] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.091 [+0.03 to +0.16] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases-check-medium

**ad_policy / dev / agent-cases-check-medium: 87 items, 9 labels.** Micro F1 0.915 [0.84–0.97], macro F1 0.925 [0.84–0.97], exact match 80/87 (92.0%) [84–96].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 5 | 0 | 3 | 100.0% [57–100] | 62.5% [31–86] | 0.769 [0.40–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 7 | 5 | 2 | 0 | 71.4% [36–92] | 100.0% [57–100] | 0.833 [0.50–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 46 | 43 | 3 | 5 | 93.5% | 89.6% | 0.915 [0.84–0.97] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 3/42 (7.1%) [2–19].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 87/87 answered; 3.08 calls and 1.14 tool calls per item; rule gate 9, quote repair 0, self-check changed 3 of 87 items (+1 / −2 labels); exact quotes 46/46; cost $0.0535 ($0.615 per 1,000 items). Items on which each tool was called: compare_labels 1%, get_label_rules 92%, phrase_stats 5%, search_cases 11%.

Confusion: exact 80, under-labelled 4, over-labelled 3, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DISPARAGE | (no predicted label) | 3 | missed |
| (no gold label) | ALCOHOL | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |

**Slices of 87 items.** Overall micro F1 0.915, exact match 92.0%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 40 | 0.927 [0.83–1.00] | 37/40 (92.5%) | 1/20 | 2/20 | +0.021 [-0.10 to +0.15] | no measured difference |
| zh | 47 | 0.906 [0.79–0.98] | 43/47 (91.5%) | 3/25 | 1/22 | -0.021 [-0.16 to +0.11] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.125 [+0.05 to +0.24] | better |
| video-words | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/2 | 0/1 | +0.089 [+0.03 to +0.16] | too few |
| synthetic | 60 | 0.867 [0.75–0.96] | 53/60 (88.3%) | 4/28 | 3/32 | -0.133 [-0.25 to -0.04] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.945 [0.88–0.99] | 41/45 (91.1%) | 4/45 | – | -0.017 [-0.13 to +0.10] (exact match) | no measured difference |
| look-alike | 27 | – | 25/27 (92.6%) | – | 2/27 | +0.009 [-0.11 to +0.13] (exact match) | no measured difference |
| plain | 15 | – | 14/15 (93.3%) | – | 1/15 | +0.017 [-0.13 to +0.12] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–55 chars | 29 | 0.968 [0.89–1.00] | 28/29 (96.6%) | 0/15 | 1/14 | +0.079 [-0.03 to +0.20] | no measured difference |
| 56–92 chars | 29 | 0.882 [0.73–1.00] | 26/29 (89.7%) | 3/16 | 0/13 | -0.051 [-0.22 to +0.08] | no measured difference |
| 93–177 chars | 29 | 0.897 [0.74–1.00] | 26/29 (89.7%) | 1/14 | 2/15 | -0.027 [-0.20 to +0.12] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 42 | – | 39/42 (92.9%) | – | 3/42 | +0.017 [-0.12 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.69–1.00] | 10/12 (83.3%) | 2/12 | – | -0.036 [-0.25 to +0.10] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.095 [+0.03 to +0.18] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.091 [+0.02 to +0.17] | too few |
| DISPARAGE | 8 | 0.778 [0.46–0.96] | 5/8 (62.5%) | 3/8 | – | -0.170 [-0.49 to +0.03] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.121 [+0.04 to +0.23] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.093 [+0.03 to +0.17] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.089 [+0.03 to +0.16] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-short

**asap / dev / prompt-short: 60 items, 18 labels.** Micro F1 0.736 [0.71–0.76], macro F1 0.689 [0.64–0.72], exact match 1/60 (1.7%) [0–9].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 59 | 57 | 2 | 0 | 96.6% [88–99] | 100.0% [94–100] | 0.983 [0.96–1.00] |
| Food#Appearance | 16 | 23 | 11 | 12 | 5 | 47.8% [29–67] | 68.8% [44–86] | 0.564 [0.36–0.73] |
| Food#Portion | 28 | 30 | 23 | 7 | 5 | 76.7% [59–88] | 82.1% [64–92] | 0.793 [0.65–0.90] |
| Food#Recommend | 12 | 43 | 12 | 31 | 0 | 27.9% [17–43] | 100.0% [76–100] | 0.436 [0.26–0.59] |
| Price#Level | 34 | 25 | 24 | 1 | 10 | 96.0% [80–99] | 70.6% [54–83] | 0.814 [0.69–0.91] |
| Price#Cost_effective | 13 | 28 | 13 | 15 | 0 | 46.4% [30–64] | 100.0% [77–100] | 0.634 [0.44–0.79] |
| Price#Discount | 16 | 10 | 8 | 2 | 8 | 80.0% [49–94] | 50.0% [28–72] | 0.615 [0.35–0.81] |
| Location#Downtown | 16 | 11 | 6 | 5 | 10 | 54.5% [28–79] | 37.5% [18–61] | 0.444 [0.18–0.65] |
| Location#Transportation | 13 | 12 | 9 | 3 | 4 | 75.0% [47–91] | 69.2% [42–87] | 0.720 [0.47–0.89] |
| Location#Easy_to_find | 11 | 14 | 8 | 6 | 3 | 57.1% [33–79] | 72.7% [43–90] | 0.640 [0.36–0.84] |
| Service#Queue | 10 | 14 | 8 | 6 | 2 | 57.1% [33–79] | 80.0% [49–94] | 0.667 [0.40–0.86] |
| Service#Hospitality | 35 | 36 | 33 | 3 | 2 | 91.7% [78–97] | 94.3% [81–98] | 0.930 [0.86–0.99] |
| Service#Parking | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| Service#Timely | 13 | 26 | 13 | 13 | 0 | 50.0% [32–68] | 100.0% [77–100] | 0.667 [0.46–0.83] |
| Ambience#Decoration | 28 | 28 | 24 | 4 | 4 | 85.7% [69–94] | 85.7% [69–94] | 0.857 [0.75–0.94] |
| Ambience#Noise | 23 | 11 | 8 | 3 | 15 | 72.7% [43–90] | 34.8% [19–55] | 0.471 [0.25–0.67] |
| Ambience#Space | 26 | 29 | 22 | 7 | 4 | 75.9% [58–88] | 84.6% [66–94] | 0.800 [0.67–0.90] |
| Ambience#Sanitary | 24 | 13 | 10 | 3 | 14 | 76.9% [50–92] | 41.7% [24–61] | 0.541 [0.32–0.72] |
| **micro** | 382 | 417 | 294 | 123 | 88 | 70.5% | 77.0% | 0.736 [0.71–0.76] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 408/417; cost $0.0120 ($0.200 per 1,000 items).

Confusion: exact 1, under-labelled 4, over-labelled 21, swapped 34.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Food#Recommend | 10 | confused |
| Price#Level | Food#Recommend | 10 | confused |
| Service#Hospitality | Food#Recommend | 8 | confused |
| Ambience#Noise | Food#Recommend | 7 | confused |
| Price#Level | Price#Cost_effective | 7 | confused |
| Food#Appearance | Food#Recommend | 6 | confused |
| Location#Downtown | Food#Recommend | 6 | confused |
| Ambience#Decoration | Food#Recommend | 5 | confused |
| Ambience#Noise | Food#Appearance | 5 | confused |
| Ambience#Sanitary | Food#Recommend | 5 | confused |

**Slices of 60 items.** Overall micro F1 0.736, exact match 1.7%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.739 [0.71–0.77] | 1/45 (2.2%) | 0/45 | – | +0.015 [-0.04 to +0.07] | no measured difference |
| 1-3 stars | 15 | 0.724 [0.68–0.76] | 0/15 (0.0%) | 0/15 | – | -0.015 [-0.07 to +0.03] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.749 [0.71–0.80] | 1/22 (4.5%) | 0/22 | – | +0.021 [-0.03 to +0.08] | no measured difference |
| 8+ labels | 23 | 0.750 [0.72–0.78] | 0/23 (0.0%) | 0/23 | – | +0.028 [-0.03 to +0.08] | no measured difference |
| 1-4 labels | 15 | 0.648 [0.57–0.72] | 0/15 (0.0%) | 0/15 | – | -0.101 [-0.19 to -0.02] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.740 [0.71–0.77] | 1/50 (2.0%) | 0/50 | – | +0.030 [-0.04 to +0.09] | no measured difference |
| no neutral mention | 10 | 0.711 [0.65–0.77] | 0/10 (0.0%) | 0/10 | – | -0.030 [-0.10 to +0.04] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.725 [0.66–0.78] | 1/20 (5.0%) | 0/20 | – | -0.015 [-0.09 to +0.05] | no measured difference |
| 241–332 chars | 20 | 0.732 [0.69–0.77] | 0/20 (0.0%) | 0/20 | – | -0.005 [-0.06 to +0.05] | no measured difference |
| 333–579 chars | 20 | 0.748 [0.71–0.79] | 0/20 (0.0%) | 0/20 | – | +0.019 [-0.04 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.750 [0.72–0.79] | 1/28 (3.6%) | 0/28 | – | +0.031 [-0.02 to +0.09] | no measured difference |
| Ambience#Noise | 23 | 0.732 [0.70–0.77] | 0/23 (0.0%) | 0/23 | – | -0.008 [-0.06 to +0.05] | no measured difference |
| Ambience#Sanitary | 24 | 0.732 [0.69–0.77] | 0/24 (0.0%) | 0/24 | – | -0.008 [-0.06 to +0.04] | no measured difference |
| Ambience#Space | 26 | 0.749 [0.72–0.78] | 0/26 (0.0%) | 0/26 | – | +0.027 [-0.03 to +0.08] | no measured difference |
| Food#Appearance | 16 | 0.756 [0.71–0.80] | 1/16 (6.2%) | 0/16 | – | +0.029 [-0.03 to +0.08] | too few |
| Food#Portion | 28 | 0.745 [0.71–0.78] | 0/28 (0.0%) | 0/28 | – | +0.020 [-0.03 to +0.07] | no measured difference |
| Food#Recommend | 12 | 0.776 [0.73–0.84] | 1/12 (8.3%) | 0/12 | – | +0.052 [-0.01 to +0.12] | too few |
| Food#Taste | 57 | 0.732 [0.71–0.76] | 1/57 (1.8%) | 0/57 | – | -0.095 [-0.19 to +0.05] | no measured difference |
| Location#Downtown | 16 | 0.732 [0.69–0.77] | 0/16 (0.0%) | 0/16 | – | -0.006 [-0.06 to +0.05] | too few |
| Location#Easy_to_find | 11 | 0.759 [0.70–0.81] | 0/11 (0.0%) | 0/11 | – | +0.029 [-0.04 to +0.10] | too few |
| Location#Transportation | 13 | 0.739 [0.69–0.79] | 0/13 (0.0%) | 0/13 | – | +0.004 [-0.05 to +0.06] | too few |
| Price#Cost_effective | 13 | 0.757 [0.72–0.79] | 0/13 (0.0%) | 0/13 | – | +0.029 [-0.02 to +0.08] | too few |
| Price#Discount | 16 | 0.718 [0.66–0.77] | 0/16 (0.0%) | 0/16 | – | -0.025 [-0.09 to +0.04] | too few |
| Price#Level | 34 | 0.753 [0.72–0.79] | 0/34 (0.0%) | 0/34 | – | +0.049 [-0.00 to +0.11] | no measured difference |
| Service#Hospitality | 35 | 0.735 [0.71–0.77] | 0/35 (0.0%) | 0/35 | – | -0.003 [-0.06 to +0.05] | no measured difference |
| Service#Parking | 7 | 0.739 [0.69–0.79] | 0/7 (0.0%) | 0/7 | – | +0.003 [-0.05 to +0.06] | too few |
| Service#Queue | 10 | 0.783 [0.72–0.85] | 1/10 (10.0%) | 0/10 | – | +0.058 [-0.01 to +0.13] | too few |
| Service#Timely | 13 | 0.768 [0.73–0.82] | 1/13 (7.7%) | 0/13 | – | +0.042 [-0.01 to +0.10] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-rules

**asap / dev / prompt-rules: 60 items, 18 labels.** Micro F1 0.799 [0.76–0.83], macro F1 0.767 [0.72–0.80], exact match 4/60 (6.7%) [3–16].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 60 | 57 | 3 | 0 | 95.0% [86–98] | 100.0% [94–100] | 0.974 [0.94–1.00] |
| Food#Appearance | 16 | 26 | 15 | 11 | 1 | 57.7% [39–74] | 93.8% [72–99] | 0.714 [0.55–0.86] |
| Food#Portion | 28 | 28 | 22 | 6 | 6 | 78.6% [60–90] | 78.6% [60–90] | 0.786 [0.64–0.89] |
| Food#Recommend | 12 | 36 | 12 | 24 | 0 | 33.3% [20–50] | 100.0% [76–100] | 0.500 [0.31–0.66] |
| Price#Level | 34 | 29 | 27 | 2 | 7 | 93.1% [78–98] | 79.4% [63–90] | 0.857 [0.75–0.94] |
| Price#Cost_effective | 13 | 25 | 12 | 13 | 1 | 48.0% [30–67] | 92.3% [67–99] | 0.632 [0.42–0.79] |
| Price#Discount | 16 | 14 | 11 | 3 | 5 | 78.6% [52–92] | 68.8% [44–86] | 0.733 [0.52–0.89] |
| Location#Downtown | 16 | 18 | 10 | 8 | 6 | 55.6% [34–75] | 62.5% [39–82] | 0.588 [0.38–0.77] |
| Location#Transportation | 13 | 11 | 8 | 3 | 5 | 72.7% [43–90] | 61.5% [36–82] | 0.667 [0.36–0.86] |
| Location#Easy_to_find | 11 | 13 | 10 | 3 | 1 | 76.9% [50–92] | 90.9% [62–98] | 0.833 [0.62–0.97] |
| Service#Queue | 10 | 13 | 8 | 5 | 2 | 61.5% [36–82] | 80.0% [49–94] | 0.696 [0.43–0.88] |
| Service#Hospitality | 35 | 37 | 34 | 3 | 1 | 91.9% [79–97] | 97.1% [85–99] | 0.944 [0.88–0.99] |
| Service#Parking | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| Service#Timely | 13 | 22 | 13 | 9 | 0 | 59.1% [39–77] | 100.0% [77–100] | 0.743 [0.55–0.89] |
| Ambience#Decoration | 28 | 34 | 25 | 9 | 3 | 73.5% [57–85] | 89.3% [73–96] | 0.806 [0.68–0.90] |
| Ambience#Noise | 23 | 22 | 19 | 3 | 4 | 86.4% [67–95] | 82.6% [63–93] | 0.844 [0.71–0.94] |
| Ambience#Space | 26 | 32 | 23 | 9 | 3 | 71.9% [55–84] | 88.5% [71–96] | 0.793 [0.66–0.89] |
| Ambience#Sanitary | 24 | 27 | 22 | 5 | 2 | 81.5% [63–92] | 91.7% [74–98] | 0.863 [0.75–0.95] |
| **micro** | 382 | 452 | 333 | 119 | 49 | 73.7% | 87.2% | 0.799 [0.76–0.83] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 440/452; cost $0.0153 ($0.255 per 1,000 items).

Confusion: exact 4, under-labelled 9, over-labelled 26, swapped 21.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Food#Recommend | 12 | confused |
| Price#Level | Food#Recommend | 10 | confused |
| Food#Portion | Price#Cost_effective | 8 | confused |
| Food#Taste | Price#Cost_effective | 8 | confused |
| Price#Level | Price#Cost_effective | 8 | confused |
| Ambience#Space | Food#Recommend | 7 | confused |
| Food#Portion | Food#Recommend | 7 | confused |
| Service#Hospitality | Food#Recommend | 6 | confused |
| Food#Portion | Food#Appearance | 5 | confused |
| Food#Taste | Ambience#Decoration | 5 | confused |

**Slices of 60 items.** Overall micro F1 0.799, exact match 6.7%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.791 [0.75–0.83] | 3/45 (6.7%) | 0/45 | – | -0.031 [-0.11 to +0.06] | no measured difference |
| 1-3 stars | 15 | 0.822 [0.74–0.88] | 1/15 (6.7%) | 0/15 | – | +0.031 [-0.06 to +0.11] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.771 [0.72–0.83] | 3/22 (13.6%) | 0/22 | – | -0.042 [-0.10 to +0.03] | no measured difference |
| 8+ labels | 23 | 0.863 [0.83–0.90] | 1/23 (4.3%) | 0/23 | – | +0.132 [+0.08 to +0.19] | better |
| 1-4 labels | 15 | 0.632 [0.59–0.68] | 0/15 (0.0%) | 0/15 | – | -0.193 [-0.25 to -0.13] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.798 [0.76–0.83] | 3/50 (6.0%) | 0/50 | – | -0.002 [-0.09 to +0.10] | no measured difference |
| no neutral mention | 10 | 0.800 [0.70–0.88] | 1/10 (10.0%) | 0/10 | – | +0.002 [-0.10 to +0.09] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.805 [0.74–0.86] | 4/20 (20.0%) | 0/20 | – | +0.009 [-0.07 to +0.08] | no measured difference |
| 241–332 chars | 20 | 0.786 [0.73–0.84] | 0/20 (0.0%) | 0/20 | – | -0.019 [-0.09 to +0.05] | no measured difference |
| 333–579 chars | 20 | 0.805 [0.74–0.86] | 0/20 (0.0%) | 0/20 | – | +0.011 [-0.07 to +0.09] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.850 [0.81–0.89] | 2/28 (7.1%) | 0/28 | – | +0.118 [+0.05 to +0.19] | better |
| Ambience#Noise | 23 | 0.835 [0.79–0.88] | 1/23 (4.3%) | 0/23 | – | +0.070 [+0.00 to +0.14] | better |
| Ambience#Sanitary | 24 | 0.864 [0.82–0.90] | 2/24 (8.3%) | 0/24 | – | +0.126 [+0.07 to +0.19] | better |
| Ambience#Space | 26 | 0.861 [0.82–0.89] | 1/26 (3.8%) | 0/26 | – | +0.132 [+0.07 to +0.19] | better |
| Food#Appearance | 16 | 0.845 [0.77–0.90] | 2/16 (12.5%) | 0/16 | – | +0.066 [-0.01 to +0.14] | too few |
| Food#Portion | 28 | 0.819 [0.77–0.86] | 1/28 (3.6%) | 0/28 | – | +0.046 [-0.02 to +0.11] | no measured difference |
| Food#Recommend | 12 | 0.827 [0.75–0.89] | 2/12 (16.7%) | 0/12 | – | +0.036 [-0.05 to +0.11] | too few |
| Food#Taste | 57 | 0.797 [0.76–0.83] | 4/57 (7.0%) | 0/57 | – | -0.042 [-0.11 to +0.11] | no measured difference |
| Location#Downtown | 16 | 0.866 [0.82–0.90] | 0/16 (0.0%) | 0/16 | – | +0.103 [+0.05 to +0.16] | too few |
| Location#Easy_to_find | 11 | 0.813 [0.72–0.89] | 0/11 (0.0%) | 0/11 | – | +0.018 [-0.08 to +0.11] | too few |
| Location#Transportation | 13 | 0.794 [0.72–0.86] | 1/13 (7.7%) | 0/13 | – | -0.006 [-0.09 to +0.07] | too few |
| Price#Cost_effective | 13 | 0.840 [0.78–0.90] | 1/13 (7.7%) | 0/13 | – | +0.056 [-0.02 to +0.13] | too few |
| Price#Discount | 16 | 0.791 [0.72–0.85] | 0/16 (0.0%) | 0/16 | – | -0.012 [-0.09 to +0.06] | too few |
| Price#Level | 34 | 0.825 [0.78–0.86] | 2/34 (5.9%) | 0/34 | – | +0.072 [+0.00 to +0.15] | better |
| Service#Hospitality | 35 | 0.807 [0.77–0.85] | 2/35 (5.7%) | 0/35 | – | +0.026 [-0.05 to +0.10] | no measured difference |
| Service#Parking | 7 | 0.786 [0.69–0.89] | 1/7 (14.3%) | 0/7 | – | -0.015 [-0.12 to +0.09] | too few |
| Service#Queue | 10 | 0.803 [0.70–0.88] | 1/10 (10.0%) | 0/10 | – | +0.005 [-0.10 to +0.10] | too few |
| Service#Timely | 13 | 0.812 [0.72–0.88] | 2/13 (15.4%) | 0/13 | – | +0.017 [-0.08 to +0.10] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent

**asap / dev / agent: 60 items, 18 labels.** Micro F1 0.841 [0.81–0.87], macro F1 0.791 [0.74–0.83], exact match 10/60 (16.7%) [9–28].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 58 | 57 | 1 | 0 | 98.3% [91–100] | 100.0% [94–100] | 0.991 [0.97–1.00] |
| Food#Appearance | 16 | 14 | 11 | 3 | 5 | 78.6% [52–92] | 68.8% [44–86] | 0.733 [0.52–0.89] |
| Food#Portion | 28 | 23 | 20 | 3 | 8 | 87.0% [68–95] | 71.4% [53–85] | 0.784 [0.64–0.89] |
| Food#Recommend | 12 | 15 | 11 | 4 | 1 | 73.3% [48–89] | 91.7% [65–99] | 0.815 [0.62–0.95] |
| Price#Level | 34 | 24 | 24 | 0 | 10 | 100.0% [86–100] | 70.6% [54–83] | 0.828 [0.70–0.92] |
| Price#Cost_effective | 13 | 18 | 13 | 5 | 0 | 72.2% [49–88] | 100.0% [77–100] | 0.839 [0.67–0.96] |
| Price#Discount | 16 | 12 | 9 | 3 | 7 | 75.0% [47–91] | 56.2% [33–77] | 0.643 [0.40–0.83] |
| Location#Downtown | 16 | 4 | 4 | 0 | 12 | 100.0% [51–100] | 25.0% [10–49] | 0.400 [0.11–0.67] |
| Location#Transportation | 13 | 8 | 8 | 0 | 5 | 100.0% [68–100] | 61.5% [36–82] | 0.762 [0.47–0.94] |
| Location#Easy_to_find | 11 | 10 | 9 | 1 | 2 | 90.0% [60–98] | 81.8% [52–95] | 0.857 [0.63–1.00] |
| Service#Queue | 10 | 11 | 6 | 5 | 4 | 54.5% [28–79] | 60.0% [31–83] | 0.571 [0.29–0.80] |
| Service#Hospitality | 35 | 31 | 31 | 0 | 4 | 100.0% [89–100] | 88.6% [74–95] | 0.939 [0.88–0.99] |
| Service#Parking | 7 | 4 | 4 | 0 | 3 | 100.0% [51–100] | 57.1% [25–84] | 0.727 [0.33–1.00] |
| Service#Timely | 13 | 17 | 13 | 4 | 0 | 76.5% [53–90] | 100.0% [77–100] | 0.867 [0.71–0.97] |
| Ambience#Decoration | 28 | 28 | 25 | 3 | 3 | 89.3% [73–96] | 89.3% [73–96] | 0.893 [0.79–0.97] |
| Ambience#Noise | 23 | 18 | 18 | 0 | 5 | 100.0% [82–100] | 78.3% [58–90] | 0.878 [0.74–0.97] |
| Ambience#Space | 26 | 26 | 22 | 4 | 4 | 84.6% [66–94] | 84.6% [66–94] | 0.846 [0.72–0.94] |
| Ambience#Sanitary | 24 | 22 | 20 | 2 | 4 | 90.9% [72–97] | 83.3% [64–93] | 0.870 [0.74–0.96] |
| **micro** | 382 | 343 | 305 | 38 | 77 | 88.9% | 79.8% | 0.841 [0.81–0.87] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 2.20 calls and 0.37 tool calls per item; rule gate 48, quote repair 3, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 343/343; cost $0.0463 ($0.772 per 1,000 items). Items on which each tool was called: compare_labels 2%, get_label_rules 35%.

Confusion: exact 10, under-labelled 24, over-labelled 9, swapped 17.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Location#Downtown | (no predicted label) | 10 | missed |
| Price#Level | (no predicted label) | 6 | missed |
| Food#Portion | (no predicted label) | 5 | missed |
| Location#Transportation | (no predicted label) | 5 | missed |
| Food#Appearance | (no predicted label) | 4 | missed |
| Ambience#Sanitary | (no predicted label) | 3 | missed |
| Food#Portion | Price#Cost_effective | 3 | confused |
| Location#Downtown | Service#Queue | 3 | confused |
| Price#Discount | (no predicted label) | 3 | missed |
| Price#Level | Price#Cost_effective | 3 | confused |

**Slices of 60 items.** Overall micro F1 0.841, exact match 16.7%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.835 [0.80–0.87] | 6/45 (13.3%) | 0/45 | – | -0.025 [-0.08 to +0.04] | no measured difference |
| 1-3 stars | 15 | 0.860 [0.81–0.91] | 4/15 (26.7%) | 0/15 | – | +0.025 [-0.04 to +0.09] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.856 [0.81–0.90] | 4/22 (18.2%) | 0/22 | – | +0.022 [-0.03 to +0.08] | no measured difference |
| 8+ labels | 23 | 0.848 [0.81–0.89] | 1/23 (4.3%) | 0/23 | – | +0.015 [-0.05 to +0.07] | no measured difference |
| 1-4 labels | 15 | 0.767 [0.66–0.88] | 5/15 (33.3%) | 0/15 | – | -0.084 [-0.19 to +0.03] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.831 [0.80–0.86] | 6/50 (12.0%) | 0/50 | – | -0.068 [-0.14 to +0.00] | no measured difference |
| no neutral mention | 10 | 0.899 [0.83–0.96] | 4/10 (40.0%) | 0/10 | – | +0.068 [-0.01 to +0.14] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.824 [0.75–0.88] | 3/20 (15.0%) | 0/20 | – | -0.025 [-0.11 to +0.05] | no measured difference |
| 241–332 chars | 20 | 0.831 [0.79–0.87] | 3/20 (15.0%) | 0/20 | – | -0.015 [-0.07 to +0.05] | no measured difference |
| 333–579 chars | 20 | 0.865 [0.82–0.91] | 4/20 (20.0%) | 0/20 | – | +0.037 [-0.02 to +0.10] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.845 [0.80–0.89] | 4/28 (14.3%) | 0/28 | – | +0.009 [-0.05 to +0.07] | no measured difference |
| Ambience#Noise | 23 | 0.834 [0.79–0.88] | 2/23 (8.7%) | 0/23 | – | -0.014 [-0.07 to +0.04] | no measured difference |
| Ambience#Sanitary | 24 | 0.872 [0.82–0.92] | 5/24 (20.8%) | 0/24 | – | +0.061 [+0.00 to +0.12] | better |
| Ambience#Space | 26 | 0.870 [0.83–0.90] | 3/26 (11.5%) | 0/26 | – | +0.064 [+0.00 to +0.12] | better |
| Food#Appearance | 16 | 0.858 [0.79–0.91] | 3/16 (18.8%) | 0/16 | – | +0.025 [-0.05 to +0.09] | too few |
| Food#Portion | 28 | 0.843 [0.80–0.89] | 3/28 (10.7%) | 0/28 | – | +0.003 [-0.06 to +0.06] | no measured difference |
| Food#Recommend | 12 | 0.861 [0.78–0.92] | 2/12 (16.7%) | 0/12 | – | +0.025 [-0.06 to +0.10] | too few |
| Food#Taste | 57 | 0.841 [0.81–0.87] | 9/57 (15.8%) | 0/57 | – | -0.005 [-0.15 to +0.11] | no measured difference |
| Location#Downtown | 16 | 0.845 [0.81–0.88] | 0/16 (0.0%) | 0/16 | – | +0.006 [-0.05 to +0.06] | too few |
| Location#Easy_to_find | 11 | 0.834 [0.78–0.88] | 0/11 (0.0%) | 0/11 | – | -0.009 [-0.08 to +0.05] | too few |
| Location#Transportation | 13 | 0.800 [0.76–0.84] | 0/13 (0.0%) | 0/13 | – | -0.054 [-0.11 to +0.00] | too few |
| Price#Cost_effective | 13 | 0.863 [0.83–0.91] | 2/13 (15.4%) | 0/13 | – | +0.030 [-0.02 to +0.09] | too few |
| Price#Discount | 16 | 0.805 [0.76–0.85] | 0/16 (0.0%) | 0/16 | – | -0.052 [-0.11 to +0.01] | too few |
| Price#Level | 34 | 0.851 [0.82–0.88] | 3/34 (8.8%) | 0/34 | – | +0.029 [-0.04 to +0.10] | no measured difference |
| Service#Hospitality | 35 | 0.839 [0.80–0.88] | 5/35 (14.3%) | 0/35 | – | -0.008 [-0.07 to +0.05] | no measured difference |
| Service#Parking | 7 | 0.889 [0.79–0.97] | 3/7 (42.9%) | 0/7 | – | +0.055 [-0.05 to +0.14] | too few |
| Service#Queue | 10 | 0.791 [0.68–0.88] | 2/10 (20.0%) | 0/10 | – | -0.062 [-0.18 to +0.04] | too few |
| Service#Timely | 13 | 0.862 [0.81–0.91] | 3/13 (23.1%) | 0/13 | – | +0.027 [-0.03 to +0.09] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases

**asap / dev / agent-cases: 60 items, 18 labels.** Micro F1 0.827 [0.79–0.86], macro F1 0.780 [0.73–0.82], exact match 11/60 (18.3%) [11–30].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 58 | 57 | 1 | 0 | 98.3% [91–100] | 100.0% [94–100] | 0.991 [0.97–1.00] |
| Food#Appearance | 16 | 14 | 11 | 3 | 5 | 78.6% [52–92] | 68.8% [44–86] | 0.733 [0.52–0.89] |
| Food#Portion | 28 | 23 | 20 | 3 | 8 | 87.0% [68–95] | 71.4% [53–85] | 0.784 [0.63–0.89] |
| Food#Recommend | 12 | 16 | 11 | 5 | 1 | 68.8% [44–86] | 91.7% [65–99] | 0.786 [0.57–0.93] |
| Price#Level | 34 | 20 | 20 | 0 | 14 | 100.0% [84–100] | 58.8% [42–74] | 0.741 [0.60–0.86] |
| Price#Cost_effective | 13 | 16 | 12 | 4 | 1 | 75.0% [51–90] | 92.3% [67–99] | 0.828 [0.64–0.96] |
| Price#Discount | 16 | 11 | 8 | 3 | 8 | 72.7% [43–90] | 50.0% [28–72] | 0.593 [0.33–0.79] |
| Location#Downtown | 16 | 4 | 4 | 0 | 12 | 100.0% [51–100] | 25.0% [10–49] | 0.400 [0.12–0.64] |
| Location#Transportation | 13 | 8 | 8 | 0 | 5 | 100.0% [68–100] | 61.5% [36–82] | 0.762 [0.47–0.94] |
| Location#Easy_to_find | 11 | 10 | 8 | 2 | 3 | 80.0% [49–94] | 72.7% [43–90] | 0.762 [0.50–0.94] |
| Service#Queue | 10 | 12 | 7 | 5 | 3 | 58.3% [32–81] | 70.0% [40–89] | 0.636 [0.33–0.85] |
| Service#Hospitality | 35 | 31 | 31 | 0 | 4 | 100.0% [89–100] | 88.6% [74–95] | 0.939 [0.87–0.99] |
| Service#Parking | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| Service#Timely | 13 | 19 | 13 | 6 | 0 | 68.4% [46–85] | 100.0% [77–100] | 0.812 [0.64–0.94] |
| Ambience#Decoration | 28 | 26 | 24 | 2 | 4 | 92.3% [76–98] | 85.7% [69–94] | 0.889 [0.79–0.97] |
| Ambience#Noise | 23 | 18 | 18 | 0 | 5 | 100.0% [82–100] | 78.3% [58–90] | 0.878 [0.74–0.97] |
| Ambience#Space | 26 | 25 | 21 | 4 | 5 | 84.0% [65–94] | 80.8% [62–91] | 0.824 [0.69–0.92] |
| Ambience#Sanitary | 24 | 23 | 20 | 3 | 4 | 87.0% [68–95] | 83.3% [64–93] | 0.851 [0.72–0.95] |
| **micro** | 382 | 339 | 298 | 41 | 84 | 87.9% | 78.0% | 0.827 [0.79–0.86] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 2.20 calls and 0.00 tool calls per item; rule gate 60, quote repair 12, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 339/339; cost $0.0578 ($0.964 per 1,000 items).

Confusion: exact 11, under-labelled 24, over-labelled 5, swapped 20.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Location#Downtown | (no predicted label) | 7 | missed |
| Price#Level | (no predicted label) | 7 | missed |
| Food#Portion | (no predicted label) | 6 | missed |
| Location#Transportation | (no predicted label) | 5 | missed |
| Price#Discount | (no predicted label) | 5 | missed |
| Ambience#Sanitary | (no predicted label) | 3 | missed |
| Ambience#Space | (no predicted label) | 3 | missed |
| Food#Appearance | (no predicted label) | 3 | missed |
| Location#Downtown | Service#Queue | 3 | confused |
| Location#Easy_to_find | (no predicted label) | 3 | missed |

**Slices of 60 items.** Overall micro F1 0.827, exact match 18.3%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.818 [0.78–0.86] | 7/45 (15.6%) | 0/45 | – | -0.038 [-0.11 to +0.05] | no measured difference |
| 1-3 stars | 15 | 0.855 [0.78–0.91] | 4/15 (26.7%) | 0/15 | – | +0.038 [-0.04 to +0.11] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.813 [0.76–0.87] | 4/22 (18.2%) | 0/22 | – | -0.021 [-0.08 to +0.05] | no measured difference |
| 8+ labels | 23 | 0.848 [0.80–0.89] | 1/23 (4.3%) | 0/23 | – | +0.047 [-0.02 to +0.11] | no measured difference |
| 1-4 labels | 15 | 0.767 [0.65–0.89] | 6/15 (40.0%) | 0/15 | – | -0.067 [-0.19 to +0.06] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.820 [0.78–0.85] | 7/50 (14.0%) | 0/50 | – | -0.045 [-0.15 to +0.07] | no measured difference |
| no neutral mention | 10 | 0.865 [0.75–0.95] | 4/10 (40.0%) | 0/10 | – | +0.045 [-0.07 to +0.14] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.832 [0.75–0.90] | 5/20 (25.0%) | 0/20 | – | +0.007 [-0.09 to +0.09] | no measured difference |
| 241–332 chars | 20 | 0.800 [0.75–0.85] | 3/20 (15.0%) | 0/20 | – | -0.041 [-0.10 to +0.03] | no measured difference |
| 333–579 chars | 20 | 0.848 [0.80–0.89] | 3/20 (15.0%) | 0/20 | – | +0.034 [-0.03 to +0.10] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.831 [0.78–0.88] | 4/28 (14.3%) | 0/28 | – | +0.011 [-0.06 to +0.08] | no measured difference |
| Ambience#Noise | 23 | 0.822 [0.76–0.88] | 3/23 (13.0%) | 0/23 | – | -0.009 [-0.07 to +0.06] | no measured difference |
| Ambience#Sanitary | 24 | 0.863 [0.82–0.91] | 4/24 (16.7%) | 0/24 | – | +0.072 [+0.01 to +0.13] | better |
| Ambience#Space | 26 | 0.854 [0.81–0.89] | 2/26 (7.7%) | 0/26 | – | +0.060 [-0.01 to +0.12] | no measured difference |
| Food#Appearance | 16 | 0.851 [0.78–0.91] | 3/16 (18.8%) | 0/16 | – | +0.035 [-0.04 to +0.10] | too few |
| Food#Portion | 28 | 0.834 [0.79–0.87] | 3/28 (10.7%) | 0/28 | – | +0.017 [-0.05 to +0.09] | no measured difference |
| Food#Recommend | 12 | 0.846 [0.75–0.92] | 2/12 (16.7%) | 0/12 | – | +0.025 [-0.08 to +0.11] | too few |
| Food#Taste | 57 | 0.829 [0.79–0.86] | 10/57 (17.5%) | 0/57 | – | +0.079 [-0.15 to +0.22] | no measured difference |
| Location#Downtown | 16 | 0.820 [0.77–0.86] | 0/16 (0.0%) | 0/16 | – | -0.010 [-0.08 to +0.05] | too few |
| Location#Easy_to_find | 11 | 0.829 [0.78–0.87] | 0/11 (0.0%) | 0/11 | – | +0.003 [-0.06 to +0.07] | too few |
| Location#Transportation | 13 | 0.785 [0.75–0.82] | 0/13 (0.0%) | 0/13 | – | -0.053 [-0.10 to +0.00] | too few |
| Price#Cost_effective | 13 | 0.835 [0.78–0.89] | 2/13 (15.4%) | 0/13 | – | +0.012 [-0.05 to +0.08] | too few |
| Price#Discount | 16 | 0.805 [0.76–0.85] | 0/16 (0.0%) | 0/16 | – | -0.031 [-0.09 to +0.03] | too few |
| Price#Level | 34 | 0.830 [0.79–0.87] | 3/34 (8.8%) | 0/34 | – | +0.009 [-0.06 to +0.08] | no measured difference |
| Service#Hospitality | 35 | 0.831 [0.79–0.87] | 5/35 (14.3%) | 0/35 | – | +0.014 [-0.05 to +0.08] | no measured difference |
| Service#Parking | 7 | 0.845 [0.75–0.94] | 2/7 (28.6%) | 0/7 | – | +0.022 [-0.08 to +0.12] | too few |
| Service#Queue | 10 | 0.818 [0.73–0.89] | 2/10 (20.0%) | 0/10 | – | -0.010 [-0.11 to +0.07] | too few |
| Service#Timely | 13 | 0.872 [0.83–0.92] | 4/13 (30.8%) | 0/13 | – | +0.060 [+0.00 to +0.13] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases-check

**asap / dev / agent-cases-check: 60 items, 18 labels.** Micro F1 0.844 [0.81–0.87], macro F1 0.795 [0.75–0.83], exact match 10/60 (16.7%) [9–28].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 58 | 57 | 1 | 0 | 98.3% [91–100] | 100.0% [94–100] | 0.991 [0.97–1.00] |
| Food#Appearance | 16 | 12 | 10 | 2 | 6 | 83.3% [55–95] | 62.5% [39–82] | 0.714 [0.50–0.88] |
| Food#Portion | 28 | 24 | 19 | 5 | 9 | 79.2% [60–91] | 67.9% [49–82] | 0.731 [0.57–0.85] |
| Food#Recommend | 12 | 12 | 10 | 2 | 2 | 83.3% [55–95] | 83.3% [55–95] | 0.833 [0.62–0.97] |
| Price#Level | 34 | 25 | 24 | 1 | 10 | 96.0% [80–99] | 70.6% [54–83] | 0.814 [0.69–0.91] |
| Price#Cost_effective | 13 | 14 | 11 | 3 | 2 | 78.6% [52–92] | 84.6% [58–96] | 0.815 [0.61–0.96] |
| Price#Discount | 16 | 12 | 9 | 3 | 7 | 75.0% [47–91] | 56.2% [33–77] | 0.643 [0.38–0.82] |
| Location#Downtown | 16 | 4 | 3 | 1 | 13 | 75.0% [30–95] | 18.8% [7–43] | 0.300 [0.00–0.56] |
| Location#Transportation | 13 | 8 | 8 | 0 | 5 | 100.0% [68–100] | 61.5% [36–82] | 0.762 [0.47–0.94] |
| Location#Easy_to_find | 11 | 10 | 10 | 0 | 1 | 100.0% [72–100] | 90.9% [62–98] | 0.952 [0.82–1.00] |
| Service#Queue | 10 | 12 | 7 | 5 | 3 | 58.3% [32–81] | 70.0% [40–89] | 0.636 [0.33–0.85] |
| Service#Hospitality | 35 | 32 | 32 | 0 | 3 | 100.0% [89–100] | 91.4% [78–97] | 0.955 [0.90–1.00] |
| Service#Parking | 7 | 4 | 4 | 0 | 3 | 100.0% [51–100] | 57.1% [25–84] | 0.727 [0.33–1.00] |
| Service#Timely | 13 | 18 | 13 | 5 | 0 | 72.2% [49–88] | 100.0% [77–100] | 0.839 [0.67–0.96] |
| Ambience#Decoration | 28 | 24 | 23 | 1 | 5 | 95.8% [80–99] | 82.1% [64–92] | 0.885 [0.77–0.96] |
| Ambience#Noise | 23 | 20 | 20 | 0 | 3 | 100.0% [84–100] | 87.0% [68–95] | 0.930 [0.84–1.00] |
| Ambience#Space | 26 | 27 | 23 | 4 | 3 | 85.2% [68–94] | 88.5% [71–96] | 0.868 [0.75–0.95] |
| Ambience#Sanitary | 24 | 22 | 21 | 1 | 3 | 95.5% [78–99] | 87.5% [69–96] | 0.913 [0.80–0.98] |
| **micro** | 382 | 338 | 304 | 34 | 78 | 89.9% | 79.6% | 0.844 [0.81–0.87] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 3.45 calls and 0.32 tool calls per item; rule gate 60, quote repair 10, self-check changed 21 of 60 items (+13 / −16 labels); exact quotes 338/338; cost $0.0979 ($1.632 per 1,000 items). Items on which each tool was called: get_label_rules 28%.

Confusion: exact 10, under-labelled 27, over-labelled 9, swapped 14.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Location#Downtown | (no predicted label) | 10 | missed |
| Price#Level | (no predicted label) | 8 | missed |
| Food#Portion | (no predicted label) | 7 | missed |
| Location#Transportation | (no predicted label) | 5 | missed |
| Food#Appearance | (no predicted label) | 4 | missed |
| Price#Discount | (no predicted label) | 4 | missed |
| Ambience#Decoration | (no predicted label) | 3 | missed |
| Ambience#Sanitary | (no predicted label) | 3 | missed |
| Food#Taste | Ambience#Space | 3 | confused |
| Food#Taste | Service#Timely | 3 | confused |

**Slices of 60 items.** Overall micro F1 0.844, exact match 16.7%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.833 [0.80–0.86] | 5/45 (11.1%) | 0/45 | – | -0.050 [-0.11 to +0.01] | no measured difference |
| 1-3 stars | 15 | 0.882 [0.82–0.93] | 5/15 (33.3%) | 0/15 | – | +0.050 [-0.01 to +0.11] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.841 [0.79–0.89] | 4/22 (18.2%) | 0/22 | – | -0.005 [-0.06 to +0.06] | no measured difference |
| 8+ labels | 23 | 0.860 [0.82–0.89] | 1/23 (4.3%) | 0/23 | – | +0.034 [-0.02 to +0.08] | no measured difference |
| 1-4 labels | 15 | 0.787 [0.71–0.86] | 5/15 (33.3%) | 0/15 | – | -0.066 [-0.14 to +0.02] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.834 [0.80–0.86] | 7/50 (14.0%) | 0/50 | – | -0.072 [-0.13 to -0.02] | worse |
| no neutral mention | 10 | 0.906 [0.86–0.95] | 3/10 (30.0%) | 0/10 | – | +0.072 [+0.02 to +0.13] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.842 [0.78–0.89] | 3/20 (15.0%) | 0/20 | – | -0.003 [-0.07 to +0.06] | no measured difference |
| 241–332 chars | 20 | 0.838 [0.80–0.88] | 3/20 (15.0%) | 0/20 | – | -0.010 [-0.06 to +0.05] | no measured difference |
| 333–579 chars | 20 | 0.853 [0.79–0.90] | 4/20 (20.0%) | 0/20 | – | +0.013 [-0.05 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.861 [0.82–0.90] | 4/28 (14.3%) | 0/28 | – | +0.039 [-0.02 to +0.09] | no measured difference |
| Ambience#Noise | 23 | 0.857 [0.82–0.89] | 2/23 (8.7%) | 0/23 | – | +0.026 [-0.03 to +0.08] | no measured difference |
| Ambience#Sanitary | 24 | 0.867 [0.83–0.90] | 3/24 (12.5%) | 0/24 | – | +0.046 [-0.01 to +0.10] | no measured difference |
| Ambience#Space | 26 | 0.864 [0.83–0.90] | 2/26 (7.7%) | 0/26 | – | +0.044 [-0.02 to +0.09] | no measured difference |
| Food#Appearance | 16 | 0.867 [0.81–0.91] | 3/16 (18.8%) | 0/16 | – | +0.033 [-0.03 to +0.10] | too few |
| Food#Portion | 28 | 0.846 [0.81–0.88] | 3/28 (10.7%) | 0/28 | – | +0.004 [-0.05 to +0.06] | no measured difference |
| Food#Recommend | 12 | 0.841 [0.78–0.90] | 1/12 (8.3%) | 0/12 | – | -0.005 [-0.08 to +0.06] | too few |
| Food#Taste | 57 | 0.846 [0.82–0.87] | 9/57 (15.8%) | 0/57 | – | +0.046 [-0.14 to +0.24] | no measured difference |
| Location#Downtown | 16 | 0.837 [0.79–0.87] | 0/16 (0.0%) | 0/16 | – | -0.012 [-0.07 to +0.04] | too few |
| Location#Easy_to_find | 11 | 0.832 [0.77–0.89] | 1/11 (9.1%) | 0/11 | – | -0.016 [-0.08 to +0.05] | too few |
| Location#Transportation | 13 | 0.792 [0.75–0.83] | 0/13 (0.0%) | 0/13 | – | -0.067 [-0.12 to -0.02] | too few |
| Price#Cost_effective | 13 | 0.848 [0.80–0.89] | 1/13 (7.7%) | 0/13 | – | +0.005 [-0.06 to +0.06] | too few |
| Price#Discount | 16 | 0.816 [0.77–0.86] | 0/16 (0.0%) | 0/16 | – | -0.041 [-0.10 to +0.01] | too few |
| Price#Level | 34 | 0.857 [0.82–0.89] | 3/34 (8.8%) | 0/34 | – | +0.034 [-0.03 to +0.09] | no measured difference |
| Service#Hospitality | 35 | 0.849 [0.81–0.89] | 5/35 (14.3%) | 0/35 | – | +0.015 [-0.04 to +0.08] | no measured difference |
| Service#Parking | 7 | 0.875 [0.78–0.95] | 2/7 (28.6%) | 0/7 | – | +0.035 [-0.06 to +0.12] | too few |
| Service#Queue | 10 | 0.818 [0.73–0.89] | 2/10 (20.0%) | 0/10 | – | -0.032 [-0.12 to +0.04] | too few |
| Service#Timely | 13 | 0.888 [0.84–0.94] | 4/13 (30.8%) | 0/13 | – | +0.057 [+0.00 to +0.12] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases-check-medium

**asap / dev / agent-cases-check-medium: 60 items, 18 labels.** Micro F1 0.863 [0.83–0.89], macro F1 0.823 [0.78–0.86], exact match 12/60 (20.0%) [12–32].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 58 | 57 | 1 | 0 | 98.3% [91–100] | 100.0% [94–100] | 0.991 [0.97–1.00] |
| Food#Appearance | 16 | 14 | 12 | 2 | 4 | 85.7% [60–96] | 75.0% [51–90] | 0.800 [0.62–0.94] |
| Food#Portion | 28 | 23 | 19 | 4 | 9 | 82.6% [63–93] | 67.9% [49–82] | 0.745 [0.59–0.86] |
| Food#Recommend | 12 | 15 | 11 | 4 | 1 | 73.3% [48–89] | 91.7% [65–99] | 0.815 [0.60–0.95] |
| Price#Level | 34 | 27 | 26 | 1 | 8 | 96.3% [82–99] | 76.5% [60–88] | 0.852 [0.75–0.94] |
| Price#Cost_effective | 13 | 16 | 13 | 3 | 0 | 81.2% [57–93] | 100.0% [77–100] | 0.897 [0.76–1.00] |
| Price#Discount | 16 | 13 | 9 | 4 | 7 | 69.2% [42–87] | 56.2% [33–77] | 0.621 [0.36–0.80] |
| Location#Downtown | 16 | 7 | 7 | 0 | 9 | 100.0% [65–100] | 43.8% [23–67] | 0.609 [0.33–0.82] |
| Location#Transportation | 13 | 8 | 8 | 0 | 5 | 100.0% [68–100] | 61.5% [36–82] | 0.762 [0.47–0.94] |
| Location#Easy_to_find | 11 | 11 | 10 | 1 | 1 | 90.9% [62–98] | 90.9% [62–98] | 0.909 [0.74–1.00] |
| Service#Queue | 10 | 10 | 5 | 5 | 5 | 50.0% [24–76] | 50.0% [24–76] | 0.500 [0.20–0.75] |
| Service#Hospitality | 35 | 33 | 31 | 2 | 4 | 93.9% [80–98] | 88.6% [74–95] | 0.912 [0.83–0.97] |
| Service#Parking | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| Service#Timely | 13 | 17 | 13 | 4 | 0 | 76.5% [53–90] | 100.0% [77–100] | 0.867 [0.71–0.97] |
| Ambience#Decoration | 28 | 27 | 26 | 1 | 2 | 96.3% [82–99] | 92.9% [77–98] | 0.945 [0.87–1.00] |
| Ambience#Noise | 23 | 21 | 21 | 0 | 2 | 100.0% [85–100] | 91.3% [73–98] | 0.955 [0.88–1.00] |
| Ambience#Space | 26 | 27 | 23 | 4 | 3 | 85.2% [68–94] | 88.5% [71–96] | 0.868 [0.75–0.95] |
| Ambience#Sanitary | 24 | 23 | 22 | 1 | 2 | 95.7% [79–99] | 91.7% [74–98] | 0.936 [0.84–1.00] |
| **micro** | 382 | 355 | 318 | 37 | 64 | 89.6% | 83.2% | 0.863 [0.83–0.89] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 3.83 calls and 0.72 tool calls per item; rule gate 57, quote repair 10, self-check changed 21 of 60 items (+18 / −9 labels); exact quotes 355/355; cost $0.1131 ($1.885 per 1,000 items). Items on which each tool was called: get_label_rules 63%.

Confusion: exact 12, under-labelled 22, over-labelled 11, swapped 15.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Portion | (no predicted label) | 7 | missed |
| Price#Level | (no predicted label) | 5 | missed |
| Location#Transportation | (no predicted label) | 4 | missed |
| Price#Discount | (no predicted label) | 4 | missed |
| Service#Queue | (no predicted label) | 4 | missed |
| Food#Appearance | (no predicted label) | 3 | missed |
| Food#Taste | Service#Timely | 3 | confused |
| Location#Downtown | (no predicted label) | 3 | missed |
| Location#Downtown | Service#Queue | 3 | confused |
| Ambience#Noise | Food#Portion | 2 | confused |

**Slices of 60 items.** Overall micro F1 0.863, exact match 20.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.854 [0.82–0.89] | 8/45 (17.8%) | 0/45 | – | -0.036 [-0.09 to +0.03] | no measured difference |
| 1-3 stars | 15 | 0.890 [0.83–0.93] | 4/15 (26.7%) | 0/15 | – | +0.036 [-0.03 to +0.09] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.849 [0.80–0.90] | 5/22 (22.7%) | 0/22 | – | -0.021 [-0.08 to +0.04] | no measured difference |
| 8+ labels | 23 | 0.892 [0.86–0.92] | 4/23 (17.4%) | 0/23 | – | +0.064 [+0.01 to +0.12] | better |
| 1-4 labels | 15 | 0.774 [0.69–0.86] | 3/15 (20.0%) | 0/15 | – | -0.102 [-0.19 to -0.02] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.858 [0.83–0.88] | 8/50 (16.0%) | 0/50 | – | -0.038 [-0.12 to +0.05] | no measured difference |
| no neutral mention | 10 | 0.895 [0.81–0.97] | 4/10 (40.0%) | 0/10 | – | +0.038 [-0.05 to +0.11] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.873 [0.82–0.92] | 5/20 (25.0%) | 0/20 | – | +0.014 [-0.05 to +0.08] | no measured difference |
| 241–332 chars | 20 | 0.835 [0.78–0.88] | 4/20 (20.0%) | 0/20 | – | -0.043 [-0.10 to +0.02] | no measured difference |
| 333–579 chars | 20 | 0.881 [0.84–0.92] | 3/20 (15.0%) | 0/20 | – | +0.029 [-0.02 to +0.08] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.880 [0.84–0.91] | 6/28 (21.4%) | 0/28 | – | +0.042 [-0.01 to +0.10] | no measured difference |
| Ambience#Noise | 23 | 0.878 [0.84–0.91] | 4/23 (17.4%) | 0/23 | – | +0.030 [-0.03 to +0.08] | no measured difference |
| Ambience#Sanitary | 24 | 0.898 [0.87–0.93] | 5/24 (20.8%) | 0/24 | – | +0.072 [+0.02 to +0.13] | better |
| Ambience#Space | 26 | 0.892 [0.86–0.92] | 5/26 (19.2%) | 0/26 | – | +0.064 [+0.01 to +0.12] | better |
| Food#Appearance | 16 | 0.892 [0.85–0.93] | 3/16 (18.8%) | 0/16 | – | +0.042 [-0.01 to +0.10] | too few |
| Food#Portion | 28 | 0.861 [0.82–0.90] | 6/28 (21.4%) | 0/28 | – | -0.003 [-0.06 to +0.05] | no measured difference |
| Food#Recommend | 12 | 0.881 [0.84–0.92] | 1/12 (8.3%) | 0/12 | – | +0.022 [-0.03 to +0.08] | too few |
| Food#Taste | 57 | 0.864 [0.84–0.89] | 11/57 (19.3%) | 0/57 | – | +0.017 [-0.12 to +0.13] | no measured difference |
| Location#Downtown | 16 | 0.863 [0.81–0.90] | 2/16 (12.5%) | 0/16 | – | -0.001 [-0.06 to +0.06] | too few |
| Location#Easy_to_find | 11 | 0.869 [0.81–0.92] | 1/11 (9.1%) | 0/11 | – | +0.008 [-0.06 to +0.07] | too few |
| Location#Transportation | 13 | 0.831 [0.79–0.87] | 0/13 (0.0%) | 0/13 | – | -0.041 [-0.10 to +0.01] | too few |
| Price#Cost_effective | 13 | 0.890 [0.85–0.93] | 3/13 (23.1%) | 0/13 | – | +0.037 [-0.01 to +0.09] | too few |
| Price#Discount | 16 | 0.833 [0.79–0.88] | 1/16 (6.2%) | 0/16 | – | -0.043 [-0.10 to +0.02] | too few |
| Price#Level | 34 | 0.876 [0.84–0.91] | 7/34 (20.6%) | 0/34 | – | +0.036 [-0.02 to +0.09] | no measured difference |
| Service#Hospitality | 35 | 0.874 [0.84–0.91] | 8/35 (22.9%) | 0/35 | – | +0.035 [-0.02 to +0.09] | no measured difference |
| Service#Parking | 7 | 0.898 [0.83–0.97] | 3/7 (42.9%) | 0/7 | – | +0.040 [-0.04 to +0.12] | too few |
| Service#Queue | 10 | 0.844 [0.77–0.90] | 0/10 (0.0%) | 0/10 | – | -0.023 [-0.11 to +0.04] | too few |
| Service#Timely | 13 | 0.912 [0.87–0.95] | 5/13 (38.5%) | 0/13 | – | +0.065 [+0.01 to +0.12] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases-synthetic

**asap / dev / agent-cases-synthetic: 60 items, 18 labels.** Micro F1 0.832 [0.80–0.86], macro F1 0.778 [0.73–0.81], exact match 10/60 (16.7%) [9–28].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 57 | 58 | 57 | 1 | 0 | 98.3% [91–100] | 100.0% [94–100] | 0.991 [0.97–1.00] |
| Food#Appearance | 16 | 15 | 11 | 4 | 5 | 73.3% [48–89] | 68.8% [44–86] | 0.710 [0.50–0.88] |
| Food#Portion | 28 | 24 | 20 | 4 | 8 | 83.3% [64–93] | 71.4% [53–85] | 0.769 [0.62–0.88] |
| Food#Recommend | 12 | 15 | 10 | 5 | 2 | 66.7% [42–85] | 83.3% [55–95] | 0.741 [0.50–0.90] |
| Price#Level | 34 | 21 | 21 | 0 | 13 | 100.0% [85–100] | 61.8% [45–76] | 0.764 [0.62–0.87] |
| Price#Cost_effective | 13 | 17 | 13 | 4 | 0 | 76.5% [53–90] | 100.0% [77–100] | 0.867 [0.72–0.97] |
| Price#Discount | 16 | 12 | 9 | 3 | 7 | 75.0% [47–91] | 56.2% [33–77] | 0.643 [0.38–0.82] |
| Location#Downtown | 16 | 5 | 4 | 1 | 12 | 80.0% [38–96] | 25.0% [10–49] | 0.381 [0.11–0.62] |
| Location#Transportation | 13 | 9 | 9 | 0 | 4 | 100.0% [70–100] | 69.2% [42–87] | 0.818 [0.57–0.96] |
| Location#Easy_to_find | 11 | 8 | 7 | 1 | 4 | 87.5% [53–98] | 63.6% [35–85] | 0.737 [0.44–0.93] |
| Service#Queue | 10 | 10 | 5 | 5 | 5 | 50.0% [24–76] | 50.0% [24–76] | 0.500 [0.18–0.75] |
| Service#Hospitality | 35 | 33 | 32 | 1 | 3 | 97.0% [85–99] | 91.4% [78–97] | 0.941 [0.88–0.99] |
| Service#Parking | 7 | 4 | 4 | 0 | 3 | 100.0% [51–100] | 57.1% [25–84] | 0.727 [0.33–1.00] |
| Service#Timely | 13 | 17 | 13 | 4 | 0 | 76.5% [53–90] | 100.0% [77–100] | 0.867 [0.70–0.97] |
| Ambience#Decoration | 28 | 26 | 24 | 2 | 4 | 92.3% [76–98] | 85.7% [69–94] | 0.889 [0.78–0.96] |
| Ambience#Noise | 23 | 19 | 19 | 0 | 4 | 100.0% [83–100] | 82.6% [63–93] | 0.905 [0.79–0.98] |
| Ambience#Space | 26 | 30 | 24 | 6 | 2 | 80.0% [63–90] | 92.3% [76–98] | 0.857 [0.74–0.94] |
| Ambience#Sanitary | 24 | 23 | 21 | 2 | 3 | 91.3% [73–98] | 87.5% [69–96] | 0.894 [0.78–0.97] |
| **micro** | 382 | 346 | 303 | 43 | 79 | 87.6% | 79.3% | 0.832 [0.80–0.86] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 60/60 answered; 2.15 calls and 0.02 tool calls per item; rule gate 60, quote repair 8, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 346/346; cost $0.0556 ($0.926 per 1,000 items). Items on which each tool was called: get_label_rules 2%.

Confusion: exact 10, under-labelled 21, over-labelled 8, swapped 21.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Location#Downtown | (no predicted label) | 8 | missed |
| Price#Level | (no predicted label) | 7 | missed |
| Food#Portion | (no predicted label) | 4 | missed |
| Ambience#Noise | Service#Timely | 3 | confused |
| Food#Appearance | (no predicted label) | 3 | missed |
| Location#Downtown | Service#Queue | 3 | confused |
| Location#Easy_to_find | (no predicted label) | 3 | missed |
| Location#Transportation | (no predicted label) | 3 | missed |
| Price#Discount | (no predicted label) | 3 | missed |
| Service#Hospitality | Service#Timely | 3 | confused |

**Slices of 60 items.** Overall micro F1 0.832, exact match 16.7%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 4-5 stars | 45 | 0.831 [0.80–0.86] | 6/45 (13.3%) | 0/45 | – | -0.006 [-0.07 to +0.06] | no measured difference |
| 1-3 stars | 15 | 0.837 [0.77–0.90] | 4/15 (26.7%) | 0/15 | – | +0.006 [-0.07 to +0.08] | too few |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 5-7 labels | 22 | 0.833 [0.79–0.88] | 3/22 (13.6%) | 0/22 | – | +0.000 [-0.06 to +0.06] | no measured difference |
| 8+ labels | 23 | 0.844 [0.80–0.88] | 1/23 (4.3%) | 0/23 | – | +0.025 [-0.03 to +0.08] | no measured difference |
| 1-4 labels | 15 | 0.783 [0.68–0.89] | 6/15 (40.0%) | 0/15 | – | -0.057 [-0.15 to +0.04] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 50 | 0.821 [0.79–0.85] | 6/50 (12.0%) | 0/50 | – | -0.083 [-0.15 to -0.02] | worse |
| no neutral mention | 10 | 0.904 [0.84–0.96] | 4/10 (40.0%) | 0/10 | – | +0.083 [+0.01 to +0.15] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 112–240 chars | 20 | 0.844 [0.78–0.90] | 3/20 (15.0%) | 0/20 | – | +0.016 [-0.06 to +0.08] | no measured difference |
| 241–332 chars | 20 | 0.810 [0.76–0.86] | 2/20 (10.0%) | 0/20 | – | -0.035 [-0.10 to +0.03] | no measured difference |
| 333–579 chars | 20 | 0.845 [0.79–0.89] | 5/20 (25.0%) | 0/20 | – | +0.020 [-0.04 to +0.08] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 28 | 0.848 [0.81–0.89] | 4/28 (14.3%) | 0/28 | – | +0.039 [-0.02 to +0.10] | no measured difference |
| Ambience#Noise | 23 | 0.846 [0.80–0.89] | 2/23 (8.7%) | 0/23 | – | +0.027 [-0.03 to +0.09] | no measured difference |
| Ambience#Sanitary | 24 | 0.866 [0.82–0.90] | 4/24 (16.7%) | 0/24 | – | +0.067 [+0.01 to +0.12] | better |
| Ambience#Space | 26 | 0.863 [0.83–0.90] | 2/26 (7.7%) | 0/26 | – | +0.068 [+0.01 to +0.12] | better |
| Food#Appearance | 16 | 0.865 [0.81–0.92] | 4/16 (25.0%) | 0/16 | – | +0.047 [-0.01 to +0.11] | too few |
| Food#Portion | 28 | 0.819 [0.78–0.86] | 2/28 (7.1%) | 0/28 | – | -0.029 [-0.09 to +0.03] | no measured difference |
| Food#Recommend | 12 | 0.830 [0.76–0.89] | 2/12 (16.7%) | 0/12 | – | -0.003 [-0.08 to +0.07] | too few |
| Food#Taste | 57 | 0.832 [0.80–0.86] | 9/57 (15.8%) | 0/57 | – | -0.014 [-0.15 to +0.10] | no measured difference |
| Location#Downtown | 16 | 0.831 [0.79–0.87] | 0/16 (0.0%) | 0/16 | – | -0.002 [-0.06 to +0.05] | too few |
| Location#Easy_to_find | 11 | 0.792 [0.72–0.86] | 1/11 (9.1%) | 0/11 | – | -0.051 [-0.13 to +0.02] | too few |
| Location#Transportation | 13 | 0.800 [0.75–0.85] | 1/13 (7.7%) | 0/13 | – | -0.042 [-0.10 to +0.02] | too few |
| Price#Cost_effective | 13 | 0.839 [0.79–0.88] | 1/13 (7.7%) | 0/13 | – | +0.009 [-0.05 to +0.07] | too few |
| Price#Discount | 16 | 0.793 [0.74–0.84] | 0/16 (0.0%) | 0/16 | – | -0.057 [-0.12 to +0.00] | too few |
| Price#Level | 34 | 0.843 [0.81–0.87] | 2/34 (5.9%) | 0/34 | – | +0.029 [-0.04 to +0.09] | no measured difference |
| Service#Hospitality | 35 | 0.839 [0.80–0.88] | 6/35 (17.1%) | 0/35 | – | +0.021 [-0.04 to +0.08] | no measured difference |
| Service#Parking | 7 | 0.842 [0.75–0.93] | 2/7 (28.6%) | 0/7 | – | +0.011 [-0.09 to +0.11] | too few |
| Service#Queue | 10 | 0.779 [0.70–0.84] | 1/10 (10.0%) | 0/10 | – | -0.066 [-0.15 to +0.01] | too few |
| Service#Timely | 13 | 0.856 [0.80–0.91] | 3/13 (23.1%) | 0/13 | – | +0.031 [-0.03 to +0.09] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


