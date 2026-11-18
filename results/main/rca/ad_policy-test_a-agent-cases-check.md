# Root causes: ad_policy / test_a / agent-cases-check

4 wrong label decisions on 4 items; the two independent passes agree on 3 of 4. 2 of the decisions were also wrong in every other arm. Cost $0.0031.

| Cause | All | False positives | Misses |
|---|---|---|---|
| prompt_defect | 1 | 0 | 1 |
| model_capability | 0 | 0 | 0 |
| rule_conflict | 2 | 1 | 1 |
| sample_distribution | 0 | 0 | 0 |
| label_ambiguity | 0 | 0 | 0 |
| split | 1 | 1 | 0 |

## Split decisions: the two causes given

| First | Second | Decisions |
|---|---|---|
| prompt_defect | rule_conflict | 1 |

## By label

| Label | Decisions | prompt_defect | model_capability | rule_conflict | sample_distribution | label_ambiguity | split |
|---|---|---|---|---|---|---|---|
| GUARANTEE | 2 | 0 | 0 | 1 | 0 | 0 | 1 |
| DATA | 2 | 1 | 0 | 1 | 0 | 0 | 0 |

## Suggested fixes (first pass), grouped by cause

### prompt_defect (1)
- DATA (miss, zh-h09): Add a prompt edit to the self-check: a percentage introduced by 实测, 测试, 检测 or 实验 is a test result and needs a source, so it must not be dropped as a spec; add cases such as "实测吸尘率 99.9%" labelled DATA and "续航 30 小时" labelled none.

### rule_conflict (2)
- GUARANTEE (false positive, ev-21): Add a rule edit clarifying whether an immediate weight-loss claim without 'guaranteed' or '100%' (e.g. 'melts fat overnight') is WEIGHT only or WEIGHT plus GUARANTEE, and add look-alike cases with this wording labelled WEIGHT only if that is the dataset convention.
- DATA (miss, zv-13): Add a rule edit and a case: efficacy percentages such as 除菌率, 过滤率, 去污率 are test results and need a stated source, so they are DATA unless the ad names the test or institution; add this ad as a positive example.

