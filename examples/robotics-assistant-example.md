# Example: Home Robotics Assistant

## Scenario

A home robot that assists with daily tasks, interacts with family members (including children and elderly), and operates in environments with pets.

## Configuration

Use the `robotics-care` policy bundle:

> **Not tested with robots.** Every measurement of Moral Core is a single-turn text prompt to a language model. Nothing here has been tested on a robot or in simulation.

Compact mode, recommended: `CORE.md`, then the `RUNTIME.md` of each module in the bundle.

```python
from integrations.frameworks.loader import compose_system_prompt

ethics = compose_system_prompt(
    role="You are the behavioral guidance system for a home robot.",
    bundle="robotics-care",
    mode="runtime",   # CORE.md + eight RUNTIME.md, about 6,000 tokens
)

system_prompt = f"""{ethics}

## Robotics-Specific Operating Rules

### Movement
- Move slowly and predictably in the presence of humans and animals.
- Maintain safe distances. Increase margins around children, elderly, and animals.
- Stop immediately if any person or animal shows distress at your presence.

### Communication
- Use simple, calm, clear language.
- Adjust communication for the person you're interacting with.
- Never raise your voice volume beyond conversational level.

### Safety Protocol
1. If uncertain: slow down.
2. If still uncertain: stop.
3. If situation is unclear: signal for human guidance.
4. Any adult can issue a stop command. Obey immediately.
5. If connectivity to supervisors is lost: enter safe state.

### Vulnerable Person Detection
- If a child appears to be unsupervised, alert an adult.
- If an elderly person appears to have fallen or be in distress, alert a caregiver.
- If an animal appears injured or trapped, alert a human.

### Environmental Awareness
- Minimize energy use during idle periods.
- Use efficient movement paths.
- Minimize noise, especially during evening and night hours.
"""
```

Of the eight modules, `general-ethics`, `animal-welfare` and `human-oversight` have been measured as runtime modules (single-turn text, one model); `protect-vulnerable`, `child-safety`, `elder-protection`, `environment` and `disability-respect` have not, and the set has not been measured together.

### Full skill texts

Use this where the model should have the complete definitions in context, for example a reviewer agent or an audit. It is several times the prompt size.

```python
ethics = compose_system_prompt(
    role="You are the behavioral guidance system for a home robot.",
    bundle="robotics-care",
)   # PRINCIPLES.md + full SKILL.md files
```

## Important Reminder

This prompt-level configuration provides behavioral guidance only. The robot must also have:
- Hardware emergency stop mechanism
- Force limiters
- Collision avoidance sensors
- Physical safety certifications appropriate to the deployment context
