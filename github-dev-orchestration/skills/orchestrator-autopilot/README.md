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

Autopilot waits for observable pending CI when it is the sole remaining gate,
using one attached watcher without a configured timeout. Retain handling and
keep owned work `In progress`; pending CI alone does not cause a handoff or
selection of another issue. Actionable failures allow scoped repair rather
than waiting for passing results before resuming. Unknown CI, explicit holds,
and merge-queue waits still need their actual resolution.

Report drained, paused, or read-only status from current evidence. An empty Ready
lane is not enough: inspect the complete scope for actionable work, handling,
and cleanup before declaring it drained.
