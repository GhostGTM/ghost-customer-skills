---
name: prioritize-accounts
description: Rank a defined Ghost account book or segment by what needs action and why now. Use for weekly priorities, renewal attention, or changes across accounts, not a single-deal assessment.
argument-hint: "[book or segment] [period or business objective]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish owner/segment, time window, and objective from `$ARGUMENTS`.

Build the population first, and say how you built it:

- **A book or pipeline ("my renewals", "my open deals this quarter").** MCP has no pipeline lister. If `GHOST_API_KEY` is set, use the API: `graph.filter_accounts` with `my_accounts` or `account_owner` to get a `filter_handle`, then `graph.query_deal_flow` or `graph.query_forecast_pipeline` with that handle, the period (`quarter`, `fiscal_year`, or `from`/`to`), and `status`. Page with `limit` and `offset` until the returned count matches the rollup. Without a key, ask the user for the account list or a segment; do not substitute a workspace-wide signal scan for a named person's book.
- **An ICP, persona, product, or use-case cohort.** Resolve the segment and use `expand_segment`.
- **A named list.** Resolve each account with `search_accounts`.

Inspect returned counts, limits, unresolved IDs, and pagination. A rollup does not prove the list is complete. If no supported pagination can recover the intended population, narrow the scope or explicitly label the priorities as covering the returned subset.

Bulk-scan the bounded cohort with `list_scoped_account_signals` (use `account_refs` or the segment, and `fact_types` or `risk_only` when the objective is risk), then read `get_deal_context` and `get_open_commitments` for the most consequential candidates. For change questions, compare source dates within the window; do not claim a trend from one snapshot.

Prioritize explainably using the customer's criteria. Without a supplied scheme, consider time-bound commitments, commercial timing (service end, close date, renewal period), severity of corroborated blockers, and credible expansion signals. Keep risks and opportunities distinct. Unknown contract value is not zero. Avoid a made-up numerical score or claims of comprehensive forecast accuracy.

Deliver an action queue: account/deal, priority reason, what changed or is due, suggested action, known owner, and supporting source/date. Start with up to five actionable items unless requested otherwise. Include the cohort, period, coverage, and missing information that might change the ranking.

Do not silently update deal stages, schedule monitoring, or send the queue to a channel.
