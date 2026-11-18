# Rulebook format

| Field | Type | Required | Meaning |
|---|---|---|---|
| `task` | string | yes | name of the labelling task |
| `version` | string | yes | change it whenever a rule changes |
| `multi_label` | bool | yes | whether one item may carry several labels |
| `empty_allowed` | bool | yes | whether an item may carry no label |
| `general` | list of text | no | rules that hold for every label |
| `labels` | list | yes | one entry per label, below |
| `precedence` | list | no | what to do when several labels fit: `{"labels": [ids], "rule": text}` |
| `sources` | text | no | where the rules come from (law, policy page, dataset paper) |

A label entry:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | letters, digits and `_ . # : / -` |
| `name` | text | no | a readable name |
| `definition` | text | yes | one or two sentences |
| `include` | list of text | no | typical cases where the label applies |
| `exclude` | list of text | lint warns if missing | look-alikes where it does not |
| `keywords` | list of strings, or lists by language | no | words that suggest the label (hints only) |
| `boundary` | list | no | `{"with": other id, "rule": text}`; shown from both labels |
| `applies_to` | list | no | the scopes (e.g. languages) where the label exists |
| `source` | text | no | the clause or section the label comes from |

"text" is a string or an object keyed by language: `{"en": "...", "zh": "..."}`. A list of text may also be keyed by language: `{"en": [...], "zh": [...]}`. The script falls back to English, then to any language present.

Writing good rules:

- Write **exclude** entries from real look-alikes: the items that were labelled wrongly. They do more for precision than a longer definition.
- Put the reason in the rule when it comes from a source ("SAMR guide §6(2)"), so a reviewer can check it.
- When a dataset has a convention that the definition does not show (for example, a general "the place is nice" counting as four ambience aspects), write it down as a rule with the evidence (how often the convention holds in the training data). An undocumented convention reads as label noise.
