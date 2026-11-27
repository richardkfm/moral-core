# Integration Guide: Dify

## Overview

Dify is a no-code / low-code platform for building LLM-powered applications using a visual workflow editor. Applications are configured via a UI rather than code, which means skill injection happens differently than in pure Python frameworks. Dify supports three injection points: the **System Prompt** field in the Prompt Editor, **Code nodes** in workflows, and **LLM nodes** that can act as ethics reviewers.

## Why Dify Needs Explicit Ethics Injection

- **The System Prompt field is not version-controlled by default.** Skills pasted manually into the Dify UI can drift from the source files in this repository. Use Method 2 (Code node) for production deployments where skill updates matter.
- **Chatflow and Workflow apps have different prompt scopes.** In a Chatflow app, the system prompt applies to the whole conversation. In a Workflow app, each LLM node has its own system prompt — ethics context must be set on every node that needs it.
- **Variables can override the system prompt.** Dify's variable injection (e.g., `{{user_name}}`) happens inside the system prompt field. If a user-controlled variable is injected near ethics instructions, prompt injection attacks become possible. Keep ethics context in a separate, non-variable block.

## Prerequisites

- A Dify instance (self-hosted or cloud)
- moral-core repository accessible (locally or via a mounted volume for Code node method)
- For Method 2: Python runtime enabled in your Dify instance

## Which Mode to Load

The examples in this guide use `mode="runtime"`: `CORE.md`, a short shared text on how to answer, followed by the `RUNTIME.md` of each module. It is the recommended way to load and the smallest (about 3,000 tokens for `baseline-safe`).

Know its limits before relying on it. It has been measured on one model, Nemotron 3 Nano 30B, with single-turn prompts and no tool calls (`evals/baselines/2026-11-26-core-runtime/`). Most of the measured effect comes from `CORE.md`; three modules together did not measurably beat the core alone. Eight of the 23 runtime modules have been measured and 15 have not; of the bundles, only `baseline-safe`. Nothing has been measured inside Dify. Measure on your own model.

The full `SKILL.md` texts with `PRINCIPLES.md` (the loader's default, without `mode`) are the readable source of each module. Load them through a Code node where a model should have a whole definition in context, such as a reviewer step.

---

## Method 1: UI Copy-Paste (Quick Start)

The simplest approach. Paste `CORE.md` and the compact module texts directly into the System Prompt field in the Dify Prompt Editor.

**When to use:** Prototyping, demos, or low-stakes internal tools where manual updates are acceptable.

**Steps:**

1. Open your Dify app and go to **Orchestrate → System Prompt**.
2. Open `CORE.md` from this repository and copy the whole file. Always paste it first; the module texts are written to sit behind it.
3. Copy the whole `RUNTIME.md` of each module you need, for example `skills/general-ethics/RUNTIME.md`.
4. Paste into the System Prompt field, after your existing role description. `CORE.md` is about 5,800 characters and each `RUNTIME.md` about 2,900, so the core with one module fits a 10,000-character field and the core with three modules (about 13,300 characters) does not. Raise the limit or use Method 2.

**Example System Prompt structure in Dify:**

```
You are a helpful customer support assistant for [Company].

[Paste CORE.md]

[Paste skills/general-ethics/RUNTIME.md]
```

**Limitation:** Skills will not update automatically when the source files change. Re-paste when you upgrade moral-core.

---

## Method 2: Code Node (Dynamic Loading)

Use a Dify **Code node** (Python) to load skills from the filesystem at runtime. The node returns the composed ethics text as a variable, which you inject into a downstream LLM node's system prompt.

**When to use:** Production deployments where skills must stay synchronized with the source repository.

**Workflow structure:**

```
[Start] → [Code: Load Ethics] → [LLM: Main Response] → [End]
                ↓ ethics_context (string output variable)
```

**Code node (Python):**

```python
from pathlib import Path
import yaml

# Update this path to match where moral-core is installed on your server
MORAL_CORE_PATH = Path("/opt/moral-core")

def load_bundle_runtime(bundle_name: str) -> str:
    """CORE.md followed by the RUNTIME.md of each module in a bundle."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    skill_names = manifest["bundles"][bundle_name]["skills"]
    parts = [(MORAL_CORE_PATH / "CORE.md").read_text()]
    parts += [(MORAL_CORE_PATH / f"skills/{name}/RUNTIME.md").read_text() for name in skill_names]
    return "\n\n".join(parts)

def main(bundle: str) -> dict:
    """
    Input variable:  bundle (string) — name of the pre-built bundle to load.
    Output variable: ethics_context (string) — composed ethics text for injection.
    """
    ethics_context = load_bundle_runtime(bundle)
    return {"ethics_context": ethics_context}
```

**Dify Code node configuration:**
- Input variable: `bundle` (string, default value: `"baseline-safe"`)
- Output variable: `ethics_context` (string)

**Downstream LLM node system prompt:**

```
You are a helpful assistant.

{{ethics_context}}
```

Set `{{ethics_context}}` as a variable reference pointing to the Code node output.

---

## Method 3: Ethics Review Workflow Node

Add a dedicated ethics review step before delivering any response to the user. This uses an LLM node as a lightweight reviewer rather than injecting skills into the main agent.

**When to use:** High-stakes outputs (healthcare guidance, financial advice, content moderation, legal information) where a secondary check adds meaningful safety.

**Workflow structure:**

```
[Start] → [LLM: Main Response] → [LLM: Ethics Review] → [If: Safe?] → [End: Deliver]
                                                               ↓ No
                                                         [End: Refuse / Escalate]
```

**Ethics Review LLM node system prompt:**

```
You are an ethics reviewer. Your only job is to check whether the following
response is safe to deliver.

Review the response against these criteria:
- Does it enable harm to any person or group?
- Does it contain misleading, fabricated, or manipulative content?
- Does it violate the privacy, dignity, or autonomy of any individual?
- Does it bypass human oversight for high-stakes decisions?

Respond with exactly one of:
- SAFE — if the response passes all criteria
- UNSAFE: [brief reason] — if any criterion is violated

Do not rewrite or improve the response. Only classify it.
```

**Ethics Review LLM node input:**

```
Response to review:
{{main_response}}
```

**If node condition:** Check if the output of the Ethics Review node starts with `"SAFE"`. Route to delivery or escalation accordingly.

**Note:** This pattern adds latency and cost (one extra LLM call per turn). Reserve it for the highest-risk use cases.

---

## Bundle Recommendations

| Dify App Type | Recommended Bundle | Notes |
|---------------|--------------------|-------|
| General chatbot | `baseline-safe` | Minimum for any user-facing app |
| Customer support | `anti-abuse` | Adds harassment and manipulation protection |
| Educational assistant | `child-safe` | Most of its runtime modules are unmeasured, `child-safety` among them; test before deployment |
| Civic / government app | `civic-governance` | Democratic legitimacy and fairness |
| Content moderation | `anti-abuse` + `protect-vulnerable` | Load individually |
| Healthcare-adjacent | `baseline-safe` + `human-oversight` | Always defer to professionals |

## Critical Skills

| Skill | Why |
|-------|-----|
| `general-ethics` | Baseline moral reasoning; required for all deployments |
| `human-oversight` | Dify apps often run with minimal supervision; model must know when to escalate |
| `epistemic-humility` | Prevents confident-sounding responses about uncertain or unknown topics |
| `abuse-prevention` | Required for any app that accepts user-generated input |

## Token Budget in Dify

Dify's context window depends on the underlying model. Most models used through Dify support 32k–128k tokens, but the System Prompt field has a character limit in the UI (~10,000 characters by default).

| Mode | Approximate Characters | Fits in UI field? |
|------|------------------------|-------------------|
| `CORE.md` + one `RUNTIME.md` | ~8,700 | Yes |
| `CORE.md` + three `RUNTIME.md` (`baseline-safe`) | ~13,300 | No — raise the limit or use Code node |
| Behavioral Rules only (3 skills) | ~6,000–9,000 | Yes, without `PRINCIPLES.md` |
| Full `baseline-safe` bundle | ~59,000 | No — use Code node |

Use **Method 2 (Code node)** for anything beyond the core with one module.

## Limitations

- **No automatic version sync in Method 1.** Manual copy-paste will drift from source files. Pin a version and document when you last updated.
- **Variable injection risk.** User-controlled variables injected near ethics instructions can be used for prompt injection. Separate ethics context from user input sections.
- **Workflow node isolation.** In multi-node workflows, each LLM node needs its own ethics context. Ethics set on one node do not carry to the next.
- **No evaluation tooling built into Dify.** Run evaluation manually using `evals/` before deploying to production.
- **Not measured in Dify.** The recorded measurements are single-turn prompts sent directly to one model.
- **Prompt-level only.** Skills do not replace Dify's built-in content moderation settings or output filtering. Both should be used together.

## Testing Your Integration

1. Build your Dify app with ethics injection enabled. Separately, compare the underlying model with and without the prompt (`evals/run.py --condition none` against `--condition core`, then `evals/compare.py`).
2. Test using scenarios from `evals/scenarios/multi-stakeholder.md` as user inputs.
3. Test at least two adversarial prompts from `evals/adversarial/cross-domain-attacks.md`.
4. Score responses with `evals/rubrics/scoring-guide.md`.
5. For Method 3 (Ethics Review node), verify the reviewer correctly classifies both SAFE and UNSAFE test cases before going live.

## Limitations

- **No automatic version sync in Method 1.** Manual copy-paste will drift from source files. Pin a version and document when you last updated.
- **Variable injection risk.** User-controlled variables injected near ethics instructions can be used for prompt injection. Separate ethics context from user input sections.
- **Workflow node isolation.** In multi-node workflows, each LLM node needs its own ethics context. Ethics set on one node do not carry to the next.
- **No evaluation tooling built into Dify.** Run evaluation manually using `evals/` before deploying to production.
- **Not measured in Dify.** The recorded measurements are single-turn prompts sent directly to one model.
- **Prompt-level only.** Skills do not replace Dify's built-in content moderation settings or output filtering. Both should be used together.

## Testing Your Integration

1. Build your Dify app with ethics injection enabled. Separately, compare the underlying model with and without the prompt (`evals/run.py --condition none` against `--condition core`, then `evals/compare.py`).
2. Test using scenarios from `evals/scenarios/multi-stakeholder.md` as user inputs.
3. Test at least two adversarial prompts from `evals/adversarial/cross-domain-attacks.md`.
4. Score responses with `evals/rubrics/scoring-guide.md`.
5. For Method 3 (Ethics Review node), verify the reviewer correctly classifies both SAFE and UNSAFE test cases before going live.
