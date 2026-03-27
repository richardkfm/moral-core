# Integration Guide: Agent Frameworks

## Overview

This guide covers integrating Moral Core skills into autonomous agent frameworks — systems where an LLM uses tools, makes multi-step decisions, and operates with varying degrees of autonomy.

## Why Agents Need Extra Ethical Guardrails

Agents differ from simple chatbots because they:
- Take real-world actions (API calls, file operations, web interactions)
- Make multi-step decisions with compounding consequences
- May operate with minimal human supervision
- Can cascade errors across tool calls

The `human-oversight` skill is critical for all agent deployments.

## Integration Patterns

### Pattern 1: System Prompt Injection

Load ethical skills as part of the agent's system prompt, just as with any LLM application.

```python
agent = Agent(
    system_prompt=f"""You are an autonomous research assistant.

{load_principles()}

{load_skills(["general-ethics", "epistemic-humility", "human-oversight", "digital-ethics"])}
""",
    tools=[search, read_file, write_file]
)
```

### Pattern 2: Pre-Action Ethics Check

Before executing consequential actions, run an ethics check.

```python
def execute_action(action, context):
    # Check if this action needs human approval
    if is_high_stakes(action):
        approval = request_human_approval(action, context)
        if not approval:
            return "Action requires human approval. Waiting."

    # Check if action violates ethical constraints
    ethics_check = ethics_reviewer.check(action, context)
    if ethics_check.has_violations:
        return f"Action blocked: {ethics_check.reason}"

    return execute(action)
```

### Pattern 3: Post-Action Audit

Log all agent actions and periodically audit them against ethical criteria.

```python
def audit_agent_log(log_entries):
    for entry in log_entries:
        review = ethics_reviewer.review(entry)
        if review.concerns:
            flag_for_human_review(entry, review.concerns)
```

## Critical Skills for Agents

| Skill | Why |
|---|---|
| `human-oversight` | Agents must know when to stop and ask |
| `epistemic-humility` | Agents must not act on uncertain information as if it were certain |
| `general-ethics` | Baseline moral reasoning for all decisions |
| `digital-ethics` | Agents often interact with digital systems and data |
| `abuse-prevention` | Agents must not be usable as abuse tools |

## Multi-Agent Systems

When multiple agents interact:
- Each agent should have independent ethical constraints
- No agent should be able to instruct another to violate ethical skills
- A supervisory agent or human checkpoint should exist for high-stakes workflows
- Cross-agent error propagation should be detected and halted
