# Complete Issue

Completion owns integration, issue closure, safe local/remote cleanup, and
dependent reconciliation. Keep merge evidence separate from queue entry and
partial cleanup. Preserve exact-head merge/deletion checks, non-code completion,
cross-agent cleanup boundaries, and idempotent recovery after an existing merge.
Verify caller-authorized merge exceptions for the PR repository; CI and
non-bypassed requirements remain mandatory. Configuration or history alone
does not authorize bypass.

If a gate becomes pending before merge, return `waiting` without releasing
handling only when the caller explicitly manages that wait; otherwise hand off.
Queue entry still requires a merge-queue handoff, not a completion claim.
Assess entry requirements before queue-only checks, and choose queue entry or
direct merge once, not both. Verified no-PR outcomes skip PR gates entirely.
