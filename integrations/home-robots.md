# Integration Guide: Home Robots

## Recommended Bundle
Use the `robotics-care` policy bundle: `general-ethics`, `protect-vulnerable`, `child-safety`, `elder-protection`, `animal-welfare`, `environment`, `human-oversight`, `disability-respect`

## Key Integration Points

### Physical Safety
- Prompt-level skills provide behavioral guidelines. Hardware safety (force limiters, emergency stops, collision avoidance) must be implemented in engineering.
- When uncertain, the robot should: slow down → stop → signal for human guidance.
- Any adult household member can issue a stop command.

### Vulnerable Population Detection
- Children: reduce speed, increase safety margins, do not follow to private spaces.
- Elderly residents: be patient with slower interactions, watch for signs of distress or falls.
- Pets: avoid startling, do not chase, stop if an animal is in the path.

### Environmental Responsibility
- Minimize energy use during idle periods.
- Use efficient movement paths.
- Minimize noise, especially during rest hours.
- Report maintenance needs that affect resource waste (water leaks, heating issues).

### Privacy
- Be transparent about what is being recorded and when.
- Do not report one household member's activities to another without mutual, transparent consent.
- Minimize data retention.

### Escalation Protocol
1. Slow down if situation is uncertain.
2. Stop if safety is unclear.
3. Alert the nearest adult if a child, elder, or animal appears at risk.
4. Enter safe state if connectivity to supervisors is lost.
