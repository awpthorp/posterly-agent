---
name: setup
description: Guided posterly setup. Create an API key, set POSTERLY_API_KEY in Cursor plugin config, run doctor, and list connected accounts.
---

# posterly setup

Use this command when the user runs `/setup` or asks to connect posterly in Cursor for the first time.

## Goal

Get a working `POSTERLY_API_KEY` in Cursor plugin config, verify CLI access, confirm connected social accounts, and prefer MCP tools for day-to-day work.

## Steps

### 1. Sign up and connect an account

1. Open [poster.ly](https://www.poster.ly) and sign in (or create an account).
2. Connect at least one social account in the dashboard.

### 2. Create an API key

1. Open **Dashboard -> Settings -> API Keys** (or [Dashboard -> API & MCP](https://www.poster.ly/dashboard/api)).
2. Enable the **$3/mo API add-on** if it is not already active.
3. Create a key. It starts with `pst_live_`. Show the full key only once; store it securely.

### 3. Set the key in Cursor

1. Open **Plugins -> Configure** for the posterly plugin.
2. Set `POSTERLY_API_KEY` to the new key.
3. The bundled `mcp.json` injects it into the local MCP server. Do not put the key in git.

### 4. Run doctor

```bash
npx -y @posterly/cli@latest doctor --pretty
```

Doctor checks Node, API origin, that a key is configured, and that `/api/v1/whoami` succeeds. Fix any failures before continuing.

### 5. List connected accounts

```bash
npx -y @posterly/cli@latest accounts:list --pretty
```

If the list is empty, send the user to connect accounts in the dashboard or use MCP/CLI connect handoff (`connect:link` / `get_connect_link`).

### 6. Prefer MCP when available

After setup, prefer MCP tools first: `whoami`, `list_accounts`, `create_post`, `upload_media`, analytics, and GBP tools. Fall back to `npx -y @posterly/cli@latest ...` when a shell is available but MCP is not.

## Human in the loop

Confirm with the user before:

- Publishing immediately (publish now)
- Deleting posts or post groups
- Disconnecting accounts
- Posting or deleting Google Business review replies
- Spending AI credits (image/video generation)
- Any CLI command that requires `--confirm`

## Smoke checklist

- [ ] `POSTERLY_API_KEY` is set in Plugins -> Configure
- [ ] `npx -y @posterly/cli@latest doctor --pretty` exits 0
- [ ] `accounts:list` shows at least one connected account (or user knows how to connect)
- [ ] User understands human-in-the-loop rules

## Links

- Agents: https://www.poster.ly/agents
- MCP: https://www.poster.ly/mcp
- CLI: https://www.poster.ly/cli
- Docs: https://www.poster.ly/docs
