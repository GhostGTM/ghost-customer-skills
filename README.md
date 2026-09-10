# Ghost customer skills for Claude Code

This is Ghost's customer plugin marketplace for Claude Code. Version 0.2.0 includes 23 playbooks for account research, meeting preparation, product context, graph corrections, and workflows.

## Install

Run inside Claude Code:

```text
/plugin marketplace add GhostGTM/ghost-customer-skills
/plugin install ghost@ghost-customer-skills
/reload-plugins
```

Open `/mcp`, authenticate the plugin's Ghost connection to your workspace, then run `/ghost:start`. Workflow authoring and operations also need `GHOST_API_KEY` with both `workflows:read` and `workflows:run`; see the [customer guide](plugins/ghost/README.md) for all grants.

To update, refresh `ghost-customer-skills` in `/plugin` marketplaces, update the installed Ghost plugin, then run `/reload-plugins`.

## Local development

From this marketplace directory, preview it without installing:

```sh
claude --plugin-dir ./plugins/ghost
```

In that session, use `/mcp` to authenticate the plugin's Ghost server, then `/ghost:start`.

To install from the local marketplace, run these inside Claude Code from this marketplace directory:

```text
/plugin marketplace add .
/plugin install ghost@ghost-customer-skills
/reload-plugins
```

See the [customer guide](plugins/ghost/README.md) and [acceptance scenarios](evals/acceptance.md).

## Maintain the library

Each folder in `plugins/ghost/skills` is one customer job. Keep its description specific, give it a concrete deliverable, and route it to the shared [Ghost usage contract](plugins/ghost/references/working-with-ghost.md). Tool names in that contract are discovery hints, not a frozen API schema. Confirm capabilities against the connected server before use.

To add a skill, follow [the authoring guide](plugins/ghost/references/authoring-playbooks.md). Keep all runtime references within the plugin directory so installation into Claude's cache works. Keep customer account data and private customer playbooks out of this distributable package.

Run from this marketplace directory:

```sh
claude plugin validate . --strict
claude plugin validate ./plugins/ghost --strict
claude plugin validate ./plugins/ghost/skills --strict
```

Run the acceptance scenarios against synthetic fixtures before each release, then a designated test workspace for OAuth, real tool schemas, and evidence links. Manifest validation alone does not verify model behavior or server capabilities.

## Distribution

The customer marketplace is [GhostGTM/ghost-customer-skills](https://github.com/GhostGTM/ghost-customer-skills). Its root contains this directory's distributable files, including `.claude-plugin/marketplace.json` and `plugins/ghost`. Publish only this package; the private web application and internal design documents are not part of the distribution.

The plugin manifest owns the version. Bump it for customer releases and test upgrading an installed copy. Ship private customer playbooks through a separate customer-controlled project or private marketplace so upstream updates do not overwrite them.
