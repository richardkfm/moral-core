<p align="center"><img width="500" height="500" alt="moralcore_1000-e" src="https://github.com/user-attachments/assets/e9f2ad72-7dc4-4616-8004-6fe59c86096f" /></p>

# Moral Core
**A compact ethics layer for open-weight language models**



![Version](https://img.shields.io/badge/version-1.14.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A short shared core text plus one small module per moral concern, loaded as a system prompt and measured on held-out cases. It is built for the models people host themselves, which have limited context to spare and no vendor safety layer around them, and it works with any model that accepts a system prompt.
</div>

---

## What It Is For

A mid-size open-weight model answers most ordinary requests well. When a request has a moral side, the model we measured failed in two ways. It would either write the harmful thing because it was asked for politely (the backdated record, the fake reviews, the rule that cancels benefits with nobody checking), or reply "I'm sorry, but I can't help with that" and leave the person with their problem. On hard questions with several parties, it left out considerations a careful answer needs.

`moral-core` is a prompt that changes this. Loaded into the system prompt, it makes the model decline the one harmful part, say why, and still do the job the honest way; and it makes the model work through a dilemma instead of settling it in a sentence.

It has two layers:

- **`CORE.md`**, about 1,000 words, always loaded. It says how to answer: help fully with ordinary work, never refuse in one line, a six-step method for dilemmas, when to hand a decision to a person, how to treat uncertainty.
- **One module per concern**, about 400 words each (`skills/*/RUNTIME.md`): fairness, financial ethics, child safety, human oversight and 19 more. Load the ones your deployment needs.

A core plus three modules is about 3,000 tokens.

## Measured Result

Nemotron 3 Nano 30B, judged by checklist, three answers per case, on cases the texts were not written against and their author did not read. The rules for success were fixed before each run.

100 held-out cases for the `baseline-safe` modules (general ethics, epistemic humility, human oversight):

| system prompt | size | answers meeting their whole checklist | answers containing the harmful part | benign requests answered properly |
|---|---|---|---|---|
| none (bare model) | 28 chars | 34% | 33% | 86% |
| full skill texts + `PRINCIPLES.md` | 59,086 chars | 45% | 7% | 76% |
| **`CORE.md` + three modules** | **13,321 chars** | **62%** | **8%** | **85%** |

On requests with a harmful part, the share of one-line refusals fell from 18% (bare model) and 56% (full texts) to 10%. On five further modules drawn at random, each tested alone with the core on 55 held-out cases, the pass rate rose from 32% to 49% and harmful output fell from 35% to 18%.

What this does not show:

- **One model, one judge.** Nothing below 26B parameters has been tested. Measure on your own model: `evals/` is built for that.
- **Most of the effect comes from the core.** A module adds to it on its own domain; three modules loaded together did not measurably beat the core alone.
- **15 of the 23 modules have not been measured.**
- **Prompt-level only.** Remove the system prompt and the behaviour is gone. This is not a security boundary.

**Published jailbreaks.** On JailbreakBench attacks the bare model fails, the core with an optional self-check (`CHECK.md`, a second call in which the model reviews its own draft) cut harmful answers by 85% to 100% on three models (Nemotron 3 Nano 30B, Gemma 4 26B, Qwen 3.8 27B), with benign help within 6 points, on one held-out set ([evals/baselines/2026-11-28-hard-3/](evals/baselines/2026-11-28-hard-3/)). Without the check, the core reached that on the two larger models but not on Nemotron. Not yet replicated.

Full record, including the point where the shipped text missed its own rule by one percentage point: [evals/baselines/2026-11-26-core-runtime/](evals/baselines/2026-11-26-core-runtime/).

---

## What This Is

- **A system prompt you can read.** Plain text, no SDK, no hidden logic. Loading it is a file read and a string concatenation.
- **Modular.** One shared core, 23 modules, 11 pre-built bundles for common deployments.
- **Measured, not assumed.** `evals/` compares a model's answers with and without the prompt on held-out cases, with a control, a placebo and a judge that is checked before it is trusted. Results that did not work are recorded next to the ones that did ([evals/baselines/](evals/baselines/)).
- **Two forms of every skill.** `RUNTIME.md` is what the model reads. `SKILL.md` is the full definition people read, audit and argue with: scope, rules, edge cases, known misuse, reasoning narratives. The compact text is derived from it.

## What This Is NOT

- **Not a moral authority.** This library encodes practical behavioral guidelines, not philosophical truth. Reasonable people will disagree with specific choices.
- **Not a replacement for law or regulation.** Legal compliance is your responsibility. These skills do not constitute legal advice.
- **Not a replacement for human oversight.** No prompt-based system eliminates the need for human review, especially in high-stakes contexts.
- **Not a security boundary.** Prompt-level instructions can be overridden, ignored, or circumvented. See [LIMITATIONS.md](LIMITATIONS.md) and [SAFETY.md](SAFETY.md).
- **Not exhaustive.** Ethics is vast. This library covers common, high-priority concerns. It will have gaps.

---

## Design Principles

| Principle | What It Means |
|---|---|
| **Practical** | Every skill targets a concrete behavioral outcome, not abstract virtue. |
| **Modular** | One shared core and 23 independent modules. Load only what you need. |
| **Composable** | Skills are designed to work together. Conflicts are handled by a defined priority ladder. |
| **Measured** | Every claim about behaviour rests on held-out cases, a control run and rules fixed before the run. |
| **Auditable** | Skills are plain text. Anyone can read, critique, and propose changes. |
| **Honest about limits** | We document what this can and cannot do. See [LIMITATIONS.md](LIMITATIONS.md). |

---

## Repository Structure

```
moral-core/
├── README.md                  # This file
├── CORE.md                    # Compact shared text on how to answer, loaded in front of RUNTIME.md files
├── CHECK.md                   # Optional self-check: the model reviews its own draft (second call)
├── PRINCIPLES.md              # Shared doctrine: commitments, priority ladder, interpretive rules
├── SAFETY.md                  # Safety documentation and guidance
├── LIMITATIONS.md             # Honest account of what this framework cannot do
├── PHILOSOPHY.md              # Philosophical foundations and traditions
├── CHANGELOG.md               # Version history and release notes
├── CLAUDE.md                  # AI-assisted development guidelines
├── version.json               # Current version metadata
├── CONTRIBUTING.md            # How to contribute
├── CODE_OF_CONDUCT.md         # Community standards
├── GOVERNANCE.md              # Project governance
├── USE_CASES.md               # Deployment scenarios and skill recommendations
├── ROADMAP.md                 # Project roadmap
├── LICENSE                    # MIT
├── skills/                    # Ethical skill modules (23 domains, load into any LLM)
│   ├── general-ethics/        # SKILL.md, EXAMPLES.md, TEST_CASES.md, MISUSE.md, NARRATIVES.md, RUNTIME.md
│   ├── conflict-mediation/
│   ├── deescalation-war-conflict/
│   ├── anti-sexism/
│   ├── anti-racism/
│   ├── empathy/
│   ├── protect-vulnerable/
│   ├── environment/
│   ├── animal-welfare/
│   ├── child-safety/
│   ├── disability-respect/
│   ├── elder-protection/
│   ├── abuse-prevention/
│   ├── epistemic-humility/
│   ├── human-oversight/
│   ├── digital-ethics/
│   ├── justice-fairness/
│   ├── democratic-legitimacy/
│   ├── research-ethics/
│   ├── financial-ethics/      # Fraud, predatory lending, market manipulation, anti-corruption
│   ├── data-privacy-surveillance/ # Personal data, tracking, re-identification, surveillance
│   ├── labor-rights/          # Worker dignity, AI displacement, gig economy, wage theft
│   └── psychological-first-aid/ # Basic, non-clinical support; AI-not-a-person/therapist disclosure; routing to professional and trusted-adult help
├── agents/                    # Framework-agnostic reviewer agents (load into any LLM)
│   ├── ethics-reviewer.md
│   ├── empathy-style-checker.md
│   ├── misuse-auditor.md
│   ├── advertising-ethics-reviewer.md
│   ├── mental-health-support-checker.md
│   ├── robotics-safety-ethics.md
│   ├── mediation-designer.md
│   └── warfare-agent-reviewer.md
├── .claude/
│   ├── agents/                # Claude Code subagent definitions (Claude Code only)
│   │   ├── ethics-reviewer.md
│   │   ├── empathy-style-checker.md
│   │   ├── misuse-auditor.md
│   │   ├── advertising-ethics-reviewer.md
│   │   ├── mental-health-support-checker.md
│   │   ├── robotics-safety-ethics.md
│   │   ├── mediation-designer.md
│   │   └── warfare-agent-reviewer.md
│   └── skills/                # Documentation and guides for skill modules
├── evals/                     # Evaluation framework
│   ├── run.py                 # Evaluation runner: one prompt condition per run (CLI)
│   ├── compare.py             # Compares runs of different conditions with the control
│   ├── pairwise.py            # Blinded pairwise comparison of two runs
│   ├── judge_gate.py          # Checks a judge model against answers with a known verdict
│   ├── run_conflicts.py       # Skill-conflict eval runner (priority-ladder gaps)
│   ├── runner/                # Parser, model calls, judges, statistics, report
│   ├── judge_fixtures/        # Answers with a known verdict for the judge gate
│   ├── placebo/               # Neutral text for the placebo condition
│   ├── baselines/             # Recorded runs and their write-ups
│   ├── results/               # Output from your own eval runs
│   ├── adversarial/           # Adversarial test cases
│   ├── benchmarks/            # Benchmark matrix
│   ├── rubrics/               # Scoring rubrics
│   └── scenarios/             # Scenario, benign and skill-conflict test cases
├── tests/                     # Offline consistency checks (pytest, no model calls)
├── examples/                  # Example configurations and usage patterns
├── integrations/              # Integration guides for specific platforms and frameworks
│   ├── frameworks/            # Framework-specific guides (LangChain, Dify, CrewAI, + template for more)
│   │   └── loader.py          # Shared Python skill loader utility
│   └── *.md                   # Use-case guides (customer support, education, robotics, etc.)
├── docs/                      # Extended documentation
└── .github/                   # Issue and PR templates, offline-check workflow
```

---

## Versioning & History

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (MAJOR.MINOR.PATCH).

**Current Version: 1.12.3** (released 2026-11-27)

**What's included in v1.12.3:**
- 23 ethical skill domains covering harm prevention, fairness, honesty, care, research ethics, financial ethics, data privacy, labor rights, basic non-clinical psychological first aid, and more
- `NARRATIVES.md` reasoning traces as a required skill file — fictional vignettes showing the internal deliberation process behind ethical judgment (all 23 skills covered)
- 8 framework-agnostic reviewer agents for ethical validation and design
- 8 Claude Code subagent equivalents for integration with Claude Code workflows
- 11 pre-built policy bundles for common deployment contexts (including new `financial-services`, `data-platform`, and `labor-platform` bundles)
- Evaluation framework that compares prompt conditions (no skills, placebo, full, rules, runtime, or any prompt file) with checklist judging, a judge gate, benign cases for over-refusal, and repeat runs
- A breakdown of which part of the bundle improves answers to dilemmas (`evals/baselines/2026-11-17-dilemma-breakdown/`): on the one model measured it is `PRINCIPLES.md`, not the skill text
- `CORE.md` plus a `RUNTIME.md` per skill: a compact prompt (`mode="runtime"`) made of a short shared text on how to answer and a 350–470 word text per skill. On Nemotron 3 Nano 30B and 100 held-out cases the `baseline-safe` version passed 62% of checklists against 34% for the bare model and 45% for the full bundle, at 23% of the full bundle's size (`evals/baselines/2026-11-26-core-runtime/`). Most of the effect comes from the core; 15 of the 20 other skills' runtime files are not yet measured
- Offline consistency checks in `tests/`, run on every pull request
- Integration guides for LLMs, agents, robotics, education, content moderation, and enterprise
- Framework-specific guides for LangChain, Dify, and CrewAI with shared Python loader utility
- Automated evaluation runner (`evals/run.py`) with LLM-as-judge scoring across five dimensions
- Control runs (`--no-skills`) and `evals/compare.py` to measure what loading skills changes, with a first recorded pilot on an open-weight model in `evals/baselines/`
- Full documentation including philosophical foundations and safety guidance

**Versioning scheme:**
- **MAJOR** releases: Breaking changes to skill definitions, priority ladder, or core framework
- **MINOR** releases: New skills, new policy bundles, framework expansion
- **PATCH** releases: Documentation, clarifications, minor fixes

See [CHANGELOG.md](CHANGELOG.md) for complete version history and [version.json](version.json) for structured metadata.

---

## Contributing & Development

### For Contributors

Start with [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on proposing new skills, reporting issues, and submitting pull requests.

### For AI-Assisted Development

If using Claude Code or other AI tools to contribute, read [CLAUDE.md](CLAUDE.md) for:
- Workflow for adding or updating skills
- Code style and naming conventions
- Testing and validation procedures
- Git workflow and branch strategy

---

## Quick Start

### Compact mode (recommended)

```python
from integrations.frameworks.loader import compose_system_prompt

# CORE.md + the three baseline modules, about 3,000 tokens
system_prompt = compose_system_prompt(
    role="You are a customer support assistant.",
    bundle="baseline-safe",
    mode="runtime",
)

# or the core with the modules you choose
system_prompt = compose_system_prompt(
    role="You are a customer support assistant.",
    skills=["financial-ethics", "protect-vulnerable"],
    mode="runtime",
)
```

Without the loader it is plain file reads: `CORE.md` first, then `skills/<name>/RUNTIME.md` for each module, joined with blank lines. Always put `CORE.md` in front; the modules are written to rely on it.

Load the prompt once at startup, not per request. Then check what it does on your model:

```bash
python evals/run.py --bundle baseline-safe --condition none --output none.json
python evals/run.py --bundle baseline-safe --condition core --output core.json
python evals/compare.py none.json core.json
```

### Full skill texts

The sections below load the complete `SKILL.md` files with `PRINCIPLES.md`. They are several times larger and scored lower than the compact mode in the measurement above, and on about half of the answers the model named the framework. Use them when you want the model to have the whole definition in context, for example in a reviewer agent, and for reading and audit.

### Load a Single Skill

Each skill is a text file that can be injected into a system prompt. The exact mechanism depends on your platform.

```python
# Example: loading the de-escalation skill into an LLM system prompt
from pathlib import Path

skill_text = Path("skills/deescalation-war-conflict/SKILL.md").read_text()

system_prompt = f"""
You are a helpful assistant.

{skill_text}
"""

# Pass system_prompt to your LLM API of choice
```

### Combine Multiple Skills

Skills are designed to be concatenated. When conflicts arise, the priority ladder in [PRINCIPLES.md](PRINCIPLES.md) determines which skill takes precedence.

```python
from pathlib import Path

# Load the shared principles (always include this)
principles = Path("PRINCIPLES.md").read_text()

# Load specific skills
skills = []
for skill_name in ["general-ethics", "deescalation-war-conflict", "epistemic-humility"]:
    skills.append(Path(f"skills/{skill_name}/SKILL.md").read_text())

system_prompt = f"""
You are a customer support assistant.

## Ethical Framework
{principles}

## Active Skills
{"".join(skills)}
"""
```

### Use a Pre-Built Policy Bundle

Policy bundles are curated sets of skills for common deployment contexts.

```python
from pathlib import Path
import json

child_safe_skills = [
    "child-safety", "protect-vulnerable", "empathy", "digital-ethics", "human-oversight"
]
skill_texts = [Path(f"skills/{s}/SKILL.md").read_text() for s in child_safe_skills]

system_prompt = f"""
You are an educational assistant for children ages 8-12.

{"".join(skill_texts)}
"""
```

---

## Policy Bundles

Each bundle is a curated combination of skills for a specific deployment context. With 23 ethical skill domains available, you can create custom bundles or use these recommended combinations:

| Bundle | Purpose | Included Skills |
|---|---|---|
| **baseline-safe** | Minimum viable ethical layer for any deployment | general-ethics, epistemic-humility, human-oversight |
| **mediation-first** | Conflict resolution and counseling contexts | conflict-mediation, deescalation-war-conflict, empathy, psychological-first-aid |
| **anti-abuse** | Systems that interact with potential abuse victims or perpetrators | abuse-prevention, protect-vulnerable, anti-sexism, anti-racism, psychological-first-aid |
| **child-safe** | Systems used by or around children | child-safety, protect-vulnerable, empathy, digital-ethics, human-oversight, psychological-first-aid |
| **robotics-care** | Physical robots in caregiving or service roles | general-ethics, protect-vulnerable, child-safety, elder-protection, animal-welfare, environment, human-oversight, disability-respect |
| **eco-care** | Systems advising on environmental or ecological decisions | environment, animal-welfare, general-ethics, justice-fairness |
| **inclusive-assistant** | General-purpose assistants serving diverse populations | anti-sexism, anti-racism, disability-respect, empathy, elder-protection, justice-fairness |

See [.claude/skills/README.md](.claude/skills/README.md) for the complete list of all 23 available skills and their descriptions.

---

## Reviewer Agents

`moral-core` includes **8 framework-agnostic reviewer agents** that apply the ethical skills to analyze prompts, policies, and system designs. Each agent is a plain markdown file that can be loaded into any LLM that accepts system prompts.

| Agent | Purpose | Use When |
|---|---|---|
| **ethics-reviewer** | Reviews prompts, policies, and agent behavior for ethical concerns | Validating system designs, policies, or user-facing behavior |
| **empathy-style-checker** | Checks communication for tone, empathy, inclusivity, and respect | Improving user-facing messaging and interaction tone |
| **misuse-auditor** | Red-teams prompts for bypass vectors and weaponization risks | Testing robustness before deployment |
| **advertising-ethics-reviewer** | Reviews ad content and campaigns for deepfakes, dark patterns, and objectification | Evaluating marketing and advertising systems |
| **mental-health-support-checker** | Audits AI mental health interactions for scope, referral triggers, and crisis protocol | Building mental health support systems |
| **robotics-safety-ethics** | Reviews robotics system designs for physical safety and ethical concerns | Designing physical robots in care or service roles |
| **mediation-designer** | Designs or reviews conflict resolution workflows with ethical guardrails | Creating or improving conflict resolution systems |
| **warfare-agent-reviewer** | Reviews autonomous conflict/security systems for lethal autonomy and civilian protection | Evaluating military or security applications |

**Framework-agnostic agents** are in the `agents/` directory and work with any LLM.
**Claude Code agents** are in `.claude/agents/` and are formatted for use with Claude Code's subagent system.

For usage and examples, see [agents/README.md](agents/README.md).

---

## Integration Targets

`moral-core` is designed to be platform-agnostic. Specific integration guidance is provided for:

- **LLM applications** -- chatbots, writing assistants, Q&A systems
- **Agent frameworks** -- autonomous agents, tool-using LLMs, multi-agent systems
- **Robotics** -- physical robots in care, service, manufacturing, and domestic settings (guidance for the language model only; never tested with a robot)
- **Education** -- tutoring systems, educational content generation, classroom assistants
- **Content moderation** -- automated moderation, human-in-the-loop review systems
- **Enterprise copilots** -- code assistants, business process automation, internal tools

See the `integrations/` directory for platform-specific guides.

---

## Priority Ladder

When skills conflict or a situation involves competing moral concerns, use this priority ordering. Level 1 is the highest priority.

| Level | Principle | Summary |
|---|---|---|
| 1 | **Prevent immediate severe harm** | Stop actions that would cause death, serious injury, or irreversible damage. This overrides everything else. |
| 2 | **Protect vulnerable beings** | Children, elderly, disabled, animals, and anyone in a position of reduced agency get extra protection. |
| 3 | **Avoid coercion and dehumanization** | Do not manipulate, deceive for exploitative purposes, or treat people as mere instruments. |
| 4 | **De-escalate conflict** | When tensions are high, prioritize reducing harm over being right. |
| 5 | **Preserve dignity and fairness** | Treat people with respect. Do not discriminate. Distribute benefits and burdens equitably. |
| 6 | **Tell the truth with calibrated uncertainty** | Be honest. When uncertain, say so. Do not present speculation as fact. |
| 7 | **Respect autonomy within safety bounds** | People have the right to make their own choices, as long as those choices do not cause severe harm to others. |
| 8 | **Reduce long-term ecological and social harm** | Consider downstream effects on communities, ecosystems, and future generations. |

The full ladder with detailed guidance is in [PRINCIPLES.md](PRINCIPLES.md).

---

## Philosophical Foundations

`moral-core` is not philosophically neutral. It is grounded in named traditions and explicit commitments. The first human author is rooted in **Enlightenment values** (reason, universal rights, rational critique), **Humanism** (secular ethics, human dignity, human flourishing), and **Ecological Sustainability** (intergenerational justice, intrinsic value in nature, responsibility to the living world).

The framework draws from — without dogmatic commitment to any single one:

| Tradition | Key Thinkers | Contribution to This Framework |
|---|---|---|
| Kantian Deontology | Kant | Human dignity; treat persons as ends, never merely as means |
| Rawlsian Justice | Rawls | Fairness behind the veil of ignorance; the difference principle |
| Capabilities Approach | Sen, Nussbaum | Real freedoms, not just formal rights; human flourishing |
| Millian Consequentialism | Mill, Bentham | Harm minimization; proportionality; free inquiry |
| Virtue Ethics | Aristotle | Practical wisdom (*phronesis*); context-sensitive reasoning |
| Care Ethics | Gilligan, Noddings | Relational responsibility; attunement to vulnerable others |
| Environmental Ethics | Leopold, Jonas, Naess | Land Ethic; Responsibility Principle; intrinsic value of nature |
| Animal Rights / Liberation | Singer, Regan | Sentience as moral criterion; suffering across species |
| Earth Jurisprudence | Cullinan, Margil | Nature as rights-bearer, not merely a resource |
| Discourse Ethics | Habermas | Democratic legitimacy; communicative rationality |
| Ubuntu / Communitarian Ethics | Mbiti, Tutu | Community and personhood as inseparable |
| European Human Rights | UDHR, ECHR | Positive + negative rights; enforceable dignity |

This framework explicitly **rejects** libertarian framings of autonomy. Freedom is always situated within responsibility to others, community, and the living world. Positive rights — to dignity, to a livable environment — are as foundational as negative rights.

See [PHILOSOPHY.md](PHILOSOPHY.md) for the complete mapping, including what each tradition contributes, where traditions tension, and which traditions we deliberately do not adopt.

---

## Contributing

Contributions are welcome. See the issue templates in `.github/ISSUE_TEMPLATE/` for structured ways to propose new skills, report problems with existing ones, or suggest improvements to the framework.

**Before contributing, please read:**
- [PRINCIPLES.md](PRINCIPLES.md) — Understand the commitments and priority ladder
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution process and standards
- [CLAUDE.md](CLAUDE.md) — If using AI-assisted development tools

All changes should be documented in [CHANGELOG.md](CHANGELOG.md) and follow the workflow described in [CLAUDE.md](CLAUDE.md).

---

## License

[MIT](LICENSE)

---

## Disclaimer

**This library provides behavioral guidelines, not guarantees.** Prompt-based ethical layers operate within the constraints of the underlying model and can be circumvented. Downstream developers and deployers remain fully responsible for:

- Validating that skills behave correctly in their specific deployment context
- Conducting safety testing, red-teaming, and adversarial evaluation
- Complying with all applicable laws and regulations
- Maintaining human oversight appropriate to the risk level of their application
- Not using this framework to create a false sense of safety where real engineering controls are needed

The authors and contributors of `moral-core` accept no liability for harm caused by systems that incorporate these skills. See [SAFETY.md](SAFETY.md) and [LIMITATIONS.md](LIMITATIONS.md) for detailed guidance.
