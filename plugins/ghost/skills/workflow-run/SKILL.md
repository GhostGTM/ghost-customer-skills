---
name: workflow-run
description: Operate an existing Ghost workflow: see its state, runs, rows, and artifacts; start a run; resume or approve a gate; pause or arm the schedule; archive. Use for "did my workflow run", "approve the gate", "turn it off"; use workflow-build to create one.
argument-hint: "[workflow name] [what to check or do]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`. Workflows exist only in the Ghost API: reads need `GHOST_API_KEY` with `workflows:read`, mutations need `workflows:run`, so a read-then-write task needs both grants. Publishing, go-live, and schedule changes require the workflow author; runs and archiving also allow workspace admins. Builder calls use `workflows.builder.<tool>` with `{ workflowId, arguments: { ...toolFields } }` as the outer arguments. Without a key, say so and stop.

Find the workflow with `workflows.list` (paged with `cursor`) and `workflows.get`; show candidates if the name is ambiguous. `access.canEdit` indicates edit access, not permission to publish, arm, or run; check the operation-specific authorization too.

**Reads, no confirmation.** `workflows.state` for the latest run or a given `runId`: status, cursor step, halted reason, per-step status, deliveries, model cost. `workflows.runs` for history. `workflows.rows` with the output id, `page`, and `pageSize` for the table a step produced; the newest step with rows is found by following edges, not by list position. `workflows.artifact` with `workflowId` and `runId` for the stored result; its `outputId` identifies the table for `workflows.rows`. `workflows.schedule` for cadence and health (`on`, `off`, `paused`, `degraded`). `workflows.builder.read_workflow_run_log` for a failing step's notes, and the step `verdict` / `verdictReasoning` from `workflows.state` for the judge's result. `get_test_run_digest` only supports legacy `kind: "test"` runs. An orchestrated sample has `kind: "full"` and `fidelity: "sample"`; use its state and artifact and do not mistake the kind for authorization to deliver.

Explain a halt from the log and the step's success criterion before proposing a change. A run waiting at a `human_gate` needs a decision, not a restart.

**Mutations, each confirmed.** State the workflow, the action, and what it will touch, then wait for a yes. Submit with `POST /operations`, the user's words as `reason`, and a fresh `Idempotency-Key`; poll the receipt.

- Start a run: `workflows.builder.start_workflow_run` with `fidelity` and `user_said` copied verbatim from the actual approval in `reason`. Bare run or test approval means `sample`. Full requires explicit real/full/live run or delivery approval; never promote sample consent to full. The direct `workflows.run` route has the same consent/readiness checks and defaults to sample. Full runs execute outward cards behind approved gates; say so.
- Approve or reject a gate: `workflows.review_gate` with `runId`, `decision`, and a `note`. Show what the gate protects (the rows and the outward card) before asking.
- Resume a paused run: `workflows.resume`. Continue a long-run checkpoint: `workflows.continue`.
- Pause or arm the schedule: `workflows.set_schedule` with `enabled`. Arming refuses when the definition has no cadence or a connector is not ready; report the server's reason.
- Send a deliverable: `workflows.builder.draft_deliverable_send` drafts first; a second call with `send_now: true` and `user_said` sends. Two separate confirmations.
- Archive: `workflows.archive` turns the schedule off and hides the workflow; not reversible from here.

Report the receipt's result verbatim. On `outcome_unknown`, read the state of the exact target: `workflows.schedule` for schedule changes, `workflows.state` for runs, and the deliverable's delivery history for sends. If the requested effect already happened, report it and do not resubmit. Do not edit cards from this playbook; route definition changes to workflow-build so validation runs.
