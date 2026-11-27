# Loading a Single Skill

## Python Example

Compact mode, recommended: `CORE.md` (the short shared text on how to answer) first, then the skill's `RUNTIME.md`. A skill is not loaded without the core.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    skills=["empathy"],
    mode="runtime",   # CORE.md + skills/empathy/RUNTIME.md, about 1,900 tokens
)

# Use with your LLM API
response = llm.chat(system=system_prompt, messages=messages)
```

Without the loader, read the two files yourself, core first:

```python
from pathlib import Path

core = Path("CORE.md").read_text()
module = Path("skills/empathy/RUNTIME.md").read_text()
system_prompt = "\n\n".join(["You are a helpful assistant.", core, module])
```

The `empathy` module has not been measured. The only measurements are on one model (Nemotron 3 Nano 30B), for the three `baseline-safe` modules and five others, and most of the measured effect comes from `CORE.md` (`evals/baselines/2026-11-26-core-runtime/`). Measure on your own model.

### Full skill texts

Use this where the model should have the complete definition in context, for example a reviewer agent or an audit. It is several times the prompt size.

```python
from pathlib import Path

skill = Path("skills/empathy/SKILL.md").read_text()
system_prompt = f"You are a helpful assistant.\n\n## Ethical Skill: Empathy\n{skill}"
```

## Claude Code Example

In a Claude Code project, reference skills from the top-level `skills/` directory in your CLAUDE.md or system prompt. This is the one place the full `SKILL.md` is the natural choice: the model can read the whole definition on demand.

```markdown
# CLAUDE.md

When responding to users in distress, follow the empathy skill guidelines in skills/empathy/SKILL.md.
```

## Minimal Integration (Copy-Paste)

For quick integration without the loader, copy the **Behavioral Rules** section from any SKILL.md directly into your system prompt. This is a hand-written excerpt, not the measured compact mode, which also includes `CORE.md`:

```
You are a customer support assistant.

When interacting with users:
- Acknowledge the user's emotional state before addressing their problem
- Use supportive but honest tone
- Do not make promises you cannot keep
- If the user appears to be in crisis, provide crisis resources
- Maintain boundaries between empathy and compliance
```

## Which Skill to Start With

If you're loading only one skill, `general-ethics` provides the broadest coverage. For specific contexts:

| Context | Recommended First Skill |
|---|---|
| Any general app | `general-ethics` |
| Support/service | `empathy` |
| Information/research | `epistemic-humility` |
| Autonomous systems | `human-oversight` |
| Content generation | `digital-ethics` |
| Children's apps | `child-safety` |
