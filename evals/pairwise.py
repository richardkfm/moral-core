"""
moral-core blinded pairwise comparison
======================================
Takes two result files from `evals/run.py --output` (a control and a
treatment condition on the same test cases) and asks a judge, for every pair
of answers, which one is better. The judge does not know which condition
wrote which answer, and sees every pair in both orders.

Usage
-----
    python evals/pairwise.py CONTROL.json TREATMENT.json \
        --judge-provider openai --judge-model "Judge Model" \
        --output evals/results/pairwise-full.json

Reading the result
------------------
The win rate is from the treatment's point of view: a win counts 1, a tie 0.5,
a loss 0, averaged per test case and then over test cases. 50% means the judge
has no preference. The 95% interval is a bootstrap over test cases; if it
includes 50%, the run does not show a difference.

Benign cases are reported separately: there, a "win" for a condition with
skills loaded means it helped at least as well as the bare model.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.compare import load
from evals.runner.llm import PROVIDERS
from evals.runner.pairwise import judge_pair
from evals.runner.parser import load_suite
from evals.runner.stats import bootstrap_ci, mean


def _usable(sample: dict) -> bool:
    return not sample.get("error") and bool(sample.get("response"))


def summarise(case_rows: list[dict]) -> dict:
    scored = [c for c in case_rows if c["score"] is not None]
    if not scored:
        return {"cases": 0, "win_rate": None, "ci": None, "wins": 0, "ties": 0, "losses": 0}
    scores = [c["score"] for c in scored]
    pairs = [p for c in scored for p in c["pairs"] if "outcome" in p]
    ci = bootstrap_ci(scores)
    return {
        "cases": len(scored),
        "win_rate": mean(scores),
        "ci": list(ci) if ci else None,
        "wins": sum(p["outcome"] == "treatment" for p in pairs),
        "ties": sum(p["outcome"] == "tie" for p in pairs),
        "losses": sum(p["outcome"] == "control" for p in pairs),
        "inconsistent": sum(not p["consistent"] for p in pairs),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("control")
    p.add_argument("treatment")
    p.add_argument("--judge-provider", required=True, choices=list(PROVIDERS))
    p.add_argument("--judge-model", required=True)
    p.add_argument("--judge-base-url")
    p.add_argument("--judge-max-tokens", type=int, default=1024)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--output", help="Path to save JSON results")
    args = p.parse_args(argv)

    control, treatment = load(args.control), load(args.treatment)
    cases = {c.id: c for c in load_suite(Path(__file__).parent)}
    ids = [i for i in control["by_id"] if i in treatment["by_id"] and i in cases]
    if not ids:
        print("No test case appears in both files.", file=sys.stderr)
        return 1

    def judge_case(cid: str) -> dict:
        case = cases[cid]
        a = [s for s in control["by_id"][cid]["samples"] if _usable(s)]
        b = [s for s in treatment["by_id"][cid]["samples"] if _usable(s)]
        pairs = []
        for sa, sb in zip(a, b):
            try:
                pairs.append(judge_pair(
                    case.prompt, case.expected_behavior, case.failure_modes,
                    sa["response"], sb["response"],
                    provider=args.judge_provider, model=args.judge_model,
                    base_url=args.judge_base_url, max_tokens=args.judge_max_tokens,
                ))
            except Exception as exc:
                pairs.append({"error": f"{type(exc).__name__}: {exc}"})
        scores = [p["score"] for p in pairs if "score" in p]
        return {"id": cid, "title": case.title, "suite": case.suite,
                "score": mean(scores) if scores else None, "pairs": pairs}

    rows = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        for n, row in enumerate(pool.map(judge_case, ids), start=1):
            rows.append(row)
            shown = "n/a" if row["score"] is None else f"{row['score']:.2f}"
            print(f"  [{n}/{len(ids)}]  {shown}  {row['title'][:60]}", flush=True)

    main_rows = [r for r in rows if r["suite"] != "benign"]
    benign_rows = [r for r in rows if r["suite"] == "benign"]
    summary = summarise(main_rows)
    summary["benign"] = summarise(benign_rows)
    summary["errors"] = sum("error" in p for r in rows for p in r["pairs"])

    c_name, t_name = control["meta"]["condition"], treatment["meta"]["condition"]

    def line(label: str, s: dict) -> None:
        if not s["cases"]:
            return
        ci = "n/a" if not s["ci"] else f"{s['ci'][0] * 100:.0f} to {s['ci'][1] * 100:.0f}"
        print(f"  {label}: win rate {s['win_rate'] * 100:.0f}%  (95% CI {ci}), "
              f"{s['cases']} cases, pairs won/tied/lost {s['wins']}/{s['ties']}/{s['losses']}, "
              f"{s['inconsistent']} tied because the two orders disagreed")

    print(f"\n{t_name} against {c_name}, judged by {args.judge_model}")
    line("adversarial + scenario", summary)
    line("benign", summary["benign"])
    if summary["errors"]:
        print(f"  {summary['errors']} pair(s) lost to judge errors")

    if args.output:
        out = {
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model": treatment["meta"]["model"],
                "control": c_name, "treatment": t_name,
                "judge_provider": args.judge_provider, "judge_model": args.judge_model,
            },
            "summary": summary,
            "cases": rows,
        }
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(f"Results saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
