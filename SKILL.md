---
name: posterly-social-manager
version: 1.2.0
title: Social Media Scheduler (via poster.ly)
description: Turn your agent (Claude Code, OpenClaw, Cursor, or any MCP- or terminal-capable runtime) into an autonomous social media manager using posterly. Prefer MCP when the runtime supports it, use the posterly CLI when you can run shell commands, and fall back to the posterly REST API with the same API key otherwise. Covers 17 platforms: brands, brand profiles, learned voice, media upload, post creation, scheduling, analytics, Google Business, and post management.
license: MIT
author: posterly <alex@poster.ly>
homepage: https://www.poster.ly/agents
repository: https://github.com/awpthorp/posterly-agent
keywords: social-media, automation, posterly, instagram, tiktok, youtube, twitter, linkedin, scheduling, mcp, cli, ai-agent
metadata:
  openclaw:
    requires:
      env:
        - POSTERLY_API_KEY
    primaryEnv: POSTERLY_API_KEY
---

# Social Media Scheduler (via poster.ly)

Autonomously manage social media posting across 17 platforms via [posterly](https://www.poster.ly).

This skill supports three interchangeable interfaces, all authenticated by the same `POSTERLY_API_KEY`:

1. **MCP** - prefer the posterly MCP server when your runtime can access MCP tools.
2. **CLI** - use `npx -y @posterly/cli@latest` when you can run shell commands (Claude Code, terminal agents, CI).
3. **REST** - call the posterly REST API directly when neither MCP nor a shell is available.

## Setup

1. Create a posterly account at [poster.ly](https://www.poster.ly)
2. Connect your social accounts (Instagram, TikTok, LinkedIn, YouTube, etc.)
3. Enable API access (Dashboard -> Settings -> API Keys) - requires the $3/mo API add-on
4. Store your API key in workspace `.env`:
   ```
   POSTERLY_API_KEY=your_api_key
   ```
5. Pick an interface: configure the posterly MCP server if your runtime supports MCP, use the CLI if you have a shell, or use the REST endpoints below.

## Auth

All requests use Bearer token:
```
Authorization: Bearer <POSTERLY_API_KEY>
```

Base URL: `https://www.poster.ly`

## Interface 1: MCP

- Hosted (streamable HTTP): `POST https://www.poster.ly/api/mcp` with the `Authorization: Bearer` header. `GET /api/mcp` returns server info without auth.
- Local (stdio): `npx -y posterly-mcp-server@latest` with `POSTERLY_API_KEY` in the environment.

Example MCP client config:

```json
{
  "mcpServers": {
    "posterly": {
      "command": "npx",
      "args": ["-y", "posterly-mcp-server@latest"],
      "env": { "POSTERLY_API_KEY": "YOUR_KEY" }
    }
  }
}
```

## Interface 2: CLI

If you can run shell commands, the posterly CLI wraps the same API with no install step:

```bash
npx -y @posterly/cli@latest doctor --pretty   # validate Node, API origin, key, and live /whoami access
npx -y @posterly/cli@latest whoami
npx -y @posterly/cli@latest accounts:list
npx -y @posterly/cli@latest posts:create --account-id <id> --caption "Launching soon" --scheduled-at 2026-07-10T09:00:00Z
```

- Reads `POSTERLY_API_KEY` from the environment; humans can also run `auth:login` (browser OAuth) or `auth:key`.
- Every command prints JSON to stdout, so output is directly parseable. Add `--pretty` for humans.
- Destructive commands (`posts:delete`, `posts:delete-group`, `accounts:disconnect`, `gbp:reply`, `webhooks:delete`, ...) refuse to run without `--confirm`. Keep that guard: confirm with the user before adding `--confirm`.
- Run `npx -y @posterly/cli@latest help` for the full command list.

Command map:

```
auth:login | auth:key | auth:status | auth:logout | doctor | whoami
accounts:list | accounts:disconnect | connect:link
oauth:clients | oauth:create-client | oauth:update-client | oauth:delete-client
brands:list | brands:get | brands:accounts | brands:profile
platforms:list | platforms:schema | platforms:trigger
posts:list | posts:get | posts:create | posts:update | posts:status | posts:missing | posts:release-id | posts:delete | posts:delete-group | posts:batch
slots:next
media:upload | media:signed-upload | media:upload-from-url
analytics:account | analytics:posts
gbp:reviews | gbp:review-link | gbp:audit | gbp:media | gbp:add-media | gbp:delete-media | gbp:suggest-reply | gbp:reply | gbp:delete-reply
ai:video-options | ai:video-function | ai:generate-video | ai:video-jobs | ai:video-job
activity:list | notifications:list | x:quota
webhooks:list | webhooks:create | webhooks:update | webhooks:delete | webhooks:test
```

## Capability Surface (60)

When MCP is available, prefer these tool names directly:

1. `whoami`
2. `get_mcp_status`
3. `create_api_key`
4. `delete_api_key`
5. `list_accounts`
6. `disconnect_account`
7. `get_connect_link`
8. `create_connect_session`
9. `get_connect_session`
10. `list_oauth_clients`
11. `create_oauth_client`
12. `update_oauth_client`
13. `delete_oauth_client`
14. `list_platforms`
15. `get_platform_schema`
16. `trigger_platform_helper`
17. `list_brands`
18. `get_brand`
19. `list_brand_accounts`
20. `get_brand_profile`
21. `get_learned_voice`
22. `create_post`
23. `create_posts_batch`
24. `list_posts`
25. `find_available_slot`
26. `upload_media`
27. `upload_media_from_url`
28. `create_signed_upload`
29. `generate_captions`
30. `generate_image`
31. `get_video_options`
32. `run_video_function`
33. `generate_video`
34. `get_video_job`
35. `get_post`
36. `get_post_missing`
37. `ask_support`
38. `update_post`
39. `update_post_status`
40. `update_post_release_id`
41. `delete_post`
42. `delete_post_group`
43. `get_account_analytics`
44. `get_post_analytics`
45. `list_google_business_reviews`
46. `get_google_business_review_link`
47. `audit_google_business_profile`
48. `suggest_google_business_review_reply`
49. `reply_google_business_review`
50. `delete_google_business_review_reply`
51. `list_google_business_media`
52. `add_google_business_media`
53. `delete_google_business_media`
54. `list_activity`
55. `list_webhooks`
56. `create_webhook`
57. `update_webhook`
58. `delete_webhook`
59. `test_webhook`
60. `get_x_posting_quota`

When MCP is not available, use the CLI command map above or the REST API routes below to access the same posterly capability surface.

## Interface 3: REST Fallback Reference

### 1. List Connected Accounts
```
GET /api/v1/accounts
```
Returns array of connected accounts with `id`, `platform`, `username`, `account_type`, and `profile_picture_url`. Store these IDs - you need them for every post.

**Response:**
```json
{
  "accounts": [
    {
      "id": "uuid-string",
      "platform": "instagram",
      "username": "myaccount",
      "account_type": "personal",
      "profile_picture_url": "https://..."
    }
  ]
}
```

### 2. Disconnect Account
```
DELETE /api/v1/accounts/<account_id>
```

Requires `accounts:write`. Only call after the user explicitly confirms the exact account ID, platform, username, and workspace. The API removes the account connection, preserves reconnect metadata for posts, archives Instagram analytics where available, and emits `account.disconnected` webhooks.

### 3. List Brands
```
GET /api/v1/brands
```

Returns the brands/clients you can access, including `id`, `name`, `workspace_id`, `source`, and `account_count`.

**Query parameters:**
- `workspace_id` - optional workspace filter

Use this when a user says things like "Grassroots", "Posterly", or "our Dubai brand" instead of naming a raw social account handle.

### 4. Get Brand
```
GET /api/v1/brands/<brand_id>
```

Returns one brand/client with its workspace, source (`canonical` or `legacy`), linked legacy brand group ID if present, and how many accounts are assigned to it.

### 5. List Brand Accounts
```
GET /api/v1/brands/<brand_id>/accounts
```

Returns the connected social accounts assigned to a brand/client. Use this to resolve a brand into the actual Instagram, LinkedIn, Google Business Profile, or other accounts you can post to or inspect.

### 6. Get Brand Profile
```
GET /api/v1/brands/<brand_id>/profile
```

Returns the saved brand profile for that brand/client, including things like:
- `brand_name`
- `tone_of_voice`
- `audience`
- `brand_values`
- `keywords`
- `competitors`
- `do_donts`
- `visual_guidelines`
- `custom_instructions`
- `topics_to_cover`
- `topics_to_avoid`
- `voice_examples`

Use this before drafting content if the user is asking for brand-specific copy, tone, positioning, or visual direction. The MCP tool `get_learned_voice` additionally exposes the voice posterly has learned from an account's real published captions.

### 7. Upload Media
```
POST /api/v1/media/upload
Content-Type: multipart/form-data OR application/json
```

**Option A - FormData (for files):**
```
Body: FormData with "file" field
```

**Option B - JSON (for base64):**
```json
{
  "data": "base64-encoded-data",
  "filename": "photo.jpg",
  "content_type": "image/jpeg"
}
```

**Supported formats:** JPEG, PNG, GIF, WebP, MP4, MOV, WebM
**Relay size limit:** decoded file up to 5MB. For larger images/videos, use signed upload.

**Response:**
```json
{
  "url": "https://...",
  "path": "media/user-id/filename.jpg"
}
```

For larger files, use the signed upload endpoint:
```
POST /api/v1/media/signed-upload
Body: { "filename": "video.mp4", "content_type": "video/mp4", "size": 15000000 }
```
Returns `upload_url` for direct PUT upload plus `public_url` for use in posts.
Signed upload supports the plan media limits, including images up to 10MB and videos up to 50MB on standard API plans.

To fetch a public remote asset into posterly storage:
```
POST /api/v1/media/upload-from-url
Body: { "url": "https://example.com/photo.jpg", "filename": "photo.jpg" }
```
Localhost/private IP targets and unsafe redirects are blocked.

### 8. Create Post
```
POST /api/v1/posts
```
```json
{
  "account_id": "uuid-string",
  "caption": "Your caption here #hashtags",
  "scheduled_at": "2026-01-15T09:00:00Z",
  "post_type": "image",
  "media_url": "https://uploaded-media-url",
  "media_urls": ["url1", "url2"],
  "metadata": {}
}
```

**Fields:**
- `account_id` (string, optional) - target account UUID. Alternative: use `username` + `platform`
- `username` (string, optional) - account username (requires `platform`)
- `platform` (string, optional) - platform name (requires `username`)
- `caption` (string, required) - post text content
- `scheduled_at` (ISO 8601, optional) - omit for immediate publish
- `post_type` (string, optional) - `text`, `image`, `video`, `carousel`, `reel`, `story`. Auto-detected from media if omitted
- `media_url` (string, optional) - single media URL
- `media_urls` (array, optional) - multiple media URLs for carousels
- `metadata` (object, optional) - platform-specific settings

**Idempotency:** Pass `Idempotency-Key` header to prevent duplicate posts on retry.

**Response:**
```json
{
  "post": {
    "id": 1247,
    "status": "scheduled",
    "scheduled_at": "2026-01-15T09:00:00Z",
    "platform": "instagram",
    "post_type": "image"
  }
}
```

### 9. Create Posts Batch
```
POST /api/v1/posts/batch
```

Create up to 25 posts in one API request:

```json
{
  "posts": [
    { "account_id": "uuid-string", "caption": "First post", "scheduled_at": "2026-01-15T09:00:00Z" },
    { "account_id": "uuid-string", "caption": "Second post", "scheduled_at": "2026-01-16T09:00:00Z" }
  ]
}
```

Each item accepts the same fields as `POST /api/v1/posts`. The response returns successful items in `posts` and failed items in `errors`, both with the original array index.

### 10. List Posts
```
GET /api/v1/posts
```

**Query parameters:**
- `status` - `scheduled`, `published`, `draft`, `failed`
- `platform` - filter by platform name
- `limit` - 1-100 (default 20)
- `offset` - pagination offset
- `sort_by` - `scheduled_at`, `updated_at`, `created_at`
- `updated_since` - ISO date for incremental sync
- `created_since` - ISO date filter

**Response:**
```json
{
  "posts": [...],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### 11. Get Post Details
```
GET /api/v1/posts/<post_id>
```
Returns full post details including status, caption, media, schedule time, and platform.

### 12. Update Post
```
PATCH /api/v1/posts/<post_id>
```
Update caption, scheduled_at, media_url, media_urls, post_type, or metadata. Only works on `draft` or `scheduled` posts.

### 13. Update Post Status
```
PUT /api/v1/posts/<post_id>/status
```
Pause a scheduled post, resume/schedule a paused, draft, or failed post, or move a scheduled/failed/paused post back to draft.

```json
{
  "status": "paused"
}
```

For `status: "scheduled"`, include `scheduled_at` when scheduling a draft or when the original paused time has passed.

### 14. Repair and Group Cleanup
```
GET /api/v1/posts/<post_id>/missing
PUT /api/v1/posts/<post_id>/release-id
DELETE /api/v1/posts/group/<group_id>?confirm=true
```

Use `/missing` to inspect missing content/settings before publish. Use `release-id` to store external release and group metadata. Use group deletion only after explicit confirmation; it only deletes draft, scheduled, failed, or paused posts.

### 15. Delete Post
```
DELETE /api/v1/posts/<post_id>
```
Delete a draft or scheduled post. Cannot delete published posts.

### 16. Find Available Slots
```
GET /api/v1/slots/next
```

**Query parameters:**
- `account_ids` - comma-separated account UUIDs (optional)
- `timezone` - IANA timezone, e.g. `America/New_York` (default)
- `count` - number of slots, 1-10 (default 5)

Respects 1-hour gaps between existing posts. Prefers 8am-10pm posting window.

**Response:**
```json
{
  "slots": [
    { "time": "2026-01-15T15:00:00Z", "local_time": "10:00 AM EST" },
    { "time": "2026-01-15T18:00:00Z", "local_time": "1:00 PM EST" }
  ]
}
```

### 17. Generate Captions
```
POST /api/v1/ai/generate-captions
```

Generate or adapt brand-aware caption suggestions for one or more platforms. Confirm platforms, brief/source caption, tone, and hashtag strategy before calling it. Uses the AI Caption Assist allowance and returns suggestions only; it does not create, draft, schedule, or publish posts.

### 18. Generate Image
```
POST /api/v1/ai/generate-image
```

Generate an AI image that can be used in a post. Confirm prompt, style, aspect ratio, and whether the user is happy to spend credits before calling it.

### 19. Get Video Options
```
GET /api/v1/ai/video-options
```

Read-only Veo video discovery: models, input modes, durations, resolutions, aspect ratios, and credit-cost estimates. This does not generate video or spend credits.

### 20. Run Video Function
```
POST /api/v1/ai/video-function
```

Run read-only Veo helpers such as `estimate_cost` and `validate_request` before generating. This does not generate video or spend credits.

### 21. Generate Video and Poll Jobs
```
POST /api/v1/ai/generate-video
GET /api/v1/ai/video-jobs
GET /api/v1/ai/video-jobs/<job_id>
```

Queue a cost-guarded Veo job and poll until `video_url` is available. Confirm prompt, model, duration, resolution, aspect ratio, audio setting, and credit cost before calling `generate_video`.

### 22. Get Account Analytics
```
GET /api/v1/analytics/accounts
```

**Query parameters:**
- `account_id` - required social account ID
- `from` - optional ISO date
- `to` - optional ISO date

Returns daily snapshots plus a summary across the requested date range for supported platforms.

### 23. Get Post Analytics
```
GET /api/v1/analytics/posts
```

**Query parameters:**
- `account_id` - required social account ID
- `from` - optional ISO date
- `to` - optional ISO date
- `limit` - optional, default 50
- `offset` - optional pagination offset

Returns per-post engagement and reach metrics for supported platforms.

### 24. Who Am I
```
GET /api/v1/whoami
```

Use this first if you need to confirm which workspaces and scopes the current API key can access.

### 25. Platform Discovery
```
GET /api/v1/platforms
GET /api/v1/accounts/<account_id>/schema
POST /api/v1/platforms/trigger
```

Use these before platform-specific posting. They expose supported post types, content limits, media rules, `settings` fields, analytics support, planned provider possibilities, and helper tools such as `pinterest.boards`, `youtube.playlists`, `tiktok.creator_info`, `linkedin.recent_mentions`, and `x.quota`.

### 26. Account Connection Handoff
```
GET /api/v1/connect
GET /api/v1/connect/<platform>
```

Use these when the user needs to connect another channel. They return the dashboard `connection_url`, connection method, provider scopes, readiness, and connected account counts. Open `connection_url` in a logged-in browser; direct OAuth URLs are not exposed because provider callbacks rely on browser state and PKCE cookies.

### 27. Google Business Profile Operations
```
GET /api/v1/google-business/reviews
GET /api/v1/google-business/review-link
GET /api/v1/google-business/audit
POST /api/v1/google-business/reviews/suggest-reply
POST /api/v1/google-business/reviews/reply
DELETE /api/v1/google-business/reviews/reply
GET /api/v1/google-business/media
POST /api/v1/google-business/media
DELETE /api/v1/google-business/media
```

Review management, profile audits, and standing profile gallery media for connected Google Business Profile accounts. Review replies and media changes affect the public listing: always confirm with the user before writing, and never post a reply the user has not approved verbatim.

### 28. Activity and Webhooks
```
GET /api/v1/activity
GET /api/v1/notifications
GET /api/v1/webhooks
POST /api/v1/webhooks
PATCH /api/v1/webhooks/<webhook_id>
DELETE /api/v1/webhooks/<webhook_id>
POST /api/v1/webhooks/<webhook_id>/test
```

Use `/activity` for operational history. Use webhooks for unattended workflows that need `post.created`, `post.updated`, `post.publishing`, `post.published`, or `post.failed` events.

## Supported Platforms (17)

- Instagram (feed, reels, stories, carousels)
- Facebook (posts, reels, stories)
- TikTok (video posts)
- X / Twitter (tweets, threads)
- LinkedIn (text, image, video)
- YouTube (Shorts, videos)
- Pinterest (pins)
- Threads (text, image, video)
- Google Business Profile (posts, events, offers, reviews, media)
- Telegram (channel posts)
- Bluesky (text, image)
- Discord (channel posts)
- Mastodon (statuses)
- Dev.to (articles)
- Hashnode (articles)
- WordPress (blog posts)
- Lemmy (community posts)

Use `GET /api/v1/platforms` (or `list_platforms` / `platforms:list`) for the live list, per-platform post types, and content limits.

## Rate Limits

- 100 create-post requests per hour per API key; media writes and reads use separate higher limits
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 response includes `retry_after` header

## Recommended Workflow

1. Pick an interface: MCP tools when available, the CLI when you have a shell, REST otherwise. All three hit the same `/api/v1` surface with the same key.
2. Call `whoami` (or `GET /api/v1/whoami`) to confirm workspaces and scopes.
3. Call `GET /api/v1/brands` if the user is talking about a client/brand rather than a raw account handle.
4. Call `GET /api/v1/brands/<brand_id>/accounts` to resolve the brand into actual social accounts.
5. Call `GET /api/v1/brands/<brand_id>/profile` when tone, positioning, or brand guidance matters.
6. List accounts to discover connected platforms and IDs.
7. Call `GET /api/v1/accounts/<account_id>/schema` before using platform-specific `settings`.
8. Find available slots to pick optimal posting times.
9. Upload media if needed (images/videos).
10. Create post with caption, media, and schedule time.
11. Use account or post analytics when the user asks how a brand or account is performing.
12. Use `/activity` or webhooks to monitor publish outcomes.
13. Use list posts with `status=failed` to catch and retry failures.

## Tips

- Treat MCP as the preferred interface, the CLI as the shell-friendly equivalent, and REST as the universal fallback.
- Keep a human in the loop for anything public or irreversible: publishing immediately, deleting posts, disconnecting accounts, and replying to reviews.
- Post to multiple platforms by creating separate posts for each account
- Resolve brands first when the user speaks in client names instead of platform handles
- Use `find_available_slot` to avoid scheduling conflicts
- Stagger posts throughout the day for better reach
- Use `Idempotency-Key` header when automating to prevent duplicates
- Monitor `status=failed` posts and retry with corrected content
- Keep captions platform-appropriate (Twitter has character limits, LinkedIn prefers professional tone)
