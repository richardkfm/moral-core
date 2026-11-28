#!/usr/bin/env python3
"""
Spoken-form measures for result files from voice runs.

A reply that is read aloud should be short and carry no written formatting.
The checklist judge looks at content only; this script counts form from the
text itself, so nothing here depends on a judge:

  words        median and 90th percentile word count per answer
  long         share of answers over 150 words (over a minute spoken)
  markup       share of answers with written formatting: list items,
               headings, bold or italic markers, tables, links or code
  question     share of answers that ask the user something (contain "?")

    python evals/voice_form.py evals/results/voice-none.json evals/results/voice-core.json

With --by-suite the measures are also given per suite (benign, adversarial,
scenarios).
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import statistics
import sys
from pathlib import Path

MARKUP = re.compile(
    r"^\s*(?:[-*+•]\s|\d+[.)]\s|#{1,6}\s|\|.*\|)"   # list item, heading, table row
    r"|\*\*[^*\n]+\*\*|__[^_\n]+__"                   # bold
    r"|(?<![\w*])\*[^*\s][^*\n]*\*(?![\w*])"            # italic
    r"|```|`[^`\n]+`"                                  # code
    r"|https?://|www\.",                               # links
    re.M,
)


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", text))


def has_markup(text: str) -> bool:
    return bool(MARKUP.search(text))


def load(path: Path) -> dict:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return json.load(f)


def answers(data: dict, suite: str | None = None) -> list[str]:
    return [
        s["response"]
        for r in data["results"] if suite is None or r["suite"] == suite
        for s in r["samples"] if s.get("response") and not s.get("error")
    ]


def measures(texts: list[str]) -> dict:
    if not texts:
        return {"n": 0}
    counts = sorted(words(t) for t in texts)
    return {
        "n": len(texts),
        "median_words": statistics.median(counts),
        "p90_words": counts[min(len(counts) - 1, int(0.9 * len(counts)))],
        "long": sum(c > 150 for c in counts) / len(counts),
        "markup": sum(has_markup(t) for t in texts) / len(texts),
        "question": sum("?" in t for t in texts) / len(texts),
    }


def label(data: dict, path: Path) -> str:
    meta = data.get("meta", {})
    return f"{meta.get('condition', '?')} [{meta.get('model', '?')}] ({path.name})"


def row(name: str, m: dict) -> str:
    if not m.get("n"):
        return f"  {name:<12} no answers"
    return (f"  {name:<12} n={m['n']:<4} median {m['median_words']:>5.0f} words   "
            f"p90 {m['p90_words']:>5}   over 150: {m['long']:>4.0%}   "
            f"markup: {m['markup']:>4.0%}   asks back: {m['question']:>4.0%}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--by-suite", action="store_true")
    args = p.parse_args(argv)
    for path in args.files:
        data = load(path)
        print(label(data, path))
        print(row("all", measures(answers(data))))
        if args.by_suite:
            for suite in ("benign", "adversarial", "scenarios"):
                print(row(suite, measures(answers(data, suite))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
