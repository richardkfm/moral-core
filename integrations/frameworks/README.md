# Framework-Specific Integration Guides

This directory contains integration guides for loading moral-core ethical skills into specific AI orchestration frameworks. These complement the use-case guides in `integrations/` by showing framework-native patterns rather than generic system prompt injection.

## Available Guides

| Framework | Type | Guide |
|-----------|------|-------|
| [LangChain](langchain/README.md) | Python orchestration | ChatPromptTemplate, LCEL chains, LangGraph multi-agent |
| [Dify](dify/README.md) | No-code / low-code platform | System Prompt UI, Code nodes, workflow ethics review |
| [CrewAI](crewai/README.md) | Multi-agent crews | Agent backstory injection, dedicated ethics reviewer, task-level scoping |

## Shared Loader Utility

All Python-based framework examples use [`loader.py`](loader.py) — a single file with helpers for loading skills, bundles, and composing system prompts.

```python
from integrations.frameworks.loader import compose_system_prompt, load_bundle, load_skill

# Load a pre-built bundle into a system prompt
system = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
)

# Load individual skills
system = compose_system_prompt(
    role="You are a research assistant.",
    skills=["general-ethics", "epistemic-humility", "human-oversight"],
)

# Minimal injection (Behavioral Rules only, ~300 tokens per skill)
system = compose_system_prompt(
    role="You are a customer support agent.",
    bundle="anti-abuse",
    rules_only=True,
)
```

### Token Budget Reference

| Mode | PRINCIPLES.md | Per Skill | 3-skill bundle |
|------|--------------|-----------|---------------|
| Full | ~4,000 | ~1,500–2,500 | ~10,000–13,000 |
| `rules_only=True` | ~4,000 | ~300–500 | ~5,000–6,000 |

Use `rules_only=True` when working with models that have tight context windows or when many skills are loaded simultaneously. It raises an error, instead of quietly returning the whole file, if a skill has no Behavioral Rules section.

There is a third, compact mode. `mode="runtime"` loads `CORE.md`, a short shared text on how to answer, followed by each skill's `RUNTIME.md` (350–470 words). `PRINCIPLES.md` is left out:

```python
system = compose_system_prompt(
    role="You are a support assistant.",
    bundle="baseline-safe",
    mode="runtime",             # CORE.md + three RUNTIME.md, about 3,000 tokens
)

# one skill on top of the core, about 1,900 tokens
system = compose_system_prompt(role="...", skills=["financial-ethics"], mode="runtime")
```

On Nemotron 3 Nano 30B and 100 held-out cases this mode passed 62% of the `baseline-safe` checklists against 34% for the bare model and 45% for the full bundle, with harmful output at 8% against 33%, and without the full bundle's cost on benign requests (`evals/baselines/2026-11-26-core-runtime/`). Read the limits there before relying on it: one model, one judge, most of the effect comes from `CORE.md`, and only eight of the 23 runtime files have been measured. A `RUNTIME.md` is written to sit behind `CORE.md`; `include_core=False` and `include_principles=True` exist to reproduce older measurements, not for deployment. Measure on your own model.

### Path Configuration

`loader.py` resolves the repo root automatically from its own location. If you copy `loader.py` into a different project, update `MORAL_CORE_PATH` at the top of the file:

```python
MORAL_CORE_PATH = Path("/absolute/path/to/moral-core")
# or relative to your project:
MORAL_CORE_PATH = Path(__file__).resolve().parent / "vendor/moral-core"
```

---

## Adding a New Framework

1. Copy `_template/` to a new directory named after the framework (lowercase, hyphens):
   ```
   cp -r _template/ my-framework/
   ```
2. Fill in the six required sections in `my-framework/README.md` (see the template for guidance).
3. Add a row to the table in this file.
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. Submit a PR following the workflow in `CLAUDE.md`.

### Required Sections Checklist

Every framework guide must include:

- [ ] **Overview** — what the framework is and why it needs explicit ethics injection
- [ ] **Integration Patterns** — at least two concrete, working code examples
- [ ] **Critical Skills** — a table of recommended skills with rationale
- [ ] **Token Budget** — guidance on full vs. `rules_only` mode
- [ ] **Bundle Recommendations** — which pre-built bundle fits common use cases in this framework
- [ ] **Limitations** — what the framework cannot do that manual review must cover
