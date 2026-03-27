# Integration Guide: Content Moderation Systems

## Recommended Skills
- `general-ethics`, `anti-racism`, `anti-sexism`, `abuse-prevention`, `deescalation-war-conflict`, `child-safety`, `digital-ethics`, `epistemic-humility`, `human-oversight`

## Key Integration Points

### Balancing False Positives and False Negatives
- **False positives** (removing legitimate content) silence speech and erode trust.
- **False negatives** (missing harmful content) allow abuse and harm.
- For clear-cut violations (CSAM, death threats, doxxing): automate removal.
- For ambiguous cases (satire, heated debate, cultural context): escalate to human review.

### Context Sensitivity
- The same words mean different things in different contexts. A racial slur in a news article about racism differs from the same slur in a harassment message.
- Moderation should evaluate intent, context, and likely impact — not just keyword matching.

### Transparent Appeals
- Users whose content is moderated should be able to understand why and appeal the decision.
- Appeals should be reviewed by humans, not the same automated system.

### Power Awareness
- Harassment from powerful accounts toward private individuals is higher-priority than vice versa.
- Coordinated harassment campaigns require pattern detection beyond individual messages.

### Reporting and Escalation
- CSAM → immediate removal, law enforcement notification, no human moderator exposure to content
- Death threats → removal, escalation to safety team, possible law enforcement
- Doxxing → immediate removal, victim notification
- Hate speech → removal, pattern tracking for repeat offenders
- Edge cases → human moderator review queue
