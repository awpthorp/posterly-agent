# posterly Claude plugin + MCP directory submission

Human checklist for shipping the official Claude plugin listing and finishing MCP connector directory steps (including PR #309 follow-up on the main posterly app).

## Claude plugin directory

### Preflight (required)

From this repo root (`posterly-agent`):

```bash
claude plugin validate . --strict
```

Must exit 0. Fix any YAML or manifest issues before submitting.

Also sanity-check:

- [ ] Public GitHub repo: https://github.com/awpthorp/posterly-agent
- [ ] `plugin.json` version is `1.3.0` (or newer) with 18-platform copy
- [ ] Root `SKILL.md` and `skills/posterly/SKILL.md` are identical
- [ ] `.mcp.json` bundles `posterly-mcp-server@latest` with `${user_config.api_key}`
- [ ] `skills/setup/SKILL.md` exists for `/posterly:setup`
- [ ] README install commands match marketplace naming:
  - `/plugin marketplace add awpthorp/posterly-agent`
  - `/plugin install posterly@posterly-agent`

### Submit the plugin

Submit through one of Anthropic's official entry points (URLs change; use whichever is live):

- https://platform.claude.com/plugins/submit
- https://claude.ai/admin-settings/directory/submissions/plugins/new
- Form shortcut: https://clau.de/plugin-directory-submission

Suggested form answers:

| Field | Value |
| --- | --- |
| Name | posterly |
| Repo | https://github.com/awpthorp/posterly-agent |
| Homepage | https://www.poster.ly/agents |
| Description | Schedule and manage social posts across 18 platforms via MCP and the posterly CLI |
| Categories | Productivity, Social media, Automation |
| Auth | API key (`pst_live_...`), $3/mo API add-on |

### After listing

- [ ] Smoke install in a clean Claude Code session
- [ ] Confirm plugin userConfig API key unlocks MCP tools
- [ ] Confirm `npx -y @posterly/cli@latest doctor --pretty` still works with the same key

---

## MCP Connectors Directory (PR #309 follow-up)

PR #309 on the main posterly app covers OAuth Dynamic Client Registration (DCR) and related MCP connector readiness. The plugin repo alone is not enough for the connectors directory.

### When PR #309 is merged

1. **Apply OAuth DCR migration**

   ```bash
   supabase db push
   ```

   Only after the PR is merged and the migration is reviewed. Do not run production DDL from this plugin repo.

2. **Verify production site URL**

   - `NEXT_PUBLIC_SITE_URL=https://www.poster.ly`

3. **Create a comped reviewer account**

   - Active posterly subscription
   - API add-on enabled
   - At least one connected social account
   - Share credentials only through Anthropic's secure reviewer channel if requested

4. **Submit to the MCP connectors directory**

   - https://clau.de/mcp-directory-submission
   - Fallback email: mcp-review@anthropic.com

5. **Reference materials for reviewers**

   - Hosted MCP: `POST https://www.poster.ly/api/mcp`
   - Stdio package: `npx -y posterly-mcp-server@latest`
   - Marketing: https://www.poster.ly/mcp
   - Agents: https://www.poster.ly/agents
   - Docs: https://www.poster.ly/docs

### Connector smoke checks

- [ ] `GET https://www.poster.ly/api/mcp` returns server info without auth
- [ ] Authenticated `tools/list` succeeds with a live API key
- [ ] OAuth / DCR paths work in production after migration
- [ ] Rate limit and billing handoff headers still surface upgrade URLs

---

## Related main-app work (not in this repo)

- Docs page for Claude plugin install
- Cross-links from MCP and CLI docs
- Keep root `SKILL.md` in the main monorepo in sync with this package
- Plan: `plans/017-claude-plugin-directory.md` in the main posterly repo

## Do not

- npm publish from this checklist (CLI and MCP packages are separate)
- Commit API keys or reviewer passwords
- Push production Supabase migrations without the normal app release process
