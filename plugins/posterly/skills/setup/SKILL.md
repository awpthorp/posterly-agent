---
name: setup
description: >-
  Guided posterly setup and onboarding for Claude Code: create an API key,
  configure env or plugin userConfig, run doctor, list connected accounts, and
  prefer MCP tools when available.
disable-model-invocation: true
---

# posterly setup

Use this skill when the user runs `/posterly:setup` or asks to connect posterly for the first time.

## Goal

Get a working `POSTERLY_API_KEY`, verify CLI access, confirm connected social accounts, and prefer MCP tools for day-to-day work.

## Steps

### 1. Get an API key

1. Open [poster.ly](https://www.poster.ly) and sign in (or create an account).
2. Connect at least one social account in the dashboard.
3. Open **Dashboard -> Settings -> API Keys** (or [Dashboard -> API & MCP](https://www.poster.ly/dashboard/api)).
4. Enable the **$3/mo API add-on** if it is not already active.
5. Create a key. It starts with `pst_live_`. Show the full key only once; store it securely.

### 2. Configure the key

**Claude Code plugin userConfig (preferred when this plugin is installed):**

- Set the plugin `api_key` field to the new key.
- The bundled `.mcp.json` injects it as `POSTERLY_API_KEY` for the local MCP server.

**Environment variable (CLI, CI, and non-plugin agents):**

```bash
export POSTERLY_API_KEY=pst_live_...
# optional; default is https://www.poster.ly
export POSTERLY_URL=https://www.poster.ly
```

Do not commit keys to git. Prefer shell env, secret managers, or plugin userConfig.

### 3. Run doctor

```bash
npx -y @posterly/cli@latest doctor --pretty
```

Doctor checks Node, API origin, that a key is configured, and that `/api/v1/whoami` succeeds. Fix any failures before continuing.

### 4. List connected accounts

```bash
npx -y @posterly/cli@latest accounts:list --pretty
```

If the list is empty, send the user to connect accounts in the dashboard or use MCP/CLI connect handoff (`connect:link` / `get_connect_link`).

### 5. Prefer MCP when available

When MCP tools are loaded (Claude Code plugin, Claude Desktop, Cursor, etc.):

- Use MCP tools first: `whoami`, `list_accounts`, `create_post`, `upload_media`, analytics, GBP tools.
- Fall back to `npx -y @posterly/cli@latest ...` when a shell is available but MCP is not.
- Use REST only when neither MCP nor a shell is available.

## Smoke checklist

- [ ] `POSTERLY_API_KEY` is set (or plugin `api_key` is configured)
- [ ] `npx -y @posterly/cli@latest doctor --pretty` exits 0
- [ ] `accounts:list` shows at least one connected account (or user knows how to connect)
- [ ] User understands human-in-the-loop rules: confirm before publish now, delete, disconnect, review replies, and any CLI `--confirm`

## Example prompts after setup

- "List my connected posterly accounts"
- "Schedule a LinkedIn post for tomorrow at 10am about our product launch"
- "Upload this image and draft an Instagram caption, then schedule it"

## Links

- Agents: https://www.poster.ly/agents
- MCP: https://www.poster.ly/mcp
- CLI: https://www.poster.ly/cli
- Docs: https://www.poster.ly/docs
