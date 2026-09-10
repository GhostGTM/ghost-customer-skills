---
name: context-update
description: Create or revise a Ghost context-library entry (ICP, persona, product, use case, competitor, case study, proof point, resource) or the company overview, from a brief, a document, or evidence. Use when the user wants Ghost's definitions changed; use context-audit-style reads when they only want to inspect them.
argument-hint: "[entry type] [name] [what to set or the source material]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. This is a confirmed action. Establish from `$ARGUMENTS` the entry type, the name, and the material: the user's brief, an attached document, or Ghost evidence the entry should reflect.

Read before writing. List the type with the matching `list_*` tool or `list_context` and find any existing entry with the same or a near name. Context upserts on MCP match on `name` within the workspace, so a spelling difference creates a duplicate and an exact match overwrites. Show which will happen. For an update, quote the current fields you will change.

Draft the entry in full, in Markdown only (no JSON or code fences in `overview`). Field sets:

- use_case: `name`, `overview`; use API `context.apply_entity` with `kind: "use_case"` because MCP has no use-case upsert
- product: `name`, `description`, `overview`
- persona: `name`, `title`, `department`, `overview`
- icp: `name`, `industry`, `company_size`, `revenue`, `employee_count_min`/`max`, `revenue_min`/`max`, `headquarters[]`, `technologies[]`, `domain`, `overview`
- competitor: `name`, `domain`, `description`, `overview`
- case_study: `name`, `customer_name`, `industry`, `overview`
- proof_point: `name`, `statement`, `category`, `source_url`, `overview`
- overview or user profile: the full replacement text for `update_overview` or `update_user_profile`

Ground every claim: if the entry is derived from calls or documents, cite the sources in the overview's own words, and keep another customer's quote out of a shareable asset unless the workspace marks it approved.

Show the payload and wait for a yes. Then write:

- MCP first: `upsert_product`, `upsert_persona`, `upsert_icp`, `upsert_competitor`, `upsert_case_study`, `upsert_proof_point`, `update_overview`, `update_user_profile`. These need an owner or admin role. `generate_icp` drafts and writes an ICP from workspace context in one call; treat it as a write and confirm it the same way.
- API chosen in advance for an analyst, use case, or resource, after the helper verifies the intended workspace/user and the catalog grants access: `context.apply_entity` with `kind`, `name`, the fields accepted by that operation's live schema, and `id` for an update (the API matches on `id`, not name). Do not copy MCP-only fields into the API payload; put unsupported descriptive material in `overview`. Resources use `kind: "resource"` with `url`, `resource_type`, `content`.

Read back the entry after the write and confirm one non-empty body before reporting the returned result. On an error, report it and stop. One confirmation covers one entry; a batch is confirmed as a list, then written one at a time, stopping at the first error.
