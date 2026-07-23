# posterly for Claude Code

Schedule, publish, and manage social content across **18 platforms** with [posterly](https://www.poster.ly) from Claude Code, other Claude surfaces that support plugins, and any agent that can run MCP or shell commands.

**Platforms:** Instagram, TikTok, LinkedIn, YouTube, X, Facebook, Threads, Pinterest, Google Business Profile, Telegram, Bluesky, Discord, Slack, Mastodon, Dev.to, Hashnode, WordPress, Lemmy.

## What it does

- List connected social accounts, brands, and brand voice profiles
- Upload media and create, schedule, update, pause, and repair posts
- Find open posting slots and avoid schedule collisions
- Pull account and per-post analytics
- Manage Google Business Profile reviews, replies, audits, and gallery media
- Generate AI captions, images, and video through posterly endpoints
- Monitor publish outcomes via activity feeds and webhooks

One API key unlocks three interfaces:

| Interface | Best for | Entry point |
| --- | --- | --- |
| MCP | Claude Code, Claude Desktop, Cursor | Bundled `.mcp.json` or `npx -y posterly-mcp-server@latest` |
| CLI | Terminal agents, scripts, CI | `npx -y @posterly/cli@latest` |
| REST | Everything else | `https://www.poster.ly/api/v1` |

## Install for Claude Code

Add the marketplace, then install the plugin:

```
/plugin marketplace add awpthorp/posterly-agent
/plugin install posterly@posterly-agent
```

When prompted, set your **posterly API key** (plugin userConfig). It is injected into the bundled MCP server as `POSTERLY_API_KEY`.

### Skills CLI (any skill-compatible agent)

```bash
npx skills add awpthorp/posterly-agent
```

Or copy [SKILL.md](SKILL.md) into your agent's skills directory manually.

### Guided setup skill

After the plugin is installed, run:

```
/posterly:setup
```

That walkthrough covers API key creation, env/userConfig, `doctor`, and `accounts:list`.

## Setup

1. Create a posterly account at [poster.ly](https://www.poster.ly) and connect your social accounts.
2. Enable API access ([Dashboard -> Settings -> API Keys](https://www.poster.ly/dashboard/api)). Requires the **$3/month API add-on** on any plan.
3. Give the key to Claude (plugin userConfig) or your shell:

```bash
export POSTERLY_API_KEY=pst_live_...
# optional override (default https://www.poster.ly)
# export POSTERLY_URL=https://www.poster.ly
```

4. Smoke test:

```bash
npx -y @posterly/cli@latest doctor --pretty
npx -y @posterly/cli@latest accounts:list --pretty
```

Global install is optional:

```bash
npm i -g @posterly/cli
posterly doctor --pretty
```

## Example prompts

- "List my connected posterly accounts"
- "Schedule a LinkedIn post about our launch for tomorrow at 10am"
- "Upload this image and create an Instagram post for Friday 9am"
- "Which of my recent posts failed, and what is missing?"
- "How did my Instagram account perform over the last 14 days?"
- "Suggest a reply to this Google Business review, then wait for my approval before posting"

## Human in the loop

- CLI commands that delete, disconnect, or write public review replies refuse to run without `--confirm`.
- The skill tells agents to confirm before immediate publish, AI credit spend, or irreversible actions.
- Idempotency keys prevent duplicate posts on retries.

Agents draft and schedule; people sign off on anything that goes live.

## Links

- Agent overview: [poster.ly/agents](https://www.poster.ly/agents)
- MCP setup: [poster.ly/mcp](https://www.poster.ly/mcp)
- CLI: [poster.ly/cli](https://www.poster.ly/cli) ([@posterly/cli on npm](https://www.npmjs.com/package/@posterly/cli))
- API reference: [poster.ly/reference](https://www.poster.ly/reference)
- Docs: [poster.ly/docs](https://www.poster.ly/docs)
- Full tool map: [SKILL.md](SKILL.md)
- Directory submission checklist: [SUBMISSION.md](SUBMISSION.md)

## License

MIT
