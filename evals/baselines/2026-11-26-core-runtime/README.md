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

## How the texts were developed

See the results section below (added after the run).
