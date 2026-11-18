# Evaluation: a reusable content-labelling agent, tuned with experiments

One labelling flow, two tasks (ad-policy labels in Chinese and English; 18 restaurant-review aspects from the public ASAP dataset), five arms compared on frozen items with preregistered hypotheses, a root-cause table of the best arm's failures, and a revision checked on items nothing was tuned on.

**Summary**

- On test A the full agent (rules, retrieved cases, self-check) reached micro F1 0.971 on ads and 0.824 on ASAP, against 0.768 and 0.715 for a short prompt. Reading the rules was the largest step; retrieved cases helped on both tasks; the self-check helped on ASAP only.
- Putting the whole rulebook in the prompt got most of the way on ads (0.878); the agent's lead over it is a measured gain only on ASAP.
- Of the 406 wrong label decisions on ASAP, the largest class is label ambiguity (158); the fixable classes were prompt defects (61), rule conflicts (18) and model capability (20).
- The revision built from those causes is ahead on held-out ASAP reviews by +0.018 [+0.005, +0.031] and is adopted; on ads its +0.021 is not a measured gain (the interval reaches 0) and it is not adopted.
- All model calls cost USD 3.6325.

## 1. Setup

### Tasks

| | Ad policy | Restaurant review aspects (ASAP) |
|---|---|---|
| Items | ad text: caption plus the words on screen, Chinese and English | Dianping restaurant reviews, Chinese |
| Labels | 7 per language (ABSOLUTE, MEDICAL, GUARANTEE, DISPARAGE, ALCOHOL, plus DATA and FLAG in Chinese, WEIGHT and BEFORE_AFTER in English) | 18 aspects in 5 groups (food, price, location, service, ambience) |
| Labels per item | mostly 0 or 1 | about 6 |
| Gold labels | fixed when each ad was written | the dataset's own annotations (Bu et al., NAACL 2021) |
| Sets | dev 87, test A 119, test B 118 | dev 120, test A 201, test B 199 |
| Case library | 600 synthetic ads | 600 real reviews from the training split; 600 synthetic; 300 + 300 mixed |
| Licence | MIT (from Policy Model Lab's `data_public`) | Apache-2.0 (only the sampled reviews are included) |

### Agent

One flow for every task. Code decides each branch; the model decides the labels.

1. **Retrieve** (case arms): the most similar labelled cases (BM25 on the item text) go into the first message.
2. **Label**: the model may call `get_label_rules`, `compare_labels`, `phrase_stats` and `search_cases`; after five tool rounds it must answer.
3. **Rule gate**: labels given without their rule having been read get their rules sent, once.
4. **Quote repair**: a quote that is not the item's own words gets one turn to be fixed or dropped.
5. **Self-check** (check arm): one more turn to confirm each label against its rule, decide unsure labels and consider labels whose keywords occur.

### Arms

| Arm | Calls | Context |
|---|---|---|
| `prompt-short` | 1 | label catalogue |
| `prompt-rules` | 1 | the whole rulebook |
| `agent` | 1 or more | catalogue + rule tools, rule gate, quote repair |
| `agent-cases` | 1 or more | + retrieved cases and case tools |
| `agent-cases-check` | 2 or more | + self-check turn |

Model `claude-haiku-5-5`, effort low, Message Batches API, one run per item and arm.

## 2. Method

- Preregistration: [`experiments/PREREGISTRATION.md`](../experiments/PREREGISTRATION.md), with the fingerprints of every frozen file.
- Data acceptance: [`DATA_ACCEPTANCE.md`](../DATA_ACCEPTANCE.md); the report is `results/ACCEPTANCE.md`.
- Metrics: per-label precision and recall with Wilson intervals, F1 and micro/macro F1 with item bootstrap intervals, the multi-label confusion matrix (MLCM), slices with a minimum size, paired bootstrap and exact McNemar for comparisons. All from the skill scripts, which are tested against `scikit-learn`, `statsmodels` and `rank_bm25`.
- Root-cause analysis: for each wrong label decision, code-computed signals, then two independent classifications into five causes.

## 3. Data

Every item set and case library passed the blocking acceptance checks before any experiment used it ([`results/ACCEPTANCE.md`](../results/ACCEPTANCE.md)).

- **Near duplicates across sets.** The first acceptance run found pairs with character 8-gram Jaccard of at least 0.3 that sat in different sets: look-alike alcohol ads built on one template, and reviews by apparently the same user that open with the same copied text. The build scripts now keep such pairs in one set (`tasks/keep_together.py`); after that, all sets passed.
- **Synthetic reviews.** 700 were generated (USD 0.2369) from specs that copy the aspect set and sentiments of randomly drawn training reviews. Checked in spec order until 600 had passed, the filters removed 21 (17 contained a strong cue of an aspect outside the spec, 3 failed language or length, 1 had a quote that was not verbatim); those 600 form the library. They pass every blocking check but trip warning A8: only 59.0% fall within the real reviews' 1st–99th percentile length (197–806 characters). The synthetic reviews are shorter than real ones, which is part of what the real-versus-synthetic comparison measures.
- **Incomplete gold labels in ASAP.** Check A10 counts reviews that contain a phrase whose training-split precision for an aspect is at least 0.95 while the review's gold labels lack that aspect: 7 rows (3.5%) of test A and 3 rows (1.5%) of test B. This is a lower bound on unlabelled mentions; it bounds the precision any labeller can reach on this data.

## 4. Development on dev

Two rounds ran on the dev sets before anything was frozen ([`results/dev1/ANALYSIS.md`](../results/dev1/ANALYSIS.md), [`results/dev2/ANALYSIS.md`](../results/dev2/ANALYSIS.md)). What they changed is listed in section 9 of the preregistration:

1. **The case tools were not used when only offered.** In dev1, the arm that offered `search_cases` and `phrase_stats` made no tool call at all on 40 of 40 ASAP reviews in its first turn, against 36 of 40 for the arm with the rule tools alone. Retrieval became a fixed step of the flow, so `agent` and `agent-cases` differ only in the cases.
2. **ASAP rulebook 1.1.** Most false positives of the one-shot arms on dev were aspects mentioned as plain facts ("won a voucher", "booked a day ahead"). ASAP is an aspect-sentiment dataset, so a general rule now labels only judged aspects.
3. **Effort.** The rule, written before dev2's results: switch every arm to effort medium only if the full agent gains at least 0.02 micro F1 on both tasks. It gained +0.002 on ads and +0.019 on ASAP, so every arm stayed at effort low.

dev2 (the design that was then frozen), micro F1:

| Arm | Ads (87) | ASAP (60) |
|---|---|---|
| `prompt-short` | 0.832 | 0.736 |
| `prompt-rules` | 0.917 | 0.799 |
| `agent` | 0.898 | 0.841 |
| `agent-cases` | 0.905 | 0.827 |
| `agent-cases-check` | 0.913 | 0.844 |

## 5. Results on test A

Micro F1 with 95% bootstrap intervals ([`results/main/ANALYSIS.md`](../results/main/ANALYSIS.md)):

| Arm | Ads (119) | ASAP (201) | USD per 1,000 items, ads / ASAP |
|---|---|---|---|
| `prompt-short` | 0.768 [0.70–0.83] | 0.715 [0.70–0.73] | 0.08 / 0.21 |
| `prompt-rules` | 0.878 [0.83–0.92] | 0.782 [0.76–0.80] | 0.10 / 0.25 |
| `agent` | 0.925 [0.88–0.96] | 0.799 [0.78–0.82] | 0.24 / 0.72 |
| `agent-cases` | 0.965 [0.93–0.99] | 0.812 [0.79–0.83] | 0.28 / 0.91 |
| `agent-cases-check` | **0.971** [0.94–0.99] | **0.824** [0.80–0.84] | 0.53 / 1.59 |
| `agent-cases-synthetic` | – | 0.802 [0.78–0.82] | – / 0.95 |
| `agent-cases-mixed` | – | 0.802 [0.78–0.82] | – / 0.92 |

Preregistered comparisons (B − A in micro F1, paired bootstrap):

| Id | A → B | Ads | ASAP |
|---|---|---|---|
| H1 | `prompt-short` → `agent` | +0.157 [+0.106, +0.214], better | +0.083 [+0.064, +0.102], better |
| H2 | `agent` → `agent-cases` | +0.040 [+0.007, +0.076], better | +0.014 [+0.003, +0.024], better |
| H3 | `agent-cases` → `agent-cases-check` | +0.006 [-0.023, +0.038], no measured difference | +0.012 [+0.001, +0.023], better |
| H4 | `prompt-rules` → `agent` | +0.047 [-0.004, +0.097], no measured difference | +0.017 [+0.000, +0.033], better |
| H5a | `agent-cases-synthetic` → `agent-cases` (real cases) | – | +0.010 [-0.001, +0.022], no measured difference |
| H5b | `agent-cases-mixed` → `agent-cases` (real cases) | – | +0.010 [+0.001, +0.021], better |

What the numbers say:

- **Reading the rules is the largest step.** The agent beats the short prompt on both tasks (H1). On ads, most of the gain is precision on look-alikes: the short prompt gave a label to 12 of 32 look-alike ads, the full agent to none.
- **Tools against the whole rulebook in the prompt (H4)** is a measured gain only on ASAP (+0.017, interval just above 0). On ads the agent is ahead by 0.047 but the interval includes 0: putting the ad rulebook in the prompt gets most of the way.
- **Retrieved cases help on both tasks (H2)**, even though the model almost never searched further by itself: in `agent-cases`, `search_cases` was called on 2% of ads and on no ASAP review. The fixed retrieval step carries the gain.
- **The self-check (H3)** is a measured gain on ASAP only, where it changed 75 of 201 reviews (+66 / −43 labels); on ads it changed 5 of 119. It raises the cost per 1,000 items from USD 0.91 to 1.59 on ASAP and from 0.28 to 0.53 on ads.
- **Real against synthetic cases (H5).** Real cases are ahead of the synthetic library by 0.010, with an interval that touches 0, and ahead of the half-and-half library by the same 0.010 with an interval just above 0. The synthetic library is not worse by much on this measure, although it is shorter than real data (section 3).
- **The flow's branches fired often.** In the full agent the rule gate sent unread rules for 200 of 201 reviews and 58 of 119 ads: at effort low the model rarely looks rules up by itself, and the code makes sure it reads them. Every quote of the full agent was the item's own words (1115 of 1115 on ASAP), against 1303 of 1330 for the short prompt.
- **Slices.** No slice of the best arm is measurably worse on ads. On ASAP, the middle length bucket (236–314 characters) is lower than the rest (−0.055); with many slices checked per arm, this is a lead to look at, not a finding.

Per label, the best ASAP arm is weakest on Location#Downtown (recall 41.0%), Food#Appearance (recall 53.7%) and Price#Cost_effective (precision 55.6%), and confuses Price#Level with Price#Cost_effective most often (15 times).

## 6. Root causes

The best v1 arm (`agent-cases-check` on both tasks) was analysed on test A ([`results/main/rca/`](../results/main/rca/)).

| | Ads | ASAP |
|---|---|---|
| Wrong label decisions | 4 on 4 items | 406 on 165 items |
| Both passes agree | 3 of 4 | 257 of 406 |
| Also wrong in every other arm | 2 | 194 |
| Label ambiguity | 0 | 158 |
| Prompt defect | 1 | 61 |
| Model capability | 0 | 20 |
| Rule conflict | 2 | 18 |
| Sample distribution | 0 | 0 |
| The two passes disagree | 1 | 149 |

- **ASAP is bounded by its labels.** The largest agreed class is label ambiguity (158), and 194 of the 406 decisions were wrong in every arm. Many are mentions the gold labels leave out (section 3) or that careful labellers could read either way. These are reported, not fitted.
- **The fixable part is the rules and the flow.** Prompt defects (61, mostly misses) are labels the agent never considered, and a self-check that deleted labels the dataset's conventions require. Most of the 18 rule conflicts are about prices, deals and mall locations (Price#Level 7, Price#Discount 3, Location#Downtown 2, Price#Cost_effective 1), where the general rule added on dev ("label only judged aspects") contradicts the dataset. On ads, the two rule conflicts are effect percentages from tests (DATA) and immediate weight-loss claims (WEIGHT or GUARANTEE).
- **Agreement between the passes is moderate on ASAP** (257 of 406). A root cause is a judgement; in 101 of the 149 split decisions one pass said label ambiguity and the other a fixable cause (rule conflict 42, prompt defect 38, model capability 21). Whether a mention "should" be labelled is exactly where an ambiguous gold label and a missing rule look alike.

## 7. Revision, checked on held-out items

v2 changes only what the root-cause tables point to ([`experiments/REVISION.md`](../experiments/REVISION.md), built by `tasks/make_v2.py`): for ASAP, the dataset's exceptions to the "judged aspects only" rule (mall locations, deals, stated prices), the general-environment convention, the boundary between Price#Level and Price#Cost_effective and a few boundary notes; for ads, effect percentages from tests as DATA and immediate weight-loss claims as WEIGHT only; for both, a prompt that goes through the whole label list before answering and a self-check that keeps convention-required labels. It was frozen before any arm labelled test B ([`results/revision/ANALYSIS.md`](../results/revision/ANALYSIS.md)).

| | Ads, test B (118) | ASAP, test B (199) | Ads, test A (119) | ASAP, test A (201) |
|---|---|---|---|---|
| v1 (`agent-cases-check`) | 0.971 [0.94–0.99] | 0.834 [0.82–0.85] | 0.971 [0.94–0.99] | 0.824 [0.80–0.84] |
| v2 | 0.993 [0.98–1.00] | 0.852 [0.83–0.87] | 0.986 [0.96–1.00] | 0.841 [0.82–0.86] |
| v2 − v1, micro F1 | +0.021 [+0.000, +0.048] | +0.018 [+0.005, +0.031] | +0.014 [-0.018, +0.048] | +0.017 [+0.003, +0.031] |
| Verdict | no measured difference | better | no measured difference | better |

- **ASAP: v2 is adopted (H6).** On test B, which nothing was tuned on, v2 is ahead by +0.018 with an interval above 0. The gain sits where the changes were aimed: per-label F1 Price#Level +0.112, Price#Discount +0.110, Location#Downtown +0.111. Exact match moved little: only v2 exact on 19 reviews, only v1 on 13.
- **Ads: v2 is not adopted.** It is ahead on test B by +0.021, but the lower end of the interval is 0, so by the preregistered rule it is not a measured improvement. v1 already made only four errors on test A; there is little left to measure. On test A, WEIGHT F1 fell by 0.091 with v2 while DATA rose by 0.167: the WEIGHT rule change fixed some errors and caused others.
- **Regression on test A** (expected to look good, since the changes were written from its failures): +0.017 on ASAP, +0.014 on ads. It is reported for completeness, not as evidence.

## 8. Limits

- **Single runs.** Each arm labelled each item once. Model sampling adds variance the item bootstrap does not include, and several differences here are close to the edge (H4 on ASAP, H5b, and the ads revision).
- **The ad items** come from the same projects as the ad rulebook (Grounded Review and Policy Model Lab); their gold labels are fixed by construction, not set by independent annotators. The ads task is close to its ceiling with the full agent.
- **ASAP's gold labels** leave out some mentions (section 3), and the root-cause classes include 158 decisions judged to be label ambiguity. Precision on ASAP is bounded by this, and some "errors" of the agent are labels the dataset arguably should have.
- **Root causes are judgements.** Two independent passes agree on 257 of 406 ASAP decisions; the revision used only the classes where the fix was clear.
- **Synthetic data.** The synthetic reviews are shorter than real ones and were generated from the same rulebook the agent reads; a different generator or prompt could change the real-versus-synthetic result.
- **dev1 cannot be replayed.** It used an earlier agent design; its records are kept as they were, and `run_all.py` re-analyses them without sending requests.

## 9. Cost

All model calls came to USD 3.6325 (claude-haiku-5-5; [`results/COSTS.md`](../results/COSTS.md)), summed from the token usage stored with each answer. The 1,035 answers the revision run copied from the main run are counted once. The full agent labels 1,000 reviews for USD 1.59 and 1,000 ads for USD 0.53 with the Message Batches API.
