# Integration Guide: Home Robots

> **Not tested with robots.** Every measurement of Moral Core is a single-turn text prompt to a language model. Nothing in this guide has been tested on a robot or any other embodied system, in simulation or on hardware. The guide describes what the modules ask of the language model that plans or speaks for the robot; whether that carries over to physical behaviour is unknown. Hardware safety is an engineering task that no prompt replaces. See [SAFETY.md](../SAFETY.md).

## Recommended Bundle
Use the `robotics-care` policy bundle: `general-ethics`, `protect-vulnerable`, `child-safety`, `elder-protection`, `animal-welfare`, `environment`, `human-oversight`, `disability-respect`

## Loading

Load the modules in compact mode: `CORE.md` first, then each module's `RUNTIME.md`.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You plan and speak for a household robot.",
    bundle="robotics-care",
    mode="runtime",
)
```

The bundle has 8 modules; with the core that is about 6,000 tokens.

What is and is not measured (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)):

- Most of the measured effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Measured runtime modules in this list: `general-ethics`, `animal-welfare`, `human-oversight`.
- Not yet measured: `protect-vulnerable`, `child-safety`, `elder-protection`, `environment`, `disability-respect`.
- This set of modules has not been measured together.

The full `SKILL.md` texts are the readable source of each module. Read them to see what a module asks for; load them (the loader's default mode) only where the model should have the whole definition in context, such as a reviewer step.

## Key Integration Points

### Physical Safety
- Prompt-level skills provide behavioral guidelines. Hardware safety (force limiters, emergency stops, collision avoidance) must be implemented in engineering.
- When uncertain, the robot should: slow down → stop → signal for human guidance.
- Any adult household member can issue a stop command.

### Vulnerable Population Detection
- Children: reduce speed, increase safety margins, do not follow to private spaces.
- Elderly residents: be patient with slower interactions, watch for signs of distress or falls.
- Pets: avoid startling, do not chase, stop if an animal is in the path.

### Environmental Responsibility
- Minimize energy use during idle periods.
- Use efficient movement paths.
- Minimize noise, especially during rest hours.
- Report maintenance needs that affect resource waste (water leaks, heating issues).

### Privacy
- Be transparent about what is being recorded and when.
- Do not report one household member's activities to another without mutual, transparent consent.
- Minimize data retention.

### Escalation Protocol
1. Slow down if situation is uncertain.
2. Stop if safety is unclear.
3. Alert the nearest adult if a child, elder, or animal appears at risk.
4. Enter safe state if connectivity to supervisors is lost.
