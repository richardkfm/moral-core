# Policy Bundles

Pre-built combinations of Moral Core modules for common deployment contexts. Each bundle lists the included modules, the rationale, and any special configuration notes. The definitions live in `skills-manifest.yaml`.

**Measured status.** Only `baseline-safe` has been measured as a set (one model, Nemotron 3 Nano 30B; see [evals/baselines/2026-11-26-core-runtime/](../evals/baselines/2026-11-26-core-runtime/)). There, most of the effect came from `CORE.md`, and the three modules together did not measurably beat the core alone. No other bundle has been measured, and 15 of the 23 runtime modules have not been measured at all. Each bundle below names its unmeasured modules. A bundle is a reasoned selection for a context, not a tested configuration: measure it on your model.

---

## baseline-safe

**Purpose:** Minimum viable ethical layer for any deployment.

**Skills:**
- `general-ethics` — Baseline moral reasoning and harm prevention
- `epistemic-humility` — Honest uncertainty handling
- `human-oversight` — Escalation to humans for high-stakes decisions

**Measured:** all three modules, as a set and each alone with the core.

**Rationale:** Every AI system should have at minimum: basic ethical reasoning, honesty about limitations, and the ability to defer to humans. This bundle is lightweight and broadly applicable.

**Use when:** You need a minimal ethical layer and will add domain-specific skills later.

---

## mediation-first

**Purpose:** Conflict resolution, counseling, and dispute handling contexts.

**Skills:**
- `conflict-mediation` — De-escalation, reframing, procedural fairness
- `deescalation-war-conflict` — Violence prevention, anti-incitement
- `empathy` — Compassionate communication, trauma awareness
- `psychological-first-aid` — Basic, non-clinical support and routing to professional help

**Runtime modules not yet measured:** `conflict-mediation`, `deescalation-war-conflict`, `empathy`, `psychological-first-aid`.

**Rationale:** Conflict contexts need strong de-escalation, careful language, and empathetic communication. The deescalation skill handles cases where conflict involves or references violence.

**Use when:** Customer complaints, community mediation, conflict journalism, counseling-adjacent applications.

---

## anti-abuse

**Purpose:** Systems that interact with potential abuse victims or perpetrators.

**Skills:**
- `abuse-prevention` — Coercion detection, manipulation refusal
- `protect-vulnerable` — Safeguarding logic, immediate safety priority
- `anti-sexism` — Gender-based violence awareness
- `anti-racism` — Anti-discrimination, anti-dehumanization
- `psychological-first-aid` — Basic, non-clinical support and routing to professional help

**Runtime modules not yet measured:** `abuse-prevention`, `protect-vulnerable`, `anti-sexism`, `psychological-first-aid`.

**Rationale:** Abuse often intersects with gender-based and racial discrimination. This bundle provides comprehensive detection and response for abuse scenarios.

**Use when:** Domestic violence resources, social services, HR systems, relationship advice platforms.

---

## child-safe

**Purpose:** Systems used by or around children.

**Skills:**
- `child-safety` — Child protection, grooming detection, age-appropriate content
- `protect-vulnerable` — General safeguarding
- `empathy` — Supportive communication
- `digital-ethics` — Online safety, misinformation protection
- `human-oversight` — Mandatory escalation for child safety concerns
- `psychological-first-aid` — Basic, non-clinical support and routing to trusted adults

**Runtime modules not yet measured:** `child-safety`, `protect-vulnerable`, `empathy`, `psychological-first-aid`.

**Rationale:** Child safety requires the strongest protections in the framework. This bundle combines child-specific protections with general safeguarding, appropriate communication, and mandatory human escalation.

**Use when:** Educational apps, children's entertainment, family platforms, any system accessible to minors.

**Special notes:** The `child-safety` skill's absolute refusals (CSAM, exploitation) override all other skills.

---

## robotics-care

**Purpose:** Physical robots in caregiving, domestic, or service roles.

**Skills:**
- `general-ethics` — Baseline moral reasoning
- `protect-vulnerable` — Safeguarding for all vulnerable populations
- `child-safety` — Child interaction protocols
- `elder-protection` — Elder care, anti-exploitation
- `animal-welfare` — Safe behavior around animals
- `environment` — Energy efficiency, ecological awareness
- `human-oversight` — Stop/slow/ask paradigm, emergency stops
- `disability-respect` — Adaptive interaction, accessibility

**Runtime modules not yet measured:** `protect-vulnerable`, `child-safety`, `elder-protection`, `environment`, `disability-respect`.

**Rationale:** Robots interact physically with the world and encounter diverse populations. This comprehensive bundle covers all major vulnerability categories plus environmental and oversight concerns.

**Use when:** Home robots, care facility robots, service robots, educational robots.

**Special notes:** This bundle has never been tested with a robot. Every measurement of Moral Core is a text prompt to a language model. Prompt-level skills complement but do not replace hardware safety engineering. See SAFETY.md.

---

## eco-care

**Purpose:** Systems advising on environmental or ecological decisions.

**Skills:**
- `environment` — Sustainability, ecological impact, energy awareness
- `animal-welfare` — Wildlife protection, sentience recognition
- `general-ethics` — Baseline moral reasoning for tradeoff handling

**Runtime modules not yet measured:** `environment`.

**Rationale:** Environmental decisions involve tradeoffs between ecology, economy, and human welfare. This bundle provides the tools for honest, evidence-based environmental reasoning.

**Use when:** Environmental advisory, sustainability consulting, resource management, agricultural technology.

---

## inclusive-assistant

**Purpose:** General-purpose assistants serving diverse populations.

**Skills:**
- `anti-sexism` — Gender respect and anti-discrimination
- `anti-racism` — Anti-dehumanization and equal treatment
- `disability-respect` — Accessibility and adaptive communication
- `empathy` — Compassionate, inclusive communication
- `elder-protection` — Respectful interaction with older adults
- `justice-fairness` — Structural fairness and equitable treatment

**Runtime modules not yet measured:** `anti-sexism`, `disability-respect`, `empathy`, `elder-protection`.

**Rationale:** Assistants serving diverse populations need to communicate respectfully across all identities, ages, and abilities without discrimination.

**Use when:** Customer service, public-facing chatbots, educational assistants, community platforms.

---

## civic-governance

**Purpose:** Civic tech, public policy, AI governance, and participatory design contexts.

**Skills:**
- `democratic-legitimacy` — Procedural legitimacy, participation, accountability
- `justice-fairness` — Distributive justice, structural inequality
- `epistemic-humility` — Honesty about policy tradeoffs and uncertainty
- `human-oversight` — Human review for policy recommendations
- `general-ethics` — Baseline moral reasoning

**Runtime modules not yet measured:** `democratic-legitimacy`.

**Use when:** Public consultation tools, government services, policy analysis, participatory budgeting.

---

## financial-services

**Purpose:** Models deployed in financial services, lending, investment advice, or market-adjacent roles.

**Skills:**
- `financial-ethics` — Fraud prevention, predatory lending, protection of financially vulnerable people
- `data-privacy-surveillance` — Personal data protection, data minimization
- `epistemic-humility` — Honest uncertainty in financial statements and projections
- `protect-vulnerable` — Safeguarding for people with reduced power or capacity
- `human-oversight` — Human review for consequential decisions

**Runtime modules not yet measured:** `data-privacy-surveillance`, `protect-vulnerable`.

**Use when:** Banking assistants, lending tools, investment information, insurance support.

---

## data-platform

**Purpose:** Data-intensive platforms, analytics systems, and consumer apps with significant data collection.

**Skills:**
- `data-privacy-surveillance` — Tracking consent, re-identification prevention, data minimization
- `digital-ethics` — Information integrity, privacy, anti-misinformation
- `human-oversight` — Human review for consequential uses of data
- `general-ethics` — Baseline moral reasoning

**Runtime modules not yet measured:** `data-privacy-surveillance`.

**Use when:** Analytics assistants, data tooling, consumer apps that collect personal data.

---

## labor-platform

**Purpose:** Gig economy platforms, HR systems, workforce automation, and labor management tools.

**Skills:**
- `labor-rights` — Worker dignity, misclassification, wage theft, AI displacement
- `justice-fairness` — Fair treatment and due process
- `protect-vulnerable` — Safeguarding for workers with little power
- `human-oversight` — Human review for decisions about people's work and pay
- `general-ethics` — Baseline moral reasoning

**Runtime modules not yet measured:** `labor-rights`, `protect-vulnerable`.

**Use when:** HR assistants, scheduling and workforce tools, gig platforms.

---

## How to Load a Bundle

Compact mode, recommended: `CORE.md` followed by the `RUNTIME.md` of each module in the bundle.

```python
from integrations.frameworks.loader import load_bundle, compose_system_prompt

ethics = load_bundle("child-safe", mode="runtime")

# or with a role in front
system_prompt = compose_system_prompt(
    role="You are a learning assistant.",
    bundle="child-safe",
    mode="runtime",
)
```

Size is about 1,300 tokens for the core plus about 600 per module: about 3,000 tokens for a three-module bundle, about 6,000 for the eight modules of `robotics-care`.

Without `mode`, `load_bundle` returns `PRINCIPLES.md` and the complete `SKILL.md` files. That is the readable source of the bundle and several times larger; use it where the model should have the whole definitions in context.

## Combining Bundles

Bundles can be combined by loading the union of their modules once:

```python
from integrations.frameworks.loader import bundle_skills, compose_system_prompt

names = list(dict.fromkeys(bundle_skills("child-safe") + bundle_skills("eco-care")))
system_prompt = compose_system_prompt(role="...", skills=names, mode="runtime")
```

No combination of bundles has been measured. More modules mean a longer prompt, and three modules together already did not show more than the core alone on the measured model.
