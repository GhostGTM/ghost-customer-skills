---
name: graph-update
description: Correct or add to the Ghost graph: a person's title or status, a new contact on an account, a relationship between people, a fact, an empty firmographic field, or a workspace label or a selected context match. Use for a small account/contact correction, "that's wrong in Ghost" and "record this"; use context-update for the context library and CRM tools for CRM fields.
argument-hint: "[account or person] [what to change or record]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. This is a confirmed action and it needs `GHOST_API_KEY` with the `graph:write` grant; MCP has no graph-correction tools. Without a key, prepare the exact change as a handoff.

Claude Code can investigate a small correction using ordinary graph/source reads and live CRM reads when granted, then submit the explicit edit itself. The user need not supply the final value before that investigation. This direct path needs no Gemini run, `graph.agent_preview`, or `research:run` grant and has no Ghost model charge; normal API fees apply. A returned receipt can still complete asynchronously.

Read the current state first so the change targets real rows: `search_accounts` for the account, `find_person` or `get_account_network` for the person id, `get_deal_context` for a deal id, `read_source` for a source id. Quote the before value.

Resolve identifier types against the live operation catalog. For `person_field`, `attendance_correction`, and contact `workspace_label` changes, the field named `person_id` takes the account membership row's **`account_people.id`**, not the canonical person's `person_id`. Relationship endpoints of kind `account_person` also take `account_people.id`; endpoints of kind `customer` and the outer `customer_id` take `customers.id`. `source_id` and `link_source_ids` take `customer_sources.id`. Verify that each row belongs to the intended account and workspace before presenting the payload; never substitute a similarly named id.

Build one `graph.apply_update` (writes immediately) or `graph.propose_update` (leaves a proposal for review in the app) with `customer_id`, a `summary` under 300 characters, and `changes[]`. Every change requires `kind` and a human-readable `target_label`, plus the fields below. Keep `changes` to at most ten items. Kinds and what each needs:

- `person_field`: `person_id`, `field` (name, title, role_inferred, status, department, is_champion, email, linkedin_url, headline, location), `after`. Booleans as the strings `"true"` or `"false"`.
- `add_person`: `target_label` (full name) plus any of title, email, linkedin_url, department, headline, location; `link_source_ids` to connect the person to the calls they came from.
- `add_relationship`: `from_entity_id` and `from_entity_kind`, `to_entity_id` and `to_entity_kind` (`account_person` or `customer`), `relation_type` (introduced, connected_to, knows, reports_to, worked_with, referred, advises, works_at), and the user's `statement`.
- `relation_edit`: selected context matches with exact `from_entity_id`/kind, `to_entity_id`/kind, `relation_type`, `mode`, and `statement`. Resolve allowed endpoint kinds, relation names, and add/retire/replace requirements from the live catalog; context IDs are not names. Explicit removal/replacement affects existing matches and needs that exact change shown and approved.
- `fact`: free-text context on the account in `statement`; `fact_comment` to annotate an existing fact, with `target_fact_id` on the outer operation arguments (not inside the change).
- `account_field`: `field` (domain, industry, employee_count, hq_city, hq_country, growth_stage), `after`, and `enrichment_source` when the value came from outside. Put the scalar value in `after`; any evidence belongs separately in `statement`. Fills empty fields only; it never overwrites an existing first-party value.
- `attendance_correction`: `person_id` and `source_id` when someone was recorded on a call they did not attend.
- `workspace_label`: `label_name`, `entity_kind` (account or contact), `person_id` for a contact. Needs the `admin` grant and an owner or admin membership.
- `deal_note` and `deal_field`: `hubspot_deal_id` from `get_deal_context`, with `statement` or `field` and `after`. Deal status changes are refused here; they are CRM operations.

Show the change list as before and after rows, say whether it will apply now or wait for review, and obtain or use the user's existing approval for that exact change. Submit with `POST /operations`, a fresh `Idempotency-Key`, and the user's words as `reason`. Poll the receipt. `succeeded` with a result means applied; `needs_review` requires inspecting the result before deciding which changes remain unapplied; `outcome_unknown` means read the target again before retrying.

Read the row back and compare its stored value with the intended `after` value before reporting a verified update. If they differ, report the mismatch and preserved receipt, inspect the actual state, and stop; never automatically replay the run, clear the field, or treat an approved proposal as proof of the intended value. Do not batch unrelated accounts into one operation, and stop at the first error.

For a job that needs an agent to inspect connected sources and populate fields across accounts, route to `graph-agent`: Claude scopes and gets approval, then Gemini executes the edits. Do not route delegated execution to a proposal-only loop.
