"""Offline tests for the five skill scripts (no model call, no cost).

The metric code uses only the standard library so that any agent can run it; here its numbers are
compared with scikit-learn, statsmodels and rank_bm25 on random multi-label data.
"""
from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def load(skill: str, script: str):
    path = SKILLS / skill / "scripts" / script
    spec = importlib.util.spec_from_file_location(script[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[script[:-3]] = mod
    spec.loader.exec_module(mod)
    return mod


lm = load("label-metrics", "label_metrics.py")
sr = load("slice-report", "slice_report.py")
cr = load("confusion-report", "confusion_report.py")
cs = load("case-search", "case_search.py")
lr = load("label-rules", "label_rules.py")

LABELS = ["A", "B", "C", "D", "E"]


def random_sets(n: int, seed: int, p_empty: float = 0.25):
    rng = random.Random(seed)
    gold, pred = [], []
    for _ in range(n):
        g = frozenset() if rng.random() < p_empty else frozenset(rng.sample(LABELS, rng.choice([1, 1, 1, 2, 3])))
        p = set(g)
        for l in LABELS:
            if rng.random() < 0.15:
                p.symmetric_difference_update({l})
        gold.append(g)
        pred.append(frozenset(p))
    return gold, pred


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


class LabelMetrics(unittest.TestCase):
    def setUp(self):
        self.gold, self.pred = random_sets(400, 7)

    def test_matches_scikit_learn(self):
        import numpy as np
        from sklearn.metrics import (accuracy_score, hamming_loss, multilabel_confusion_matrix,
                                     precision_recall_fscore_support)
        s = lm.summarise(self.gold, self.pred, LABELS, boot=0)
        yt = np.array([[int(l in g) for l in LABELS] for g in self.gold])
        yp = np.array([[int(l in p) for l in LABELS] for p in self.pred])
        p, r, f, sup = precision_recall_fscore_support(yt, yp, average=None, zero_division=0)
        cms = multilabel_confusion_matrix(yt, yp)
        for k, row in enumerate(s["per_label"]):
            self.assertAlmostEqual(row["precision"], p[k], places=12)
            self.assertAlmostEqual(row["recall"], r[k], places=12)
            self.assertAlmostEqual(row["f1"], f[k], places=12)
            self.assertEqual(row["support"], sup[k])
            tn, fp, fn, tp = cms[k].ravel()
            self.assertEqual((row["tn"], row["fp"], row["fn"], row["tp"]), (tn, fp, fn, tp))
        _, _, f_micro, _ = precision_recall_fscore_support(yt, yp, average="micro", zero_division=0)
        self.assertAlmostEqual(s["micro"]["f1"], f_micro, places=12)
        present = [k for k in range(len(LABELS)) if yt[:, k].sum() > 0]          # macro over labels present in gold
        _, _, f_macro, _ = precision_recall_fscore_support(yt, yp, average="macro", labels=present, zero_division=0)
        self.assertAlmostEqual(s["macro"]["f1"], f_macro, places=12)
        self.assertAlmostEqual(s["exact_match"]["rate"], accuracy_score(yt, yp), places=12)
        self.assertAlmostEqual(s["hamming_loss"], hamming_loss(yt, yp), places=12)

    def test_wilson_matches_statsmodels(self):
        from statsmodels.stats.proportion import proportion_confint
        for k, n in [(0, 10), (10, 10), (3, 7), (41, 120), (1, 500), (250, 500)]:
            lo, hi = lm.wilson(k, n)
            ref = proportion_confint(k, n, alpha=0.05, method="wilson")
            self.assertAlmostEqual(lo, ref[0], places=9)
            self.assertAlmostEqual(hi, ref[1], places=9)
        self.assertIsNone(lm.wilson(0, 0))

    def test_mcnemar_matches_statsmodels(self):
        from statsmodels.stats.contingency_tables import mcnemar
        for b, c in [(0, 5), (3, 9), (12, 12), (1, 30), (7, 2)]:
            ref = mcnemar([[10, b], [c, 10]], exact=True).pvalue
            self.assertAlmostEqual(lm.binom_two_sided(b, c), ref, places=12)
        self.assertIsNone(lm.binom_two_sided(0, 0))

    def test_bootstrap_interval_contains_the_estimate_and_is_reproducible(self):
        a = lm.summarise(self.gold, self.pred, LABELS, boot=300, seed=1)
        b = lm.summarise(self.gold, self.pred, LABELS, boot=300, seed=1)
        self.assertEqual(a, b)
        lo, hi = a["micro"]["f1_ci"]
        self.assertLessEqual(lo, a["micro"]["f1"])
        self.assertGreaterEqual(hi, a["micro"]["f1"])
        self.assertLess(hi - lo, 0.15)

    def test_percentile_matches_numpy(self):
        import numpy as np
        rng = random.Random(3)
        vals = [rng.random() for _ in range(137)]
        for q in (0.025, 0.5, 0.975):
            self.assertAlmostEqual(lm.percentile(vals, q), float(np.percentile(vals, 100 * q)), places=12)

    def test_macro_ignores_labels_absent_from_gold(self):
        gold = [frozenset("A"), frozenset("B"), frozenset()]
        pred = [frozenset("A"), frozenset("B"), frozenset("C")]          # C never in gold: a false positive
        s = lm.summarise(gold, pred, ["A", "B", "C"], boot=0)
        self.assertEqual(s["macro"]["f1"], 1.0)
        self.assertEqual(s["macro"]["labels_counted"], 2)
        self.assertLess(s["micro"]["f1"], 1.0)
        c = lm.compare(gold, [frozenset("A"), frozenset("B"), frozenset()], pred, ["A", "B", "C"], boot=0)
        self.assertEqual(c["macro_f1"]["diff"], 0.0)

    def test_decision_rates(self):
        gold = [frozenset("A"), frozenset("A"), frozenset(), frozenset(), frozenset("B")]
        pred = [frozenset("A"), frozenset(), frozenset("B"), frozenset(), frozenset("A")]
        d = lm.summarise(gold, pred, boot=0)["decision"]
        self.assertEqual((d["miss"]["k"], d["miss"]["n"]), (1, 3))
        self.assertEqual((d["false_alarm"]["k"], d["false_alarm"]["n"]), (1, 2))

    def test_compare_is_paired(self):
        gold, pred_a = self.gold, self.pred
        pred_b = list(gold[:200]) + list(pred_a[200:])       # B is right on the first half
        c = lm.compare(gold, pred_a, pred_b, LABELS, boot=300, seed=2)
        self.assertGreater(c["micro_f1"]["diff"], 0)
        self.assertGreater(c["micro_f1"]["diff_ci"][0], 0)
        self.assertEqual(c["exact_match"]["a_only_right"], 0)
        self.assertLess(c["exact_match"]["mcnemar_exact_p"], 0.001)
        same = lm.compare(gold, pred_a, pred_a, LABELS, boot=100, seed=2)
        self.assertEqual(same["micro_f1"]["diff"], 0)
        self.assertIsNone(same["exact_match"]["mcnemar_exact_p"])

    def test_missing_and_unparsed_predictions_count_as_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            g, p = Path(tmp) / "g.jsonl", Path(tmp) / "p.jsonl"
            write_jsonl(g, [{"id": 1, "labels": ["A"]}, {"id": 2, "labels": []}, {"id": 3, "labels": ["B"]}])
            write_jsonl(p, [{"id": 1, "labels": ["A"]}, {"id": 3, "labels": None}, {"id": 9, "labels": ["A"]}])
            d = lm.load_pairs(str(g), str(p))
            self.assertEqual((d["missing"], d["unparsed"], d["not_in_gold"]), ([2], [3], [9]))
            self.assertEqual(d["pred"], [frozenset("A"), frozenset(), frozenset()])
            r = subprocess.run([sys.executable, str(SKILLS / "label-metrics/scripts/label_metrics.py"), str(g), str(p), "--boot", "0"],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("| A | 1 | 1 | 1 | 0 | 0 |", r.stdout)
            bad = subprocess.run([sys.executable, str(SKILLS / "label-metrics/scripts/label_metrics.py"), str(g), str(Path(tmp) / "none.jsonl")],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(bad.returncode, 2)


class SliceReport(unittest.TestCase):
    def test_slices_add_up_and_flag_a_bad_slice(self):
        gold, pred = random_sets(300, 11)
        rows_g, rows_p = [], []
        for i, (g, p) in enumerate(zip(gold, pred)):
            lang = "zh" if i % 3 == 0 else "en"
            if lang == "zh":                      # make the Chinese slice clearly worse
                p = frozenset(LABELS) - g
            rows_g.append({"id": i, "labels": sorted(g), "text": "x" * (5 + i % 90), "meta": {"lang": lang}})
            rows_p.append({"id": i, "labels": sorted(p)})
        rep = sr.build(rows_g, rows_p, ["meta.lang"], "text", True, boot=200, seed=5)
        by_lang = {s["value"]: s for s in rep["groups"][0]["slices"]}
        self.assertEqual(by_lang["zh"]["n"] + by_lang["en"]["n"], 300)
        self.assertEqual(by_lang["zh"]["verdict"], "worse")
        self.assertEqual(by_lang["en"]["verdict"], "better")
        self.assertEqual(sum(s["n"] for s in rep["groups"][1]["slices"]), 300)       # length buckets partition the items
        self.assertEqual(len(rep["groups"][1]["slices"]), 3)
        # the micro F1 of a slice equals label_metrics on the same items
        zh = [i for i in range(300) if i % 3 == 0]
        ref = lm.summarise([gold[i] for i in zh], [frozenset(LABELS) - gold[i] for i in zh], LABELS, boot=0)
        self.assertAlmostEqual(by_lang["zh"]["micro_f1"] or 0.0, ref["micro"]["f1"] or 0.0, places=12)

    def test_slices_without_gold_labels_compare_exact_match(self):
        rows_g = [{"id": i, "labels": ["A"] if i < 30 else [], "meta": {"kind": "violating" if i < 30 else "look-alike"}} for i in range(60)]
        rows_p = [{"id": i, "labels": ["A"] if i < 30 or i % 2 else []} for i in range(60)]      # half the look-alikes flagged
        rep = sr.build(rows_g, rows_p, ["meta.kind"], None, False, boot=200, seed=3)
        s = {x["value"]: x for x in rep["groups"][0]["slices"]}
        self.assertIsNone(s["look-alike"]["micro_f1"])
        self.assertEqual(s["look-alike"]["measure"], "exact match")
        self.assertEqual((s["look-alike"]["false_alarm"]["k"], s["look-alike"]["false_alarm"]["n"]), (15, 30))
        self.assertEqual(s["look-alike"]["verdict"], "worse")                    # 50% exact against 100%
        self.assertEqual((s["violating"]["miss"]["k"], s["violating"]["miss"]["n"]), (0, 30))

    def test_small_slices_get_no_verdict(self):
        rows_g = [{"id": i, "labels": ["A"], "meta": {"src": "rare" if i < 5 else "common"}} for i in range(60)]
        rows_p = [{"id": i, "labels": [] if i < 5 else ["A"]} for i in range(60)]
        rep = sr.build(rows_g, rows_p, ["meta.src"], None, False, boot=100)
        verdicts = {s["value"]: s["verdict"] for s in rep["groups"][0]["slices"]}
        self.assertEqual(verdicts["rare"], "too few")


class ConfusionReport(unittest.TestCase):
    def test_single_label_equals_scikit_learn_confusion_matrix(self):
        from sklearn.metrics import confusion_matrix
        rng = random.Random(4)
        gold = [rng.choice(LABELS) for _ in range(300)]
        pred = [g if rng.random() < 0.7 else rng.choice(LABELS) for g in gold]
        res = cr.mlcm(list(range(300)), [frozenset([g]) for g in gold], [frozenset([p]) for p in pred], LABELS)
        ref = confusion_matrix(gold, pred, labels=LABELS)
        for r in range(5):
            self.assertEqual(res["matrix"][r][:5], list(ref[r]))
            self.assertEqual(res["matrix"][r][5], 0)

    def test_the_four_cases_of_the_method(self):
        L = ["A", "B", "C"]
        f = frozenset
        cases = [
            (f("AB"), f("AB")),      # exact: two diagonal counts
            (f(), f("C")),           # no gold label: C in the last row
            (f("AB"), f("A")),       # missed B, nothing added: B in the last column
            (f("A"), f("AC")),       # all gold found, C added: counts against A
            (f("AB"), f("AC")),      # missed B, added C: counts against B only
            (f(), f()),              # nothing and nothing
        ]
        res = cr.mlcm(list(range(len(cases))), [g for g, _ in cases], [p for _, p in cases], L)
        m = res["matrix"]
        self.assertEqual(m[0], [4, 0, 1, 0])    # A: diagonal x4 (items 0,2,3,4), A->C once (item 3)
        self.assertEqual(m[1], [0, 1, 1, 1])    # B: diagonal once, B->C (item 4), missed (item 2)
        self.assertEqual(m[2], [0, 0, 0, 0])
        self.assertEqual(m[3], [0, 0, 1, 1])    # no gold: C added (item 1), empty/empty (item 5)

    def test_diagonal_equals_true_positives_and_kinds_add_up(self):
        gold, pred = random_sets(300, 21)
        rows_g = [{"id": i, "labels": sorted(g)} for i, g in enumerate(gold)]
        rows_p = [{"id": i, "labels": sorted(p)} for i, p in enumerate(pred)]
        rep = cr.build(rows_g, rows_p, LABELS)
        s = lm.summarise(gold, pred, LABELS, boot=0)
        for k, row in enumerate(s["per_label"]):
            self.assertEqual(rep["matrix"][k][k], row["tp"])
        self.assertEqual(sum(rep["item_kinds"].values()), 300)
        self.assertEqual(rep["item_kinds"]["exact"], s["exact_match"]["k"])
        self.assertTrue(all(p["gold"] != p["predicted"] for p in rep["top_pairs"]))


class CaseSearch(unittest.TestCase):
    CASES = [
        {"id": "c1", "text": "The world's best mattress, period. Free delivery.", "labels": ["ABSOLUTE"]},
        {"id": "c2", "text": "Reapply sunscreen every 2 hours for best results.", "labels": []},
        {"id": "c3", "text": "护眼效果全国第一，孩子写作业不再眼累。", "labels": ["ABSOLUTE"]},
        {"id": "c4", "text": "根治失眠多梦，每晚一杯喝出好睡眠。", "labels": ["MEDICAL"]},
        {"id": "c5", "text": "开封后请冷藏，最好在 3 天内饮用完。", "labels": []},
        {"id": "c6", "text": "Burn fat without exercise: two capsules a day.", "labels": ["WEIGHT"]},
        {"id": "c7", "text": "Best mattress deals this weekend only.", "labels": []},
    ]

    def test_scores_equal_rank_bm25(self):
        from rank_bm25 import BM25Okapi
        docs = [cs.tokens(c["text"]) for c in self.CASES]
        ours, ref = cs.BM25(docs), BM25Okapi(docs)
        for q in ["best mattress in the world", "全国第一的护眼台灯", "失眠", "2 hours", "nothing shared zzz"]:
            a, b = ours.scores(cs.tokens(q)), ref.get_scores(cs.tokens(q))
            for x, y in zip(a, b):
                self.assertAlmostEqual(x, float(y), places=9)

    def test_search_finds_the_similar_case_in_both_languages(self):
        index = cs.CaseIndex(self.CASES)
        self.assertEqual(index.search("the best mattress in the world", k=1)[0]["id"], "c1")
        self.assertEqual(index.search("这款台灯护眼效果全国第一", k=1)[0]["id"], "c3")
        self.assertEqual(index.search("zzz qqq", k=3), [])
        self.assertTrue(all("ABSOLUTE" in h["labels"] for h in index.search("best 第一", k=5, label="ABSOLUTE")))
        self.assertNotIn("c1", [h["id"] for h in index.search("best mattress", k=5, exclude_ids=["c1"])])
        limited = index.search("best mattress results", k=5, per_label=1)
        combos = [tuple(h["labels"]) for h in limited]
        self.assertEqual(len(combos), len(set(combos)))

    def test_tokens(self):
        self.assertEqual(cs.tokens("World's BEST 床垫!"), ["world's", "best", "床", "垫", "床垫"])


class LabelRules(unittest.TestCase):
    BOOK = {
        "task": "demo", "version": "1", "multi_label": True, "empty_allowed": True,
        "general": {"en": ["Judge what the item says, not what it might imply."], "zh": ["按内容实际说了什么判断。"]},
        "labels": [
            {"id": "ABSOLUTE", "name": {"en": "Absolute claim", "zh": "绝对化用语"},
             "definition": {"en": "A superlative about the product.", "zh": "对商品使用最高级表述。"},
             "include": {"en": ["best, No.1 about the product"], "zh": ["最好、第一"]},
             "exclude": {"en": ["usage advice such as 'for best results'"], "zh": ["使用建议"]},
             "keywords": ["best", "No.1", "第一", "最好"],
             "boundary": [{"with": "DATA", "rule": {"en": "A ranking with a source is DATA's question, not ABSOLUTE.", "zh": "带出处的排名看 DATA。"}}]},
            {"id": "DATA", "definition": "A statistic without a source.", "exclude": ["a statistic with its source"], "keywords": ["%"]},
        ],
        "precedence": [{"labels": ["ABSOLUTE", "DATA"], "rule": "Give both when a superlative also cites an unsourced figure."}],
    }

    def run_cli(self, *args, book=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.json"
            path.write_text(json.dumps(book or self.BOOK, ensure_ascii=False), encoding="utf-8")
            return subprocess.run([sys.executable, str(SKILLS / "label-rules/scripts/label_rules.py"), str(path), *args],
                                  capture_output=True, text=True, encoding="utf-8")

    def test_show_in_two_languages(self):
        en = self.run_cli("show", "ABSOLUTE", "--lang", "en")
        zh = self.run_cli("show", "ABSOLUTE", "--lang", "zh")
        self.assertEqual(en.returncode, 0, en.stderr)
        self.assertIn("A superlative about the product.", en.stdout)
        self.assertIn("usage advice", en.stdout)
        self.assertIn("对商品使用最高级表述。", zh.stdout)
        self.assertIn("带出处的排名看 DATA。", zh.stdout)

    def test_boundary_is_visible_from_both_labels(self):
        v = lr.view(self.BOOK, lr.by_id(self.BOOK)["DATA"], "en")
        self.assertEqual(v["boundary"][0]["with"], "ABSOLUTE")
        r = self.run_cli("between", "DATA", "ABSOLUTE", "--format", "json")
        data = json.loads(r.stdout)
        self.assertEqual(len(data["boundary"]), 1)
        self.assertEqual(len(data["precedence"]), 1)

    def test_keyword_match_respects_word_boundaries(self):
        hits = lr.keyword_hits(self.BOOK, "Our bestseller is the No.1 choice, 90% agree")
        self.assertEqual({h["id"]: h["keywords"] for h in hits}, {"ABSOLUTE": ["No.1"], "DATA": ["%"]})
        self.assertEqual(lr.keyword_hits(self.BOOK, "全国第一")[0]["id"], "ABSOLUTE")
        self.assertEqual(lr.keyword_hits(self.BOOK, "a plain sentence"), [])

    def test_lint(self):
        self.assertEqual(lr.lint(self.BOOK), [])
        self.assertEqual(self.run_cli("lint").returncode, 0)
        bad = {"labels": [{"id": "A", "definition": "x", "boundary": [{"with": "Z", "rule": "r"}]}, {"id": "A"}]}
        problems = lr.lint(bad)
        self.assertTrue(any("unknown label 'Z'" in p for p in problems))
        self.assertTrue(any("duplicate id" in p for p in problems))
        self.assertTrue(any("missing 'definition'" in p for p in problems))
        self.assertTrue(any("multi_label" in p for p in problems))
        self.assertEqual(self.run_cli("lint", book=bad).returncode, 1)

    def test_unknown_label_is_an_input_error(self):
        self.assertEqual(self.run_cli("show", "NOPE").returncode, 2)


if __name__ == "__main__":
    unittest.main()
