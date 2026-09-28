# Development Flow

## Issue delivery cycle

```text
claim-issue -> design-issue -> implement-issue -> self-review
  -> open-pr -> iterate-pr -> complete-issue
```

`claim-issue` and `complete-issue` are the required endpoints for delivering a
new issue. The intermediate skills are optional: use them in any order, repeat,
or skip them. The arrows show a usual route, not mandatory checkpoints.
`complete-issue` requires a PR, not an invocation of `open-pr`.

## Roadmap planning cycle

```text
roadmap review -> plan-issues -> updated issue graph/board -> roadmap review
```

`plan-issues` works at the product/project roadmap level, adding, editing, or
removing issues and relationships from the plan. This is separate from delivering
one issue. Routine design changes do not restart planning; discoveries affecting
goals, outcomes, or dependencies may inform the next roadmap review.
Preserve issue history when withdrawing work.

## Handoff between handling agents

```text
handoff-issue -> continue-issue -> next useful activity
```

Handoff records progress and releases the outgoing handling agent.
Continuation lets the next handling agent restore the same issue and task branch,
recreating its worktree if needed. This is not a new claim or a restart of the
delivery cycle. The same transfer also supports a new session for the same agent.

## Supporting capabilities

| Need | Skill |
|---|---|
| Missing context or explicit configuration setup | `orchestrator-boot` |
| Board snapshot or status drift | `reconcile-board` |
| Drive issue delivery, one issue at a time | `orchestrator-autopilot` |

Board updates accompany changed facts, not every arrow. Load
`..\..\reconcile-board\references\PROJECT.md` only for board operations.
