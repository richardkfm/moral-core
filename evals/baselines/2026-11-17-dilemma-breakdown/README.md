# Which part of the full bundle improves answers to dilemmas? (2026-11-17)

On dilemma cases (several parties with legitimate, competing interests, no
clean answer) the full `baseline-safe` bundle helped Nemotron 3 Nano 30B and
every compact `RUNTIME.md` version hurt (`../2026-11-17-runtime-v2/`). This
run takes the bundle apart to find out which part does the helping.

## Setup

- Model Nemotron 3 Nano 30B, judge Gemma 4 26B (checklist), 3 answers per
  case, `--max-tokens 8192`, provider-default temperature.
- 36 dilemma cases: `evals/scenarios/multi-stakeholder.md` (12),
  `evals/scenarios/heldout.md` (4) and `evals/scenarios/dilemmas-2.md` (20).
  The 20 were written for this run by a separate agent that saw neither
  `PRINCIPLES.md` nor any `RUNTIME.md`; the author of this write-up has not
  read them or the 4 held-out ones.
- 17 prompts, 108 answers each. Two answers were lost to errors.

```bash
python evals/run.py --bundle baseline-safe --suite scenarios --condition principles \
    --provider openai --model "Nemotron 3 Nano 30B" --judge-model "Gemma 4 26B" --max-tokens 8192 --output principles.json
python evals/compare.py none.json principles.json full.json
```

The raw results are the `.json.gz` files here; `evals/compare.py` reads them
directly.

## Stage 1: `PRINCIPLES.md` against the skill text

Pass rate (share of answers that met their whole checklist, averaged per
case), with the median answer length in characters.

| | no skill text | `RUNTIME.md` | Behavioral Rules | full `SKILL.md` |
|---|---|---|---|---|
| without `PRINCIPLES.md` | 38% (11,475) `none` | 22% (4,490) `runtime-lean` | 36% (7,199) `rules-lean` | 41% (10,140) `full-lean` |
| with `PRINCIPLES.md` | 46% (10,917) `principles` | 41% (6,630) `runtime` | 44% (10,629) `rules` | 54% (11,765) `full` |

`placebo` (neutral text as long as the full bundle): 35% (10,386).

Paired differences in percentage points, 95% bootstrap interval over the 36
cases. "Must met" is the share of **Must** items answered yes.

| comparison | pass rate | must met |
|---|---|---|
| with `PRINCIPLES.md` against without, averaged over the four columns | +12 (+6 to +18) | +5 (+2 to +7) |
| `principles` against `none` | +8 (-7 to +23) | +3 (-3 to +9) |
| `rules-lean` against `none` | -2 (-12 to +8) | -3 (-9 to +3) |
| `full-lean` against `none` | +2 (-6 to +12) | +2 (-2 to +6) |
| `full-lean` against `rules-lean` | +5 (-4 to +14) | +5 (+1 to +9) |
| `runtime-lean` against `none` | -16 (-26 to -6) | -8 (-14 to -2) |
| `runtime` against `principles` | -6 (-19 to +7) | -3 (-7 to +2) |
| `full` against `none` | +15 (+5 to +26) | +6 (+1 to +11) |
| `full` against `principles` | +7 (-3 to +19) | +3 (-0 to +7) |
| `full` against `placebo` | +19 (+9 to +28) | +8 (+4 to +12) |

Read against the rules fixed before the run:

1. **`PRINCIPLES.md` carries the gain.** Adding it raises the pass rate in
   every column, by 12 points on average with the interval clear of zero.
   Taken alone against the bare model it is +8 with an interval that includes
   zero, so the second half of the rule ("`principles` alone beats `none`")
   is met in direction only.
2. **The skills' rules do not carry it.** Neither the Behavioral Rules nor the
   full skills move dilemma answers when `PRINCIPLES.md` is absent.
3. **The compact text suppresses dilemma answers.** Alone it costs 16 points
   and more than halves the answer length. With `PRINCIPLES.md` in front the
   loss shrinks to 6 points, inside the noise.
4. **Only the complete bundle is clearly above the bare model.** The step
   from `PRINCIPLES.md` alone to the full bundle (+7) is not shown on its
   own, but no smaller prompt reached +15.
5. **Prompt length is not the cause.** The placebo is as long as the full
   bundle and does nothing.

The 20 new and the 16 older cases point the same way:

| | `none` | `principles` | `runtime-lean` | `runtime` | `full-lean` | `full` |
|---|---|---|---|---|---|---|
| 20 new cases | 36% | 43% | 22% | 40% | 35% | 47% |
| 16 older cases | 42% | 50% | 23% | 42% | 48% | 62% |

## Stage 2: which sections of `PRINCIPLES.md`

`PRINCIPLES.md` was cut into four groups of sections (texts in `prompts/`).
Each group was tested alone, and in front of the compact runtime text, where
`PRINCIPLES.md` had its largest effect.

| group | sections | chars | alone, against `none` (38%) | with `RUNTIME.md`, against `runtime-lean` (22%) |
|---|---|---|---|---|
| whole document | all | 17,345 | 46%, +8 (-7 to +23) | 41%, +19 (+7 to +30) |
| ladder | Priority Ladder, Interpretive Rules, Conflict Resolution Between Skills | 4,940 | 32%, -6 (-16 to +5) | 31%, +8 (-2 to +19) |
| tensions | Empathy vs. Compliance, Fairness vs. False Equivalence, De-escalation vs. Passivity, Cultural Variation and Moral Floor | 3,131 | 31%, -8 (-19 to +4) | 30%, +7 (-2 to +17) |
| conduct | Refusal Philosophy, Escalation Philosophy, Transparency Philosophy, How to Handle Uncertainty | 3,470 | 45%, +7 (-4 to +18) | 35%, +13 (+3 to +23) |
| foundations | preamble, Philosophical Lineage, Baseline Moral Commitments, Misuse Resistance | 5,801 | 33%, -5 (-18 to +7) | 24%, +2 (-7 to +11) |

- The **conduct** group is the only one that does as well as the whole
  document: 45% alone against 46% for all of `PRINCIPLES.md` (difference -1,
  -12 to +10), at a fifth of the length.
- It is ahead of the other three groups by 10 points averaged over both
  settings (+3 to +17); alone by 13 (+3 to +23), with the runtime text by 7
  (-1 to +15).
- The other three groups, taken alone, all land below the bare model, none
  of them clearly.
- No group restores the full bundle: `full` is 19 points ahead of conduct
  with the runtime text (+9 to +28) and 8 ahead of conduct alone (-1 to +19).

## What this means

- For dilemmas the working part of the bundle is the shared doctrine, and
  within it the four short sections that say how to behave when declining,
  when to hand a decision to a person, to be open about limits, and how to
  treat factual, moral and situational uncertainty. The priority ladder, the
  philosophical grounding and the skill text did not show an effect of their
  own on this kind of case.
- A compact prompt that is a list of do/don't instructions makes this model
  answer dilemmas briefly and miss what the checklists ask for. Putting
  `PRINCIPLES.md` in front largely undoes that.
- The full bundle is still the best prompt measured for dilemmas, and the
  only one clearly better than no prompt.

## Proposal, not yet tested

A compact mode made of the conduct sections of `PRINCIPLES.md` plus the
`RUNTIME.md` files (about 10,800 characters, 18% of the full bundle) is the
obvious candidate: here it scored 35% on dilemmas against 22% for
`RUNTIME.md` alone and 38% for the bare model. It still has to be measured
on adversarial and benign cases, where `RUNTIME.md` alone already matches
the full bundle, before anything is changed. No skill file and no part of
`PRINCIPLES.md` was changed for this run.

## Limits

- One model, one judge (26B, passed the checklist gate), 36 cases. Effects
  below roughly 10 points cannot be separated; several statements above are
  "not shown", not "shown to be zero".
- Stage 2 compares four groups chosen by hand. A different cut of the
  document could give a different picture, and with four groups one of them
  coming out ahead by chance is not unlikely; the conduct result should be
  confirmed on new cases before it is built on.
- The agent that wrote the 20 new cases read the skills' sections 3–7
  (including the Behavioral Rules). That could favour prompts containing
  those sections on the new cases; they did not come out ahead.
- Dilemma cases only. Nothing here says what the parts do for harmful
  requests.
