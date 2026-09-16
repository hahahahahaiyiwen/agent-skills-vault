# Azure DevOps-first Orchestration Model

This workspace uses a **Azure DevOps-first orchestration model**.

## Model overview

- Azure DevOps (Board + WorkItem + Comment) is the shared cross-session context.
- Operational behavior, governance, and lifecycle standards are loaded by `orchestrator-boot`.

### Startup entrypoint

- At session start, check `$env:ADO_ORCH_ORG_URL` and `$env:ADO_ORCH_PROJECT`; run **`orchestrator-boot`** only if either value is missing or empty.
- If both values are already set for the current session, do not run `orchestrator-boot` again.
- `orchestrator-boot` is the only startup skill referenced by this file.
- `orchestrator-boot` is responsible for loading:
  - governance and development standards (`references/CORE.md`, `references/DEV-FLOW.md`)
  - project mapping (`references/RESOURCE-MAP.yml`)
  - operational skill routing for the task lifecycle

Natural language can express intent, but runtime execution should follow the skill routing loaded by `orchestrator-boot`.

# OS Context 

## PowerShell quoting guardrail

- In PowerShell, the backtick (`` ` ``) is the escape character.
- Do not put markdown backticks inside double-quoted strings unless you intentionally escape them.
- For CLI arguments that include markdown/code formatting, prefer single-quoted strings (for example: `--body 'Start development, branch: `<branch>`'`) or assign a single-quoted here-string to a variable and pass that variable.

# Product Context