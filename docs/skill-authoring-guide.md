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
