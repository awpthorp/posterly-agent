# Install posterly MCP in Cline

Use the published npm package; this public repository contains integration configuration and skills, not the server implementation. Node.js 18 or later and npm are required.

Ask the user to create a posterly API key at https://www.poster.ly/dashboard/api if they do not already have one. API access needs a paid plan with API access. Starter + API is available from $10/month; confirm current pricing at https://www.poster.ly/agents/signup. Do not collect payment details or passwords.

Merge this entry into Cline's MCP server settings without replacing other servers:

```json
{
  "mcpServers": {
    "posterly": {
      "command": "npx",
      "args": ["-y", "posterly-mcp-server@0.50.4"],
      "env": {"POSTERLY_API_KEY": "<user-provided posterly API key>"},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Enter credentials only in the client's private configuration, never in a repository or response. Leave auto-approval empty. Restart the MCP connection, call `whoami`, and list connected accounts. If authentication fails, use https://www.poster.ly/mcp for setup help. Do not publish a post to test installation.

Use `skills/posterly/SKILL.md` for the normal publishing workflow. Validate drafts and obtain approval of the exact account, caption, media, and schedule before writing. The server sends authorized API calls to https://www.poster.ly and can access connected accounts, posts, media, and analytics within the key's scopes.
