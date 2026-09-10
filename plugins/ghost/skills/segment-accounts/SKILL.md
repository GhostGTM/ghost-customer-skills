---
name: segment-accounts
description: Classify accounts into ICP, persona, product, or custom segments and compare cohorts using Ghost definitions and evidence. Use for segmentation, ICP fit checks, tiering, and cohort comparison, not for editing the definitions themselves.
argument-hint: "[accounts or cohort] [segment scheme or ICP]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish from `$ARGUMENTS` the accounts to classify (a named list, a segment, or the whole book) and the scheme: existing ICPs and personas from Ghost, or criteria the user supplies.

Load the definitions first: `list_icps`, `list_personas`, `list_products`, `list_use_cases`, and `get_pmm_context` for their stated criteria (industry, size, revenue, headquarters, technologies, pains). Quote each criterion you will test. If a definition has no testable criteria, say so and treat fit as unknown rather than inferring from the name.

Build the population: `search_accounts` for named accounts, `expand_segment` for a cohort, or with `GHOST_API_KEY` `graph.filter_accounts` and `GET /api/v1/data/accounts`. State the count.

Assess each account against each criterion. Use `get_account_context` for classifications, industry, and size as Ghost holds them, and with a key `GET /api/v1/data/firmographics?accountId=...` for the structured fields with their provenance. Record match, partial, no, or unknown per criterion, and the failing or missing criterion. Overall fit is the weakest criterion, not an average, unless the user supplies weights. For lookalikes of an ICP, use `graph.find_icp_lookalikes` when a key is set; otherwise say the capability needs the API.

For cohort comparison, run `list_scoped_account_signals` and `search_segment_activity` in `mode: "aggregate"` per cohort with the same terms and window, and compare distributions, not raw counts, with the denominators shown.

Deliver: a table of account, proposed segment, fit, the deciding criterion, and evidence; a list of accounts that fit no segment or several; criteria that could not be measured and why; and proposed definition changes as text. Keep observed facts separate from your classification.

This playbook does not write. Assigning a label or classification, or changing an ICP, is a confirmed action through the supported write path, or a handoff with the exact proposed values.
