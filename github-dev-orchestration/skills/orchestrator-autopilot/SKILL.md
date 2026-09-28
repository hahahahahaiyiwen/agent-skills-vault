---
name: orchestrator-autopilot
description: Drive GitHub issue delivery from a Project, one issue at a time.
---

# Orchestrator Autopilot

## When to use

Only on an explicit request to drive board work. The same agent handles one
issue at a time; do not delegate issue delivery.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The configured GitHub Project and requested scope. A read-only request returns
a snapshot without claims or writes.

Use optional `repos.<key>.autopilot` for the operation's repository, including
the PR repository. `mode` is `reasonable-approval` (default), following
request/manifest delegation and normal GitHub approvals/queues, with no admin
bypass. `auto-approval` permits in-scope decisions and authorized review/queue
exceptions during this explicit run.

Reject unsupported modes or invalid settings. Neither mode waives CI or explicit
holds. Never fabricate human approval.

## Guidance

- Read all pages of the requested board scope using
  `..\reconcile-board\references\PROJECT.md`. Prefer existing actionable work,
  including PR repairs and cleanup. Use `claim-issue` for new unblocked work or
  `continue-issue` for existing work; do not take over another handling agent.
- Choose the next useful action from issue and project guidance, not a fixed
  sequence. Design and self-review are optional unless required. Raise
  consequential uncertainty; honor any review's scope, report-only mode,
  threshold, and remaining budget.
- For observable pending CI as the sole remaining gate, use one attached CI
  watcher without a configured timeout; retain owned handling and keep owned
  work `In progress`. Do not hand off or select another issue for a CI-only wait.
  Observe released work read-only. Stop and reassess on completion, failure,
  interruption, or changed head/base; actionable failures return to scoped
  repair. Unknown CI and merge-queue waits need their actual resolution, not a
  CI watcher. Waiting grants no merge permission.
- Finish through `complete-issue` or `handoff-issue` before selecting another issue.
  For a permitted exception, pass an explicit admin-bypass request to
  `complete-issue`. Refresh affected facts; stop on uncertain ownership or failed
  persistence, and do not repeat actions for unchanged waits.

## Output

Report completed issues, waits, decisions, and failed/partial updates. Distinguish
drained, paused, and read-only snapshot. Drained requires a fresh, complete view
with no actionable work, active/preparing handling agent, or actionable cleanup.
An empty Ready lane, unknown state, or incomplete reads cannot establish it.
On interruption, hand off owned work where possible and report anything unsaved.
