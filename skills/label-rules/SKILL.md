---
name: label-rules
description: Looks up labelling rules from a JSON rulebook - what a label means, when it applies and when it does not, the boundary between two labels, which labels a text's keywords point to - and checks a rulebook for gaps and contradictions. Use it whenever an agent or a person labels content against a policy or a codebook, needs the exact rule for a borderline item, is writing or revising a labelling guideline, or asks "what is the rule for label X", "what's the difference between A and B", "check my labelling guideline", "这个标签的规则是什么", "A 和 B 怎么区分", "检查一下标注规范". A bundled script reads the rulebook so the rule text is quoted, never paraphrased from memory.
metadata:
  version: "0.1.0"
---

# Label rules

Labelling quality depends on the rule being applied, not remembered. Keep the rules in one rulebook file and look them up: the definition, the cases where the label applies, the cases where it does not (the look-alikes), and the boundary with neighbouring labels.

## The rulebook

One JSON file per labelling task. Format in `references/rulebook-format.md`; the essentials:

```json
{"task": "ad_policy", "version": "1.0", "multi_label": true, "empty_allowed": true,
 "general": ["Judge what the ad actually claims about the product."],
 "labels": [{"id": "ABSOLUTE", "name": "Absolute claim", "definition": "...",
             "include": ["..."], "exclude": ["usage advice such as 'for best results'"],
             "keywords": ["best", "No. 1"], "boundary": [{"with": "DATA", "rule": "..."}],
             "applies_to": ["zh", "en"]}],
 "precedence": [{"labels": ["ABSOLUTE", "DATA"], "rule": "..."}]}
```

Any text can be bilingual: `{"en": "...", "zh": "..."}`. `applies_to` limits a label to some items (a language, a market).

## Run the script

```bash
python <this-skill-folder>/scripts/label_rules.py rules.json list --lang en
python <this-skill-folder>/scripts/label_rules.py rules.json show ABSOLUTE MEDICAL --lang zh --scope zh
python <this-skill-folder>/scripts/label_rules.py rules.json between ABSOLUTE DATA
python <this-skill-folder>/scripts/label_rules.py rules.json match --text "the world's best mattress" --scope en
python <this-skill-folder>/scripts/label_rules.py rules.json search "before and after"
python <this-skill-folder>/scripts/label_rules.py rules.json lint
```

Python 3.9+, standard library only. `show` includes boundary notes written under the other label and the precedence rules for the pair. `match` lists labels whose keywords occur (whole words for Latin keywords): a hint for candidates, never a decision. Exit codes: 0 found or lint passed; 1 nothing found or lint problems; 2 unreadable rulebook or unknown label.

## Label with the rules

1. List candidate labels for the item (`match` helps you not miss one).
2. `show` every candidate; read **does not apply** first: look-alikes are where labellers fail.
3. For two candidates that both fit, `between A B`; follow the precedence rule if there is one.
4. Keep a label only with the item's own words as evidence.
5. If no rule decides the item, say so and propose the missing sentence; do not invent a rule silently.

## Maintain the rulebook

Run `lint` after every edit: it checks ids, required fields, unknown labels in boundaries and precedence, labels with no "does not apply" entry, and whether multi-label and empty items are allowed. Give the rulebook a new version number when a rule changes, so results stay tied to the rules that produced them, and add the items that motivated the change to a regression set.
