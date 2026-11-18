"""Synthetic restaurant reviews for the real-versus-synthetic case-library comparison.

Each spec copies the aspect set and the sentiment of each aspect from a randomly drawn training review
(seed 20261118), so the synthetic library has the same label distribution as the real one. The generator
gets the same rulebook the labelling agent gets and is asked for a review of a fictional restaurant that
mentions exactly those aspects with those sentiments and no other aspect. The labels of a synthetic
review are the aspects of its spec. Generation uses claude-haiku-5-5 through the Message Batches API.

    python tasks/asap/synth.py generate --mode batch     # about USD 0.1; answers stored in results/synth-asap/
    python tasks/asap/synth.py build                     # acceptance checks -> cases_synth.jsonl + synth_report.json

Filters (lak/accept.py runs the same checks on every data file): the answer parses; the review is Chinese
and 120-600 characters; every evidence quote is verbatim; no strong cue of an aspect outside the spec
(a phrase whose training-split precision for that aspect is at least 0.95, from cues.json); not a near
duplicate of another synthetic review (character 5-gram Jaccard >= 0.6) or of any dev or test review
(character 8-gram Jaccard >= 0.3). The first 600 accepted reviews, in spec order, form the library.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from lak import llm  # noqa: E402
from lak.task import get_task, read_jsonl  # noqa: E402

SEED = 20261118
N_SPECS = 700
N_KEEP = 600
STORE = ROOT / "results" / "synth-asap" / "responses.jsonl"
POL = {1: "正面", 0: "中性（轻微的好或不好）", -1: "负面"}
STYLES = ["朋友聚餐后写的长评", "一个人吃饭的简短打卡", "带家人吃饭的流水账", "吃货的逐道菜点评", "第一次来的探店笔记", "老顾客的回访评价", "下班后随手写的几句", "约会后的点评"]
CUISINES = ["川菜", "粤菜", "火锅", "日料", "烧烤", "西餐", "东北菜", "本帮菜", "湘菜", "茶餐厅", "自助餐", "面馆", "烤鸭", "海鲜", "甜品店", "小龙虾"]


def specs() -> list[dict]:
    sys.path.insert(0, str(HERE))
    import build  # noqa: E402
    train = sorted(build.read_split("train"), key=lambda r: r["id"])
    rng = random.Random(SEED)
    picked = rng.sample(train, N_SPECS)
    return [{"sid": f"synth-{n:04d}", "aspects": r["meta"]["polarity"], "style": rng.choice(STYLES), "cuisine": rng.choice(CUISINES)}
            for n, r in enumerate(picked)]


SYSTEM = """你为一个标注项目写合成的大众点评餐厅点评。点评要像真实用户写的：口语、具体、有细节，可以有错别字和网络用语。餐厅和菜名都是虚构的，不要用真实品牌。

标注规则（这个项目的标签只按这些规则判断）：
{rules}

要求：点评必须提到下面列出的每个方面，并且情感符合要求；不能提到列表以外的任何方面（按上面的规则判断，例如笼统评价“环境”会同时算装修、嘈杂、空间、卫生四个方面）。字数 150 到 400 个汉字。

只输出一个 JSON 对象：{{"review": "<点评正文>", "evidence": [{{"aspect": "<方面标签>", "quote": "<点评里体现这个方面的原话>"}}]}}，evidence 要覆盖每个要求的方面，原话必须一字不差地出现在点评里。"""


def request(spec: dict, rules: str) -> dict:
    lines = [f"- {a}：{POL[p]}" for a, p in spec["aspects"].items()]
    user = (f"写一条{spec['cuisine']}餐厅的点评，风格：{spec['style']}。\n必须提到的方面和情感：\n" + "\n".join(lines))
    return {"system": [{"type": "text", "text": SYSTEM.format(rules=rules), "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": user}],
            "output_config": {"format": {"type": "json_schema", "schema": {
                "type": "object", "properties": {"review": {"type": "string"}, "evidence": {"type": "array", "items": {
                    "type": "object", "properties": {"aspect": {"type": "string"}, "quote": {"type": "string"}},
                    "required": ["aspect", "quote"], "additionalProperties": False}}},
                "required": ["review", "evidence"], "additionalProperties": False}}}}


def job(spec: dict, rules: str):
    resp = yield request(spec, rules)
    data, why = llm.final_json(resp)
    return {"sid": spec["sid"], "spec": spec, "data": data, "error": why,
            "cost_usd": llm.cost_of(resp.get("usage", {}), resp.get("pricing", "batch")) if "usage" in resp else 0.0}


def generate(mode: str) -> None:
    task = get_task("asap")
    rules = task.rules_text({"id": "x", "text": ""}, task.all_labels)
    engine = llm.Engine(STORE, mode=mode, budget_usd=0.5)
    out = engine.run({s["sid"]: job(s, rules) for s in specs()})
    rows = [out[k] for k in sorted(out)]
    path = STORE.parent / "generated.jsonl"
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(f"{len(rows)} generated, {sum(1 for r in rows if r['data'] is None)} unparsed, cost ${sum(r['cost_usd'] for r in rows):.4f}")


def build_library() -> None:
    from lak import accept
    task = get_task("asap")
    rows = read_jsonl(STORE.parent / "generated.jsonl")
    cues = json.loads((HERE / "cues.json").read_text(encoding="utf-8"))["labels"]
    strong = {l: [c["phrase"] for c in v["cues"] if c["precision"] >= 0.95] for l, v in cues.items()}
    refs = [r["text"] for s in ("dev", "test_a", "test_b") for r in task.items(s)]
    ref_grams = [accept.grams(t, 8) for t in refs]
    kept, report = [], {"generated": len(rows), "rejected": {}}
    seen_grams = []

    def reject(why: str) -> None:
        report["rejected"][why] = report["rejected"].get(why, 0) + 1

    for r in rows:
        d = r["data"]
        if not d or not isinstance(d.get("review"), str):
            reject("unparsed"); continue
        text = " ".join(d["review"].split())
        labels = [a for a in task.all_labels if a in r["spec"]["aspects"]]
        if not accept.is_chinese(text) or not 120 <= len(text) <= 600:
            reject("language or length"); continue
        ev = {e.get("aspect"): " ".join(str(e.get("quote", "")).split()) for e in (d.get("evidence") or []) if isinstance(e, dict)}
        if any(a not in ev for a in labels) or any(not q or q not in text for q in ev.values()):
            reject("evidence missing or not verbatim"); continue
        if any(p in text for l, ps in strong.items() if l not in labels for p in ps):
            reject("strong cue of an aspect outside the spec"); continue
        g5 = accept.grams(text, 5)
        if any(accept.jaccard(g5, s) >= 0.6 for s in seen_grams):
            reject("near duplicate of another synthetic review"); continue
        g8 = accept.grams(text, 8)
        if any(accept.jaccard(g8, s) >= 0.3 for s in ref_grams):
            reject("close to a dev or test review"); continue
        seen_grams.append(g5)
        kept.append({"id": r["sid"], "text": text, "labels": labels, "source": "synthetic"})
        if len(kept) >= N_KEEP:
            break
    report["accepted_before_cap"] = len(kept)
    report["kept"] = len(kept)
    report["cost_usd"] = round(sum(r["cost_usd"] for r in rows), 5)
    (HERE / "cases_synth.jsonl").write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kept), encoding="utf-8", newline="\n")
    (HERE / "synth_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["generate", "build"])
    ap.add_argument("--mode", default="offline", choices=["batch", "direct", "offline"])
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    generate(a.mode) if a.command == "generate" else build_library()
