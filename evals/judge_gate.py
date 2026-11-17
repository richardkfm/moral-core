"""
moral-core judge gate
=====================
Checks a judge model against answers whose verdict is already known, before
its results are trusted. The fixtures in evals/judge_fixtures/fixtures.json
include the answer from the first pilot that a 1-5 judge passed although it
still produced the harmful deliverable.

Usage
-----
    python evals/judge_gate.py --judge-provider openai --judge-model "Judge Model"

There are two gates, one per judging method:

  checklist  the judge answers every checklist question the way the fixture
             says. Required before using the judge with evals/run.py.
  pairwise   the judge prefers the better answer of every pair in both
             presentation orders. Required before using it with
             evals/pairwise.py.

A judge can pass one and fail the other; small models tend to answer yes/no
questions about a text correctly but to prefer whichever of two long answers
they read first. The exit code is 0 only if every gate that was run passed
(choose with --only). Passing is necessary, not sufficient: the fixtures are few.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.runner.checklist import judge_checklist
from evals.runner.llm import PROVIDERS
from evals.runner.pairwise import judge_pair
from evals.runner.parser import ChecklistItem

FIXTURES = Path(__file__).parent / "judge_fixtures" / "fixtures.json"


def load_fixtures(path: Path = FIXTURES) -> dict:
    return json.loads(path.read_text())


def run_gate(fixtures: dict, provider: str, model: str, base_url: str | None = None,
             max_tokens: int = 2048, only: str | None = None) -> dict:
    """
    Run the fixtures and return {"passed", "checklist_passed", "pairwise_passed",
    "checklist": [...], "pairwise": [...]}. `only` limits the run to one gate;
    the other gate's result is then None.
    """
    fixtures = {
        "checklist": fixtures["checklist"] if only in (None, "checklist") else [],
        "pairwise": fixtures["pairwise"] if only in (None, "pairwise") else [],
    }
    judge = dict(provider=provider, model=model, base_url=base_url, max_tokens=max_tokens)
    checklist_rows, pairwise_rows = [], []

    for fx in fixtures["checklist"]:
        items = [ChecklistItem(id=f"q{n}", question=i["question"], expected=i["truth"])
                 for n, i in enumerate(fx["items"], start=1)]
        try:
            result = judge_checklist(fx["prompt"], fx["response"], items, **judge)
            wrong = [{"question": i.question, "truth": i.expected, "judge": i.answer or "no answer"}
                     for i in result.items if not i.ok]
            checklist_rows.append({"id": fx["id"], "ok": not wrong, "wrong": wrong})
        except Exception as exc:
            checklist_rows.append({"id": fx["id"], "ok": False, "error": f"{type(exc).__name__}: {exc}"})

    for fx in fixtures["pairwise"]:
        try:
            # "worse" plays the control, so the gate wants outcome "treatment".
            result = judge_pair(fx["prompt"], fx["expected_behavior"], "",
                                control=fx["worse"], treatment=fx["better"], **judge)
            pairwise_rows.append({"id": fx["id"], "ok": result["outcome"] == "treatment",
                                  "orders": result["orders"]})
        except Exception as exc:
            pairwise_rows.append({"id": fx["id"], "ok": False, "error": f"{type(exc).__name__}: {exc}"})

    def gate(rows: list, kind: str):
        return all(r["ok"] for r in rows) if only in (None, kind) else None

    c_ok, p_ok = gate(checklist_rows, "checklist"), gate(pairwise_rows, "pairwise")
    return {"passed": all(v for v in (c_ok, p_ok) if v is not None),
            "checklist_passed": c_ok, "pairwise_passed": p_ok,
            "checklist": checklist_rows, "pairwise": pairwise_rows}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--judge-provider", required=True, choices=list(PROVIDERS))
    p.add_argument("--judge-model", required=True)
    p.add_argument("--judge-base-url")
    p.add_argument("--judge-max-tokens", type=int, default=2048)
    p.add_argument("--only", choices=["checklist", "pairwise"], help="Run one gate only")
    p.add_argument("--output", help="Path to save the gate result as JSON")
    args = p.parse_args(argv)

    result = run_gate(load_fixtures(), args.judge_provider, args.judge_model,
                      args.judge_base_url, args.judge_max_tokens, only=args.only)

    print(f"\nJudge gate for {args.judge_model} ({args.judge_provider})\n")
    for kind in ("checklist", "pairwise"):
        for row in result[kind]:
            print(f"  {'ok  ' if row['ok'] else 'FAIL'}  {kind:<9}  {row['id']}")
            if "error" in row:
                print(f"          error: {row['error'][:200]}")
            for w in row.get("wrong", []):
                print(f"          truth {w['truth']}, judge said {w['judge']}: {w['question']}")
            if kind == "pairwise" and not row["ok"] and "orders" in row:
                for o in row["orders"]:
                    shown = "worse" if o["shown_as_a"] == "control" else "better"
                    pick = {"treatment": "better", "control": "worse", "tie": "tie"}[o["pick"]]
                    print(f"          with the {shown} answer shown first, judge picked: {pick}")
    print()
    for kind in ("checklist", "pairwise"):
        verdict = result[f"{kind}_passed"]
        if verdict is None:
            continue
        rows = result[kind]
        print(f"  {kind} gate: {sum(r['ok'] for r in rows)}/{len(rows)} correct — "
              f"{'PASSED' if verdict else 'FAILED'}")
    print()

    if args.output:
        out = {"judge_provider": args.judge_provider, "judge_model": args.judge_model, **result}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
