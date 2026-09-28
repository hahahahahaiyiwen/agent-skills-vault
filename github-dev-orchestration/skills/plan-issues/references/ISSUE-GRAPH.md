# Native Issue Graph

Parent/sub-issue links express decomposition; blocked-by links express
prerequisites. A parent is not automatically a blocker. Hierarchy and dependency
graphs are checked separately for self-links and cycles; a parent may depend on
a child.

## API lookup

Use `gh api` with `-H "X-GitHub-Api-Version: 2026-03-10"`. Paths below are relative
to `repos/<owner>/<repo>/issues/<number>` in the issue's actual repository.

| Read | GET suffix |
|---|---|
| Parent | `parent` |
| Children | `sub_issues` |
| Prerequisites | `dependencies/blocked_by` |
| Dependents | `dependencies/blocking` |

- Children: `POST sub_issues` or `DELETE sub_issue` on the parent, with
  `-F sub_issue_id=<child-id>`.
- Prerequisites: `POST dependencies/blocked_by` with `-F issue_id=<blocker-id>`,
  or `DELETE dependencies/blocked_by/<blocker-id>` on the dependent.

Read referenced issues in their own repositories for numeric database `id`
values, not issue numbers or GraphQL node IDs. Read relationship lists with
`--paginate`; failed or incomplete reads are unknown, not empty. Verify issue
access before treating not-found as no parent.

A prerequisite is satisfied only when closed with `state_reason=completed`,
not cancelled. Read current links before writing; verify changes and report
failed/partial updates. Do not remove a real blocker merely to change status.
