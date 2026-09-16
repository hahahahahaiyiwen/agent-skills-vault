# GitHub Development Orchestration

A lightweight set of skills that keeps an agent aware of the GitHub development
lifecycle without taking over its engineering reasoning. The agent does the
work; the skills provide orientation, coordination, and continuity.

These principles guide the design and refinement of the skill set. The
[two-cycle model and skill responsibilities](STATE-MACHINE.md) describe the
workflow implemented by the thirteen skills. `orchestrator-autopilot`
coordinates that lifecycle across Ready and resumable board work.

## 1. Lightweight

Keep the always-loaded context small: the lifecycle map, essential boundaries,
and the selected project's guidance. Load detailed skills only for the action
being performed.

An individual skill returns its result and suggested next action, then stops.
Only an explicitly requested workflow sequences lifecycle stages; approval alone
does not authorize another stage.

Prefer scoped reads and reuse of unchanged discovery results over repeated
full-board scans. Keep tool output and durable updates concise. Carry only
necessary coordination state between tasks, using handoffs or fresh task
contexts rather than accumulating every issue's history.

Diagnostics and investigation tooling are optional, not prerequisites for
development.

## 2. Project neutral, manifest guided

Skills describe GitHub lifecycle actions, not a particular product, language,
toolchain, or workspace layout. Workspace configuration such as
`RESOURCE-MAP.yml` locates repositories, boards, and their manifests, and holds
small project-specific skill settings such as self-review mode and iteration
limit. Per-repository `autopilot.mode` is interpreted only by the autopilot
skill, not by individual lifecycle skills.

On explicit first use, `orchestrator-boot` initializes its bundled
`references\RESOURCE-MAP.yml` in place. Later boots reuse it; implicit or
read-only calls report missing configuration without writing.

Each project supplies a manifest describing its goals, priorities, tradeoffs,
constraints, and the decisions delegated to the agent. Use that guidance,
repository instructions, and existing conventions to make project-specific
choices. Keep those choices out of universal skills.

The manifest should give the agent enough direction to act independently, not
become an exhaustive approval checklist.

## 3. GitHub holds durable development state

GitHub is the shared source of truth across agents and sessions.

| Information | Durable location |
|---|---|
| Task scope and acceptance criteria | Issue body |
| Work state | Project board status |
| Decomposition and prerequisites | Native parent/sub-issue and dependency relationships |
| Ownership and implementation | Remote task branch, claim/continuation/handoff records, and PR |
| Progress, decisions, and handoffs | Issue and PR comments |
| Review and completion | PR reviews, required checks, merge state, and issue closure |

Implementation uses a local repository checkout and an issue worktree. From
successful claim or continuation until handoff or completion, exactly one
agent actively handles the issue and has its local development environment.

Handoff ends active handling, not durable work. A different agent may resume
by restoring or recreating the checkout, worktree, and repository-declared
setup from GitHub state and project guidance. Prior agent memory and local
paths are not recovery requirements.

Record concise decisions and safe progress in GitHub so continuation does not
depend on the original context. Avoid duplicate updates and parallel state
journals.

## 4. The board is the plan and roadmap

The board's issue graph and current state express the plan and roadmap; no
separate authoritative plan document is needed.

Each issue uses native GitHub relationships:

- **Parent issue:** the larger goal this issue contributes to. Root issues
  have no parent.
- **Blocked by:** zero or more prerequisite issues that must be completed
  before development can start.

Parent links describe work breakdown; blocked-by links determine execution
order and readiness. Having a parent does not itself make an issue blocked.

| State | Meaning |
|---|---|
| `Backlog` | At least one blocked-by dependency is not yet satisfied. |
| `Ready` | All blocked-by dependencies are satisfied, or there are none; work is available to start or resume. |
| `In progress` | Claimed or continued work, including design, implementation, PR review, and documented waits. |
| `Done` | Work is complete, the PR is merged where applicable, and the issue is closed as completed. |

When a blocker completes, re-evaluate every dependent's remaining blockers.
Move each dependent from `Backlog` to `Ready` once all are satisfied. Issues
with no blockers start in `Ready`.

Claiming an issue or continuing existing work moves it from `Ready` to
`In progress`. Work stays there through design, implementation, review, and
waits for approval or CI. A handoff records the resume condition when handling
is released. If a new issue dependency prevents progress, preserve the work
and return it to `Backlog` until its blockers are cleared. Review and handoff
do not introduce separate board states.

Revise the graph as new evidence changes the plan, and keep the board aligned
with GitHub task state. Design documents may explain intent and decisions, but
do not duplicate the execution plan.

## 5. Prefer agent autonomy

Give the agent outcomes, acceptance criteria, and project guidance; let it
choose how to investigate, implement, validate, review, and advance the work.
Routine implementation within an accepted design should not require approval
for every choice. Without delegated authority, discuss material plans/design
with the human and obtain approval; the calling workflow supplies delegation
where appropriate.

Involve a human when a consequential ambiguity cannot be resolved from project
guidance, an action requires authority not already granted, or a high-impact,
hard-to-reverse decision is outside the manifest's delegation. Explicit human
constraints, platform permissions, and CI still apply. Any merge exception
needs current, explicit authority; otherwise normal GitHub requirements apply.

When one issue needs human input, record the specific decision and resume
condition, then continue other work that can proceed. Add universal policy
only to protect a concrete boundary that project guidance and ordinary agent
judgment cannot adequately address.
