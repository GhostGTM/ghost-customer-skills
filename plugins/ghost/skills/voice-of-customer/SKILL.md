---
name: voice-of-customer
description: Synthesize a defined Ghost customer cohort's needs, objections, and language from actual calls and emails. Use for customer research and PMM insight; do not use it to claim market-wide prevalence.
argument-hint: "[question] [cohort] [period]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish the research question, account/persona/product cohort, and period. Resolve the relevant workspace definitions and expand the cohort before searching. Use supplied scope when clear; ask only for ambiguity that changes whose evidence is included.

Use `search_segment_activity` for raw source evidence and `list_scoped_account_signals` for extracted themes. Use `mode: "aggregate"` for counts and distributions across the whole scope and `mode: "sources"` for examples. `content_query` matches every term, so scan a few synonyms as separate aggregate passes and union them. For a named account's exact wording, use `search_source_content` and `read_source`. Ranked snippets are not a random or complete sample. Inspect actual returned coverage and filter semantics.

Persona searches can include account-wide activity with matched-person voices preferred. Verify the speaker and role before attributing a quote or theme to the target persona. Count distinct accounts/people separately from repeated mentions. Separate salesperson claims from the customer's own language. Read original sources for exact quotations and context.

Deliver the leading themes with evidence, customer wording, affected roles/use cases, counterexamples, and practical messaging/product/sales implications. Distinguish observed findings from hypotheses to investigate. Include denominators only when the tool establishes a consistent population; otherwise use descriptions such as "observed in three of the eight accounts examined," not a market percentage.

Explain scope, time range, source mix, missing/truncated data, and sampling limits. A zero-match query does not prove customers lack a need. Cross-customer synthesis is internal unless shareable material is explicitly established. Do not publish quotes, create proof points, or overwrite ICP/persona definitions as part of analysis.
