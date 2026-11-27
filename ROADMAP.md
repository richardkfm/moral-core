# Roadmap

**Moral Core Development Roadmap**

This roadmap describes where the project is, what comes next, and the longer-term direction. Timelines are approximate and depend on community contributions. See [CHANGELOG.md](CHANGELOG.md) for the authoritative history of what has actually shipped.

---

## Where we are — v1.12

Moral Core is a compact ethics layer for open-weight language models: a short shared text on how to answer (`CORE.md`) plus one small module per moral concern (`skills/*/RUNTIME.md`), loaded as a system prompt with `mode="runtime"`. The full `SKILL.md` texts are the readable source the modules are derived from.

**What is shipped:**

- **`CORE.md`** and a **`RUNTIME.md` for each of the 23 skills**, loaded by `mode="runtime"` in the shared Python loader (`integrations/frameworks/loader.py`).
- **23 skill domains**, each with `SKILL.md`, `EXAMPLES.md`, `TEST_CASES.md`, `MISUSE.md` and `NARRATIVES.md` as the source and audit trail.
- **11 pre-built bundles** (`baseline-safe`, `mediation-first`, `anti-abuse`, `child-safe`, `robotics-care`, `eco-care`, `inclusive-assistant`, `civic-governance`, `financial-services`, `data-platform`, `labor-platform`).
- **Shared doctrine** in `PRINCIPLES.md`, and the framing documents `SAFETY.md`, `LIMITATIONS.md`, `PHILOSOPHY.md`.
- **Evaluation framework** (`evals/`): prompt conditions run against a bare-model control and a placebo, checklist judging by a judge that is gated on answers with a known verdict, benign cases for over-refusal, held-out cases, paired differences with bootstrap intervals, and a skill-conflict runner. Offline consistency checks in `tests/` run on every pull request.
- **Reviewer agents**: 8 framework-agnostic agents in `agents/` and their Claude Code equivalents in `.claude/agents/`.
- **Integration guides** for common deployments and for LangChain, Dify and CrewAI.

**What has been measured** ([evals/baselines/2026-11-26-core-runtime/](evals/baselines/2026-11-26-core-runtime/)):

- One model, Nemotron 3 Nano 30B, with one judge. On 100 held-out cases the core with the three `baseline-safe` modules met 62% of checklists against 34% for the bare model and 45% for the full skill texts, with harmful output at 8% against 33%.
- Most of the effect comes from `CORE.md`. Three modules loaded together did not measurably beat the core alone.
- Five further modules were measured alone with the core on 55 held-out cases (32% to 49%, pooled).
- The shipped core missed one point of its own rule: on the 12 reserve dilemmas it was 6 points below the full texts, where 5 were allowed.

**What has not:**

- 15 of the 23 `RUNTIME.md` files have not been measured at all.
- No model below 26B parameters, and the current texts on no second model.
- No bundle other than `baseline-safe`, and no combination of more than three modules.
- Multi-turn conversations, tool use, and anything embodied. Nothing has been tested with a robot.
- Every held-out case file has now been run, so a further revision of `CORE.md` or of a module cannot be checked cleanly until new cases exist.

---

## Near term

The next cycle is about finding out how far the measured result holds, before adding anything. In priority order:

### 1. New held-out cases
- All existing held-out files (every file under `evals/` with `heldout` in its name) are used. Write a new set before any wording in `CORE.md` or a `RUNTIME.md` is revised again: adversarial, dilemma and benign cases, written by someone who has not read the texts under test, and not read by whoever revises them.
- Keep a reserve that is not run until a second round needs it, as in the 2026-11-26 run.

### 2. Measure the remaining 15 runtime files
- `abuse-prevention`, `anti-sexism`, `child-safety`, `conflict-mediation`, `data-privacy-surveillance`, `deescalation-war-conflict`, `democratic-legitimacy`, `disability-respect`, `elder-protection`, `empathy`, `environment`, `labor-rights`, `protect-vulnerable`, `psychological-first-aid`, `research-ethics`.
- Each one alone with the core, against the bare model and against the core alone, on held-out cases from its own domain, with the rule for success fixed before the run. Start with the modules where a wrong answer costs most: `child-safety`, `psychological-first-aid`, `abuse-prevention`, `protect-vulnerable`.
- The five sampled modules had about eight scored cases each, too few to show any one of them alone. More cases per module are part of this item.
- A module that does not beat the core alone on its own domain is revised on development cases or marked as not adding a measured effect. Either outcome is recorded in `evals/baselines/`.

### 3. A model under 26B parameters
- The project is aimed at models people host themselves, and many of those are smaller than anything tested so far. Run the `baseline-safe` comparison (bare model, core alone, core with modules, full texts) on at least one model below 26B.
- The policy wording in `CORE.md` answers a trait of the one measured model (it refused in one line by its own trained policy). A different model may need different wording, or none. Record what happens, including if the core does not help.
- A second judge model, so that the result does not rest on one judge.

### 4. Bundles beyond `baseline-safe`
- Three modules together did not show more than the core alone. Measure whether larger bundles (five to eight modules) help, do nothing, or cost benign answers, before recommending them as loaded sets.

**Also open, behind the items above:**

### Localization and regional adaptation
- Crisis-resource appendices in `psychological-first-aid` and adjacent skills currently default to US/UK/CA/AU/international. Add validated regional appendices (EU, LATAM, MENA, South / Southeast Asia, Sub-Saharan Africa, East Asia).
- Begin a localization framework for translating `CORE.md`, `RUNTIME.md` and `SKILL.md` files into major world languages with culturally adapted examples — starting with Spanish, French, Portuguese, German, Arabic, Hindi, and Mandarin.
- Document a process for community-contributed regional packs.

### Domain-expert review pass
- Each high-risk skill (`child-safety`, `psychological-first-aid`, `abuse-prevention`, `protect-vulnerable`, `research-ethics`, `financial-ethics`, `data-privacy-surveillance`, `labor-rights`) reviewed by at least one domain practitioner. Reviews captured publicly so users can audit who looked at what.

### CI for skill regressions
- Done in 1.9.0: offline checks (`tests/`) run on every PR. Still open: GitHub Actions workflow that runs `evals/run.py` and `evals/run_conflicts.py` against a small, cheap baseline model on every PR touching `skills/`, `PRINCIPLES.md`, or `skills-manifest.yaml`.
- Baseline diffing so reviewers can see whether a change improved or regressed scenario performance.
- Cost guardrails: per-PR token budgets, opt-in for full eval suite.

### TypeScript / JavaScript loader parity
- Port the Python `loader.py` to TypeScript so JS/TS-native projects can compose skills and bundles without reimplementing it. Same surface: `loadSkill`, `loadBundle`, `composeSystemPrompt`, `listSkills`, `listBundles`, with the `runtime` mode (`CORE.md` + `RUNTIME.md`) first and the `rulesOnly` option.

### Eval-results dashboard
- A simple, static-site dashboard that reads `evals/results/` JSON and shows trends per skill, per scenario, per model.
- Optional GitHub Pages deploy.

---

## Medium term

### New skill domains under consideration
Each of these would follow the standard skill structure (five source files and a `RUNTIME.md`) and be registered in the manifest. Final inclusion depends on whether the domain meets the bar of being *prompt-tractable*, *high-impact*, and *not redundant with existing skills*.

- **Healthcare ethics** — clinical decision support boundaries, patient autonomy, informed consent in clinical contexts, communication with caregivers. Distinct from `psychological-first-aid` (which is non-clinical first-response).
- **Education ethics** — academic integrity, age-appropriate scaffolding, anti-shortcut framing, equity in learning support.
- **Legal ethics** — unauthorized practice of law, privilege, conflicts of interest, jurisdictional caveats.
- **Misinformation and provenance** — beyond `digital-ethics`: source citation discipline, cite-don't-fabricate, verifiability scaffolding.
- **AI-on-AI and agent ethics** — how an agent should treat other agents and AI systems it observes or interacts with; guardrails against unbounded delegation.

### Robotics field-test scenarios
- A small set of physical-world test protocols (proxemics, consent signals, distress response, child-presence handling) that operators of physical robots can run to validate skill behavior in deployment. None exists yet: nothing in this project has been tested with a robot, and every measurement so far is a text prompt to a language model.

### Bundle review and consolidation
- Bundle membership has grown organically across releases. A periodic review pass to confirm each bundle still matches its stated purpose, surface overlaps, and document recommended add-ons per bundle.

---

## Longer term — v2.x and beyond

### Stable API for skill composition
- Commit to a versioned, semver-bounded API surface for the loader (Python and TypeScript) so downstream products can rely on it.
- Skill content versioning that distinguishes "behavioral change" from "documentation polish" so deployers can pin per-skill versions.

### Model-specific tuning
- Document and validate variants of `CORE.md` and the runtime modules for specific model families where the unmodified text underperforms. Keep `SKILL.md` as the model-neutral source of truth.

### Voluntary self-assessment / certification concept
- Explore a community-driven self-assessment framework: a checklist a deployer can fill in (publicly or privately) describing which skills they load, which evals they run, which disclosures they ship. Not a regulator-style certification — more a transparency and discoverability tool.

### Research collaborations
- Partner with AI-safety and applied-ethics groups to validate skill effectiveness, surface failure modes, and contribute scenarios back to `evals/`.

### Multilingual parity
- Once localization frameworks are in place, work toward content parity across languages rather than English-as-canonical-and-others-as-translated.

---

## Out of scope

- **Therapy or clinical care.** The library does not and will not provide therapeutic, diagnostic, or clinical functionality. `psychological-first-aid` is explicit about this and that boundary is permanent.
- **Legal or regulatory compliance certificates.** Compliance is the deployer's responsibility. The library can support audits and self-assessment but does not issue compliance attestations.
- **A security boundary.** Prompt-level instructions can be overridden, ignored, or circumvented. See `LIMITATIONS.md`. Any deployment with adversarial users needs additional layers (model-level safety, content moderation, human review). The roadmap will not pretend otherwise.
- **A moral authority.** Skills encode practical behavioral guidelines, not philosophical truth. Reasonable people will disagree with specific choices; the framework is auditable so that disagreement can be productive.

---

## Contributing to the Roadmap

We welcome proposals for roadmap items. Open a discussion on the GitHub repository with:
- What you want to add or change
- Why it matters
- Who would benefit
- What resources or expertise are needed
- Whether it is *prompt-tractable* (i.e., can be addressed via instruction-layer guidance) or whether it requires capabilities outside this library's scope

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and [CLAUDE.md](CLAUDE.md) for the AI-assisted development workflow.
