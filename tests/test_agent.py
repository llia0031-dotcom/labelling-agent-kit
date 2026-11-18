"""Offline tests of the agent flow, the round engine and the stored-answer replay, with a stand-in model.

The stand-in answers by keyword: it looks up the rules of the labels whose keywords occur, then gives
them. It is there to exercise every branch of the code, not to label well.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lak import agent, llm, run  # noqa: E402
from lak.task import Task, get_task  # noqa: E402


def usage(i=100, o=50):
    return {"input_tokens": i, "output_tokens": o, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}


def text_answer(obj):
    return {"content": [{"type": "text", "text": json.dumps(obj, ensure_ascii=False)}], "stop_reason": "end_turn", "usage": usage(), "pricing": "batch"}


def tool_answer(name, inp, n=1):
    return {"content": [{"type": "tool_use", "id": f"tu{n}", "name": name, "input": inp}], "stop_reason": "tool_use", "usage": usage(), "pricing": "batch"}


class KeywordModel:
    """First turn: look up rules (if tools are offered). Then: label every keyword hit with the keyword as quote.
    bad_quote=True makes the first answer use a quote that is not in the item."""

    def __init__(self, task: Task, bad_quote=False):
        self.task, self.bad_quote, self.calls = task, bad_quote, []

    def __call__(self, key, params):
        self.calls.append((key, params))
        item_text = params["messages"][0]["content"].split(">\n", 1)[1].rsplit("\n</", 1)[0]
        item = {"id": "x", "text": item_text, "meta": {"lang": "zh" if any("一" <= ch <= "鿿" for ch in item_text) else "en"}}
        hits = self.task.keyword_hits(item)
        allowed = params["output_config"]["format"]["schema"]["properties"]["labels"]["items"]["properties"]["id"]["enum"]
        hits = [h for h in hits if h["id"] in allowed]
        n_assistant = sum(1 for m in params["messages"] if m["role"] == "assistant")
        if params.get("tools") and n_assistant == 0 and hits:
            return tool_answer("get_label_rules", {"labels": [h["id"] for h in hits][:2]})
        quote = lambda h: (h["keywords"][0] if not (self.bad_quote and n_assistant <= 1) else "words that are not there")
        return text_answer({"labels": [{"id": h["id"], "evidence": quote(h), "confidence": "sure"} for h in hits], "rejected": []})


class AgentFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ad = get_task("ad_policy")
        cls.asap = get_task("asap")

    def drive(self, task, item, arm, model):
        engine = llm.Engine(Path(tempfile.mkdtemp()) / "r.jsonl", mode="fake", fake=model, log=lambda *_: None)
        return engine.run({"j": agent.label_job(task, item, arm)})["j"]

    def test_tools_then_answer(self):
        item = {"id": "t1", "text": "The world's best mattress. Free delivery.", "labels": ["ABSOLUTE"], "meta": {"lang": "en"}}
        model = KeywordModel(self.ad)
        rec = self.drive(self.ad, item, agent.ARMS["agent"], model)
        self.assertTrue(rec["ok"], rec["error"])
        self.assertEqual(rec["labels"], ["ABSOLUTE"])
        self.assertEqual(rec["tool_rounds"], 1)
        self.assertEqual(rec["tool_calls"][0]["name"], "get_label_rules")
        self.assertIn("ABSOLUTE", rec["rules_read"])
        second = model.calls[1][1]["messages"]
        self.assertEqual(second[-1]["content"][0]["type"], "tool_result")
        self.assertIn("Does not apply when", second[-1]["content"][0]["content"])

    def test_one_shot_arms_offer_no_tools_and_full_rules_only_in_prompt_rules(self):
        item = {"id": "t2", "text": "云栖羽绒服，全网销量第一。", "labels": ["ABSOLUTE"], "meta": {"lang": "zh"}}
        for name, full in (("prompt-short", False), ("prompt-rules", True)):
            model = KeywordModel(self.ad)
            rec = self.drive(self.ad, item, agent.ARMS[name], model)
            self.assertEqual(rec["calls"], 1)
            params = model.calls[0][1]
            self.assertNotIn("tools", params)
            system = params["system"][0]["text"]
            self.assertEqual("The full rulebook:" in system, full)
            self.assertIn("ABSOLUTE (绝对化用语)", system)          # Chinese ad -> Chinese rule text
            self.assertNotIn("WEIGHT", system)                       # English-only label is out of scope

    def test_scope_limits_labels_and_schema(self):
        zh = {"id": "a", "text": "x", "meta": {"lang": "zh"}}
        en = {"id": "b", "text": "x", "meta": {"lang": "en"}}
        self.assertIn("DATA", self.ad.labels_for(zh))
        self.assertNotIn("DATA", self.ad.labels_for(en))
        self.assertIn("WEIGHT", self.ad.labels_for(en))
        self.assertEqual(len(self.asap.labels_for({"id": "c", "text": "x"})), 18)

    def test_quote_repair_branch(self):
        item = {"id": "t3", "text": "Burn fat without exercise: two capsules a day.", "labels": ["WEIGHT"], "meta": {"lang": "en"}}
        rec = self.drive(self.ad, item, agent.ARMS["agent"], KeywordModel(self.ad, bad_quote=True))
        self.assertTrue(rec["ok"])
        self.assertEqual(rec["branches"]["repair"], ["WEIGHT"])
        self.assertTrue(all(rec["evidence_ok"].values()))
        rec2 = self.drive(self.ad, item, agent.ARMS["prompt-short"], KeywordModel(self.ad, bad_quote=True))
        self.assertIsNone(rec2["branches"]["repair"])           # one-shot arms do not repair
        self.assertFalse(all(rec2["evidence_ok"].values()))

    def test_check_branch_lists_keyword_hints(self):
        item = {"id": "t4", "text": "交通很方便，就在地铁口，环境不错，服务员态度很好，味道一般。", "labels": [], "meta": {}}

        class Forgetful(KeywordModel):
            def __call__(self, key, params):
                r = super().__call__(key, params)
                checked = any(m["role"] == "user" and isinstance(m["content"], str) and "Check your answer" in m["content"]
                              for m in params["messages"])
                if r["stop_reason"] == "end_turn" and not checked:
                    data = json.loads(r["content"][0]["text"])
                    data["labels"] = [l for l in data["labels"] if l["id"] != "Location#Transportation"]
                    r["content"][0]["text"] = json.dumps(data, ensure_ascii=False)
                return r

        model = Forgetful(self.asap)
        rec = self.drive(self.asap, item, agent.ARMS["agent-cases-check"], model)
        self.assertTrue(rec["ok"])
        self.assertIn("Location#Transportation", rec["branches"]["check"]["hinted"])
        self.assertEqual(rec["branches"]["check"]["added"], ["Location#Transportation"])
        check_msg = model.calls[-1][1]["messages"][-1]["content"]
        self.assertIn("Location#Transportation", check_msg)

    def test_rule_gate_sends_unread_rules_once(self):
        item = {"id": "t6", "text": "QuickLoan: guaranteed returns every month.", "labels": ["GUARANTEE"], "meta": {"lang": "en"}}

        class NoLookup(KeywordModel):
            def __call__(self, key, params):
                params = dict(params)
                params.pop("tools", None)              # never calls a tool
                return super().__call__(key, params)

        model = NoLookup(self.ad)
        rec = self.drive(self.ad, item, agent.ARMS["agent"], model)
        self.assertTrue(rec["ok"])
        self.assertEqual(rec["branches"]["rule_gate"], ["GUARANTEE"])
        self.assertEqual(rec["calls"], 2)
        gate_msg = model.calls[1][1]["messages"][-1]["content"]
        self.assertIn("without reading their rules", gate_msg)
        self.assertIn("Does not apply when", gate_msg)
        self.assertIsNone(self.drive(self.ad, item, agent.ARMS["prompt-rules"], NoLookup(self.ad))["branches"]["rule_gate"])

    def test_tools_return_rules_cases_and_phrase_stats(self):
        item = {"id": "t5", "text": "环境一般，排队很久。", "meta": {}}
        arm = agent.ARMS["agent-cases"]
        out, err = agent.run_tool(self.asap, item, arm, "phrase_stats", {"phrase": "环境一般"})
        self.assertFalse(err)
        self.assertIn("Ambience#Noise", out)
        out, err = agent.run_tool(self.asap, item, arm, "search_cases", {"query": "排队等位", "k": 2})
        self.assertFalse(err)
        self.assertIn("Service#Queue", out)
        out, err = agent.run_tool(self.asap, item, arm, "compare_labels", {"a": "Service#Queue", "b": "Service#Timely"})
        self.assertIn("等位子是排队", out)
        out, err = agent.run_tool(self.asap, item, agent.ARMS["agent"], "search_cases", {"query": "x"})
        self.assertTrue(err)                                       # the agent arm has no case tools

    def test_ad_cases_are_searched_in_the_item_language(self):
        out, _ = agent.run_tool(self.ad, {"id": "q", "text": "", "meta": {"lang": "en"}}, agent.ARMS["agent-cases"],
                                "search_cases", {"query": "guaranteed returns", "k": 5})
        self.assertNotRegex(out, "[一-鿿]")

    def test_quote_ok(self):
        t = "Brightfold Cloud mattress: the world's best mattress, period."
        self.assertTrue(agent.quote_ok("the world’s best mattress", t))
        self.assertTrue(agent.quote_ok("Brightfold … best mattress", t))
        self.assertFalse(agent.quote_ok("the best bed", t))
        self.assertTrue(agent.quote_ok("全网 销量第一", "云栖羽绒服，全网销量第一。"))


class EngineAndReplay(unittest.TestCase):
    def test_store_replays_offline_and_refuses_changed_prompts(self):
        task = get_task("ad_policy")
        items = task.items("dev")[:6]
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "r.jsonl"
            model = KeywordModel(task)
            e1 = llm.Engine(store, mode="fake", fake=model, log=lambda *_: None)
            out1 = e1.run({it["id"]: agent.label_job(task, it, agent.ARMS["agent-cases-check"]) for it in items})
            e2 = llm.Engine(store, mode="offline", log=lambda *_: None)
            out2 = e2.run({it["id"]: agent.label_job(task, it, agent.ARMS["agent-cases-check"]) for it in items})
            self.assertEqual(out1, out2)
            self.assertEqual(e2.sent, 0)
            changed = agent.Arm("agent-cases-check", tools=("rules", "cases"), check=True, prompt="v1")
            agent.PROMPTS["vtest"] = dict(agent.PROMPTS["v1"], intro=agent.PROMPTS["v1"]["intro"] + " Changed.")
            try:
                e3 = llm.Engine(store, mode="offline", log=lambda *_: None)
                arm = agent.Arm(changed.id, changed.rules, changed.tools, changed.check, prompt="vtest")
                with self.assertRaises(SystemExit):
                    e3.run({it["id"]: agent.label_job(task, it, arm) for it in items})
            finally:
                del agent.PROMPTS["vtest"]

    def test_reuse_takes_answers_from_another_store(self):
        task = get_task("ad_policy")
        items = task.items("dev")[:4]
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a" / "r.jsonl"
            llm.Engine(first, mode="fake", fake=KeywordModel(task), log=lambda *_: None).run(
                {it["id"]: agent.label_job(task, it, agent.ARMS["agent"]) for it in items})
            e = llm.Engine(Path(tmp) / "b" / "r.jsonl", mode="offline", log=lambda *_: None, reuse=[first])
            out = e.run({it["id"]: agent.label_job(task, it, agent.ARMS["agent"]) for it in items})
            self.assertEqual(len(out), 4)
            self.assertEqual(e.sent, 0)
            again = llm.Engine(Path(tmp) / "b" / "r.jsonl", mode="offline", log=lambda *_: None)   # copied over
            self.assertEqual(len(again.run({it["id"]: agent.label_job(task, it, agent.ARMS["agent"]) for it in items})), 4)

    def test_rounds_are_shared_across_jobs(self):
        task = get_task("ad_policy")
        items = task.items("dev")[:10]
        model = KeywordModel(task)
        log = []
        e = llm.Engine(Path(tempfile.mkdtemp()) / "r.jsonl", mode="fake", fake=model, log=log.append)
        e.run({it["id"]: agent.label_job(task, it, agent.ARMS["agent"]) for it in items})
        self.assertLessEqual(len(log), 3)                          # at most: tools round, answer round, (none needed)
        self.assertIn("round 1: 10 requests", log[0])

    def test_cost(self):
        u = {"input_tokens": 1_000_000, "output_tokens": 1_000_000, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
        self.assertAlmostEqual(llm.cost_of(u, "standard"), 0.60)
        self.assertAlmostEqual(llm.cost_of(u, "batch"), 0.30)

    def test_run_writes_records_and_predictions(self):
        exp = {"name": "_test_run", "runs": [{"task": "ad_policy", "set": "dev", "limit": 5, "arms": [{"arm": "prompt-short"}, {"arm": "agent"}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "exp.json"
            path.write_text(json.dumps(exp), encoding="utf-8")
            old = run.RESULTS
            run.RESULTS = Path(tmp) / "results"
            try:
                s = run.run(path, mode="fake", fake=KeywordModel(get_task("ad_policy")), log=lambda *_: None)
            finally:
                run.RESULTS = old
            self.assertEqual(len(s["units"]), 2)
            pred = Path(tmp) / "results" / "_test_run" / "ad_policy" / "dev" / "agent.pred.jsonl"
            self.assertEqual(len(pred.read_text(encoding="utf-8").splitlines()), 5)

    def test_frozen_check(self):
        task = get_task("ad_policy")
        good = {"name": "x", "frozen": run.freeze_list(["ad_policy", "asap"], ["v1"]), "runs": []}
        self.assertEqual(run.check_frozen(good), [])
        self.assertIn("prompts/v1.json", good["frozen"])
        self.assertIn("tasks/asap/cases_real.jsonl", good["frozen"])
        bad = {"name": "x", "frozen": {"tasks/ad_policy/rules.json": "000000000000"}, "runs": []}
        self.assertTrue(run.check_frozen(bad))


if __name__ == "__main__":
    unittest.main()
