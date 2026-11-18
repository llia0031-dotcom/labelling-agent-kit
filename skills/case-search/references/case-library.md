# Case library format and search details

One JSON object per line:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes (else the line number) | unique id |
| `text` | yes | the case content |
| `labels` | no (empty list) | gold labels of the case; a single string is read as one label |
| `source` | no | where the case comes from, e.g. `real` or `synthetic` |
| `note` | no | a reviewer's note |

Other field names: `--text-field`, `--label-field`, `--id-field`.

## Tokens

- Latin script: lower-cased words and numbers (`world's`, `best`, `2025`).
- Chinese, Japanese, Korean: every character and every pair of adjacent characters (`床垫` gives `床`, `垫`, `床垫`). Pairs catch most two-character words without a segmenter; single characters keep recall for rare words.

## Scoring

BM25 Okapi with k1 = 1.5, b = 0.75 and rank_bm25's floor for negative inverse document frequencies (terms in more than half the cases get a small positive weight instead of a negative one). Ties are broken by library order, so results are deterministic.

## Phrase statistics

`--phrase` is an exact, case-insensitive substring match over the case texts. It returns the number of matching cases, the share carrying each label, how many carry no label, and up to three short examples centred on the phrase. Use it for conventions ("what do cases saying X get?"), not for similarity.

## Building a library

- Use training or reference data only; never the items you will evaluate on.
- Keep the label distribution close to the data you will label, or note where it differs.
- Mark synthetic cases with `"source": "synthetic"`: they show what their generator thought the labels meant.
- Run the data acceptance checks (duplicates, overlap with test sets, label vocabulary) before use.
