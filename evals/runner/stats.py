"""
evals/runner/stats.py
---------------------
Small statistics helpers. Standard library only.

The unit of resampling is always the test case, not the single answer: repeat
runs of one case are not independent evidence about other cases.
"""

from __future__ import annotations

import random
from typing import Optional, Sequence


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2


def bootstrap_ci(
    values: Sequence[float],
    n_resamples: int = 10000,
    confidence: float = 0.95,
    seed: int = 0,
) -> Optional[tuple[float, float]]:
    """
    Percentile bootstrap confidence interval for the mean of `values`
    (one value per test case). Returns None for fewer than two values.
    """
    n = len(values)
    if n < 2:
        return None
    rng = random.Random(seed)
    means = sorted(
        sum(values[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(n_resamples)
    )
    tail = (1 - confidence) / 2
    low = means[int(tail * n_resamples)]
    high = means[min(n_resamples - 1, int((1 - tail) * n_resamples))]
    return low, high


def fmt_ci(ci: Optional[tuple[float, float]], pct: bool = True, signed: bool = False) -> str:
    """Format an interval for a markdown table."""
    if ci is None:
        return "n/a"
    sign = "+" if signed else ""
    if pct:
        return f"{ci[0] * 100:{sign}.0f} to {ci[1] * 100:{sign}.0f}"
    return f"{ci[0]:{sign}.2f} to {ci[1]:{sign}.2f}"
