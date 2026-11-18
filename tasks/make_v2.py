"""Builds the revised rulebooks (rules_v2.json) and prompt (prompts/v2.json) from version 1.

Every change answers a group of failures in the root-cause tables of the best v1 arm on test A
(results/main/rca/*.md); experiments/REVISION.md lists each change with the failures behind it.
Training-split statistics quoted in the ASAP rules are in tasks/asap/v2_train_stats.txt.

    python tasks/make_v2.py
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, d: dict) -> None:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def label(book: dict, lid: str) -> dict:
    return next(l for l in book["labels"] if l["id"] == lid)


def asap() -> None:
    src = ROOT / "tasks" / "asap" / "rules.json"
    b = copy.deepcopy(load(src))
    b["version"] = "2.0"
    # R1: the general "judged aspects only" rule was too strict for the dataset's conventions (rule conflict, prompt defect)
    b["general"]["zh"][1] = (
        "只标点评人对这个方面有所交代的地方（好、不好、“还行”“一般”这样的轻微评价都算）。纯粹的过程叙述不标，例如“点了七个菜”“几点到的”。"
        "数据集的习惯（训练集统计）：下面三类即使没有明显评价也标——店在商场、广场、百货、商厦、商业街里或旁边，标 Location#Downtown（含这些词的点评 82% 带它）；"
        "用了或提到团购、券、优惠、霸王餐、免费试吃，标 Price#Discount（85%、80%；这个标签 49% 是中性）；写了人均或一共花了多少钱，标 Price#Level（94%）。")
    b["general"]["en"][1] = (
        "Label what the reviewer tells about an aspect (good, bad, or mild such as \"OK\" or \"average\"). Plain narration is not labelled, "
        "for example \"ordered seven dishes\" or \"arrived at seven\". Dataset conventions (training-split statistics): three kinds are labelled "
        "even without a clear judgement: the restaurant is in or next to a mall, plaza, department store or commercial street (Location#Downtown, "
        "82% of reviews with these words); a group deal, voucher, offer, free trial meal or 霸王餐 is used or mentioned (Price#Discount, 85% and 80%; "
        "49% of this label is neutral); the spend per person or the bill is stated (Price#Level, 94%).")
    # R2: general environment verdicts and the self-check removing them (prompt defect)
    b["general"]["zh"].insert(2, "笼统评价环境（“环境很好”“环境一般”“环境优雅”“整体环境几星”）时，装修、嘈杂、空间、卫生四个都标，即使后面又具体说了其中一项；自查时不要因为没有具体细节就删掉其中几个。")
    b["general"]["en"].insert(2, "A general verdict on the surroundings (\"环境很好\", \"环境一般\", \"环境优雅\", a star rating for the surroundings) gets all four Ambience labels, even when one of them is also described specifically; the self-check must not drop some of them for lack of detail.")
    # R3: Price#Level against Price#Cost_effective (largest confusion)
    lv = label(b, "Price#Level")
    lv["include"]["zh"] = ["说价钱高低的任何说法：价格（91%）、贵（91%）、便宜（含“便宜”而没有“性价比、值”字样的点评 87% 带此标签）、人均多少（94%）、价位、实惠（81%）、“才 10 元”“这么便宜”。",
                           "写出花了多少钱，或某道菜多少钱，并带一点评价（“有点贵”“可以接受”）。"]
    lv["include"]["en"] = ["Any word on how high or low prices are: price, expensive, cheap (87% of reviews that say 便宜 without value-for-money words), per-person spend (94%), price range, affordable (81%), \"only 10 yuan\".",
                           "An amount spent, or a dish price, with a comment on it."]
    ce = label(b, "Price#Cost_effective")
    ce["include"]["zh"] = ["把价钱和东西好坏放在一起说：性价比（96%）、物超所值、值这个价、不值、超值（68%）、划算（68%）。"]
    ce["include"]["en"] = ["Price weighed against what you get: value for money (96%), worth the price, not worth it, great value (68%), a good deal (68%)."]
    ce["exclude"]["zh"] = ["只说便宜、不贵、价格合理，没有和东西好坏比：标 Price#Level，不标性价比（含“便宜”而没有“性价比、值”的点评只有 19% 带性价比）。",
                           "“这个价位这个水平”“贵但能接受”这类只是价格判断。",
                           "对点菜的建议（“人多来点套餐合适”）不算性价比。"]
    ce["exclude"]["en"] = ["Only cheap, not expensive, reasonable, with no weighing against quality: Price#Level, not Cost_effective (19% of reviews with 便宜 and no value words carry it).",
                           "\"For this price, this level\" or \"expensive but acceptable\" is a price judgement only.",
                           "Advice on what to order (\"a set menu suits a group\") is not value for money."]
    lv["boundary"] = [{"with": "Price#Cost_effective", "rule": {
        "zh": "说价钱高低标价格水平；把价钱和东西好坏比才加性价比。“性价比”“实惠”“划算”常常两个都标（含“性价比”的点评 67% 也带价格水平），只说“便宜”只标价格水平。",
        "en": "Price high or low is Price#Level; add Cost_effective only when price is weighed against quality. 性价比, 实惠 and 划算 often get both (67% of reviews with 性价比 also carry Price#Level); 便宜 alone gets Price#Level only."}},
        {"with": "Price#Discount", "rule": {"zh": "团购、优惠券、打折是折扣；团购价后面评价了便宜或贵，再加价格水平。", "en": "Group deals, coupons and discounts are Discount; add Price#Level if the price is also judged."}}]
    # R4: location and discount cues missed (prompt defect, rule conflict)
    dt = label(b, "Location#Downtown")
    dt["include"]["zh"] = ["店在某某广场（84%）、商场（77%）、百货、商厦、商业街、商业区、购物中心、步行街里或旁边，或在市中心、商圈。只写了“在某某商场几楼”也标。"]
    dt["include"]["en"] = ["The restaurant is inside or next to a named plaza, mall, department store, commercial building or street, shopping centre or pedestrian street, or in the city centre. \"On floor 3 of X mall\" counts."]
    dt["keywords"] = dt["keywords"] + ["商厦", "商业区", "大厦"]
    dc = label(b, "Price#Discount")
    dc["include"]["zh"] = dc["include"]["zh"] + ["用了或提到团购、券、优惠、霸王餐、免费试吃、积分兑换，即使没有评价力度，也标（这个标签 49% 是中性）。"]
    dc["include"]["en"] = dc["include"]["en"] + ["A deal, voucher, offer, free trial meal or points redemption is used or mentioned, even without a word on how good it is (49% of this label is neutral)."]
    # R5: boundary notes from the model-capability failures
    pt = label(b, "Food#Portion")
    pt["include"]["zh"] = pt["include"]["zh"] + ["料足、料多（含这些词的点评 76% 带此标签）。"]
    pt["include"]["en"] = pt["include"]["en"] + ["Generous fillings or ingredients: 料足, 料多 (76%)."]
    pt["exclude"]["zh"] = pt["exclude"]["zh"] + ["某样食材个头大（虾很大、块很大）说的是食材，不是分量；“吃撑了”“吃饱了”只有和菜量连在一起时才算。"]
    pt["exclude"]["en"] = pt["exclude"]["en"] + ["One ingredient being big (big prawns) is about the ingredient, not the portion; \"so full\" counts only when tied to how much was served."]
    sp = label(b, "Ambience#Space")
    sp["exclude"]["zh"] = sp["exclude"]["zh"] + ["只数了几张桌子、说坐在门口或窗边，没有说大小、宽敞或拥挤。"]
    sp["exclude"]["en"] = sp["exclude"]["en"] + ["Only a count of tables or where they sat, with nothing about size, room or crowding."]
    save(ROOT / "tasks" / "asap" / "rules_v2.json", b)


def ads() -> None:
    src = ROOT / "tasks" / "ad_policy" / "rules.json"
    b = copy.deepcopy(load(src))
    b["version"] = "2.0"
    # A1: test-result percentages without a source (rule conflict, prompt defect)
    d = label(b, "DATA")
    d["include"]["zh"] = d["include"]["zh"] + ["靠测试、检测、实验得出的效果百分比（“实测除菌率 99.9%”“过滤率 95%”“检测证明”），没写是谁、什么时候测的。"]
    d["exclude"]["zh"] = [e if "规格参数" not in e else "商品自身的规格参数、价格、容量、时长：“52%vol”“续航 30 小时”“¥399”。效果百分比（除菌率、过滤率）不是规格，看上一条。" for e in d["exclude"]["zh"]]
    # A2: immediate weight-loss claims are WEIGHT; GUARANTEE needs explicit guarantee wording there (rule conflict)
    g = label(b, "GUARANTEE")
    g["include"]["en"] = [x if not x.startswith("A product effect promised") else
                          "A product effect promised as certain or immediate: \"thicker hair in 30 days, guaranteed\", \"get slim legs right away\". For weight-loss and body results, see the boundary with WEIGHT."
                          for x in g["include"]["en"]]
    g["boundary"] = [{"with": "WEIGHT", "rule": {"en": "A weight-loss or muscle claim, even an immediate or effortless one (\"melts fat overnight\"), is WEIGHT. Add GUARANTEE only when the ad promises the result in so many words: guaranteed, 100%, we promise, or your money back if it fails."}}]
    for p in b["precedence"]:
        if p["labels"] == ["GUARANTEE", "WEIGHT"]:
            p["rule"] = {"en": "Give both only when a weight or muscle result is explicitly guaranteed (guaranteed, 100%, promise, money back); an immediate or effortless weight claim alone is WEIGHT."}
    save(ROOT / "tasks" / "ad_policy" / "rules_v2.json", b)


def prompt() -> None:
    p = load(ROOT / "prompts" / "v1.json")
    # P1: misses where the agent never considered a label (prompt defect: "check every label's applies-when list")
    p["work_end"] = [
        "Before answering, go through the whole label list once: for every label you did not take as a candidate, make sure nothing in the {noun} matches its \"applies when\" entries or the rulebook's general conventions.",
        "Keep a label only if you can quote the {noun}'s own words that show it.",
    ]
    # P2: the self-check dropped labels that a rule or convention requires (prompt defect)
    p["check"] = ("Check your answer before it is final.\n"
                  "1. For each label you gave, make sure its quote fits the label's rule and no \"does not apply\" entry covers it; "
                  "look up the rule if you have not read it.\n"
                  "2. Do not drop a label that the rulebook's general rules or conventions require (for example a general verdict that the rules "
                  "expand to several labels, or a mention the rules say to label even without a judgement) just because the evidence is brief or neutral.\n"
                  "3. Decide each label marked unsure: keep it as sure, or drop it.\n"
                  "{hints}"
                  "Then give the final answer in the same JSON format.")
    p["hints"] = "4. These labels have keywords in the {noun} but you did not give them: {labels}. Check each against its rule.\n"
    save(ROOT / "prompts" / "v2.json", p)


if __name__ == "__main__":
    asap()
    ads()
    prompt()
    print("wrote tasks/asap/rules_v2.json, tasks/ad_policy/rules_v2.json, prompts/v2.json")
