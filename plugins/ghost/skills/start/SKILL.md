---
name: start
description: Help a customer set up the Ghost plugin, check its connection, and choose a first playbook. Use for onboarding or a connection check, not an ordinary account question.
---

Read `${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md`.

Check whether a Ghost MCP connection and relevant tools are available. If sign-in is needed, guide the user through `/mcp` and the Ghost browser sign-in. Do not read secrets or silently edit their Claude configuration. If multiple Ghost connections exist, identify the intended workspace before fetching customer data.

Use authenticated metadata when available to identify the workspace; if the server does not expose it, say that and ask the user to verify the workspace in the connection flow. A listed tool is not proof of a successful authenticated read. Once a user names a known account, a narrow `search_accounts` call can verify usable account access without dumping their workspace.

If `GHOST_API_KEY` is set in the environment, run the bundled API helper’s `identity` command and report its workspace, user, and grants. Compare that identity with the intended MCP connection before combining either transport’s data; stop on a mismatch or unresolved identity. Never print the key. If it is absent, mention that pipeline and cohort jobs work best with a key minted in the web app's Dev tab, and leave it there.

For API setup distinguish stored graph reads (`graph:read`), Ghost edits (`graph:write`), direct live CRM reads (`crm:read`), and confirmed CRM writes (`crm:write`). CRM read and write are independent; never default to write merely to validate CRM data. Delegated Gemini graph execution needs `graph:read`, `graph:write`, and `research:run`, plus `crm:read` if its approved queries use HubSpot. The Gemini path permits owners, admins and analysts and does not need `admin`; the older `/compute/*` refresh paths require both `admin` and owner/admin membership. An existing key is not silently upgraded; report missing grants. A Ghost system administrator can apply an audited grant change to the same developer key without rotation; ask for the workspace and key name/ID, never the secret. The current Dev UI creates and revokes keys; it does not edit grants. After a grant update, rerun identity and capability discovery before resuming. Workflow execution is separate automation authority with the effects described in the shared contract.

Offer the first task that fits their role: meeting prep for a seller, renewal/deal review for customer success, or a scoped voice-of-customer question for an operator. If they already provided a task, continue it using the appropriate playbook's instructions.

Return connection status, any specific missing prerequisite, and at most three relevant command examples. Do not claim all connectors work because one Ghost lookup succeeds.
