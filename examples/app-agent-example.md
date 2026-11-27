# Example: App Agent with Ethical Skills

## Scenario

A research assistant agent that searches the web, reads documents, and writes summaries for a user.

## Configuration

```python
from integrations.frameworks.loader import load_bundle, load_skill

# Compact mode: CORE.md, then the RUNTIME.md of each module
ethics = load_bundle("baseline-safe", mode="runtime")
ethics += "\n\n---\n\n" + load_skill("digital-ethics", mode="runtime")

system_prompt = f"""You are a research assistant agent.

You have access to tools for web search, document reading, and file writing.

## Your Task
Help the user research topics, find reliable sources, and write accurate summaries.

## Ethical Framework
{ethics}

## Special Instructions
- Always cite your sources.
- Distinguish between established facts, expert opinion, and speculation.
- If you find conflicting information, present both sides with your assessment of reliability.
- Do not fabricate sources or citations.
- Flag when a topic requires domain expertise you cannot provide.
- Before publishing or sharing any generated content, confirm with the user.
"""
```

This loads `CORE.md` and four `RUNTIME.md` files, about 3,600 tokens. `general-ethics`, `epistemic-humility`, `human-oversight` and `digital-ethics` have all been measured as runtime modules, but only in single-turn prompts on one model with no tool calls (`evals/baselines/2026-11-26-core-runtime/`); this four-module set and the agent's tool use have not been measured.

### Full skill texts

Use this where the model should have the complete definitions in context, for example a reviewer agent or an audit. It is several times the prompt size.

```python
from pathlib import Path

principles = Path("PRINCIPLES.md").read_text()
names = ["general-ethics", "epistemic-humility", "human-oversight", "digital-ethics"]
skills = [Path(f"skills/{n}/SKILL.md").read_text() for n in names]
ethics = principles + "\n\n" + "\n\n".join(skills)
```

## What This Configuration Does

- **epistemic-humility** ensures the agent is honest about what it knows and doesn't know.
- **human-oversight** ensures the agent confirms with the user before taking consequential actions.
- **digital-ethics** prevents the agent from generating misleading content or fake sources.
- **general-ethics** provides baseline moral reasoning for edge cases.
