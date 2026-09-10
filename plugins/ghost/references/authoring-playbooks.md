# Authoring customer playbooks

A useful playbook changes a decision: which account to act on, what to ask, which claim is defensible, or what needs verification. Start with a repeated customer job and the deliverable they actually use.

## Establish the contract

Capture the trigger, audience, input scope, required capabilities, deliverable, and a few success criteria. Ask only for details that change the workflow. Reuse the customer's existing methodology when supplied; do not impose MEDDICC, a numerical health score, or a standard sales process by default.

Separate three kinds of information:

- **Method:** durable steps, qualification criteria, output format. These belong in the skill.
- **Workspace context:** products, personas, approved proof, language, stage definitions. Retrieve these from Ghost at runtime.
- **Run inputs:** account IDs, meeting, date range, scope. Take these from the user's request and validate them at runtime.

## Create the files

For a local customer project, use `.claude/skills/<customer-job>/SKILL.md`, unless the user specifies another location. Resolve the actual customer project first; do not write into this installed plugin's cache. Inspect any existing skill before editing and preserve unrelated content.

Use lowercase hyphenated names and concise frontmatter:

```yaml
---
name: renewal-review
description: Review a named customer's renewal readiness using our renewal methodology and Ghost evidence. Use for preparing a renewal review, not a portfolio-wide forecast.
argument-hint: "[account] [renewal period]"
---
```

In the body, include the specific decision rules and deliverable. Consume `$ARGUMENTS` as task input, not shell commands. Preserve automatic discovery unless the user wants an explicit-only skill. Avoid auto-allowing tools through `allowed-tools` or adding hooks merely to avoid permission prompts.

Make the new skill self-contained: adapt the essential connection, identity, evidence, freshness, and action rules from `working-with-ghost.md`, either into its body or a reference copied inside the new skill directory. Use relative links to its own references. Do not leave `${CLAUDE_PLUGIN_ROOT}` references that would resolve to the wrong package, absolute author-machine paths, or dependencies on another installed skill's hidden instructions.

## Check usefulness

Exercise three realistic cases with synthetic data: a normal request, incomplete/conflicting evidence, and an ambiguous entity or out-of-scope action. Check the actual output against the deliverable contract. If no model execution is available, document these as pending scenarios; do not say they passed.

Use `claude plugin validate <skill-directory>` when available. This checks packaging, not whether the judgment is good. Report the new file path, invocation, assumptions, and which checks actually ran. Do not publish the playbook or sync it into Ghost without a user request.
