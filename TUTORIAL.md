# Plug in a new labelling task

The agent, the experiments and the analysis never name a label: everything specific to a project lives in one folder under `tasks/`. This walk-through adds a task step by step; the two tasks in the repository (`tasks/ad_policy/`, `tasks/asap/`) are complete examples of every file.

[中文](TUTORIAL.zh-CN.md)

## 1. Items

One JSONL file per set: `items_dev.jsonl` for development, `items_test_a.jsonl` and `items_test_b.jsonl` for testing.

```json
{"id": "ex-001", "text": "the content to label", "labels": ["LABEL_A"], "meta": {"lang": "en", "source": "where it came from"}}
```

- `labels` are the gold labels. Take them from the dataset or fix them when the item is written; an empty list means no label applies.
- Put anything you want to slice by under `meta` (language, source, difficulty, market).
- Keep test B untouched until your revised version is fixed: it is the only set that measures a revision honestly.

## 2. Rulebook

`rules.json`: a definition, *applies when*, *does not apply when* and boundaries for every label. Format: [`skills/label-rules/references/rulebook-format.md`](skills/label-rules/references/rulebook-format.md).

```bash
python skills/label-rules/scripts/label_rules.py tasks/my_task/rules.json lint
python skills/label-rules/scripts/label_rules.py tasks/my_task/rules.json show LABEL_A
```

Write the *does not apply* entries from real look-alikes; they do more for precision than a longer definition. If the data has a convention that the definitions do not show, write it down with the evidence, as `tasks/asap/rules.json` does with counts from the training split (`tasks/asap/cues.json`).

## 3. Case library

`cases_*.jsonl`: labelled examples the agent retrieves (never test items).

```json
{"id": "case-0001", "text": "...", "labels": ["LABEL_A"], "source": "real"}
```

Check what a phrase usually gets: `python skills/case-search/scripts/case_search.py tasks/my_task/cases_real.jsonl --phrase "some phrase"`.

## 4. Task config

`task.json`:

```json
{
  "name": "my_task", "title": "My labels", "item_noun": "post",
  "description": "One or two sentences the agent reads: what an item is and what to label.",
  "scope_field": null, "rule_lang": "en",
  "sets": {"dev": "items_dev.jsonl", "test_a": "items_test_a.jsonl", "test_b": "items_test_b.jsonl"},
  "case_libraries": {"real": "cases_real.jsonl"}, "default_cases": "real",
  "prefetch_cases": 4, "prefetch_snippet": 0,
  "slices": ["meta.lang", "meta.source"], "length_field": "text"
}
```

- `scope_field` (e.g. `meta.lang`) together with `applies_to` in the rulebook gives each item only the labels that exist for it.
- `prefetch_cases` is how many similar cases the flow retrieves for the case arms; `prefetch_snippet` shortens long cases to that many characters around the best match.

## 5. Data acceptance

```bash
python -m lak.accept
```

Every folder under `tasks/` with a `task.json` is checked. Blocking checks must pass: schema, label vocabulary, language, duplicates, overlap with the test sets, provenance ([`DATA_ACCEPTANCE.md`](DATA_ACCEPTANCE.md)).

## 6. Develop on dev, then freeze

```json
// experiments/my_dev.json
{"name": "my_dev", "runs": [{"task": "my_task", "set": "dev", "arms": [{"arm": "prompt-short"}, {"arm": "agent"}, {"arm": "agent-cases"}]}]}
```

```bash
python -m lak.run experiments/my_dev.json --mode batch --budget 0.2
python -m lak.analyze experiments/my_dev.json
python tools/inspect_run.py my_dev --items
```

Change the rulebook and `prompts/v1.json` until dev looks right. Then write the experiment for test A with its hypotheses, freeze it, and only then run it:

```bash
python tools/freeze.py experiments/my_main.json --prompts v1
python -m lak.run experiments/my_main.json --mode batch --budget 1
python -m lak.analyze experiments/my_main.json
```

`lak.run` refuses to start if a frozen file changed.

## 7. Failures, root causes, revision

```bash
python -m lak.rca experiments/my_main.json --task my_task --set test_a --arm agent-cases --mode batch
```

Each wrong label decision gets its signals and a root cause (prompt defect, model capability, rule conflict, sample distribution, label ambiguity). Fix what the table points to in `prompts/v2.json` or `rules_v2.json`, then compare v1 and v2 on test B with a paired test (`experiments/revision.json` shows the shape).

## 8. Use the skills without the agent

The five skills in `skills/` are plain scripts plus instructions; any agent that reads SKILL.md files (Claude Code, Codex, DeerFlow) or a person can use them on their own JSONL files. Each has a worked example in its `references/tutorial.md`.
