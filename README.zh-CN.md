# 标注 Agent 工具箱（Labelling Agent Kit）

一个内容标注 Agent：换一个标注任务，只要换一个放规则和案例的文件夹。配套一整套用证据调它的工具：预注册的 A/B 对照实验，每个标签的精确率、召回率和 F1（带区间），多标签混淆和切片分析，失败样本根因表，以及按根因改版后在没用过的样本上验证。常用的几样（指标、切片、混淆、案例检索、规则查询）做成了五个 Agent Skill，别的 Agent 也能直接调用。

[English](README.md) · [结果查看页](https://llia0031-dotcom.github.io/labelling-agent-kit/) · [评测报告（英文）](eval/EVALUATION.md)

## 在整套项目里的位置

这个项目属于同一组项目，主线是：AI 要拿出证据。

- **[Grounded Review（有据审核）](https://github.com/llia0031-dotcom/grounded-review)** 是广告审核 Agent：说出广告违反哪一条、原话是哪句。这里的两个任务之一用的是它公开的测试广告。
- **[Grounded Labelling Pipeline（有据标注流水线）](https://github.com/llia0031-dotcom/grounded-labelling-pipeline)** 是运营层：分流、复核队列、提示词版本、灰度、每周指标。它回答“核对过的答案怎么变成每天跑的流程”。
- **[Policy Model Lab（审核模型实验）](https://github.com/llia0031-dotcom/policy-model-lab)** 测广告审核需要看什么输入、用什么模型。它公开的数据（写好的广告、视频广告里的字、合成广告）是这里广告任务的来源。
- **这个工具箱是调优层。** 流水线负责把 Agent 跑起来；这里回答“Agent 怎么设计标得最好，在哪些标签、哪类样本上出错，为什么错，改了以后在新样本上还成不成立”，适用于任何标注任务，并把分析能力做成可复用的 Skill。

## 里面有什么

| 部分 | 做什么 | 在哪里 |
|---|---|---|
| Agent | 一套通用流程：检索相似案例，用规则和案例工具标注，规则门、原话修正、自查 | [`lak/agent.py`](lak/agent.py) |
| 两个任务 | 广告政策标签（中英文），和公开数据集 ASAP 的餐厅点评方面标签（18 个） | [`tasks/`](tasks/) |
| 实验 | 5 种做法、预注册的假设、冻结的文件、配对检验 | [`experiments/PREREGISTRATION.md`](experiments/PREREGISTRATION.md) |
| 根因 | 每个错的标签判断：先算线索，再归到提示词缺陷、模型能力、规则冲突、样本分布、标签歧义 | [`lak/rca.py`](lak/rca.py) |
| 数据 | 验收标准和检查；真实案例和合成案例的对比 | [`DATA_ACCEPTANCE.zh-CN.md`](DATA_ACCEPTANCE.zh-CN.md) |
| Skill | `label-metrics`、`slice-report`、`confusion-report`、`case-search`、`label-rules` | [`skills/`](skills/) |
| 查看页 | 各做法的结果、按标签看精确率和召回率的监控表、混淆矩阵、切片、带根因的失败样本、改版前后 | [`viewer/`](viewer/) |
| 教程 | 接入一个新的标注任务 | [`TUTORIAL.zh-CN.md`](TUTORIAL.zh-CN.md) |

## 结果

测试集 A，微平均 F1（广告 119 条、点评 201 条；[完整报告（英文）](eval/EVALUATION.md)）：

| 做法 | 广告 | 点评（ASAP） |
|---|---|---|
| 短提示词 | 0.768 | 0.715 |
| 整本规则放进提示词 | 0.878 | 0.782 |
| 会查规则的 Agent | 0.925 | 0.799 |
| 再加检索相似案例 | 0.965 | 0.812 |
| 再加自查 | **0.971** | **0.824** |

- **查规则是最大的一步**（比短提示词高 +0.157、+0.083）。广告上主要是精确率：短提示词给 32 条“像违规其实合规”的广告里的 12 条打了标签，完整的 Agent 是 0 条。
- **检索相似案例在两个任务上都有用**（+0.040、+0.014），虽然模型几乎从不自己去搜；起作用的是流程里固定的检索这一步。
- **自查只在点评上有用**（+0.012），每千条点评的费用从 0.91 美元升到 1.59 美元。
- **真实案例和合成案例**：没测出差别（+0.010 [-0.001, +0.022]）。
- **点评任务的根因**：406 个错误判断里，标签歧义 158、提示词缺陷 61、模型能力 20、规则冲突 18；两次独立归因有 257 个一致。这份数据的标准标签本身，限制了任何标注方能达到的上限。
- **按根因改出第二版，在没用过的样本上检验**：点评 +0.018 [+0.005, +0.031]（0.834 到 0.852），采用；广告 +0.021 [+0.000, +0.048]，区间碰到 0，不采用。
- **费用**：完整的 Agent 标 1,000 条点评 1.59 美元、1,000 条广告 0.53 美元（claude-haiku-5-5，批量接口）；整个项目的模型调用一共 3.6325 美元。

## 怎么运行

需要 Python 3.10 或更新版本。

```bash
pip install -r requirements.txt
python run_all.py --offline     # 用存下的回答重算所有表格、分析和查看页数据，再跑测试
```

`python run_all.py` 重跑实验，只发送还没存下回答的请求（走批量接口）。密钥从 `EVAL_ENV_FILE` 指的文件里读（一行 `ANTHROPIC_API_KEY=...`，见 `.env.example`）。

几个 Skill 只要有 Python 就能用：

```bash
python skills/label-metrics/scripts/label_metrics.py gold.jsonl pred.jsonl --compare pred_v2.jsonl
python skills/confusion-report/scripts/confusion_report.py gold.jsonl pred.jsonl
python skills/slice-report/scripts/slice_report.py gold.jsonl pred.jsonl --by meta.lang --length text
python skills/case-search/scripts/case_search.py cases.jsonl --phrase "环境一般"
python skills/label-rules/scripts/label_rules.py rules.json show ABSOLUTE
```

在 Claude Code 里把几个 Skill 装成插件（能读 SKILL.md 的其他 Agent 可以直接用 `skills/` 下的文件夹）：

```
/plugin marketplace add llia0031-dotcom/labelling-agent-kit
/plugin install label-metrics@labelling-agent-kit
/plugin install slice-report@labelling-agent-kit
/plugin install confusion-report@labelling-agent-kit
/plugin install case-search@labelling-agent-kit
/plugin install label-rules@labelling-agent-kit
```

从源数据重建任务文件：`tasks/asap/build.py download` 和 `sample`（从 GitHub 取 ASAP）；`tasks/ad_policy/build.py --src` 指向 Policy Model Lab 的 `data_public`。

## 数据和许可

- **ASAP**：Jiahao Bu 等，“ASAP: A Chinese Review Dataset Towards Aspect Category Sentiment Analysis and Rating Prediction”，NAACL 2021；[Meituan-Dianping/asap](https://github.com/Meituan-Dianping/asap)，Apache-2.0。仓库里只放抽到的点评（1,120 条），标签是数据集自带的。
- **广告样本和合成广告**：[Policy Model Lab](https://github.com/llia0031-dotcom/policy-model-lab) 的 `data_public`，MIT。每条广告的标签在写广告时就定好了。
- 代码和其余内容：MIT。
