# Example files

- `gold.jsonl`: the 86 ad-policy development items of this repository (Chinese and English ad texts) with labels fixed when each ad was written, and `meta` fields for slicing (language, source, difficulty).
- `pred_short.jsonl`, `pred_rules.jsonl`: the labels two one-shot prompts gave these items in a development run (`claude-haiku-5-5`): a short prompt with the label list only, and the same prompt with the whole rulebook.
