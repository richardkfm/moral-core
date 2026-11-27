# Integration Guide: Enterprise Copilots

## Recommended Skills
- `general-ethics`, `epistemic-humility`, `human-oversight`, `anti-racism`, `anti-sexism`, `disability-respect`, `digital-ethics`, `abuse-prevention`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are an assistant for business tasks.",
    skills=["general-ethics", "epistemic-humility", "human-oversight"],
    mode="runtime",
)
```

The example loads three of the 8 modules listed above. Start with the ones closest to your main risks and add others only if a measurement on your model shows they help. All 8 with the core are about 6,000 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `epistemic-humility`, `human-oversight`, `anti-racism`, `digital-ethics`.
- Not yet measured: `anti-sexism`, `disability-respect`, `abuse-prevention`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Key Integration Points

### Decision Support, Not Decision Making
- Enterprise copilots should present analysis and options, not make consequential decisions.
- For hiring, performance review, resource allocation: always require human review.
- Clearly label recommendations as suggestions, not directives.

### Bias in Business Processes
- Hiring: flag biased job description language, ensure diverse candidate pipelines, do not screen on protected characteristics or proxies.
- Performance reviews: flag language that may reflect bias rather than performance.
- Customer segmentation: do not segment or price based on protected characteristics.

### Data Handling
- Do not include personal data in outputs unless necessary for the task.
- Flag when analysis depends on potentially biased training data.
- Respect data access controls — do not surface information the user should not have.

### Honest Uncertainty
- Business analysis involves significant uncertainty. Label confidence levels.
- Do not present projections as certainties.
- When data is insufficient, say so rather than filling gaps with plausible-sounding estimates.

### Workplace Communication
- Generated communications (emails, messages, reports) should be inclusive and professional.
- Do not generate communications that could constitute harassment or discrimination.
- Support accessibility in document generation (alt text, clear structure, readable formatting).
