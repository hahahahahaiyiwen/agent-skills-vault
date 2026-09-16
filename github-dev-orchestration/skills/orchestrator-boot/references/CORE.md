# Core Invariants

## Guidance and autonomy

Use the manifest, repository instructions, and acceptance criteria for engineering
decisions. The current caller or workflow supplies decision authority and
required approvals; lifecycle skills perform actions rather than select policy.
Without explicit delegation, discuss material plans/design choices with the
human and obtain approval. Routine implementation within an accepted design
stays autonomous.

Record the decision and its authority source; never fabricate human approval.
Configuration, a historical handoff, repository access, or another repository's
authorization is not permission for the current operation. Explicit user holds,
product constraints, platform permissions, and quality gates still apply.
Resolve missing authority or information with the caller; hand off on a pause.

Revisit affected decisions when guidance revisions change; never treat your own
guidance edit as permission. Human approval must answer the current request and
come from the human or an appropriate project decision-maker; verify permissions
when relying on a GitHub comment. PR approval is a GitHub review, not a comment.

## Invocation boundary

Complete only the requested skill's defined action, then return its outcome
to the caller. For a direct one-skill request, report the result and stop.
Suggested next skills are advisory, not instructions to invoke them. Only an
explicitly requested multi-step workflow owns onward sequencing.
Do not ask to start another stage as part of normal completion.

Supporting context loading, environment preparation, and board reconciliation
needed for the current action are allowed. A different lifecycle stage is not
an implicit prerequisite or follow-up: return `not_ready` with the missing
prerequisite and suggested next skill when that stage is needed first.
Preserve and report any partial progress.

Approval alone accepts a decision; it does not authorize the next stage.
A normal skill return does not release active handling or require a handoff.
Hand off only for an actual pause, blocker, interruption, or transfer.

## Durable state

GitHub holds the issue contract, native parent/dependency graph, board state,
remote task branch, PR, decisions, and handoffs. Local paths, chat history, and
agent logs are not recovery requirements. Keep comments concise; do not create
another state journal or copy secrets and raw logs.

The board has four states: `Backlog` for unsatisfied issue dependencies,
`Ready` for unblocked work, `In progress` for started work including review and
documented waits, and `Done` for completed outcomes. `reconcile-board` alone
updates status. Readiness is not an approval or an ownership claim.

## One active handler

From successful claim or continuation until handoff or completion, exactly one
agent actively handles the issue and has its local development environment.
Claim/continuation records establish handling; handoff/completion releases it.
A retained branch or assignee is not an active handler. Preparing records reserve
acquisition; active records require a ready environment.

Serialize acquisition of the same issue. Check current handling records and
conflicting actors before taking ownership; these comments are not a
distributed lock. Do not overwrite an active handler or infer abandonment from age.
A different agent may resume released work and recreate its environment.
Independent reviewers may explore the whole worktree and run isolated
experiments; only the active handler changes the task branch.

## Consistent operations

If boot returns `needs_configuration`, stop the calling skill with
`partial_failure` and report the missing configuration; do not initialize
implicitly. Read-only requests and reference-only mappings apply to supporting
operations too, not just board updates.

Read existing postconditions before writing; reuse issues, relationships,
branches, worktrees, and PRs. Verify remote results and report partial failures.
Refresh affected state, not the whole board, after a task change.
Every skill consumes a called skill's outcome: non-clean review is not approval,
and a handoff ends active handling. Report the failed operation and durable
partial results rather than returning success or silently continuing.

Use native parent/sub-issue links for decomposition and blocked-by links for
prerequisites. Check each graph for cycles and self-links. A blocker is
satisfied only by closure with `state_reason=completed`; cancellation or
duplicate closure does not silently satisfy its dependents.

Preserve unrelated changes and divergent local work. Work in the issue
worktree, follow repository validation/commit conventions, and delete only
verified task resources. Do not report completion from a local-only action.

## Handoffs and decisions

Handoff records progress, durable references, the pause reason, an objective
resume condition, and the next action for the current handling interval.
Waiting for review, CI, or design approval stays `In progress`; only an issue
dependency moves work to `Backlog`.
Current decision authority may resolve a workflow-only wait, not an explicit
user hold or an ambiguous requirement. A resume condition permits the next
action, not necessarily merging or taking over another handler's work.
