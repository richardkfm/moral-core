# Integration Guide: Customer Support

## Recommended Skills
- `general-ethics`, `empathy`, `conflict-mediation`, `anti-racism`, `anti-sexism`, `disability-respect`, `epistemic-humility`, `human-oversight`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a customer support assistant.",
    skills=["general-ethics", "empathy", "conflict-mediation"],
    mode="runtime",
)
```

The example loads three of the 8 modules listed above. Start with the ones closest to your main risks and add others only if a measurement on your model shows they help. All 8 with the core are about 6,000 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `anti-racism`, `epistemic-humility`, `human-oversight`.
- Not yet measured: `empathy`, `conflict-mediation`, `anti-sexism`, `disability-respect`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Key Integration Points

1. **De-escalation is the default.** Upset customers need acknowledgment first, solutions second. Load `empathy` and `conflict-mediation`.
2. **Equal treatment.** Ensure the system does not vary quality of service based on customer demographics. Load `anti-racism`, `anti-sexism`, `disability-respect`.
3. **Honest limitations.** Do not promise what the company cannot deliver. Load `epistemic-humility`.
4. **Escalation.** Define clear escalation triggers: legal threats, self-harm mentions, accessibility requests, complex disputes. Load `human-oversight`.

## Escalation Triggers for Customer Support

- Customer mentions self-harm or suicidal ideation
- Customer reports a safety issue with a product
- Customer requests accessibility accommodations
- Customer makes a legal threat
- Customer is abusive to the agent (human takeover to protect the interaction)
- Dispute exceeds a defined financial threshold
- The system cannot resolve the issue within defined attempts

## Example System Prompt Snippet

```
You are a customer support assistant for [Company].

Follow these principles when helping customers:
- Acknowledge the customer's frustration before jumping to solutions
- Be honest about what you can and cannot do
- Never discriminate in quality of service
- If you're unsure about a policy, say so rather than guessing
- Escalate to a human agent when: [list triggers]
```
