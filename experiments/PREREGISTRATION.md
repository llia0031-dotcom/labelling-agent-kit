# Preregistration: labelling agent experiments

Written and frozen before any test item was labelled. The file fingerprints at the end fix the item sets, rulebooks, case libraries and prompts; `lak.run` refuses to start when one of them has changed. Anything changed after a run is listed under **Changes after the run** with the reason, and results affected by it are reported as such.

## 1. Question

Does a labelling agent that looks up label rules and labelled cases, and checks its own answer, label content better than a single prompt, and which of those parts helps? After the failures are analysed and the agent is revised, does the revision hold on items it was not tuned on?

## 2. Tasks and items

| Task | Items | Labels | Gold labels come from | Sets (frozen) |
|---|---|---|---|---|
| `ad_policy` | ad texts (caption plus on-screen words), Chinese and English | 7 per language (9 in all), multi-label, most ads 0 or 1 | fixed when each ad was written (Grounded Review's public items and Policy Model Lab's video ads) | dev 87, test A 119, test B 118 |
| `asap` | Dianping restaurant reviews, Chinese | 18 aspects, multi-label, about 6 per review | the ASAP dataset's own annotations (Bu et al., NAACL 2021) | dev 120, test A 201, test B 199 |

- **dev** is used for prompt and rule development. Two development rounds ran on it (`experiments/dev1.json`, `experiments/dev2.json`); what they changed is listed in section 9. **Test A** is labelled by every arm; its failures are analysed and drive the revision, so later results on test A are regression results, not held-out results. **Test B** is not labelled by any arm before the revision is fixed; it is the held-out set.
- Case libraries (never drawn from the test sets; data acceptance check A6): ad policy, 600 synthetic ads from Policy Model Lab's training split; ASAP, 600 real reviews from the official training split, 600 synthetic reviews (`tasks/asap/synth.py`), and a mixed library of the first 300 of each.
- Every item set and library passed the blocking data acceptance checks (`DATA_ACCEPTANCE.md`) before freezing.

## 3. Arms

All arms use `claude-haiku-5-5`, effort `low`, at most 6,000 output tokens per call, structured JSON output with the label list as an enum, the Message Batches API (a round of the tool loops with fewer than 30 requests goes out as direct calls at full price), one run per item. They share the label catalogue (id, name, one-line definition), the general rules and the answer format.

| Arm | What it adds |
|---|---|
| `prompt-short` | one call; the label catalogue only |
| `prompt-rules` | one call; the whole rulebook in the prompt |
| `agent` | tools `get_label_rules` and `compare_labels`; the rule gate (labels given without reading their rule get their rules sent once); one quote-repair turn |
| `agent-cases` | plus a retrieval step: the flow puts the most similar labelled cases (BM25 on the item text; 5 ads, or 3 review snippets of 240 characters) into the first message; plus the tools `search_cases` and `phrase_stats` over the same library |
| `agent-cases-check` | plus one self-check turn (confirm each label against its rule, decide unsure labels, consider labels whose keywords occur) |
| `agent-cases-synthetic`, `agent-cases-mixed` (ASAP only) | `agent-cases` with the synthetic or the mixed case library instead of the real one |

## 4. Measures

- **Primary**: micro F1 over all label decisions on test A, per task, with a 95% bootstrap interval (2,000 resamples of items, seed 20261118).
- **Secondary**: macro F1; exact-match rate; per-label precision, recall and F1 (Wilson intervals for rates); for ad policy, the miss rate (a violating ad given no label) and the false-alarm rate (a compliant ad given a label); cost per item and calls per item from the stored usage.
- A run with no parseable answer counts as "no label". The number of such runs is reported per arm.

## 5. Hypotheses and decision rule

A comparison "B better than A" holds when the 95% paired-bootstrap interval of B − A in micro F1 on the same items lies above 0; "B worse" when it lies below 0; otherwise "no measured difference". Exact McNemar on exact match is reported alongside.

| Id | Task | A | B | Expected |
|---|---|---|---|---|
| H1-ad, H1-asap | both | `prompt-short` | `agent` | B better: rules read before deciding reduce look-alike false alarms (ads) and convention misses (ASAP) |
| H2-ad, H2-asap | both | `agent` | `agent-cases` | B better: cases show how labels are applied |
| H3-ad, H3-asap | both | `agent-cases` | `agent-cases-check` | B better |
| H4-ad, H4-asap | both | `prompt-rules` | `agent` | no direction expected: are tools better than putting the whole rulebook in the prompt? |
| H5a | asap | `agent-cases-synthetic` | `agent-cases` | B (real cases) better: real cases carry the dataset's labelling conventions |
| H5b | asap | `agent-cases-mixed` | `agent-cases` | no direction expected |
| H6-ad, H6-asap | both | best v1 arm | its revision (v2), on test B | B better |

## 6. Analysis plan

- For every arm: per-label table, multi-label confusion matrix (MLCM), and slices fixed here: ad policy by language, source and difficulty (violating / look-alike / plain) plus three length buckets; ASAP by star band, number of gold labels, whether a gold mention is neutral, plus three length buckets; and one slice per gold label. Slices under 20 items get no verdict.
- **Root-cause analysis** on test A for the best v1 arm of each task (highest micro F1; on a tie, the cheaper arm): every wrong label decision gets the code-computed signals and is classified twice, independently, into prompt defect, model capability, rule conflict, sample distribution or label ambiguity (`lak/rca.py`). Agreement between the two passes is reported; split decisions are reported as split.
- **Revision**: v2 changes only what the root-cause table points to (prompt file `prompts/v2.json` and/or rulebook `rules_v2.json`). Every change is listed with the failures that motivated it. v2 and the best v1 arm are then run on test B, and v2 also on test A. H6 decides adoption on test B; test A results are reported as regression.

## 7. Budget and stopping

Project limit USD 5 for all model calls. A run stops sending when its own budget is used up; nothing is rerun to get a better number. Costs are summed from the stored usage of every answer.

## 8. Known limits

- The ad items were written by the same author as the rulebook's source projects; their labels are fixed by construction, not by independent annotators.
- ASAP's labels are the dataset's; some mentions look unlabelled (data acceptance check A10 measures how often a strong cue of a missing aspect appears). Precision on ASAP is bounded by this.
- One run per item and arm: model sampling adds variance that the item bootstrap does not include.

## 9. What development on dev changed

- **Rule gate** (after `smoke`): at effort low the agent often answered without reading any rule, so labels given without a rule read now get their rules sent once.
- **Retrieval step** (after `dev1`): when the case tools were only offered, the model called no tool at all on 40 of 40 ASAP dev reviews in its first turn (36 of 40 with the rule tools alone). The case arms now retrieve the closest cases in code, so `agent` and `agent-cases` differ only in the cases.
- **ASAP rulebook 1.1** (after `dev1`): a general rule that only judged aspects are labelled, citing the dataset paper (aspect-sentiment annotation). The one-shot arms' false positives on dev were mostly facts with no judgement.
- **Effort** (rule set in the development log before dev2's results came in, and added to this file after the main run without change): every arm switches to effort medium only if the full agent gains at least 0.02 micro F1 on the dev sets of both tasks with medium; otherwise every arm stays at effort low. dev2 measured +0.002 on ads and +0.019 on ASAP, so every arm uses effort low.
- **Text clean-up** (before any run on test sets): ASAP stores line breaks, tabs and carriage returns as escape sequences; they are converted in `tasks/asap/build.py`.

## Fingerprints

Filled in when frozen (sha256 of each file with LF line endings, first 12 characters; the same list is in `experiments/main.json` under `frozen`).


| File | sha256 (first 12) |
|---|---|
| `prompts/v1.json` | `ee6b7c3c8cd0` |
| `tasks/ad_policy/cases_synth.jsonl` | `d569ed6a2627` |
| `tasks/ad_policy/items_dev.jsonl` | `223817e58786` |
| `tasks/ad_policy/items_test_a.jsonl` | `a70de712e5d1` |
| `tasks/ad_policy/items_test_b.jsonl` | `36cda6184e2f` |
| `tasks/ad_policy/rules.json` | `fc0a865e1783` |
| `tasks/ad_policy/task.json` | `f75f00ad200a` |
| `tasks/asap/cases_real.jsonl` | `16f85144391e` |
| `tasks/asap/cases_synth.jsonl` | `47d6f19f5412` |
| `tasks/asap/items_dev.jsonl` | `a793c41bd989` |
| `tasks/asap/items_test_a.jsonl` | `9eab2dc85fbd` |
| `tasks/asap/items_test_b.jsonl` | `aab7919703cc` |
| `tasks/asap/rules.json` | `df9e816f0f43` |
| `tasks/asap/task.json` | `604c19a47bec` |

## Changes after the run

None yet.
