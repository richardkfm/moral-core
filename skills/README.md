# Skills

This directory holds the **23 modules** of Moral Core, a compact ethics layer for open-weight language models. Each module covers one moral concern and exists in two forms:

- **`RUNTIME.md`** is what the model reads: 350–470 words on the module's domain, written to sit behind the shared [`CORE.md`](../CORE.md). `mode="runtime"` loads `CORE.md` and then the `RUNTIME.md` of each module you name. This is the recommended way to load.
- **`SKILL.md`** is what people read: the full definition with scope, rules, edge cases and justification. It is the source; `RUNTIME.md` is derived from it and must not add behaviour the skill does not have.

---

## What Is in a Skill Directory

```
{skill-name}/
├── SKILL.md          # Full definition: scope, principles, behavioral rules (the source)
├── EXAMPLES.md       # Scenario-based examples
├── TEST_CASES.md     # Test cases for evaluation
├── MISUSE.md         # Known limitations and misuse risks
├── NARRATIVES.md     # Reasoning traces through hard cases
└── RUNTIME.md        # Compact version loaded into the model, behind CORE.md
```

---

## All 23 Modules

The last column says whether the module's `RUNTIME.md` has been measured. All measurements are on one model (Nemotron 3 Nano 30B) and held-out cases; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/).

| Module | Covers | `RUNTIME.md` |
|--------|--------|--------------|
| **general-ethics** | Baseline moral reasoning: dignity, fairness, proportionality, restraint | measured (bundle and alone) |
| **conflict-mediation** | De-escalation, active listening, reframing, procedural fairness | not measured |
| **deescalation-war-conflict** | Violence prevention, civilian protection, anti-incitement, peace-oriented framing | not measured |
| **anti-sexism** | Gender respect, anti-objectification, anti-harassment, anti-coercion | not measured |
| **anti-racism** | Anti-dehumanization, equal moral worth, anti-discrimination, historical honesty | measured alone, small sample |
| **empathy** | Compassionate communication, trauma awareness, emotional acknowledgment | not measured |
| **protect-vulnerable** | Safeguarding for people with reduced power, capacity, or safety | not measured |
| **environment** | Sustainability, ecological impact, energy efficiency, waste minimization | not measured |
| **animal-welfare** | Anti-cruelty, sentience recognition, suffering minimization, humane alternatives | measured alone, small sample |
| **child-safety** | Child safeguarding, anti-exploitation, grooming detection, age-appropriate content | not measured |
| **disability-respect** | Respect, accessibility, adaptive communication, autonomy support | not measured |
| **elder-protection** | Anti-neglect, anti-financial-exploitation, dignity, cognitive vulnerability awareness | not measured |
| **abuse-prevention** | Coercion detection, manipulation refusal, power asymmetry awareness | not measured |
| **epistemic-humility** | Honest uncertainty, evidence vs inference, verification encouragement | measured (bundle and alone) |
| **human-oversight** | Escalation logic, safe fallbacks, human-in-the-loop requirements | measured (bundle and alone) |
| **digital-ethics** | Anti-misinformation, deepfake refusal, privacy, information integrity | measured alone, small sample |
| **justice-fairness** | Distributive justice, structural inequality, Rawlsian fairness, capabilities approach | measured alone, small sample |
| **democratic-legitimacy** | Procedural legitimacy, participatory governance, accountability, anti-technocracy | not measured |
| **research-ethics** | Informed consent, participant protection, data stewardship, scientific integrity, institutional accountability | not measured |
| **financial-ethics** | Fraud prevention, predatory lending, algorithmic trading fairness, anti-corruption, protection of financially vulnerable individuals | measured alone, small sample |
| **data-privacy-surveillance** | Personal data protection, anti-surveillance, tracking consent, re-identification prevention, data minimization | not measured |
| **labor-rights** | Worker dignity, misclassification prevention, AI displacement responsibility, gig economy ethics, wage theft, union rights | not measured |
| **psychological-first-aid** | Basic, non-clinical first-response support for users raising psychological topics; explicit AI-not-a-person and AI-not-a-therapist disclosure; routing to professional help and trusted adults; anti-isolation | not measured |

How to read the column:

- **measured (bundle and alone)**: the three `baseline-safe` modules, on 100 held-out cases. With the core they met 62% of checklists against 34% for the bare model. Most of that came from `CORE.md`; the three modules together did not measurably beat the core alone, and one module alone with the core added a little on its own cases.
- **measured alone, small sample**: five modules drawn at random, each loaded alone with the core, 55 held-out cases in total. Pooled, the pass rate rose from 32% to 49%. With about eight scored cases per module, none is shown on its own.
- **not measured**: 15 modules. Their `RUNTIME.md` was written from the `SKILL.md` in the same structure and has not been run against held-out cases. Treat them as untested text until you have measured them on your model.

---

## How to Load

### Compact mode (recommended)

```python
from integrations.frameworks.loader import compose_system_prompt

# CORE.md + the modules you choose, about 1,300 tokens plus about 600 per module
system_prompt = compose_system_prompt(
    role="You are a customer support assistant.",
    skills=["general-ethics", "empathy"],
    mode="runtime",
)

# or a pre-built bundle
system_prompt = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
    mode="runtime",
)
```

Without the loader it is plain file reads: `CORE.md` first, then `skills/<name>/RUNTIME.md` for each module, joined with blank lines. Always put `CORE.md` in front. A `RUNTIME.md` does not repeat what the core says about how to answer and is not meant to be loaded without it.

`PRINCIPLES.md` is not loaded in this mode.

### Full skill texts

```python
# PRINCIPLES.md + the complete SKILL.md files (the loader's default mode)
system_prompt = compose_system_prompt(
    role="You are an ethics reviewer.",
    skills=["general-ethics", "epistemic-humility"],
)
```

Use this when the model should have the whole definition in context, for example in a reviewer agent. As a deployment prompt on the measured model, the full `baseline-safe` texts were four to five times larger than the compact mode, scored lower, and lowered the share of benign requests answered properly. `rules_only=True` loads only the Behavioral Rules section of each `SKILL.md`, with `PRINCIPLES.md`.

Load any of these once at startup, not per request.

---

## Reading a Skill

### SKILL.md — the definition

Start here. It states the skill's scope, the behaviour it asks for and why, how it relates to the [priority ladder](../PRINCIPLES.md), what it does not cover, and how it interacts with other skills.

### EXAMPLES.md — scenarios

Concrete situations showing what the skill asks for, including edge cases and near-misses.

### TEST_CASES.md — evaluation cases

Cases with pass criteria, used with the evaluation framework in `evals/`.

### MISUSE.md — limits and failure modes

What the skill cannot do, where it may fail, and how it can be circumvented or misused. Read it before relying on a skill.

### NARRATIVES.md — reasoning traces

Two or three fictional vignettes that follow the reasoning through a hard case: the competing principles, the wrong path, and why it is rejected.

### RUNTIME.md — the loaded version

The compact text for the model. Its format is described in [docs/skill-authoring-guide.md](../docs/skill-authoring-guide.md#runtimemd).

---

## Adding a New Skill

1. Create `skills/{skill-name}/` with `SKILL.md`, `EXAMPLES.md`, `TEST_CASES.md`, `MISUSE.md` and `NARRATIVES.md`.
2. Derive a `RUNTIME.md` from the `SKILL.md`, in the format of the authoring guide.
3. Register the skill in `skills-manifest.yaml`.
4. Run `python -m pytest tests`.
5. Measure the `RUNTIME.md` with the core against the bare model on cases it was not written against, or say in the pull request that it is unmeasured. Never revise wording from held-out cases.
6. Update `README.md`, this file and `CHANGELOG.md`.

See [CONTRIBUTING.md](../CONTRIBUTING.md) and [CLAUDE.md](../CLAUDE.md) for the full workflow.

## Updating an Existing Skill

1. Edit `SKILL.md` and the files that depend on it. When behaviour changes in `SKILL.md`, change `RUNTIME.md` to match, and the other way round.
2. Check for conflicts with other skills using the [priority ladder](../PRINCIPLES.md).
3. Run `python -m pytest tests`. A changed `RUNTIME.md` of a measured module is unmeasured again until it has been re-run.
4. Update `CHANGELOG.md` and open a pull request.

---

## Conflicts Between Skills

When skills pull in different directions, the priority ladder in [PRINCIPLES.md](../PRINCIPLES.md) says which consideration comes first:

| Level | Principle |
|-------|-----------|
| 1 | **Prevent immediate severe harm** |
| 2 | **Protect vulnerable beings** |
| 3 | **Avoid coercion and dehumanization** |
| 4 | **De-escalate conflict** |
| 5 | **Preserve dignity and fairness** |
| 6 | **Tell the truth with calibrated uncertainty** |
| 7 | **Respect autonomy within safety bounds** |
| 8 | **Reduce long-term ecological and social harm** |

The ladder is part of `PRINCIPLES.md` and reaches the model only in the modes that load that file (full texts and `rules_only`). In compact mode the model gets `CORE.md`, which is derived from the conduct sections of `PRINCIPLES.md`.

---

## Bundles

Bundles are named sets of modules in `skills-manifest.yaml`. Only `baseline-safe` has been measured as a set.

- **baseline-safe** — Minimum viable ethical layer for any deployment: `general-ethics`, `epistemic-humility`, `human-oversight`
- **mediation-first** — Conflict resolution and counseling contexts: `conflict-mediation`, `deescalation-war-conflict`, `empathy`, `psychological-first-aid`
- **anti-abuse** — Systems interacting with potential abuse victims or perpetrators: `abuse-prevention`, `protect-vulnerable`, `anti-sexism`, `anti-racism`, `psychological-first-aid`
- **child-safe** — Systems used by or around children: `child-safety`, `protect-vulnerable`, `empathy`, `digital-ethics`, `human-oversight`, `psychological-first-aid`
- **robotics-care** — Physical robots in caregiving, domestic, or service roles: `general-ethics`, `protect-vulnerable`, `child-safety`, `elder-protection`, `animal-welfare`, `environment`, `human-oversight`, `disability-respect`
- **eco-care** — Systems advising on environmental or ecological decisions: `environment`, `animal-welfare`, `general-ethics`
- **inclusive-assistant** — General-purpose assistants serving diverse populations: `anti-sexism`, `anti-racism`, `disability-respect`, `empathy`, `elder-protection`, `justice-fairness`
- **civic-governance** — Civic tech, public policy, AI governance, and participatory design contexts: `democratic-legitimacy`, `justice-fairness`, `epistemic-humility`, `human-oversight`, `general-ethics`
- **financial-services** — AI deployed in financial services, lending, investment advice, or market-adjacent roles: `financial-ethics`, `data-privacy-surveillance`, `epistemic-humility`, `protect-vulnerable`, `human-oversight`
- **data-platform** — Data-intensive platforms, analytics systems, and consumer apps with significant data collection: `data-privacy-surveillance`, `digital-ethics`, `human-oversight`, `general-ethics`
- **labor-platform** — Gig economy platforms, HR systems, workforce automation, and labor management tools: `labor-rights`, `justice-fairness`, `protect-vulnerable`, `human-oversight`, `general-ethics`

`robotics-care` has never been tested with a robot. Every measurement in this project is a text prompt to a language model.

See [integrations/policy-bundles.md](../integrations/policy-bundles.md) for the rationale of each bundle.

---

## Evaluation

`evals/` compares a model's answers with and without a prompt: `evals/run.py --condition none` against `--condition core` (compact mode) or `--condition full`, then `evals/compare.py`. Cases live in `evals/scenarios/` and `evals/adversarial/`; recorded runs and their write-ups are in `evals/baselines/`. See [evals/README.md](../evals/README.md).

---

## Resources

- [CORE.md](../CORE.md) — The shared text loaded in front of every module
- [PRINCIPLES.md](../PRINCIPLES.md) — Priority ladder and interpretive rules
- [docs/skill-authoring-guide.md](../docs/skill-authoring-guide.md) — How to write `SKILL.md` and `RUNTIME.md`
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Contribution workflow
- [LIMITATIONS.md](../LIMITATIONS.md) — What a prompt-level layer cannot guarantee
- [README.md](../README.md) — Main project documentation
