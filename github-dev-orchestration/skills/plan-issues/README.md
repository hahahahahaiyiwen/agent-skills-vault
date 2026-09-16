# Plan Issues

One entry point owns initial planning and graph revision. It creates or
revises native relationships and issue contracts; reconciliation owns status.
The graph API reference is loaded only for graph operations. Preserve
idempotency, evidence-based revision, cross-repository identities, and the
distinction between hierarchy and prerequisites.
Unresolved planning without an owned handling interval returns `needs_decision`,
not a fabricated handoff or successful plan. Keep the proposal on an existing
issue when available; do not create an issue just to host a wait.
