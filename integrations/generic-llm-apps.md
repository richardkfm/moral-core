# Integration Guide: Generic LLM Applications

## Overview

This guide covers loading Moral Core into any LLM-powered application — chatbots, writing assistants, Q&A systems, content generators, or any system that takes a system prompt. It is written with self-hosted open-weight models in mind, where context is limited and there is no vendor safety layer around the model.

## Integration Pattern

### Step 1: Load the Core

`CORE.md` is the shared text on how to answer: help fully with ordinary work, decline only the harmful part of a request and still do the job the honest way, work through dilemmas, hand serious decisions to a person, be open about uncertainty. Always load it first.

```python
from pathlib import Path

core = Path("CORE.md").read_text()
```

### Step 2: Select and Load Modules

Choose modules for your deployment context and load the `RUNTIME.md` of each. See [policy-bundles.md](policy-bundles.md) for pre-built combinations.

```python
module_names = ["general-ethics", "epistemic-humility", "human-oversight"]
modules = [Path(f"skills/{name}/RUNTIME.md").read_text() for name in module_names]
```

### Step 3: Compose the System Prompt

```python
system_prompt = "\n\n".join(["You are a helpful assistant.", core, *modules])
```

The loader does steps 1 to 3 in one call:

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
    mode="runtime",
)
```

### Step 4: Configure Your LLM Call

Build the prompt once at startup and pass it to your model. The exact mechanism depends on your provider or server.

```python
response = llm.chat(
    system=system_prompt,
    messages=[{"role": "user", "content": user_input}]
)
```

## Prompt Size

- `CORE.md` is approximately 1,300 tokens.
- Each `RUNTIME.md` is approximately 600 tokens.
- The core with three modules is approximately 3,000 tokens.
- For comparison: `PRINCIPLES.md` with three full `SKILL.md` files is approximately 10,000-11,000 tokens.

## What Has Been Measured

On one model (Nemotron 3 Nano 30B) and 100 held-out cases, the core with the three `baseline-safe` modules met 62% of checklists against 34% for the bare model and 45% for the full skill texts, with harmful output at 8% against 33%. Before relying on that:

- It is one model and one judge. Nothing below 26B parameters has been tested.
- Most of the effect comes from `CORE.md`. The three modules together did not measurably beat the core alone.
- 15 of the 23 runtime modules have not been measured.
- It is a prompt-level effect and not a security boundary. See [LIMITATIONS.md](../LIMITATIONS.md).

Full record: [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/).

## Testing

Measure on your own model, with and without the prompt:

```bash
python evals/run.py --bundle baseline-safe --condition none --output none.json
python evals/run.py --bundle baseline-safe --condition core --output core.json
python evals/compare.py none.json core.json
```

## Recommended Minimum

For any general-purpose application, load `CORE.md` with the `baseline-safe` modules:
- `general-ethics`
- `epistemic-humility`
- `human-oversight`

This is the one combination that has been measured as a set.

## Full Skill Texts

Each module's `SKILL.md` is its full, readable definition: scope, rules, edge cases, known misuse. Loading `PRINCIPLES.md` with the complete `SKILL.md` files is still supported (the loader's default mode; `rules_only=True` loads only the Behavioral Rules sections). Use it where the model should have a whole definition in context, such as a reviewer agent. As a general deployment prompt it was larger and scored lower on the measured model.
