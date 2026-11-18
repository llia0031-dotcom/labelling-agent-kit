---
name: slice-report
description: Cuts labelling metrics by slices of the data - language, source, difficulty, text length, star rating, or one slice per gold label - and says which slices are measurably worse or better than the rest, with bootstrap intervals and a minimum slice size. Use it when an overall score looks fine but someone suspects it hides a weak group, before rolling a labelling agent or classifier out to a new market or content type, or when asked "where does the model fail", "break the F1 down by language", "is it worse on long texts", "分组看效果", "按语言/长度切片", "哪类样本最差". A bundled script does the grouping and the statistics; the agent explains what the weak slices have in common.
metadata:
  version: "0.1.0"
---

# Slice report

An average over all items can hide a slice where the labeller is much worse: Chinese ads, long reviews, look-alike items. The script groups the items by fields of the gold file and compares each slice with all other items, so a weak slice is named only when the evidence says so.

## Inputs

The gold and prediction JSONL files (shared `id`, `labels` list). Slice fields live in the gold file, for example:

```json
{"id": "ad-017", "labels": ["ABSOLUTE"], "text": "...", "meta": {"lang": "zh", "source": "video", "difficulty": "look-alike"}}
```

## Run the script

```bash
python <this-skill-folder>/scripts/slice_report.py gold.jsonl pred.jsonl --by meta.lang --by meta.difficulty
python <this-skill-folder>/scripts/slice_report.py gold.jsonl pred.jsonl --length text --buckets 3
python <this-skill-folder>/scripts/slice_report.py gold.jsonl pred.jsonl --by-label
```

Python 3.9+, standard library only. `--by` takes any field path and can repeat; a list-valued field puts an item in several slices. `--length FIELD` makes buckets with about equal numbers of items. `--min-n` (default 20) sets the smallest slice that gets a verdict. `--format json` gives every number. Exit code 0: report written; 2: an input could not be read.

For each slice: items, micro F1 with a bootstrap interval, exact match, miss and false-alarm counts (when the slice has both labelled and unlabelled items), and the difference from all other items with a bootstrap interval. The verdict is **worse** or **better** only when that interval excludes 0; otherwise **no measured difference**; slices under `--min-n` items are **too few**.

## Read the result

1. Report the worse slices first, with their size and the difference from the rest.
2. Do not call a small slice bad on its point estimate. "Too few" means look at its items one by one, not that it is fine.
3. Explain what the items of a weak slice share: open the failures in it (from the prediction file or `confusion-report`'s example ids). A weak "long text" slice may really be one label that long texts carry more often; check `--by-label` before blaming length.
4. Turn it into an action: more cases of that kind, a rule for that pattern, or a separate threshold for that market.

## Report

The shape, with the numbers of the example in `references/tutorial.md` (86 ads, a short prompt):

```markdown
**86 ads, micro F1 0.816 overall. One slice is measurably worse: Chinese ads (47), micro F1 0.754 against 0.905 for English (difference -0.151 [-0.28 to -0.01]). The largest group of their errors: GUARANTEE ads also given ABSOLUTE (5 of 15). Look-alike ads carry no gold label, so they are compared on exact match: no measured difference; 5 of 27 got a label.**

| Slice | Items | Micro F1 | Exact match | Miss | False alarm | Against the rest | Verdict |
|---|---|---|---|---|---|---|---|
| zh | 47 | 0.754 [0.65–0.85] | 32/47 (68.1%) | 3/25 | 4/22 | -0.151 [-0.28 to -0.01] | worse |
```
