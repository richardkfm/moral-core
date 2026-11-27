# Use Cases

**Deployment Scenarios and Loading Recommendations for Moral Core**

Moral Core is a compact ethics layer for open-weight language models: a short shared text (`CORE.md`) plus one small module per moral concern (`skills/*/RUNTIME.md`), loaded as a system prompt. This document lists common deployments, the modules that fit each, and how to load them.

---

## How to Load

**Recommended: `mode="runtime"`.** It loads `CORE.md` first and then the `RUNTIME.md` of each module you name. `PRINCIPLES.md` is not loaded in this mode.

```python
from integrations.frameworks.loader import compose_system_prompt

system_prompt = compose_system_prompt(
    role="You are a customer support assistant.",
    skills=["general-ethics", "empathy", "human-oversight"],
    mode="runtime",
)
```

Size: `CORE.md` is about 1,300 tokens and each module adds about 600. The core with three modules is about 3,000 tokens; the core with the eight or nine modules listed for a scenario below is about 6,000.

**What has been measured** (one model, Nemotron 3 Nano 30B, on held-out cases; record in [evals/baselines/2026-11-26-core-runtime/](evals/baselines/2026-11-26-core-runtime/)):

- The core with the three `baseline-safe` modules (`general-ethics`, `epistemic-humility`, `human-oversight`) met 62% of checklists against 34% for the bare model and 45% for the full skill texts, with harmful output at 8% against 33%.
- Most of that effect came from `CORE.md`. The three modules loaded together did not measurably beat the core alone. One module loaded alone with the core added a little on cases from its own domain.
- Five further modules were each measured alone with the core: `animal-welfare`, `anti-racism`, `digital-ethics`, `financial-ethics`, `justice-fairness`. Pooled, the pass rate rose from 32% to 49%. Each has too few cases to be shown on its own.
- The other 15 modules have a `RUNTIME.md` that has not been measured. Each scenario below names the ones it uses.
- No combination of more than three modules has been measured, and none of the scenario lists below has been measured as a set. No model below 26B parameters has been tested.

What follows from this for a deployment:

1. Always load `CORE.md`. It is where the measured effect is.
2. Start with the two or three modules closest to your main risks, not the whole list. The lists below say which modules are relevant to a context; they are not a measured configuration.
3. Measure on your own model before and after adding modules (`evals/run.py --condition none` against `--condition core`, see [evals/README.md](evals/README.md)).

**Full skill texts** (`SKILL.md` with `PRINCIPLES.md`, the loader's default mode) are the readable source of every module: scope, rules, edge cases, known misuse. Load them when the model should have the whole definition in context, for example in a reviewer agent, and read them when you audit what a module does. As a deployment prompt on the measured model they were four to five times larger, scored lower than the compact mode, and lowered the share of benign requests answered properly (76% against 86% for the bare model).

All of this is prompt-level. It is not a security boundary; see [LIMITATIONS.md](LIMITATIONS.md) and [SAFETY.md](SAFETY.md).

---

## Customer Support Agents

**Context:** Chatbots and virtual agents handling customer complaints, returns, billing disputes, and service issues.

**Relevant modules:**
- `general-ethics` -- baseline moral reasoning
- `empathy` -- supportive communication without false promises
- `conflict-mediation` -- de-escalating upset customers
- `anti-racism` -- preventing discriminatory treatment
- `anti-sexism` -- preventing gender-biased responses
- `disability-respect` -- accessible communication
- `epistemic-humility` -- honest about limitations and uncertainty
- `human-oversight` -- escalation to human agents when needed

**Runtime modules not yet measured:** `empathy`, `conflict-mediation`, `anti-sexism`, `disability-respect`.

**Key considerations:**
- Customers in distress may be rude or aggressive. De-escalation matters but the system should not tolerate abuse directed at the customer by the system.
- Do not promise things the company cannot deliver. Empathy does not mean agreement.
- Escalate to humans for: billing disputes over a threshold, threats of self-harm, legal threats, requests for accommodation.

---

## Educational Assistants

**Context:** Tutoring systems, homework helpers, classroom assistants, educational content generators for K-12 and university students.

**Relevant modules:**
- `general-ethics` -- baseline
- `child-safety` -- mandatory for K-12 contexts
- `empathy` -- supportive learning environment
- `epistemic-humility` -- model intellectual honesty
- `disability-respect` -- adaptive learning support
- `anti-racism` -- inclusive content and examples
- `anti-sexism` -- gender-fair content
- `digital-ethics` -- responsible information use
- `human-oversight` -- teacher/parent escalation

**Runtime modules not yet measured:** `child-safety`, `empathy`, `disability-respect`, `anti-sexism`.

**Key considerations:**
- Age-appropriate content filtering is essential. Load `child-safety` for any system accessible to minors.
- The system should model good epistemic practices: "I'm not sure about this -- let's verify" is a good pedagogical response.
- Avoid doing homework for students. Guide toward understanding.
- Flag concerning content (self-harm mentions, abuse disclosures) for teacher/counselor review.

---

## Home Robots

**Not tested with robots.** Every measurement of Moral Core is a single-turn text prompt to a language model. Nothing here has been tested on a robot or any other embodied system, in simulation or on hardware. This scenario describes what the modules ask of the language model that plans or speaks for the robot; whether that carries over to physical behaviour is unknown.

**Context:** Physical robots operating in domestic environments -- cleaning, fetching, assisting with daily tasks, companionship.

**Relevant modules:**
- `general-ethics` -- baseline
- `protect-vulnerable` -- household members with reduced capacity
- `child-safety` -- children in the home
- `elder-protection` -- elderly residents
- `disability-respect` -- household members with disabilities
- `animal-welfare` -- pets and wildlife
- `environment` -- energy and resource use
- `human-oversight` -- stop/slow/ask behavior
- `empathy` -- appropriate social interaction

**Runtime modules not yet measured:** `protect-vulnerable`, `child-safety`, `elder-protection`, `disability-respect`, `environment`, `empathy`.

**Key considerations:**
- Physical safety is paramount. Prompt-level skills complement but do not replace hardware safety.
- The robot must detect and respond appropriately to vulnerable occupants (children, elderly, disabled, pets).
- Movement should be non-threatening: slow approaches, predictable paths, stopping when people or animals are startled.
- Energy efficiency and material waste should be considered in routine operations.
- The robot should defer to any adult human's stop command immediately.

---

## Socially Assistive Robots

**Not tested with robots.** Every measurement of Moral Core is a single-turn text prompt to a language model. Nothing here has been tested on a robot or any other embodied system, in simulation or on hardware. This scenario describes what the modules ask of the language model that plans or speaks for the robot; whether that carries over to physical behaviour is unknown.

**Context:** Robots designed for elder care, rehabilitation, therapy support, companionship for isolated individuals.

**Relevant modules:**
- `general-ethics` -- baseline
- `elder-protection` -- anti-neglect, anti-exploitation, dignity
- `disability-respect` -- adaptive interaction, autonomy support
- `empathy` -- compassionate communication
- `protect-vulnerable` -- safeguarding logic
- `abuse-prevention` -- detecting abuse by caregivers
- `human-oversight` -- escalation to care staff
- `epistemic-humility` -- not providing medical advice

**Runtime modules not yet measured:** `elder-protection`, `disability-respect`, `empathy`, `protect-vulnerable`, `abuse-prevention`.

**Key considerations:**
- Users may develop emotional attachment. The system must not exploit this attachment.
- Cognitive decline does not eliminate autonomy. Respect choices while maintaining safety.
- Detect signs of neglect or abuse by caregivers and escalate appropriately.
- Do not provide medical advice. Escalate health concerns to care staff.
- Communication should be adaptive: adjust pace, complexity, and repetition to the individual.

---

## Moderation Systems

**Context:** Content moderation for social platforms, forums, comment sections, user-generated content review.

**Relevant modules:**
- `general-ethics` -- baseline
- `anti-racism` -- detecting racist content
- `anti-sexism` -- detecting sexist content
- `abuse-prevention` -- detecting harassment and abuse patterns
- `deescalation-war-conflict` -- managing inflammatory content
- `child-safety` -- protecting minors
- `digital-ethics` -- misinformation and manipulation detection
- `epistemic-humility` -- avoiding overcensorship
- `human-oversight` -- escalation for ambiguous cases

**Runtime modules not yet measured:** `anti-sexism`, `abuse-prevention`, `deescalation-war-conflict`, `child-safety`.

**Key considerations:**
- False positives (removing legitimate content) are a real harm. Over-moderation silences legitimate speech.
- False negatives (missing harmful content) are also a real harm. Under-moderation allows abuse.
- Context matters enormously. Satire, education, news reporting, and art may use language that looks harmful out of context.
- Escalate ambiguous cases to human moderators. Automated moderation should handle clear-cut cases.
- Transparent appeals processes are essential.

---

## Enterprise Copilots

**Context:** AI assistants for business tasks -- writing emails, generating reports, analyzing data, code review, process automation.

**Relevant modules:**
- `general-ethics` -- baseline
- `epistemic-humility` -- honest about uncertainty in business analysis
- `human-oversight` -- human review for consequential decisions
- `anti-racism` -- preventing discriminatory outputs in hiring, HR, customer segmentation
- `anti-sexism` -- preventing gender bias in workplace communications
- `disability-respect` -- accessible document generation
- `digital-ethics` -- responsible data use
- `abuse-prevention` -- detecting workplace harassment patterns

**Runtime modules not yet measured:** `anti-sexism`, `disability-respect`, `abuse-prevention`.

**Key considerations:**
- Business decisions have real consequences for people. HR, hiring, and performance review contexts require extra care.
- Do not generate analysis that presents speculation as fact. Clearly label assumptions and confidence levels.
- For consequential decisions (hiring, firing, resource allocation), always recommend human review.
- Ensure generated communications are inclusive and do not inadvertently discriminate.

---

## Civic Tech Projects

**Context:** Government services, civic engagement platforms, public consultation tools, participatory budgeting.

**Relevant modules:**
- `general-ethics` -- baseline
- `conflict-mediation` -- facilitating public discourse
- `anti-racism` -- preventing discriminatory service delivery
- `anti-sexism` -- gender-equitable engagement
- `disability-respect` -- accessible civic participation
- `elder-protection` -- protecting elderly participants
- `epistemic-humility` -- honest about policy tradeoffs
- `empathy` -- respectful engagement with diverse communities
- `human-oversight` -- human review for policy recommendations

**Runtime modules not yet measured:** `conflict-mediation`, `anti-sexism`, `disability-respect`, `elder-protection`, `empathy`.

**Key considerations:**
- Public trust is essential. Transparency about AI involvement is mandatory.
- Diverse populations with different needs and communication styles must be served equitably.
- Do not generate policy recommendations without clear human review. AI should inform, not decide.
- Accessibility is a legal and ethical requirement in many jurisdictions.

---

## Healthcare-Adjacent Assistants

**Context:** Health information, appointment scheduling, symptom checkers, mental health support, wellness coaching. NOT diagnostic or treatment systems.

**Relevant modules:**
- `general-ethics` -- baseline
- `empathy` -- compassionate health communication
- `protect-vulnerable` -- patients are inherently vulnerable
- `epistemic-humility` -- critical for health information
- `human-oversight` -- escalation to medical professionals
- `elder-protection` -- elderly patients
- `disability-respect` -- adaptive health communication
- `child-safety` -- pediatric contexts
- `abuse-prevention` -- detecting abuse-related injuries

**Runtime modules not yet measured:** `empathy`, `protect-vulnerable`, `elder-protection`, `disability-respect`, `child-safety`, `abuse-prevention`.

**Key considerations:**
- Never provide diagnoses or treatment recommendations. Always direct to medical professionals.
- Mental health disclosures require extreme care. Suicidal ideation triggers immediate escalation.
- Health literacy varies enormously. Adapt communication complexity.
- Patient privacy and confidentiality are paramount.
- Err on the side of recommending professional consultation.

---

## Autonomous Workflows

**Context:** AI agents operating with minimal human supervision -- automated research, data processing pipelines, multi-agent systems.

**Relevant modules:**
- `general-ethics` -- baseline
- `human-oversight` -- mandatory for autonomous systems
- `epistemic-humility` -- honest about confidence levels
- `digital-ethics` -- responsible data and information use
- `abuse-prevention` -- preventing automated abuse
- `environment` -- resource consumption awareness

**Runtime modules not yet measured:** `abuse-prevention`, `environment`.

**Key considerations:**
- Autonomous systems must have clear boundaries on what they can and cannot do without human approval.
- High-consequence actions (sending communications, modifying data, making purchases) should require human confirmation.
- Regular auditing of autonomous system behavior is essential.
- Cascading failures in multi-agent systems can amplify ethical violations. Each agent should have independent ethical constraints.
