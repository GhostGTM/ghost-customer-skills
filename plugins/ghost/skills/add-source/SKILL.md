---
name: add-source
description: Save a transcript, meeting notes, document, email thread, or research brief to a Ghost account so it becomes part of the graph. Use when the user pastes or attaches material and wants Ghost to keep it; use call-recap to read what is already there.
argument-hint: "[account] [what the material is]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. This is a confirmed action. Establish the account and the material from `$ARGUMENTS`, the conversation, or an attachment.

Resolve the account with `search_accounts`; show candidates if ambiguous. Read the material in full. Do not truncate, summarize, or clean it: the source is the evidence, and ingest extracts from it later. Choose the type from what it is, not what it is about: `transcript`, `email_thread`, `google_doc`, `notion_page`, `pdf`, `markdown`, `slack_thread`, or `raw_text`. Use the material's own title or date as the title; never invent one. Include `occurred_at` when the material states its date, so the event date is not the ingest date.

Check for duplicates first with `search_source_content` on a distinctive phrase scoped to the account. Source rows are not deduplicated: sending the same material twice creates two sources.

Show the account, type, title, date, character count, and the first and last lines. Wait for a yes. Then write:

- MCP: `customer_add_source` with `customer_ref`, `source_type`, `text`, `title`, `source_url` when there is one, and `metadata` for the date and participants. Any member can write a source; it does not need admin.
- API alternative when `GHOST_API_KEY` is set: `graph.save_account_note` for a note attributed to the key owner, or `graph.apply_update` with a change of kind `add_source` (`source_title`, `source_content`, `source_kind: transcript|note|email|research`) when the material should carry a source kind and link to an account through a proposal.

Report the returned source id and chunk count verbatim, and that brief regeneration was scheduled if the tool says so. Ingest runs later; do not claim facts were extracted. On an error, report it and stop; do not resend.

Research briefs from outside Ghost are third-party material: use `source_kind: research` on the API path or say so in the title on the MCP path, so derived facts stay visibly distinct from first-party data.
