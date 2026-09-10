# Ghost for Claude Code

Use your account history, customer conversations, commitments, and product context inside Claude Code.

## Connect

After loading or installing the plugin, open `/mcp`, select the plugin's Ghost connection, and complete the browser sign-in for the intended Ghost workspace. Then run `/ghost:start`. MCP credentials stay in Claude's authentication flow; this package contains no API keys.

If Ghost is already connected separately, distinguish the existing connection from the plugin connection in `/mcp`. Authenticate and use one connection for the intended workspace. Do not assume a second connection belongs to the same workspace.

## Choose a playbook

| Command                                                    | What you get                                              |
| ---------------------------------------------------------- | --------------------------------------------------------- |
| `/ghost:start`                                             | Connection check and a suggested first task               |
| `/ghost:account-brief Acme`                                | What matters about an account now, with sources           |
| `/ghost:meeting-prep Acme renewal discussion`              | Meeting objective, context, questions, and next-step ask  |
| `/ghost:follow-up Acme latest meeting`                     | A grounded email draft in your voice                      |
| `/ghost:deal-review Acme renewal`                          | Evidence-based deal assessment and next moves             |
| `/ghost:stakeholder-map Acme`                              | Known relationships, buying roles, and coverage gaps      |
| `/ghost:commitments Acme`                                  | Open promises, owners, dates, and overdue items           |
| `/ghost:reconnect my dormant relationships`                | Reconnection candidates and relevant message drafts       |
| `/ghost:prioritize-accounts my renewals this month`        | An explained, bounded account action queue                |
| `/ghost:expansion-plan Acme`                               | Evidence-backed expansion hypotheses and validation steps |
| `/ghost:voice-of-customer enterprise onboarding friction`  | Customer themes, source quotes, and coverage limits       |
| `/ghost:call-recap Acme last pricing call`                 | The transcript, a recap, or what a person said, verbatim  |
| `/ghost:renewal-prep Acme FY27`                            | Commercial facts table, objection history, and the ask    |
| `/ghost:customer-lookup which customers use our API`       | A filtered account list with evidence and coverage        |
| `/ghost:segment-accounts tier 1 accounts against our ICPs` | Fit per account and criterion, cohort comparison          |
| `/ghost:proof-finder onboarding time savings`              | Case-study and reference candidates with customer quotes  |
| `/ghost:competitive-intel Contoso this year`               | Competitor mentions, displacement, and lost-deal reasons  |
| `/ghost:create-playbook our renewal review`                | A reusable customer-specific Claude Code skill            |

Playbooks that write to Ghost show the exact payload and wait for your yes:

| Command                                                    | What it writes                                                                         |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `/ghost:context-update persona "Head of RevOps"`           | A context-library entry or the overview, created or updated                            |
| `/ghost:add-source Acme paste of yesterday's call`         | A transcript, note, thread, or brief saved on the account                              |
| `/ghost:graph-agent this cohort reconcile titles from CRM` | Claude plans; Ghost analyzes approved sources and applies scoped graph edits (API key) |
| `/ghost:graph-update Acme Jane is now VP Operations`       | A person, relationship, fact, firmographic gap, or label in the graph (API key)        |
| `/ghost:workflow-build weekly renewal risk digest`         | A new workflow: plan, cards, validation, sample run, publish, schedule (API key)       |
| `/ghost:workflow-run renewal digest approve the gate`      | Run, resume, approve, pause, or archive an existing workflow (API key)                 |

These names also support natural-language discovery. Example names above are fictional.

## Optional: an API key for pipeline, graph writes, and workflows

Some jobs need the Ghost developer API: a deal list for your book or quarter, deterministic account filters, recent calls by attendee, lookalikes, graph corrections, and everything about workflows. An owner, admin, or analyst can mint a key in the web app's Dev tab. Set it as `GHOST_API_KEY` in the environment that launches Claude Code without pasting it into chat or committing it. The API helper requires Python 3.11+ and verifies the key's workspace and user before customer-data requests. Use only the grants needed for the job, and revoke the key in the Dev tab when it is no longer needed. Grants by job: `graph:read` for reads, `graph:write` for context and graph writes, both `workflows:read` and `workflows:run` for building and operating workflows. The playbooks never print the key, confirm before any write or spend, and fall back to asking you for scope when the key is absent.

For a small account or contact correction, `/ghost:graph-update` lets Claude Code read evidence and apply the exact edit directly. No managed AI run or Ghost model charge is required; normal API fees apply. For delegated batch reconciliation, `/ghost:graph-agent` has Claude plan the scope and budget, then Ghost executes the approved work. That path permits owners, admins and analysts with `graph:read`, `graph:write` and `research:run`; add `crm:read` for live CRM queries. It does not need `admin`. The older `/compute/*` refresh endpoints require both `admin` and an owner/admin workspace role.

If an existing developer key is missing a grant, a Ghost system administrator can update it without rotating its secret. Provide the workspace, key name/ID and requested grants, never the secret. The current Dev page supports create and revoke, not editing grants. Run `/ghost:start` again after the update to recheck identity and access.

## What to expect

Most playbooks read Ghost and produce answers or drafts. The write playbooks above can change the context library, save sources, correct the graph, and build or operate workflows; each shows the exact payload and waits for your yes, and workflow runs and deliveries also pass Ghost's own gates (validation before publish, a human gate before anything outward, your words recorded as consent). Research and follow-up playbooks produce drafts. Approved full workflows and deliverable sends can send email or Slack messages, write CRM records, and update configured sheets, trackers, or context documents. An enabled schedule can repeat those effects in future runs. Treat `workflows:run` as permission to operate that automation, and review its destinations, rows, and actions before approving. Sample runs suppress outward effects but can still consume API, model, and judge usage.

The plugin is guidance, not a server permission boundary. Ghost enforces API grants, workspace and workflow access, and its runtime gates; Claude controls local tool permissions. Approval words are recorded as the caller’s assertion of intent, not independent proof that a human clicked approval. Keep Claude’s normal permission checks enabled; do not broadly auto-allow shell or MCP writes to make onboarding easier.

Ghost data retrieved by a playbook enters your Claude session and is subject to your organization’s Claude account, retention, and data-use settings. API request files and generated artifacts are local copies of that data. The package includes one on-demand API request helper; it installs no hooks or background processes and collects no separate telemetry.

Available context depends on your workspace's connected data. A missing source, incomplete cohort, or historical CRM snapshot is labeled rather than filled in. The assistant asks for clarification when an account or person is ambiguous.

To customize a repeated workflow, use `/ghost:create-playbook` in your customer project. Keep stable methodology in your skill; retrieve changing account and product information from Ghost when it runs. Your custom skills remain separate from this plugin's updates.

This package targets Claude Code. Installation and authentication in other Claude surfaces have not been validated for this release.

Live CRM validation uses the separate `crm:read` grant; confirmed CRM writes use `crm:write`. Neither implies the other. Account detail includes firmographics, and contact detail includes provenance and CRM IDs. The API also exposes ICPs and the other context areas as paginated resources. For Ghost-managed AI analysis, grant `graph:read`, `graph:write`, and `research:run`, adding `crm:read` only when the plan reads CRM. Claude shows the scope and model-credit cap for approval, then Ghost executes directly and reports verified edits and gaps. API fees are separate from model usage; user-requested analysis work is recorded separately from ingestion.
