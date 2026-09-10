---
name: proof-finder
description: Find customers and evidence suitable for a case study, proof point, testimonial, or reference call, from Ghost calls and emails. Use for "who could be a case study", "quotes about outcome X", or anonymized success bullets; use voice-of-customer for problem themes.
argument-hint: "[product or outcome] [optional cohort or account]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish from `$ARGUMENTS` the product or use case, the outcome the story needs, the cohort (or a named account), and the intended use: internal shortlist, anonymized bullets, or a draft for customer approval.

Check what already exists: `list_case_studies` and `list_proof_points` for approved assets on the same product or outcome, so you build on them rather than duplicate.

Build the candidate pool: `expand_segment` by product or use case, or the named accounts. Scan for outcome language with `search_segment_activity` in `mode: "aggregate"` using separate passes for results words (improved, reduced, saved, adopted, rolled out, renewed, expanded) and the user's outcome terms, then `mode: "sources"` on the top accounts. Add `list_scoped_account_signals` for extracted outcomes and next steps. For each strong candidate, read the sources with `read_source` to get exact wording, speaker, and date.

Qualify each candidate on three story beats and two gates:

- Beats: the challenge in the customer's words, why they chose this product, and the result they stated, each with a verbatim quote, speaker role, and date.
- Gates: commercial standing from `get_deal_context` (active, renewed, expanded, at risk, churned) and open issues from `get_open_commitments` and risk signals. A customer with an unresolved complaint or a live escalation is not a reference candidate this week.

Deliver a ranked shortlist: account, the three beats with quotes, standing, blockers, and whether an approved asset already exists. On request, produce anonymized bullets ("a mid-size footwear brand") that keep the customer's language and drop identifying detail. Only customer statements count as proof; a rep's description of the win is context, not a quote.

Everything here is internal until the customer approves. Creating a case study or proof point record is a confirmed action (`upsert_case_study`, `upsert_proof_point`) with the full payload shown first; publishing, contacting the customer, or sharing quotes externally is a handoff.
