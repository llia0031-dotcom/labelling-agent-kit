---
name: confusion-report
description: Shows which labels a labeller confuses with which - a confusion matrix that also works when items carry several labels (MLCM), the most frequent confused pairs with the ids of the items behind them, and how many items were under-labelled, over-labelled or swapped. Use it after scoring a classifier, labelling agent or annotation batch, when someone asks why a label is wrong, which labels get mixed up, or what the error pattern is - for example "confusion matrix for my multi-label predictions", "which labels does the model confuse", "what does it predict instead of X", "标签混淆分析", "哪些标签容易混", "错成了什么". A bundled script builds the matrix exactly; the agent turns the top confusions into concrete rule or prompt fixes.
metadata:
  version: "0.1.0"
---

# Confusion report

Per-label scores say a label is weak; the confusion matrix says what it is mistaken for. With one label per item that is the ordinary matrix. With several labels per item the ordinary matrix is not defined, so the script builds the multi-label confusion matrix (MLCM) of Heydarian, Doyle and Samavi (IEEE Access, 2022), which reduces to the ordinary matrix for single-label data.

## Inputs

The same two JSONL files as `label-metrics`: gold and predictions, one line per item, shared `id`, a `labels` list.

## Run the script

```bash
python <this-skill-folder>/scripts/confusion_report.py gold.jsonl pred.jsonl
python <this-skill-folder>/scripts/confusion_report.py gold.jsonl pred.jsonl --top 15 --examples 8 --format json
```

Python 3.9+, standard library only. `--labels` fixes the order of rows and columns. Exit code 0: report written; 2: an input could not be read.

## How to read the matrix

Rows are gold labels, columns are predicted labels. There is one extra row, **(no gold label)**, and one extra column, **(no predicted label)**. For each item (gold set T, predicted set P):

- every label in both counts on the diagonal
- T empty: each predicted label counts in the (no gold label) row: a false alarm
- labels missed and none added: each missed label counts in the (no predicted label) column: a miss
- labels added and none missed: each added label counts against every gold label of the item
- some missed and some added: each added label counts against every missed label: a swap

So an off-diagonal cell (gold A, predicted B) means "where A was right, B was given instead or as well". One item can add several counts; details and a worked example in `references/mlcm.md`.

## Turn confusions into fixes

For each of the top pairs, open two or three of the listed items and decide which kind of problem it is:

1. **Boundary between two labels** (A and B swapped both ways): the rules need a boundary sentence for this pair ("a ranking with a time and place stated is DATA, not ABSOLUTE").
2. **One label absorbs another** (A often predicted as B, rarely the reverse): B's "does not apply" list is missing the case.
3. **False alarms** (no gold label row): a look-alike pattern; add it to the label's "does not apply" entries.
4. **Misses** (no predicted label column): the label is under-triggered; check whether the item's wording is covered by the rule, or whether the gold is debatable.

Then say what would change: which rule or prompt line, and which items should flip if the fix works. Keep the items as a regression set for the next version.

## Report

The shape, with the numbers of the example in `references/tutorial.md` (86 ads, a short prompt):

```markdown
**86 ads: 67 exact, 6 under-labelled, 13 over-labelled, 0 swapped.**

| Gold | Predicted | Count | Example ids | What it is | Fix |
|---|---|---|---|---|---|
| GUARANTEE | ABSOLUTE | 6 | en-d12, syn-val-047, ... | promises in strong words ("100% pass rate") also read as superlatives | boundary rule: a promised outcome is GUARANTEE, ABSOLUTE is only superlatives and rank |
| DISPARAGE | (no predicted label) | 4 | syn-val-045, ... | rivals run down without being named | an *applies when* entry for unnamed rivals, after checking the gold |
```
