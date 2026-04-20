---
name: posterly-social-manager
version: 1.1.0
title: Social Media Scheduler (via poster.ly)
description: Turn your OpenClaw into an autonomous social media manager using posterly in hybrid mode. Prefer MCP when your OpenClaw runtime supports it, and fall back to the posterly REST API with the same API key when it does not. Covers brands, brand profiles, media upload, post creation, scheduling, analytics, and post management.
license: MIT
author: posterly <alex@poster.ly>
homepage: https://www.poster.ly/openclaw
repository: https://github.com/awpthorp/posterly-agent
keywords: social-media, automation, posterly, instagram, tiktok, youtube, twitter, linkedin, scheduling, mcp
metadata:
  openclaw:
    requires:
      env:
        - POSTERLY_API_KEY
    primaryEnv: POSTERLY_API_KEY
---

# Social Media Scheduler (via poster.ly)

Autonomously manage social media posting via [posterly](https://www.poster.ly).

This skill is designed for hybrid use:

- Prefer the posterly MCP server when your OpenClaw runtime can access MCP tools.
- Fall back to direct posterly REST API calls when MCP is unavailable.
- Use the same `POSTERLY_API_KEY` for both modes.

## Setup

1. Create a posterly account at [poster.ly](https://www.poster.ly)
2. Connect your social accounts (Instagram, TikTok, LinkedIn, YouTube, etc.)
3. Enable API access (Dashboard -> Settings -> API Keys) - requires $3/mo add-on
4. Store your API key in workspace `.env`:
   ```
   POSTERLY_API_KEY=your_api_key
   ```
5. If your OpenClaw runtime supports MCP, configure the posterly MCP server as the preferred transport. If not, use the REST endpoints below with the same key.

## Auth

All requests use Bearer token:
```
Authorization: Bearer <POSTERLY_API_KEY>
```

Base URL: `https://www.poster.ly`

## Capability Surface (16)

When MCP is available, prefer these tool names directly:

1. `whoami`
2. `list_accounts`
3. `list_brands`
4. `get_brand`
5. `list_brand_accounts`
6. `get_brand_profile`
7. `create_post`
8. `list_posts`
9. `find_available_slot`
10. `upload_media`
11. `generate_image`
12. `get_post`
13. `update_post`
14. `delete_post`
15. `get_account_analytics`
16. `get_post_analytics`

When MCP is not available, use the REST API routes below to access the same posterly capability surface.

## REST Fallback Reference

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

### 2. List Brands
```
GET /api/v1/brands
```

Returns the brands/clients you can access, including `id`, `name`, `workspace_id`, `source`, and `account_count`.

**Query parameters:**
- `workspace_id` - optional workspace filter

Use this when a user says things like "Grassroots", "Posterly", or "our Dubai brand" instead of naming a raw social account handle.

### 3. Get Brand
```
GET /api/v1/brands/<brand_id>
```

Returns one brand/client with its workspace, source (`canonical` or `legacy`), linked legacy brand group ID if present, and how many accounts are assigned to it.

### 4. List Brand Accounts
```
GET /api/v1/brands/<brand_id>/accounts
```

Returns the connected social accounts assigned to a brand/client. Use this to resolve a brand into the actual Instagram, LinkedIn, Google Business Profile, or other accounts you can post to or inspect.

### 5. Get Brand Profile
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

Use this before drafting content if the user is asking for brand-specific copy, tone, positioning, or visual direction.

### 6. Upload Media
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
  "file_data": "base64-encoded-data",
  "file_name": "photo.jpg",
  "content_type": "image/jpeg"
}
```

**Supported formats:** JPEG, PNG, GIF, WebP, MP4, MOV, WebM
**Size limits:** Images up to 10MB, videos up to 50MB

**Response:**
```json
{
  "url": "https://...",
  "path": "media/user-id/filename.jpg"
}
```

For large files (>3MB), use the signed upload endpoint:
```
POST /api/v1/media/signed-upload
Body: { "filename": "video.mp4", "content_type": "video/mp4", "size": 15000000 }
```
Returns `upload_url` for direct PUT upload plus `public_url` for use in posts.

### 7. Create Post
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

### 8. List Posts
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

### 9. Get Post Details
```
GET /api/v1/posts/<post_id>
```
Returns full post details including status, caption, media, schedule time, and platform.

### 10. Update Post
```
PATCH /api/v1/posts/<post_id>
```
Update caption, scheduled_at, media_url, media_urls, post_type, or metadata. Only works on `draft` or `scheduled` posts.

### 11. Delete Post
```
DELETE /api/v1/posts/<post_id>
```
Delete a draft or scheduled post. Cannot delete published posts.

### 12. Find Available Slots
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

### 13. Generate Image
```
POST /api/v1/ai/generate-image
```

Generate an AI image that can be used in a post. Confirm prompt, style, aspect ratio, and whether the user is happy to spend credits before calling it.

### 14. Get Account Analytics
```
GET /api/v1/analytics/accounts
```

**Query parameters:**
- `account_id` - required social account ID
- `from` - optional ISO date
- `to` - optional ISO date

Returns daily snapshots plus a summary across the requested date range for supported platforms.

### 15. Get Post Analytics
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

### 16. Who Am I
```
GET /api/v1/whoami
```

Use this first if you need to confirm which workspaces and scopes the current API key can access.

## Supported Platforms (11)

- Instagram (feed, reels, stories, carousels)
- TikTok (video posts)
- LinkedIn (text, image, video)
- YouTube (Shorts, videos)
- X / Twitter (tweets, threads)
- Facebook (posts, reels, stories)
- Threads (text, image, video)
- Pinterest (pins)
- Google Business Profile (posts, events, offers)
- Bluesky (text, image)
- Telegram (channel posts)

## Rate Limits

- 100 requests per hour per API key
- Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 response includes `retry_after` header

## Recommended Workflow

1. Prefer MCP tools when they are available in the runtime.
2. If MCP is unavailable, call the REST fallback routes documented here with the same `POSTERLY_API_KEY`.
3. Call `GET /api/v1/brands` if the user is talking about a client/brand rather than a raw account handle.
4. Call `GET /api/v1/brands/<brand_id>/accounts` to resolve the brand into actual social accounts.
5. Call `GET /api/v1/brands/<brand_id>/profile` when tone, positioning, or brand guidance matters.
6. List accounts to discover connected platforms and IDs.
7. Find available slots to pick optimal posting times.
8. Upload media if needed (images/videos).
9. Create post with caption, media, and schedule time.
10. Use account or post analytics when the user asks how a brand or account is performing.
11. Check post status to confirm scheduling/publishing.
12. Use list posts with `status=failed` to catch and retry failures.

## Tips

- Treat MCP as the preferred interface and REST as the fallback interface.
- Post to multiple platforms by creating separate posts for each account
- Resolve brands first when the user speaks in client names instead of platform handles
- Use `find_available_slot` to avoid scheduling conflicts
- Stagger posts throughout the day for better reach
- Use `Idempotency-Key` header when automating to prevent duplicates
- Monitor `status=failed` posts and retry with corrected content
- Keep captions platform-appropriate (Twitter has character limits, LinkedIn prefers professional tone)
