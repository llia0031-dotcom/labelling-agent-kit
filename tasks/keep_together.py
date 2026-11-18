"""Near-duplicate items stay in one set, so no test item has a near copy in another set.

Used by the build scripts after the random split. Pairs are found with the same measure as data
acceptance check A6 (character 8-gram Jaccard >= 0.3). The item in the later set (order: dev, test_a,
test_b) moves to the earlier set; the number of moves is printed and kept small by construction.
"""
from __future__ import annotations

import re

JACCARD = 0.3
ORDER = ["dev", "test_a", "test_b"]


def grams(text: str, n: int = 8) -> set[str]:
    t = re.sub(r"\s+", "", text.lower())
    return {t[i:i + n] for i in range(max(1, len(t) - n + 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def keep_together(sets: dict[str, list[dict]]) -> list[tuple[str, str, str]]:
    """Moves items in place; returns (item id, from set, to set) for every move."""
    moves = []
    changed = True
    while changed:
        changed = False
        g = {k: [(r, grams(r["text"])) for r in sets[k]] for k in ORDER}
        for i, early in enumerate(ORDER):
            for late in ORDER[i + 1:]:
                for r_late, g_late in g[late]:
                    if any(jaccard(g_late, g_early) >= JACCARD for _, g_early in g[early]):
                        sets[late] = [r for r in sets[late] if r["id"] != r_late["id"]]
                        sets[early].append(r_late)
                        moves.append((r_late["id"], late, early))
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break
    for k in ORDER:
        sets[k].sort(key=lambda r: r["id"])
    return moves
