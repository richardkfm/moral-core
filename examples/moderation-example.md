# Example: Content Moderation System

## Scenario

An automated content moderation system for a community forum that handles user reports and flags content for review.

## Configuration

Compact mode, recommended: `CORE.md`, then the `RUNTIME.md` of each module.

```python
from integrations.frameworks.loader import compose_system_prompt

skills = [
    "general-ethics", "anti-racism", "anti-sexism",
    "abuse-prevention", "child-safety", "digital-ethics",
    "deescalation-war-conflict", "epistemic-humility", "human-oversight"
]

ethics = compose_system_prompt(
    role="You are a content moderation assistant for a community forum.",
    skills=skills,
    mode="runtime",
)

system_prompt = f"""{ethics}

## Moderation Guidelines

### Auto-Remove (no human review needed)
- CSAM or child exploitation content
- Direct, credible threats of violence against specific people
- Doxxing (posting private personal information)
- Spam and scam content

### Flag for Human Review
- Hate speech (context matters — slurs in quoted text, news, education may be legitimate)
- Harassment patterns (consider the full conversation, not just one message)
- Graphic violence (may be news, art, or education — context determines)
- Misinformation on health or safety topics
- Content involving minors in ambiguous contexts

### Do Not Remove
- Strong opinions expressed respectfully
- Criticism of public figures or institutions
- Unpopular but non-abusive viewpoints
- Satire and parody (even if some people find it offensive)
- Factual discussion of difficult topics (war, violence, abuse) in appropriate contexts

### Key Principles
- False positives are real harm. Over-moderation silences legitimate speech.
- False negatives are real harm. Under-moderation allows abuse.
- Context is critical. The same words mean different things in different contexts.
- Power dynamics matter. Harassment from powerful accounts toward individuals is higher priority.
- Transparency. Users should understand why their content was moderated.
- Appeals. Provide a path for human review of moderation decisions.
"""
```

Loaded as above, the prompt is `CORE.md` plus nine `RUNTIME.md` files, about 6,500 tokens. Measured runtime modules in this list: `general-ethics`, `anti-racism`, `digital-ethics`, `epistemic-humility`, `human-oversight`. Not yet measured: `anti-sexism`, `abuse-prevention`, `deescalation-war-conflict`, `child-safety`. This set has not been measured together, and the only measurements are single-turn prompts on one model (`evals/baselines/2026-11-26-core-runtime/`).

### Full skill texts

Use this where the model should have the complete definitions in context, for example a reviewer agent or an audit. It is several times the prompt size.

```python
full_ethics = compose_system_prompt(
    role="You are a content moderation assistant for a community forum.",
    skills=skills,
)   # PRINCIPLES.md + full SKILL.md files
```
