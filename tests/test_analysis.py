"""Offline tests of data acceptance, the analysis step and the root-cause signals (no model call)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lak import accept, analyze, rca  # noqa: E402
from lak.task import get_task  # noqa: E402


def rec(item_id, labels, ok=True, rules_read=(), rejected=(), evidence=None, check=None):
    ev = evidence or {}
    return {"item_id": item_id, "arm": "x", "labels": sorted(labels), "ok": ok, "error": None if ok else "failed",
            "answer": {"labels": [{"id": l, "evidence": ev.get(l, "q"), "confidence": "sure"} for l in sorted(labels)],
                       "rejected": [{"id": r, "reason": "not shown"} for r in rejected]},
            "calls": 1, "tool_rounds": 0, "tool_calls": [], "rules_read": list(rules_read),
            "branches": {"rule_gate": None, "repair": None, "check": check}, "stages": [], "cost_usd": 0.001,
            "usage": {"input_tokens": 100, "output_tokens": 10, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
            "evidence_ok": {l: True for l in labels}}


class Acceptance(unittest.TestCase):
    def test_blocking_checks_catch_bad_rows(self):
        task = get_task("ad_policy")
        rows = [
            {"id": "a", "text": "The world's best mattress, period.", "labels": ["ABSOLUTE"], "meta": {"lang": "en", "source": "x"}},
            {"id": "a", "text": "Another ad entirely about shoes.", "labels": [], "meta": {"lang": "en", "source": "x"}},   # duplicate id
            {"id": "c", "text": "全网销量第一的羽绒服。", "labels": ["WEIGHT"], "meta": {"lang": "zh", "source": "x"}},            # out of scope
            {"id": "d", "text": "A plain ad.", "labels": ["NOPE"], "meta": {"lang": "en"}},                                     # unknown, no source
            {"id": "e", "text": "这是中文。", "labels": [], "meta": {"lang": "en", "source": "x"}},                              # wrong language
        ]
        test = [{"id": "t1", "text": "The world's best mattress, period. Free delivery.", "labels": []}]
        res = accept.check(rows, task, None, {"test_a": test}, None)
        failed = set(res["blocking_failed"])
        self.assertTrue({"A1", "A2", "A4", "A6", "A7"} <= failed, failed)
        self.assertFalse(res["accepted"])

    def test_frozen_sets_are_accepted(self):
        rep = accept.run()
        for f in rep["files"]:
            if f["rows"] == 0:          # a library still being generated
                self.assertFalse(f["accepted"])
                continue
            self.assertTrue(f["accepted"], (f["task"], f["set"], f["blocking_failed"]))
        self.assertTrue(any(f["set"] == "test_b" and f["task"] == "asap" for f in rep["files"]))

    def test_near_duplicates(self):
        a = accept.grams("服务员态度很好，上菜很快，味道不错，下次还来。", 5)
        b = accept.grams("服务员态度很好，上菜很快，味道不错，下次还会来。", 5)
        self.assertGreaterEqual(accept.jaccard(a, b), 0.6)
        self.assertTrue(accept.is_chinese("环境不错 good"))
        self.assertFalse(accept.is_chinese("Nice place 好"))


class Analysis(unittest.TestCase):
    def test_unit_metrics_match_label_metrics_and_ops_count_failures(self):
        task = get_task("ad_policy")
        items = task.items("dev")[:20]
        recs = [rec(it["id"], it["labels"] if i % 4 else ["ABSOLUTE"]) for i, it in enumerate(items)]
        recs[3]["ok"] = False
        u = analyze.analyse_unit(task, "dev", recs, task.all_labels)
        gold = [frozenset(it["labels"]) for it in items]
        pred = [frozenset(r["labels"]) if r["ok"] else frozenset() for r in recs]
        ref = analyze.lm.summarise(gold, pred, task.all_labels, 0)
        self.assertAlmostEqual(u["metrics"]["micro"]["f1"], ref["micro"]["f1"])
        self.assertEqual(u["ops"]["failed"], 1)
        self.assertEqual(sum(u["confusion"]["item_kinds"].values()), 20)
        self.assertTrue(u["slices"]["groups"])


class RootCauseSignals(unittest.TestCase):
    def test_signals(self):
        task = get_task("asap")
        item = {"id": "s1", "text": "交通很便利，地铁口出来就是。服务员态度一般。环境不错。", "labels": ["Location#Transportation", "Service#Hospitality", "Ambience#Noise"],
                "meta": {"polarity": {"Location#Transportation": 1, "Service#Hospitality": 0, "Ambience#Noise": 1}}}
        r = rec("s1", ["Location#Transportation", "Food#Taste"], rules_read=["Food#Taste"], rejected=["Service#Hospitality"],
                evidence={"Food#Taste": "环境不错"})
        others = {"a": {"Location#Transportation", "Food#Taste"}, "b": {"Location#Transportation", "Service#Hospitality"}}
        sig = {(s["label"], s["kind"]): s for s in rca.signals(task, item, r, others, None)}
        fp = sig[("Food#Taste", "false_positive")]
        self.assertEqual(fp["same_error_arms"], 1)                  # arm a made the same false positive
        self.assertTrue(fp["rule_read"])
        self.assertEqual(fp["evidence"], "环境不错")
        miss = sig[("Service#Hospitality", "miss")]
        self.assertTrue(miss["considered"])
        self.assertEqual(miss["gold_polarity"], 0)
        self.assertEqual(miss["same_error_arms"], 1)                # arm a also missed it
        noise = sig[("Ambience#Noise", "miss")]
        self.assertEqual(noise["same_error_arms"], 2)               # a stable miss
        self.assertNotIn(("Location#Transportation", "miss"), sig)

    def test_request_lists_causes_in_both_orders(self):
        task = get_task("asap")
        item = task.items("dev")[0]
        r = rec(item["id"], [])
        sig = rca.signals(task, item, r, {}, None)
        p1 = rca.request(task, item, r, sig, False)["system"]
        p2 = rca.request(task, item, r, sig, True)["system"]
        self.assertLess(p1.index("prompt_defect"), p1.index("label_ambiguity"))
        self.assertGreater(p2.index("prompt_defect"), p2.index("label_ambiguity"))


if __name__ == "__main__":
    unittest.main()
