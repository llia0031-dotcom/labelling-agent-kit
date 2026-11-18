#!/usr/bin/env python3
"""case_search.py - find labelled cases that resemble a new item (BM25, Chinese and English).

The case file is JSONL: each line has an id, a text and its labels. The script ranks the cases against
the query text with BM25 (Okapi) and prints the closest ones with their labels, so a labeller or a
labelling agent can see how similar content was labelled before.

    python case_search.py cases.jsonl --query "best mattress in the world, period" -k 5
    python case_search.py cases.jsonl --query-file item.txt -k 8 --per-label 2
    python case_search.py cases.jsonl --query "..." --label ABSOLUTE          # only cases with this label
    python case_search.py cases.jsonl --query "..." --exclude-id test-042 --format json
    python case_search.py cases.jsonl --phrase "环境一般"     # how were cases containing this phrase labelled?

Tokens: lower-cased words and numbers for Latin text; single characters and character pairs for Chinese,
Japanese and Korean text, so no word segmenter is needed. --per-label N keeps at most N cases per
label combination, which stops one frequent label from filling the whole result. --snippet N shows at
most N characters of a long case, centred on the part that best matches the query.

--phrase counts the cases that contain the exact phrase and the share of them carrying each label: a
quick way to see a labelling convention ("of 37 cases that say 环境一般, 34 carry Ambience#Noise").

Python 3.9+, standard library only. Exit code 0: results printed; 1: nothing matched; 2: bad input.
The scores equal rank_bm25's BM25Okapi on the same tokens (tested in the repository).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+(?:['’][a-z]+)?|[㐀-䶿一-鿿぀-ヿ가-힯]+")
CJK_RE = re.compile(r"[㐀-䶿一-鿿぀-ヿ가-힯]")


def tokens(text: str) -> list[str]:
    out = []
    for m in TOKEN_RE.finditer((text or "").lower()):
        s = m.group(0)
        if CJK_RE.match(s):
            out.extend(s)                                   # single characters
            out.extend(s[i:i + 2] for i in range(len(s) - 1))   # character pairs
        else:
            out.append(s)
    return out


class BM25:
    """BM25 Okapi with the constants and the negative-IDF floor of rank_bm25.BM25Okapi."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75, epsilon: float = 0.25):
        self.k1, self.b = k1, b
        self.n = len(docs)
        self.freqs = [Counter(d) for d in docs]
        self.lengths = [len(d) for d in docs]
        self.avg = sum(self.lengths) / self.n if self.n else 0.0
        df: Counter = Counter()
        for f in self.freqs:
            df.update(f.keys())
        self.idf, negative, total = {}, [], 0.0
        for term, n_t in df.items():
            v = math.log(self.n - n_t + 0.5) - math.log(n_t + 0.5)
            self.idf[term] = v
            total += v
            if v < 0:
                negative.append(term)
        floor = epsilon * (total / len(self.idf)) if self.idf else 0.0
        for term in negative:
            self.idf[term] = floor

    def scores(self, query: list[str]) -> list[float]:
        out = [0.0] * self.n
        for q in query:
            idf = self.idf.get(q)
            if idf is None:
                continue
            for i, f in enumerate(self.freqs):
                tf = f.get(q, 0)
                if tf:
                    out[i] += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg))
        return out


def read_cases(path: str, text_field: str = "text", label_field: str = "labels", id_field: str = "id") -> list[dict]:
    cases = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}: line {n} is not valid JSON ({e.msg})")
        text = r.get(text_field)
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"{path}: line {n} has no '{text_field}'")
        labels = r.get(label_field, [])
        labels = [labels] if isinstance(labels, str) else list(labels or [])
        cases.append({"id": r.get(id_field, n), "text": text, "labels": labels,
                      "note": r.get("note"), "source": r.get("source")})
    return cases


def snippet(text: str, query: str, width: int) -> str:
    """At most `width` characters of the text, centred on the window that shares most tokens with the query."""
    text = " ".join(text.split())
    if width <= 0 or len(text) <= width:
        return text
    q = set(tokens(query))
    best, best_at = -1, 0
    step = max(1, width // 4)
    for start in range(0, len(text) - width + step, step):
        start = min(start, len(text) - width)
        score = len(q & set(tokens(text[start:start + width])))
        if score > best:
            best, best_at = score, start
    out = text[best_at:best_at + width]
    return ("…" if best_at > 0 else "") + out + ("…" if best_at + width < len(text) else "")


def phrase_stats(cases: list[dict], phrase: str, examples: int = 3, width: int = 60) -> dict:
    """Cases whose text contains the phrase (case-insensitive) and the share of them carrying each label."""
    low = phrase.lower()
    hits = [c for c in cases if low in c["text"].lower()]
    counts: Counter = Counter(l for c in hits for l in c["labels"])
    no_label = sum(1 for c in hits if not c["labels"])
    shares = [{"label": l, "cases": n, "share": round(n / len(hits), 3)} for l, n in counts.most_common()]
    ex = []
    for c in hits[:examples]:
        i = c["text"].lower().find(low)
        lo, hi = max(0, i - width // 2), min(len(c["text"]), i + len(phrase) + width // 2)
        ex.append({"id": c["id"], "labels": c["labels"],
                   "text": ("…" if lo > 0 else "") + " ".join(c["text"][lo:hi].split()) + ("…" if hi < len(c["text"]) else "")})
    return {"phrase": phrase, "cases_with_phrase": len(hits), "of_all_cases": len(cases), "without_label": no_label,
            "label_shares": shares, "examples": ex}


class CaseIndex:
    def __init__(self, cases: list[dict]):
        self.cases = cases
        self.bm25 = BM25([tokens(c["text"]) for c in cases])

    def search(self, query: str, k: int = 5, label: str | None = None, exclude_ids=(), per_label: int = 0,
               min_score: float = 0.0) -> list[dict]:
        scores = self.bm25.scores(tokens(query))
        order = sorted(range(len(self.cases)), key=lambda i: (-scores[i], i))
        excluded = set(exclude_ids)
        out, per = [], Counter()
        for i in order:
            if scores[i] <= min_score:
                break
            c = self.cases[i]
            if c["id"] in excluded or (label is not None and label not in c["labels"]):
                continue
            key = tuple(sorted(c["labels"]))
            if per_label and per[key] >= per_label:
                continue
            per[key] += 1
            out.append({**c, "score": round(scores[i], 4)})
            if len(out) >= k:
                break
        return out


def phrase_markdown(st: dict) -> str:
    if not st["cases_with_phrase"]:
        return f"No case contains \"{st['phrase']}\" ({st['of_all_cases']} cases searched).\n"
    lines = [f"**{st['cases_with_phrase']} of {st['of_all_cases']} cases contain \"{st['phrase']}\".** "
             f"Share carrying each label (no label: {st['without_label']}):", ""]
    lines += [f"- {s['label']}: {s['cases']} ({100 * s['share']:.0f}%)" for s in st["label_shares"]] or ["- (none)"]
    lines += ["", "Examples:"] + [f"- [{', '.join(e['labels']) or 'no label'}] {e['text']}" for e in st["examples"]]
    return "\n".join(lines) + "\n"


def to_markdown(hits: list[dict], query: str) -> str:
    if not hits:
        return "No case shares a word with the query.\n"
    lines = [f"**{len(hits)} closest cases** for: {query[:120]}{'…' if len(query) > 120 else ''}", "",
             "| # | Labels | Case | Score | Id |", "|---|---|---|---|---|"]
    for n, h in enumerate(hits, 1):
        text = h["text"].replace("\n", " ").replace("|", "\\|")
        labels = ", ".join(h["labels"]) if h["labels"] else "(no label)"
        lines.append(f"| {n} | {labels} | {text} | {h['score']:.2f} | {h['id']} |")
    lines += ["", "Cases are evidence of how similar content was labelled, not rules. When a case and the label rules disagree, the rules win."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Find labelled cases similar to a text (BM25).")
    ap.add_argument("cases")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--query")
    g.add_argument("--query-file")
    g.add_argument("--phrase", help="label shares among the cases that contain this exact phrase")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--label", help="only cases that carry this label")
    ap.add_argument("--per-label", type=int, default=0, help="at most this many cases per label combination (0 = no limit)")
    ap.add_argument("--exclude-id", action="append", default=[])
    ap.add_argument("--snippet", type=int, default=0, help="show at most this many characters of each case (0 = all)")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--label-field", default="labels")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args(argv)
    try:
        cases = read_cases(a.cases, a.text_field, a.label_field, a.id_field)
        if a.phrase is not None:
            st = phrase_stats(cases, a.phrase)
            sys.stdout.reconfigure(encoding="utf-8")
            print(json.dumps(st, ensure_ascii=False, indent=1) if a.format == "json" else phrase_markdown(st), end="\n" if a.format == "json" else "")
            return 0 if st["cases_with_phrase"] else 1
        query = a.query if a.query is not None else Path(a.query_file).read_text(encoding="utf-8-sig")
        index = CaseIndex(cases)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    hits = index.search(query, a.k, a.label, a.exclude_id, a.per_label)
    if a.snippet:
        hits = [{**h, "text": snippet(h["text"], query, a.snippet)} for h in hits]
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(hits, ensure_ascii=False, indent=1) if a.format == "json" else to_markdown(hits, query), end="\n" if a.format == "json" else "")
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
