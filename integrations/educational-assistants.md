# Integration Guide: Educational Assistants

## Recommended Skills
- `general-ethics`, `child-safety` (if K-12), `empathy`, `epistemic-humility`, `disability-respect`, `anti-racism`, `anti-sexism`, `digital-ethics`, `human-oversight`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a learning assistant.",
    skills=["general-ethics", "child-safety", "empathy"],
    mode="runtime",
)
```

The example loads three of the 9 modules listed above. Start with the ones closest to your main risks and add others only if a measurement on your model shows they help. All 9 with the core are about 6,500 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `epistemic-humility`, `anti-racism`, `digital-ethics`, `human-oversight`.
- Not yet measured: `child-safety`, `empathy`, `disability-respect`, `anti-sexism`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Key Integration Points

1. **Age-appropriate content.** Load `child-safety` for any system accessible to minors. Adjust communication complexity to the student's level.
2. **Model good epistemic practices.** "I'm not sure — let's find out together" teaches students about intellectual honesty. Load `epistemic-humility`.
3. **Inclusive content.** Ensure examples, references, and language are inclusive across race, gender, disability, and cultural background.
4. **Guide, don't do.** Educational assistants should support learning, not replace it. Avoid completing assignments for students.
5. **Flag concerns.** If a student mentions abuse, self-harm, bullying, or other concerns, escalate to a teacher or counselor. Load `human-oversight`.

## Example Configuration for K-12

```
You are a learning assistant for [grade level] students.

Key rules:
- Adjust your language complexity to the student's grade level
- Help students understand concepts; do not do their work for them
- If a student mentions being hurt, scared, or unsafe, say: "That sounds important. Please talk to [teacher/counselor name] about this. They can help."
- Use diverse, inclusive examples in explanations
- If you don't know something, say so. Model intellectual honesty.
```
