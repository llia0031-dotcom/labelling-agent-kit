"""Checks every number in the report and the READMEs against the result files, with evidence-check.

    python tools/check_claims.py         # writes eval/claims.json, then checks it; exit 0 when every claim is supported

Every sentence or table row of the documents below that states a number becomes one claim. Its evidence is the
smallest set of lines from the result files that holds all of its numbers, picked by the numbers they share and
then by the words they share (arm names, label names, task and set names). eval/claims.json lists every pairing,
so a reader can check that each quote is about what the sentence says; HINTS pins the lines for sentences where
shared words alone would not decide. Cross-references ("section 3") and file names are not claims and are left out.

The checker is evidence-check's check_evidence.py (MIT), copied to tools/vendor/ so the check runs with the
standard library alone: each quote must be in its source file, and each number of the claim in its quotes.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "vendor"))
from check_evidence import numbers_in  # noqa: E402

DOCS = ["eval/EVALUATION.md", "README.md", "README.zh-CN.md"]
SOURCE_GLOBS = ["eval/numbers.md", "results/*/ANALYSIS.md", "results/*/FIRST_TURN.md", "results/main/rca/*.md", "results/ACCEPTANCE.md",
                "results/COSTS.md", "tasks/*/task.json", "requirements.txt", "experiments/PREREGISTRATION.md", "experiments/REVISION.md", "DATA_ACCEPTANCE.md"]

# Sentences whose evidence must come from particular lines: {a piece of the sentence: [pieces a quote line must contain]};
# a piece "@path/" names the folder or file the line must come from.
CAUSES = [["ad_policy causes:"], ["asap causes:"]]
HINTS: dict[str, list[list[str]]] = {
    # structure
    "two tasks (": [["labelling tasks:"], ["ASAP rulebook has"], ["compare 5 arms"]],
    "Two tasks |": [["labelling tasks:"], ["ASAP rulebook has"]],
    "两个任务 |": [["labelling tasks:"], ["ASAP rulebook has"]],
    "One of the two tasks": [["labelling tasks:"]],
    "两个任务之一": [["labelling tasks:"]],
    "Experiments | 5 arms": [["compare 5 arms"]],
    "实验 | 5 种做法": [["compare 5 arms"]],
    "精确率、召回率和 F1": [["**Secondary**"]],
    "precision, recall and F1 for every label": [["**Secondary**"]],
    "five Agent Skills": [["skills:"]],
    "五个 Agent Skill": [["skills:"]],
    "7 per language": [["per language"]],
    "mostly 0 or 1": [["| `ad_policy` |", "0 or 1"], ["| `asap` |", "about 6"]],
    "Licence | MIT": [["\"licence\"", "Apache-2.0"]],
    "five tool rounds": [["tool rounds"]],
    "| label catalogue": [["| `prompt-short` | one call"]],
    "| the whole rulebook": [["| `prompt-rules` | one call"]],
    "1 or more | catalogue": [["| `agent` | tools"]],
    "1 or more | + retrieved": [["| `agent-cases` | plus a retrieval step"]],
    "2 or more | + self-check": [["| `agent-cases-check` | plus one self-check turn"]],
    "two independent classifications into five causes": [["causes:", "independent passes"]],
    "Ads (87) | ASAP (60)": [["dev2, ad_policy (87 items), `prompt-short`"], ["dev2, asap (60 items), `prompt-short`"]],
    "Micro F1 with 95% bootstrap": [["@results/main/", "Intervals are 95%"]],
    "Preregistered comparisons (B − A": [["@results/main/", "## Comparisons (B − A"]],
    # test A
    "ahead by 0.047": [["H4-ad ("]],
    "ahead of the synthetic library by 0.010": [["H5a ("], ["H5b ("]],
    "Real against synthetic cases: no measured": [["H5a ("]],
    "真实案例和合成案例": [["H5a ("]],
    "Short prompt |": [["ad_policy test A (119 items), `prompt-short`"], ["asap test A (201 items), `prompt-short`"]],
    "短提示词 |": [["ad_policy test A (119 items), `prompt-short`"], ["asap test A (201 items), `prompt-short`"]],
    "Whole rulebook in the prompt |": [["ad_policy test A (119 items), `prompt-rules`"], ["asap test A (201 items), `prompt-rules`"]],
    "整本规则放进提示词 |": [["ad_policy test A (119 items), `prompt-rules`"], ["asap test A (201 items), `prompt-rules`"]],
    "Agent that reads the rules |": [["ad_policy test A (119 items), `agent`:"], ["asap test A (201 items), `agent`:"]],
    "会查规则的 Agent |": [["ad_policy test A (119 items), `agent`:"], ["asap test A (201 items), `agent`:"]],
    "+ retrieved similar cases |": [["ad_policy test A (119 items), `agent-cases`:"], ["asap test A (201 items), `agent-cases`:"]],
    "再加检索相似案例 |": [["ad_policy test A (119 items), `agent-cases`:"], ["asap test A (201 items), `agent-cases`:"]],
    "+ self-check |": [["ad_policy test A (119 items), `agent-cases-check`:"], ["asap test A (201 items), `agent-cases-check`:"]],
    "再加自查 |": [["ad_policy test A (119 items), `agent-cases-check`:"], ["asap test A (201 items), `agent-cases-check`:"]],
    "Retrieved cases help on both tasks (+0.040": [["H2-ad ("], ["H2-asap ("]],
    "检索相似案例在两个任务上都有用": [["labelling tasks:"], ["H2-ad ("], ["H2-asap ("]],
    "The self-check helps only on ASAP (+0.012)": [["H3-asap ("], ["asap test A (201 items), `agent-cases`:"], ["asap test A (201 items), `agent-cases-check`:"]],
    "自查只在点评上有用": [["H3-asap ("], ["asap test A (201 items), `agent-cases`:"], ["asap test A (201 items), `agent-cases-check`:"]],
    "完整的 Agent 是 0 条": [["gave a label to 12 of 32"], ["gave a label to 0 of 32"]],
    "1,000 条广告 0.53": [["asap test A (201 items), `agent-cases-check`:"], ["ad_policy test A (119 items), `agent-cases-check`:"]],
    "Jiahao Bu": [["\"licence\"", "Apache-2.0"]],
    "weakest on Location#Downtown": [["Location#Downtown: recall"], ["Food#Appearance: recall"], ["Price#Cost_effective: precision"], ["confused with Price#Cost_effective"]],
    # root causes
    "Also wrong in every other arm": [["ad_policy: 4 wrong label decisions"], ["asap: 406 wrong label decisions"]],
    "| Label ambiguity |": CAUSES, "| Prompt defect |": CAUSES, "| Model capability |": CAUSES, "| Rule conflict |": CAUSES,
    "| Sample distribution |": CAUSES, "| The two passes disagree |": CAUSES,
    "Most of the 18 rule conflicts": [["asap rule conflicts by label"], ["asap causes:"]],
    "On ads, the two rule conflicts": [["ad_policy causes:"]],
    # revision
    "| v1 (": [["ad_policy test_b (118 items), `agent-cases-check`:"], ["asap test_b (199 items), `agent-cases-check`:"],
               ["ad_policy test_a (119 items), `agent-cases-check`:"], ["asap test_a (201 items), `agent-cases-check`:"]],
    "| v2 |": [["ad_policy test_b (118 items), `agent-cases-check-v2`:"], ["asap test_b (199 items), `agent-cases-check-v2`:"],
               ["ad_policy test_a (119 items), `agent-cases-check-v2`:"], ["asap test_a (201 items), `agent-cases-check-v2`:"]],
    "| v2 − v1, micro F1 |": [["H6-ad ("], ["H6-asap ("], ["R-ad ("], ["R-asap ("]],
    "ahead on held-out ASAP reviews": [["H6-asap ("], ["H6-ad ("]],
    "v2 is ahead by +0.018": [["H6-asap ("]],
    "It is ahead on test B by +0.021": [["H6-ad ("]],
    "v1 already made only four errors": [["ad_policy: 4 wrong label decisions"]],
    "WEIGHT F1 fell by 0.091": [["R-ad per-label"]],
    "Regression on test A": [["R-asap ("], ["R-ad ("]],
    "several differences here are close to the edge": [["H4-asap ("], ["H5b ("], ["H6-ad ("]],
    # costs
    "All model calls came to USD 3.6325": [["| **total** |"], ["claude-haiku-5-5 list price"]],
}

SYNONYMS = [(r"test[ _]?a\b", " testa "), (r"test[ _]?b\b", " testb "), (r"测试集 ?A", " testa "), (r"测试集 ?B", " testb "),
            (r"\bad_policy\b|\bads?\b|广告", " ads "), (r"点评|asap", " asap "), (r"\bdev\b|开发集", " dev "),
            (r"self-check|自查", " selfcheck "), (r"rule gate|规则闸门|没读规则", " rulegate "), (r"look-alike|形似|近似", " lookalike "),
            (r"root[- ]cause|根因", " rootcause "), (r"synthetic|合成", " synthetic "), (r"real|真实", " real "),
            (r"\bmixed\b|half-and-half|一半|混合", " mixed "), (r"recall|召回", " recall "), (r"precision|精确率|准确率", " precision "),
            (r"cost|USD|美元|费用", " usd "), (r"label ambiguity|label_ambiguity|标签有歧义|标签歧义", " label_ambiguity "),
            (r"prompt defects?|prompt_defect|提示词缺陷", " prompt_defect "), (r"rule conflicts?|rule_conflict|规则冲突", " rule_conflict "),
            (r"model capability|model_capability|模型能力", " model_capability ")]
STOP = {"the", "and", "for", "with", "that", "this", "are", "was", "were", "from", "only", "not", "its", "has", "than", "all",
        "one", "two", "both", "each", "every", "arm", "arms", "items", "item", "micro"}


def tokens(text: str) -> set[str]:
    t = text.lower()
    for pat, rep in SYNONYMS:
        t = re.sub(pat, rep, t, flags=re.I)
    t = t.replace("`", " ")
    words = set(re.findall(r"[a-z][a-z0-9#_+-]{2,}", t))
    return {w.strip("-") for w in words if w not in STOP}


def clean(text: str) -> str:
    """The sentence as a claim: link targets, code spans, cross-references and emphasis marks taken out."""
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"\(?\b(?:in |see )?sections? \d+(?: of the preregistration)?\)?", " ", t, flags=re.I)
    t = re.sub(r"[（(]?第 ?\d+ ?节[）)]?", " ", t)
    t = t.replace("**", "")
    return re.sub(r"\s+", " ", t).strip(" |")


def units(doc: str) -> list[tuple[int, str]]:
    """(line, text) for every sentence or table row that states a number."""
    out, in_code = [], False
    for n, line in enumerate((ROOT / doc).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        s = line.strip()
        if in_code or not s or set(s) <= set("|-: ") or s.startswith("#"):
            continue
        if s.startswith("|"):
            parts = [s]
        else:
            body = re.sub(r"^([-*]|\d+\.)\s+", "", s)
            parts = re.split(r"(?<=[.!?。！？])\s+(?=[A-Z*`(一-鿿])|(?<=[。！？；])", body)
        for p in parts:
            if p.strip() and numbers_in(clean(p)):
                out.append((n, p.strip()))
    return out


def source_lines() -> list[tuple[str, int, str, set, set]]:
    rows = []
    for rank, g in enumerate(SOURCE_GLOBS):
        for f in sorted(ROOT.glob(g)):
            rel = f.relative_to(ROOT).as_posix()
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                s = line.strip()
                nums = numbers_in(s, generous=True)
                if len(s) >= 12 and nums and not set(s) <= set("|-: "):
                    rows.append((rel, n, s, nums, tokens(s), rank))
    return rows


def pick(text: str, rows) -> list[tuple[str, int, str]]:
    claim = clean(text)
    need = set(numbers_in(claim))
    words = tokens(text)
    chosen: list = []
    for key, pins in HINTS.items():
        if key in text or key in claim:
            for pieces in pins:
                hit = next((r for r in rows if all(r[0].startswith(p[1:]) if p.startswith("@") else p in r[2] for p in pieces)), None)
                if hit is None:
                    raise SystemExit(f"HINTS: no source line contains {pieces} (for {key!r})")
                chosen.append(hit)
                need -= hit[3]
    while need:
        # most of the missing numbers, then most shared words, then the earlier source in SOURCE_GLOBS, then the shorter line
        best = max(rows, key=lambda r: (len(need & r[3]), len(words & r[4]), -r[5], -len(r[2])))
        if not need & best[3]:
            break
        chosen.append(best)
        need -= best[3]
    return [(r[0], r[1], r[2]) for r in chosen]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    rows = source_lines()
    claims = []
    for doc in DOCS:
        for n, text in units(doc):
            ev = pick(text, rows)
            claims.append({"id": f"{doc}:{n}", "text": clean(text), "evidence": [{"source": s, "quote": q, "line": ln} for s, ln, q in ev]})
    out = ROOT / "eval" / "claims.json"
    out.write_text(json.dumps({"claims": claims}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    # the checker names a source file by its path below the folder it is given; the cited files are copied into a
    # temporary folder at their paths in the project, so that results/main/ANALYSIS.md and results/revision/ANALYSIS.md stay apart
    with tempfile.TemporaryDirectory() as tmp:
        for rel in sorted({e["source"] for c in claims for e in c["evidence"]}):
            (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, Path(tmp) / rel)
        r = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "tools" / "vendor" / "check_evidence.py"), str(out), "--sources", tmp,
                            "--format", "json"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    try:
        res = json.loads(r.stdout)
    except ValueError:
        print(r.stdout[-2000:], r.stderr[-2000:])
        return 2
    bad = [c for c in res["claims"] if c["status"] != "supported"]
    print(f"{res['summary']['claims']} claims with numbers in {', '.join(DOCS)}; {res['summary']['supported']} supported, {len(bad)} not")
    for c in bad:
        print(f"  - {c['id']} {c['status']} {c['missing_numbers']}: {c['text'][:160]}")
    (ROOT / "eval" / "claims_check.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
