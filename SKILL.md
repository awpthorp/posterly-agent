---
name: posterly-social-manager
version: 1.0.0
title: Social Media Scheduler (via poster.ly)
description: Turn your OpenClaw into an autonomous social media manager using the posterly API. Use when scheduling, posting, or managing content across Instagram, TikTok, LinkedIn, YouTube, X (Twitter), Facebook, Threads, Pinterest, Google Business Profile, Bluesky, or Telegram. Covers media upload, post creation, scheduling, slot finding, and post management.
license: MIT
author: posterly <alex@poster.ly>
homepage: https://www.poster.ly/openclaw
repository: https://github.com/posterly/posterly-agent
keywords: social-media, automation, posterly, instagram, tiktok, youtube, twitter, linkedin, scheduling, mcp
metadata:
  openclaw:
    requires:
      env:
        - POSTERLY_API_KEY
    primaryEnv: POSTERLY_API_KEY
---

# Social Media Scheduler (via poster.ly)

Autonomously manage social media posting via [posterly](https://www.poster.ly) API.

## Setup

1. Create a posterly account at [poster.ly](https://www.poster.ly)
2. Connect your social accounts (Instagram, TikTok, LinkedIn, YouTube, etc.)
3. Enable API access (Dashboard → Settings → API Keys) — requires $3/mo add-on
4. Store your API key in workspace `.env`:
   ```
   POSTERLY_API_KEY=your_api_key
   ```

## Auth

All requests use Bearer token:
```
Authorization: Bearer <POSTERLY_API_KEY>
```

Base URL: `https://www.poster.ly`

## Core Workflow

### 1. List Connected Accounts
```
GET /api/v1/accounts
```
Returns array of connected accounts with `id`, `platform`, `username`, `account_type`, and `profile_picture_url`. Store these IDs — you need them for every post.

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

### 2. Upload Media
```
POST /api/v1/media/upload
Content-Type: multipart/form-data OR application/json
```

**Option A — FormData (for files):**
```
Body: FormData with "file" field
```

**Option B — JSON (for base64):**
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

### 3. Create Post
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
- `account_id` (string, optional) — target account UUID. Alternative: use `username` + `platform`
- `username` (string, optional) — account username (requires `platform`)
- `platform` (string, optional) — platform name (requires `username`)
- `caption` (string, required) — post text content
- `scheduled_at` (ISO 8601, optional) — omit for immediate publish
- `post_type` (string, optional) — `text`, `image`, `video`, `carousel`, `reel`, `story`. Auto-detected from media if omitted
- `media_url` (string, optional) — single media URL
- `media_urls` (array, optional) — multiple media URLs for carousels
- `metadata` (object, optional) — platform-specific settings

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

### 4. List Posts
```
GET /api/v1/posts
```

**Query parameters:**
- `status` — `scheduled`, `published`, `draft`, `failed`
- `platform` — filter by platform name
- `limit` — 1-100 (default 20)
- `offset` — pagination offset
- `sort_by` — `scheduled_at`, `updated_at`, `created_at`
- `updated_since` — ISO date for incremental sync
- `created_since` — ISO date filter

**Response:**
```json
{
  "posts": [...],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### 5. Get Post Details
```
GET /api/v1/posts/<post_id>
```
Returns full post details including status, caption, media, schedule time, and platform.

### 6. Update Post
```
PATCH /api/v1/posts/<post_id>
```
Update caption, scheduled_at, media_url, media_urls, post_type, or metadata. Only works on `draft` or `scheduled` posts.

### 7. Delete Post
```
DELETE /api/v1/posts/<post_id>
```
Delete a draft or scheduled post. Cannot delete published posts.

### 8. Find Available Slots
```
GET /api/v1/slots/next
```

**Query parameters:**
- `account_ids` — comma-separated account UUIDs (optional)
- `timezone` — IANA timezone, e.g. `America/New_York` (default)
- `count` — number of slots, 1-10 (default 5)

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

1. List accounts to discover connected platforms and IDs
2. Find available slots to pick optimal posting times
3. Upload media if needed (images/videos)
4. Create post with caption, media, and schedule time
5. Check post status to confirm scheduling/publishing
6. Use list posts with `status=failed` to catch and retry failures

## Tips

- Post to multiple platforms by creating separate posts for each account
- Use `find_available_slot` to avoid scheduling conflicts
- Stagger posts throughout the day for better reach
- Use `Idempotency-Key` header when automating to prevent duplicates
- Monitor `status=failed` posts and retry with corrected content
- Keep captions platform-appropriate (Twitter has character limits, LinkedIn prefers professional tone)
