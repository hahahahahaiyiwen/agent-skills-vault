# Roadmap Planning, Issue Delivery, and Board State

This guide applies the [design principles](README.md). The thirteen skills
support two lifecycles, with handoff/continuation for cross-agent delivery.
`..\skills\orchestrator-boot\references\DEV-FLOW.md` shows the routes and is
loaded by boot.

## Two lifecycles

| Cycle | Purpose |
|---|---|
| Roadmap planning | Review product/project goals and use `plan-issues` to add, edit, or remove planned issues and relationships. Preserve history when withdrawing work. |
| Issue delivery | Use `claim-issue` to start new work and `complete-issue` to finish delivery. Design, implementation, self-review, PR publication, and PR iteration skills are optional and may run in any order. |

Planning is not a prerequisite for each issue's delivery. Discoveries that
change goals, outcomes, or dependencies may feed back into the roadmap.
Routine changes to an issue's implementation approach do not restart planning.

`handoff-issue` releases the outgoing handling agent after preserving progress;
`continue-issue` restores the same issue/branch for the next handling agent.
Use `## HANDOFF` and `## CONTINUE` issue comments for these transfer records.
Resume at the next useful activity, not through a new claim or by replaying
completed activities. The same workflow supports continuation in a fresh session.

## Choose actions from the work

Use issue acceptance criteria, repository instructions, and the configured
manifest to decide what is needed. A real prerequisite is missing information,
authority, an external dependency, or evidence required for the intended action,
not a missing optional skill invocation. The required delivery endpoints do not
turn standalone read-only design or review requests into issue acquisition.

| Situation | Useful behavior |
|---|---|
| A small change is understood | Implement directly, reasoning about the approach within the work. No separate design action or issue comment is necessary. |
| Work would benefit from early collaboration | Open a PR, using a draft for unfinished work and identifying pending evidence. Review may happen afterward. |
| The implementation approach changes within scope | Adapt it; update a meaningful decision record if future work depends on the change. Do not automatically replan or reconcile. |
| Outcomes or dependencies change | Revise affected issues/relationships under the request's authority, and update only affected statuses. Planning is available when it helps. |
| Review proposes unrelated improvements | Preserve the findings and rationale, but do not expand the issue to implement every suggestion. |
| A decision exceeds delegated authority | Present the specific uncertainty and recommendation. Hand off only if work actually pauses or transfers. |

A direct skill request performs that action and returns. Supporting reads,
local reasoning, and necessary in-scope updates do not require separate skill
handshakes. Conversely, approval of a design does not authorize implementation,
and asking to open a PR does not authorize merging. Autopilot or another explicit
end-to-end request may choose further actions.

## Context and configuration

Boot loads CORE, DEV-FLOW, and the bundled workspace configuration.
`..\skills\orchestrator-boot\references\CORE.md` defines GitHub records, the
relationship between handling agent, issue, and worktree, the local worktree
layout, and reloading missing configuration.
`..\skills\orchestrator-boot\references\INITIALIZE.md` guides configuration
when requested entries are missing or incomplete.
DEV-FLOW owns lifecycle orientation, not configuration setup.
Use known repository and PR identities directly; board mapping is needed for board
operations, not unrelated publication. Report declared but unreadable guidance
or conflicting mappings rather than ignoring them.

The bundled map is
`..\skills\orchestrator-boot\references\RESOURCE-MAP.yml`. Explicit setup may
initialize it in place; implicit/read-only use never writes it. Configure only
needed entries. `repos.<key>.path` identifies the main worktree on the repository
default branch; `worktrees.convention` locates separate issue worktrees when
configured. Both paths use the retained workspace root, not the current working
directory; manifest paths use the repository root. Prepare or verify main before
creating issue worktrees, and never switch it onto an issue branch. Separate
installed copies can hold different workspace maps.

The manifest expresses goals, constraints, tradeoffs, and delegated decisions.
Skill settings are optional and apply to their owner only. They do not enable
or disable lifecycle stages, and loading configuration grants no new authority.

## Durable state without an activity log

GitHub remains the shared source of truth: issues for scope, native relationships
for decomposition/dependencies, Projects for status, branches/PRs for delivery,
and concise decisions or handoffs for continuity.

Persist information another contributor or session needs to understand or
resume work. Use the issue body, PR description, an existing comment, or a linked
repository document. `design-issue` records approved designs under `## DESIGN`;
`implement-issue` records finished changes and verification under `## IMPLEMENT`.
These issue comments do not create new stage prerequisites. Avoid approval
tokens, per-refinement ledgers, or a new comment after each action.

For implementation, one handling agent works on one issue in one issue worktree
on its task branch. Independent reviewers do not take over its branch.
Before acquiring work, establish that no other active/preparing handling agent
owns it. Record taking and releasing handling; comments alone are not a
distributed lock. A branch or assignee is not proof of a live handling agent,
and elapsed time does not authorize takeover.

On an actual pause, preserve coherent remote progress and state the remaining
work, decision/event needed, and next useful action. Identify local-only data
honestly. Resume from current GitHub evidence, not old paths or an old workflow's
next-skill suggestion. Prepare only the environment needed for that action.

## Board state is a projection of facts

| State | Meaning |
|---|---|
| `Backlog` | At least one native blocked-by dependency is unsatisfied. |
| `Ready` | New work is unblocked, or a released dependency wait has cleared. |
| `In progress` | Started work, including documented approval, review, or CI waits. |
| `Done` | Accepted delivery is verified and the issue is closed as completed. |

Parent links describe decomposition, not execution order. A blocker is satisfied
by completed closure, not cancellation. Retain started branches when work returns
from Backlog to Ready. A handoff is not another board state.

Any acting skill may update affected items through shared Project guidance;
`reconcile-board` is useful for snapshots or drift. Reuse metadata, paginate
the requested scope completely, and avoid full-board reads for one changed
issue. Completion can unblock dependents without another planning cycle.
Surface ambiguous state and unfinished cleanup instead of guessing.

## Review and integration are separate concerns

Self-review is available when requested, useful for risk, or explicitly required
by the project. Its independent reviewer can inspect relevant whole-worktree
context, including design, rather than only the diff. Read-only review requires
neither ownership nor a clean committed worktree.

Ask the user for a severity threshold when missing: Low, Medium, High, or Critical.
The selected level and all higher levels must have zero findings; lower-level
findings still appear in the report.

Optional per-repository settings remain:

```yaml
self_review:
  mode: until_clean
  max_iterations: 3
```

`single_pass` and read-only requests are report-only; `until_clean` repeats
review, scoped fixes, and re-review until the severity target is met or the cap
is reached. Omitted mode/limit defaults to `until_clean` and three passes;
an explicit configured limit overrides that default. Started, interrupted,
and verification passes count toward the same request. Preserve the threshold
and remaining budget across continuation, not as a global publication or repair
permit.

Raise consequential uncertainty before speculative edits and keep unresolved
findings counted. Only a completed independent review of the current version
can confirm the target is met. Cap exhaustion or a blocker without that evidence
leaves the target unmet; lower-severity findings may remain even when it is met.

Opening a PR can precede review or completion of CI. Merging must meet the
accepted outcome and requirements not covered by an explicitly authorized
bypass. Admin bypass must be requested explicitly in completion input;
CI and explicit holds remain binding. Queue entry is not a completed merge.
`complete-issue` requires a PR, not a prior `open-pr` invocation. After merge,
record `## COMPLETE` on the issue and update issue/board status. An already
merged PR needs only missing completion updates or cleanup. After issue closure,
remove only the verified, clean issue worktree and fast-forward a clean,
behind-only main worktree. Preserve dirty, extra, or divergent work and record
cleanup/main-update results separately from delivered status before releasing
handling.

## Autopilot chooses, rather than marches

Preflight loads missing orchestration context. Input identifies the Project
and requested scope; a read-only request returns a snapshot without writes.
An explicit autopilot request authorizes the same agent to drive issue delivery
one issue at a time: claim or continue, choose useful intermediate activities,
and complete or hand off. It does not spawn issue workers or force intermediate
skills to run. Prefer existing actionable work, including PR repairs and cleanup;
finish or durably hand off before selecting another issue.
Invoked reviews retain their scope, severity threshold, report-only mode, and
remaining budget.

Optional settings belong to the operation's repository:

```yaml
autopilot:
  mode: reasonable-approval
  wait_for_ci: false
```

`reasonable-approval` is the default: act within the request and project
delegation, retaining normal GitHub approvals and queues. `auto-approval` can
select recommended in-scope decisions and supply guarded review/queue exceptions
during this explicit run, never a CI waiver. Neither mode resolves ambiguous
requirements by blanket approval or overrides an explicit hold.

With `wait_for_ci: true`, observe CI when it is the sole remaining gate, without
a configured timeout. Retain owned handling; released work can be observed
read-only. Other waits still require their actual decisions or events. Stop
watchers and reassess on changed conditions, and do not treat watcher completion
as permission to merge.

Refresh affected facts while working. Before reporting the board drained,
verify the complete requested scope has no actionable work, active/preparing
handling agent, or actionable cleanup. Empty Ready is not enough. Unknown state or
incomplete reads cannot establish success.

## Maintaining the skills

When refining a skill, use **When to use / Preflight / Input / Guidance / Output**.
Keep concrete direction and a few necessary boundaries rather than a required
algorithm. Share small operational references, not a hidden policy engine. Do not
make return tokens, comment markers, or optional skill execution prerequisites
elsewhere.

Run document contracts from the vault root:

```powershell
python -B -m unittest discover -s .\github-dev-orchestration\tests -q
```

They cover document integrity, lightweight text budgets, independent actions,
and retained coordination/integration safeguards. They do not establish live
agent compliance, GitHub behavior, or runtime latency.
