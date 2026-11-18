# Analysis: dev1

## ad_policy / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 86 | 0.816 [0.74–0.88] | 0.871 [0.78–0.92] | 67/86 | 4/45 | 6/41 | 1.00 | 0.00 | 0.09 | 0 |
| prompt-rules | 86 | 0.905 [0.83–0.96] | 0.925 [0.84–0.97] | 78/86 | 4/45 | 2/41 | 1.00 | 0.00 | 0.11 | 0 |
| agent | 86 | 0.887 [0.81–0.95] | 0.892 [0.79–0.95] | 76/86 | 4/45 | 5/41 | 1.83 | 0.70 | 0.24 | 0 |
| agent-cases | 86 | 0.926 [0.87–0.97] | 0.937 [0.87–0.98] | 79/86 | 3/45 | 3/41 | 1.73 | 0.41 | 0.24 | 0 |
| agent-cases-check | 86 | 0.915 [0.85–0.97] | 0.925 [0.83–0.97] | 79/86 | 4/45 | 3/41 | 2.85 | 0.52 | 0.46 | 0 |

## asap / dev

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 40 | 0.728 [0.68–0.77] | 0.694 [0.62–0.74] | 1/40 | – | – | 1.00 | 0.00 | 0.21 | 0 |
| prompt-rules | 40 | 0.789 [0.75–0.83] | 0.762 [0.69–0.81] | 3/40 | – | – | 1.00 | 0.00 | 0.27 | 0 |
| agent | 40 | 0.831 [0.79–0.87] | 0.809 [0.74–0.85] | 7/40 | – | – | 2.25 | 0.93 | 0.67 | 0 |
| agent-cases | 40 | 0.823 [0.78–0.87] | 0.790 [0.72–0.84] | 8/40 | – | – | 2.33 | 0.00 | 0.92 | 0 |
| agent-cases-check | 40 | 0.824 [0.79–0.86] | 0.799 [0.73–0.84] | 8/40 | – | – | 3.50 | 0.35 | 1.42 | 0 |


# Details per arm

## ad_policy / dev / prompt-short

**ad_policy / dev / prompt-short: 86 items, 9 labels.** Micro F1 0.816 [0.74–0.88], macro F1 0.871 [0.78–0.92], exact match 67/86 (77.9%) [68–85].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 19 | 10 | 9 | 2 | 52.6% [32–73] | 83.3% [55–95] | 0.645 [0.42–0.83] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 4 | 1 | 4 | 80.0% [38–96] | 50.0% [22–78] | 0.615 [0.20–0.89] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 7 | 5 | 2 | 0 | 71.4% [36–92] | 100.0% [57–100] | 0.833 [0.50–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| **micro** | 48 | 55 | 42 | 13 | 6 | 76.4% | 87.5% | 0.816 [0.74–0.88] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 6/41 (14.6%) [7–28].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 86/86 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 54/55; cost $0.0073 ($0.085 per 1,000 items).

Confusion: exact 67, under-labelled 6, over-labelled 13, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| GUARANTEE | ABSOLUTE | 6 | confused |
| DISPARAGE | (no predicted label) | 4 | missed |
| (no gold label) | ABSOLUTE | 2 | added to an unlabelled item |
| (no gold label) | ALCOHOL | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | BEFORE_AFTER | 1 | added to an unlabelled item |
| (no gold label) | DISPARAGE | 1 | added to an unlabelled item |
| DISPARAGE | ABSOLUTE | 1 | confused |

**Slices of 86 items.** Overall micro F1 0.816, exact match 77.9%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.754 [0.65–0.85] | 32/47 (68.1%) | 3/25 | 4/22 | -0.151 [-0.28 to -0.02] | worse |
| en | 39 | 0.905 [0.80–0.98] | 35/39 (89.7%) | 1/20 | 2/19 | +0.151 [+0.02 to +0.28] | better |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 0.857 [0.76–0.96] | 19/24 (79.2%) | 0/15 | 2/9 | +0.063 [-0.08 to +0.21] | no measured difference |
| video-words | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.192 [+0.12 to +0.26] | too few |
| synthetic | 60 | 0.781 [0.68–0.87] | 46/60 (76.7%) | 4/28 | 4/32 | -0.091 [-0.23 to +0.05] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.866 [0.81–0.93] | 32/45 (71.1%) | 4/45 | – | -0.143 [-0.30 to +0.04] (exact match) | no measured difference |
| look-alike | 27 | – | 22/27 (81.5%) | – | 5/27 | +0.052 [-0.13 to +0.23] (exact match) | no measured difference |
| plain | 14 | – | 13/14 (92.9%) | – | 1/14 | +0.179 [-0.01 to +0.32] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–54 chars | 28 | 0.848 [0.76–0.95] | 23/28 (82.1%) | 0/14 | 0/14 | +0.048 [-0.07 to +0.19] | no measured difference |
| 55–91 chars | 29 | 0.718 [0.53–0.86] | 18/29 (62.1%) | 3/16 | 5/13 | -0.157 [-0.35 to -0.00] | worse |
| 92–177 chars | 29 | 0.903 [0.77–1.00] | 26/29 (89.7%) | 1/15 | 1/14 | +0.125 [-0.02 to +0.26] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 41 | – | 35/41 (85.4%) | – | 6/41 | +0.143 [-0.02 to +0.30] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.77–1.00] | 9/12 (75.0%) | 1/12 | – | +0.099 [-0.04 to +0.23] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.204 [+0.13 to +0.28] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.196 [+0.12 to +0.28] | too few |
| DISPARAGE | 8 | 0.667 [0.40–0.84] | 2/8 (25.0%) | 3/8 | – | -0.180 [-0.47 to +0.01] | too few |
| GUARANTEE | 14 | 0.824 [0.74–0.90] | 8/14 (57.1%) | 0/14 | – | +0.012 [-0.10 to +0.16] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.200 [+0.13 to +0.27] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.192 [+0.12 to +0.27] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / prompt-rules

**ad_policy / dev / prompt-rules: 86 items, 9 labels.** Micro F1 0.905 [0.83–0.96], macro F1 0.925 [0.84–0.97], exact match 78/86 (90.7%) [83–95].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 13 | 10 | 3 | 2 | 76.9% [50–92] | 83.3% [55–95] | 0.800 [0.58–0.96] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 5 | 0 | 3 | 100.0% [57–100] | 62.5% [31–86] | 0.769 [0.36–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.57–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 47 | 43 | 4 | 5 | 91.5% | 89.6% | 0.905 [0.83–0.96] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 2/41 (4.9%) [1–16].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 86/86 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 47/47; cost $0.0092 ($0.107 per 1,000 items).

Confusion: exact 78, under-labelled 4, over-labelled 4, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DISPARAGE | (no predicted label) | 3 | missed |
| ABSOLUTE | (no predicted label) | 2 | missed |
| GUARANTEE | ABSOLUTE | 2 | confused |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |

**Slices of 86 items.** Overall micro F1 0.905, exact match 90.7%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.889 [0.76–0.97] | 42/47 (89.4%) | 3/25 | 0/22 | -0.038 [-0.17 to +0.10] | no measured difference |
| en | 39 | 0.927 [0.81–1.00] | 36/39 (92.3%) | 1/20 | 2/19 | +0.038 [-0.10 to +0.17] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.138 [+0.05 to +0.25] | better |
| video-words | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.099 [+0.04 to +0.18] | too few |
| synthetic | 60 | 0.852 [0.74–0.94] | 52/60 (86.7%) | 4/28 | 2/32 | -0.148 [-0.26 to -0.06] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.925 [0.86–0.98] | 39/45 (86.7%) | 4/45 | – | -0.085 [-0.20 to +0.03] (exact match) | no measured difference |
| look-alike | 27 | – | 26/27 (96.3%) | – | 1/27 | +0.082 [-0.03 to +0.19] (exact match) | no measured difference |
| plain | 14 | – | 13/14 (92.9%) | – | 1/14 | +0.026 [-0.14 to +0.15] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–54 chars | 28 | 0.966 [0.89–1.00] | 27/28 (96.4%) | 0/14 | 0/14 | +0.087 [-0.02 to +0.21] | no measured difference |
| 55–91 chars | 29 | 0.857 [0.70–0.97] | 25/29 (86.2%) | 3/16 | 0/13 | -0.076 [-0.24 to +0.07] | no measured difference |
| 92–177 chars | 29 | 0.903 [0.76–1.00] | 26/29 (89.7%) | 1/15 | 2/14 | -0.003 [-0.17 to +0.13] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 41 | – | 39/41 (95.1%) | – | 2/41 | +0.085 [-0.03 to +0.20] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.69–1.00] | 10/12 (83.3%) | 2/12 | – | -0.023 [-0.22 to +0.12] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.106 [+0.04 to +0.19] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.101 [+0.04 to +0.18] | too few |
| DISPARAGE | 8 | 0.778 [0.40–0.96] | 5/8 (62.5%) | 3/8 | – | -0.157 [-0.55 to +0.05] | too few |
| GUARANTEE | 14 | 0.933 [0.85–1.00] | 12/14 (85.7%) | 0/14 | – | +0.041 [-0.07 to +0.18] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.103 [+0.04 to +0.18] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.099 [+0.04 to +0.17] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent

**ad_policy / dev / agent: 86 items, 9 labels.** Micro F1 0.887 [0.81–0.95], macro F1 0.892 [0.79–0.95], exact match 76/86 (88.4%) [80–94].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 5 | 4 | 1 | 0 | 80.0% [38–96] | 100.0% [51–100] | 0.889 [0.50–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 5 | 0 | 3 | 100.0% [57–100] | 62.5% [31–86] | 0.769 [0.36–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 9 | 5 | 4 | 0 | 55.6% [27–81] | 100.0% [57–100] | 0.714 [0.33–0.94] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 49 | 43 | 6 | 5 | 87.8% | 89.6% | 0.887 [0.81–0.95] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 5/41 (12.2%) [5–26].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 86/86 answered; 1.83 calls and 0.70 tool calls per item; rule gate 12, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 49/49; cost $0.0206 ($0.240 per 1,000 items). Items on which each tool was called: get_label_rules 69%.

Confusion: exact 76, under-labelled 4, over-labelled 6, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ALCOHOL | 4 | added to an unlabelled item |
| DISPARAGE | (no predicted label) | 3 | missed |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |
| GUARANTEE | MEDICAL | 1 | confused |

**Slices of 86 items.** Overall micro F1 0.887, exact match 88.4%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.889 [0.76–0.97] | 42/47 (89.4%) | 3/25 | 2/22 | +0.005 [-0.16 to +0.15] | no measured difference |
| en | 39 | 0.884 [0.76–0.97] | 34/39 (87.2%) | 1/20 | 3/19 | -0.005 [-0.15 to +0.14] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.164 [+0.07 to +0.28] | better |
| video-words | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.118 [+0.05 to +0.20] | too few |
| synthetic | 60 | 0.825 [0.70–0.92] | 50/60 (83.3%) | 4/28 | 5/32 | -0.175 [-0.30 to -0.08] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.935 [0.87–0.98] | 40/45 (88.9%) | 4/45 | – | +0.011 [-0.13 to +0.15] (exact match) | no measured difference |
| look-alike | 27 | – | 23/27 (85.2%) | – | 4/27 | -0.046 [-0.21 to +0.10] (exact match) | no measured difference |
| plain | 14 | – | 13/14 (92.9%) | – | 1/14 | +0.054 [-0.13 to +0.19] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–54 chars | 28 | 0.966 [0.88–1.00] | 27/28 (96.4%) | 0/14 | 1/14 | +0.113 [-0.01 to +0.24] | no measured difference |
| 55–91 chars | 29 | 0.857 [0.69–0.97] | 25/29 (86.2%) | 3/16 | 1/13 | -0.046 [-0.22 to +0.10] | no measured difference |
| 92–177 chars | 29 | 0.848 [0.70–0.97] | 24/29 (82.8%) | 1/15 | 3/14 | -0.058 [-0.23 to +0.09] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 41 | – | 36/41 (87.8%) | – | 5/41 | -0.011 [-0.15 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.69–1.00] | 10/12 (83.3%) | 2/12 | – | +0.003 [-0.20 to +0.16] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.126 [+0.05 to +0.22] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.121 [+0.05 to +0.21] | too few |
| DISPARAGE | 8 | 0.778 [0.40–0.96] | 5/8 (62.5%) | 3/8 | – | -0.134 [-0.50 to +0.08] | too few |
| GUARANTEE | 14 | 0.966 [0.90–1.00] | 13/14 (92.9%) | 0/14 | – | +0.113 [-0.01 to +0.24] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.124 [+0.05 to +0.21] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.118 [+0.05 to +0.20] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases

**ad_policy / dev / agent-cases: 86 items, 9 labels.** Micro F1 0.926 [0.87–0.97], macro F1 0.937 [0.87–0.98], exact match 79/86 (91.9%) [84–96].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 6 | 6 | 0 | 2 | 100.0% [61–100] | 75.0% [41–93] | 0.857 [0.57–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 7 | 5 | 2 | 0 | 71.4% [36–92] | 100.0% [57–100] | 0.833 [0.50–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 47 | 44 | 3 | 4 | 93.6% | 91.7% | 0.926 [0.87–0.97] |

Miss rate (a labelled item predicted with no label): 3/45 (6.7%) [2–18]. False-alarm rate (an unlabelled item given a label): 3/41 (7.3%) [3–19].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 86/86 answered; 1.73 calls and 0.41 tool calls per item; rule gate 30, quote repair 2, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 47/47; cost $0.0207 ($0.240 per 1,000 items). Items on which each tool was called: get_label_rules 36%, search_cases 2%.

Confusion: exact 79, under-labelled 4, over-labelled 3, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ALCOHOL | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| DISPARAGE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |

**Slices of 86 items.** Overall micro F1 0.926, exact match 91.9%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.926 [0.84–0.98] | 43/47 (91.5%) | 2/25 | 1/22 | -0.001 [-0.11 to +0.12] | no measured difference |
| en | 39 | 0.927 [0.81–1.00] | 36/39 (92.3%) | 1/20 | 2/19 | +0.001 [-0.13 to +0.11] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.108 [+0.04 to +0.20] | better |
| video-words | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.077 [+0.03 to +0.14] | too few |
| synthetic | 60 | 0.885 [0.79–0.96] | 53/60 (88.3%) | 3/28 | 3/32 | -0.115 [-0.21 to -0.04] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.957 [0.91–0.99] | 41/45 (91.1%) | 3/45 | – | -0.016 [-0.13 to +0.10] (exact match) | no measured difference |
| look-alike | 27 | – | 25/27 (92.6%) | – | 2/27 | +0.011 [-0.11 to +0.13] (exact match) | no measured difference |
| plain | 14 | – | 13/14 (92.9%) | – | 1/14 | +0.012 [-0.16 to +0.12] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–54 chars | 28 | 1.000 [1.00–1.00] | 28/28 (100.0%) | 0/14 | 0/14 | +0.104 [+0.04 to +0.19] | better |
| 55–91 chars | 29 | 0.889 [0.76–0.98] | 25/29 (86.2%) | 2/16 | 1/13 | -0.060 [-0.20 to +0.05] | no measured difference |
| 92–177 chars | 29 | 0.903 [0.76–1.00] | 26/29 (89.7%) | 1/15 | 2/14 | -0.034 [-0.18 to +0.08] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 41 | – | 38/41 (92.7%) | – | 3/41 | +0.016 [-0.10 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.929 [0.82–1.00] | 10/12 (83.3%) | 1/12 | – | +0.003 [-0.12 to +0.11] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.082 [+0.03 to +0.15] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.079 [+0.03 to +0.14] | too few |
| DISPARAGE | 8 | 0.842 [0.62–0.97] | 5/8 (62.5%) | 2/8 | – | -0.105 [-0.36 to +0.05] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.104 [+0.03 to +0.19] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.080 [+0.03 to +0.14] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.077 [+0.02 to +0.14] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / dev / agent-cases-check

**ad_policy / dev / agent-cases-check: 86 items, 9 labels.** Micro F1 0.915 [0.85–0.97], macro F1 0.925 [0.83–0.97], exact match 79/86 (91.9%) [84–96].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| MEDICAL | 4 | 4 | 4 | 0 | 0 | 100.0% [51–100] | 100.0% [51–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 14 | 14 | 0 | 0 | 100.0% [78–100] | 100.0% [78–100] | 1.000 [1.00–1.00] |
| DISPARAGE | 8 | 5 | 5 | 0 | 3 | 100.0% [57–100] | 62.5% [31–86] | 0.769 [0.36–1.00] |
| DATA | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| ALCOHOL | 5 | 7 | 5 | 2 | 0 | 71.4% [36–92] | 100.0% [57–100] | 0.833 [0.50–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 2 | 2 | 2 | 0 | 0 | 100.0% [34–100] | 100.0% [34–100] | 1.000 |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 48 | 46 | 43 | 3 | 5 | 93.5% | 89.6% | 0.915 [0.85–0.97] |

Miss rate (a labelled item predicted with no label): 4/45 (8.9%) [4–21]. False-alarm rate (an unlabelled item given a label): 3/41 (7.3%) [3–19].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 86/86 answered; 2.85 calls and 0.52 tool calls per item; rule gate 29, quote repair 1, self-check changed 4 of 86 items (+0 / −4 labels); exact quotes 46/46; cost $0.0392 ($0.455 per 1,000 items). Items on which each tool was called: get_label_rules 49%, search_cases 2%.

Confusion: exact 79, under-labelled 4, over-labelled 3, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| DISPARAGE | (no predicted label) | 3 | missed |
| (no gold label) | ALCOHOL | 2 | added to an unlabelled item |
| ABSOLUTE | (no predicted label) | 2 | missed |
| (no gold label) | ABSOLUTE | 1 | added to an unlabelled item |

**Slices of 86 items.** Overall micro F1 0.915, exact match 91.9%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.906 [0.78–0.98] | 43/47 (91.5%) | 3/25 | 1/22 | -0.021 [-0.16 to +0.11] | no measured difference |
| en | 39 | 0.927 [0.81–1.00] | 36/39 (92.3%) | 1/20 | 2/19 | +0.021 [-0.12 to +0.16] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written | 24 | 1.000 [1.00–1.00] | 24/24 (100.0%) | 0/15 | 0/9 | +0.125 [+0.04 to +0.23] | better |
| video-words | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.089 [+0.03 to +0.16] | too few |
| synthetic | 60 | 0.867 [0.75–0.96] | 53/60 (88.3%) | 4/28 | 3/32 | -0.133 [-0.25 to -0.04] | worse |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 45 | 0.945 [0.88–0.99] | 41/45 (91.1%) | 4/45 | – | -0.016 [-0.13 to +0.10] (exact match) | no measured difference |
| look-alike | 27 | – | 25/27 (92.6%) | – | 2/27 | +0.011 [-0.11 to +0.13] (exact match) | no measured difference |
| plain | 14 | – | 13/14 (92.9%) | – | 1/14 | +0.012 [-0.16 to +0.12] (exact match) | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 23–54 chars | 28 | 1.000 [1.00–1.00] | 28/28 (100.0%) | 0/14 | 0/14 | +0.121 [+0.04 to +0.23] | better |
| 55–91 chars | 29 | 0.857 [0.69–0.97] | 25/29 (86.2%) | 3/16 | 1/13 | -0.092 [-0.26 to +0.05] | no measured difference |
| 92–177 chars | 29 | 0.903 [0.76–1.00] | 26/29 (89.7%) | 1/15 | 2/14 | -0.017 [-0.17 to +0.12] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 41 | – | 38/41 (92.7%) | – | 3/41 | +0.016 [-0.10 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 12 | 0.889 [0.69–1.00] | 10/12 (83.3%) | 2/12 | – | -0.036 [-0.25 to +0.10] | too few |
| ALCOHOL | 5 | 1.000 [1.00–1.00] | 5/5 (100.0%) | 0/5 | – | +0.095 [+0.03 to +0.18] | too few |
| DATA | 3 | 1.000 [1.00–1.00] | 3/3 (100.0%) | 0/3 | – | +0.091 [+0.03 to +0.17] | too few |
| DISPARAGE | 8 | 0.778 [0.40–0.96] | 5/8 (62.5%) | 3/8 | – | -0.170 [-0.55 to +0.05] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.121 [+0.04 to +0.22] | too few |
| MEDICAL | 4 | 1.000 [1.00–1.00] | 4/4 (100.0%) | 0/4 | – | +0.093 [+0.03 to +0.18] | too few |
| WEIGHT | 2 | 1.000 [1.00–1.00] | 2/2 (100.0%) | 0/2 | – | +0.089 [+0.03 to +0.16] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-short

**asap / dev / prompt-short: 40 items, 18 labels.** Micro F1 0.728 [0.68–0.77], macro F1 0.694 [0.62–0.74], exact match 1/40 (2.5%) [0–13].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 36 | 38 | 36 | 2 | 0 | 94.7% [83–99] | 100.0% [90–100] | 0.973 [0.93–1.00] |
| Food#Appearance | 12 | 13 | 8 | 5 | 4 | 61.5% [36–82] | 66.7% [39–86] | 0.640 [0.38–0.83] |
| Food#Portion | 14 | 21 | 13 | 8 | 1 | 61.9% [41–79] | 92.9% [69–99] | 0.743 [0.55–0.88] |
| Food#Recommend | 12 | 28 | 11 | 17 | 1 | 39.3% [24–58] | 91.7% [65–99] | 0.550 [0.35–0.72] |
| Price#Level | 22 | 12 | 12 | 0 | 10 | 100.0% [76–100] | 54.5% [35–73] | 0.706 [0.50–0.86] |
| Price#Cost_effective | 11 | 21 | 10 | 11 | 1 | 47.6% [28–68] | 90.9% [62–98] | 0.625 [0.39–0.80] |
| Price#Discount | 14 | 17 | 14 | 3 | 0 | 82.4% [59–94] | 100.0% [78–100] | 0.903 [0.76–1.00] |
| Location#Downtown | 7 | 7 | 3 | 4 | 4 | 42.9% [16–75] | 42.9% [16–75] | 0.429 [0.00–0.71] |
| Location#Transportation | 10 | 8 | 8 | 0 | 2 | 100.0% [68–100] | 80.0% [49–94] | 0.889 [0.67–1.00] |
| Location#Easy_to_find | 5 | 4 | 2 | 2 | 3 | 50.0% [15–85] | 40.0% [12–77] | 0.444 [0.00–0.80] |
| Service#Queue | 8 | 12 | 8 | 4 | 0 | 66.7% [39–86] | 100.0% [68–100] | 0.800 [0.55–0.96] |
| Service#Hospitality | 16 | 17 | 14 | 3 | 2 | 82.4% [59–94] | 87.5% [64–97] | 0.848 [0.69–0.97] |
| Service#Parking | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Service#Timely | 6 | 12 | 4 | 8 | 2 | 33.3% [14–61] | 66.7% [30–90] | 0.444 [0.12–0.70] |
| Ambience#Decoration | 15 | 13 | 12 | 1 | 3 | 92.3% [67–99] | 80.0% [55–93] | 0.857 [0.69–0.97] |
| Ambience#Noise | 11 | 7 | 5 | 2 | 6 | 71.4% [36–92] | 45.5% [21–72] | 0.556 [0.19–0.80] |
| Ambience#Space | 12 | 16 | 8 | 8 | 4 | 50.0% [28–72] | 66.7% [39–86] | 0.571 [0.32–0.77] |
| Ambience#Sanitary | 16 | 7 | 6 | 1 | 10 | 85.7% [49–97] | 37.5% [18–61] | 0.522 [0.22–0.73] |
| **micro** | 230 | 256 | 177 | 79 | 53 | 69.1% | 77.0% | 0.728 [0.68–0.77] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 40/40 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 247/256; cost $0.0084 ($0.209 per 1,000 items).

Confusion: exact 1, under-labelled 3, over-labelled 13, swapped 23.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | Food#Recommend | 8 | confused |
| Ambience#Sanitary | Price#Cost_effective | 5 | confused |
| Food#Taste | Food#Recommend | 5 | confused |
| Price#Level | Price#Cost_effective | 5 | confused |
| Ambience#Sanitary | Food#Recommend | 4 | confused |
| Food#Appearance | Food#Recommend | 4 | confused |
| Food#Taste | Ambience#Space | 4 | confused |
| Food#Taste | Food#Appearance | 4 | confused |
| Food#Taste | Price#Cost_effective | 4 | confused |
| Food#Taste | Service#Timely | 4 | confused |

**Slices of 40 items.** Overall micro F1 0.728, exact match 2.5%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 11 | 0.651 [0.52–0.76] | 0/11 (0.0%) | 0/11 | – | -0.105 [-0.24 to +0.01] | too few |
| 4-5 stars | 29 | 0.756 [0.71–0.79] | 1/29 (3.4%) | 0/29 | – | +0.105 [-0.02 to +0.24] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 10 | 0.705 [0.60–0.78] | 0/10 (0.0%) | 0/10 | – | -0.037 [-0.15 to +0.05] | too few |
| 1-4 labels | 12 | 0.652 [0.57–0.74] | 1/12 (8.3%) | 0/12 | – | -0.094 [-0.18 to +0.01] | too few |
| 5-7 labels | 18 | 0.780 [0.73–0.83] | 0/18 (0.0%) | 0/18 | – | +0.093 [+0.01 to +0.18] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 34 | 0.732 [0.67–0.78] | 1/34 (2.9%) | 0/34 | – | +0.023 [-0.04 to +0.09] | no measured difference |
| no neutral mention | 6 | 0.709 [0.67–0.74] | 0/6 (0.0%) | 0/6 | – | -0.023 [-0.09 to +0.04] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 200–226 chars | 13 | 0.766 [0.69–0.83] | 1/13 (7.7%) | 0/13 | – | +0.055 [-0.04 to +0.15] | too few |
| 227–321 chars | 13 | 0.748 [0.71–0.79] | 0/13 (0.0%) | 0/13 | – | +0.029 [-0.04 to +0.10] | too few |
| 322–585 chars | 14 | 0.678 [0.57–0.77] | 0/14 (0.0%) | 0/14 | – | -0.079 [-0.20 to +0.02] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 15 | 0.708 [0.63–0.78] | 0/15 (0.0%) | 0/15 | – | -0.038 [-0.14 to +0.05] | too few |
| Ambience#Noise | 11 | 0.753 [0.68–0.81] | 0/11 (0.0%) | 0/11 | – | +0.038 [-0.05 to +0.13] | too few |
| Ambience#Sanitary | 16 | 0.733 [0.66–0.79] | 1/16 (6.2%) | 0/16 | – | +0.010 [-0.09 to +0.10] | too few |
| Ambience#Space | 12 | 0.737 [0.66–0.80] | 0/12 (0.0%) | 0/12 | – | +0.014 [-0.08 to +0.10] | too few |
| Food#Appearance | 12 | 0.715 [0.63–0.78] | 0/12 (0.0%) | 0/12 | – | -0.020 [-0.11 to +0.07] | too few |
| Food#Portion | 14 | 0.740 [0.67–0.79] | 0/14 (0.0%) | 0/14 | – | +0.021 [-0.07 to +0.11] | too few |
| Food#Recommend | 12 | 0.783 [0.71–0.85] | 1/12 (8.3%) | 0/12 | – | +0.081 [-0.00 to +0.18] | too few |
| Food#Taste | 36 | 0.726 [0.68–0.77] | 1/36 (2.8%) | 0/36 | – | -0.019 [-0.16 to +0.12] | no measured difference |
| Location#Downtown | 7 | 0.709 [0.56–0.81] | 0/7 (0.0%) | 0/7 | – | -0.025 [-0.18 to +0.09] | too few |
| Location#Easy_to_find | 5 | 0.699 [0.49–0.80] | 0/5 (0.0%) | 0/5 | – | -0.036 [-0.25 to +0.08] | too few |
| Location#Transportation | 10 | 0.735 [0.63–0.81] | 0/10 (0.0%) | 0/10 | – | +0.010 [-0.10 to +0.10] | too few |
| Price#Cost_effective | 11 | 0.762 [0.63–0.85] | 1/11 (9.1%) | 0/11 | – | +0.048 [-0.09 to +0.15] | too few |
| Price#Discount | 14 | 0.767 [0.72–0.81] | 0/14 (0.0%) | 0/14 | – | +0.064 [-0.02 to +0.14] | too few |
| Price#Level | 22 | 0.749 [0.69–0.80] | 0/22 (0.0%) | 0/22 | – | +0.050 [-0.04 to +0.16] | no measured difference |
| Service#Hospitality | 16 | 0.702 [0.61–0.77] | 0/16 (0.0%) | 0/16 | – | -0.046 [-0.15 to +0.04] | too few |
| Service#Parking | 3 | 0.764 [0.75–0.78] | 0/3 (0.0%) | 0/3 | – | +0.040 [-0.01 to +0.10] | too few |
| Service#Queue | 8 | 0.716 [0.63–0.80] | 0/8 (0.0%) | 0/8 | – | -0.016 [-0.12 to +0.08] | too few |
| Service#Timely | 6 | 0.684 [0.47–0.85] | 0/6 (0.0%) | 0/6 | – | -0.054 [-0.27 to +0.12] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / prompt-rules

**asap / dev / prompt-rules: 40 items, 18 labels.** Micro F1 0.789 [0.75–0.83], macro F1 0.762 [0.69–0.81], exact match 3/40 (7.5%) [3–20].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 36 | 39 | 36 | 3 | 0 | 92.3% [80–97] | 100.0% [90–100] | 0.960 [0.91–1.00] |
| Food#Appearance | 12 | 10 | 9 | 1 | 3 | 90.0% [60–98] | 75.0% [47–91] | 0.818 [0.60–0.96] |
| Food#Portion | 14 | 20 | 12 | 8 | 2 | 60.0% [39–78] | 85.7% [60–96] | 0.706 [0.50–0.86] |
| Food#Recommend | 12 | 22 | 10 | 12 | 2 | 45.5% [27–65] | 83.3% [55–95] | 0.588 [0.36–0.76] |
| Price#Level | 22 | 18 | 17 | 1 | 5 | 94.4% [74–99] | 77.3% [57–90] | 0.850 [0.71–0.95] |
| Price#Cost_effective | 11 | 19 | 10 | 9 | 1 | 52.6% [32–73] | 90.9% [62–98] | 0.667 [0.45–0.83] |
| Price#Discount | 14 | 20 | 14 | 6 | 0 | 70.0% [48–85] | 100.0% [78–100] | 0.824 [0.65–0.94] |
| Location#Downtown | 7 | 7 | 4 | 3 | 3 | 57.1% [25–84] | 57.1% [25–84] | 0.571 [0.18–0.86] |
| Location#Transportation | 10 | 7 | 7 | 0 | 3 | 100.0% [65–100] | 70.0% [40–89] | 0.824 [0.57–1.00] |
| Location#Easy_to_find | 5 | 5 | 3 | 2 | 2 | 60.0% [23–88] | 60.0% [23–88] | 0.600 [0.00–0.91] |
| Service#Queue | 8 | 10 | 8 | 2 | 0 | 80.0% [49–94] | 100.0% [68–100] | 0.889 [0.67–1.00] |
| Service#Hospitality | 16 | 17 | 15 | 2 | 1 | 88.2% [66–97] | 93.8% [72–99] | 0.909 [0.79–1.00] |
| Service#Parking | 3 | 4 | 3 | 1 | 0 | 75.0% [30–95] | 100.0% [44–100] | 0.857 [0.00–1.00] |
| Service#Timely | 6 | 11 | 5 | 6 | 1 | 45.5% [21–72] | 83.3% [44–97] | 0.588 [0.23–0.83] |
| Ambience#Decoration | 15 | 17 | 14 | 3 | 1 | 82.4% [59–94] | 93.3% [70–99] | 0.875 [0.71–0.97] |
| Ambience#Noise | 11 | 10 | 8 | 2 | 3 | 80.0% [49–94] | 72.7% [43–90] | 0.762 [0.50–0.94] |
| Ambience#Space | 12 | 16 | 9 | 7 | 3 | 56.2% [33–77] | 75.0% [47–91] | 0.643 [0.40–0.83] |
| Ambience#Sanitary | 16 | 12 | 11 | 1 | 5 | 91.7% [65–99] | 68.8% [44–86] | 0.786 [0.58–0.92] |
| **micro** | 230 | 264 | 195 | 69 | 35 | 73.9% | 84.8% | 0.789 [0.75–0.83] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 40/40 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 262/264; cost $0.0107 ($0.267 per 1,000 items).

Confusion: exact 3, under-labelled 5, over-labelled 18, swapped 14.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Food#Recommend | 7 | confused |
| Food#Taste | Ambience#Space | 6 | confused |
| Price#Level | Food#Recommend | 6 | confused |
| Food#Taste | Food#Portion | 4 | confused |
| Food#Taste | Price#Cost_effective | 4 | confused |
| Food#Taste | Service#Timely | 4 | confused |
| Ambience#Sanitary | Price#Cost_effective | 3 | confused |
| Food#Portion | Food#Recommend | 3 | confused |
| Food#Portion | Price#Cost_effective | 3 | confused |
| Food#Taste | Ambience#Decoration | 3 | confused |

**Slices of 40 items.** Overall micro F1 0.789, exact match 7.5%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 11 | 0.750 [0.63–0.84] | 0/11 (0.0%) | 0/11 | – | -0.054 [-0.18 to +0.04] | too few |
| 4-5 stars | 29 | 0.804 [0.76–0.84] | 3/29 (10.3%) | 0/29 | – | +0.054 [-0.04 to +0.17] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 10 | 0.804 [0.73–0.87] | 0/10 (0.0%) | 0/10 | – | +0.024 [-0.06 to +0.11] | too few |
| 1-4 labels | 12 | 0.602 [0.54–0.67] | 0/12 (0.0%) | 0/12 | – | -0.231 [-0.31 to -0.16] | too few |
| 5-7 labels | 18 | 0.857 [0.81–0.90] | 3/18 (16.7%) | 0/18 | – | +0.121 [+0.04 to +0.21] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 34 | 0.805 [0.76–0.84] | 3/34 (8.8%) | 0/34 | – | +0.096 [-0.03 to +0.21] | no measured difference |
| no neutral mention | 6 | 0.709 [0.60–0.83] | 0/6 (0.0%) | 0/6 | – | -0.096 [-0.22 to +0.03] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 200–226 chars | 13 | 0.823 [0.76–0.88] | 1/13 (7.7%) | 0/13 | – | +0.049 [-0.03 to +0.12] | too few |
| 227–321 chars | 13 | 0.821 [0.75–0.89] | 2/13 (15.4%) | 0/13 | – | +0.045 [-0.04 to +0.13] | too few |
| 322–585 chars | 14 | 0.733 [0.65–0.81] | 0/14 (0.0%) | 0/14 | – | -0.088 [-0.18 to -0.00] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 15 | 0.812 [0.76–0.86] | 1/15 (6.7%) | 0/15 | – | +0.043 [-0.04 to +0.13] | too few |
| Ambience#Noise | 11 | 0.832 [0.78–0.88] | 1/11 (9.1%) | 0/11 | – | +0.066 [-0.01 to +0.14] | too few |
| Ambience#Sanitary | 16 | 0.820 [0.77–0.87] | 2/16 (12.5%) | 0/16 | – | +0.064 [-0.02 to +0.15] | too few |
| Ambience#Space | 12 | 0.823 [0.76–0.88] | 1/12 (8.3%) | 0/12 | – | +0.055 [-0.02 to +0.14] | too few |
| Food#Appearance | 12 | 0.773 [0.70–0.84] | 1/12 (8.3%) | 0/12 | – | -0.025 [-0.11 to +0.07] | too few |
| Food#Portion | 14 | 0.804 [0.74–0.86] | 1/14 (7.1%) | 0/14 | – | +0.025 [-0.06 to +0.11] | too few |
| Food#Recommend | 12 | 0.827 [0.77–0.88] | 2/12 (16.7%) | 0/12 | – | +0.056 [-0.02 to +0.13] | too few |
| Food#Taste | 36 | 0.779 [0.73–0.82] | 2/36 (5.6%) | 0/36 | – | -0.094 [-0.20 to -0.01] | worse |
| Location#Downtown | 7 | 0.817 [0.76–0.85] | 0/7 (0.0%) | 0/7 | – | +0.036 [-0.03 to +0.10] | too few |
| Location#Easy_to_find | 5 | 0.813 [0.74–0.85] | 0/5 (0.0%) | 0/5 | – | +0.029 [-0.05 to +0.10] | too few |
| Location#Transportation | 10 | 0.807 [0.74–0.87] | 1/10 (10.0%) | 0/10 | – | +0.027 [-0.06 to +0.12] | too few |
| Price#Cost_effective | 11 | 0.861 [0.82–0.90] | 0/11 (0.0%) | 0/11 | – | +0.103 [+0.04 to +0.17] | too few |
| Price#Discount | 14 | 0.816 [0.77–0.85] | 0/14 (0.0%) | 0/14 | – | +0.045 [-0.03 to +0.12] | too few |
| Price#Level | 22 | 0.806 [0.75–0.86] | 2/22 (9.1%) | 0/22 | – | +0.038 [-0.04 to +0.13] | no measured difference |
| Service#Hospitality | 16 | 0.789 [0.72–0.85] | 2/16 (12.5%) | 0/16 | – | -0.001 [-0.09 to +0.08] | too few |
| Service#Parking | 3 | 0.857 [0.75–0.94] | 0/3 (0.0%) | 0/3 | – | +0.076 [-0.03 to +0.16] | too few |
| Service#Queue | 8 | 0.714 [0.61–0.81] | 0/8 (0.0%) | 0/8 | – | -0.094 [-0.20 to +0.02] | too few |
| Service#Timely | 6 | 0.857 [0.74–0.95] | 1/6 (16.7%) | 0/6 | – | +0.082 [-0.04 to +0.19] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent

**asap / dev / agent: 40 items, 18 labels.** Micro F1 0.831 [0.79–0.87], macro F1 0.809 [0.74–0.85], exact match 7/40 (17.5%) [9–32].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 36 | 38 | 36 | 2 | 0 | 94.7% [83–99] | 100.0% [90–100] | 0.973 [0.93–1.00] |
| Food#Appearance | 12 | 7 | 6 | 1 | 6 | 85.7% [49–97] | 50.0% [25–75] | 0.632 [0.33–0.86] |
| Food#Portion | 14 | 15 | 13 | 2 | 1 | 86.7% [62–96] | 92.9% [69–99] | 0.897 [0.75–1.00] |
| Food#Recommend | 12 | 10 | 9 | 1 | 3 | 90.0% [60–98] | 75.0% [47–91] | 0.818 [0.60–0.96] |
| Price#Level | 22 | 12 | 11 | 1 | 11 | 91.7% [65–99] | 50.0% [31–69] | 0.647 [0.43–0.81] |
| Price#Cost_effective | 11 | 14 | 10 | 4 | 1 | 71.4% [45–88] | 90.9% [62–98] | 0.800 [0.58–0.95] |
| Price#Discount | 14 | 18 | 13 | 5 | 1 | 72.2% [49–88] | 92.9% [69–99] | 0.812 [0.64–0.94] |
| Location#Downtown | 7 | 5 | 4 | 1 | 3 | 80.0% [38–96] | 57.1% [25–84] | 0.667 [0.25–0.92] |
| Location#Transportation | 10 | 8 | 8 | 0 | 2 | 100.0% [68–100] | 80.0% [49–94] | 0.889 [0.67–1.00] |
| Location#Easy_to_find | 5 | 5 | 3 | 2 | 2 | 60.0% [23–88] | 60.0% [23–88] | 0.600 [0.00–0.91] |
| Service#Queue | 8 | 9 | 8 | 1 | 0 | 88.9% [57–98] | 100.0% [68–100] | 0.941 [0.80–1.00] |
| Service#Hospitality | 16 | 16 | 14 | 2 | 2 | 87.5% [64–97] | 87.5% [64–97] | 0.875 [0.72–0.97] |
| Service#Parking | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Service#Timely | 6 | 8 | 5 | 3 | 1 | 62.5% [31–86] | 83.3% [44–97] | 0.714 [0.33–0.93] |
| Ambience#Decoration | 15 | 14 | 13 | 1 | 2 | 92.9% [69–99] | 86.7% [62–96] | 0.897 [0.75–1.00] |
| Ambience#Noise | 11 | 8 | 8 | 0 | 3 | 100.0% [68–100] | 72.7% [43–90] | 0.842 [0.60–1.00] |
| Ambience#Space | 12 | 14 | 11 | 3 | 1 | 78.6% [52–92] | 91.7% [65–99] | 0.846 [0.67–0.97] |
| Ambience#Sanitary | 16 | 9 | 9 | 0 | 7 | 100.0% [70–100] | 56.2% [33–77] | 0.720 [0.48–0.88] |
| **micro** | 230 | 213 | 184 | 29 | 46 | 86.4% | 80.0% | 0.831 [0.79–0.87] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 40/40 answered; 2.25 calls and 0.93 tool calls per item; rule gate 9, quote repair 4, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 213/213; cost $0.0268 ($0.671 per 1,000 items). Items on which each tool was called: get_label_rules 90%.

Confusion: exact 7, under-labelled 12, over-labelled 7, swapped 14.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Appearance | (no predicted label) | 5 | missed |
| Ambience#Sanitary | (no predicted label) | 4 | missed |
| Ambience#Noise | (no predicted label) | 3 | missed |
| Price#Level | (no predicted label) | 3 | missed |
| Price#Level | Price#Cost_effective | 3 | confused |
| Price#Level | Price#Discount | 3 | confused |
| Ambience#Decoration | (no predicted label) | 2 | missed |
| Ambience#Sanitary | Price#Cost_effective | 2 | confused |
| Ambience#Sanitary | Service#Hospitality | 2 | confused |
| Food#Taste | Ambience#Space | 2 | confused |

**Slices of 40 items.** Overall micro F1 0.831, exact match 17.5%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 11 | 0.835 [0.76–0.89] | 2/11 (18.2%) | 0/11 | – | +0.006 [-0.08 to +0.08] | too few |
| 4-5 stars | 29 | 0.829 [0.78–0.87] | 5/29 (17.2%) | 0/29 | – | -0.006 [-0.07 to +0.07] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 10 | 0.800 [0.74–0.86] | 0/10 (0.0%) | 0/10 | – | -0.050 [-0.12 to +0.02] | too few |
| 1-4 labels | 12 | 0.730 [0.64–0.84] | 3/12 (25.0%) | 0/12 | – | -0.121 [-0.22 to -0.01] | too few |
| 5-7 labels | 18 | 0.894 [0.86–0.93] | 4/18 (22.2%) | 0/18 | – | +0.116 [+0.06 to +0.18] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 34 | 0.827 [0.79–0.86] | 4/34 (11.8%) | 0/34 | – | -0.026 [-0.16 to +0.10] | no measured difference |
| no neutral mention | 6 | 0.853 [0.73–0.98] | 3/6 (50.0%) | 0/6 | – | +0.026 [-0.11 to +0.16] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 200–226 chars | 13 | 0.828 [0.76–0.89] | 2/13 (15.4%) | 0/13 | – | -0.005 [-0.08 to +0.07] | too few |
| 227–321 chars | 13 | 0.867 [0.82–0.91] | 2/13 (15.4%) | 0/13 | – | +0.054 [-0.01 to +0.12] | too few |
| 322–585 chars | 14 | 0.800 [0.73–0.87] | 3/14 (21.4%) | 0/14 | – | -0.047 [-0.14 to +0.03] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 15 | 0.817 [0.76–0.87] | 1/15 (6.7%) | 0/15 | – | -0.028 [-0.10 to +0.05] | too few |
| Ambience#Noise | 11 | 0.838 [0.77–0.90] | 2/11 (18.2%) | 0/11 | – | +0.011 [-0.07 to +0.09] | too few |
| Ambience#Sanitary | 16 | 0.825 [0.78–0.87] | 1/16 (6.2%) | 0/16 | – | -0.012 [-0.08 to +0.06] | too few |
| Ambience#Space | 12 | 0.834 [0.78–0.89] | 1/12 (8.3%) | 0/12 | – | +0.006 [-0.07 to +0.08] | too few |
| Food#Appearance | 12 | 0.819 [0.76–0.89] | 2/12 (16.7%) | 0/12 | – | -0.017 [-0.09 to +0.07] | too few |
| Food#Portion | 14 | 0.832 [0.77–0.89] | 3/14 (21.4%) | 0/14 | – | +0.003 [-0.07 to +0.08] | too few |
| Food#Recommend | 12 | 0.824 [0.76–0.89] | 2/12 (16.7%) | 0/12 | – | -0.011 [-0.09 to +0.07] | too few |
| Food#Taste | 36 | 0.831 [0.79–0.87] | 7/36 (19.4%) | 0/36 | – | +0.001 [-0.08 to +0.06] | no measured difference |
| Location#Downtown | 7 | 0.822 [0.79–0.85] | 0/7 (0.0%) | 0/7 | – | -0.011 [-0.06 to +0.04] | too few |
| Location#Easy_to_find | 5 | 0.829 [0.80–0.86] | 0/5 (0.0%) | 0/5 | – | -0.002 [-0.05 to +0.05] | too few |
| Location#Transportation | 10 | 0.835 [0.80–0.88] | 1/10 (10.0%) | 0/10 | – | +0.007 [-0.06 to +0.08] | too few |
| Price#Cost_effective | 11 | 0.863 [0.83–0.90] | 1/11 (9.1%) | 0/11 | – | +0.048 [-0.02 to +0.11] | too few |
| Price#Discount | 14 | 0.809 [0.76–0.85] | 0/14 (0.0%) | 0/14 | – | -0.036 [-0.11 to +0.03] | too few |
| Price#Level | 22 | 0.833 [0.79–0.88] | 3/22 (13.6%) | 0/22 | – | +0.005 [-0.07 to +0.08] | no measured difference |
| Service#Hospitality | 16 | 0.827 [0.76–0.89] | 4/16 (25.0%) | 0/16 | – | -0.007 [-0.08 to +0.07] | too few |
| Service#Parking | 3 | 0.920 [0.86–1.00] | 1/3 (33.3%) | 0/3 | – | +0.101 [+0.03 to +0.19] | too few |
| Service#Queue | 8 | 0.791 [0.69–0.90] | 2/8 (25.0%) | 0/8 | – | -0.050 [-0.15 to +0.07] | too few |
| Service#Timely | 6 | 0.897 [0.85–0.94] | 1/6 (16.7%) | 0/6 | – | +0.081 [+0.02 to +0.14] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases

**asap / dev / agent-cases: 40 items, 18 labels.** Micro F1 0.823 [0.78–0.87], macro F1 0.790 [0.72–0.84], exact match 8/40 (20.0%) [10–35].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 36 | 38 | 36 | 2 | 0 | 94.7% [83–99] | 100.0% [90–100] | 0.973 [0.93–1.00] |
| Food#Appearance | 12 | 7 | 6 | 1 | 6 | 85.7% [49–97] | 50.0% [25–75] | 0.632 [0.33–0.86] |
| Food#Portion | 14 | 16 | 14 | 2 | 0 | 87.5% [64–97] | 100.0% [78–100] | 0.933 [0.82–1.00] |
| Food#Recommend | 12 | 10 | 9 | 1 | 3 | 90.0% [60–98] | 75.0% [47–91] | 0.818 [0.59–0.96] |
| Price#Level | 22 | 10 | 10 | 0 | 12 | 100.0% [72–100] | 45.5% [27–65] | 0.625 [0.38–0.80] |
| Price#Cost_effective | 11 | 13 | 10 | 3 | 1 | 76.9% [50–92] | 90.9% [62–98] | 0.833 [0.63–0.97] |
| Price#Discount | 14 | 16 | 12 | 4 | 2 | 75.0% [51–90] | 85.7% [60–96] | 0.800 [0.61–0.93] |
| Location#Downtown | 7 | 3 | 2 | 1 | 5 | 66.7% [21–94] | 28.6% [8–64] | 0.400 [0.00–0.75] |
| Location#Transportation | 10 | 7 | 7 | 0 | 3 | 100.0% [65–100] | 70.0% [40–89] | 0.824 [0.57–1.00] |
| Location#Easy_to_find | 5 | 6 | 3 | 3 | 2 | 50.0% [19–81] | 60.0% [23–88] | 0.545 [0.00–0.86] |
| Service#Queue | 8 | 9 | 8 | 1 | 0 | 88.9% [57–98] | 100.0% [68–100] | 0.941 [0.80–1.00] |
| Service#Hospitality | 16 | 15 | 13 | 2 | 3 | 86.7% [62–96] | 81.2% [57–93] | 0.839 [0.67–0.97] |
| Service#Parking | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Service#Timely | 6 | 9 | 5 | 4 | 1 | 55.6% [27–81] | 83.3% [44–97] | 0.667 [0.29–0.90] |
| Ambience#Decoration | 15 | 13 | 13 | 0 | 2 | 100.0% [77–100] | 86.7% [62–96] | 0.929 [0.80–1.00] |
| Ambience#Noise | 11 | 9 | 9 | 0 | 2 | 100.0% [70–100] | 81.8% [52–95] | 0.900 [0.71–1.00] |
| Ambience#Space | 12 | 15 | 10 | 5 | 2 | 66.7% [42–85] | 83.3% [55–95] | 0.741 [0.52–0.90] |
| Ambience#Sanitary | 16 | 11 | 11 | 0 | 5 | 100.0% [74–100] | 68.8% [44–86] | 0.815 [0.62–0.95] |
| **micro** | 230 | 210 | 181 | 29 | 49 | 86.2% | 78.7% | 0.823 [0.78–0.87] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 40/40 answered; 2.33 calls and 0.00 tool calls per item; rule gate 40, quote repair 13, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 208/210; cost $0.0367 ($0.917 per 1,000 items).

Confusion: exact 8, under-labelled 12, over-labelled 6, swapped 14.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | (no predicted label) | 4 | missed |
| Food#Appearance | (no predicted label) | 3 | missed |
| Food#Taste | Ambience#Space | 3 | confused |
| Price#Level | Price#Discount | 3 | confused |
| Service#Hospitality | Service#Timely | 3 | confused |
| Ambience#Decoration | Service#Timely | 2 | confused |
| Ambience#Sanitary | (no predicted label) | 2 | missed |
| Food#Taste | Service#Timely | 2 | confused |
| Location#Downtown | (no predicted label) | 2 | missed |
| Location#Transportation | (no predicted label) | 2 | missed |

**Slices of 40 items.** Overall micro F1 0.823, exact match 20.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 11 | 0.810 [0.73–0.88] | 2/11 (18.2%) | 0/11 | – | -0.017 [-0.11 to +0.07] | too few |
| 4-5 stars | 29 | 0.827 [0.77–0.88] | 6/29 (20.7%) | 0/29 | – | +0.017 [-0.07 to +0.11] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 10 | 0.788 [0.71–0.86] | 1/10 (10.0%) | 0/10 | – | -0.056 [-0.16 to +0.04] | too few |
| 1-4 labels | 12 | 0.714 [0.60–0.82] | 2/12 (16.7%) | 0/12 | – | -0.129 [-0.25 to -0.01] | too few |
| 5-7 labels | 18 | 0.890 [0.84–0.94] | 5/18 (27.8%) | 0/18 | – | +0.123 [+0.05 to +0.21] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 34 | 0.815 [0.76–0.87] | 6/34 (17.6%) | 0/34 | – | -0.051 [-0.16 to +0.06] | no measured difference |
| no neutral mention | 6 | 0.866 [0.77–0.96] | 2/6 (33.3%) | 0/6 | – | +0.051 [-0.06 to +0.16] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 200–226 chars | 13 | 0.814 [0.72–0.90] | 2/13 (15.4%) | 0/13 | – | -0.013 [-0.12 to +0.08] | too few |
| 227–321 chars | 13 | 0.887 [0.82–0.94] | 4/13 (30.8%) | 0/13 | – | +0.095 [+0.01 to +0.18] | too few |
| 322–585 chars | 14 | 0.771 [0.70–0.84] | 2/14 (14.3%) | 0/14 | – | -0.079 [-0.17 to +0.01] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 15 | 0.811 [0.74–0.88] | 3/15 (20.0%) | 0/15 | – | -0.023 [-0.12 to +0.07] | too few |
| Ambience#Noise | 11 | 0.838 [0.75–0.92] | 4/11 (36.4%) | 0/11 | – | +0.023 [-0.09 to +0.12] | too few |
| Ambience#Sanitary | 16 | 0.837 [0.77–0.90] | 4/16 (25.0%) | 0/16 | – | +0.031 [-0.06 to +0.12] | too few |
| Ambience#Space | 12 | 0.836 [0.74–0.92] | 4/12 (33.3%) | 0/12 | – | +0.022 [-0.08 to +0.12] | too few |
| Food#Appearance | 12 | 0.792 [0.70–0.88] | 2/12 (16.7%) | 0/12 | – | -0.046 [-0.14 to +0.05] | too few |
| Food#Portion | 14 | 0.806 [0.73–0.88] | 3/14 (21.4%) | 0/14 | – | -0.028 [-0.12 to +0.06] | too few |
| Food#Recommend | 12 | 0.795 [0.70–0.88] | 2/12 (16.7%) | 0/12 | – | -0.043 [-0.15 to +0.06] | too few |
| Food#Taste | 36 | 0.820 [0.77–0.87] | 7/36 (19.4%) | 0/36 | – | -0.027 [-0.16 to +0.08] | no measured difference |
| Location#Downtown | 7 | 0.788 [0.74–0.82] | 0/7 (0.0%) | 0/7 | – | -0.045 [-0.11 to +0.03] | too few |
| Location#Easy_to_find | 5 | 0.805 [0.78–0.82] | 0/5 (0.0%) | 0/5 | – | -0.022 [-0.08 to +0.04] | too few |
| Location#Transportation | 10 | 0.826 [0.79–0.88] | 1/10 (10.0%) | 0/10 | – | +0.005 [-0.07 to +0.09] | too few |
| Price#Cost_effective | 11 | 0.870 [0.83–0.93] | 2/11 (18.2%) | 0/11 | – | +0.068 [-0.01 to +0.15] | too few |
| Price#Discount | 14 | 0.800 [0.72–0.87] | 2/14 (14.3%) | 0/14 | – | -0.038 [-0.14 to +0.05] | too few |
| Price#Level | 22 | 0.828 [0.78–0.88] | 3/22 (13.6%) | 0/22 | – | +0.013 [-0.08 to +0.11] | no measured difference |
| Service#Hospitality | 16 | 0.804 [0.73–0.88] | 2/16 (12.5%) | 0/16 | – | -0.033 [-0.13 to +0.05] | too few |
| Service#Parking | 3 | 0.898 [0.80–1.00] | 1/3 (33.3%) | 0/3 | – | +0.085 [-0.02 to +0.20] | too few |
| Service#Queue | 8 | 0.791 [0.67–0.91] | 2/8 (25.0%) | 0/8 | – | -0.040 [-0.16 to +0.09] | too few |
| Service#Timely | 6 | 0.911 [0.84–0.99] | 3/6 (50.0%) | 0/6 | – | +0.108 [+0.02 to +0.19] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / dev / agent-cases-check

**asap / dev / agent-cases-check: 40 items, 18 labels.** Micro F1 0.824 [0.79–0.86], macro F1 0.799 [0.73–0.84], exact match 8/40 (20.0%) [10–35].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 36 | 38 | 36 | 2 | 0 | 94.7% [83–99] | 100.0% [90–100] | 0.973 [0.93–1.00] |
| Food#Appearance | 12 | 8 | 7 | 1 | 5 | 87.5% [53–98] | 58.3% [32–81] | 0.700 [0.42–0.90] |
| Food#Portion | 14 | 15 | 13 | 2 | 1 | 86.7% [62–96] | 92.9% [69–99] | 0.897 [0.75–1.00] |
| Food#Recommend | 12 | 9 | 9 | 0 | 3 | 100.0% [70–100] | 75.0% [47–91] | 0.857 [0.67–1.00] |
| Price#Level | 22 | 11 | 9 | 2 | 13 | 81.8% [52–95] | 40.9% [23–61] | 0.545 [0.31–0.73] |
| Price#Cost_effective | 11 | 14 | 10 | 4 | 1 | 71.4% [45–88] | 90.9% [62–98] | 0.800 [0.58–0.95] |
| Price#Discount | 14 | 19 | 13 | 6 | 1 | 68.4% [46–85] | 92.9% [69–99] | 0.788 [0.61–0.92] |
| Location#Downtown | 7 | 3 | 2 | 1 | 5 | 66.7% [21–94] | 28.6% [8–64] | 0.400 [0.00–0.75] |
| Location#Transportation | 10 | 8 | 8 | 0 | 2 | 100.0% [68–100] | 80.0% [49–94] | 0.889 [0.67–1.00] |
| Location#Easy_to_find | 5 | 7 | 4 | 3 | 1 | 57.1% [25–84] | 80.0% [38–96] | 0.667 [0.22–0.92] |
| Service#Queue | 8 | 9 | 8 | 1 | 0 | 88.9% [57–98] | 100.0% [68–100] | 0.941 [0.80–1.00] |
| Service#Hospitality | 16 | 19 | 16 | 3 | 0 | 84.2% [62–94] | 100.0% [81–100] | 0.914 [0.80–1.00] |
| Service#Parking | 3 | 3 | 3 | 0 | 0 | 100.0% [44–100] | 100.0% [44–100] | 1.000 [1.00–1.00] |
| Service#Timely | 6 | 8 | 5 | 3 | 1 | 62.5% [31–86] | 83.3% [44–97] | 0.714 [0.33–0.93] |
| Ambience#Decoration | 15 | 13 | 12 | 1 | 3 | 92.3% [67–99] | 80.0% [55–93] | 0.857 [0.69–0.97] |
| Ambience#Noise | 11 | 8 | 8 | 0 | 3 | 100.0% [68–100] | 72.7% [43–90] | 0.842 [0.60–1.00] |
| Ambience#Space | 12 | 12 | 10 | 2 | 2 | 83.3% [55–95] | 83.3% [55–95] | 0.833 [0.62–0.97] |
| Ambience#Sanitary | 16 | 10 | 10 | 0 | 6 | 100.0% [72–100] | 62.5% [39–82] | 0.769 [0.55–0.92] |
| **micro** | 230 | 214 | 183 | 31 | 47 | 85.5% | 79.6% | 0.824 [0.79–0.86] |

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 40/40 answered; 3.50 calls and 0.35 tool calls per item; rule gate 39, quote repair 7, self-check changed 14 of 40 items (+9 / −8 labels); exact quotes 210/214; cost $0.0570 ($1.425 per 1,000 items). Items on which each tool was called: get_label_rules 32%.

Confusion: exact 8, under-labelled 12, over-labelled 6, swapped 14.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | (no predicted label) | 5 | missed |
| Ambience#Decoration | (no predicted label) | 3 | missed |
| Ambience#Sanitary | (no predicted label) | 3 | missed |
| Food#Appearance | (no predicted label) | 3 | missed |
| Food#Taste | Price#Discount | 3 | confused |
| Food#Taste | Service#Timely | 3 | confused |
| Price#Level | Price#Discount | 3 | confused |
| Ambience#Noise | (no predicted label) | 2 | missed |
| Ambience#Sanitary | Price#Cost_effective | 2 | confused |
| Food#Taste | Ambience#Space | 2 | confused |

**Slices of 40 items.** Overall micro F1 0.824, exact match 20.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 11 | 0.833 [0.76–0.90] | 3/11 (27.3%) | 0/11 | – | +0.012 [-0.08 to +0.09] | too few |
| 4-5 stars | 29 | 0.821 [0.77–0.87] | 5/29 (17.2%) | 0/29 | – | -0.012 [-0.10 to +0.07] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 10 | 0.807 [0.74–0.87] | 1/10 (10.0%) | 0/10 | – | -0.028 [-0.11 to +0.06] | too few |
| 1-4 labels | 12 | 0.718 [0.64–0.82] | 3/12 (25.0%) | 0/12 | – | -0.129 [-0.22 to -0.02] | too few |
| 5-7 labels | 18 | 0.882 [0.84–0.93] | 4/18 (22.2%) | 0/18 | – | +0.103 [+0.04 to +0.18] | too few |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 34 | 0.816 [0.78–0.85] | 4/34 (11.8%) | 0/34 | – | -0.054 [-0.20 to +0.09] | no measured difference |
| no neutral mention | 6 | 0.870 [0.74–1.00] | 4/6 (66.7%) | 0/6 | – | +0.054 [-0.09 to +0.20] | too few |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 200–226 chars | 13 | 0.819 [0.76–0.88] | 1/13 (7.7%) | 0/13 | – | -0.007 [-0.09 to +0.07] | too few |
| 227–321 chars | 13 | 0.879 [0.82–0.94] | 4/13 (30.8%) | 0/13 | – | +0.081 [+0.01 to +0.16] | too few |
| 322–585 chars | 14 | 0.780 [0.71–0.85] | 3/14 (21.4%) | 0/14 | – | -0.069 [-0.15 to +0.01] | too few |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| Ambience#Decoration | 15 | 0.813 [0.75–0.87] | 3/15 (20.0%) | 0/15 | – | -0.023 [-0.10 to +0.05] | too few |
| Ambience#Noise | 11 | 0.845 [0.77–0.92] | 4/11 (36.4%) | 0/11 | – | +0.032 [-0.05 to +0.12] | too few |
| Ambience#Sanitary | 16 | 0.833 [0.78–0.89] | 3/16 (18.8%) | 0/16 | – | +0.020 [-0.05 to +0.10] | too few |
| Ambience#Space | 12 | 0.836 [0.77–0.90] | 3/12 (25.0%) | 0/12 | – | +0.020 [-0.06 to +0.10] | too few |
| Food#Appearance | 12 | 0.822 [0.75–0.91] | 4/12 (33.3%) | 0/12 | – | -0.004 [-0.09 to +0.09] | too few |
| Food#Portion | 14 | 0.820 [0.76–0.88] | 2/14 (14.3%) | 0/14 | – | -0.008 [-0.09 to +0.07] | too few |
| Food#Recommend | 12 | 0.816 [0.75–0.88] | 2/12 (16.7%) | 0/12 | – | -0.013 [-0.09 to +0.07] | too few |
| Food#Taste | 36 | 0.821 [0.77–0.86] | 7/36 (19.4%) | 0/36 | – | -0.025 [-0.15 to +0.07] | no measured difference |
| Location#Downtown | 7 | 0.808 [0.77–0.84] | 0/7 (0.0%) | 0/7 | – | -0.022 [-0.08 to +0.04] | too few |
| Location#Easy_to_find | 5 | 0.829 [0.80–0.86] | 0/5 (0.0%) | 0/5 | – | +0.006 [-0.05 to +0.06] | too few |
| Location#Transportation | 10 | 0.826 [0.78–0.88] | 1/10 (10.0%) | 0/10 | – | +0.002 [-0.07 to +0.08] | too few |
| Price#Cost_effective | 11 | 0.849 [0.81–0.89] | 0/11 (0.0%) | 0/11 | – | +0.036 [-0.03 to +0.10] | too few |
| Price#Discount | 14 | 0.804 [0.76–0.84] | 0/14 (0.0%) | 0/14 | – | -0.033 [-0.10 to +0.04] | too few |
| Price#Level | 22 | 0.822 [0.78–0.87] | 2/22 (9.1%) | 0/22 | – | -0.005 [-0.09 to +0.08] | no measured difference |
| Service#Hospitality | 16 | 0.837 [0.77–0.90] | 5/16 (31.2%) | 0/16 | – | +0.022 [-0.06 to +0.11] | too few |
| Service#Parking | 3 | 0.941 [0.86–1.00] | 2/3 (66.7%) | 0/3 | – | +0.132 [+0.04 to +0.22] | too few |
| Service#Queue | 8 | 0.791 [0.69–0.90] | 2/8 (25.0%) | 0/8 | – | -0.042 [-0.14 to +0.08] | too few |
| Service#Timely | 6 | 0.883 [0.82–0.95] | 1/6 (16.7%) | 0/6 | – | +0.071 [-0.00 to +0.15] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


