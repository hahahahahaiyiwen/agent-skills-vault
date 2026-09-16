# Native Issue Graph

Use `gh api` against the issue's actual repository, including for cross-repo
parents or blockers. Add `-H "X-GitHub-Api-Version: 2026-03-10"` to REST calls.
Read all pages of relationship lists with `--paginate`; an unavailable or
incomplete relationship view is not an empty dependency set.

| Read | Endpoint |
|---|---|
| Issue state and database ID | `repos/<owner>/<repo>/issues/<number>` |
| Parent | `repos/<owner>/<repo>/issues/<number>/parent` |
| Children | `repos/<owner>/<repo>/issues/<number>/sub_issues` |
| Prerequisites | `repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by` |
| Dependents | `repos/<owner>/<repo>/issues/<number>/dependencies/blocking` |

An authoritative absent-parent response means a root issue. Verify access to
the issue before interpreting a not-found response as an absent relationship.
`state=closed` satisfies a blocker only with `state_reason=completed`.

## Writes

Read numeric database `id` values from REST issue responses; they are not
issue numbers or GraphQL node IDs.

```powershell
gh api --method POST `
  -H "X-GitHub-Api-Version: 2026-03-10" `
  repos/<parent-owner>/<parent-repo>/issues/<parent-number>/sub_issues `
  -F sub_issue_id=<child-database-id>

gh api --method POST `
  -H "X-GitHub-Api-Version: 2026-03-10" `
  repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by `
  -F issue_id=<blocker-database-id>
```

Remove a blocker with `DELETE` at
`repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by/<blocker-database-id>`.
Remove a child with `DELETE` at
`repos/<parent-owner>/<parent-repo>/issues/<parent-number>/sub_issue` and
`-F sub_issue_id=<child-database-id>`.

Before each write, inspect current relationships and skip an existing
postcondition. Validate referenced issues, hierarchy depth, self-links, and
cycles. Hierarchy and dependency graphs are checked separately: a parent may
legitimately depend on a child. Preserve changes already made if a later
operation fails; record the partial result and re-read before retrying.

Adding or removing a dependency changes the execution plan. Apply
`plan-issues` judgment and record why; do not remove a real prerequisite just
to make an issue Ready.
