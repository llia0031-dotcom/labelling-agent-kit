# Analysis: main

## ad_policy / test_a

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 119 | 0.768 [0.70–0.83] | 0.789 [0.68–0.86] | 84/119 | 5/67 | 15/52 | 1.00 | 0.00 | 0.08 | 0 |
| prompt-rules | 119 | 0.878 [0.83–0.92] | 0.884 [0.80–0.94] | 101/119 | 4/67 | 3/52 | 1.00 | 0.00 | 0.10 | 0 |
| agent | 119 | 0.925 [0.88–0.96] | 0.929 [0.86–0.97] | 108/119 | 1/67 | 4/52 | 1.86 | 0.73 | 0.24 | 0 |
| agent-cases | 119 | 0.965 [0.93–0.99] | 0.962 [0.91–0.99] | 114/119 | 0/67 | 1/52 | 1.71 | 0.21 | 0.28 | 0 |
| agent-cases-check | 119 | 0.971 [0.94–0.99] | 0.967 [0.92–1.00] | 115/119 | 1/67 | 0/52 | 2.96 | 0.55 | 0.53 | 0 |

## asap / test_a

| Arm | Items | Micro F1 | Macro F1 | Exact match | Miss | False alarm | Calls/item | Tools/item | $ per 1k items | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| prompt-short | 201 | 0.715 [0.70–0.73] | 0.675 [0.65–0.70] | 6/201 | 0/199 | 0/2 | 1.00 | 0.00 | 0.21 | 0 |
| prompt-rules | 201 | 0.782 [0.76–0.80] | 0.750 [0.72–0.77] | 16/201 | 0/199 | 0/2 | 1.00 | 0.00 | 0.25 | 0 |
| agent | 201 | 0.799 [0.78–0.82] | 0.756 [0.73–0.78] | 21/201 | 0/199 | 0/2 | 2.14 | 0.39 | 0.72 | 0 |
| agent-cases | 201 | 0.812 [0.79–0.83] | 0.776 [0.75–0.80] | 28/201 | 0/199 | 0/2 | 2.13 | 0.01 | 0.91 | 0 |
| agent-cases-check | 201 | 0.824 [0.80–0.84] | 0.789 [0.76–0.81] | 36/201 | 0/199 | 0/2 | 3.40 | 0.26 | 1.59 | 0 |
| agent-cases-synthetic | 201 | 0.802 [0.78–0.82] | 0.761 [0.73–0.78] | 28/201 | 0/199 | 0/2 | 2.19 | 0.03 | 0.95 | 0 |
| agent-cases-mixed | 201 | 0.802 [0.78–0.82] | 0.762 [0.73–0.78] | 23/201 | 0/199 | 0/2 | 2.12 | 0.00 | 0.92 | 0 |

## Comparisons (B − A, micro F1, paired bootstrap 95%)

| Id | Task / set | A | B | Δ micro F1 | Δ macro F1 | McNemar p (exact match) | Verdict |
|---|---|---|---|---|---|---|---|
| H1-ad | ad_policy / test_a | prompt-short | agent | +0.157 [+0.106, +0.214] | +0.139 [+0.085, +0.219] | 0.000 | B better |
| H1-asap | asap / test_a | prompt-short | agent | +0.083 [+0.064, +0.102] | +0.081 [+0.055, +0.106] | 0.001 | B better |
| H2-ad | ad_policy / test_a | agent | agent-cases | +0.040 [+0.007, +0.076] | +0.034 [+0.005, +0.081] | 0.070 | B better |
| H2-asap | asap / test_a | agent | agent-cases | +0.014 [+0.003, +0.024] | +0.020 [+0.005, +0.035] | 0.143 | B better |
| H3-ad | ad_policy / test_a | agent-cases | agent-cases-check | +0.006 [-0.023, +0.038] | +0.004 [-0.057, +0.068] | 1.000 | no measured difference |
| H3-asap | asap / test_a | agent-cases | agent-cases-check | +0.012 [+0.001, +0.023] | +0.013 [-0.003, +0.028] | 0.185 | B better |
| H4-ad | ad_policy / test_a | prompt-rules | agent | +0.047 [-0.004, +0.097] | +0.044 [-0.030, +0.125] | 0.143 | no measured difference |
| H4-asap | asap / test_a | prompt-rules | agent | +0.017 [+0.000, +0.033] | +0.006 [-0.018, +0.026] | 0.405 | B better |
| H5a | asap / test_a | agent-cases-synthetic | agent-cases | +0.010 [-0.001, +0.022] | +0.015 [-0.001, +0.032] | 1.000 | no measured difference |
| H5b | asap / test_a | agent-cases-mixed | agent-cases | +0.010 [+0.001, +0.021] | +0.014 [-0.001, +0.030] | 0.302 | B better |


# Details per arm

## ad_policy / test_a / prompt-short

**ad_policy / test_a / prompt-short: 119 items, 9 labels.** Micro F1 0.768 [0.70–0.83], macro F1 0.789 [0.68–0.86], exact match 84/119 (70.6%) [62–78].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 24 | 10 | 14 | 0 | 41.7% [24–61] | 100.0% [72–100] | 0.588 [0.36–0.75] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 25 | 14 | 11 | 0 | 56.0% [37–73] | 100.0% [78–100] | 0.718 [0.53–0.86] |
| DISPARAGE | 9 | 7 | 7 | 0 | 2 | 100.0% [65–100] | 77.8% [45–94] | 0.875 [0.62–1.00] |
| DATA | 7 | 6 | 5 | 1 | 2 | 83.3% [44–97] | 71.4% [36–92] | 0.769 [0.40–1.00] |
| ALCOHOL | 7 | 5 | 4 | 1 | 3 | 80.0% [38–96] | 57.1% [25–84] | 0.667 [0.25–0.92] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| BEFORE_AFTER | 0 | 3 | 0 | 3 | 0 | 0.0% [0–56] | – | 0.000 [0.00–0.00] |
| **micro** | 70 | 94 | 63 | 31 | 7 | 67.0% | 90.0% | 0.768 [0.70–0.83] |

Miss rate (a labelled item predicted with no label): 5/67 (7.5%) [3–16]. False-alarm rate (an unlabelled item given a label): 15/52 (28.8%) [18–42].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 93/94; cost $0.0099 ($0.083 per 1,000 items).

Confusion: exact 84, under-labelled 5, over-labelled 28, swapped 2.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| (no gold label) | ABSOLUTE | 11 | added to an unlabelled item |
| MEDICAL | GUARANTEE | 7 | confused |
| WEIGHT | GUARANTEE | 4 | confused |
| ALCOHOL | (no predicted label) | 3 | missed |
| (no gold label) | BEFORE_AFTER | 2 | added to an unlabelled item |
| DATA | ABSOLUTE | 2 | confused |
| DISPARAGE | (no predicted label) | 2 | missed |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |
| (no gold label) | DATA | 1 | added to an unlabelled item |
| (no gold label) | WEIGHT | 1 | added to an unlabelled item |

**Slices of 119 items.** Overall micro F1 0.768, exact match 70.6%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.721 [0.62–0.80] | 37/60 (61.7%) | 4/35 | 6/25 | -0.100 [-0.24 to +0.03] | no measured difference |
| zh | 59 | 0.821 [0.71–0.91] | 47/59 (79.7%) | 1/32 | 9/27 | +0.100 [-0.03 to +0.23] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 0.857 [0.71–1.00] | 10/13 (76.9%) | 0/8 | 1/5 | +0.102 [-0.06 to +0.25] | too few |
| written-lookalike | 12 | 0.706 [0.44–0.90] | 7/12 (58.3%) | 1/6 | 2/6 | -0.070 [-0.35 to +0.13] | too few |
| written | 48 | 0.696 [0.58–0.79] | 29/48 (60.4%) | 4/28 | 8/20 | -0.125 [-0.27 to +0.00] | no measured difference |
| video-words | 46 | 0.842 [0.73–0.94] | 38/46 (82.6%) | 0/25 | 4/21 | +0.113 [-0.03 to +0.25] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 0.851 [0.79–0.91] | 47/67 (70.1%) | 5/67 | – | -0.010 [-0.17 to +0.15] (exact match) | no measured difference |
| plain | 20 | – | 17/20 (85.0%) | – | 3/20 | +0.173 [-0.03 to +0.35] (exact match) | no measured difference |
| look-alike | 32 | – | 20/32 (62.5%) | – | 12/32 | -0.111 [-0.30 to +0.08] (exact match) | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 0.902 [0.80–0.98] | 34/39 (87.2%) | 1/22 | 4/17 | +0.194 [+0.07 to +0.31] | better |
| 49–85 chars | 40 | 0.615 [0.47–0.74] | 23/40 (57.5%) | 2/19 | 8/21 | -0.224 [-0.38 to -0.08] | worse |
| 86–299 chars | 40 | 0.787 [0.71–0.87] | 27/40 (67.5%) | 2/26 | 3/14 | +0.030 [-0.08 to +0.16] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 37/52 (71.2%) | – | 15/52 | +0.010 [-0.17 to +0.17] (exact match) | no measured difference |
| ABSOLUTE | 10 | 1.000 [1.00–1.00] | 10/10 (100.0%) | 0/10 | – | +0.271 [+0.21 to +0.34] | too few |
| ALCOHOL | 7 | 0.727 [0.25–0.92] | 4/7 (57.1%) | 3/7 | – | -0.044 [-0.48 to +0.20] | too few |
| DATA | 7 | 0.800 [0.50–1.00] | 5/7 (71.4%) | 0/7 | – | +0.036 [-0.26 to +0.26] | too few |
| DISPARAGE | 9 | 0.778 [0.56–0.94] | 6/9 (66.7%) | 2/9 | – | +0.011 [-0.22 to +0.22] | too few |
| GUARANTEE | 14 | 0.933 [0.85–1.00] | 12/14 (85.7%) | 0/14 | – | +0.202 [+0.09 to +0.31] | too few |
| MEDICAL | 18 | 0.837 [0.77–0.92] | 11/18 (61.1%) | 0/18 | – | +0.093 [-0.02 to +0.21] | too few |
| WEIGHT | 5 | 0.714 [0.67–0.83] | 1/5 (20.0%) | 0/5 | – | -0.059 [-0.15 to +0.08] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_a / prompt-rules

**ad_policy / test_a / prompt-rules: 119 items, 9 labels.** Micro F1 0.878 [0.83–0.92], macro F1 0.884 [0.80–0.94], exact match 101/119 (84.9%) [77–90].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 12 | 10 | 2 | 0 | 83.3% [55–95] | 100.0% [72–100] | 0.909 [0.75–1.00] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 24 | 14 | 10 | 0 | 58.3% [39–76] | 100.0% [78–100] | 0.737 [0.54–0.88] |
| DISPARAGE | 9 | 8 | 8 | 0 | 1 | 100.0% [68–100] | 88.9% [57–98] | 0.941 [0.77–1.00] |
| DATA | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.44–1.00] |
| ALCOHOL | 7 | 6 | 5 | 1 | 2 | 83.3% [44–97] | 71.4% [36–92] | 0.769 [0.40–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 5 | 5 | 0 | 0 | 100.0% [57–100] | 100.0% [57–100] | 1.000 [1.00–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 70 | 78 | 65 | 13 | 5 | 83.3% | 92.9% | 0.878 [0.83–0.92] |

Miss rate (a labelled item predicted with no label): 4/67 (6.0%) [2–14]. False-alarm rate (an unlabelled item given a label): 3/52 (5.8%) [2–16].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 78/78; cost $0.0121 ($0.102 per 1,000 items).

Confusion: exact 101, under-labelled 5, over-labelled 13, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| MEDICAL | GUARANTEE | 6 | confused |
| WEIGHT | GUARANTEE | 4 | confused |
| (no gold label) | ABSOLUTE | 2 | added to an unlabelled item |
| ALCOHOL | (no predicted label) | 2 | missed |
| DATA | (no predicted label) | 2 | missed |
| (no gold label) | ALCOHOL | 1 | added to an unlabelled item |
| DISPARAGE | (no predicted label) | 1 | missed |

**Slices of 119 items.** Overall micro F1 0.878, exact match 84.9%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.831 [0.76–0.90] | 47/60 (78.3%) | 3/35 | 0/25 | -0.098 [-0.19 to -0.00] | worse |
| zh | 59 | 0.930 [0.86–0.98] | 54/59 (91.5%) | 1/32 | 3/27 | +0.098 [-0.00 to +0.18] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 0.947 [0.84–1.00] | 12/13 (92.3%) | 0/8 | 0/5 | +0.079 [-0.04 to +0.17] | too few |
| written-lookalike | 12 | 0.800 [0.55–1.00] | 9/12 (75.0%) | 1/6 | 1/6 | -0.087 [-0.35 to +0.10] | too few |
| written | 48 | 0.839 [0.75–0.91] | 38/48 (79.2%) | 2/28 | 1/20 | -0.068 [-0.17 to +0.03] | no measured difference |
| video-words | 46 | 0.923 [0.85–0.98] | 42/46 (91.3%) | 1/25 | 1/21 | +0.069 [-0.03 to +0.16] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 0.897 [0.85–0.94] | 52/67 (77.6%) | 4/67 | – | -0.166 [-0.28 to -0.05] (exact match) | worse |
| plain | 20 | – | 19/20 (95.0%) | – | 1/20 | +0.122 [-0.01 to +0.23] (exact match) | no measured difference |
| look-alike | 32 | – | 30/32 (93.8%) | – | 2/32 | +0.121 [-0.01 to +0.23] (exact match) | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 0.958 [0.88–1.00] | 37/39 (94.9%) | 1/22 | 1/17 | +0.118 [+0.02 to +0.20] | better |
| 49–85 chars | 40 | 0.818 [0.71–0.91] | 32/40 (80.0%) | 1/19 | 2/21 | -0.086 [-0.20 to +0.03] | no measured difference |
| 86–299 chars | 40 | 0.857 [0.78–0.93] | 32/40 (80.0%) | 2/26 | 0/14 | -0.034 [-0.13 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 49/52 (94.2%) | – | 3/52 | +0.166 [+0.05 to +0.29] (exact match) | better |
| ABSOLUTE | 10 | 1.000 [1.00–1.00] | 10/10 (100.0%) | 0/10 | – | +0.145 [+0.09 to +0.20] | too few |
| ALCOHOL | 7 | 0.833 [0.60–1.00] | 5/7 (71.4%) | 2/7 | – | -0.049 [-0.33 to +0.14] | too few |
| DATA | 7 | 0.889 [0.71–1.00] | 5/7 (71.4%) | 1/7 | – | +0.012 [-0.18 to +0.14] | too few |
| DISPARAGE | 9 | 0.889 [0.74–1.00] | 7/9 (77.8%) | 1/9 | – | +0.012 [-0.16 to +0.14] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.150 [+0.09 to +0.21] | too few |
| MEDICAL | 18 | 0.857 [0.78–0.95] | 12/18 (66.7%) | 0/18 | – | -0.030 [-0.12 to +0.08] | too few |
| WEIGHT | 5 | 0.714 [0.67–0.83] | 1/5 (20.0%) | 0/5 | – | -0.181 [-0.27 to -0.05] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_a / agent

**ad_policy / test_a / agent: 119 items, 9 labels.** Micro F1 0.925 [0.88–0.96], macro F1 0.929 [0.86–0.97], exact match 108/119 (90.8%) [84–95].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 12 | 10 | 2 | 0 | 83.3% [55–95] | 100.0% [72–100] | 0.909 [0.74–1.00] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 19 | 14 | 5 | 0 | 73.7% [51–88] | 100.0% [78–100] | 0.848 [0.68–0.96] |
| DISPARAGE | 9 | 9 | 9 | 0 | 0 | 100.0% [70–100] | 100.0% [70–100] | 1.000 [1.00–1.00] |
| DATA | 7 | 5 | 5 | 0 | 2 | 100.0% [57–100] | 71.4% [36–92] | 0.833 [0.50–1.00] |
| ALCOHOL | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| BEFORE_AFTER | 0 | 1 | 0 | 1 | 0 | 0.0% [0–79] | – | 0.000 |
| **micro** | 70 | 77 | 68 | 9 | 2 | 88.3% | 97.1% | 0.925 [0.88–0.96] |

Miss rate (a labelled item predicted with no label): 1/67 (1.5%) [0–8]. False-alarm rate (an unlabelled item given a label): 4/52 (7.7%) [3–18].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 1.86 calls and 0.73 tool calls per item; rule gate 16, quote repair 1, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 77/77; cost $0.0286 ($0.240 per 1,000 items). Items on which each tool was called: compare_labels 1%, get_label_rules 71%.

Confusion: exact 108, under-labelled 2, over-labelled 9, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| WEIGHT | GUARANTEE | 3 | confused |
| (no gold label) | ABSOLUTE | 2 | added to an unlabelled item |
| DATA | (no predicted label) | 2 | missed |
| MEDICAL | GUARANTEE | 2 | confused |
| (no gold label) | BEFORE_AFTER | 1 | added to an unlabelled item |
| (no gold label) | WEIGHT | 1 | added to an unlabelled item |

**Slices of 119 items.** Overall micro F1 0.925, exact match 90.8%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.897 [0.84–0.96] | 52/60 (86.7%) | 0/35 | 3/25 | -0.059 [-0.14 to +0.02] | no measured difference |
| zh | 59 | 0.957 [0.90–1.00] | 56/59 (94.9%) | 1/32 | 1/27 | +0.059 [-0.02 to +0.14] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 1.000 [1.00–1.00] | 13/13 (100.0%) | 0/8 | 0/5 | +0.085 [+0.04 to +0.14] | too few |
| written-lookalike | 12 | 1.000 [1.00–1.00] | 12/12 (100.0%) | 0/6 | 0/6 | +0.083 [+0.04 to +0.13] | too few |
| written | 48 | 0.875 [0.79–0.94] | 40/48 (83.3%) | 0/28 | 3/20 | -0.089 [-0.17 to -0.01] | worse |
| video-words | 46 | 0.941 [0.86–1.00] | 43/46 (93.5%) | 1/25 | 1/21 | +0.025 [-0.07 to +0.11] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 0.951 [0.92–0.98] | 60/67 (89.6%) | 1/67 | – | -0.028 [-0.13 to +0.08] (exact match) | no measured difference |
| plain | 20 | – | 18/20 (90.0%) | – | 2/20 | -0.009 [-0.15 to +0.11] (exact match) | no measured difference |
| look-alike | 32 | – | 30/32 (93.8%) | – | 2/32 | +0.041 [-0.06 to +0.14] (exact match) | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 1.000 [1.00–1.00] | 39/39 (100.0%) | 0/22 | 0/17 | +0.111 [+0.06 to +0.17] | better |
| 49–85 chars | 40 | 0.837 [0.73–0.94] | 33/40 (82.5%) | 1/19 | 3/21 | -0.124 [-0.23 to -0.02] | worse |
| 86–299 chars | 40 | 0.929 [0.86–0.98] | 36/40 (90.0%) | 0/26 | 1/14 | +0.005 [-0.07 to +0.09] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 48/52 (92.3%) | – | 4/52 | +0.028 [-0.07 to +0.13] (exact match) | no measured difference |
| ABSOLUTE | 10 | 1.000 [1.00–1.00] | 10/10 (100.0%) | 0/10 | – | +0.089 [+0.05 to +0.14] | too few |
| ALCOHOL | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.083 [+0.04 to +0.13] | too few |
| DATA | 7 | 0.889 [0.67–1.00] | 5/7 (71.4%) | 1/7 | – | -0.041 [-0.25 to +0.08] | too few |
| DISPARAGE | 9 | 0.947 [0.86–1.00] | 8/9 (88.9%) | 0/9 | – | +0.025 [-0.08 to +0.11] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.092 [+0.05 to +0.15] | too few |
| MEDICAL | 18 | 0.947 [0.88–1.00] | 16/18 (88.9%) | 0/18 | – | +0.030 [-0.05 to +0.11] | too few |
| WEIGHT | 5 | 0.769 [0.67–0.91] | 2/5 (40.0%) | 0/5 | – | -0.171 [-0.29 to -0.02] | too few |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## ad_policy / test_a / agent-cases

**ad_policy / test_a / agent-cases: 119 items, 9 labels.** Micro F1 0.965 [0.93–0.99], macro F1 0.962 [0.91–0.99], exact match 114/119 (95.8%) [91–98].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| ABSOLUTE | 10 | 10 | 10 | 0 | 0 | 100.0% [72–100] | 100.0% [72–100] | 1.000 [1.00–1.00] |
| MEDICAL | 18 | 18 | 18 | 0 | 0 | 100.0% [82–100] | 100.0% [82–100] | 1.000 [1.00–1.00] |
| GUARANTEE | 14 | 17 | 14 | 3 | 0 | 82.4% [59–94] | 100.0% [78–100] | 0.903 [0.76–1.00] |
| DISPARAGE | 9 | 9 | 9 | 0 | 0 | 100.0% [70–100] | 100.0% [70–100] | 1.000 [1.00–1.00] |
| DATA | 7 | 6 | 6 | 0 | 1 | 100.0% [61–100] | 85.7% [49–97] | 0.923 [0.67–1.00] |
| ALCOHOL | 7 | 7 | 7 | 0 | 0 | 100.0% [65–100] | 100.0% [65–100] | 1.000 [1.00–1.00] |
| FLAG | 0 | 0 | 0 | 0 | 0 | – | – | – |
| WEIGHT | 5 | 6 | 5 | 1 | 0 | 83.3% [44–97] | 100.0% [57–100] | 0.909 [0.67–1.00] |
| BEFORE_AFTER | 0 | 0 | 0 | 0 | 0 | – | – | – |
| **micro** | 70 | 73 | 69 | 4 | 1 | 94.5% | 98.6% | 0.965 [0.93–0.99] |

Miss rate (a labelled item predicted with no label): 0/67 (0.0%) [0–5]. False-alarm rate (an unlabelled item given a label): 1/52 (1.9%) [0–10].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 119/119 answered; 1.71 calls and 0.21 tool calls per item; rule gate 63, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 73/73; cost $0.0335 ($0.281 per 1,000 items). Items on which each tool was called: compare_labels 1%, get_label_rules 18%, phrase_stats 1%, search_cases 2%.

Confusion: exact 114, under-labelled 1, over-labelled 4, swapped 0.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| WEIGHT | GUARANTEE | 3 | confused |
| (no gold label) | WEIGHT | 1 | added to an unlabelled item |
| DATA | (no predicted label) | 1 | missed |

**Slices of 119 items.** Overall micro F1 0.965, exact match 95.8%.

### By meta.lang

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| en | 60 | 0.946 [0.89–0.99] | 56/60 (93.3%) | 0/35 | 1/25 | -0.040 [-0.10 to +0.02] | no measured difference |
| zh | 59 | 0.986 [0.95–1.00] | 58/59 (98.3%) | 0/32 | 0/27 | +0.040 [-0.01 to +0.10] | no measured difference |

### By meta.source

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| written-hard | 13 | 1.000 [1.00–1.00] | 13/13 (100.0%) | 0/8 | 0/5 | +0.040 [+0.01 to +0.08] | too few |
| written-lookalike | 12 | 1.000 [1.00–1.00] | 12/12 (100.0%) | 0/6 | 0/6 | +0.039 [+0.01 to +0.07] | too few |
| written | 48 | 0.949 [0.89–1.00] | 45/48 (93.8%) | 0/28 | 1/20 | -0.027 [-0.10 to +0.03] | no measured difference |
| video-words | 46 | 0.962 [0.91–1.00] | 44/46 (95.7%) | 0/25 | 0/21 | -0.005 [-0.07 to +0.05] | no measured difference |

### By meta.difficulty

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| violating | 67 | 0.972 [0.94–0.99] | 63/67 (94.0%) | 0/67 | – | -0.040 [-0.10 to +0.02] (exact match) | no measured difference |
| plain | 20 | – | 19/20 (95.0%) | – | 1/20 | -0.010 [-0.12 to +0.07] (exact match) | no measured difference |
| look-alike | 32 | – | 32/32 (100.0%) | – | 0/32 | +0.057 [+0.01 to +0.11] (exact match) | better |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 26–48 chars | 39 | 1.000 [1.00–1.00] | 39/39 (100.0%) | 0/22 | 0/17 | +0.053 [+0.01 to +0.10] | better |
| 49–85 chars | 40 | 0.927 [0.85–1.00] | 37/40 (92.5%) | 0/19 | 1/21 | -0.054 [-0.13 to +0.02] | no measured difference |
| 86–299 chars | 40 | 0.963 [0.92–1.00] | 38/40 (95.0%) | 0/26 | 0/14 | -0.003 [-0.06 to +0.06] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 52 | – | 51/52 (98.1%) | – | 1/52 | +0.040 [-0.02 to +0.10] (exact match) | no measured difference |
| ABSOLUTE | 10 | 1.000 [1.00–1.00] | 10/10 (100.0%) | 0/10 | – | +0.042 [+0.01 to +0.08] | too few |
| ALCOHOL | 7 | 1.000 [1.00–1.00] | 7/7 (100.0%) | 0/7 | – | +0.039 [+0.01 to +0.07] | too few |
| DATA | 7 | 0.947 [0.84–1.00] | 6/7 (85.7%) | 0/7 | – | -0.020 [-0.14 to +0.06] | too few |
| DISPARAGE | 9 | 0.947 [0.86–1.00] | 8/9 (88.9%) | 0/9 | – | -0.020 [-0.13 to +0.06] | too few |
| GUARANTEE | 14 | 1.000 [1.00–1.00] | 14/14 (100.0%) | 0/14 | – | +0.043 [+0.01 to +0.08] | too few |
| MEDICAL | 18 | 1.000 [1.00–1.00] | 18/18 (100.0%) | 0/18 | – | +0.047 [+0.01 to +0.09] | too few |
| WEIGHT | 5 | 0.769 [0.67–0.91] | 2/5 (40.0%) | 0/5 | – | -0.215 [-0.32 to -0.07] | too few |

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


## asap / test_a / prompt-short

**asap / test_a / prompt-short: 201 items, 18 labels.** Micro F1 0.715 [0.70–0.73], macro F1 0.675 [0.65–0.70], exact match 6/201 (3.0%) [1–6].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 192 | 190 | 2 | 0 | 99.0% [96–100] | 100.0% [98–100] | 0.995 [0.99–1.00] |
| Food#Appearance | 54 | 80 | 38 | 42 | 16 | 47.5% [37–58] | 70.4% [57–81] | 0.567 [0.46–0.66] |
| Food#Portion | 88 | 93 | 70 | 23 | 18 | 75.3% [66–83] | 79.5% [70–87] | 0.773 [0.70–0.84] |
| Food#Recommend | 32 | 160 | 31 | 129 | 1 | 19.4% [14–26] | 96.9% [84–99] | 0.323 [0.24–0.41] |
| Price#Level | 94 | 60 | 52 | 8 | 42 | 86.7% [76–93] | 55.3% [45–65] | 0.675 [0.59–0.76] |
| Price#Cost_effective | 41 | 106 | 38 | 68 | 3 | 35.8% [27–45] | 92.7% [81–97] | 0.517 [0.41–0.60] |
| Price#Discount | 73 | 40 | 31 | 9 | 42 | 77.5% [62–88] | 42.5% [32–54] | 0.549 [0.43–0.65] |
| Location#Downtown | 39 | 27 | 12 | 15 | 27 | 44.4% [28–63] | 30.8% [19–46] | 0.364 [0.20–0.51] |
| Location#Transportation | 52 | 49 | 41 | 8 | 11 | 83.7% [71–91] | 78.8% [66–88] | 0.812 [0.72–0.89] |
| Location#Easy_to_find | 47 | 41 | 33 | 8 | 14 | 80.5% [66–90] | 70.2% [56–81] | 0.750 [0.64–0.84] |
| Service#Queue | 35 | 49 | 31 | 18 | 4 | 63.3% [49–75] | 88.6% [74–95] | 0.738 [0.62–0.84] |
| Service#Hospitality | 111 | 114 | 103 | 11 | 8 | 90.4% [84–95] | 92.8% [86–96] | 0.916 [0.88–0.95] |
| Service#Parking | 12 | 11 | 9 | 2 | 3 | 81.8% [52–95] | 75.0% [47–91] | 0.783 [0.53–0.95] |
| Service#Timely | 28 | 55 | 27 | 28 | 1 | 49.1% [36–62] | 96.4% [82–99] | 0.651 [0.52–0.76] |
| Ambience#Decoration | 90 | 94 | 81 | 13 | 9 | 86.2% [78–92] | 90.0% [82–95] | 0.880 [0.83–0.93] |
| Ambience#Noise | 64 | 35 | 26 | 9 | 38 | 74.3% [58–86] | 40.6% [29–53] | 0.525 [0.40–0.64] |
| Ambience#Space | 76 | 72 | 51 | 21 | 25 | 70.8% [59–80] | 67.1% [56–77] | 0.689 [0.60–0.77] |
| Ambience#Sanitary | 71 | 52 | 40 | 12 | 31 | 76.9% [64–86] | 56.3% [45–67] | 0.650 [0.55–0.74] |
| **micro** | 1197 | 1330 | 904 | 426 | 293 | 68.0% | 75.5% | 0.715 [0.70–0.73] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1303/1330; cost $0.0416 ($0.207 per 1,000 items).

Confusion: exact 6, under-labelled 10, over-labelled 47, swapped 138.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | Food#Recommend | 32 | confused |
| Ambience#Sanitary | Food#Recommend | 30 | confused |
| Price#Discount | Food#Recommend | 29 | confused |
| Price#Level | Price#Cost_effective | 27 | confused |
| Ambience#Noise | Food#Recommend | 26 | confused |
| Food#Taste | Food#Recommend | 26 | confused |
| Location#Downtown | Food#Recommend | 23 | confused |
| Food#Portion | Food#Recommend | 21 | confused |
| Ambience#Space | Food#Recommend | 20 | confused |
| Service#Hospitality | Food#Recommend | 16 | confused |

**Slices of 201 items.** Overall micro F1 0.715, exact match 3.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.724 [0.69–0.76] | 1/37 (2.7%) | 0/37 | – | +0.011 [-0.03 to +0.06] | no measured difference |
| 4-5 stars | 164 | 0.713 [0.69–0.73] | 5/164 (3.0%) | 0/162 | 0/2 | -0.011 [-0.05 to +0.04] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.754 [0.73–0.78] | 0/56 (0.0%) | 0/56 | – | +0.064 [+0.03 to +0.10] | better |
| 5-7 labels | 79 | 0.711 [0.69–0.74] | 1/79 (1.3%) | 0/79 | – | -0.007 [-0.04 to +0.03] | no measured difference |
| 1-4 labels | 66 | 0.647 [0.61–0.69] | 5/66 (7.6%) | 0/64 | 0/2 | -0.086 [-0.13 to -0.04] | worse |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.717 [0.70–0.74] | 3/148 (2.0%) | 0/148 | – | +0.007 [-0.03 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.710 [0.67–0.74] | 3/53 (5.7%) | 0/51 | 0/2 | -0.007 [-0.05 to +0.03] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.721 [0.69–0.75] | 4/67 (6.0%) | 0/65 | 0/2 | +0.008 [-0.03 to +0.05] | no measured difference |
| 236–314 chars | 67 | 0.708 [0.68–0.74] | 1/67 (1.5%) | 0/67 | – | -0.011 [-0.05 to +0.03] | no measured difference |
| 315–946 chars | 67 | 0.718 [0.69–0.75] | 1/67 (1.5%) | 0/67 | – | +0.003 [-0.03 to +0.04] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.980 [+0.96 to +0.99] (exact match) | too few |
| Ambience#Decoration | 90 | 0.735 [0.71–0.76] | 1/90 (1.1%) | 0/90 | – | +0.044 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.724 [0.70–0.75] | 0/64 (0.0%) | 0/64 | – | +0.015 [-0.02 to +0.05] | no measured difference |
| Ambience#Sanitary | 71 | 0.735 [0.71–0.76] | 0/71 (0.0%) | 0/71 | – | +0.035 [-0.00 to +0.07] | no measured difference |
| Ambience#Space | 76 | 0.737 [0.72–0.76] | 0/76 (0.0%) | 0/76 | – | +0.042 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.732 [0.70–0.76] | 2/54 (3.7%) | 0/54 | – | +0.025 [-0.01 to +0.06] | no measured difference |
| Food#Portion | 88 | 0.731 [0.71–0.76] | 1/88 (1.1%) | 0/88 | – | +0.030 [-0.00 to +0.06] | no measured difference |
| Food#Recommend | 32 | 0.804 [0.77–0.84] | 3/32 (9.4%) | 0/32 | – | +0.108 [+0.07 to +0.15] | better |
| Food#Taste | 190 | 0.715 [0.70–0.73] | 3/190 (1.6%) | 0/190 | – | -0.016 [-0.11 to +0.09] | no measured difference |
| Location#Downtown | 39 | 0.687 [0.65–0.72] | 0/39 (0.0%) | 0/39 | – | -0.038 [-0.07 to +0.00] | no measured difference |
| Location#Easy_to_find | 47 | 0.743 [0.71–0.78] | 1/47 (2.1%) | 0/47 | – | +0.040 [-0.00 to +0.08] | no measured difference |
| Location#Transportation | 52 | 0.730 [0.70–0.76] | 1/52 (1.9%) | 0/52 | – | +0.022 [-0.02 to +0.06] | no measured difference |
| Price#Cost_effective | 41 | 0.754 [0.72–0.79] | 0/41 (0.0%) | 0/41 | – | +0.050 [+0.01 to +0.09] | better |
| Price#Discount | 73 | 0.722 [0.70–0.75] | 0/73 (0.0%) | 0/73 | – | +0.011 [-0.02 to +0.05] | no measured difference |
| Price#Level | 94 | 0.703 [0.68–0.73] | 2/94 (2.1%) | 0/94 | – | -0.025 [-0.06 to +0.01] | no measured difference |
| Service#Hospitality | 111 | 0.728 [0.71–0.75] | 1/111 (0.9%) | 0/111 | – | +0.034 [+0.00 to +0.07] | better |
| Service#Parking | 12 | 0.728 [0.68–0.78] | 0/12 (0.0%) | 0/12 | – | +0.014 [-0.03 to +0.07] | too few |
| Service#Queue | 35 | 0.718 [0.68–0.75] | 1/35 (2.9%) | 0/35 | – | +0.004 [-0.04 to +0.05] | no measured difference |
| Service#Timely | 28 | 0.752 [0.72–0.78] | 0/28 (0.0%) | 0/28 | – | +0.044 [+0.01 to +0.08] | better |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / prompt-rules

**asap / test_a / prompt-rules: 201 items, 18 labels.** Micro F1 0.782 [0.76–0.80], macro F1 0.750 [0.72–0.77], exact match 16/201 (8.0%) [5–13].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 195 | 190 | 5 | 0 | 97.4% [94–99] | 100.0% [98–100] | 0.987 [0.97–1.00] |
| Food#Appearance | 54 | 90 | 41 | 49 | 13 | 45.6% [36–56] | 75.9% [63–85] | 0.569 [0.47–0.66] |
| Food#Portion | 88 | 90 | 69 | 21 | 19 | 76.7% [67–84] | 78.4% [69–86] | 0.775 [0.71–0.84] |
| Food#Recommend | 32 | 109 | 29 | 80 | 3 | 26.6% [19–36] | 90.6% [76–97] | 0.411 [0.31–0.51] |
| Price#Level | 94 | 80 | 70 | 10 | 24 | 87.5% [78–93] | 74.5% [65–82] | 0.805 [0.74–0.87] |
| Price#Cost_effective | 41 | 100 | 39 | 61 | 2 | 39.0% [30–49] | 95.1% [84–99] | 0.553 [0.45–0.64] |
| Price#Discount | 73 | 75 | 61 | 14 | 12 | 81.3% [71–89] | 83.6% [73–90] | 0.824 [0.75–0.89] |
| Location#Downtown | 39 | 44 | 26 | 18 | 13 | 59.1% [44–72] | 66.7% [51–79] | 0.627 [0.49–0.75] |
| Location#Transportation | 52 | 52 | 44 | 8 | 8 | 84.6% [72–92] | 84.6% [72–92] | 0.846 [0.76–0.91] |
| Location#Easy_to_find | 47 | 53 | 39 | 14 | 8 | 73.6% [60–84] | 83.0% [70–91] | 0.780 [0.68–0.87] |
| Service#Queue | 35 | 55 | 31 | 24 | 4 | 56.4% [43–69] | 88.6% [74–95] | 0.689 [0.57–0.79] |
| Service#Hospitality | 111 | 119 | 105 | 14 | 6 | 88.2% [81–93] | 94.6% [89–97] | 0.913 [0.88–0.95] |
| Service#Parking | 12 | 13 | 10 | 3 | 2 | 76.9% [50–92] | 83.3% [55–95] | 0.800 [0.59–0.95] |
| Service#Timely | 28 | 44 | 26 | 18 | 2 | 59.1% [44–72] | 92.9% [77–98] | 0.722 [0.59–0.83] |
| Ambience#Decoration | 90 | 97 | 81 | 16 | 9 | 83.5% [75–90] | 90.0% [82–95] | 0.866 [0.81–0.91] |
| Ambience#Noise | 64 | 50 | 44 | 6 | 20 | 88.0% [76–94] | 68.8% [57–79] | 0.772 [0.68–0.85] |
| Ambience#Space | 76 | 89 | 64 | 25 | 12 | 71.9% [62–80] | 84.2% [74–91] | 0.776 [0.70–0.84] |
| Ambience#Sanitary | 71 | 66 | 54 | 12 | 17 | 81.8% [71–89] | 76.1% [65–84] | 0.788 [0.71–0.86] |
| **micro** | 1197 | 1421 | 1023 | 398 | 174 | 72.0% | 85.5% | 0.782 [0.76–0.80] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 1.00 calls and 0.00 tool calls per item; rule gate 0, quote repair 0, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1385/1421; cost $0.0505 ($0.251 per 1,000 items).

Confusion: exact 16, under-labelled 13, over-labelled 85, swapped 87.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Food#Taste | Food#Recommend | 36 | confused |
| Food#Taste | Food#Appearance | 26 | confused |
| Food#Taste | Price#Cost_effective | 26 | confused |
| Price#Level | Price#Cost_effective | 25 | confused |
| Price#Level | Food#Recommend | 21 | confused |
| Food#Portion | Food#Recommend | 20 | confused |
| Price#Level | Food#Appearance | 20 | confused |
| Food#Portion | Price#Cost_effective | 19 | confused |
| Ambience#Sanitary | Food#Recommend | 18 | confused |
| Price#Discount | Food#Recommend | 17 | confused |

**Slices of 201 items.** Overall micro F1 0.782, exact match 8.0%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.741 [0.70–0.77] | 2/37 (5.4%) | 0/37 | – | -0.050 [-0.09 to -0.01] | worse |
| 4-5 stars | 164 | 0.791 [0.77–0.81] | 14/164 (8.5%) | 0/162 | 0/2 | +0.050 [+0.01 to +0.09] | better |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.818 [0.79–0.84] | 4/56 (7.1%) | 0/56 | – | +0.062 [+0.03 to +0.10] | better |
| 5-7 labels | 79 | 0.774 [0.75–0.80] | 5/79 (6.3%) | 0/79 | – | -0.013 [-0.05 to +0.02] | no measured difference |
| 1-4 labels | 66 | 0.720 [0.69–0.75] | 7/66 (10.6%) | 0/64 | 0/2 | -0.076 [-0.11 to -0.04] | worse |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.783 [0.76–0.80] | 10/148 (6.8%) | 0/148 | – | +0.007 [-0.03 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.776 [0.74–0.81] | 6/53 (11.3%) | 0/51 | 0/2 | -0.007 [-0.05 to +0.03] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.797 [0.76–0.83] | 11/67 (16.4%) | 0/65 | 0/2 | +0.021 [-0.02 to +0.06] | no measured difference |
| 236–314 chars | 67 | 0.768 [0.74–0.79] | 4/67 (6.0%) | 0/67 | – | -0.019 [-0.05 to +0.01] | no measured difference |
| 315–946 chars | 67 | 0.782 [0.76–0.80] | 1/67 (1.5%) | 0/67 | – | +0.000 [-0.03 to +0.03] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.930 [+0.89 to +0.96] (exact match) | too few |
| Ambience#Decoration | 90 | 0.803 [0.78–0.83] | 7/90 (7.8%) | 0/90 | – | +0.049 [+0.02 to +0.08] | better |
| Ambience#Noise | 64 | 0.801 [0.77–0.83] | 3/64 (4.7%) | 0/64 | – | +0.034 [-0.00 to +0.07] | no measured difference |
| Ambience#Sanitary | 71 | 0.805 [0.78–0.83] | 4/71 (5.6%) | 0/71 | – | +0.042 [+0.01 to +0.08] | better |
| Ambience#Space | 76 | 0.811 [0.79–0.83] | 5/76 (6.6%) | 0/76 | – | +0.058 [+0.03 to +0.09] | better |
| Food#Appearance | 54 | 0.785 [0.76–0.81] | 3/54 (5.6%) | 0/54 | – | +0.006 [-0.03 to +0.04] | no measured difference |
| Food#Portion | 88 | 0.780 [0.76–0.80] | 3/88 (3.4%) | 0/88 | – | -0.003 [-0.04 to +0.03] | no measured difference |
| Food#Recommend | 32 | 0.846 [0.81–0.88] | 4/32 (12.5%) | 0/32 | – | +0.078 [+0.04 to +0.12] | better |
| Food#Taste | 190 | 0.786 [0.77–0.80] | 13/190 (6.8%) | 0/190 | – | +0.119 [+0.01 to +0.24] | better |
| Location#Downtown | 39 | 0.776 [0.74–0.81] | 4/39 (10.3%) | 0/39 | – | -0.007 [-0.05 to +0.03] | no measured difference |
| Location#Easy_to_find | 47 | 0.812 [0.78–0.84] | 5/47 (10.6%) | 0/47 | – | +0.044 [+0.01 to +0.08] | better |
| Location#Transportation | 52 | 0.798 [0.77–0.83] | 5/52 (9.6%) | 0/52 | – | +0.023 [-0.01 to +0.06] | no measured difference |
| Price#Cost_effective | 41 | 0.823 [0.79–0.86] | 4/41 (9.8%) | 0/41 | – | +0.055 [+0.02 to +0.09] | better |
| Price#Discount | 73 | 0.793 [0.77–0.82] | 4/73 (5.5%) | 0/73 | – | +0.020 [-0.01 to +0.05] | no measured difference |
| Price#Level | 94 | 0.766 [0.74–0.79] | 3/94 (3.2%) | 0/94 | – | -0.034 [-0.07 to -0.00] | worse |
| Service#Hospitality | 111 | 0.794 [0.77–0.81] | 8/111 (7.2%) | 0/111 | – | +0.032 [-0.01 to +0.07] | no measured difference |
| Service#Parking | 12 | 0.780 [0.69–0.85] | 0/12 (0.0%) | 0/12 | – | -0.001 [-0.10 to +0.07] | too few |
| Service#Queue | 35 | 0.779 [0.74–0.82] | 2/35 (5.7%) | 0/35 | – | -0.004 [-0.05 to +0.04] | no measured difference |
| Service#Timely | 28 | 0.769 [0.73–0.80] | 0/28 (0.0%) | 0/28 | – | -0.016 [-0.06 to +0.02] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / agent

**asap / test_a / agent: 201 items, 18 labels.** Micro F1 0.799 [0.78–0.82], macro F1 0.756 [0.73–0.78], exact match 21/201 (10.4%) [7–15].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 192 | 189 | 3 | 1 | 98.4% [96–99] | 99.5% [97–100] | 0.990 [0.98–1.00] |
| Food#Appearance | 54 | 40 | 31 | 9 | 23 | 77.5% [62–88] | 57.4% [44–70] | 0.660 [0.54–0.77] |
| Food#Portion | 88 | 81 | 64 | 17 | 24 | 79.0% [69–86] | 72.7% [63–81] | 0.757 [0.68–0.83] |
| Food#Recommend | 32 | 57 | 27 | 30 | 5 | 47.4% [35–60] | 84.4% [68–93] | 0.607 [0.47–0.72] |
| Price#Level | 94 | 60 | 53 | 7 | 41 | 88.3% [78–94] | 56.4% [46–66] | 0.688 [0.60–0.77] |
| Price#Cost_effective | 41 | 81 | 38 | 43 | 3 | 46.9% [36–58] | 92.7% [81–97] | 0.623 [0.51–0.71] |
| Price#Discount | 73 | 46 | 38 | 8 | 35 | 82.6% [69–91] | 52.1% [41–63] | 0.639 [0.53–0.74] |
| Location#Downtown | 39 | 15 | 9 | 6 | 30 | 60.0% [36–80] | 23.1% [13–38] | 0.333 [0.16–0.49] |
| Location#Transportation | 52 | 43 | 39 | 4 | 13 | 90.7% [78–96] | 75.0% [62–85] | 0.821 [0.72–0.90] |
| Location#Easy_to_find | 47 | 44 | 36 | 8 | 11 | 81.8% [68–90] | 76.6% [63–86] | 0.791 [0.69–0.88] |
| Service#Queue | 35 | 34 | 27 | 7 | 8 | 79.4% [63–90] | 77.1% [61–88] | 0.783 [0.66–0.88] |
| Service#Hospitality | 111 | 107 | 98 | 9 | 13 | 91.6% [85–96] | 88.3% [81–93] | 0.899 [0.85–0.94] |
| Service#Parking | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| Service#Timely | 28 | 30 | 24 | 6 | 4 | 80.0% [63–90] | 85.7% [69–94] | 0.828 [0.70–0.92] |
| Ambience#Decoration | 90 | 88 | 80 | 8 | 10 | 90.9% [83–95] | 88.9% [81–94] | 0.899 [0.85–0.94] |
| Ambience#Noise | 64 | 45 | 44 | 1 | 20 | 97.8% [88–100] | 68.8% [57–79] | 0.807 [0.72–0.88] |
| Ambience#Space | 76 | 71 | 59 | 12 | 17 | 83.1% [73–90] | 77.6% [67–86] | 0.803 [0.73–0.87] |
| Ambience#Sanitary | 71 | 57 | 52 | 5 | 19 | 91.2% [81–96] | 73.2% [62–82] | 0.812 [0.73–0.88] |
| **micro** | 1197 | 1102 | 918 | 184 | 279 | 83.3% | 76.7% | 0.799 [0.78–0.82] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 2.14 calls and 0.39 tool calls per item; rule gate 137, quote repair 14, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1100/1102; cost $0.1447 ($0.720 per 1,000 items). Items on which each tool was called: compare_labels 0%, get_label_rules 39%.

Confusion: exact 21, under-labelled 61, over-labelled 38, swapped 81.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Level | Price#Cost_effective | 20 | confused |
| Price#Discount | (no predicted label) | 15 | missed |
| Price#Level | (no predicted label) | 13 | missed |
| Food#Portion | (no predicted label) | 12 | missed |
| Location#Downtown | (no predicted label) | 12 | missed |
| Food#Appearance | (no predicted label) | 11 | missed |
| Service#Hospitality | Price#Cost_effective | 11 | confused |
| Ambience#Space | (no predicted label) | 10 | missed |
| Food#Taste | Price#Cost_effective | 10 | confused |
| Price#Discount | Food#Recommend | 10 | confused |

**Slices of 201 items.** Overall micro F1 0.799, exact match 10.4%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.773 [0.73–0.81] | 1/37 (2.7%) | 0/37 | – | -0.031 [-0.08 to +0.01] | no measured difference |
| 4-5 stars | 164 | 0.804 [0.78–0.82] | 20/164 (12.2%) | 0/162 | 0/2 | +0.031 [-0.01 to +0.08] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.814 [0.79–0.84] | 2/56 (3.6%) | 0/56 | – | +0.027 [-0.01 to +0.06] | no measured difference |
| 5-7 labels | 79 | 0.796 [0.77–0.82] | 8/79 (10.1%) | 0/79 | – | -0.004 [-0.04 to +0.03] | no measured difference |
| 1-4 labels | 66 | 0.767 [0.73–0.81] | 11/66 (16.7%) | 0/64 | 0/2 | -0.038 [-0.08 to +0.00] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.800 [0.78–0.82] | 13/148 (8.8%) | 0/148 | – | +0.008 [-0.03 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.792 [0.76–0.83] | 8/53 (15.1%) | 0/51 | 0/2 | -0.008 [-0.05 to +0.04] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.817 [0.78–0.85] | 13/67 (19.4%) | 0/65 | 0/2 | +0.026 [-0.02 to +0.07] | no measured difference |
| 236–314 chars | 67 | 0.769 [0.74–0.80] | 5/67 (7.5%) | 0/67 | – | -0.044 [-0.08 to -0.01] | worse |
| 315–946 chars | 67 | 0.810 [0.78–0.84] | 3/67 (4.5%) | 0/67 | – | +0.018 [-0.02 to +0.05] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.905 [+0.86 to +0.94] (exact match) | too few |
| Ambience#Decoration | 90 | 0.816 [0.79–0.84] | 7/90 (7.8%) | 0/90 | – | +0.041 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.812 [0.78–0.84] | 4/64 (6.2%) | 0/64 | – | +0.025 [-0.01 to +0.06] | no measured difference |
| Ambience#Sanitary | 71 | 0.821 [0.79–0.85] | 7/71 (9.9%) | 0/71 | – | +0.041 [+0.01 to +0.08] | better |
| Ambience#Space | 76 | 0.824 [0.80–0.85] | 6/76 (7.9%) | 0/76 | – | +0.050 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.781 [0.75–0.81] | 2/54 (3.7%) | 0/54 | – | -0.025 [-0.06 to +0.01] | no measured difference |
| Food#Portion | 88 | 0.805 [0.78–0.83] | 6/88 (6.8%) | 0/88 | – | +0.012 [-0.02 to +0.05] | no measured difference |
| Food#Recommend | 32 | 0.856 [0.82–0.89] | 5/32 (15.6%) | 0/32 | – | +0.071 [+0.03 to +0.11] | better |
| Food#Taste | 190 | 0.803 [0.78–0.82] | 18/190 (9.5%) | 0/190 | – | +0.137 [+0.03 to +0.26] | better |
| Location#Downtown | 39 | 0.759 [0.72–0.79] | 0/39 (0.0%) | 0/39 | – | -0.052 [-0.10 to -0.01] | worse |
| Location#Easy_to_find | 47 | 0.812 [0.77–0.85] | 4/47 (8.5%) | 0/47 | – | +0.018 [-0.02 to +0.06] | no measured difference |
| Location#Transportation | 52 | 0.805 [0.77–0.84] | 5/52 (9.6%) | 0/52 | – | +0.009 [-0.03 to +0.05] | no measured difference |
| Price#Cost_effective | 41 | 0.816 [0.78–0.85] | 6/41 (14.6%) | 0/41 | – | +0.023 [-0.02 to +0.06] | no measured difference |
| Price#Discount | 73 | 0.798 [0.77–0.82] | 3/73 (4.1%) | 0/73 | – | -0.000 [-0.03 to +0.04] | no measured difference |
| Price#Level | 94 | 0.782 [0.76–0.81] | 9/94 (9.6%) | 0/94 | – | -0.035 [-0.07 to +0.00] | no measured difference |
| Service#Hospitality | 111 | 0.802 [0.78–0.82] | 6/111 (5.4%) | 0/111 | – | +0.010 [-0.03 to +0.05] | no measured difference |
| Service#Parking | 12 | 0.762 [0.68–0.84] | 0/12 (0.0%) | 0/12 | – | -0.040 [-0.12 to +0.04] | too few |
| Service#Queue | 35 | 0.785 [0.74–0.83] | 2/35 (5.7%) | 0/35 | – | -0.017 [-0.07 to +0.03] | no measured difference |
| Service#Timely | 28 | 0.787 [0.74–0.83] | 0/28 (0.0%) | 0/28 | – | -0.014 [-0.06 to +0.03] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / agent-cases

**asap / test_a / agent-cases: 201 items, 18 labels.** Micro F1 0.812 [0.79–0.83], macro F1 0.776 [0.75–0.80], exact match 28/201 (13.9%) [10–19].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 191 | 189 | 2 | 1 | 99.0% [96–100] | 99.5% [97–100] | 0.992 [0.98–1.00] |
| Food#Appearance | 54 | 39 | 29 | 10 | 25 | 74.4% [59–85] | 53.7% [41–66] | 0.624 [0.49–0.73] |
| Food#Portion | 88 | 77 | 63 | 14 | 25 | 81.8% [72–89] | 71.6% [61–80] | 0.764 [0.68–0.83] |
| Food#Recommend | 32 | 44 | 25 | 19 | 7 | 56.8% [42–70] | 78.1% [61–89] | 0.658 [0.53–0.77] |
| Price#Level | 94 | 62 | 56 | 6 | 38 | 90.3% [80–95] | 59.6% [49–69] | 0.718 [0.63–0.79] |
| Price#Cost_effective | 41 | 73 | 39 | 34 | 2 | 53.4% [42–64] | 95.1% [84–99] | 0.684 [0.57–0.77] |
| Price#Discount | 73 | 47 | 40 | 7 | 33 | 85.1% [72–93] | 54.8% [43–66] | 0.667 [0.56–0.76] |
| Location#Downtown | 39 | 17 | 13 | 4 | 26 | 76.5% [53–90] | 33.3% [21–49] | 0.464 [0.29–0.62] |
| Location#Transportation | 52 | 44 | 40 | 4 | 12 | 90.9% [79–96] | 76.9% [64–86] | 0.833 [0.75–0.91] |
| Location#Easy_to_find | 47 | 39 | 34 | 5 | 13 | 87.2% [73–94] | 72.3% [58–83] | 0.791 [0.68–0.88] |
| Service#Queue | 35 | 35 | 28 | 7 | 7 | 80.0% [64–90] | 80.0% [64–90] | 0.800 [0.67–0.89] |
| Service#Hospitality | 111 | 107 | 96 | 11 | 15 | 89.7% [83–94] | 86.5% [79–92] | 0.881 [0.83–0.92] |
| Service#Parking | 12 | 12 | 11 | 1 | 1 | 91.7% [65–99] | 91.7% [65–99] | 0.917 [0.77–1.00] |
| Service#Timely | 28 | 29 | 23 | 6 | 5 | 79.3% [62–90] | 82.1% [64–92] | 0.807 [0.67–0.91] |
| Ambience#Decoration | 90 | 90 | 79 | 11 | 11 | 87.8% [79–93] | 87.8% [79–93] | 0.878 [0.82–0.93] |
| Ambience#Noise | 64 | 47 | 46 | 1 | 18 | 97.9% [89–100] | 71.9% [60–81] | 0.829 [0.74–0.90] |
| Ambience#Space | 76 | 73 | 60 | 13 | 16 | 82.2% [72–89] | 78.9% [69–87] | 0.805 [0.73–0.87] |
| Ambience#Sanitary | 71 | 62 | 57 | 5 | 14 | 91.9% [82–97] | 80.3% [70–88] | 0.857 [0.79–0.91] |
| **micro** | 1197 | 1088 | 928 | 160 | 269 | 85.3% | 77.5% | 0.812 [0.79–0.83] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 2.13 calls and 0.01 tool calls per item; rule gate 198, quote repair 27, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1087/1088; cost $0.1836 ($0.914 per 1,000 items). Items on which each tool was called: get_label_rules 1%.

Confusion: exact 28, under-labelled 70, over-labelled 34, swapped 69.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Discount | (no predicted label) | 20 | missed |
| Price#Level | (no predicted label) | 16 | missed |
| Price#Level | Price#Cost_effective | 16 | confused |
| Food#Appearance | (no predicted label) | 15 | missed |
| Food#Portion | (no predicted label) | 13 | missed |
| Food#Taste | Price#Cost_effective | 12 | confused |
| Location#Downtown | (no predicted label) | 11 | missed |
| Ambience#Space | (no predicted label) | 10 | missed |
| Service#Hospitality | Price#Cost_effective | 10 | confused |
| Ambience#Decoration | (no predicted label) | 7 | missed |

**Slices of 201 items.** Overall micro F1 0.812, exact match 13.9%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.787 [0.75–0.82] | 2/37 (5.4%) | 0/37 | – | -0.031 [-0.08 to +0.01] | no measured difference |
| 4-5 stars | 164 | 0.818 [0.80–0.84] | 26/164 (15.9%) | 0/162 | 0/2 | +0.031 [-0.01 to +0.08] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.828 [0.80–0.86] | 4/56 (7.1%) | 0/56 | – | +0.028 [-0.01 to +0.07] | no measured difference |
| 5-7 labels | 79 | 0.805 [0.78–0.83] | 8/79 (10.1%) | 0/79 | – | -0.013 [-0.05 to +0.02] | no measured difference |
| 1-4 labels | 66 | 0.791 [0.76–0.83] | 16/66 (24.2%) | 0/64 | 0/2 | -0.025 [-0.07 to +0.02] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.821 [0.80–0.84] | 22/148 (14.9%) | 0/148 | – | +0.040 [+0.00 to +0.09] | better |
| no neutral mention | 53 | 0.781 [0.74–0.82] | 6/53 (11.3%) | 0/51 | 0/2 | -0.040 [-0.08 to +0.00] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.837 [0.80–0.87] | 16/67 (23.9%) | 0/65 | 0/2 | +0.034 [-0.01 to +0.07] | no measured difference |
| 236–314 chars | 67 | 0.784 [0.75–0.81] | 6/67 (9.0%) | 0/67 | – | -0.041 [-0.08 to -0.00] | worse |
| 315–946 chars | 67 | 0.817 [0.79–0.84] | 6/67 (9.0%) | 0/67 | – | +0.008 [-0.03 to +0.04] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.869 [+0.82 to +0.91] (exact match) | too few |
| Ambience#Decoration | 90 | 0.833 [0.81–0.86] | 13/90 (14.4%) | 0/90 | – | +0.048 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.827 [0.80–0.86] | 8/64 (12.5%) | 0/64 | – | +0.028 [-0.01 to +0.06] | no measured difference |
| Ambience#Sanitary | 71 | 0.840 [0.81–0.87] | 11/71 (15.5%) | 0/71 | – | +0.051 [+0.02 to +0.09] | better |
| Ambience#Space | 76 | 0.835 [0.81–0.86] | 9/76 (11.8%) | 0/76 | – | +0.046 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.792 [0.76–0.82] | 3/54 (5.6%) | 0/54 | – | -0.030 [-0.07 to +0.01] | no measured difference |
| Food#Portion | 88 | 0.812 [0.79–0.84] | 8/88 (9.1%) | 0/88 | – | -0.001 [-0.04 to +0.03] | no measured difference |
| Food#Recommend | 32 | 0.843 [0.80–0.88] | 3/32 (9.4%) | 0/32 | – | +0.037 [-0.01 to +0.08] | no measured difference |
| Food#Taste | 190 | 0.816 [0.80–0.84] | 25/190 (13.2%) | 0/190 | – | +0.109 [+0.02 to +0.23] | better |
| Location#Downtown | 39 | 0.777 [0.74–0.81] | 2/39 (5.1%) | 0/39 | – | -0.047 [-0.09 to -0.00] | worse |
| Location#Easy_to_find | 47 | 0.817 [0.78–0.85] | 4/47 (8.5%) | 0/47 | – | +0.007 [-0.03 to +0.05] | no measured difference |
| Location#Transportation | 52 | 0.804 [0.77–0.84] | 4/52 (7.7%) | 0/52 | – | -0.011 [-0.05 to +0.03] | no measured difference |
| Price#Cost_effective | 41 | 0.828 [0.79–0.87] | 6/41 (14.6%) | 0/41 | – | +0.020 [-0.02 to +0.06] | no measured difference |
| Price#Discount | 73 | 0.811 [0.78–0.84] | 4/73 (5.5%) | 0/73 | – | -0.001 [-0.04 to +0.03] | no measured difference |
| Price#Level | 94 | 0.793 [0.77–0.82] | 10/94 (10.6%) | 0/94 | – | -0.040 [-0.07 to -0.01] | worse |
| Service#Hospitality | 111 | 0.825 [0.80–0.85] | 13/111 (11.7%) | 0/111 | – | +0.034 [-0.00 to +0.07] | no measured difference |
| Service#Parking | 12 | 0.774 [0.70–0.85] | 0/12 (0.0%) | 0/12 | – | -0.042 [-0.12 to +0.03] | too few |
| Service#Queue | 35 | 0.807 [0.77–0.84] | 3/35 (8.6%) | 0/35 | – | -0.007 [-0.05 to +0.04] | no measured difference |
| Service#Timely | 28 | 0.774 [0.73–0.82] | 0/28 (0.0%) | 0/28 | – | -0.046 [-0.09 to +0.00] | no measured difference |

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


## asap / test_a / agent-cases-synthetic

**asap / test_a / agent-cases-synthetic: 201 items, 18 labels.** Micro F1 0.802 [0.78–0.82], macro F1 0.761 [0.73–0.78], exact match 28/201 (13.9%) [10–19].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 193 | 189 | 4 | 1 | 97.9% [95–99] | 99.5% [97–100] | 0.987 [0.97–1.00] |
| Food#Appearance | 54 | 35 | 29 | 6 | 25 | 82.9% [67–92] | 53.7% [41–66] | 0.652 [0.52–0.76] |
| Food#Portion | 88 | 73 | 61 | 12 | 27 | 83.6% [73–90] | 69.3% [59–78] | 0.758 [0.68–0.83] |
| Food#Recommend | 32 | 43 | 25 | 18 | 7 | 58.1% [43–72] | 78.1% [61–89] | 0.667 [0.53–0.78] |
| Price#Level | 94 | 59 | 55 | 4 | 39 | 93.2% [84–97] | 58.5% [48–68] | 0.719 [0.64–0.79] |
| Price#Cost_effective | 41 | 77 | 39 | 38 | 2 | 50.6% [40–62] | 95.1% [84–99] | 0.661 [0.55–0.75] |
| Price#Discount | 73 | 43 | 37 | 6 | 36 | 86.0% [73–93] | 50.7% [39–62] | 0.638 [0.53–0.73] |
| Location#Downtown | 39 | 17 | 12 | 5 | 27 | 70.6% [47–87] | 30.8% [19–46] | 0.429 [0.26–0.58] |
| Location#Transportation | 52 | 40 | 37 | 3 | 15 | 92.5% [80–97] | 71.2% [58–82] | 0.804 [0.70–0.88] |
| Location#Easy_to_find | 47 | 43 | 35 | 8 | 12 | 81.4% [67–90] | 74.5% [60–85] | 0.778 [0.67–0.86] |
| Service#Queue | 35 | 36 | 28 | 8 | 7 | 77.8% [62–88] | 80.0% [64–90] | 0.789 [0.68–0.88] |
| Service#Hospitality | 111 | 106 | 98 | 8 | 13 | 92.5% [86–96] | 88.3% [81–93] | 0.903 [0.86–0.94] |
| Service#Parking | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| Service#Timely | 28 | 31 | 24 | 7 | 4 | 77.4% [60–89] | 85.7% [69–94] | 0.814 [0.69–0.91] |
| Ambience#Decoration | 90 | 86 | 76 | 10 | 14 | 88.4% [80–94] | 84.4% [76–91] | 0.864 [0.81–0.92] |
| Ambience#Noise | 64 | 46 | 42 | 4 | 22 | 91.3% [80–97] | 65.6% [53–76] | 0.764 [0.67–0.85] |
| Ambience#Space | 76 | 74 | 62 | 12 | 14 | 83.8% [74–90] | 81.6% [71–89] | 0.827 [0.75–0.89] |
| Ambience#Sanitary | 71 | 57 | 50 | 7 | 21 | 87.7% [77–94] | 70.4% [59–80] | 0.781 [0.69–0.86] |
| **micro** | 1197 | 1070 | 909 | 161 | 288 | 85.0% | 75.9% | 0.802 [0.78–0.82] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 2.19 calls and 0.03 tool calls per item; rule gate 198, quote repair 37, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1070/1070; cost $0.1908 ($0.949 per 1,000 items). Items on which each tool was called: get_label_rules 2%.

Confusion: exact 28, under-labelled 69, over-labelled 31, swapped 73.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Discount | (no predicted label) | 20 | missed |
| Price#Level | Price#Cost_effective | 19 | confused |
| Price#Level | (no predicted label) | 15 | missed |
| Location#Downtown | (no predicted label) | 14 | missed |
| Food#Appearance | (no predicted label) | 13 | missed |
| Food#Portion | (no predicted label) | 13 | missed |
| Service#Hospitality | Price#Cost_effective | 12 | confused |
| Ambience#Sanitary | (no predicted label) | 11 | missed |
| Food#Taste | Price#Cost_effective | 11 | confused |
| Food#Portion | Price#Cost_effective | 10 | confused |

**Slices of 201 items.** Overall micro F1 0.802, exact match 13.9%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.773 [0.73–0.82] | 2/37 (5.4%) | 0/37 | – | -0.036 [-0.09 to +0.01] | no measured difference |
| 4-5 stars | 164 | 0.809 [0.79–0.83] | 26/164 (15.9%) | 0/162 | 0/2 | +0.036 [-0.01 to +0.09] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.814 [0.78–0.84] | 5/56 (8.9%) | 0/56 | – | +0.021 [-0.02 to +0.06] | no measured difference |
| 5-7 labels | 79 | 0.797 [0.77–0.83] | 8/79 (10.1%) | 0/79 | – | -0.008 [-0.05 to +0.03] | no measured difference |
| 1-4 labels | 66 | 0.784 [0.74–0.82] | 15/66 (22.7%) | 0/64 | 0/2 | -0.022 [-0.07 to +0.02] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.802 [0.78–0.83] | 19/148 (12.8%) | 0/148 | – | +0.002 [-0.04 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.800 [0.76–0.84] | 9/53 (17.0%) | 0/51 | 0/2 | -0.002 [-0.05 to +0.04] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.832 [0.79–0.87] | 20/67 (29.9%) | 0/65 | 0/2 | +0.041 [-0.00 to +0.08] | no measured difference |
| 236–314 chars | 67 | 0.773 [0.74–0.81] | 5/67 (7.5%) | 0/67 | – | -0.042 [-0.08 to +0.00] | no measured difference |
| 315–946 chars | 67 | 0.804 [0.77–0.83] | 3/67 (4.5%) | 0/67 | – | +0.003 [-0.04 to +0.04] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.869 [+0.82 to +0.91] (exact match) | too few |
| Ambience#Decoration | 90 | 0.820 [0.79–0.85] | 13/90 (14.4%) | 0/90 | – | +0.043 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.813 [0.78–0.84] | 7/64 (10.9%) | 0/64 | – | +0.019 [-0.02 to +0.06] | no measured difference |
| Ambience#Sanitary | 71 | 0.825 [0.79–0.85] | 9/71 (12.7%) | 0/71 | – | +0.043 [+0.00 to +0.08] | better |
| Ambience#Space | 76 | 0.825 [0.80–0.85] | 10/76 (13.2%) | 0/76 | – | +0.046 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.778 [0.74–0.81] | 1/54 (1.9%) | 0/54 | – | -0.035 [-0.08 to +0.01] | no measured difference |
| Food#Portion | 88 | 0.806 [0.78–0.83] | 10/88 (11.4%) | 0/88 | – | +0.008 [-0.03 to +0.05] | no measured difference |
| Food#Recommend | 32 | 0.829 [0.78–0.87] | 4/32 (12.5%) | 0/32 | – | +0.033 [-0.02 to +0.08] | no measured difference |
| Food#Taste | 190 | 0.805 [0.78–0.82] | 25/190 (13.2%) | 0/190 | – | +0.075 [-0.02 to +0.19] | no measured difference |
| Location#Downtown | 39 | 0.772 [0.73–0.81] | 2/39 (5.1%) | 0/39 | – | -0.041 [-0.09 to +0.01] | no measured difference |
| Location#Easy_to_find | 47 | 0.816 [0.78–0.85] | 6/47 (12.8%) | 0/47 | – | +0.020 [-0.02 to +0.06] | no measured difference |
| Location#Transportation | 52 | 0.797 [0.76–0.83] | 6/52 (11.5%) | 0/52 | – | -0.007 [-0.05 to +0.03] | no measured difference |
| Price#Cost_effective | 41 | 0.813 [0.77–0.85] | 4/41 (9.8%) | 0/41 | – | +0.015 [-0.03 to +0.06] | no measured difference |
| Price#Discount | 73 | 0.799 [0.77–0.83] | 4/73 (5.5%) | 0/73 | – | -0.006 [-0.04 to +0.03] | no measured difference |
| Price#Level | 94 | 0.783 [0.76–0.81] | 11/94 (11.7%) | 0/94 | – | -0.041 [-0.08 to -0.00] | worse |
| Service#Hospitality | 111 | 0.803 [0.78–0.83] | 10/111 (9.0%) | 0/111 | – | +0.004 [-0.04 to +0.04] | no measured difference |
| Service#Parking | 12 | 0.765 [0.68–0.85] | 0/12 (0.0%) | 0/12 | – | -0.040 [-0.12 to +0.05] | too few |
| Service#Queue | 35 | 0.805 [0.76–0.85] | 3/35 (8.6%) | 0/35 | – | +0.004 [-0.04 to +0.05] | no measured difference |
| Service#Timely | 28 | 0.780 [0.73–0.83] | 1/28 (3.6%) | 0/28 | – | -0.026 [-0.08 to +0.03] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


## asap / test_a / agent-cases-mixed

**asap / test_a / agent-cases-mixed: 201 items, 18 labels.** Micro F1 0.802 [0.78–0.82], macro F1 0.762 [0.73–0.78], exact match 23/201 (11.4%) [8–17].

| Label | Gold | Predicted | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| Food#Taste | 190 | 191 | 189 | 2 | 1 | 99.0% [96–100] | 99.5% [97–100] | 0.992 [0.98–1.00] |
| Food#Appearance | 54 | 36 | 30 | 6 | 24 | 83.3% [68–92] | 55.6% [42–68] | 0.667 [0.54–0.77] |
| Food#Portion | 88 | 74 | 62 | 12 | 26 | 83.8% [74–90] | 70.5% [60–79] | 0.765 [0.69–0.83] |
| Food#Recommend | 32 | 45 | 26 | 19 | 6 | 57.8% [43–71] | 81.2% [65–91] | 0.675 [0.55–0.79] |
| Price#Level | 94 | 61 | 53 | 8 | 41 | 86.9% [76–93] | 56.4% [46–66] | 0.684 [0.60–0.76] |
| Price#Cost_effective | 41 | 73 | 37 | 36 | 4 | 50.7% [39–62] | 90.2% [77–96] | 0.649 [0.54–0.74] |
| Price#Discount | 73 | 45 | 37 | 8 | 36 | 82.2% [69–91] | 50.7% [39–62] | 0.627 [0.51–0.72] |
| Location#Downtown | 39 | 16 | 12 | 4 | 27 | 75.0% [51–90] | 30.8% [19–46] | 0.436 [0.27–0.59] |
| Location#Transportation | 52 | 40 | 37 | 3 | 15 | 92.5% [80–97] | 71.2% [58–82] | 0.804 [0.70–0.89] |
| Location#Easy_to_find | 47 | 36 | 31 | 5 | 16 | 86.1% [71–94] | 66.0% [52–78] | 0.747 [0.63–0.84] |
| Service#Queue | 35 | 36 | 28 | 8 | 7 | 77.8% [62–88] | 80.0% [64–90] | 0.789 [0.67–0.88] |
| Service#Hospitality | 111 | 107 | 99 | 8 | 12 | 92.5% [86–96] | 89.2% [82–94] | 0.908 [0.87–0.95] |
| Service#Parking | 12 | 11 | 10 | 1 | 2 | 90.9% [62–98] | 83.3% [55–95] | 0.870 [0.67–1.00] |
| Service#Timely | 28 | 31 | 24 | 7 | 4 | 77.4% [60–89] | 85.7% [69–94] | 0.814 [0.69–0.91] |
| Ambience#Decoration | 90 | 88 | 76 | 12 | 14 | 86.4% [78–92] | 84.4% [76–91] | 0.854 [0.79–0.90] |
| Ambience#Noise | 64 | 50 | 47 | 3 | 17 | 94.0% [84–98] | 73.4% [62–83] | 0.825 [0.74–0.89] |
| Ambience#Space | 76 | 74 | 59 | 15 | 17 | 79.7% [69–87] | 77.6% [67–86] | 0.787 [0.71–0.86] |
| Ambience#Sanitary | 71 | 58 | 53 | 5 | 18 | 91.4% [81–96] | 74.6% [63–83] | 0.822 [0.74–0.89] |
| **micro** | 1197 | 1072 | 910 | 162 | 287 | 84.9% | 76.0% | 0.802 [0.78–0.82] |

Miss rate (a labelled item predicted with no label): 0/199 (0.0%) [0–2]. False-alarm rate (an unlabelled item given a label): 0/2 (0.0%) [0–66].

Intervals are 95%: Wilson for precision, recall and rates, percentile bootstrap over items for F1.

Operations: 201/201 answered; 2.12 calls and 0.00 tool calls per item; rule gate 199, quote repair 27, self-check changed 0 of 0 items (+0 / −0 labels); exact quotes 1071/1072; cost $0.1851 ($0.921 per 1,000 items).

Confusion: exact 23, under-labelled 73, over-labelled 34, swapped 71.

| Gold | Predicted | Count | Kind |
|---|---|---|---|
| Price#Discount | (no predicted label) | 19 | missed |
| Price#Level | Price#Cost_effective | 17 | confused |
| Price#Level | (no predicted label) | 16 | missed |
| Food#Portion | (no predicted label) | 15 | missed |
| Food#Appearance | (no predicted label) | 13 | missed |
| Location#Downtown | (no predicted label) | 13 | missed |
| Ambience#Sanitary | (no predicted label) | 11 | missed |
| Ambience#Space | (no predicted label) | 11 | missed |
| Price#Discount | Price#Cost_effective | 9 | confused |
| Ambience#Decoration | (no predicted label) | 8 | missed |

**Slices of 201 items.** Overall micro F1 0.802, exact match 11.4%.

### By meta.stars_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 1-3 stars | 37 | 0.776 [0.73–0.81] | 2/37 (5.4%) | 0/37 | – | -0.033 [-0.08 to +0.01] | no measured difference |
| 4-5 stars | 164 | 0.808 [0.79–0.83] | 21/164 (12.8%) | 0/162 | 0/2 | +0.033 [-0.01 to +0.08] | no measured difference |

### By meta.n_labels_band

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 8+ labels | 56 | 0.823 [0.79–0.85] | 3/56 (5.4%) | 0/56 | – | +0.036 [-0.00 to +0.07] | no measured difference |
| 5-7 labels | 79 | 0.784 [0.75–0.81] | 5/79 (6.3%) | 0/79 | – | -0.030 [-0.07 to +0.01] | no measured difference |
| 1-4 labels | 66 | 0.793 [0.76–0.83] | 15/66 (22.7%) | 0/64 | 0/2 | -0.011 [-0.05 to +0.03] | no measured difference |

### By meta.has_neutral

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| has a neutral mention | 148 | 0.803 [0.78–0.83] | 16/148 (10.8%) | 0/148 | – | +0.005 [-0.03 to +0.05] | no measured difference |
| no neutral mention | 53 | 0.798 [0.76–0.83] | 7/53 (13.2%) | 0/51 | 0/2 | -0.005 [-0.05 to +0.04] | no measured difference |

### By length of text

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| 122–235 chars | 67 | 0.816 [0.78–0.85] | 16/67 (23.9%) | 0/65 | 0/2 | +0.019 [-0.02 to +0.06] | no measured difference |
| 236–314 chars | 67 | 0.768 [0.73–0.80] | 4/67 (6.0%) | 0/67 | – | -0.050 [-0.09 to -0.01] | worse |
| 315–946 chars | 67 | 0.820 [0.79–0.85] | 3/67 (4.5%) | 0/67 | – | +0.030 [-0.01 to +0.07] | no measured difference |

### By gold label

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| (no gold label) | 2 | – | 2/2 (100.0%) | – | 0/2 | +0.894 [+0.85 to +0.93] (exact match) | too few |
| Ambience#Decoration | 90 | 0.821 [0.80–0.85] | 8/90 (8.9%) | 0/90 | – | +0.045 [+0.01 to +0.08] | better |
| Ambience#Noise | 64 | 0.814 [0.78–0.84] | 4/64 (6.2%) | 0/64 | – | +0.022 [-0.02 to +0.06] | no measured difference |
| Ambience#Sanitary | 71 | 0.829 [0.80–0.86] | 7/71 (9.9%) | 0/71 | – | +0.051 [+0.01 to +0.09] | better |
| Ambience#Space | 76 | 0.827 [0.80–0.85] | 7/76 (9.2%) | 0/76 | – | +0.049 [+0.01 to +0.08] | better |
| Food#Appearance | 54 | 0.783 [0.75–0.82] | 2/54 (3.7%) | 0/54 | – | -0.027 [-0.07 to +0.01] | no measured difference |
| Food#Portion | 88 | 0.801 [0.78–0.83] | 7/88 (8.0%) | 0/88 | – | -0.002 [-0.04 to +0.04] | no measured difference |
| Food#Recommend | 32 | 0.829 [0.79–0.87] | 2/32 (6.2%) | 0/32 | – | +0.033 [-0.01 to +0.07] | no measured difference |
| Food#Taste | 190 | 0.806 [0.79–0.83] | 20/190 (10.5%) | 0/190 | – | +0.102 [+0.02 to +0.22] | better |
| Location#Downtown | 39 | 0.776 [0.74–0.81] | 1/39 (2.6%) | 0/39 | – | -0.034 [-0.08 to +0.01] | no measured difference |
| Location#Easy_to_find | 47 | 0.821 [0.79–0.85] | 4/47 (8.5%) | 0/47 | – | +0.028 [-0.01 to +0.07] | no measured difference |
| Location#Transportation | 52 | 0.807 [0.77–0.84] | 4/52 (7.7%) | 0/52 | – | +0.007 [-0.04 to +0.05] | no measured difference |
| Price#Cost_effective | 41 | 0.808 [0.77–0.85] | 4/41 (9.8%) | 0/41 | – | +0.008 [-0.04 to +0.05] | no measured difference |
| Price#Discount | 73 | 0.797 [0.77–0.82] | 2/73 (2.7%) | 0/73 | – | -0.009 [-0.04 to +0.03] | no measured difference |
| Price#Level | 94 | 0.776 [0.75–0.80] | 9/94 (9.6%) | 0/94 | – | -0.056 [-0.09 to -0.02] | worse |
| Service#Hospitality | 111 | 0.815 [0.79–0.84] | 9/111 (8.1%) | 0/111 | – | +0.036 [-0.00 to +0.07] | no measured difference |
| Service#Parking | 12 | 0.772 [0.69–0.85] | 0/12 (0.0%) | 0/12 | – | -0.033 [-0.12 to +0.04] | too few |
| Service#Queue | 35 | 0.789 [0.74–0.83] | 1/35 (2.9%) | 0/35 | – | -0.017 [-0.06 to +0.03] | no measured difference |
| Service#Timely | 28 | 0.778 [0.73–0.82] | 0/28 (0.0%) | 0/28 | – | -0.029 [-0.08 to +0.02] | no measured difference |

"Against the rest" is the slice's micro F1 minus that of all other items, with a 95% bootstrap interval; where a side has no gold label, F1 is not defined and the exact-match rate is compared instead. A slice is called worse or better only when the interval excludes 0; slices under 20 items get no verdict.


