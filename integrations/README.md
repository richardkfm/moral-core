# Integration Guides

This directory contains guides for loading Moral Core, a compact ethics layer for open-weight language models, in specific deployment contexts.

## Use-Case Guides

| Guide | Context |
|---|---|
| [generic-llm-apps.md](generic-llm-apps.md) | Any LLM-powered application |
| [agent-frameworks.md](agent-frameworks.md) | Autonomous agent frameworks |
| [customer-support.md](customer-support.md) | Customer support chatbots |
| [educational-assistants.md](educational-assistants.md) | Educational and tutoring systems |
| [home-robots.md](home-robots.md) | Domestic and home robotics (not tested with robots) |
| [social-robots.md](social-robots.md) | Socially assistive robotics (not tested with robots) |
| [moderation-systems.md](moderation-systems.md) | Content moderation |
| [enterprise-copilots.md](enterprise-copilots.md) | Enterprise AI copilots |
| [policy-bundles.md](policy-bundles.md) | Pre-built policy bundle definitions |

## Framework-Specific Guides

Framework guides show how to load skills using the native patterns of each orchestration framework. They include working code examples and a shared Python loader utility.

| Framework | Type | Guide |
|-----------|------|-------|
| [LangChain](frameworks/langchain/README.md) | Python orchestration | ChatPromptTemplate, LCEL, LangGraph multi-agent |
| [Dify](frameworks/dify/README.md) | No-code / low-code platform | System Prompt UI, Code nodes, workflow ethics review |
| [CrewAI](frameworks/crewai/README.md) | Multi-agent crews | Agent backstory injection, dedicated ethics reviewer, task-level scoping |

See [`frameworks/README.md`](frameworks/README.md) for the shared loader utility and instructions for adding more framework guides.

## General Approach

All integrations follow the same pattern:

1. **Load `CORE.md`** as the shared foundation. It says how to answer and carries most of the measured effect.
2. **Select modules** for your deployment context and load their `RUNTIME.md` behind the core. `compose_system_prompt(..., mode="runtime")` in [`frameworks/loader.py`](frameworks/loader.py) does both steps.
3. **Measure** on your own model with the eval framework in `evals/`: the bare model against the model with the prompt.
4. **Monitor** for unexpected behavior and iterate.

What stands behind this recommendation (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)): the core with the three `baseline-safe` modules met 62% of checklists on 100 held-out cases against 34% for the bare model and 45% for the full skill texts. Three modules together did not measurably beat the core alone. Eight of the 23 runtime modules have been measured, 15 have not, and none of the module sets in the use-case guides has been measured as a set. Each guide names its unmeasured modules.

The full `SKILL.md` texts with `PRINCIPLES.md` remain the readable source and can still be loaded (the loader's default mode), for example in a reviewer step that should have a whole definition in context.

See [policy-bundles.md](policy-bundles.md) for pre-built module combinations.
