---
name: customer-lookup
description: Answer "which customers use or have X", "who has said X", and "is Y a customer" with a filtered account list and evidence from Ghost. Use for adoption, attribute, and membership questions across the book; use voice-of-customer for themes and quotes.
argument-hint: "[attribute, product, or account name]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish from `$ARGUMENTS` whether this is a single-account question or a book-wide filter, and what counts as a match: a commercial record (they bought it), a definition (they are in the segment), a stated fact (they said they have it), or a mention (it came up).

**Single account.** Resolve with `search_accounts`; show candidates if the name is ambiguous. Read `get_account_context` for commercial status, products, and classifications, and `get_deal_context` for the current contract. Answer yes, no, or unknown, with the status, the evidence, and its date.

**Book-wide filter.** Choose the source of truth by match type, and use more than one when the question spans them:

- Segment membership by product, use case, ICP, or persona: `expand_segment`.
- Extracted facts (has a target, uses a tool, plans a rollout): `list_scoped_account_signals` with `query` or `fact_types`, scoped by segment or `account_refs`.
- Mentions in calls and emails: `search_segment_activity` with `mode: "aggregate"` and two or three synonyms as separate passes, then `mode: "sources"` for the evidence on the matched accounts.
- Deterministic facets (pipeline status, location, owner, has sources) and full rows: with `GHOST_API_KEY`, `graph.filter_accounts` for the cohort and `GET /api/v1/data/{resource}` for firmographics, classifications, or labels.

Deliver a table: account, match type (record, definition, fact, mention), the evidence excerpt or field value, its date, and confidence. Sort by strength of match. Follow with coverage: accounts scanned versus total in scope, truncation, and which match types were not checked. A zero result on one path is not "no customer has this"; say which paths were searched.

Do not treat a mention as adoption, a segment definition as a purchase, or a rep's statement as the customer's. Do not create labels, update records, or export the list as part of the lookup; those are separate confirmed actions or handoffs.
