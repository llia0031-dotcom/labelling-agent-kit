# Skills

Five Agent Skills for labelling work. Each folder is self-contained: `SKILL.md` (when and how to use it), `scripts/` (Python 3.9+, standard library only), `references/` (definitions and a tutorial with real outputs) and, for the three analysis skills, `examples/` to try it on.

| Skill | Question it answers | Script |
|---|---|---|
| [`label-metrics`](label-metrics/) | How good is this run, per label, and is run B really better than run A? | `label_metrics.py gold.jsonl pred.jsonl [--compare pred_b.jsonl]` |
| [`confusion-report`](confusion-report/) | What is each label mistaken for, and which items show it? | `confusion_report.py gold.jsonl pred.jsonl` |
| [`slice-report`](slice-report/) | Is the labeller weaker on a language, a source, long items, one label? | `slice_report.py gold.jsonl pred.jsonl --by meta.lang --length text` |
| [`case-search`](case-search/) | How were similar items labelled, and what does a phrase usually get? | `case_search.py cases.jsonl --query "..."` / `--phrase "..."` |
| [`label-rules`](label-rules/) | What exactly does the rule say, and where do two labels part? | `label_rules.py rules.json show LABEL` / `between A B` / `lint` |

The labelling agent in this repository calls the same functions as its tools (`lak/task.py`), and its evaluation runs through the same scripts (`lak/analyze.py`), so what an agent or a person gets from a skill is exactly what the experiments used. The scripts are tested against scikit-learn, statsmodels and rank_bm25 (`tests/test_skill_scripts.py`).

Install in Claude Code: `/plugin marketplace add llia0031-dotcom/labelling-agent-kit`, then `/plugin install <skill>@labelling-agent-kit`.
