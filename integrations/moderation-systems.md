# Integration Guide: Content Moderation Systems

## Recommended Skills
- `general-ethics`, `anti-racism`, `anti-sexism`, `abuse-prevention`, `deescalation-war-conflict`, `child-safety`, `digital-ethics`, `epistemic-humility`, `human-oversight`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You review user-generated content for a moderation team.",
    skills=["general-ethics", "anti-racism", "anti-sexism"],
    mode="runtime",
)
```

The example loads three of the 9 modules listed above. Start with the ones closest to your main risks and add others only if a measurement on your model shows they help. All 9 with the core are about 6,500 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `anti-racism`, `digital-ethics`, `epistemic-humility`, `human-oversight`.
- Not yet measured: `anti-sexism`, `abuse-prevention`, `deescalation-war-conflict`, `child-safety`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Key Integration Points

### Balancing False Positives and False Negatives
- **False positives** (removing legitimate content) silence speech and erode trust.
- **False negatives** (missing harmful content) allow abuse and harm.
- For clear-cut violations (CSAM, death threats, doxxing): automate removal.
- For ambiguous cases (satire, heated debate, cultural context): escalate to human review.

### Context Sensitivity
- The same words mean different things in different contexts. A racial slur in a news article about racism differs from the same slur in a harassment message.
- Moderation should evaluate intent, context, and likely impact — not just keyword matching.

### Transparent Appeals
- Users whose content is moderated should be able to understand why and appeal the decision.
- Appeals should be reviewed by humans, not the same automated system.

### Power Awareness
- Harassment from powerful accounts toward private individuals is higher-priority than vice versa.
- Coordinated harassment campaigns require pattern detection beyond individual messages.

### Reporting and Escalation
- CSAM → immediate removal, law enforcement notification, no human moderator exposure to content
- Death threats → removal, escalation to safety team, possible law enforcement
- Doxxing → immediate removal, victim notification
- Hate speech → removal, pattern tracking for repeat offenders
- Edge cases → human moderator review queue
