---
name: meeting-prep
description: Prepare a seller or customer-success manager for a specific meeting with a Ghost account. Use for pre-call context, agendas, discovery questions, and a grounded next-step ask.
argument-hint: "[account or attendee] [meeting purpose]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Establish the account, meeting purpose, and any supplied attendees/date from `$ARGUMENTS` or the conversation. Ask about purpose only if the available context does not support a useful preparation brief. Do not imply calendar access unless an appropriate tool is connected.

Resolve identities. Read focused account context, the relevant deal context, and recent touchpoints. Check `get_open_commitments` so the user knows what they promised before asking for more. Retrieve product/persona/proof context only for the actual meeting topic.

Identify the decision this meeting should advance. Separate what the customer already said from questions still worth asking. If preparing a renewal, inspect value delivered, unresolved obligations, contract timing evidence, and stakeholder continuity. For discovery, identify what would validate or falsify fit.

Deliver a usable prep card:

1. Desired outcome and a suggested opening grounded in the last interaction.
2. Attendees, known relationship context, and role/authority unknowns.
3. What changed, what was promised, and what must be addressed.
4. A short agenda with three to five targeted questions tied to evidence gaps.
5. Likely objections supported by history, relevant approved proof, and a concrete next-step ask.

Attach sources to the internal preparation notes, not to words the user is meant to say verbatim. A generic list of discovery questions is insufficient when customer history exists. Do not book the meeting, contact attendees, or generate extra paid research unless requested.
