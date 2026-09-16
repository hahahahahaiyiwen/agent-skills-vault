# Plan and Dev Cycles

This guide describes the workflow behind the principles in
[README.md](README.md). Twelve active skills implement the Plan/Dev lifecycle.
`orchestrator-autopilot` coordinates them, making thirteen active skills.

## Two connected cycles

```text
Plan:
  goal or development discovery -> high-level design
    -> plan-issues: create or revise the issue graph
    -> reconcile-board

Dev:
  claim-issue -> design-issue -> implement-issue -> self-review
    -> open-pr -> iterate-pr -> complete-issue
```

Planning shapes outcomes, shared design, work breakdown, and dependencies.
Development delivers one issue's accepted outcome. Ready work need not have
every implementation detail designed; issue-level design belongs inside Dev.

Existing work enters through `continue-issue`, which restores its environment
and suggests its next unfinished step rather than claiming it again.
Both cycles use the project manifest for direction. These are activities, not
mandatory documents; scale design effort to the work. The calling workflow
determines required approvals; individual skills remain mode-agnostic.

The durable plan is the issue graph and board. Design notes may explain
architecture and rationale, but do not create a second execution plan.

### Individual invocations and workflow sequencing

A direct skill invocation performs that action, returns its outcome and
suggested next skill, and stops. Routing arrows are advisory, not instructions
for a leaf skill to invoke its successor.

```text
/claim-issue     -> claimed -> stop
/design-issue    -> brief -> approval -> ready_to_implement -> stop
/implement-issue -> ready_for_review -> stop
```

Context loading, environment preparation, and reconciliation needed for the
requested action remain allowed. A different lifecycle stage is not an implicit
prerequisite: return `not_ready` with the missing prerequisite and suggestion.
Only an explicitly requested multi-step workflow, such as autopilot, decides
and invokes the next stage after each result.

Before human design approval, include the goal, approach, affected areas,
tradeoffs/risks, and scope boundaries in the approval message. A link alone is
insufficient. Ask only to approve or revise the design, not to implement or
hand off. Re-brief material revisions before approval; approval alone does not
expand execution scope.

A normal skill return retains the current handling interval and environment.
It is not a handoff; release handling only for an actual pause, blocker,
interruption, transfer, or completion.

### Returning to planning

Design, implementation, or review may reveal that the issue graph must change.

| Discovery | Response |
|---|---|
| A different implementation approach within the same outcome | Adjust the issue-level design and continue Dev. |
| An independent improvement | Create or revise a follow-up issue without expanding the current issue. |
| A missing prerequisite | Add the dependency, preserve current work, and pause the blocked issue. |
| A shared design assumption or work breakdown is wrong | Revisit the relevant design and affected issues, then resume Dev. |

Returning to Plan does not itself require a handoff. Settle material decisions
under the caller's authority, record the revision, and continue if possible.
An individual skill suggests that planning step rather than invoking it.
Use `handoff-issue` when execution must pause or continue in another agent or context.
Planning without an owned handling interval instead returns `needs_decision`
when a required decision is unresolved. Preserve the proposal on an existing
issue when available; do not create a handoff-only issue.
Ordinary completion usually just reconciles and unblocks work; it does not
require another high-level planning pass.

## Skill responsibilities

Grouping describes purpose, not which cycle may call a skill. Load each skill
only when its action is needed.

| Group | Skill | Purpose |
|---|---|---|
| Plan | `plan-issues` | Turn goals or discoveries into high-level design and create or revise issues, acceptance criteria, parent links, and dependencies. |
| Plan | `reconcile-board` | Derive and repair board state from issue, dependency, claim, handoff, and PR facts; report what can proceed. |
| Dev | `claim-issue` | Start a Ready issue, create its remote task branch, prepare its local development environment, and record the active agent and claim. |
| Dev | `design-issue` | Produce just-enough design and resolve required decisions/approvals before implementation. |
| Dev | `implement-issue` | Implement the accepted outcome, update affected tests and documentation, verify the change, and push coherent progress. |
| Dev | `self-review` | Independently assess the solution using the whole worktree; report once or iterate within the project's limit, recording commit-bound evidence. |
| Dev | `open-pr` | Create or update one issue-linked PR and publish its scope, acceptance evidence, and review context. |
| Dev | `iterate-pr` | Inspect PR feedback and CI, address actionable problems, and route to further work, handoff, or completion. |
| Dev | `complete-issue` | Verify completion, merge the PR where applicable, close the issue as completed, safely clean task resources, and reconcile dependent work. |
| Shared | `handoff-issue` | Persist progress, the pause reason, resume condition, and next action; end the current agent's active handling without discarding work. |
| Shared | `continue-issue` | Verify resume conditions, restore or recreate the local environment, and return the next unfinished action to the caller. |
| Shared | `orchestrator-boot` | Initialize its bundled map on explicit first use; load the compact model and project guidance, then return without running lifecycle actions. |
| Shared | `orchestrator-autopilot` | The invoking agent handles Ready and resumable issues itself, sequentially through the lifecycle until none remains actionable. |

There is no separate `close-pr` skill for the normal flow: merging and closing
belong to `complete-issue`. Closing an unmerged PR is cancellation or
supersession, not completion or satisfaction of a dependency.

### First-use configuration

An explicit, non-read-only `orchestrator-boot` initializes its own bundled
`references\RESOURCE-MAP.yml` in place when the map is missing or incomplete.
There is no second workspace configuration file. Setup discovers existing
checkouts/remotes and Project metadata, asks for unresolved choices together,
then saves and re-reads valid YAML before finishing context loading.
It does not clone repositories, enumerate board items, or mutate GitHub.

Complete mappings stay unchanged unless reconfiguration is requested.
Implicit or read-only boot returns `needs_configuration` when setup is needed,
without initializing or starting another skill. Its caller stops with the
configuration problem rather than proceeding with placeholders. Setup details
are loaded only on that path. Skill settings are collected as data, not applied
as decision authority. Checkout/worktree paths retain boot's workspace-root anchor;
manifest paths remain repository-relative. Use separate installed skill copies
when workspaces need independent maps.

### Project-guided review

Design and implementation use the manifest selected by `repos.<key>.manifest`
in `RESOURCE-MAP.yml`; its path is relative to that repository. Small skill
options live beside it, under `repos.<key>.self_review`:

| Setting | Meaning |
|---|---|
| `mode: single_pass` | One independent review, reporting findings without automatic fixes. |
| `mode: until_clean` | Review, address findings, and review again; the default mode. |
| `max_iterations: 3` | Default maximum review passes per run, including verification; a positive integer. Single-pass mode always uses one pass. |

The reviewer can explore the entire worktree, architecture, and surrounding
behavior, not only changed lines. This is access to relevant context, not an
instruction to load the whole repository eagerly.

Self-review evidence belongs to exact code and guidance revisions and can be
recorded on the issue before a PR exists. Record the run, pinned settings, and
pass before review; started or interrupted passes count. Handoff/continuation
preserves the count. Final-pass findings trigger a handoff, not unreviewed
fixes. A later independent request can start a new run (for example, reviewing
new PR-feedback repairs); retrying exhausted work cannot.

Only clean review proceeds to submission/completion. PR review handles
submitted feedback, CI, and repository requirements; it need not repeat
unchanged self-review or introduce a universal human-approval gate.

## Board state

| State | Meaning |
|---|---|
| `Backlog` | One or more native issue dependencies remain unsatisfied. |
| `Ready` | Dependencies are satisfied, or absent; work can start or resume. |
| `In progress` | Claimed or continued work, including design, implementation, PR review, and documented waits. |
| `Done` | The issue's outcome is complete, its PR is merged where applicable, and the issue is closed as completed. |

Map these states to four distinct Project options; a shared Backlog/Ready
option would erase dependency readiness.

`reconcile-board` owns status updates. Other skills change task facts and
request reconciliation. Reuse recent results and refresh affected work when
facts change, rather than repeating full-board discovery at every step.

When every blocker is completed, move a dependent from `Backlog` to `Ready`.
Issues without blockers start Ready. Starting or resuming work moves it to
`In progress`. If a new issue dependency prevents progress, preserve the work,
hand it off, and reconcile it back to `Backlog`.

Waiting for design approval, external PR review, or CI alone stays
`In progress`. A handoff explains the wait when the handler steps away; an
agent observing CI may remain active. Review and handoff are not
additional board states. A retained branch means continuation, not a new claim,
when dependency-blocked work becomes Ready again.

## Single-agent execution invariant

**From successful `claim-issue` or `continue-issue` until `handoff-issue` or
`complete-issue`, an issue is actively handled by exactly one agent, and that
agent has the issue's local development environment.**

Claim or continuation establishes this condition; handoff or completion ends
active handling. Project status records lifecycle progress, not live agent
ownership: a handed-off issue can remain `In progress` with no active handler.
Independent review contexts may explore the worktree and experiment in
isolation; only the handler owns changes to the issue branch.

The environment consists of a repository checkout, an isolated issue worktree
on the task branch, and the repository-declared tools, dependencies, and
configuration needed for the work. Claim or continuation is not successful
until that environment is ready; partial setup failure must be reported.
An acquisition may be recorded as `preparing` during setup; only its successful
transition to `active` establishes the handling interval.

The active agent is not permanently attached to the issue. A different agent,
session, or machine may continue it after handoff. Before continuing, verify
that another agent has not already resumed active handling. Preserve existing
work instead of taking over an active task or resetting its branch.

## Handoff and environment recovery

A handoff records enough information to continue without the original agent's
memory or filesystem:

- Progress, accepted design decisions, remaining work, and concise evidence.
- Repository and issue identity, remote branch, commit, and PR references.
- Why execution paused and the exact decision or event being awaited.
- An objective resume condition.
- The next skill or action once that condition is satisfied.

Push coherent progress and verify the referenced remote commits before
handing off. Identify anything still local-only rather than presenting it as
recoverable. Local paths are hints, not portable task identities; do not copy
secrets or whole agent logs into the handoff.

Resume conditions may be an explicit design approval, completion of all
blockers, new actionable PR feedback, or a changed CI result. External review
must not wait only for approval: requested changes can also require action.

### Continuing on an existing or fresh environment

`continue-issue` owns recovery for the resuming agent, which need not be the
agent that claimed or handed off the issue:

1. Read the current issue, graph, latest claim/handoff/continuation, and PR
   state. Verify the resume condition and that no other agent is actively
   handling the issue. An unchanged wait does not start another continuation.
   Ignore handoffs superseded by later acquisitions. New feedback or failed CI
   can permit repair without first satisfying every merge gate.
2. Resolve the repository in the current workspace. Clone it if absent;
   otherwise verify its remote and fetch current GitHub state using this
   environment's repository access.
3. Restore the existing task branch and create its isolated worktree, or reuse
   an already-correct worktree. Verify the current remote head against task
   records; do not start from a new default-branch claim or overwrite
   divergent local work. For completed delivery with deleted refs, use a verified
   recovery commit without recreating the task branch.
4. Load the manifest and repository setup instructions. Prepare the declared
   toolchain, dependencies, and local configuration needed for the next action.
   Cleanup needs only its own tools, not the complete delivery toolchain.
   Obtain credentials through the environment's normal mechanisms, not from
   another agent's handoff.
5. Confirm the environment is ready and task state is still current. Record
   the continuing agent, branch/head, triggering evidence, and next action;
   reconcile the board and return the suggested next action to the caller.
   Continuation does not execute that action or restart Dev.

If remote work cannot be verified or the environment cannot be reconstructed,
record the concrete blocker instead of claiming a successful continuation.
Reuse existing branches, PRs, and records after partial failures.

Completion cleans up only safe task resources in the current environment and
the corresponding remote task refs. It does not assume access to a previous
agent's local worktrees.

## Autopilot

The agent running autopilot itself claims or continues an issue, prepares its
local environment, and follows the ordinary lifecycle skills. It completes or
durably hands off that issue before starting another; it does not pass delivery
to an issue agent. Independent reviewers may assist without taking ownership.

Configure each repository in `RESOURCE-MAP.yml`:

```yaml
repos:
  <repository>:
    autopilot:
      mode: reasonable-approval
      wait_for_ci: true
```

Only `orchestrator-autopilot` interprets the modes:

| Mode | Behavior |
|---|---|
| `auto-approval` | Approve recommended design/implementation choices and permit guarded admin PR-approval/queue bypass after clean self-review and CI. |
| `reasonable-approval` | Proceed when the recommendation fits the referenced manifest's constraints and delegation, has no material ambiguity, and requires no explicit approval. Otherwise hand off. Keep normal GitHub review/queue requirements; no automatic admin bypass. |

The executing agent applies the selected policy and supplies decisions or
authorized exceptions to ordinary skills.
Those skills perform their actions without reading or branching on modes.
Reconciliation reports approval waits; autopilot judges whether it can supply
the missing decision before concluding that the issue cannot advance.

Missing manifest guidance does not grant reasonable self-approval. Missing or
unsupported mode settings are configuration problems, not silent defaults.
Config alone, an earlier handoff, or another repository's mode never grants
authority to a new direct call. Resolve policy for the operation's repository,
especially the PR repository.

Optional `wait_for_ci` is a YAML boolean, interpreted only by autopilot.
Omitted or `false` preserves handoff on pending CI. With `true`, pending CI
as the sole remaining gate is observed until completion, without a configured
timeout. The agent retains active handling and its local environment and does
not start another issue. Ordinary PR skills return `waiting` when the caller
explicitly chooses to observe that wait; direct calls still hand off by default.
Previously released CI-only waits may be observed read-only, without
reacquiring until the resume condition is satisfied.

Use a native watcher or event subscription with conservative polling, then
refresh head/base, checks, feedback, and requirements. CI failures return to
repair assessment; unchanged clean self-review is reused without spending
another review pass. Required human review/approval, explicit holds, merge
queues, missing/unknown CI, and capability/infrastructure blockers still hand
off. Waiting grants no extra authority. Stop the watcher and preserve work
on interruption; unavailable observation is a blocker, not a reason to spin.

Both modes preserve explicit user holds, product constraints, review limits,
CI, and non-bypassed requirements. `--admin` is broad, so the completion skill
verifies caller-authorized exceptions and quality evidence, then binds merge
to the reviewed head. Closing an unmerged PR is not completion.

Queue admission and direct merge have different readiness conditions.
`iterate-pr` can suggest `complete-issue` once pre-queue requirements are met;
checks that run only inside the queue cannot block entry. Completion selects
the queue or direct-merge path, then verifies actual merge or records a queue
handoff. Queue-only CI is never waived for an admin bypass.

```text
boot and reconcile the board
repeat until the normal stopping condition holds:
    resume started work that can advance; otherwise select Ready work
    before stopping, consider enabled CI-only waits for read-only observation
    resolve that repository's settings; personally continue or claim when ready
    follow Plan/Dev, observing enabled CI-only waits and reassessing changed evidence
    complete or durably hand off before selecting again
    consume outcomes and refresh affected work
    before stopping, refresh the complete board and resume conditions
```

Load only the current issue's project guidance and environment; retain concise
durable references between issues rather than accumulating implementation history.
New issues or dependencies discovered during development return to the board.
No extra enablement flag, issue label, or tracking-parent exclusion is needed.

The normal stopping condition (`drained`) is:

- No issues remain Ready.
- Every remaining `In progress` issue has a handoff with an unsatisfied resume
  condition and no active/preparing handler.
- Other issues are dependency-blocked in `Backlog` or completed in `Done`.

No preparing/active handler may remain in any state, and no completion cleanup
may be actionable. In particular, Done does not by itself prove ownership release.

An empty Ready lane is not enough: actionable feedback, approvals, CI changes,
and merged-PR cleanup can resume existing work. End the current handling interval
before the final assessment; another agent's active work means `paused`, not
`drained`. Except for configured CI observation, do not poll unchanged waits.
Never repeatedly publish the same handoff.

Report-only self-review findings require a handoff for a remediation decision.
Autopilot does not automatically fix them, reset review counts, or treat a new
autopilot invocation as an independent review request.
PR iteration checks these constraints before repairs. Current clean evidence
still permits completion when it used the final review pass.

Incomplete reads, unresolved issue items, uncertain ownership, or other unresolved
failures prevent a successful drain. After a local failure, continue other work
only if the current handling interval has ended; a lost handler with unresolved
ownership stops the run with `partial_failure`. Do not retry failed or waiting
issues without relevant new evidence. On interruption, preserve work and hand
off. Never change status merely to empty Ready or pretend that an unavailable
handler released its work. A read-only request returns `snapshot` without
execution.

## Skill conventions and validation

Each active skill uses **Use / Steps / Output** sections. Common invariants
live in core guidance, not repeated policy blocks in every skill.
Approval-mode and CI-wait configuration belong only to `orchestrator-autopilot`.
Load initialization and operational references only when needed.

Run the document contract checks from the vault root:

```powershell
python -B -m unittest discover -s .\github-dev-orchestration\tests -q
```

These checks cover all thirteen skills' inventory, routing, references, four-state
model, and recovery requirements without modifying GitHub. They validate the
skill documents, not live GitHub coordination.
