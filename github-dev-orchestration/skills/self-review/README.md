# Self Review

Self-review uses **When to use / Preflight / Input / Guidance / Output**.
Preflight loads missing orchestration context; input identifies the issue and
the user's severity threshold. Ask for the threshold if it has not been supplied.

The target is inclusive: High means zero High or Critical findings. Review the
relevant whole worktree independently, address qualifying findings within scope,
and re-review. Raise consequential uncertainty rather than making speculative
changes or dropping unresolved findings from the count.

Keep the configured iteration cap (default 3 when omitted) across retries and
continuation; all started, interrupted, and verification passes count.
`single_pass` and read-only requests remain report-only. Reaching the cap or
pausing without a completed current review meeting the target is an unmet
target, not success.

Report counts at every severity, including lower-level findings left open.
Meeting the selected target does not mean every finding is cleared and is
not a publication or merge prerequisite unless explicitly required.
