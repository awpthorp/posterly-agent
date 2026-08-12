# posterly for Cursor

Schedule, publish, and analyze social posts across 18 platforms from Cursor via MCP.

**Platforms:** Instagram, TikTok, LinkedIn, YouTube, X, Facebook, Threads, Pinterest, Google Business Profile, Telegram, Bluesky, Discord, Slack, Mastodon, Dev.to, Hashnode, WordPress, Lemmy.

## Install

Once listed, search **posterly** in Cursor Marketplace / Customize and install it.

Until the listing is live, test locally:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /absolute/path/to/posterly-agent/plugins/posterly ~/.cursor/plugins/local/posterly
```

Then reload Cursor.

## Configure

Open **Plugins -> Configure** and set `POSTERLY_API_KEY`.

Get a key from [Dashboard -> Settings -> API Keys](https://www.poster.ly/dashboard/api). Keys start with `pst_live_`. API access requires the $3/mo API add-on.

## Example prompts

- "List my connected posterly accounts"
- "Schedule a LinkedIn post about our launch for tomorrow at 10am"
- "Upload this image and create an Instagram post for Friday 9am"
- "Which of my recent posts failed, and what is missing?"
- "How did my Instagram account perform over the last 14 days?"

## Human in the loop

Confirm before publish now, delete, disconnect, review replies, or AI credit spend.

## Links

- Site: [poster.ly](https://www.poster.ly)
- Agents: [poster.ly/agents](https://www.poster.ly/agents)
- MCP: [poster.ly/mcp](https://www.poster.ly/mcp)
- CLI: [poster.ly/cli](https://www.poster.ly/cli)
- Docs: [poster.ly/docs](https://www.poster.ly/docs)
