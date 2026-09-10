---
name: follow-up
description: Draft a follow-up to a specific customer meeting, email thread, or commitment using Ghost history and the user's writing style. Use for a message grounded in an interaction, not a cold outreach campaign.
argument-hint: "[account or person] [interaction or purpose]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Identify the recipient and interaction from `$ARGUMENTS` and context. Resolve the person/account before drafting. If "latest meeting" is ambiguous or an attendee is unknown, clarify the specific thread or meeting.

Read the relevant meeting/email source or supplied transcript, recent relationship context, and open commitments. Retrieve `get_my_writing_style`, a small relevant sample from `get_my_sent_email_examples`, and the recipient's communication profile when available. Reuse tone and structure; never copy unrelated private content from sample emails. If style data is unavailable, use a concise neutral draft and say so outside the message.

Extract only actual decisions and commitments. Preserve who promised what. Distinguish an agreed deadline from a suggested date; do not turn a question into a commitment, or say an attachment is included when no attachment exists. Address unresolved obligations before making a new ask.

Return:

- A subject and ready-to-edit message with one clear next step.
- A short internal evidence note with links/IDs for the commitments and material claims.
- Any unresolved recipient, promised asset, or deadline that must be verified before sending.

Use the requested length and channel. Omit unsupported praise, manufactured urgency, and unapproved customer proof. The deliverable is a draft in the conversation; neither "follow up" nor "write an email" alone requests delivery. If sending is explicitly requested, apply the shared action boundary and report its actual supported status.
