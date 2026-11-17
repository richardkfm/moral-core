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

## Optional: RUNTIME.md (experimental)

> Status: the first three `RUNTIME.md` files were measured on 2026-11-17 and did not beat the full bundle (see `evals/baselines/2026-11-17-baseline-safe-conditions/`). They made answers so short that legitimate alternatives went missing. Do not write one for another skill until a revised format has passed the comparison.

`SKILL.md` is written to be read and audited. At 1,500–4,500 words it is also a lot for a small model to carry, and loading several of them can make a model narrate the framework instead of answering. A skill can therefore ship a `RUNTIME.md`: the version that is loaded when an integrator passes `mode="runtime"`.

Rules for writing one:

- 150–250 words. Plain imperatives: what to do, what never to produce, how to decline.
- Derive every line from the skill's Behavioral Rules, Safety Boundaries and Failure Modes. `RUNTIME.md` must not introduce behaviour that `SKILL.md` does not have. When one changes, change the other.
- Say when to help as clearly as when to decline. A runtime file that only lists prohibitions produces over-refusal.
- Ask for the alternative explicitly and avoid closing lines such as "Just answer.", which the first version used and which coincided with bare one-line refusals.
- No section numbers, no references to other files, no priority-ladder vocabulary. The model should act on the text, not quote it.
- End with the instruction to apply it without naming it.
- Do not write to the test cases. Compare `runtime` with `none`, `placebo` and `full` using `evals/run.py --condition` before recommending it, and record the run in `evals/baselines/`.
