---
name: competitive-intel
description: Summarize what customers and prospects say about competitors and why deals were lost, from Ghost evidence. Use for competitor mentions, displacement, closed-lost reasons, and competitive objections; use deal-review for one live deal.
argument-hint: "[competitor or 'closed lost'] [optional cohort or period]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish from `$ARGUMENTS` the competitors (named, or "all"), the cohort (whole book, a segment, new business only, or named accounts), and the period.

Resolve competitor names and known aliases from `list_context` with type `competitor`; add the user's synonyms. If the workspace has no competitor entries, work from the names the user gives and say so.

Measure mentions before interpreting them. For each competitor term run `search_segment_activity` in `mode: "aggregate"` over the cohort and period to get accounts, source types, and months, then `mode: "sources"` for the passages on the most active accounts. Add `list_scoped_account_signals` with `fact_types` for competitor, objection, and blocker facts. Read sources with `read_source` before quoting.

For lost deals: `get_deal_context` per account gives closed-lost deals and the recorded lost reason; with `GHOST_API_KEY`, `graph.query_deal_flow` with `status: "closed_lost"` and the period lists them across the book with the rollup. Pair each recorded reason with what the customer actually said in the sources, and flag where they disagree.

Classify each account-competitor pair: evaluating, chose the competitor, displaced the competitor, incumbent, or mentioned only. Separate customer statements from rep interpretation and from the CRM field.

Deliver:

- Per competitor: accounts by classification, recency, the typical context in which the name comes up, and three to five verbatim quotes with speaker role and date.
- A lost-reasons table: account, deal, recorded reason, customer-stated reason, source, date.
- Contradictions, gaps (accounts with a loss but no source), and coverage: cohort size, sources scanned, terms used.
- Implications as a labeled hypothesis section, not as findings.

Counts are of accounts and sources examined, never a market share. Do not update competitor records or write objection-handling into the context library as part of the analysis; propose those as confirmed actions with the payload shown, or hand off.
