---
name: deal-review
description: Assess a named opportunity or renewal using Ghost commercial context and customer evidence. Use for qualification, deal risk, renewal readiness, or deal coaching; use prioritize-accounts for a whole book.
argument-hint: "[account] [opportunity or renewal]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Resolve the account, then `get_deal_context`. If several deals match, identify the intended deal before treating their values, stakeholders, or close dates as one opportunity.

Read the relevant network, commitments, and supporting customer sources. Load the customer's qualification methodology if supplied or available in workspace context. Otherwise assess business need, demonstrated value, buyer access, decision process, timing, and unresolved obligations without imposing a named framework or arbitrary score.

Evaluate evidence rather than CRM-stage optimism. A recorded close date does not establish buyer agreement. A champion's enthusiasm does not establish procurement approval. Low activity alone does not prove churn risk. Mark qualification dimensions as supported, contradicted, or unknown, with the source and date.

Return:

- A clear assessment and the evidence that most affects it.
- A compact table of commercial facts, qualification gaps, and conflicting signals.
- The strongest plausible reason the assessment could be wrong.
- Three prioritized next moves, each with an owner if known, the decision it unlocks, and a proposed timing clearly distinguished from an agreed date.

For renewals, separate contractual dates, any fallback date used by the tool, value evidence, sponsor continuity, and unresolved delivery. Do not fabricate a probability, silently change the forecast, or update a CRM record. Include exact proposed corrections as a handoff only when requested.
