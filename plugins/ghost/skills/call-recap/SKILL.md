---
name: call-recap
description: Find a specific call or email thread in Ghost and return its transcript, a recap, or what a named person said about a topic. Use for "find the call", "what did X say about Y", "give me the transcript"; use meeting-prep for an upcoming meeting.
argument-hint: "[account or person] [date, topic, or 'transcript']"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish from `$ARGUMENTS` the account or person, the interaction (date, topic, or "latest"), and whether the user wants the transcript, a recap, or an answer to a question about it.

Locate the source. Resolve the account with `search_accounts` and any named person with `find_person`. Then search: `search_source_content` with the topic or the person's name as `query`, `account_refs`, and `source_scope` (`calls`, `emails`, or `all`). If `GHOST_API_KEY` is set and the user asked by date or attendee, `graph.list_recent_calls` with `customer_id`, `channel`, and an attendee filter gives the dated list directly. `get_account_network` touchpoints are the fallback. If several sources match, list them with date, type, title, and attendees and ask which one, unless the request makes the choice obvious.

Then deliver what was asked:

- **Transcript.** Page `read_source` from `offset: 0` until `has_more` is false or the requested span is covered. Return the verbatim text with the source title, date, and the offsets covered, plus the provider deep link when the tool returns one. Do not summarize in its place. Say plainly if only a summary or excerpt exists in Ghost.
- **Recap.** Date, attendees as recorded, decisions, customer asks, promises made by each side (cross-check `get_open_commitments`), open questions, and three to five verbatim quotes with offsets. Keep interpretation in its own labeled section.
- **"What did X say about Y."** The verbatim passages attributed to that person, each with date and offset, then a one-line answer.

Speaker attribution follows the transcript's labels. When two people shared one microphone or a label is generic, say attribution is uncertain rather than guessing. Never invent a recording, a date, or a quote. If no source matches, say what was searched (account, scope, terms) and offer the nearest matches.

This is a read task. Saving notes or a new source is a separate confirmed action.
