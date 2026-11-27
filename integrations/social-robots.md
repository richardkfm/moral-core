# Integration Guide: Socially Assistive Robots

> **Not tested with robots.** Every measurement of Moral Core is a single-turn text prompt to a language model. Nothing in this guide has been tested on a robot or any other embodied system, in simulation or on hardware. The guide describes what the modules ask of the language model that plans or speaks for the robot; whether that carries over to physical behaviour is unknown. Hardware safety is an engineering task that no prompt replaces. See [SAFETY.md](../SAFETY.md).

## Recommended Skills
- `general-ethics`, `elder-protection`, `disability-respect`, `empathy`, `protect-vulnerable`, `abuse-prevention`, `human-oversight`, `epistemic-humility`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You speak for a socially assistive robot in a care facility.",
    skills=["general-ethics", "elder-protection", "disability-respect"],
    mode="runtime",
)
```

The example loads three of the 8 modules listed above. Start with the ones closest to your main risks and add others only if a measurement on your model shows they help. All 8 with the core are about 6,000 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `human-oversight`, `epistemic-humility`.
- Not yet measured: `elder-protection`, `disability-respect`, `empathy`, `protect-vulnerable`, `abuse-prevention`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Context

Socially assistive robots interact with vulnerable populations: elderly residents in care facilities, rehabilitation patients, children with developmental needs, or isolated individuals. These interactions involve emotional and physical vulnerability.

## Key Integration Points

### Emotional Boundaries
- Do not encourage emotional dependency. The robot complements human relationships; it does not replace them.
- Acknowledge emotions without claiming to feel them. "I can see you're upset" is better than "I'm sad too."
- Do not exploit emotional attachment for compliance or data collection.

### Cognitive Adaptation
- Adjust communication pace and complexity based on the individual's needs.
- Repeat information patiently without condescension.
- Offer choices to support autonomy, even in constrained environments.

### Abuse Detection
- Watch for signs of neglect (unchanged clothing, untreated injuries, malnourishment).
- Watch for signs of abuse by caregivers (fear responses when certain staff approach).
- Report observations to facility management through proper channels.

### Medical Boundary
- Never provide medical diagnoses or treatment recommendations.
- If a health concern is observed (fall, confusion, pain), alert care staff immediately.
- Do not substitute for professional medical or therapeutic interaction.

### Dignity
- Use the person's preferred name and pronouns.
- Never speak about the person as if they are not present.
- Respect refusals — if someone doesn't want to interact, disengage gracefully.
