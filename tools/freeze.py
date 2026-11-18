"""Freezes an experiment: writes the fingerprints of every file its runs read into the experiment file and into
the preregistration's Fingerprints section.

    python tools/freeze.py experiments/main.json --prompts v1
    python tools/freeze.py experiments/main.json --check      # exit 1 if a frozen file changed
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lak.run import check_frozen, freeze_list  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment")
    ap.add_argument("--prompts", nargs="*", default=["v1"])
    ap.add_argument("--prereg", default="experiments/PREREGISTRATION.md")
    ap.add_argument("--section", default="## Fingerprints")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    path = ROOT / a.experiment
    exp = json.loads(path.read_text(encoding="utf-8"))
    if a.check:
        problems = check_frozen(exp)
        print("\n".join(problems) or f"all {len(exp.get('frozen', {}))} frozen files unchanged")
        return 1 if problems else 0
    tasks = sorted({r["task"] for r in exp["runs"]})
    extra = {}
    for r in exp["runs"]:
        for arm in r["arms"]:
            if arm.get("rules_file"):
                from lak.task import get_task, sha12
                extra[f"tasks/{r['task']}/{arm['rules_file']}"] = sha12(get_task(r["task"]).dir / arm["rules_file"])
    frozen = {**freeze_list(tasks, a.prompts), **extra}
    exp["frozen"] = dict(sorted(frozen.items()))
    path.write_text(json.dumps(exp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    pre = ROOT / a.prereg
    text = pre.read_text(encoding="utf-8")
    table = "\n".join(["| File | sha256 (first 12) |", "|---|---|"] + [f"| `{k}` | `{v}` |" for k, v in exp["frozen"].items()])
    head = a.section
    start = text.index(head)
    nxt = text.find("\n## ", start + len(head))
    body = text[start:nxt if nxt != -1 else len(text)]
    intro = body.split("\n\n")[1] if body.count("\n\n") >= 1 else ""
    new_body = f"{head}\n\n{intro}\n\n{table}\n"
    text = text[:start] + new_body + (text[nxt:] if nxt != -1 else "")
    pre.write_text(text, encoding="utf-8", newline="\n")
    print(f"froze {len(exp['frozen'])} files into {a.experiment} and {a.prereg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
