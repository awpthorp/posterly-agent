# posterly agent skill

Social media scheduling for AI agents. This skill teaches Claude Code, OpenClaw, Cursor, and any other skill-compatible agent how to schedule and manage posts across **17 platforms** through [posterly](https://www.poster.ly): Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Facebook, Threads, Pinterest, Google Business Profile, Bluesky, Telegram, Discord, Mastodon, Dev.to, Hashnode, WordPress, and Lemmy.

One skill, three interchangeable interfaces, all using the same API key:

| Interface | Best for | Entry point |
| --- | --- | --- |
| MCP | MCP-capable runtimes (Claude Code, Claude Desktop, Cursor) | `POST https://www.poster.ly/api/mcp` or `npx -y posterly-mcp-server@latest` |
| CLI | Terminal-capable agents, scripts, CI | `npx -y @posterly/cli@latest` |
| REST | Everything else | `https://www.poster.ly/api/v1` |

## Install

With the [skills](https://skills.sh) CLI (Claude Code, OpenClaw, and other compatible agents):

```bash
npx skills add awpthorp/posterly-agent
```

As a Claude Code plugin:

```
/plugin marketplace add awpthorp/posterly-agent
/plugin install posterly@posterly-agent
```

Or copy [SKILL.md](SKILL.md) into your agent's skills directory manually.

## Setup

1. Create a posterly account at [poster.ly](https://www.poster.ly) and connect your social accounts.
2. Enable API access (Dashboard -> Settings -> API Keys). Requires the $3/month API add-on on any plan.
3. Give the key to your agent:

```bash
export POSTERLY_API_KEY=pst_live_...
```

4. Smoke test:

```bash
npx -y @posterly/cli@latest doctor --pretty
```

## What agents can do with it

- Discover connected accounts, brands, brand voice profiles, and per-platform posting rules
- Upload media and create, schedule, update, pause, and repair posts (single or 25-post batches)
- Find optimal open posting slots and avoid schedule collisions
- Pull account and per-post analytics
- Manage Google Business Profile reviews, review replies, audits, and gallery media
- Generate AI captions, images, and video through posterly's AI endpoints
- Monitor publish outcomes via activity feeds and webhooks

The full tool list (60 MCP tools), CLI command map, and REST reference live in [SKILL.md](SKILL.md).

## Human in the loop

The skill and tooling are built so agents stay safe by default:

- CLI commands that touch anything public or irreversible (deleting posts, disconnecting accounts, posting review replies) refuse to run without an explicit `--confirm` flag.
- The SKILL.md instructs agents to confirm with the user before publishing immediately, spending AI credits, or writing to public listings.
- Idempotency keys prevent duplicate posts on retries.

Keep a human approving anything that goes live. Agents draft and schedule; people sign off.

## Links

- Agent overview: [poster.ly/agents](https://www.poster.ly/agents)
- MCP setup: [poster.ly/mcp](https://www.poster.ly/mcp)
- CLI: [poster.ly/cli](https://www.poster.ly/cli) ([@posterly/cli on npm](https://www.npmjs.com/package/@posterly/cli))
- API reference: [poster.ly/reference](https://www.poster.ly/reference)
- Docs: [poster.ly/docs](https://www.poster.ly/docs)

## License

MIT
