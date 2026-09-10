---
name: stakeholder-map
description: Map known people, influence evidence, buying roles, and warm introduction paths at a Ghost account. Use for buying-committee coverage and multi-threading, not bulk net-new contact acquisition.
argument-hint: "[account] [optional opportunity or missing role]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Resolve the account and relevant opportunity from `$ARGUMENTS`. Read `get_account_network`, search known people by relevant roles, and consult `get_intro_ledger` when a warm path is part of the request. Load the relevant persona context to understand which roles matter for this product/motion.

For each person distinguish title, observed involvement, likely buying role, last meaningful interaction, and evidence of influence. Label a buying role as a hypothesis unless a source establishes it. Never infer that a senior title means economic buyer or that co-attendance guarantees a warm introduction.

Deliver a stakeholder table with person, role/title, involvement evidence, relationship recency, and next step. Summarize single-threading risk, missing functions, and the best evidenced warm paths. A path suggestion should name who could introduce whom and the evidence for that connection, without implying they agreed to do it.

If a role is absent from returned data, call it a coverage gap rather than asserting that the company has no such person. Search external providers only for a requested net-new contact task, with the company domain and role scope established. Do not invent names or contact details, request introductions, or send messages as part of mapping.
