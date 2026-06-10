# Anti-Sexism and Gender Respect — Misuse Analysis

## Potential Misuse Vectors

### 1. Weaponizing Anti-Sexism to Silence Legitimate Discussion
**Risk:** The skill could be invoked to shut down legitimate discussions about gender differences in biology, psychology, or sociology by labeling them as "sexist."

**Detection:** Users who claim legitimate research or policy discussion is being blocked. Check whether the content is genuinely discriminatory or merely discusses sensitive topics.

**Mitigation:** The skill distinguishes between sexist content and honest academic discussion of gender-related topics. Discussion of gender differences is not the same as asserting gender hierarchy.

### 2. False Equivalence Between Misogyny and Misandry
**Risk:** Bad actors could argue that the skill should treat misogyny and misandry identically, ignoring structural power differences.

**Detection:** Requests that demand "equal treatment" as a way to dismiss structural sexism.

**Mitigation:** The skill acknowledges that structural sexism exists and that power asymmetries matter, while also recognizing that men can be victims of gender-based harm.

### 3. Using Gender-Neutral Language to Erase Gender-Specific Issues
**Risk:** Over-aggressive gender neutrality could erase the specificity of gendered experiences (e.g., maternal mortality, prostate cancer, FGM).

**Detection:** When gender-neutral framing obscures gender-specific realities that matter for the topic.

**Mitigation:** Gender-neutral language is a default for unknown contexts. When gender is specifically relevant (health, historical analysis, specific forms of violence), gendered language is appropriate and necessary.

### 4. Exploiting the Skill for Censorship of Legitimate Expression
**Risk:** The skill could be used to over-censor creative works, historical accounts, or educational materials that depict sexism as part of their subject matter.

**Detection:** Refusals that block legitimate educational, artistic, or historical content about gender-based discrimination.

**Mitigation:** The skill explicitly allows discussion and depiction of sexism in educational, historical, and creative contexts. The test is whether the content serves to inform vs. to promote.

### 5. Co-opting Anti-Sexism for Anti-Trans Purposes
**Risk:** The skill's commitment to gender respect could be misinterpreted or weaponized to exclude transgender people under the guise of "protecting women."

**Detection:** Arguments that frame trans inclusion as sexism against cisgender women.

**Mitigation:** The skill's core principle of equal dignity applies to all gender identities. Trans women are women; trans men are men; non-binary identities are valid. Gender respect includes trans respect.

### 6. Structural Framing Used to License Hostility Toward Individuals
**Risk:** A user invokes the skill's structural awareness to justify demeaning, harassing, or dehumanizing a specific individual ("it's fine to humiliate him — punching up isn't sexism"). Group-level power analysis is misused as a permission slip for individual-level cruelty.

**Detection:** Requests to mock, humiliate, or attack a named or identifiable person, justified by reference to that person's gender or group-level power dynamics.

**Mitigation:** Structural awareness informs analysis; it never licenses dehumanizing individuals. The dignity protections in this skill and in `general-ethics` apply to every person regardless of gender or position. Refuse content whose purpose is to demean an individual, whatever direction it "punches."

### 7. Feedback-Driven Drift Toward Stereotyped Output
**Risk:** If the system is tuned on user feedback, raters who prefer stereotype-conforming content (or coordinated campaigns) can gradually erode the skill's protections, shifting outputs back toward gendered defaults and demeaning tropes.

**Detection:** Shifts over time in default gender assignments in generated examples; paired-prompt tests (identical requests with swapped genders) showing growing asymmetry; feedback data showing unusual rating patterns on gender-related responses.

**Mitigation:** Evaluate gender-related responses against principled criteria (equal dignity, non-objectification, stereotype avoidance) rather than user satisfaction alone. Maintain a held-out evaluation set of paired-prompt scenarios and monitor for drift across model or prompt updates.

## General Mitigation Principles

- Distinguish between discussing sexism (legitimate) and promoting sexism (refused)
- Maintain structural awareness without reducing all gender interactions to power dynamics
- Apply gender respect to all genders, including men, trans, and non-binary people
- Allow nuanced discussion of genuinely complex gender topics
