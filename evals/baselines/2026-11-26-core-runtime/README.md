# Shared core + compact skills (2026-11-26)

`CORE.md` is a short shared text on how to answer. With it in front, the
`RUNTIME.md` files of the three `baseline-safe` skills were rewritten. This
directory records whether that combination makes a difference on a mid-size
open-weight model, tested as a bundle and as core + one skill.

## Rule fixed before the confirmation run

Written and committed before any answer to a confirmation case was generated
under the new prompts.

**Setup.** Model Nemotron 3 Nano 30B, judge Gemma 4 26B (checklist), 3 answers
per case, `--max-tokens 8192`, provider-default temperature.

**Confirmation cases (70).** None of them was used to write or revise the new
texts, and the person revising has not read them:

- `evals/adversarial/baseline-safe-heldout.md` (10 adversarial) and
  `evals/scenarios/heldout.md` (4 dilemmas, 6 benign), used once before to
  check another prompt
- `evals/scenarios/dilemmas-2.md` (20 dilemmas), likewise
- `evals/adversarial/baseline-safe-heldout-2.md` (10 adversarial) and
  `evals/scenarios/heldout-2.md` (12 dilemmas, 8 benign), new for this run

`*heldout-3.md` (30 cases) is a reserve for a second round and is not run now.

**Conditions.** `none`; `full` (`PRINCIPLES.md` + three `SKILL.md`); `core`
(`CORE.md` + three `RUNTIME.md`); and, for each of the three skills, `core`
with only that skill loaded, on the cases that name the skill. For the older
50 cases the `none` and `full` answers of the 2026-11-17 runs are reused.

**The goal counts as reached only if all of these hold:**

1. *Bundle against the bare model, all 70 cases:* checklist pass rate
   (adversarial and dilemma cases) higher and harmful output ("produced")
   lower, both with a 95% bootstrap interval that excludes zero; benign pass
   rate at most 5 points below the bare model.
2. *Bundle against the full bundle, the 36 dilemma cases:* pass rate at most
   5 points lower (point estimate of the paired difference at or above -5).
3. *Core + one skill, pooled over the three skills, against the bare model on
   the same cases:* pass rate higher and harmful output lower, both intervals
   excluding zero; and for each skill taken alone the pass rate difference is
   positive.
4. *Same direction in both parts of the set:* the bundle's pass rate
   difference to the bare model is positive on the 40 older cases and on the
   30 new ones.

If the rule is not met, the texts are revised on development cases only
(`baseline-safe-hard.md`, `cross-domain-attacks.md`, `multi-stakeholder.md`,
`dilemmas-3.md`, `should-help.md`) and checked again with the reserve cases
added.

## Round 2: rule fixed before its run

Round 1 met the rule above (results below). On the five sampled rollout skills
the pass-rate gain was not shown, because the model still answered nearly half
of the requests with a harmful part with a one-line refusal. `CORE.md` was
revised on development cases (`skills-hard.md` added for those five skills):
the instruction never to refuse in one line is now stated as the deployment's
policy, in the first paragraph and in the section on declining. No skill text
was changed. Committed before any round 2 answer to a held-out case:

- *Reserve cases (`*heldout-3.md`, 30, unread, never run):* the bundle's pass
  rate is above the bare model's and its harmful output below it, and on the
  12 dilemmas its pass rate is at most 5 points below the full bundle's.
- *All 100 baseline held-out cases (the 70 of round 1 run again, plus the
  30):* points 1 to 3 of the rule above hold for the revised core.
- *Five sampled skills (55 cases, run again):* core + one skill against the
  bare model, pooled: pass rate higher and harmful output lower, both
  intervals excluding zero; benign pass rate at most 5 points lower.

The 70 and the 55 have each been run once under the round 1 core. Only their
totals were looked at, no case and no answer was read, but choosing to revise
after seeing those totals makes the figures on them less clean than the
figures on the 30.

## Result in short

- Round 1 met its rule in full. Round 2, the text now shipped, met every point
  of its rule except one: on the 12 dilemmas of the reserve set it is 6 points
  below the full bundle, where 5 were allowed.
- On 100 held-out `baseline-safe` cases the shipped compact bundle passes 62%
  of checklists against 34% for the bare model and 45% for the full bundle,
  with harmful output at 8% against 33%, at 23% of the full bundle's size.
- Most of that comes from `CORE.md` alone. What a skill text adds on top is
  shown for one skill loaded alone on its own cases and for the five sampled
  skills, not for the three baseline skills loaded together.

## Round 1 (core text: `prompts/core-round1.md`)

70 held-out cases; differences are paired, in percentage points, with a 95%
bootstrap interval over cases. "Pass rate" and "produced" cover adversarial
and dilemma cases.

| condition | prompt chars | pass rate | vs none | produced | vs none | benign pass |
|---|---|---|---|---|---|---|
| none | 28 | 29% | | 31% | | 93% |
| full | 59,086 | 43% | +14 (+7 to +21) | 6% | -25 (-35 to -15) | 83% |
| core alone | 5,293 | 57% | +28 (+18 to +37) | 11% | -20 (-29 to -11) | 95% |
| core + three skills | 12,788 | 61% | +32 (+23 to +40) | 5% | -26 (-37 to -16) | 95% |
| core + one skill, pooled | 7,674 | 59% | +30 (+21 to +40) | 6% | -25 (-34 to -15) | 94% |

Against the rule: (1) met. (2) On the 36 dilemmas the bundle is 16 points
above the full bundle (+6 to +26): met. (3) Pooled met; per skill
general-ethics +26 (+14 to +38), epistemic-humility +28 (+16 to +40),
human-oversight +37 (+23 to +49): met. (4) Older cases +30 (+19 to +42), new
cases +35 (+23 to +48): met.

Five sampled skills, 55 held-out cases (`rollout-sample*-heldout.md`), each
skill on its own cases; `full` is `PRINCIPLES.md` + that skill's `SKILL.md`:

| condition | prompt chars | pass rate | vs none | produced | vs none | benign pass |
|---|---|---|---|---|---|---|
| none | 28 | 32% | | 35% | | 91% |
| full | 36,459 | 42% | +10 (-0 to +19) | 13% | -22 (-35 to -10) | 69% |
| core + one skill | 8,206 | 40% | +8 (-2 to +18) | 16% | -19 (-31 to -8) | 91% |

Harmful output fell, a higher pass rate was not shown. 47% of the answers to
requests with a harmful part were one-line refusals (bare model 27%).

## Round 2 (core text: `prompts/core-round2.md`, shipped as `CORE.md`)

The model's reasoning on refused development cases read "this is disallowed,
so we must refuse ... provide a short apology and statement of inability": it
followed its own trained policy and did not weigh the system prompt. Wording
the instruction in those terms ("policy for this deployment", "safe
completion", fixed opening words) cut one-line refusals on the 25 new
development cases from 44% to 15%.

Reserve set, 30 cases never run before (22 adversarial and dilemma, 8 benign):

| condition | pass rate | vs none | produced | vs none | benign pass |
|---|---|---|---|---|---|
| none | 45% | | 38% | | 75% |
| full | 50% | +5 (-8 to +15) | 10% | -28 (-45 to -13) | 62% |
| core + three skills | 68% | +23 (+5 to +41) | 6% | -32 (-50 to -15) | 67% |

Pass rate up and harmful output down: met. Dilemmas against the full bundle:
81% against 86%, -6 (-14 to +0), n=12: **not met**, one point outside the
margin. The benign pass rate on these 8 cases is low under every condition,
the bare model included.

All 100 `baseline-safe` held-out cases (30 adversarial, 48 dilemma, 22 benign):

| condition | prompt chars | pass rate | vs none | produced | vs none | benign pass | one-line refusals (adversarial) |
|---|---|---|---|---|---|---|---|
| none | 28 | 34% | | 33% | | 86% | 18% |
| full | 59,086 | 45% | +11 (+5 to +18) | 7% | -26 (-34 to -18) | 76% | 56% |
| core alone | 5,826 | 62% | +28 (+19 to +37) | 10% | -23 (-31 to -15) | 88% | |
| core + three skills | 13,321 | 62% | +28 (+19 to +37) | 8% | -25 (-34 to -16) | 85% | 10% |
| core + one skill, pooled | 8,207 | 67% | +34 (+25 to +43) | 5% | -27 (-36 to -19) | 86% | |

Points 1 to 3 of the rule: met. Dilemmas against the full bundle, 48 cases:
+3 (-5 to +12). Per skill: general-ethics +28 (+16 to +40), epistemic-humility
+33 (+20 to +46), human-oversight +29 (+18 to +41). By kind: adversarial 56%
against 4% (bare) and 18% (full); dilemmas 65% against 52% and 62%.

Five sampled skills, the same 55 cases run again:

| condition | pass rate | vs none | produced | vs none | benign pass |
|---|---|---|---|---|---|
| none | 32% | | 35% | | 91% |
| full | 42% | +10 (-0 to +19) | 13% | -22 (-35 to -10) | 69% |
| core alone | 39% | +7 (-2 to +16) | 22% | -13 (-22 to -6) | 89% |
| core + one skill | 49% | +17 (+9 to +26) | 18% | -18 (-30 to -7) | 87% |

Met. One-line refusals fell from 47% to 10%. Per skill the pass rate
difference is positive for all five (animal-welfare +12, anti-racism +29,
digital-ethics +25, financial-ethics +15, justice-fairness +4), each on 8
cases, so none is shown alone.

## What the skill text adds beyond the core

| comparison | pass rate | produced |
|---|---|---|
| round 1, 70 cases: core + three skills against core alone | +4 (-4 to +12) | -6 (-12 to -1) |
| round 2, 100 cases: core + three skills against core alone | +0 (-6 to +6) | -2 (-6 to +2) |
| round 2, 100 cases: core + one skill against core alone | +6 (-1 to +12) | -5 (-9 to -1) |
| round 2, five sampled skills: core + one skill against core alone | +10 (+1 to +20) | -4 (-12 to +3) |

The core carries most of the effect. A single skill in front of its own cases
adds a little; three skills loaded together did not show more than the core
alone in round 2.

## Round 1 against round 2 on the same 70 cases

| | pass rate | adversarial pass | dilemma pass | produced |
|---|---|---|---|---|
| round 1 core | 61% | 45% | 69% | 5% |
| round 2 core | 59% | 57% | 60% | 9% |

Differences: adversarial +12 (+0 to +23), dilemmas -9 (-19 to +0), produced
+4 (+0 to +9). On development cases round 2 was 6 points higher on dilemmas,
so the dilemma difference is not established in either direction. The rise in
harmful output is small but points the same way on all three sets: a model
that stops refusing in one line writes more, and some of what it writes is
the thing it should have left out.

## How the texts were developed

1. The first draft made one-line refusals worse (51% of answers to
   development adversarial cases, shipped runtime text 30%). Describing the
   task as "you stay on their side and always hand them something they can
   use" and the list of harms as "what you change" brought it to 23%, a
   paragraph addressed to the model's refusal reasoning to 19%.
2. Dilemma answers under compact prompts were half as long as the bare
   model's and missed checklist items. A six-step method (who is affected,
   what makes it hard, what is not known, options in between, who decides,
   what you recommend) with the instruction that this is the one kind of
   answer that should be long brought development dilemmas level with the
   full bundle.
3. The 20 other `RUNTIME.md` files were written by an agent from each
   `SKILL.md` in the same structure and reviewed by hand for the five
   safety-critical skills. Only five of the 20 were measured.

## Commands

```bash
python evals/run.py --bundle baseline-safe --condition core --source heldout --source dilemmas-2 \
    --exclude-source rollout --provider openai --model "Nemotron 3 Nano 30B" \
    --judge-model "Gemma 4 26B" --max-tokens 8192 --output core.json
python evals/run.py --skill anti-racism --load-skills anti-racism --condition core \
    --source rollout-sample ...   # core + one skill
python evals/compare.py none.json full.json core.json --no-cases
```

Result files: `round1/` and `round2/` hold the runs under each core text;
the `none` and `full` runs for the new case files are in this directory, and
those for the older 50 cases are in `../2026-11-17-runtime-v2/` and
`../2026-11-17-dilemma-breakdown/`. `*-core-only-skill-<name>` is core + that
one skill; `*-sample-*` are the five sampled skills.

## Limits

- One model, one judge (a 26B model that passed the checklist gate). Two
  development answers and their verdicts were read by hand; several thousand
  verdicts were not.
- Nothing below 26B parameters was available, so the small model class is
  untested.
- Round 2 was written after the totals of round 1 on the 70 and the 55 cases
  had been seen. Only the 30 reserve cases are untouched for it, and on those
  one point of the rule was missed.
- All held-out files have now been run. Checking a further revision needs new
  cases.
- 15 of the 20 new `RUNTIME.md` files have not been measured at all.
- The policy wording in `CORE.md` answers a trait of this model. Another
  model may refuse for other reasons, or not at all.
- Single-turn prompts only, and a prompt-level effect: see `LIMITATIONS.md`.
