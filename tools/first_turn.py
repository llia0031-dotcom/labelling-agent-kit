"""How each arm's first model turn ended (answered, or called a tool), and which tools were called, from the
stored answers of an experiment.

    python tools/first_turn.py dev1      # -> results/dev1/FIRST_TURN.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    name = sys.argv[1]
    store = ROOT / "results" / name / "responses.jsonl"
    first, tools = Counter(), Counter()
    items = Counter()
    sys.path.insert(0, str(ROOT))
    from lak.llm import store_lines
    for line in store_lines(store):
        e = json.loads(line)
        task, set_name, arm, rest = e["key"].split("|")
        if rest.split("#")[1] != "1":
            for b in e["response"]["content"]:
                if b.get("type") == "tool_use":
                    tools[(task, arm, b["name"])] += 1
            continue
        items[(task, arm)] += 1
        first[(task, arm, e["response"]["stop_reason"])] += 1
        for b in e["response"]["content"]:
            if b.get("type") == "tool_use":
                tools[(task, arm, b["name"])] += 1
    lines = [f"# First model turn per arm: {name}", "",
             "| Task | Arm | Items | First turn called a tool | First turn answered |", "|---|---|---|---|---|"]
    for (task, arm), n in sorted(items.items()):
        lines.append(f"| {task} | {arm} | {n} | {first[(task, arm, 'tool_use')]} of {n} | {first[(task, arm, 'end_turn')]} of {n} |")
    lines += ["", "| Task | Arm | Tool | Calls (all turns) |", "|---|---|---|---|"]
    lines += [f"| {t} | {a} | {tool} | {n} |" for (t, a, tool), n in sorted(tools.items())]
    out = ROOT / "results" / name / "FIRST_TURN.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines[:20]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
