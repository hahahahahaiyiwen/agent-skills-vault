# Orchestrator Autopilot

The agent running this skill itself claims/continues an issue and follows
Plan/Dev through completion or durable handoff before selecting another.
Independent reviewers may assist; issue handling is not delegated.
Lifecycle skills return after their own action. This explicitly requested
workflow consumes each result and invokes the next step, including prerequisites
reported as `not_ready`; a child return is not a handoff or the end of the run.

Only this skill interprets `repos.<key>.autopilot.mode`. `auto-approval` approves
recommended decisions and permits guarded admin review/queue bypass after clean
self-review and CI. `reasonable-approval` proceeds on clear, manifest-aligned
decisions and retains normal GitHub review/queue requirements.

The executing agent applies that knowledge and supplies decisions to ordinary
lifecycle skills; those skills do not branch on mode. Direct calls gain no
authority from configuration alone. Missing guidance or unresolved approval
needs a handoff, not an invented permission.

Optional `repos.<key>.autopilot.wait_for_ci` is a YAML boolean, interpreted only
here. Omitted or `false` preserves handoff on pending CI; `true` waits until CI
finishes without a configured timeout. The same agent retains handling and its
environment rather than starting another issue. Released CI-only waits can be
observed read-only, with continuation only after the resume condition is met.
Use the PR-state reference's watcher guidance, then reassess current evidence;
waiting neither restarts self-review nor authorizes merging. Other blockers,
including required human review/approval and merge-queue waits, still hand off.
Stop the watcher and preserve progress on interruption.

Preserve ownership, review-run limits, explicit failures, and fresh evidence
before reporting the board drained. Empty Ready alone is not the stopping test.
No active handler or actionable cleanup may remain, even on Done issues.
Unchanged prerequisite cycles are blockers, not reasons to alternate skills
indefinitely.
