# GitHub Development Orchestration

Lightweight, project-neutral capabilities for doing development work with
GitHub. The agent chooses how to deliver the requested outcome; the skills
provide useful direction, coordination, and continuity, not an enforced lifecycle.

The [development guide](STATE-MACHINE.md) explains their use and shared boundaries.

## 1. Lightweight

Load the selected skill, reuse known project context, and read operational
references only when needed. Boot is a context helper, not a prerequisite for
every action. A missing optional map entry does not block an otherwise
well-understood repository or PR action.

Roadmap planning and issue delivery are separate cycles. Delivery requires
`claim-issue` for new work and `complete-issue` to finish; intermediate skills
are optional and may run in any order. Their usual route is not a mandatory chain
or a checklist of documents and return tokens. A direct request ends after its
action; an explicit end-to-end request permits further actions. Decision approval
does not silently expand execution scope.

## 2. Project neutral, manifest guided

Keep project-specific goals, priorities, tradeoffs, constraints, and delegated
decisions in the project's manifest and repository instructions, not universal
skills. The optional bundled resource map locates repositories, boards, and
manifests; small skill settings apply only when relevant.

The manifest provides direction and decision boundaries, not a checklist of
stages or approvals. Honor explicit requirements without inventing new ones.

## 3. GitHub holds durable development state

Keep issue scope, native relationships, board status, task branches, PRs,
important decisions, and handoffs recoverable from GitHub.

Durability does not mean recording every activity. Persist consequential
decisions and enough progress for collaboration or recovery; reuse issue text,
PR descriptions, or linked repository documents. Headings such as `## CLAIM`,
`## DESIGN`, `## IMPLEMENT`, `## COMPLETE`, `## HANDOFF`, and `## CONTINUE` identify
record types, not workflow prerequisites; keep the body concise and flexible.
Avoid per-refinement design records, duplicate journals, or raw session transcripts.

For implementation, one handling agent works on one issue in its issue worktree;
independent reviewers do not take over its branch. A handoff records recoverable
progress and a real resume condition before releasing that agent; another agent
can restore the environment without the original machine or conversation.

## 4. The board is the plan and roadmap

Native parent/sub-issue links express decomposition; blocked-by links express
prerequisites. Parenthood alone proves neither blocking nor completion.

| State | Meaning |
|---|---|
| `Backlog` | A real issue dependency prevents progress. |
| `Ready` | Unblocked work can start, or dependency-paused work can resume. |
| `In progress` | Started work, including review, approval, and CI waits. |
| `Done` | Verified delivery, merged PR where applicable, and completed issue closure. |

Update affected items when facts change. Any acting skill can do this directly;
reconciliation is for snapshots or inconsistent state, not every design change.
The roadmap-planning cycle adds, edits, or removes planned issues when project
goals, outcomes, or dependencies change, not for every implementation choice.
Preserve issue history when withdrawing work. No separate authoritative roadmap
is required.

## 5. Prefer agent autonomy

Let the agent investigate, adapt the design, implement, review when useful, and
publish a PR without ritual prerequisites. Opening a PR is not merging it.
Optional self-review is not a universal publication or merge gate; actual project
requirements, acceptance problems, GitHub protections, and explicit holds remain.

Involve a human for consequential uncertainty or authority not already delegated.
Keep non-actionable suggestions separate from required corrections. Prefer the
smallest useful coordination action over another planning or approval round trip.
