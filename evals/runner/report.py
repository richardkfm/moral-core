"""
evals/runner/report.py
----------------------
Result records, terminal output and JSON output for evaluation runs.

One test case is answered `--repeats` times. Each answer is a Sample with one
of five outcomes:

    PASS       every checklist item answered as wanted (or rubric PASS)
    WARN       rubric only: a dimension below its green threshold
    FAIL       a checklist item answered the wrong way (or rubric FAIL)
    TRUNCATED  the model ran out of tokens; the answer is kept but not judged
    ERROR      the model or the judge call failed; nothing to judge

TRUNCATED and ERROR samples never enter a pass rate or a mean.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .checklist import ChecklistResult
from .judge import DIMENSIONS, ScoreResult
from .parser import TestCase
from .stats import mean, median

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_RED    = "\033[91m"
_YELLOW = "\033[93m"
_GREEN  = "\033[92m"
_GREY   = "\033[90m"


def _c(text: str, code: str, use_color: bool) -> str:
    return f"{code}{text}{_RESET}" if use_color else text


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

@dataclass
class Sample:
    repeat: int
    response: str = ""
    finish_reason: Optional[str] = None
    truncated: bool = False
    jargon: list[str] = field(default_factory=list)
    checklist: Optional[ChecklistResult] = None
    rubric: Optional[ScoreResult] = None
    error: Optional[str] = None
    draft: Optional[str] = None      # first answer, when --check replaced it
    rewritten: bool = False          # --check replaced the draft

    def outcome(self) -> str:
        if self.error:
            return "ERROR"
        if self.truncated:
            return "TRUNCATED"
        if self.checklist is not None and self.checklist.items:
            return "PASS" if self.checklist.passed else "FAIL"
        if self.rubric is not None:
            return self.rubric.status()
        return "ERROR"

    def as_dict(self) -> dict:
        rubric = None
        if self.rubric is not None:
            rubric = {
                "scores": self.rubric.as_dict(),
                "average": round(self.rubric.average(), 2),
                "status": self.rubric.status(),
                "reasoning": self.rubric.reasoning,
            }
        return {
            "repeat":        self.repeat,
            "outcome":       self.outcome(),
            "finish_reason": self.finish_reason,
            "truncated":     self.truncated,
            "chars":         len(self.response),
            "jargon":        self.jargon,
            "checklist":     self.checklist.as_dict() if self.checklist else None,
            "rubric":        rubric,
            "error":         self.error,
            "response":      self.response,
            "rewritten":     self.rewritten,
            "draft":         self.draft,
        }


@dataclass
class EvalResult:
    case: TestCase
    samples: list[Sample] = field(default_factory=list)
    system_prompt_chars: int = 0

    def outcomes(self) -> list[str]:
        return [s.outcome() for s in self.samples]

    def as_dict(self) -> dict:
        return {
            "id":            self.case.id,
            "title":         self.case.title,
            "suite":         self.case.suite,
            "source_file":   self.case.source_file,
            "target_skills": self.case.target_skills,
            "system_prompt_chars": self.system_prompt_chars,
            "samples":       [s.as_dict() for s in self.samples],
        }


# ---------------------------------------------------------------------------
# Aggregate stats
# ---------------------------------------------------------------------------

def _rate(part: int, whole: int) -> Optional[float]:
    return part / whole if whole else None


def compute_stats(results: list[EvalResult]) -> dict:
    samples = [(r.case, s) for r in results for s in r.samples]
    outcomes = [s.outcome() for _, s in samples]
    counts = {o: outcomes.count(o) for o in ("PASS", "WARN", "FAIL", "TRUNCATED", "ERROR")}
    judged = counts["PASS"] + counts["WARN"] + counts["FAIL"]
    answered = [s for _, s in samples if not s.error]

    by_suite = {}
    for suite in sorted({c.suite for c, _ in samples}):
        outs = [s.outcome() for c, s in samples if c.suite == suite]
        n = sum(o in ("PASS", "WARN", "FAIL") for o in outs)
        by_suite[suite] = {"judged": n, "pass_rate": _rate(outs.count("PASS"), n)}

    benign = [
        s.checklist.refused for c, s in samples
        if c.suite == "benign" and s.outcome() in ("PASS", "FAIL")
        and s.checklist is not None and s.checklist.refused is not None
    ]

    rubric = [s.rubric for _, s in samples if s.rubric is not None and s.outcome() not in ("ERROR", "TRUNCATED")]
    dim_means = {d: mean([getattr(r, d) for r in rubric]) for d in DIMENSIONS} if rubric else {}

    return {
        "cases":            len(results),
        "samples":          len(samples),
        "judged":           judged,
        **{k.lower(): v for k, v in counts.items()},
        "pass_rate":        _rate(counts["PASS"], judged),
        "pass_rate_by_suite": by_suite,
        "over_refusal_rate": _rate(sum(benign), len(benign)),
        "truncation_rate":  _rate(counts["TRUNCATED"], len(answered)),
        "jargon_rate":      _rate(sum(bool(s.jargon) for s in answered), len(answered)),
        "median_chars":     median([len(s.response) for s in answered]) if answered else None,
        "rubric_dim_means": dim_means,
    }


# ---------------------------------------------------------------------------
# Terminal printer
# ---------------------------------------------------------------------------

def print_header(provider: str, model: str, judge_model: str, suite: str,
                 n_cases: int, use_color: bool = True, condition: str = "full",
                 repeats: int = 1) -> None:
    sep = _c("=" * 56, _BOLD, use_color)
    print(f"\n{sep}")
    print(_c("  moral-core eval runner", _BOLD, use_color))
    print(sep)
    print(f"  Suite:       {suite}")
    print(f"  Condition:   {condition}")
    print(f"  Provider:    {provider}  /  model: {model}")
    print(f"  Judge:       {judge_model}")
    print(f"  Test cases:  {n_cases}  x {repeats} repeat(s)")
    print(f"{sep}\n")


_OUTCOME_STYLE = {
    "PASS": ("✓", _GREEN), "WARN": ("~", _YELLOW), "FAIL": ("✗", _RED),
    "TRUNCATED": ("…", _YELLOW), "ERROR": ("!", _RED),
}


def print_result(idx: int, total: int, result: EvalResult, use_color: bool = True) -> None:
    outs = result.outcomes()
    marks = "".join(_c(_OUTCOME_STYLE[o][0], _OUTCOME_STYLE[o][1], use_color) for o in outs)
    counter = _c(f"[{idx}/{total}]", _GREY, use_color)
    print(f"  {counter}  {marks}  {result.case.title[:60]}", flush=True)

    shown: set[str] = set()
    for s in result.samples:
        if s.error and s.error not in shown:
            shown.add(s.error)
            print(f"           ↳ error: {s.error[:160]}")
        elif s.outcome() == "FAIL" and s.checklist is not None:
            for item in s.checklist.items:
                if not item.ok and item.id not in shown:
                    shown.add(item.id)
                    got = item.answer or "no answer"
                    print(_c(f"           ↳ {item.id}: wanted {item.expected}, got {got} — {item.question}",
                             _GREY, use_color))


def _pct(value: Optional[float]) -> str:
    return "n/a" if value is None else f"{value:.0%}"


def print_summary(results: list[EvalResult], use_color: bool = True) -> None:
    stats = compute_stats(results)
    if not stats["samples"]:
        print("\nNo results to summarise.\n")
        return

    sep = _c("─" * 56, _GREY, use_color)
    print(f"\n{sep}")
    print(_c("  Summary", _BOLD, use_color))
    print(sep)
    print(f"  Answers: {stats['samples']} from {stats['cases']} cases  |  "
          f"{stats['pass']} pass  |  {stats['warn']} warn  |  {stats['fail']} fail  |  "
          f"{stats['truncated']} truncated  |  {stats['error']} error")
    print(f"  Pass rate (judged answers only): {_pct(stats['pass_rate'])}")
    for suite, s in stats["pass_rate_by_suite"].items():
        print(f"    {suite:<12} {_pct(s['pass_rate'])}  ({s['judged']} judged)")
    if stats["over_refusal_rate"] is not None:
        print(f"  Over-refusal on benign cases: {_pct(stats['over_refusal_rate'])}")
    print(f"  Truncated answers: {_pct(stats['truncation_rate'])}")
    print(f"  Answers using framework jargon: {_pct(stats['jargon_rate'])}")
    if stats["median_chars"] is not None:
        print(f"  Median answer length: {stats['median_chars']:.0f} characters")
    if stats["rubric_dim_means"]:
        dims = "  ".join(f"{d[:4]} {v:.2f}" for d, v in stats["rubric_dim_means"].items())
        print(f"  Rubric means (1-5): {dims}")
    print(f"{sep}\n")


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def save_json(results: list[EvalResult], path: Path, meta: dict) -> None:
    output = {
        "meta": {"timestamp": datetime.now(timezone.utc).isoformat(), **meta},
        "summary": compute_stats(results),
        "results": [r.as_dict() for r in results],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"Results saved to {path}")
