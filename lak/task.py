"""A labelling task: its config, rulebook, case libraries and item sets.

Everything specific to one labelling project lives in tasks/<name>/ (task.json, rules.json, cases and
items). The agent and the analysis read the task through this class and never name a label themselves,
which is what lets a new project plug in by adding a folder.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from functools import cached_property
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
SKILLS = ROOT / "skills"


def skill_module(skill: str, script: str):
    """Imports a skill's script as a module, so the agent's tools run the same code as the skill."""
    name = script[:-3]
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SKILLS / skill / "scripts" / script)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


label_rules = skill_module("label-rules", "label_rules.py")
case_search = skill_module("case-search", "case_search.py")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def sha12(path: Path) -> str:
    """sha256 of a file with LF line endings, first 12 characters (what the preregistration lists)."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:12]


def dig(row: dict, field: str | None):
    if not field:
        return None
    cur = row
    for part in field.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


class Task:
    def __init__(self, name: str, rules_file: str = "rules.json"):
        self.name = name
        self.dir = TASKS / name
        self.rules_file = rules_file
        self.config = json.loads((self.dir / "task.json").read_text(encoding="utf-8"))
        self.book = label_rules.load(str(self.dir / rules_file))
        self._indexes: dict = {}

    # ----- items -----
    def items(self, set_name: str) -> list[dict]:
        return read_jsonl(self.dir / self.config["sets"][set_name])

    def scope(self, item: dict) -> str | None:
        return dig(item, self.config.get("scope_field"))

    def rule_lang(self, item: dict) -> str | None:
        return dig(item, self.config.get("rule_lang_field")) or self.config.get("rule_lang")

    def labels_for(self, item: dict | None = None) -> list[str]:
        scope = self.scope(item) if item else None
        return [l["id"] for l in self.book["labels"] if label_rules.in_scope(l, scope)]

    @cached_property
    def all_labels(self) -> list[str]:
        return [l["id"] for l in self.book["labels"]]

    # ----- rules -----
    def scoped_book(self, item: dict) -> dict:
        return label_rules.scoped(self.book, self.scope(item))

    def catalogue(self, item: dict) -> str:
        """One line per label: id, name and definition, in the item's rule language."""
        lang = self.rule_lang(item)
        book = self.scoped_book(item)
        lines = []
        for l in book["labels"]:
            name = label_rules.tx(l.get("name"), lang)
            lines.append(f"- {l['id']}" + (f" ({name})" if name else "") + f": {label_rules.tx(l.get('definition'), lang)}")
        return "\n".join(lines)

    def general_rules(self, item: dict) -> list[str]:
        return label_rules.txs(self.book.get("general"), self.rule_lang(item))

    def rules_text(self, item: dict, labels: list[str]) -> str:
        book = self.scoped_book(item)
        ids = label_rules.by_id(book)
        known = [x for x in labels if x in ids]
        unknown = [x for x in labels if x not in ids]
        text = "\n".join(label_rules.show_text(label_rules.view(book, ids[x], self.rule_lang(item))) for x in known)
        if unknown:
            text += f"\nUnknown label id(s) for this item: {', '.join(unknown)}. Known: {', '.join(ids)}."
        return text.strip() or "No label given."

    def full_rulebook(self, item: dict) -> str:
        return self.rules_text(item, self.labels_for(item))

    def compare(self, item: dict, a: str, b: str) -> str:
        book = self.scoped_book(item)
        ids = label_rules.by_id(book)
        if a not in ids or b not in ids:
            return f"Give two known labels. Known: {', '.join(ids)}."
        r = label_rules.between(book, a, b, self.rule_lang(item))
        lines = [f"{a} and {b}:"]
        lines += [f"- (written under {x['written_under']}) {x['rule']}" for x in r["boundary"]] or ["- The rulebook has no boundary rule for this pair."]
        lines += [f"- When both fit: {p['rule']}" for p in r["precedence"]]
        if not r["precedence"]:
            lines.append("- Both may be given to one item." if r["may_both_apply"] else "- Only one label per item.")
        return "\n".join(lines)

    def keyword_hits(self, item: dict) -> list[dict]:
        return label_rules.keyword_hits(self.scoped_book(item), item["text"], self.rule_lang(item))

    # ----- cases -----
    def cases(self, library: str | None = None) -> list[dict]:
        library = library or self.config.get("default_cases")
        spec = self.config["case_libraries"][library]
        if isinstance(spec, str):
            return read_jsonl(self.dir / spec)
        rows = []
        for part in spec:                      # "file.jsonl:300" = the first 300 cases of that file
            fname, _, n = part.partition(":")
            got = read_jsonl(self.dir / fname)
            rows += got[: int(n)] if n else got
        return rows

    def case_index(self, library: str | None, scope: str | None):
        key = (library, scope)
        if key not in self._indexes:
            field = self.config.get("case_scope_field")
            cases = self.cases(library)
            if field and scope is not None:
                cases = [c for c in cases if c.get(field) == scope]
            self._indexes[key] = case_search.CaseIndex(cases)
        return self._indexes[key]

    def search_cases(self, item: dict, library: str | None, query: str, k: int = 5, label: str | None = None) -> str:
        index = self.case_index(library, self.scope(item))
        hits = index.search(query, max(1, min(k, 8)), label=label, exclude_ids=[item["id"]])
        width = self.config.get("snippet_chars", 0)
        if not hits:
            return "No case shares a word with the query."
        lines = []
        for n, h in enumerate(hits, 1):
            text = case_search.snippet(h["text"], query, width) if width else " ".join(h["text"].split())
            lines.append(f"{n}. [{', '.join(h['labels']) or 'no label'}] {text}")
        return "\n".join(lines) + "\nCases show how similar items were labelled; when a case and the rules disagree, follow the rules."

    def prefetch_cases(self, item: dict, library: str | None) -> str:
        """The k cases most similar to the whole item, as the flow's fixed retrieval step (k and snippet length from task.json)."""
        k = int(self.config.get("prefetch_cases", 4))
        width = int(self.config.get("prefetch_snippet", 0))
        hits = self.case_index(library, self.scope(item)).search(item["text"], k, exclude_ids=[item["id"]])
        if not hits:
            return "(no similar case found)"
        lines = []
        for n, h in enumerate(hits, 1):
            text = case_search.snippet(h["text"], item["text"], width) if width else " ".join(h["text"].split())
            lines.append(f"{n}. [{', '.join(h['labels']) or 'no label'}] {text}")
        return "\n".join(lines)

    def phrase_stats(self, item: dict, library: str | None, phrase: str) -> str:
        index = self.case_index(library, self.scope(item))
        st = case_search.phrase_stats(index.cases, phrase, examples=2, width=60)
        if not st["cases_with_phrase"]:
            return f"No case contains \"{phrase}\" ({st['of_all_cases']} cases)."
        shares = ", ".join(f"{s['label']} {100 * s['share']:.0f}%" for s in st["label_shares"][:10])
        return (f"{st['cases_with_phrase']} of {st['of_all_cases']} cases contain \"{phrase}\". Share carrying each label: {shares}"
                + (f"; no label: {st['without_label']}" if st["without_label"] else "") + ".")

    # ----- bookkeeping -----
    def fingerprints(self) -> dict:
        files = ["task.json", self.rules_file, *self.config["sets"].values()]
        for spec in self.config["case_libraries"].values():
            files += [spec] if isinstance(spec, str) else [s.partition(":")[0] for s in spec]
        return {f: sha12(self.dir / f) for f in sorted(set(files)) if (self.dir / f).exists()}


_TASKS: dict = {}


def get_task(name: str, rules_file: str = "rules.json") -> Task:
    key = (name, rules_file)
    if key not in _TASKS:
        _TASKS[key] = Task(name, rules_file)
    return _TASKS[key]
