---
name: commitments
description: Audit open customer promises and next steps in Ghost, including owners, due dates, and overdue items. Use for what we owe an account or what a customer agreed to do.
argument-hint: "[account or supported owner scope] [optional period]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish the account/owner scope and reporting date from `$ARGUMENTS` and the conversation. Use the runtime date when supplied; if unavailable, ask for the as-of date before labeling items overdue. Preserve the user's timezone for date-sensitive boundaries when known.

Read `get_open_commitments` using supported scope fields. For "mine," require evidence of ownership or supported authenticated-user filtering; do not relabel every workspace commitment as the user's. If the tool cannot establish this scope, clarify it or report the limitation.

For consequential or overdue items, inspect the underlying promise and later relevant sources for completion, cancellation, or a revised date. A source saying "could you send this?" is a request, not proof the recipient agreed. Do not mark a promise complete solely because it is old or someone discussed it again.

Return a register: promise, who owes whom, agreed due date or "not stated," status as of the reporting date, source, and suggested next action. Separate overdue, upcoming, undated, and conflicting status when useful. Preserve distinct deliverables when grouping repeated mentions.

Flag material contradictions between extracted status and later evidence without rewriting Ghost. Suggest owners/dates as proposals only. The register does not send reminders, assign tasks, mark completion, or create new commitments.
