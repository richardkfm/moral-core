"""
moral-core eval comparison
==========================
Compares two result files written by `evals/run.py --output` on the same test
cases — typically a control run (`--no-skills`) against a run with skills
loaded — and prints the paired difference as markdown.

Usage
-----
    python evals/compare.py CONTROL.json TREATMENT.json

Only test cases scored in both files are compared. Deltas are
treatment minus control; a positive delta means the second file scored higher.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DIMENSIONS = ["harm_avoidance", "helpfulness", "proportionality", "clarity", "honesty"]


def _load(path: str) -> tuple[dict, dict[str, dict]]:
    data = json.loads(Path(path).read_text())
    scored = {r["id"]: r for r in data["results"] if r.get("scores")}
    return data, scored


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _label(data: dict) -> str:
    meta = data["meta"]
    return "with skills" if meta.get("skills_loaded", True) else "no skills"


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    control, control_scored = _load(argv[1])
    treatment, treatment_scored = _load(argv[2])
    ids = [i for i in control_scored if i in treatment_scored]
    if not ids:
        print("No test cases were scored in both files.", file=sys.stderr)
        return 1

    a, b = _label(control), _label(treatment)
    print(f"Model: {treatment['meta']['model']}  |  Judge: {treatment['meta']['judge_model']}")
    print(f"Paired test cases: {len(ids)} "
          f"(of {len(control['results'])} / {len(treatment['results'])} run)\n")

    print(f"| Dimension | {a} | {b} | delta |")
    print("|---|---|---|---|")
    for dim in DIMENSIONS + ["average"]:
        if dim == "average":
            x = _mean([control_scored[i]["average"] for i in ids])
            y = _mean([treatment_scored[i]["average"] for i in ids])
        else:
            x = _mean([control_scored[i]["scores"][dim] for i in ids])
            y = _mean([treatment_scored[i]["scores"][dim] for i in ids])
        print(f"| {dim} | {x:.2f} | {y:.2f} | {y - x:+.2f} |")

    deltas = [treatment_scored[i]["average"] - control_scored[i]["average"] for i in ids]
    better = sum(d > 0 for d in deltas)
    worse = sum(d < 0 for d in deltas)
    print(f"\nPer case: {better} higher, {worse} lower, {len(ids) - better - worse} unchanged\n")

    print(f"| Test case | suite | {a} | {b} | delta |")
    print("|---|---|---|---|---|")
    for i in sorted(ids, key=lambda i: treatment_scored[i]["average"] - control_scored[i]["average"]):
        c, t = control_scored[i], treatment_scored[i]
        print(f"| {t['title']} | {t['suite']} | {c['average']:.1f} ({c['status']}) "
              f"| {t['average']:.1f} ({t['status']}) | {t['average'] - c['average']:+.1f} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
