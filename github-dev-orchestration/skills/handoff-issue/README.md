# Handoff Issue

Handoff persists enough state for a different agent to continue and releases
active handling only after that record is durable. It is not a board lane or
an approval. Preserve precise resume conditions, remote progress verification,
explicit local-only limitations, and write-before-reconcile ordering.
Normal skill return or design approval is not an automatic handoff.
Bind the record to its handler/acquisition; reuse it only within the same
handling interval, never to release a later acquisition.
