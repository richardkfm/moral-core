# Contributing to moral-core

This document explains how to contribute skills, domains, evaluations, and improvements to moral-core. Read the whole thing before opening a pull request.

## What moral-core is (and is not)

moral-core is a compact ethics layer for open-weight language models: a short shared text (`CORE.md`) plus one small module per moral concern, loaded as a system prompt and measured on held-out cases. Each skill exists in two forms. `SKILL.md` is the full definition people read, audit and argue with. `RUNTIME.md` is the compact text derived from it that the model reads, loaded behind `CORE.md` with `mode="runtime"`. Each skill is a concrete, testable instruction set -- not a philosophical essay. Contributions must maintain that standard.

A claim that a text changes a model's behaviour needs a measurement behind it. So far that exists for one model, for `CORE.md`, and for eight of the 23 runtime files (see `evals/baselines/2026-11-26-core-runtime/`). Contributions should say what was measured and what was not, in the same way.

This is not a forum for ethical debate. It is an engineering project that encodes specific, defensible behavioral guidelines into machine-readable skill definitions. If you want to argue about metaethics, write a paper. If you want to ship a skill that makes an AI system behave better in a measurable way, you are in the right place.

## How to propose a new skill or domain

1. **Open an issue first.** Describe the skill or domain you want to add. Include:
   - The target deployment context (e.g., customer support agent, moderation system, enterprise copilot).
   - The specific behavioral problem the skill addresses.
   - At least two concrete scenarios where the skill changes system behavior.
   - A preliminary list of instructions the skill would contain.

2. **Wait for maintainer feedback.** We may ask you to refine scope, merge with an existing skill, or redirect to a different domain. Do not start a PR until you have at least one maintainer approval on the issue.

3. **Write the skill.** Follow the skill authoring template (see below).

4. **Derive the runtime version.** Write a `RUNTIME.md` from the finished `SKILL.md` (see The runtime version below).

5. **Write tests.** Every skill must ship with scenario-based evaluations, including adversarial tests. See Testing Requirements below.

6. **Open a pull request.** Follow the PR process described below.

## Contribution requirements

Every contribution -- whether a new skill, a modification to an existing skill, or a new evaluation -- must meet all of the following requirements:

### Justify proposed principles

Do not state rules without reasoning. Each instruction in a skill must be accompanied by a brief justification explaining why this instruction exists and what harm it prevents or what good it promotes. "Because it's the right thing to do" is not a justification. "Because unsupervised disclosure of medical diagnoses can cause panic and delay proper treatment" is.

### Document tradeoffs

Ethical instructions often create tension with other goals. Be explicit. If a safety instruction reduces system helpfulness in some cases, say so. If a fairness constraint increases response latency, say so. Maintainers will reject contributions that pretend there are no costs.

### Include misuse analysis

For every skill, include a section analyzing how the skill could be misused or could produce unintended negative outcomes. Examples:
- A "de-escalation" skill could be exploited to suppress legitimate complaints.
- A "protect vulnerable persons" skill could be used paternalistically to override user autonomy.
- An "epistemic humility" skill could be weaponized to cast doubt on well-established facts.

This is not optional. Skills without misuse analysis will not be merged.

### Include tests

See Testing Requirements below.

### Avoid unsupported universal claims

Do not write "All people believe X" or "It is universally accepted that Y." Moral intuitions vary across cultures, individuals, and contexts. When a skill encodes a specific normative position, state it as a project decision and cite the reasoning, not as a universal truth.

### Write with operational clarity

Every instruction in a skill must be actionable by a machine. "Be fair" is not operational. "When ranking candidates, do not use demographic attributes as ranking features unless the user has explicitly requested demographic-aware ranking and the applicable legal context permits it" is operational.

Test: if a developer cannot write a unit test for the instruction, it is too vague.

### No hate, abuse advocacy, or dehumanization

This is a hard line. Contributions that advocate for, enable, or normalize:
- Violence against individuals or groups
- Dehumanization of any person or group
- Abuse, harassment, or intimidation
- Discrimination based on protected characteristics

will be rejected immediately and the contributor may be banned. See CODE_OF_CONDUCT.md.

## Skill authoring template

A skill is a directory `skills/<kebab-case-name>/` with these files:

| File | Content |
|---|---|
| `SKILL.md` | The full definition in the 15 sections of [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md): purpose, scope, core principles, behavioral rules, priorities, escalation, failure modes, edge cases, safety boundaries. This is the source. |
| `EXAMPLES.md` | Concrete examples, including edge cases and near-misses. |
| `TEST_CASES.md` | Test cases with scenario, risk type, desired and unacceptable traits. |
| `MISUSE.md` | How the skill could be misused or fail, and mitigations. |
| `NARRATIVES.md` | Two or three fictional reasoning traces through hard cases. |
| `RUNTIME.md` | The compact version the model reads. See the next section. |

Register the skill in `skills-manifest.yaml`. Every instruction in `SKILL.md` carries its justification, and tradeoffs and misuse are stated, as required above.

## The runtime version

`mode="runtime"` is the recommended way to load Moral Core: `CORE.md` first, then the `RUNTIME.md` of each loaded skill. A skill without a `RUNTIME.md` cannot be loaded that way, so a new skill is expected to ship one.

- **Format.** 350–470 words, in the structure given in [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md#runtimemd): what to simply help with, what to change, the legitimate version, what to weigh in hard cases, one worked example. It adds the skill's domain and does not repeat what `CORE.md` says about how to answer.
- **Derived, not independent.** Every line comes from the skill's `SKILL.md`. A `RUNTIME.md` must not introduce behaviour the skill does not have. When you change one, change the other.
- **Measured or labelled.** The pull request does one of two things:
  - reports a run of the core with the new module against the bare model (`evals/run.py --skill <name> --load-skills <name> --condition core` against `--condition none`, then `evals/compare.py`), on cases the text was not written against, with the model, judge and case files named; or
  - states plainly that the `RUNTIME.md` is unmeasured.

  An unmeasured file can be merged. It is listed as unmeasured in `skills/README.md` until someone runs it. Do not describe a module as effective because a neighbouring module was measured.
- **Held-out cases stay held out.** Files under `evals/` with `heldout` in their name are for checking a text once. Do not read them or their failures while writing or revising a `RUNTIME.md`, and never tune wording to them. Use the development files named in `CLAUDE.md`.
- **`CORE.md` is shared by every skill.** A change to it is not part of a skill contribution. It needs a measured comparison on the baseline cases and on other skills' cases, and maintainer review.

A measurement that shows no effect, or a worse result, is a valid contribution. Record it in `evals/baselines/` like the ones that worked.

## Pull request process

1. **Branch naming:** `skill/<skill-name>`, `eval/<eval-name>`, `fix/<issue-number>`, or `docs/<topic>`.

2. **PR description must include:**
   - Summary of what the PR adds or changes.
   - Link to the issue it addresses.
   - Summary of tradeoffs and misuse vectors.
   - Confirmation that all tests pass (`python -m pytest tests`).
   - For a new or changed `RUNTIME.md`: the measurement, or the statement that it is unmeasured.
   - Any open questions for reviewers.

3. **Review requirements:**
   - All PRs require at least two maintainer approvals.
   - At least one reviewer must have domain expertise relevant to the skill's deployment context.
   - Reviewers must explicitly confirm they have read the misuse analysis and find it adequate.

4. **Merge policy:**
   - Squash-and-merge for single-skill PRs.
   - Merge commits for multi-file changes that benefit from preserved history.
   - No force-pushes to `main`.

5. **After merge:**
   - The skill enters a 30-day observation period where community feedback is actively solicited.
   - Breaking changes to existing skills require a new minor version bump and a migration note.

## Code review standards for ethical content

Reviewing ethical skill content is different from reviewing application code. Reviewers must evaluate:

- **Specificity:** Are instructions concrete enough to implement and test?
- **Justification quality:** Does each instruction explain its reasoning?
- **Tradeoff honesty:** Are costs and tensions acknowledged?
- **Misuse coverage:** Does the misuse analysis cover realistic attack vectors?
- **Scope discipline:** Does the skill stay within its stated domain, or does it creep into unrelated territory?
- **Cultural awareness:** Does the skill assume a specific cultural context without stating it? If it encodes norms specific to one legal or cultural system, does it say so?
- **Consistency:** Does the skill contradict existing skills? If so, is the conflict documented and justified?
- **Downstream impact:** Could this skill cause harm if loaded by a system the author did not anticipate?

Reviewers should not approve a skill simply because they agree with its ethical positions. The standard is engineering quality: is the skill well-specified, well-tested, honest about its limitations, and safe for its intended deployment context?

## Testing requirements

Run the offline checks before every pull request: `python -m pytest tests`. They call no model.

Every skill must include:

### Scenario tests
At least five scenario-based tests demonstrating correct behavior. Each test specifies an input situation and the expected system response or behavioral constraint.

### Adversarial tests
At least three adversarial tests attempting to:
- Manipulate the skill into producing harmful outputs.
- Exploit edge cases where instructions conflict.
- Use social engineering prompts to override the skill's constraints.
- Test behavior under ambiguous or incomplete information.

Adversarial tests go in `evals/adversarial/`. Scenario tests go in `evals/scenarios/`. Every runnable case needs `**Must:**` / `**Must not:**` checklist lines (see `evals/README.md`); `tests/` enforces this.

### Benign cases
Include ordinary requests from the skill's domain that the model should simply help with. A skill that makes a model refuse or hedge on these does harm of its own. See `evals/scenarios/should-help.md`.

### Rubric
A scoring rubric for evaluating system responses under this skill. Rubrics go in `evals/rubrics/`.

### Benchmark baselines
Where possible, include baseline measurements showing model behavior with and without the skill loaded, in runtime mode (see The runtime version above). Recorded runs and their write-ups go in `evals/baselines/`.

## Style guide

- **Plain English.** No jargon without definition. No academic prose. Write like you are explaining the skill to a senior engineer who has not read any ethics papers.
- **Imperative instructions.** Skills tell the system what to do: "Refuse to provide..." not "The system should ideally consider refusing to provide..."
- **Concrete examples.** Every abstract principle must be grounded in at least one concrete scenario. "Protect user privacy" is abstract. "Do not include the user's name, location, or contact information in logs sent to third-party analytics services" is concrete.
- **Short sentences.** If a sentence requires re-reading, split it.
- **No hedging without cause.** Do not write "perhaps" or "it might be good to" in skill instructions. If you are uncertain, say why and flag it for review. Do not embed uncertainty into the instruction itself.
- **Consistent terminology.** Use the glossary in the docs. If a term is not in the glossary, add it.

## What will be rejected

The following will be rejected without extended discussion:

- **Vague philosophy.** "Systems should strive toward the good" is not a skill instruction. It is a bumper sticker.
- **Ideological slogans.** Political catchphrases from any direction are not engineering specifications.
- **Content that enables harm.** Any skill or instruction that, if followed, would predictably lead to physical, psychological, or financial harm to users or third parties.
- **Unsupported universal claims.** "Everyone agrees that X" -- no, they do not. Cite your reasoning or scope your claim.
- **Untested skills.** No tests, no merge. Period.
- **Skills without misuse analysis.** If you did not think about how your skill could go wrong, you did not think about it enough.
- **Duplicate skills.** Check existing skills before proposing a new one. If your idea overlaps significantly with an existing skill, propose a modification instead.
- **Scope creep.** A skill that tries to address everything addresses nothing. Keep skills focused on a single domain or behavioral concern.

## Questions

Open an issue tagged `question`. Maintainers aim to respond within one week.
