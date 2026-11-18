"""Model calls for the labelling agent: one engine, three ways to answer a request.

  batch    every request of a round goes out in one Message Batch (half price); used for experiments. A round
           with fewer than 30 requests (the tail of the tool loops) goes out as direct calls at full price.
  direct   one Messages call per request; used for a single item or a quick smoke run
  offline  no network: every answer must already be in the store; used to rebuild all results

A job is a Python generator that yields request parameters and receives the answer as a plain dict
({"content": [...], "stop_reason": ..., "usage": {...}} or {"error": "..."}). The engine runs many jobs
round by round: all requests that are waiting are sent together, each job gets its answer and yields its
next request, until every job has returned. Each answer is stored under the job's key and a hash of the
request, so a rerun sends only what is missing and an offline run replays the stored answers exactly.

The API key is read from a file (EVAL_ENV_FILE, default .env in the project folder), never from the shell
environment, and is never printed or stored. Batch plumbing adapted from creator-skills (same author, MIT).
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Generator

ROOT = Path(__file__).resolve().parents[1]
MODEL = "claude-haiku-5-5"       # cheapest current model
EFFORT = "low"
MAX_TOKENS = 6000
PRICE = {"input": 0.10 / 1e6, "output": 0.50 / 1e6}    # Claude Haiku 5.5 list price, prompts up to 100K tokens
CACHE_WRITE, CACHE_READ = 1.25, 0.10                     # multiples of the input price
BATCH_DISCOUNT = 0.5
MAX_TRIES = 3


def _read_key() -> str:
    env_file = Path(os.environ.get("EVAL_ENV_FILE") or (ROOT / ".env"))
    if not env_file.is_absolute():
        env_file = (ROOT / env_file).resolve()
    if not env_file.exists():
        raise SystemExit(f"API key file not found: {env_file}. Put a line ANTHROPIC_API_KEY=... in .env or set EVAL_ENV_FILE.")
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("ANTHROPIC_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ANTHROPIC_API_KEY missing in the key file")


@lru_cache(maxsize=1)
def client():
    for k in [k for k in os.environ if k.startswith("ANTHROPIC_")]:
        del os.environ[k]
    import anthropic

    return anthropic.Anthropic(api_key=_read_key(), base_url="https://api.anthropic.com", max_retries=4)


def cost_of(usage: dict, pricing: str) -> float:
    full = ((usage.get("input_tokens", 0) + CACHE_WRITE * usage.get("cache_creation_input_tokens", 0)
             + CACHE_READ * usage.get("cache_read_input_tokens", 0)) * PRICE["input"]
            + usage.get("output_tokens", 0) * PRICE["output"])
    return full * BATCH_DISCOUNT if pricing == "batch" else full


def request_hash(params: dict) -> str:
    return hashlib.sha256(json.dumps(params, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _usage(message: dict) -> dict:
    u = message.get("usage") or {}
    return {k: int(u.get(k) or 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}


def _slim(message: dict, pricing: str, batch_id: str | None = None) -> dict:
    out = {"content": message.get("content", []), "stop_reason": message.get("stop_reason"), "usage": _usage(message),
           "pricing": pricing, "model": message.get("model")}
    if batch_id:
        out["batch"] = batch_id
    return out


def store_lines(path: Path) -> list[str]:
    """The lines of an answer store: path, or path + ".gz" (how the published copy keeps them)."""
    path = Path(path)
    if path.exists():
        return path.read_text(encoding="utf-8").splitlines()
    gz = Path(str(path) + ".gz")
    if gz.exists():
        import gzip
        return gzip.decompress(gz.read_bytes()).decode("utf-8").splitlines()
    return []


class Store:
    """Answers on disk, one JSON line per request: {"key", "hash", "response"}."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.data: dict[tuple[str, str], dict] = {}
        for line in store_lines(self.path):
            if line.strip():
                e = json.loads(line)
                self.data[(e["key"], e["hash"])] = e["response"]

    def get(self, key: str, h: str) -> dict | None:
        return self.data.get((key, h))

    def put(self, key: str, h: str, response: dict) -> None:
        self.data[(key, h)] = response
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"key": key, "hash": h, "response": response}, ensure_ascii=False) + "\n")


class Engine:
    def __init__(self, store: Path, mode: str = "offline", fake: Callable[[str, dict], dict] | None = None,
                 log: Callable[[str], None] = print, poll_seconds: float = 20.0, budget_usd: float | None = None,
                 model: str = MODEL, effort: str = EFFORT, max_tokens: int = MAX_TOKENS, reuse: list[Path] | None = None,
                 direct_below: int = 30):
        assert mode in ("batch", "direct", "offline", "fake")
        self.mode, self.fake, self.log, self.poll = mode, fake, log, poll_seconds
        Path(store).parent.mkdir(parents=True, exist_ok=True)
        self.store = Store(store)
        self.reuse = [Store(p) for p in (reuse or []) if store_lines(p)]   # other runs' answers, read only
        self.journal = Path(str(store) + ".batches.jsonl")
        self.model, self.effort, self.max_tokens = model, effort, max_tokens
        self.budget = budget_usd
        self.direct_below = direct_below   # in batch mode, a round with fewer requests goes out as direct calls
        self.spent = 0.0          # cost of answers fetched from the API in this process
        self.sent = 0
        self.reused = 0
        self.batches: list[dict] = []

    # ----- request assembly -----
    def params(self, req: dict) -> dict:
        p = dict(model=self.model, max_tokens=self.max_tokens, **req)
        p["output_config"] = {"effort": self.effort, **req.get("output_config", {})}
        return p

    # ----- the round loop -----
    def run(self, jobs: dict[str, Generator[dict, dict, Any]]) -> dict[str, Any]:
        done: dict[str, Any] = {}
        waiting: dict[str, tuple[str, dict]] = {}     # job -> (call key, params)
        calls: dict[str, int] = {}

        def advance(name: str, answer: dict | None) -> None:
            gen = jobs[name]
            try:
                req = next(gen) if answer is None else gen.send(answer)
            except StopIteration as stop:
                done[name] = stop.value
                return
            calls[name] = calls.get(name, 0) + 1
            waiting[name] = (f"{name}#{calls[name]}", self.params(req))

        for name in jobs:
            advance(name, None)
        rnd = 0
        while waiting:
            rnd += 1
            current, waiting = waiting, {}
            answers: dict[str, dict] = {}
            todo: dict[str, tuple[str, dict, str]] = {}
            for name, (key, params) in current.items():
                h = request_hash(params)
                hit = self.store.get(key, h)
                if hit is None:
                    for other in self.reuse:
                        hit = other.get(key, h)
                        if hit is not None:
                            self.store.put(key, h, hit)      # copied, so this run replays on its own
                            break
                if hit is not None:
                    answers[name] = hit
                    self.reused += 1
                else:
                    todo[name] = (key, params, h)
            if todo:
                self.log(f"round {rnd}: {len(todo)} requests to send, {len(answers)} answers already stored")
                fetched = self._fetch(todo)
                for name, resp in fetched.items():
                    key, _, h = todo[name]
                    if "error" not in resp:
                        self.store.put(key, h, resp)
                    answers[name] = resp
            for name, resp in answers.items():
                advance(name, resp)
        return done

    def _fetch(self, todo: dict[str, tuple[str, dict, str]]) -> dict[str, dict]:
        if self.mode == "offline":
            missing = sorted(key for key, _, _ in todo.values())
            raise SystemExit(f"offline run: {len(missing)} answers are not in {self.store.path.name} "
                             f"(first: {missing[0]}). The prompts or items differ from the stored run.")
        if self.mode == "fake":
            return {name: self.fake(key, params) for name, (key, params, _) in todo.items()}
        if self.budget is not None and self.spent >= self.budget:
            raise SystemExit(f"budget of ${self.budget:.2f} for this run is used up (${self.spent:.4f} spent)")
        small = self.mode == "batch" and len(todo) < self.direct_below
        if small:
            self.log(f"  {len(todo)} requests: sent as direct calls (fewer than {self.direct_below}, full price)")
        out = self._direct(todo) if self.mode == "direct" or small else self._batch(todo)
        for resp in out.values():
            if "error" not in resp:
                self.spent += cost_of(resp["usage"], resp["pricing"])
                self.sent += 1
        return out

    def _direct(self, todo: dict) -> dict[str, dict]:
        def one(item):
            name, (key, params, _) = item
            try:
                msg = client().messages.create(**params)
                return name, _slim(msg.model_dump(mode="json", exclude_none=True), "standard")
            except Exception as e:  # stored as a failed call; the scorer counts it against the arm
                return name, {"error": f"{type(e).__name__}: {e}"}

        with ThreadPoolExecutor(max_workers=8) as pool:
            return dict(pool.map(one, todo.items()))

    def _batch(self, todo: dict) -> dict[str, dict]:
        from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
        from anthropic.types.messages.batch_create_params import Request

        out: dict[str, dict] = {}
        pending = dict(todo)
        # answers of a batch that was sent before an interruption
        for name, (key, params, h) in list(pending.items()):
            got = self._from_journal(key, h)
            if got is not None:
                out[name] = got
                del pending[name]
        for attempt in range(1, MAX_TRIES + 1):
            if not pending:
                break
            names = list(pending)
            ids = {f"r{n}": name for n, name in enumerate(names)}
            c = client()
            batch = c.messages.batches.create(requests=[
                Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**pending[name][1])) for cid, name in ids.items()])
            with self.journal.open("a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps({"batch": batch.id, "requests": {cid: [pending[name][0], pending[name][2]] for cid, name in ids.items()}}) + "\n")
            t0 = time.time()
            while True:
                b = c.messages.batches.retrieve(batch.id)
                if b.processing_status == "ended":
                    break
                time.sleep(self.poll)
            counts = b.request_counts
            self.batches.append({"id": batch.id, "requests": len(names), "minutes": round((time.time() - t0) / 60, 1),
                                 "succeeded": counts.succeeded, "errored": counts.errored, "expired": counts.expired})
            self.log(f"  batch {batch.id}: {len(names)} requests, ended after {(time.time() - t0) / 60:.1f} min "
                     f"({counts.succeeded} succeeded, {counts.errored} errored, {counts.expired} expired)")
            for r in c.messages.batches.results(batch.id):
                name = ids.get(r.custom_id)
                if name is None:
                    continue
                if r.result.type == "succeeded":
                    out[name] = _slim(r.result.message.model_dump(mode="json", exclude_none=True), "batch", batch.id)
                    del pending[name]
                else:
                    err = getattr(getattr(r.result, "error", None), "error", None)
                    why = f"{r.result.type} ({getattr(err, 'type', '')}: {getattr(err, 'message', '')})"
                    if "invalid_request" in why or attempt == MAX_TRIES:
                        out[name] = {"error": f"batch request {why}"}
                        del pending[name]
        for name in pending:
            out[name] = {"error": "batch request missing from the results"}
        return out

    def _from_journal(self, key: str, h: str) -> dict | None:
        if not self.journal.exists():
            return None
        if not hasattr(self, "_journal_index"):
            self._journal_index, self._fetched = {}, {}
            for line in self.journal.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    e = json.loads(line)
                    for cid, (k, hh) in e["requests"].items():
                        self._journal_index[(k, hh)] = (e["batch"], cid)
        hit = self._journal_index.get((key, h))
        if hit is None:
            return None
        batch_id, cid = hit
        if batch_id not in self._fetched:
            c = client()
            while c.messages.batches.retrieve(batch_id).processing_status != "ended":
                time.sleep(self.poll)
            self._fetched[batch_id] = {r.custom_id: r.result for r in c.messages.batches.results(batch_id)}
        res = self._fetched[batch_id].get(cid)
        if res is None or res.type != "succeeded":
            return None
        return _slim(res.message.model_dump(mode="json", exclude_none=True), "batch", batch_id)


def text_of(response: dict) -> str:
    return "".join(b.get("text", "") for b in response.get("content", []) if b.get("type") == "text").strip()


def tool_uses(response: dict) -> list[dict]:
    return [b for b in response.get("content", []) if b.get("type") == "tool_use"]


def final_json(response: dict) -> tuple[Any, str | None]:
    """The JSON object of a final answer, or (None, why)."""
    if "error" in response:
        return None, response["error"]
    if response.get("stop_reason") == "refusal":
        return None, "the model declined to answer"
    text = text_of(response)
    if not text:
        return None, f"no text in the answer (stop reason {response.get('stop_reason')})"
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1]), None
            except json.JSONDecodeError:
                pass
        return None, "the answer is not valid JSON"
