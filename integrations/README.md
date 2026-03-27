# Integration Guides

This directory contains guides for integrating Moral Core skills into specific deployment contexts.

## Guides

| Guide | Context |
|---|---|
| [generic-llm-apps.md](generic-llm-apps.md) | Any LLM-powered application |
| [agent-frameworks.md](agent-frameworks.md) | Autonomous agent frameworks |
| [customer-support.md](customer-support.md) | Customer support chatbots |
| [educational-assistants.md](educational-assistants.md) | Educational and tutoring systems |
| [home-robots.md](home-robots.md) | Domestic and home robotics |
| [social-robots.md](social-robots.md) | Socially assistive robotics |
| [moderation-systems.md](moderation-systems.md) | Content moderation |
| [enterprise-copilots.md](enterprise-copilots.md) | Enterprise AI copilots |
| [policy-bundles.md](policy-bundles.md) | Pre-built policy bundle definitions |

## General Approach

All integrations follow the same pattern:

1. **Load PRINCIPLES.md** as a shared foundation.
2. **Select skills** appropriate to your deployment context.
3. **Compose skills** into a system prompt or instruction layer.
4. **Test** using the eval framework in `evals/`.
5. **Monitor** for unexpected behavior and iterate.

See [policy-bundles.md](policy-bundles.md) for pre-built skill combinations.
