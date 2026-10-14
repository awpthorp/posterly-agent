---
name: posterly
description: >-
  Use posterly MCP to schedule and publish social posts across connected
  platforms (Instagram, TikTok, LinkedIn, YouTube, X, Facebook, Threads,
  Pinterest, Google Business Profile, and others). Use when the user wants
  to list accounts, draft or validate a post, schedule or publish, or
  manage social publishing through hosted MCP rather than a dashboard.
metadata:
  openclaw:
    requires:
      env:
        - POSTERLY_API_KEY
    primaryEnv: POSTERLY_API_KEY
  clawdbot:
    emoji: "📣"
    requires:
      bins: []
      env:
        - POSTERLY_API_KEY
        - POSTERLY_URL
---

# posterly

Agent skill for the posterly hosted MCP. Prefer MCP tools over inventing REST or CLI calls. Live tool schemas are the source of truth.

Use this skill when the user wants to schedule or publish social posts, list connected accounts, or validate a draft before it goes live.

## When to use hosted MCP

Use hosted MCP when the runtime can call MCP tools (Claude Code plugin, Cursor, or any MCP client).

- Docs: https://www.poster.ly/mcp
- Endpoint: `POST https://www.poster.ly/api/mcp?profile=claude`
- `GET https://www.poster.ly/api/mcp` returns server info without auth

Do not invent a second product surface, UI, Autopilot, or a live Claude Connectors listing. If MCP tools are missing, point the user at the MCP docs rather than pasting a long REST map.

Local stdio is optional: `node ${CLAUDE_PLUGIN_ROOT}/node_modules/posterly-mcp-server/dist/index.js` with `POSTERLY_DIRECTORY_PROFILE=claude` and the sensitive plugin API-key setting. Claude Code plugins that ship this package can load MCP from `.mcp.json` using plugin `userConfig.api_key`.

## Auth

API and MCP access need a paid posterly plan with API access. Starter + API is available from $10/month; check current pricing on the signup page.

- Environment: `POSTERLY_API_KEY` (starts with `pst_live_`)
- Claude plugin: `userConfig.api_key`, injected as `POSTERLY_API_KEY`
- Header: `Authorization: Bearer <POSTERLY_API_KEY>`

If the key is missing, send the user to https://www.poster.ly/mcp or https://www.poster.ly/agents/signup. Do not collect card numbers, posterly passwords, or social passwords. Do not invent a signup flow.

Never start signup if `whoami` already works. Never ask the user to paste a key they already have.

## Safe publish loop

Follow this loop for almost every publishing task. Confirm with the human before any write.

1. **whoami**
   Confirm the key, workspace, and scopes. Call this at the start of a session.

2. **List accounts**
   Call `list_accounts`. If the user named a brand or client, resolve it with brand tools first, then use the social account IDs.

3. **Draft and validate**
   Draft caption, media, account, and `scheduled_at`. Call `validate_post` with the complete payload. Fix errors before you ask for a live create.

4. **Schedule or publish with confirmation**
   Show account, platform, caption, schedule (or publish now), media, and workspace. Wait for an explicit yes. Then call `create_post` with the same payload and `confirm: true`.

Omitting `scheduled_at` publishes immediately. Never infer consent from an earlier standing instruction.

## Writes that need a human yes

Confirm the exact target before:

- Immediate publish (no `scheduled_at`)
- `create_post` / `create_posts_batch`
- Delete post, post group, comment, or disconnect
- Review replies, DMs, hide or unhide comments
- API-key changes

Do not pass `confirm: true` until the user has approved that action.

## Useful read tools

Prefer MCP names. Do not dump raw JSON unless the user is debugging.

- `whoami`, `list_accounts`, `list_brands`, `list_platforms`
- `validate_post`, `list_posts`, `get_post`, `list_analytics`
- `find_available_slot`, `list_media`, `list_activity`
- Analytics tools when the user asks how content performed

`get_post` and `list_posts` show when each post was created and who created it (`created_by`: `user_id`, `name`, `source`).

## Media

Chat paperclips do not reach hosted MCP. Use the upload path the runtime can actually run:

- Small files: `upload_media`.
- A laptop file in a client that cannot send bytes (ChatGPT web, Claude.ai, Gemini web): `create_media_drop`, then send the user the drop URL. One link takes up to 20 files (`max_files` is 1 to 20, default 10). Afterwards call `list_media` with the drop session ID to read each `public_url`.
- Larger files, or several files at once, when the runtime can HTTP PUT: `create_signed_upload`. Pass one file (`filename`, `content_type`, `size`) or `files` with up to 20 `{filename, content_type, size}` items in one call. Do not mix the two forms. Each file gets its own slot (`upload_url`, `public_url`, `headers`) or its own error, so check every slot and retry only the files that failed. PUT the raw bytes to `upload_url` with the returned headers. Slots expire after 15 minutes.

Accepted types are an explicit allowlist: JPEG, PNG, GIF, WebP, MP4, MOV, WebM, and PDF (up to 50MB). HEIC is not accepted, so ask the user to export it as JPG or PNG. A PDF is only for LinkedIn document posts: set `post_type` to `document`, `media_url` to the PDF `public_url`, and `settings.document_title` (required).

Fresh uploads are checked when a post is created, updated, or created in a batch. A video that cannot be repaired automatically, such as one with a low frame rate, comes back as a warning rather than a block, so show any `warnings` to the user before they confirm.


## After create

Tell the user the post was created, share any dashboard link the tool returned, and offer the next natural step. Inspect failed posts before retrying. Do not republish reconnect, re-upload, or edit-and-retry failures until the user has done that work.

## Fallback

If MCP is unavailable, explain how to configure the plugin or direct the user to the MCP documentation. Do not use CLI or REST fallbacks to bypass the directory profile.

## Links

- MCP: https://www.poster.ly/mcp
- Hosted MCP: https://www.poster.ly/api/mcp
- Agents signup: https://www.poster.ly/agents/signup

## Claude directory scope

This plugin uses the restricted Claude directory catalog. It supports social publishing, existing-media uploads, text captions, analytics, and social inboxes. AI image, video, and audio generation and billing mutations are unavailable. Never attempt them through a CLI, REST endpoint, or another posterly tool. Account signup and any payments remain human actions in the browser. Legacy tool aliases are unavailable; use the live canonical schemas and their view or action selectors.
