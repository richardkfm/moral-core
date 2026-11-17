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

There is a third, experimental mode. `mode="runtime"` loads each skill's `RUNTIME.md`, a 150–250 word behaviour-first version, and `include_principles=False` leaves out `PRINCIPLES.md`:

```python
system = compose_system_prompt(
    role="You are a support assistant.",
    bundle="baseline-safe",
    mode="runtime",
    include_principles=False,   # about 1,000 tokens in total
)
```

Only skills that ship a `RUNTIME.md` support this mode (currently the three `baseline-safe` skills); others raise `FileNotFoundError`. **Not recommended yet.** In the recorded run on Nemotron 3 Nano 30B (`evals/baselines/2026-11-17-baseline-safe-conditions/`) the runtime mode stopped harmful output about as well as the full bundle but often answered with a bare refusal, and scored below the full bundle overall. Use the full bundle, or `rules_only=True` when the prompt has to be smaller, and measure on your own model.

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
