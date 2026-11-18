#!/usr/bin/env python3
"""label_rules.py - look up the rules of a label, the boundary between two labels, and check a rulebook.

A rulebook is one JSON file per labelling task (format in references/rulebook-format.md):

    {"task": "...", "version": "1.0", "multi_label": true, "empty_allowed": true,
     "general": ["rules that hold for every label"],
     "labels": [{"id": "ABSOLUTE", "name": "...", "definition": "...", "applies_to": ["zh", "en"],
                 "include": ["..."], "exclude": ["..."], "keywords": ["best", "No.1"],
                 "boundary": [{"with": "DATA", "rule": "..."}], "source": "..."}],
     "precedence": [{"labels": ["A", "B"], "rule": "..."}]}

Any text may be a string or an object keyed by language, e.g. {"en": "...", "zh": "..."}.

    python label_rules.py rules.json list
    python label_rules.py rules.json show ABSOLUTE MEDICAL
    python label_rules.py rules.json between ABSOLUTE DATA      # boundary and precedence rules for a pair
    python label_rules.py rules.json match --text "the world's best mattress"   # labels whose keywords occur
    python label_rules.py rules.json search "before and after"  # labels whose rules mention the words
    python label_rules.py rules.json lint                       # is the rulebook complete and consistent?

Add --lang zh|en to choose the language of bilingual rulebooks, --scope VALUE to keep only the labels
whose "applies_to" includes that value, and --format json for machine output.
Python 3.9+, standard library only. Exit code 0: found / rulebook passes; 1: nothing found / lint
problems; 2: the rulebook or the arguments could not be read.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ("id", "definition")
LIST_FIELDS = ("include", "exclude", "keywords")


def load(path: str) -> dict:
    try:
        book = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{path}: not valid JSON ({e.msg}, line {e.lineno})")
    if not isinstance(book, dict) or not isinstance(book.get("labels"), list):
        raise ValueError(f"{path}: a rulebook is an object with a 'labels' list")
    return book


def tx(value, lang: str | None) -> str:
    """A text field in the wanted language (falls back to English, then to any language)."""
    if value is None:
        return ""
    if isinstance(value, dict):
        for key in (lang, "en"):
            if key and value.get(key):
                return str(value[key])
        return next((str(v) for v in value.values() if v), "")
    return str(value)


def txs(values, lang: str | None) -> list[str]:
    """A list field in the wanted language. The list itself may be keyed by language."""
    if isinstance(values, dict):
        values = values.get(lang) or values.get("en") or next(iter(values.values()), [])
    return [tx(v, lang) for v in (values or []) if tx(v, lang)]


def by_id(book: dict) -> dict:
    return {l.get("id"): l for l in book["labels"] if isinstance(l, dict)}


def in_scope(label: dict, scope: str | None) -> bool:
    """A label with "applies_to": ["zh"] only exists for items of that scope (a language, a market, a content type)."""
    applies = label.get("applies_to")
    return scope is None or not applies or scope in applies


def scoped(book: dict, scope: str | None) -> dict:
    """The rulebook as it applies to one scope: labels outside it are removed."""
    if scope is None:
        return book
    return {**book, "labels": [l for l in book["labels"] if isinstance(l, dict) and in_scope(l, scope)]}


def view(book: dict, label: dict, lang: str | None) -> dict:
    """One label's rule as plain data in one language."""
    ids = by_id(book)
    out = {"id": label["id"], "name": tx(label.get("name"), lang), "definition": tx(label.get("definition"), lang),
           "include": txs(label.get("include"), lang), "exclude": txs(label.get("exclude"), lang),
           "boundary": [{"with": b.get("with"), "rule": tx(b.get("rule"), lang)} for b in label.get("boundary", [])],
           "source": tx(label.get("source"), lang)}
    # boundary notes written under the other label also apply here
    for other in book["labels"]:
        if other.get("id") == label["id"]:
            continue
        for b in other.get("boundary", []):
            if b.get("with") == label["id"]:
                out["boundary"].append({"with": other["id"], "rule": tx(b.get("rule"), lang)})
    out["precedence"] = [{"labels": p.get("labels", []), "rule": tx(p.get("rule"), lang)}
                         for p in book.get("precedence", [])
                         if label["id"] in p.get("labels", []) and all(x in ids for x in p.get("labels", []))]
    out["boundary"] = [b for b in out["boundary"] if b["with"] in ids]
    return out


def show_text(v: dict) -> str:
    lines = [f"## {v['id']}" + (f": {v['name']}" if v["name"] else ""), "", v["definition"], ""]
    if v["include"]:
        lines += ["Applies when:"] + [f"- {x}" for x in v["include"]] + [""]
    if v["exclude"]:
        lines += ["Does not apply when:"] + [f"- {x}" for x in v["exclude"]] + [""]
    if v["boundary"]:
        lines += ["Boundary with other labels:"] + [f"- {b['with']}: {b['rule']}" for b in v["boundary"]] + [""]
    if v["precedence"]:
        lines += ["When several labels fit:"] + [f"- {' + '.join(p['labels'])}: {p['rule']}" for p in v["precedence"]] + [""]
    if v["source"]:
        lines += [f"Source: {v['source']}", ""]
    return "\n".join(lines)


def between(book: dict, a: str, b: str, lang: str | None) -> dict:
    ids = by_id(book)
    notes = []
    for x, y in ((a, b), (b, a)):
        for bd in ids[x].get("boundary", []):
            if bd.get("with") == y:
                notes.append({"written_under": x, "rule": tx(bd.get("rule"), lang)})
    prec = [{"labels": p.get("labels", []), "rule": tx(p.get("rule"), lang)}
            for p in book.get("precedence", []) if a in p.get("labels", []) and b in p.get("labels", [])]
    return {"labels": [a, b], "boundary": notes, "precedence": prec,
            "may_both_apply": bool(book.get("multi_label", True))}


def keyword_hits(book: dict, text: str, lang: str | None = None) -> list[dict]:
    """Labels whose keywords occur in the text. A keyword list may be keyed by language; all are tried."""
    low = text.lower()
    out = []
    for l in book["labels"]:
        kws = l.get("keywords") or []
        if isinstance(kws, dict):
            kws = [k for v in kws.values() for k in v]
        found = []
        for k in kws:
            k_low = str(k).lower()
            if re.fullmatch(r"[a-z0-9 .'%-]+", k_low):
                # a keyword that starts or ends with a letter or digit must not be part of a longer word
                left = r"(?<![a-z0-9])" if k_low[0].isalnum() else ""
                right = r"(?![a-z0-9])" if k_low[-1].isalnum() else ""
                if re.search(left + re.escape(k_low) + right, low):
                    found.append(k)
            elif k_low in low:
                found.append(k)
        if found:
            out.append({"id": l["id"], "keywords": found})
    return out


def search(book: dict, query: str, lang: str | None) -> list[dict]:
    words = [w for w in re.findall(r"[a-z0-9]+|[一-鿿]+", query.lower()) if w]
    out = []
    for l in book["labels"]:
        v = view(book, l, lang)
        blob = " ".join([v["id"], v["name"], v["definition"], *v["include"], *v["exclude"], *(b["rule"] for b in v["boundary"])]).lower()
        hit = [w for w in words if w in blob]
        if hit:
            out.append({"id": l["id"], "matched": hit, "definition": v["definition"]})
    out.sort(key=lambda x: -len(x["matched"]))
    return out


def lint(book: dict) -> list[str]:
    """Problems that would make the rulebook unusable or ambiguous for a labeller."""
    problems, seen = [], set()
    for n, l in enumerate(book["labels"], 1):
        if not isinstance(l, dict):
            problems.append(f"label {n}: not an object")
            continue
        lid = l.get("id")
        where = f"label {lid or n}"
        for f in REQUIRED:
            if not l.get(f):
                problems.append(f"{where}: missing '{f}'")
        if lid in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(lid)
        if lid and not re.fullmatch(r"[A-Za-z0-9_.#:/-]+", str(lid)):
            problems.append(f"{where}: an id may only use letters, digits and _ . # : / -")
        if "applies_to" in l and not (isinstance(l["applies_to"], list) and l["applies_to"]):
            problems.append(f"{where}: 'applies_to' must be a non-empty list")
        for f in LIST_FIELDS:
            v = l.get(f)
            if v is not None and not isinstance(v, (list, dict)):
                problems.append(f"{where}: '{f}' must be a list")
        if not l.get("exclude"):
            problems.append(f"{where}: no 'exclude' entries (say what looks like this label but is not)")
    ids = {l.get("id") for l in book["labels"] if isinstance(l, dict)}
    for l in book["labels"]:
        if not isinstance(l, dict):
            continue
        for b in l.get("boundary", []):
            if b.get("with") not in ids:
                problems.append(f"label {l.get('id')}: boundary with unknown label {b.get('with')!r}")
            if b.get("with") == l.get("id"):
                problems.append(f"label {l.get('id')}: boundary with itself")
            if not b.get("rule"):
                problems.append(f"label {l.get('id')}: boundary with {b.get('with')} has no rule")
    for n, p in enumerate(book.get("precedence", []), 1):
        for lid in p.get("labels", []):
            if lid not in ids:
                problems.append(f"precedence {n}: unknown label {lid!r}")
        if len(p.get("labels", [])) < 2 or not p.get("rule"):
            problems.append(f"precedence {n}: needs two or more labels and a rule")
    if "multi_label" not in book:
        problems.append("rulebook: say whether an item may carry several labels ('multi_label': true or false)")
    if "empty_allowed" not in book:
        problems.append("rulebook: say whether an item may carry no label ('empty_allowed': true or false)")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Look up label rules in a rulebook.")
    ap.add_argument("rulebook")
    ap.add_argument("command", choices=["list", "show", "between", "match", "search", "lint"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--text", help="for match: the item text")
    ap.add_argument("--lang", help="language of bilingual rule text, e.g. zh or en")
    ap.add_argument("--scope", help="only labels whose 'applies_to' includes this value (labels without 'applies_to' always count)")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args(argv)
    try:
        book = load(a.rulebook)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    full_book = book
    book = scoped(book, a.scope)
    ids = by_id(book)
    as_json = a.format == "json"

    def emit(data, text: str) -> None:
        print(json.dumps(data, ensure_ascii=False, indent=1) if as_json else text.rstrip("\n"))

    if a.command == "list":
        rows = [{"id": l["id"], "name": tx(l.get("name"), a.lang), "definition": tx(l.get("definition"), a.lang)} for l in book["labels"]]
        emit(rows, "\n".join(f"- {r['id']}" + (f" ({r['name']})" if r["name"] else "") + f": {r['definition']}" for r in rows))
        return 0
    if a.command == "show":
        unknown = [x for x in a.args if x not in ids]
        if unknown or not a.args:
            print(f"error: unknown label(s) {unknown}; known: {', '.join(map(str, ids))}", file=sys.stderr)
            return 2
        views = [view(book, ids[x], a.lang) for x in a.args]
        general = txs(book.get("general"), a.lang)
        text = "\n".join(show_text(v) for v in views)
        if general:
            text += "\nRules for every label:\n" + "\n".join(f"- {g}" for g in general)
        emit({"labels": views, "general": general}, text)
        return 0
    if a.command == "between":
        if len(a.args) != 2 or any(x not in ids for x in a.args):
            print(f"error: give two known labels; known: {', '.join(map(str, ids))}", file=sys.stderr)
            return 2
        r = between(book, a.args[0], a.args[1], a.lang)
        lines = [f"## {a.args[0]} and {a.args[1]}", ""]
        lines += [f"- ({b['written_under']}) {b['rule']}" for b in r["boundary"]] or ["- The rulebook has no boundary rule for this pair."]
        lines += [f"- When both fit: {p['rule']}" for p in r["precedence"]]
        if not r["precedence"]:
            lines.append("- Both may be given to one item." if r["may_both_apply"] else "- Only one label per item: the rulebook does not say which wins.")
        emit(r, "\n".join(lines))
        return 0 if r["boundary"] or r["precedence"] else 1
    if a.command == "match":
        text = a.text if a.text is not None else " ".join(a.args)
        hits = keyword_hits(book, text, a.lang)
        emit(hits, "\n".join(f"- {h['id']}: {', '.join(map(str, h['keywords']))}" for h in hits) or "No label keyword occurs in the text.")
        return 0 if hits else 1
    if a.command == "search":
        hits = search(book, " ".join(a.args), a.lang)
        emit(hits, "\n".join(f"- {h['id']} (matched: {', '.join(h['matched'])}): {h['definition']}" for h in hits) or "No rule mentions these words.")
        return 0 if hits else 1
    problems = lint(full_book)
    emit({"labels": len(full_book["labels"]), "problems": problems},
         f"{len(book['labels'])} labels, {len(problems)} problem(s)." + "".join(f"\n- {p}" for p in problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
