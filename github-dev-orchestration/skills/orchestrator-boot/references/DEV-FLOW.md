# Plan and Dev Routing

```text
Plan: goal/discovery -> high-level design -> plan-issues -> reconcile-board
Dev:  claim-issue -> design-issue -> implement-issue -> self-review
        -> open-pr -> iterate-pr -> complete-issue
```

Arrows show the normal order, not permission for a skill to invoke its successor.
Each skill returns to its caller; only an explicitly requested workflow sequences
the stages. A direct invocation stops at its result, including after approval.

| Need | Skill |
|---|---|
| Initialize local mapping on explicit first use, or load context and guidance | `orchestrator-boot` |
| Create or revise the issue graph | `plan-issues` |
| Inspect or repair board state | `reconcile-board` |
| Start unclaimed Ready work | `claim-issue` |
| Design one issue's solution | `design-issue` |
| Implement and verify it | `implement-issue` |
| Independently assess the solution in project context | `self-review` |
| Publish the issue-linked PR | `open-pr` |
| Handle PR feedback, checks, and review waits | `iterate-pr` |
| Merge where applicable, close, and clean up | `complete-issue` |
| Pause and release active handling | `handoff-issue` |
| Restore released work and resume its next action | `continue-issue` |
| Drive Ready and resumable board work until only blocked/waiting outcomes remain | `orchestrator-autopilot` |

Outcome, decomposition, or dependency changes suggest `plan-issues`; a material
implementation-choice revision suggests `design-issue`. Independent follow-ups
do not expand or block current work. A new prerequisite can return started work
to Backlog; continue the retained branch after it clears.

Self-review follows project settings and preserves its run count across
continuation. PR feedback can trigger repair before merge gates are satisfied;
eligible queue entry belongs to completion, not an indefinite review wait.
No-PR outcomes bypass publication, not acceptance evidence.

Autopilot supplies decisions and sequences returned actions, handling one issue
through completion or handoff before another. Ordinary skills do not select
its policy. Only real pauses release handling.
