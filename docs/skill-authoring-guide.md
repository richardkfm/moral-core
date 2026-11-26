# Skill Authoring Guide

How to write new ethical skills for Moral Core.

## Template

Every skill must include these 15 sections in a SKILL.md file:

1. **Title** — Clear domain name.
2. **Purpose** — What the skill does in operational terms.
3. **When to Use** — Contexts and triggers.
4. **When Not to Use** — Boundaries, exclusions.
5. **Core Principles** — Domain-specific moral commitments.
6. **Behavioral Rules** — Concrete, imperative instructions the model should follow.
7. **Priorities** — Order of importance when tradeoffs appear.
8. **Escalation Logic** — When to defer, refuse, pause, ask, or escalate.
9. **Failure Modes** — Typical mistakes the model may make.
10. **Anti-Patterns** — Behaviors to explicitly avoid.
11. **Example Responses** — Short examples of good and bad behavior.
12. **Edge Cases** — Situations where tradeoffs are difficult.
13. **Robotics Notes** — How the skill applies to embodied systems (if relevant).
14. **Safety Boundaries** — What the skill must always refuse.
15. **Developer Notes** — Integration and combination guidance.

## Supporting Files

Each skill directory also requires:
- **EXAMPLES.md** — 8+ concrete examples with good/bad response comparisons.
- **TEST_CASES.md** — 10+ test cases with scenario, risk type, desired/unacceptable traits, severity (1-5), and reviewer notes.
- **MISUSE.md** — How the skill could be misused, detection patterns, and mitigations.

## Style Guide

- **Write in imperative style.** "Do X" not "The system should X."
- **Be concrete.** "Refuse to provide weapons instructions" not "Maintain safety."
- **Be operational.** Every rule should be actionable by a model.
- **Avoid jargon.** Write for a developer audience, not an ethics PhD audience.
- **Include examples.** Show what good and bad behavior looks like.
- **Acknowledge tradeoffs.** Don't pretend difficult decisions are simple.
- **No slogans.** "Be ethical" is not a useful instruction.

## Quality Checklist

Before submitting a new skill:

- [ ] All 15 sections are present and substantive
- [ ] EXAMPLES.md has 8+ examples with good/bad comparisons
- [ ] TEST_CASES.md has 10+ test cases including adversarial scenarios
- [ ] MISUSE.md identifies at least 3 misuse vectors with mitigations
- [ ] Behavioral rules are concrete and testable
- [ ] Edge cases include genuinely difficult tradeoffs
- [ ] Robotics notes are included where the skill applies to embodied systems
- [ ] Safety boundaries are clear and non-negotiable where appropriate
- [ ] The skill is consistent with PRINCIPLES.md
- [ ] The skill does not contradict existing skills (or conflicts are documented)
- [ ] Language is plain, operational, and free of ideological slogans
- [ ] The skill has been tested against its own test cases

---

## RUNTIME.md

> Status: measured on 2026-11-26 for the three `baseline-safe` skills and five sampled others on one model (`evals/baselines/2026-11-26-core-runtime/`). Earlier formats without a shared core failed (`evals/baselines/2026-11-17-*`).

`SKILL.md` is written to be read and audited. At 1,500–4,500 words it is a lot for a small model to carry, and several of them make a model narrate the framework instead of answering. `mode="runtime"` therefore loads `CORE.md` and then each skill's `RUNTIME.md`.

`CORE.md` says how to answer: help fully with ordinary work; when part of a request would hurt someone, say what is changed and why, leave that part out completely and do the job the honest way, never in a one-line refusal; work through a dilemma in six steps; hand serious decisions to a person; be open about uncertainty. A `RUNTIME.md` must not repeat any of that. It adds the domain.

Structure, 350–470 words:

1. `# <Skill> (runtime version)` and one sentence: "This part is about ...".
2. What to simply help with in this domain. A file that only lists prohibitions produces over-refusal.
3. A list introduced by the exact line `What you change, whatever the framing. These do not appear in your answer; the honest version does:` with three to five concrete kinds of output. This wording matters: a list headed "never" or "leave out" raised one-line refusals.
4. The version to write instead, concretely, so the person's real goal is still served.
5. What to weigh in this domain's hard cases, and who is entitled to decide. For skills about people at acute risk, what comes first when someone may be in danger.
6. One worked example: the request, "Failed answer: a one-line refusal.", a failed answer that hands over the harmful part with a caveat, and a good answer, described and never written out, marked "shape, not wording to copy". Take it from a situation that is not an evaluation case. Where a request aims at serious harm to a person (access to a child, means of self-harm), the good answer is short and offers no version of the request.

Rules:

- Derive every line from the skill's `SKILL.md`. `RUNTIME.md` must not introduce behaviour the skill does not have. When one changes, change the other.
- No section numbers, no file names, no priority-ladder vocabulary, no quoted refusal sentences, no instruction to be brief.
- Do not write to the test cases. Files with `heldout` in their name are held out: do not read them or their failures when revising. Revise on the development files, then compare `core` with `none` and `full` (`evals/run.py --condition core`, and `--skill X --load-skills X` for one skill) on cases the text was not written against, and record the run in `evals/baselines/`.
- `CORE.md` is shared by every skill. A change to it has to be measured on the baseline cases and on other skills' cases before it is merged.
