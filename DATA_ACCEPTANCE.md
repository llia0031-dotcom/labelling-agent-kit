# Data acceptance standard

Every item set and case library in this kit passes these checks before an experiment uses it. They run with `python -m lak.accept`, which writes `results/acceptance.json` and `results/ACCEPTANCE.md`. Blocking checks must pass; warnings are reported with their numbers and explained in the evaluation report.

[中文](DATA_ACCEPTANCE.zh-CN.md)

## Checks

| Code | Check | Kind | Threshold | Why |
|---|---|---|---|---|
| A1 | Schema: every row has a unique `id`, a non-empty `text` and a `labels` list of strings | blocking | 0 failures | malformed rows silently become "no label" |
| A2 | Every label exists in the task's rulebook and fits the item's scope (e.g. a Chinese-only label on a Chinese item) | blocking | 0 failures | a label outside the rulebook cannot be predicted |
| A3 | Rows without a label only where the rulebook allows them (`empty_allowed`) | blocking | 0 failures | |
| A4 | The text is in the stated language (Chinese: at least 30% CJK characters; English: under 30%) | blocking | 0 failures | |
| A5 | No exact duplicate texts; near duplicates (character 5-gram Jaccard ≥ 0.6) at most 1% of rows | blocking | 0 exact, ≤ 1% near | duplicates over-weight one pattern |
| A6 | No overlap with the frozen test sets: no pair with character 8-gram Jaccard ≥ 0.3 between this file and any test set (and between test A and test B) | blocking | 0 pairs | a near copy of a test item in the cases or the other test set leaks the answer |
| A7 | Every row states where it comes from (`source` or `meta.source`) | blocking | 0 missing | real and synthetic data must stay distinguishable |
| A8 | Length: rows within the 1st–99th percentile of the real reference data | warning | ≥ 95% of rows | synthetic text that is much shorter or longer is a different task |
| A9 | Label share: each label's share within 10 percentage points of the real reference data | warning | max gap ≤ 10 points | a skewed library teaches a skewed prior |
| A10 | Cue conflicts: rows that contain a strong cue phrase of a label they do not carry (a phrase whose training-split precision for that label is ≥ 0.95) | warning | ≤ 5% of rows | in synthetic data: the generator wrote about an aspect it was told to leave out; in real data: an estimate of incomplete gold labels |

Reference data for A8–A10: for ASAP, the real case library drawn from the official training split; for the ad-policy task, the written test ads.

## How the test sets were made to pass

The first acceptance run flagged three near-duplicate pairs that straddled two sets: two look-alike alcohol ads built on the same template (dev and test A, test A and test B), and two reviews by apparently the same user that open with the same copied text (ASAP test A and test B). The build scripts now keep each near-duplicate pair in one set: the item of the later set moves to the earlier one (dev, then test A, then test B). The rule and the moves are in `tasks/keep_together.py` and in the build output; sets were frozen after this.

## Gold labels

- Gold labels come only from the dataset itself (ASAP's annotations) or were fixed when each item was written (the ad-policy items). Nothing in this kit was relabelled.
- Gold labels are not assumed perfect. A10 on real data and the root-cause analysis's `label_ambiguity` class measure where they are debatable; such items are reported, not silently dropped or changed.

## Synthetic data

A synthetic case library additionally passes, before A1–A10, the generator's own filters (in `tasks/asap/synth.py`): the answer parses, every evidence quote is verbatim, no strong cue of an aspect outside the requested set, and no near copy of a dev or test item. Its report (`tasks/asap/synth_report.json`) lists how many generated rows each filter removed.
