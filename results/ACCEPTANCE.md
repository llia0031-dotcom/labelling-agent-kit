# Data acceptance

Rules and thresholds: DATA_ACCEPTANCE.md. B = blocking, W = warning.

## ad_policy / dev (items_dev.jsonl, 87 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 42 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, test_b |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A8 length within the real data's 1st-99th percentile for 95% of rows | W | pass | 98.9% within 24-287 characters |
| A9 each label's share within 10 points of the real data | W | pass | largest gaps: MEDICAL 5% vs 12%, GUARANTEE 16% vs 12%, DISPARAGE 9% vs 6% |

## ad_policy / test_a (items_test_a.jsonl, 119 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 52 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_b, dev |
| A7 every row states where it comes from | B | pass | 0 rows without a source |

## ad_policy / test_b (items_test_b.jsonl, 118 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 57 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, dev |
| A7 every row states where it comes from | B | pass | 0 rows without a source |

## ad_policy / cases:synthetic (cases_synth.jsonl, 600 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 262 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, test_b |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A8 length within the real data's 1st-99th percentile for 95% of rows | W | pass | 99.8% within 24-287 characters |
| A9 each label's share within 10 points of the real data | W | pass | largest gaps: BEFORE_AFTER 4% vs 0%, GUARANTEE 8% vs 12%, ALCOHOL 8% vs 5% |

## asap / dev (items_dev.jsonl, 120 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 0 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, test_b |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A8 length within the real data's 1st-99th percentile for 95% of rows | W | pass | 98.3% within 197-806 characters |
| A9 each label's share within 10 points of the real data | W | warn | largest gaps: Ambience#Noise 38% vs 27%, Ambience#Sanitary 40% vs 32%, Food#Recommend 23% vs 16% |
| A10 strong cue of a label that the row does not carry in at most 5% of rows | W | pass | 0 rows (0.0%) contain a phrase whose training-split precision for a missing label is >= 0.95 |

## asap / test_a (items_test_a.jsonl, 201 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 2 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_b, dev |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A10 strong cue of a label that the row does not carry in at most 5% of rows | W | pass | 7 rows (3.5%) contain a phrase whose training-split precision for a missing label is >= 0.95 |

## asap / test_b (items_test_b.jsonl, 199 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 0 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, dev |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A10 strong cue of a label that the row does not carry in at most 5% of rows | W | pass | 3 rows (1.5%) contain a phrase whose training-split precision for a missing label is >= 0.95 |

## asap / cases:real (cases_real.jsonl, 600 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 0 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, test_b |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A8 length within the real data's 1st-99th percentile for 95% of rows | W | pass | 98.2% within 197-806 characters |
| A9 each label's share within 10 points of the real data | W | pass | largest gaps: Service#Timely 13% vs 13%, Service#Queue 17% vs 17%, Service#Parking 6% vs 6% |
| A10 strong cue of a label that the row does not carry in at most 5% of rows | W | pass | 7 rows (1.2%) contain a phrase whose training-split precision for a missing label is >= 0.95 |

## asap / cases:synthetic (cases_synth.jsonl, 600 rows): accepted

| Check | | Result | Detail |
|---|---|---|---|
| A1 schema: unique id, text, label list | B | pass | 0 malformed rows, 0 duplicate ids |
| A2 labels exist in the rulebook and fit the item's scope | B | pass | 0 rows with unknown labels, 0 with a label outside the item's scope |
| A3 empty-label rows only where the rulebook allows them | B | pass | 0 rows without a label; rulebook allows them |
| A4 text is in the stated language | B | pass | 0 rows in another language |
| A5 no exact duplicates; near duplicates at most 1% | B | pass | 0 exact duplicate texts; 0 near duplicates (0.0%, character 5-gram Jaccard >= 0.6) |
| A6 no overlap with the frozen test sets | B | pass | 0 pairs with character 8-gram Jaccard >= 0.3 against test_a, test_b |
| A7 every row states where it comes from | B | pass | 0 rows without a source |
| A8 length within the real data's 1st-99th percentile for 95% of rows | W | warn | 59.0% within 197-806 characters |
| A9 each label's share within 10 points of the real data | W | pass | largest gaps: Location#Transportation 19% vs 24%, Food#Recommend 20% vs 16%, Food#Appearance 27% vs 23% |
| A10 strong cue of a label that the row does not carry in at most 5% of rows | W | pass | 0 rows (0.0%) contain a phrase whose training-split precision for a missing label is >= 0.95 |
