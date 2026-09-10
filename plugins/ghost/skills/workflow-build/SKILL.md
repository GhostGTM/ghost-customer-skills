---
name: workflow-build
description: Build a new Ghost workflow from a goal: plan the stages, create the cards with bindings and success criteria, validate, run a sample, publish, and arm the schedule. Use for "make this recurring", "build a workflow that..."; use workflow-run to operate one that exists.
argument-hint: "[goal in one sentence] [cadence and destination if known]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Workflows exist only in the Ghost API: this needs `GHOST_API_KEY` with both `workflows:read` and `workflows:run`, and the key owner becomes the workflow's author. Without a key, produce the plan and the card list as a handoff.

Every mutation is a `POST /operations` call with the user's words as `reason` and a fresh `Idempotency-Key`; poll the receipt and read `result` before continuing. Reads go through `POST /query`. Builder calls use `workflows.builder.<tool>` with `{ workflowId, arguments: { ...toolFields } }` as the outer arguments, including `{}` for no-input tools. There are four confirmation gates; everything else runs without asking.

**1. Goal and plan (gate one).** Restate the goal as the outcome the user will read, the cadence, and the destination. Confirm, then `workflows.create` with `name` and `template: "blank"`, `workflows.builder.set_workflow_goal`, and `workflows.builder.plan_workflow_stages` with the goal. Use `describe_systems` and `search_workflow_fields` to learn which system holds each field before designing cards.

**2. The cards (gate two).** Present the full card list once, in execution order, and one yes applies all of them. Each card: `id` (kebab-case), `kind`, `icon` (from the catalog enum), `title`, `col`, `row`, `operation` or an `intent` with `tools` for an open card, `params`, `success_criteria`, and `connect_from`. Kinds: `source`, `rule`, `enrich`, `gather`, `ai_judgment`, `ai_generation`, `context_doc`, `human_gate`, `action`, `notify`. Operations include `load_accounts`, `load_calls`, `filter_untouched`, `filter_by_activity`, `merge_dedupe`, `find_people`, `resolve_account_cohort`, `load_account_facts`, `load_account_activity`, `classify_icp`, `apply_ai_fields`, `select_contacts`, `research_accounts`, `ground_context`, `generate_sequence`, `compose_report`, `upsert_graph_entities`, `write_hubspot_records`. The catalog's `validate_workflow` output and the operation list in the builder tool are authoritative.

Ordering rules the server and the run judge enforce: select before qualify, qualify before anything that spends, ground before generate, rank before cap, and a `human_gate` immediately before every `action` or `notify` card. Send `connect_from` as an array of `{ "from": "<existing step id>", "style": "default" }` objects, not strings. Execution order comes from `connect_from`, not from the order cards were created. A success criterion states only what the card guarantees; an overstated one halts correct runs.

Apply with `workflows.builder.upsert_workflow_step` per card and `bind_card_fields` for pinned fields, then `configure_workflow` for `schedule` (`trigger`, `enabled`, `days`, `time`, `timezone`, `refresh`) and `deliveries`. Run `validate_workflow` and fix every error before moving on; show warnings.

**3. Sample run (gate three).** Confirm, then `workflows.builder.start_workflow_run` with `fidelity: "sample"` and `user_said` copied verbatim from the `reason` you send; the server rejects consent it cannot find in `reason`. Sample runs never execute outward cards. Poll `workflows.state`, then read `get_test_run_digest` and `workflows.rows` for the output card. Show the user real rows and the judge's notes, and repair cards before publishing.

**4. Publish and arm (gate four).** Confirm, then `publish_workflow` with `confirm: true` (refused until validation is ready), then, for a recurring or event cadence, `set_workflow_live` with `live: true` or `workflows.set_schedule` with `enabled: true`. A manual workflow is published for on-demand runs and has no schedule to arm. Report the schedule summary the server returns; `definition.schedule.enabled` alone does not arm anything.

Report the workflow id, version, schedule, delivery, and what a full run will do that the sample did not. Do not start a full run or send a deliverable unless asked; those are workflow-run actions with their own consent.
