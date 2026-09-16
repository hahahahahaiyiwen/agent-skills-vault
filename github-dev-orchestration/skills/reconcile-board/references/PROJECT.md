# Project Access

Resolve IDs from the configured Project owner (user or organization), number,
and status names. Reuse metadata until it changes. Never embed a workspace's
Project or option IDs in skills.

```powershell
gh project view <number> --owner <owner> --format json
gh project field-list <number> --owner <owner> --format json
```

Read the Status field and its four configured options. Require four distinct
status option IDs; mapping two lifecycle states to one option loses readiness.
If field enumeration is truncated, paginate ProjectV2 fields with GraphQL
before resolving IDs.
Missing fields or options are configuration errors, not permission to invent
another status or change the board schema.

## Complete versus targeted reads

For one issue, paginate its GraphQL `projectItems` and select the configured
Project ID. Do not enumerate the whole board just to find its item.

For a whole-board request, page through ProjectV2 items. A fixed item limit is
not a complete snapshot. For example, after resolving the Project node ID:

```powershell
gh api graphql --paginate -F id='<project-node-id>' -f query='
query($id: ID!, $endCursor: String) {
  node(id: $id) {
    ... on ProjectV2 {
      items(first: 100, after: $endCursor) {
        nodes {
          id
          content {
            __typename
            ... on Issue { id number url title state repository { nameWithOwner } }
          }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name optionId }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'
```

Use the discovered Status field name if customized. Process each response
page; retain only task identity, state, and actionability in working context.
Resolve native graph details for affected issues separately. A GraphQL error,
missing node, inaccessible item, or incomplete pagination must be reported.

## Writes

Add an issue with `gh project item-add <number> --owner <owner> --url <issue-url>`
only after checking that its Project item does not already exist.
`reconcile-board` changes status using discovered IDs:

```powershell
gh project item-edit `
  --id <item-id> --project-id <project-id> `
  --field-id <status-field-id> --single-select-option-id <option-id>
```

Verify the saved value after a write. Snapshot mode performs neither command.
