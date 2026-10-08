# posterly

Use the posterly MCP tools for social scheduling and analytics. Read `skills/posterly/SKILL.md` for the publishing workflow and `skills/setup/SKILL.md` when connection setup is needed.

Use live tool schemas as the source of truth. Call `whoami` first, resolve the workspace and connected account, and validate the complete post before asking the user to approve publishing or scheduling. Never send a public post, delete data, disconnect an account, or spend credits without approval of the exact action. Keep keys out of responses and logs.

The MCP server uses the API key entered during extension installation. It sends authorized requests to https://www.poster.ly. Account creation and payment stay in the user's browser.
