# Labelling Agent Kit

A content-labelling agent that plugs into any labelling task through a folder of rules and cases, and the kit to tune it with evidence: preregistered A/B experiments, precision, recall and F1 for every label with intervals, multi-label confusion and slice analysis, a root-cause table of failures, and a revision checked on items it never saw. The everyday pieces (metrics, slices, confusion, case search, rule lookup) are five Agent Skills any agent can call.

[中文说明](README.zh-CN.md) · [Results viewer](https://llia0031-dotcom.github.io/labelling-agent-kit/) · [Evaluation report](eval/EVALUATION.md)

## Where this fits

This project belongs to a set of projects built on one idea: an AI should show its evidence.

- **[Grounded Review](https://github.com/llia0031-dotcom/grounded-review)** is the ad-review agent: it names the clause an ad breaks and quotes the words. One of the two tasks here uses its public test ads.
- **[Grounded Labelling Pipeline](https://github.com/llia0031-dotcom/grounded-labelling-pipeline)** is the operations layer: routing, a review queue, prompt versions, canary release and weekly metrics. It answers *how a checked answer becomes a daily workflow*.
- **[Policy Model Lab](https://github.com/llia0031-dotcom/policy-model-lab)** tests which inputs and which models an ad check needs. Its public data (written ads, video-ad words, synthetic ads) is the ad-policy task's source here.
- **This kit is the tuning layer.** The pipeline runs an agent; this kit asks *which design of the agent labels best, on which labels and slices it fails, why, and whether a fix holds on new items*, for any labelling task, and packages the analysis as reusable skills.

## What is in it

| Part | What it does | Where |
|---|---|---|
| Agent | one generic flow: retrieve similar cases, label with rule and case tools, rule gate, quote repair, self-check | [`lak/agent.py`](lak/agent.py) |
| Two tasks | ad-policy labels (Chinese and English) and restaurant-review aspects from the public ASAP dataset (18 labels) | [`tasks/`](tasks/) |
| Experiments | 5 arms, preregistered hypotheses, frozen files, paired tests | [`experiments/PREREGISTRATION.md`](experiments/PREREGISTRATION.md) |
| Root causes | each wrong label decision: signals, then prompt defect / model capability / rule conflict / sample distribution / label ambiguity | [`lak/rca.py`](lak/rca.py) |
| Data | acceptance standard and checks; a real-versus-synthetic case-library comparison | [`DATA_ACCEPTANCE.md`](DATA_ACCEPTANCE.md) |
| Skills | `label-metrics`, `slice-report`, `confusion-report`, `case-search`, `label-rules` | [`skills/`](skills/) |
| Viewer | per-arm results, a per-label precision and recall monitor, confusion, slices, failures with root causes, the revision | [`viewer/`](viewer/) |
| Tutorial | plug in a new labelling task | [`TUTORIAL.md`](TUTORIAL.md) |

## What it found

Test A, micro F1 (119 ads, 201 reviews; [full report](eval/EVALUATION.md)):

| Arm | Ads | ASAP |
|---|---|---|
| Short prompt | 0.768 | 0.715 |
| Whole rulebook in the prompt | 0.878 | 0.782 |
| Agent that reads the rules | 0.925 | 0.799 |
| + retrieved similar cases | 0.965 | 0.812 |
| + self-check | **0.971** | **0.824** |

- **Reading the rules is the largest step** (+0.157 on ads, +0.083 on ASAP over the short prompt). On ads it is mostly precision: the short prompt gave a label to 12 of 32 look-alike ads, the full agent to 0 of 32.
- **Retrieved cases help on both tasks** (+0.040 and +0.014), though the model almost never searched by itself; the fixed retrieval step carries it.
- **The self-check helps only on ASAP** (+0.012) and raises the cost per 1,000 reviews from USD 0.91 to 1.59.
- **Real against synthetic cases:** no measured difference (+0.010 [-0.001, +0.022]).
- **Root causes on ASAP:** of 406 wrong label decisions, 158 are label ambiguity, 61 prompt defects, 20 model capability and 18 rule conflicts; the two independent passes agree on 257. The gold labels bound what any labeller can reach here.
- **Revision from the root causes, checked on held-out items:** on ASAP, +0.018 [+0.005, +0.031] (0.834 to 0.852), adopted; on ads, +0.021 [+0.000, +0.048], an interval that reaches 0, so not adopted.
- **Cost:** the full agent labels 1,000 reviews for USD 1.59 and 1,000 ads for USD 0.53 (claude-haiku-5-5, Message Batches); every model call of the project came to USD 3.6325.

## Run it

Python 3.10 or later.

```bash
pip install -r requirements.txt
python run_all.py --offline     # rebuild every table, analysis and the viewer data from the stored answers, then run the tests
```

`python run_all.py` reruns the experiments, sending only the requests whose answers are not stored (Message Batches API). The key is read from the file named by `EVAL_ENV_FILE` (a line `ANTHROPIC_API_KEY=...`, see `.env.example`).

The skills need nothing but Python:

```bash
python skills/label-metrics/scripts/label_metrics.py gold.jsonl pred.jsonl --compare pred_v2.jsonl
python skills/confusion-report/scripts/confusion_report.py gold.jsonl pred.jsonl
python skills/slice-report/scripts/slice_report.py gold.jsonl pred.jsonl --by meta.lang --length text
python skills/case-search/scripts/case_search.py cases.jsonl --phrase "环境一般"
python skills/label-rules/scripts/label_rules.py rules.json show ABSOLUTE
```

Install the skills in Claude Code as plugins (other agents that read SKILL.md files can use the `skills/` folders directly):

```
/plugin marketplace add llia0031-dotcom/labelling-agent-kit
/plugin install label-metrics@labelling-agent-kit
/plugin install slice-report@labelling-agent-kit
/plugin install confusion-report@labelling-agent-kit
/plugin install case-search@labelling-agent-kit
/plugin install label-rules@labelling-agent-kit
```

To rebuild the task files from their sources: `tasks/asap/build.py download` and `sample` (ASAP from GitHub), and `tasks/ad_policy/build.py --src` pointing at Policy Model Lab's `data_public`.

## Data and licences

- **ASAP**: Jiahao Bu et al., "ASAP: A Chinese Review Dataset Towards Aspect Category Sentiment Analysis and Rating Prediction", NAACL 2021; [Meituan-Dianping/asap](https://github.com/Meituan-Dianping/asap), Apache-2.0. Only the sampled reviews (1,120) are included; their labels are the dataset's.
- **Ad items and synthetic ads**: [Policy Model Lab](https://github.com/llia0031-dotcom/policy-model-lab) `data_public`, MIT. Labels were fixed when each ad was written.
- Code and everything else: MIT.
