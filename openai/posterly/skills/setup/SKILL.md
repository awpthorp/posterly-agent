---
name: setup
description: Connect posterly through OAuth, check accessible workspaces and social accounts, and guide the first validated social post.
---

# Set up posterly

1. Probe the existing connection once with `whoami`. If it works, reuse it.
2. If disconnected, use the ChatGPT or Codex plugin connection flow and sign in
   to posterly through OAuth. Passwords and OAuth consent stay in the browser.
   Never ask the user to paste an API key or password into chat.
3. Read the returned workspace permissions and onboarding state. If posterly
   reports missing subscription or API access, explain the returned requirement
   neutrally. Link only to a verified informational entitlement page that does
   not initiate a purchase. Never display subscription offers, initiate new subscriptions
   or upgrades, sell credit packs, or link to checkout, even if requested.
4. Call `list_accounts`. If no account is connected, use `list_platforms` with
   `view: connect_link` or `create_connect_session` for the user's chosen
   platform. Guide the browser handoff. Poll using `list_accounts` with
   `view: connect_session` and the returned session ID when applicable.
5. Resolve one account and the user's timezone. Draft a caption, find a suitable
   slot, and run `validate_post`. Show the exact destination, content, media,
   and scheduled time. Ask for approval before `create_post` with `confirm: true`.
6. Report the saved post ID and actual status. A scheduled post has not yet
   been published.

Use the main posterly skill for subsequent work. Help is available at
https://www.poster.ly/about and https://www.poster.ly/mcp.
