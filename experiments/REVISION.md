# Revision: from the root-cause tables to v2

Written after the root-cause analysis of the best v1 arm (`agent-cases-check` on both tasks) on test A, and before any arm labelled test B. Every change answers a group of wrong label decisions in [`results/main/rca/asap-test_a-agent-cases-check.md`](../results/main/rca/asap-test_a-agent-cases-check.md) and [`results/main/rca/ad_policy-test_a-agent-cases-check.md`](../results/main/rca/ad_policy-test_a-agent-cases-check.md). The files are built by [`tasks/make_v2.py`](../tasks/make_v2.py) from v1, so every difference is in that script. Statistics quoted in the ASAP rules come from the training split ([`tasks/asap/v2_train_stats.txt`](../tasks/asap/v2_train_stats.txt)).

## What changed

| Id | File | Change | Failures behind it (test A) |
|---|---|---|---|
| R1 | `tasks/asap/rules_v2.json` | The general rule "label only judged aspects" (added on dev) gets the dataset's three exceptions: a mall or plaza location → Location#Downtown, a deal or voucher mentioned → Price#Discount, a stated spend → Price#Level, each with its training-split share | 30 missed Downtown, Discount and Level decisions on 27 reviews, classified as prompt defect or rule conflict; several fixes name the self-check deleting such labels |
| R2 | `tasks/asap/rules_v2.json` | The general-environment convention (all four Ambience labels) becomes a general rule, with "the self-check must not drop them" | 17 missed Ambience decisions on 7 reviews, classified as prompt defect |
| R3 | `tasks/asap/rules_v2.json` | Price#Level and Price#Cost_effective: cheap or expensive alone is Price#Level; Cost_effective needs price weighed against quality (training split: 87% of reviews saying 便宜 without value words carry Price#Level, 19% Cost_effective) | the largest confusion: 70 decisions on 62 reviews (Cost_effective given wrongly, Price#Level missed) |
| R4 | `tasks/asap/rules_v2.json` | Downtown adds 商厦, 商业街, 商业区, and a floor number in a mall still counts; Discount adds free trial meals and points redemption | included in R1's failures |
| R5 | `tasks/asap/rules_v2.json` | Portion: 料足 counts, a big ingredient does not; Space: a count of tables is not space | 8 decisions on 8 reviews classified as model capability |
| A1 | `tasks/ad_policy/rules_v2.json` | DATA: an effect percentage from a test (除菌率, 实测) with no source is DATA, not a specification | zh-h09 (prompt defect), zv-13 (rule conflict): both missed DATA |
| A2 | `tasks/ad_policy/rules_v2.json` | An immediate or effortless weight-loss claim is WEIGHT; GUARANTEE is added only with explicit guarantee wording | ev-21 (rule conflict) and en-t28 (split): GUARANTEE given to WEIGHT ads |
| P1 | `prompts/v2.json` | Before answering, go through the whole label list once and check the labels not taken as candidates | 51 misses on 34 reviews classified as prompt defect |
| P2 | `prompts/v2.json` | The self-check must not drop a label that the general rules or conventions require because the evidence is brief or neutral | the self-check deletions named in R1 and R2 |

Not changed: the 158 decisions classified as label ambiguity (gold labels that careful labellers could set either way, or that look incomplete), and the 149 decisions where the two classification passes disagreed. They are reported, not fitted.

## How it is tested

- **Held out (decides adoption, H6):** v1 and v2 of `agent-cases-check` on test B, which no arm had labelled. v2 is adopted for a task when the 95% paired-bootstrap interval of its micro F1 minus v1's lies above 0.
- **Regression (reported, not a held-out result):** v2 on test A against the v1 run already stored in `results/main` (`"reuse": ["main"]`, so v1 is replayed, not rerun). The changes were written after reading test A's failures, so a gain there is expected and says little.
- Same model, effort, batch settings and case libraries as the main run; frozen files below.

## Fingerprints

Filled in when frozen.


| File | sha256 (first 12) |
|---|---|
| `prompts/v1.json` | `ee6b7c3c8cd0` |
| `prompts/v2.json` | `d0adb199bf9b` |
| `tasks/ad_policy/cases_synth.jsonl` | `d569ed6a2627` |
| `tasks/ad_policy/items_dev.jsonl` | `223817e58786` |
| `tasks/ad_policy/items_test_a.jsonl` | `a70de712e5d1` |
| `tasks/ad_policy/items_test_b.jsonl` | `36cda6184e2f` |
| `tasks/ad_policy/rules.json` | `fc0a865e1783` |
| `tasks/ad_policy/rules_v2.json` | `5112348ab95b` |
| `tasks/ad_policy/task.json` | `f75f00ad200a` |
| `tasks/asap/cases_real.jsonl` | `16f85144391e` |
| `tasks/asap/cases_synth.jsonl` | `47d6f19f5412` |
| `tasks/asap/items_dev.jsonl` | `a793c41bd989` |
| `tasks/asap/items_test_a.jsonl` | `9eab2dc85fbd` |
| `tasks/asap/items_test_b.jsonl` | `aab7919703cc` |
| `tasks/asap/rules.json` | `df9e816f0f43` |
| `tasks/asap/rules_v2.json` | `b0263f90bf2c` |
| `tasks/asap/task.json` | `604c19a47bec` |

## Changes after the run

None yet.
