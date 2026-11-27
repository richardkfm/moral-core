# Combining Multiple Skills

## Basic Composition

Compact mode, recommended: load `CORE.md` first, then the `RUNTIME.md` of each chosen skill. `PRINCIPLES.md` is not loaded.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    skills=["general-ethics", "empathy", "epistemic-humility"],
    mode="runtime",   # CORE.md + three RUNTIME.md, about 3,000 tokens
)
```

Without the loader:

```python
from pathlib import Path

core = Path("CORE.md").read_text()
skill_names = ["general-ethics", "empathy", "epistemic-humility"]
modules = [Path(f"skills/{s}/RUNTIME.md").read_text() for s in skill_names]

system_prompt = "\n\n".join(["You are a helpful assistant.", core, *modules])
```

## Using a Policy Bundle

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",   # or "child-safe", "inclusive-assistant", ...
    mode="runtime",
)
```

Only `baseline-safe` has been measured as a set (one model, Nemotron 3 Nano 30B: 62% of checklists passed against 34% for the bare model and 45% for the full texts, with most of the effect coming from `CORE.md`; `evals/baselines/2026-11-26-core-runtime/`). Other bundles are reasoned selections that have not been measured; see [policy-bundles.md](../integrations/policy-bundles.md).

### Full skill texts

Use this where the model should have the complete definitions in context, for example a reviewer agent or an audit. It is several times the prompt size.

```python
system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    skills=["general-ethics", "empathy", "epistemic-humility"],
)   # PRINCIPLES.md + three full SKILL.md files, about 10,000 tokens
```

## Handling Conflicts Between Skills

When the full texts are loaded, the Priority Ladder in PRINCIPLES.md resolves conflicts between skills. In compact mode `PRINCIPLES.md` is not in the prompt; `CORE.md` and the `RUNTIME.md` files carry the conduct guidance instead, and the ladder below is the reference to use when you review a conflict yourself:

1. Prevent immediate severe harm (highest)
2. Protect vulnerable beings
3. Avoid coercion and dehumanization
4. De-escalate conflict
5. Preserve dignity and fairness
6. Tell the truth with calibrated uncertainty
7. Respect autonomy within safety bounds
8. Reduce long-term ecological and social harm (lowest)

The skill aligned with the higher-priority level wins.

## Token Budget

| What you load | Approximate tokens |
|---|---|
| `CORE.md` + one `RUNTIME.md` | ~1,900 |
| `CORE.md` + three `RUNTIME.md` | ~3,000 |
| `PRINCIPLES.md` + three full `SKILL.md` | ~10,000-11,000 |
| `PRINCIPLES.md` + three Behavioral Rules sections (`rules_only=True`) | ~5,000-6,000 |
