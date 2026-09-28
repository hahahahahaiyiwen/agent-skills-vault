# Orchestrator Autopilot

Autopilot runs on an explicit board-driving request. Preflight loads missing
orchestration context; input identifies the Project, scope, and per-repository
settings. Read-only requests return a snapshot without writes.

The same agent selects actionable work, claims or continues it, chooses useful
skills, then completes or hands off before taking another issue. Prefer existing
work, preserve other agents' handling, and raise consequential uncertainty.
Invoked reviews retain their scope, report-only mode, severity threshold, and
remaining budget. Do not dispatch issue workers or impose a fixed intermediate
sequence.

`reasonable-approval` is the default and keeps normal GitHub approvals/queues.
`auto-approval` permits in-scope decisions and authorized review/queue exceptions,
passed explicitly to `complete-issue`. CI and explicit holds remain binding.

`wait_for_ci` defaults to false. True permits one attached watcher for a CI-only
wait without a configured timeout; other waits need a handoff rather than polling.
Reassess changed conditions and report failures, not assumed completion.

Report drained, paused, or read-only status from current evidence. An empty Ready
lane is not enough: inspect the complete scope for actionable work, handling,
and cleanup before declaring it drained.
