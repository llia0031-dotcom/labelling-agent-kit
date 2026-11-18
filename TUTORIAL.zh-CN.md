# 接入一个新的标注任务

Agent、实验和分析的代码里不出现任何一个具体标签：一个项目特有的东西都放在 `tasks/` 下的一个文件夹里。这份教程一步一步接入一个新任务；仓库里的两个任务（`tasks/ad_policy/`、`tasks/asap/`）就是每个文件的完整样例。

[English](TUTORIAL.md)

## 1. 样本

每份样本一个 JSONL 文件：开发用 `items_dev.jsonl`，测试用 `items_test_a.jsonl` 和 `items_test_b.jsonl`。

```json
{"id": "ex-001", "text": "要标注的内容", "labels": ["LABEL_A"], "meta": {"lang": "zh", "source": "来源"}}
```

- `labels` 是标准标签：从数据集里取，或者在写样本时就定好；空列表表示不该有标签。
- 想按什么切片，就放进 `meta`（语言、来源、难度、市场）。
- 在改出的第二版定下来之前，测试集 B 不要动：只有它能如实衡量改版有没有用。

## 2. 规则本

`rules.json`：每个标签写定义、“适用”“不适用”和与其他标签的边界。格式见 [`skills/label-rules/references/rulebook-format.md`](skills/label-rules/references/rulebook-format.md)。

```bash
python skills/label-rules/scripts/label_rules.py tasks/my_task/rules.json lint
python skills/label-rules/scripts/label_rules.py tasks/my_task/rules.json show LABEL_A
```

“不适用”的条目从真实的“看起来像、其实不是”的样本里写，它对精确率的帮助比把定义写长更大。数据里有定义看不出来的标注习惯时，把它连同依据一起写下来，就像 `tasks/asap/rules.json` 写进了训练集里的统计（`tasks/asap/cues.json`）。

## 3. 案例库

`cases_*.jsonl`：Agent 检索用的带标签样例（绝不能是测试样本）。

```json
{"id": "case-0001", "text": "...", "labels": ["LABEL_A"], "source": "real"}
```

想知道某个说法一般标什么：`python skills/case-search/scripts/case_search.py tasks/my_task/cases_real.jsonl --phrase "某个说法"`。

## 4. 任务配置

`task.json`：

```json
{
  "name": "my_task", "title": "My labels", "item_noun": "post",
  "description": "Agent 会读的一两句话：一条样本是什么、要标什么。",
  "scope_field": null, "rule_lang": "zh",
  "sets": {"dev": "items_dev.jsonl", "test_a": "items_test_a.jsonl", "test_b": "items_test_b.jsonl"},
  "case_libraries": {"real": "cases_real.jsonl"}, "default_cases": "real",
  "prefetch_cases": 4, "prefetch_snippet": 0,
  "slices": ["meta.lang", "meta.source"], "length_field": "text"
}
```

- `scope_field`（例如 `meta.lang`）配合规则本里的 `applies_to`，让每条样本只看到对它适用的标签。
- `prefetch_cases` 是带案例的几组做法里，流程先检索几条相似案例；`prefetch_snippet` 把长案例截成最相关的那么多个字。

## 5. 数据验收

```bash
python -m lak.accept
```

`tasks/` 下每个有 `task.json` 的文件夹都会被检查。必过项一定要过：格式、标签表、语言、重复、和测试集的重叠、来源（见 [`DATA_ACCEPTANCE.zh-CN.md`](DATA_ACCEPTANCE.zh-CN.md)）。

## 6. 先在开发集上调，再冻结

```json
// experiments/my_dev.json
{"name": "my_dev", "runs": [{"task": "my_task", "set": "dev", "arms": [{"arm": "prompt-short"}, {"arm": "agent"}, {"arm": "agent-cases"}]}]}
```

```bash
python -m lak.run experiments/my_dev.json --mode batch --budget 0.2
python -m lak.analyze experiments/my_dev.json
python tools/inspect_run.py my_dev --items
```

改规则本和 `prompts/v1.json`，直到开发集上看着对了。然后写测试集 A 的实验文件和假设，冻结，冻结之后才跑：

```bash
python tools/freeze.py experiments/my_main.json --prompts v1
python -m lak.run experiments/my_main.json --mode batch --budget 1
python -m lak.analyze experiments/my_main.json
```

冻结的文件一旦变了，`lak.run` 就不肯开跑。

## 7. 失败样本、根因、改版

```bash
python -m lak.rca experiments/my_main.json --task my_task --set test_a --arm agent-cases --mode batch
```

每个错的标签判断都会带上线索，并归到一个根因：提示词缺陷、模型能力、规则冲突、样本分布、标签歧义。照根因表在 `prompts/v2.json` 或 `rules_v2.json` 里改，再在测试集 B 上用配对检验比较第一版和第二版（格式见 `experiments/revision.json`）。

## 8. 不用 Agent，单独用 Skill

`skills/` 里的五个 Skill 就是脚本加说明：能读 SKILL.md 的 Agent（Claude Code、Codex、DeerFlow），或者人，都可以拿自己的 JSONL 文件直接用。每个 Skill 的 `references/tutorial.md` 里有一个完整的例子。
