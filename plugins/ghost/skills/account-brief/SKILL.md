---
name: account-brief
description: Explain the current state of a named Ghost account using relationship history, commercial context, and dated evidence. Use for account background or a handoff; use meeting-prep for a specific upcoming meeting.
argument-hint: "[account] [optional focus]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Use `$ARGUMENTS` and the conversation to establish the account and focus.

Resolve the account, then call `get_account_context` with the user's actual question as `query`. Add `get_deal_context` for commercial questions, `get_account_network` for relationship/handoff questions, and `get_account_topics` for recurring themes. For a consequential claim, pull the verbatim evidence with `search_source_content` scoped to the account and read the source page before relying on it.

Prioritize the current business objective, commercial motion, active stakeholders, open commitments, and the latest meaningful change. For "what changed" questions, order evidence by source date, not by when Ghost ingested it: an old call recently ingested is historical context, not a new development.

Produce a short account brief:

- One-paragraph situation and why it matters now.
- Known people and roles, distinguishing demonstrated influence from inferred roles.
- Active opportunity or relationship state, including the dates of commercial evidence.
- Outstanding commitments, blockers, and contradictions with sources.
- The next useful action and the missing information that could change it.

State coverage/freshness limits briefly. Do not invent company news, contract facts, or recommended CRM updates to fill empty sections. This is a read/analysis task; saving a new source is a separate action.
