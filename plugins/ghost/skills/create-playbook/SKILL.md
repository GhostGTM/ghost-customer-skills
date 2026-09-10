---
name: create-playbook
description: Create or refine a reusable customer-specific Claude Code skill for a repeated Ghost workflow. Use when a customer wants to save their methodology as a playbook, not when they only want to run an existing task once.
argument-hint: "[repeated job and desired deliverable]"
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md` and `${CLAUDE_PLUGIN_ROOT}/references/authoring-playbooks.md`.

Use `$ARGUMENTS`, the user's demonstrated workflow, and any supplied methodology to define the skill. Establish the customer project/output location, repeated trigger, required inputs, deliverable, and decisions that need customer-specific guidance. Ask only about missing requirements that materially change it; do useful drafting while they answer.

Check the advertised Ghost tools before binding the skill to capabilities. If Ghost is unavailable, create a draft that names capability requirements and runtime checks, without promising successful live execution. Do not invent a workflow API or use the historical server-side `skills` table as though it were a Claude plugin catalog.

Write the customer skill into their specified location or `.claude/skills/<customer-job>/` in the confirmed customer project. Keep runtime references self-contained, account examples synthetic, and changing customer data out of the instructions. Do not edit the installed Ghost plugin or make the new skill depend on its cache path.

Include a normal, incomplete-evidence, and ambiguous/out-of-scope scenario. Run the available structural validator and report whether behavioral testing actually occurred. Return the path, invocation, output contract, tool prerequisites, and any remaining assumptions. A created local playbook is not published or synchronized to other customers.
