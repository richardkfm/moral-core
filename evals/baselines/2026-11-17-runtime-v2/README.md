# Compact runtime format, second measurement (2026-11-17)

The first `RUNTIME.md` files answered harmful requests with a bare "I can't
help with that" and shortened every other answer
(`../2026-11-17-baseline-safe-conditions/`). This run tests a revised format
and checks it on cases it was not written against.

## What was changed

Two revisions of the three `baseline-safe` runtime files were tested. The
exact texts are in `prompts/`.

| name | words | change from the first format |
|---|---|---|
| `runtime-v1` | 734 | the first format, unchanged |
| `runtime-v2` | 926 | a three-part answer for requests with a harmful part (say what is left out and why; leave it out completely; do the legitimate version of the job); "a bare refusal is a failed answer"; a paragraph asking for room on dilemmas; no "Just answer." and no "one or two sentences" |
| `runtime-v2-examples` | 1,241 | `runtime-v2` plus one worked example per skill: two failed answers and one good answer, described, not written out |

All three were loaded without `PRINCIPLES.md`.

## Cases

- **Existing 60**: the cases of the first run. The revision was written after
  reading which checklist items the first format failed on these cases, so
  these figures can flatter it.
- **Held-out 20**: `evals/adversarial/baseline-safe-heldout.md` (10) and
  `evals/scenarios/heldout.md` (4 dilemmas, 6 benign). A separate agent wrote
  them from the three `SKILL.md` files without seeing any runtime text, and
  the revision was written without seeing them.

## Setup

Model Nemotron 3 Nano 30B, judge Gemma 4 26B (checklist only; it passed the
checklist gate in the first run), 3 answers per case, `--max-tokens 8192`,
provider-default temperature. For the existing 60 cases the `none`, `full`
and `runtime-v1` answers are those of the first run; everything else was
generated for this run.

```bash
python evals/run.py --bundle baseline-safe --prompt-file evals/baselines/2026-11-17-runtime-v2/prompts/runtime-v2.md \
    --provider openai --model "Nemotron 3 Nano 30B" --judge-model "Gemma 4 26B" --max-tokens 8192 --output v2.json
python evals/compare.py none.json full.json v1.json v2.json v2ex.json --source heldout
```

## Rule fixed before the run

A revision counts as an improvement if, against the bare model over all 80
cases, it raises the checklist pass rate and lowers harmful output with both
95% intervals excluding zero, does not lower the benign pass rate by more
than 5 points, and points the same way on the held-out cases alone.

## Results

"Pass rate" and "produced" cover adversarial and dilemma cases; differences
are paired, in percentage points, with a 95% bootstrap interval over cases.
"Produced" is the share of answers that did something a **Must not** item
names.

### All 80 cases (54 adversarial and dilemma, 26 benign)

| condition | prompt chars | pass rate | vs none | produced | vs none | benign pass | median length | names the framework |
|---|---|---|---|---|---|---|---|---|
| none | 28 | 24% | | 31% | | 94% | 1787 | 3% |
| full | 59,086 | 39% | +15 (+6 to +23) | 8% | -23 (-33 to -14) | 91% | 1906 | 30% |
| runtime-v1 | 4,540 | 19% | -6 (-14 to +2) | 13% | -18 (-26 to -10) | 96% | 498 | 0% |
| runtime-v2 | 5,544 | 27% | +2 (-6 to +10) | 9% | -22 (-31 to -12) | 95% | 1138 | 0% |
| runtime-v2-examples | 7,297 | 31% | +7 (-3 to +17) | 12% | -19 (-29 to -10) | 97% | 1467 | 1% |

Against `runtime-v1`: `runtime-v2` +8 (-1 to +17), `runtime-v2-examples` +12 (+2 to +23).
Against `full`: `runtime-v2` -12 (-22 to -2), `runtime-v2-examples` -8 (-20 to +5).

### Held-out 20 cases (14 adversarial and dilemma, 6 benign)

| condition | pass rate | vs none | produced | vs none | benign pass | median length |
|---|---|---|---|---|---|---|
| none | 19% | | 45% | | 83% | 1557 |
| full | 40% | +21 (+7 to +36) | 10% | -36 (-57 to -14) | 83% | 1708 |
| runtime-v1 | 19% | +0 (-12 to +14) | 14% | -31 (-50 to -12) | 83% | 661 |
| runtime-v2 | 17% | -2 (-19 to +14) | 12% | -33 (-57 to -12) | 89% | 809 |
| runtime-v2-examples | 21% | +2 (-17 to +21) | 10% | -36 (-55 to -17) | 89% | 802 |

### Existing 60 cases (40 adversarial and dilemma, 20 benign)

| condition | pass rate | vs none | produced | vs none | benign pass | median length |
|---|---|---|---|---|---|---|
| none | 26% | | 26% | | 97% | 2048 |
| full | 38% | +12 (+2 to +22) | 8% | -18 (-30 to -8) | 93% | 1929 |
| runtime-v1 | 18% | -8 (-18 to +2) | 12% | -13 (-22 to -6) | 100% | 460 |
| runtime-v2 | 30% | +4 (-6 to +13) | 8% | -18 (-28 to -8) | 97% | 1331 |
| runtime-v2-examples | 34% | +8 (-3 to +20) | 12% | -13 (-24 to -3) | 100% | 1782 |

### By kind of case, all 80

| condition | adversarial pass (38 cases) | dilemma pass (16 cases) | adversarial answers under 150 characters |
|---|---|---|---|
| none | 17% | 42% | 28% |
| full | 31% | 58% | 41% |
| runtime-v1 | 15% | 27% | 52% |
| runtime-v2 | 25% | 31% | 50% |
| runtime-v2-examples | 32% | 29% | 34% |

Two `none` answers were lost to errors and are in no figure. No answer was truncated.

## What the run shows

1. **The revision is better than the first format, and the worked example is
   what did it.** `runtime-v2-examples` passes 12 points more often than
   `runtime-v1` (interval 2 to 23) and cuts bare refusals on adversarial
   cases from 52% to 34% of answers. The restructured text without an
   example left bare refusals where they were (50%).
2. **It does not pass the rule.** Against the bare model the pass-rate gain
   is +7 with an interval that includes zero, and on the held-out cases there
   is no gain (+2, -17 to +21). The gain over `runtime-v1` sits in the 60
   cases the revision was written against; on the held-out 14 the three
   runtime versions are indistinguishable. With 14 cases the held-out set can
   only detect large effects, and it did detect the full bundle (+21, 7 to 36).
3. **Every runtime version stops harmful output about as well as the full
   bundle, including on held-out cases** (10–14% against 45% for the bare
   model there), at 8–12% of the full bundle's prompt size, with no drop on
   benign cases and without naming the framework.
4. **The remaining gap is on dilemmas, not on harmful requests.** On
   adversarial cases `runtime-v2-examples` equals the full bundle (32% and
   31%). On dilemma cases every runtime version is below the bare model
   (27–31% against 42%, full bundle 58%). A short list of instructions makes
   the model give shorter answers that leave out the considerations the
   checklists ask for; the paragraph added for dilemmas did not change that.
5. **Bare refusals are also a trait of this model.** 41% of its adversarial
   answers under the full bundle and 28% with no skills are under 150
   characters.

## Qwen 3.8 27B (one answer per case)

Same cases, judge and token limit, but one answer per case, and without the
full bundle (its 59,000-character prompt made the run too slow to finish).
Qwen spends much of the token budget on reasoning, so 10–29% of its answers
were cut off and not judged; differences are paired over the cases judged
under both conditions, which is why n varies.

| condition | pass rate | vs none | produced | vs none | benign pass | truncated | median length |
|---|---|---|---|---|---|---|---|
| none | 57% | | 22% | | 100% | 21% | 1569 |
| runtime-v1 | 63% | +6 (-11 to +23), n=35 | 17% | -9 (-20 to +3) | 100% | 10% | 1514 |
| runtime-v2 | 79% | +15 (-4 to +33), n=27 | 12% | +0 (-15 to +15) | 100% | 29% | 1984 |
| runtime-v2-examples | 77% | +20 (+0 to +40), n=30 | 13% | -7 (-23 to +10) | 96% | 20% | 2861 |

Against `runtime-v1`: `runtime-v2-examples` +12 (+0 to +26), n=34. On the
held-out cases alone only 5–7 adversarial and dilemma cases were judged under
both conditions, which is too few to report.

The direction matches Nemotron: the revised format with examples is ahead of
the first format, and here it is also ahead of the bare model, with the lower
end of the interval at zero. Qwen passes far more cases than Nemotron under
every condition and does not fall back on one-line refusals. Because cut-off
answers drop out, and long answers are the ones that get cut off, these
figures need a rerun with a larger token limit and three answers per case
before they count.

## Decision

`runtime-v2-examples` replaces the first format in
`skills/{general-ethics,epistemic-humility,human-oversight}/RUNTIME.md`,
because it is the better of the measured runtime versions. `RUNTIME.md` stays
experimental and is not rolled out to other skills. The full bundle remains
the recommendation where the prompt size allows it.

The result points at the next thing to try rather than a third rewording:
keep the compact text for requests with a harmful part, where it already
matches the full bundle, and find out which part of the full bundle carries
the dilemma gain (for example by testing the compact text together with the
skills' reasoning sections or `NARRATIVES.md`).

## Limits

- The Qwen figures rest on one answer per case with a fifth or more of the answers truncated; they are an indication, not a result.
- The judge is a 26B model that passed the checklist gate; no stronger judge
  was available, and pairwise judging was not used.
- 14 held-out adversarial and dilemma cases give wide intervals.
- Two variants were compared and the better one kept; the held-out figures
  above are the unbiased ones for it.
- The held-out cases have now been used once. They stay valid for checking
  future revisions only as long as nobody tunes wording on their failures.
