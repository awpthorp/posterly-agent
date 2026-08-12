---
name: setup
description: >-
  First-time posterly connect. Probe for an existing key, then onboard with
  agent signup, CLI login, or human pages. Never collect cards or passwords.
disable-model-invocation: true
---

# posterly setup

Use this skill when the user runs `/posterly:setup` or asks to connect posterly for the first time.

## First run

Probe once. If MCP `whoami` or `npx -y @posterly/cli@latest doctor --pretty` succeeds, skip onboarding. Never start signup. Never ask the user to paste a key they already have. Prefer MCP tools for day-to-day work after the probe succeeds.

If the probe fails, posterly is a social scheduler. API and MCP access need a paid plan plus the $3/mo API add-on. Never collect card numbers, posterly passwords, or social passwords. Payment and password setup stay in the user's browser.

Signup APIs never return a `pst_live_` key. Do not dump raw JSON. Narrate progress in plain language.

### Path 1: agent signup (preferred when public MCP signup tools exist)

1. Call `get_agent_signup_info`.
2. Ask the user for their email, then call `start_signup` with the Starter plan and `api_addon=true`.
3. Send them `checkout_redirect_url` so they can pay in the browser.
4. Poll `get_signup_session` and tell them what is happening (checkout pending, payment confirmed, password required, agent access required).
5. When status is `agent_access_required`, ask them to copy the dashboard setup instructions or API key into this chat, plugin config, or `POSTERLY_API_KEY`.

### Path 2: CLI login (shell, existing or new account)

```bash
npx -y @posterly/cli@latest auth:login
npx -y @posterly/cli@latest doctor --pretty
```

### Path 3: human pages

- New users: https://www.poster.ly/agents/signup
- Existing users: https://www.poster.ly/dashboard/api
- Then paste the key into chat, env, or plugin config.

### After auth

1. Call `whoami`.
2. Ask which social account to connect first.
3. Use `create_connect_session` or `connect:link`, send the connect URL, and poll until connected.
4. Help schedule the first post.

If doctor or whoami failed, stay on this script. Do not invent a second setup.

## Human in the loop

Confirm with the user before:

- Publishing immediately (publish now)
- Deleting posts or post groups
- Disconnecting accounts
- Posting or deleting Google Business review replies
- Spending AI credits (image/video generation)
- Any CLI command that requires `--confirm`

## Smoke checklist

- [ ] Probe succeeded (`whoami` or `doctor --pretty`)
- [ ] At least one social account is connected, or the user has a connect URL
- [ ] User understands human-in-the-loop rules

## Links

- Agents: https://www.poster.ly/agents
- Agent signup: https://www.poster.ly/agents/signup
- MCP: https://www.poster.ly/mcp
- CLI: https://www.poster.ly/cli
- Docs: https://www.poster.ly/docs
