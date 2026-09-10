---
name: renewal-prep
description: Prepare a renewal, price change, or packaging conversation with a named Ghost account: the commercial facts table, prior objections, and the ask. Use for renewals and pricing; use deal-review to qualify a new opportunity.
argument-hint: "[account] [renewal period or pricing change]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Resolve the account from `$ARGUMENTS`. Establish the renewal period and any proposed change the user names.

Gather the commercial record and the conversation history:

- `get_deal_context` for deals, amounts, service and close dates, and the commercial motion brief. Separate each deal; a past renewal and the coming one are different rows.
- `get_account_context` with a query such as "renewal pricing contract terms".
- `search_source_content` over calls and emails for renewal, price, fee, invoice, quote, tier, discount, and the customer's own product names. Read the source for any number you will present.
- `get_open_commitments` for promises either side made since the last renewal.
- `get_account_network` for who was in the last commercial conversations and whether they are still there.

Build the facts table before writing anything else. One row per distinct figure: item, amount, kind (paid, invoiced, proposed, quoted, list), who bills whom, period covered, source and date. If two parties invoice separately, keep their figures apart. If the record holds no broken-out figure for what the user asked, write "not in record" and say so up front; do not fill the gap with a related number.

Then deliver a prep card:

1. The facts table.
2. What changed since the last renewal: usage, stakeholders, delivery, open obligations.
3. Objection history: what this customer pushed back on before, with quotes and dates, and how it was resolved or left open.
4. The proposed ask or options, each tied to evidence of value the customer stated, with the concessions already given.
5. Risks and contradictions: stale sponsors, unresolved complaints, dates that conflict across sources.
6. A suggested opening and the three questions to ask before naming a number.

Distinguish agreed dates from proposed ones. Do not compute a renewal price the record does not support, change a CRM field, or send anything. If the user asks for a follow-up email, hand off to the follow-up playbook with the facts table as its evidence.
