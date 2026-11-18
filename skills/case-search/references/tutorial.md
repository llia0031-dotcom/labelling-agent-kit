# Tutorial: precedents for a borderline item, and a dataset convention

Files: the repository's two case libraries, `tasks/ad_policy/cases_synth.jsonl` (600 synthetic ads) and `tasks/asap/cases_real.jsonl` (600 real Dianping reviews from ASAP's training split). All outputs below are copied from real runs.

## 1. How were similar items labelled?

The ad to label says "Reapply every 2 hours for best results." Search the ad library:

```bash
python scripts/case_search.py tasks/ad_policy/cases_synth.jsonl --query "Reapply every 2 hours for best results" -k 4
```

```text
| # | Labels | Case | Score | Id |
|---|---|---|---|---|
| 1 | (no label) | Glowmist Daily Shield offers broad-spectrum protection ... reapply every two hours for best results. | 30.50 | case-0181 |
| 2 | (no label) | Quill Harbor Savings is proud to serve you with the best customer support hours in our region, ... | 11.81 | case-0108 |
| 3 | ABSOLUTE | - Lumen Code Academy: the best coding bootcamp for career changers in the region. ... | 10.52 | case-0336 |
| 4 | GUARANTEE | Try GummyGlow Daily Vitamins today ... Guaranteed results, every time! | 10.33 | case-0243 |
```

The closest case uses the same usage advice and carries no label; case 3 shows what does get ABSOLUTE (a superlative about the product). The deciding difference is whether "best" ranks the product or describes how to use it, which is exactly the rulebook's exclusion.

## 2. What does a phrase usually get?

In ASAP, does "位置很好" ("the location is great") count as *easy to find*, *transport* or *near a commercial centre*?

```bash
python scripts/case_search.py tasks/asap/cases_real.jsonl --phrase "位置很好"
```

```text
**5 of 600 cases contain "位置很好".** Share carrying each label (no label: 0):

- Food#Taste: 5 (100%)
- Location#Easy_to_find: 4 (80%)
- Location#Transportation: 3 (60%)
...
```

Five cases is an anecdote, not a convention; the training-split count in `tasks/asap/cues.json` (thousands of reviews) is what the rulebook cites. Report the count with every share.

## 3. Use it inside an agent

In this repository the flow retrieves the closest cases for every item before the model answers (`Task.prefetch_cases`), and the model can call `phrase_stats` and `search_cases` itself. Both use this script's `CaseIndex` and `phrase_stats`. The test item is excluded from its own search, and the case libraries pass the overlap check against the test sets (`DATA_ACCEPTANCE.md`, check A6).
