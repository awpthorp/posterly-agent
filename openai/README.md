# posterly for OpenAI

The OpenAI package lives in `openai/posterly/`. It adapts this repository's
posterly workflows for ChatGPT and Codex with the existing hosted MCP server
and OAuth. Its version is independent of the Claude and Cursor packages.

## Build the ZIP

From the repository root:

```bash
python3 scripts/package-openai.py
```

The script validates the package and inspects the actual ZIP in `dist/`.
Only the five required source files are included. The upload contains no
credentials, private app bindings, local stdio configuration, lifecycle hooks,
or other hosts' manifests.

The listing uses the existing public ChatGPT landing page, the About page's
support contact, Privacy Policy, and Terms of Service. The 512 px transparent
icon is the existing posterly app icon. Grassroots Marketing LLC is the
publisher selected by Alex. Country targeting is all available countries.

The service sells subscriptions and credits independently on its website. OpenAI
currently prohibits digital commerce through plugins. This package permits existing
users to use their included entitlements and prohibits checkout links, new
subscriptions, upgrades, and credit purchases. Informational entitlement links
are allowed. The commerce disclosure remains true to disclose the paid service
and existing subscription management tools to reviewers.

## Review preparation

Five positive and three negative cases are in `plugin.json`. They cover account
discovery, a complete calendar range, account-specific platform requirements,
timezone-aware slots, a validated post preview, and three unsupported requests.
All cases are **Not run** against a dedicated reviewer account as of 2026-10-07.
Public discovery confirms hosted MCP 0.49.2 and 61 tools with the three required
boolean annotations. Public discovery is not authenticated case execution.

The existing posterly development connection also successfully returned
`whoami`, `list_accounts`, and `list_platforms` on 2026-10-07. Those read-only
checks used the author's existing account, not the isolated reviewer account,
and do not count as saved-version review case results. At Alex's request, further
read-only developer checks used his existing Alex Thorp LinkedIn connection:
three Asia/Dubai slots returned, its scheduled-post filter was empty, and the
sample text post validated successfully for 2026-10-08 at 08:00 Asia/Dubai.
Validation was a dry run; no post was created or published. These checks use
the existing development connector, not an isolated saved-version reviewer run.

Prepare a dedicated, isolated reviewer account with:

- Active comped subscription and API entitlement for the review period.
- Password sign-in without MFA, mailbox codes, or private network access.
- A connected test LinkedIn account and its normal account permissions.
- A sample draft and one clearly marked sample scheduled post seven days ahead.

Use a test social destination. Avoid sharing a real customer's workspace.
Store the password and reviewer instructions only in OpenAI's secure Review
details form. Do not put them in this repository, the ZIP, or public URLs.

## Record the walkthrough

The existing `https://www.poster.ly/videos/mcp-api-demo.mp4` shows an older
Claude workflow. It is reference material, not evidence for this OpenAI version.

Use the existing development plugin connection in ChatGPT or Codex and the
dedicated reviewer account. Start the user's screen recorder with only that
window visible. Demonstrate:

1. OAuth connection and account discovery using positive case 1.
2. Calendar results using case 2, including the sample scheduled post.
3. Account capabilities and three returned Asia/Dubai slots using cases 3 and 4.
4. The exact caption and successful validation from case 5. Show the preview and
   that the assistant waits before scheduling.
5. One unsupported request from the negative cases and its explanation.

Rehearse first. Show real returned tool results and enough time to read them.
Stop recording, review playback, and check that no credentials or unrelated
private content appear. Host the actual recording at a reviewer-accessible URL,
verify playback without private sign-in, then set
`extensions.com.openai.review.demo_recording_url` and rebuild:

```bash
python3 scripts/package-openai.py --ready
```

That flag only verifies a demo URL was supplied. It does not certify playback,
reviewer access, successful cases, policy compliance, or approval.

## Console setup

Use the existing Grassroots organization and poster.ly project. The portal
currently labels its business identity `Grassroots`; confirm that verified
identity belongs to Grassroots Marketing LLC and inspect the imported public
developer name. Package author text cannot override a verified identity.

An incomplete 1.0.0 draft was uploaded on 2026-10-07 at Alex's request.
Version 1.0.1 removes subscription wording from the listing and restricts digital
commerce guidance following the portal checks. Version 1.0.2 selects the supported
Business & Operations category for its social marketing workflows. Check the imported listing and skills, then
connect `https://www.poster.ly/api/mcp` with OAuth. No static bearer secret belongs
in `mcp.json`.

The main posterly app already serves `/.well-known/openai-apps-challenge` from
`OPENAI_APPS_CHALLENGE_TOKEN`. The production variable was configured on
2026-10-07 from this draft's portal challenge. Redeploy the current production
revision to apply it. Production redeployment dpl_58g2gRYcvdd1pFJy4jBzyBRggXA8
completed successfully. The public route returned HTTP 200, text/plain, and the
exact challenge body. OpenAI subsequently marked the domain verified. Do not replace a token used
by another plugin at the same URL.

The portal saved version 1.0.2 on 2026-10-07. Subscription wording and category
findings cleared; privacy-policy assessment and missing review materials remain.
Alex approved OAuth access at action time. OpenAI now shows authentication
Authorized, domain verified, and MCP configuration Configured. Discovery
returned all 61 hosted tools, and both bundled skills passed checks.

The first authenticated scan on 2026-10-07 found 15 tools requiring further
OpenAI review: manage_workspace_member, manage_publishing_pause, connect_account,
manage_oauth_client, list_platforms, trigger_platform_helper, submit_product_feedback,
update_post, run_video_function, manage_google_business_review,
manage_google_business_media, manage_conversation, manage_comment, manage_webhook,
and resume_subscription. Their common portal finding is "This tool update needs
further review before it can go live." This is not an approval or a precise
implementation diagnosis.

The scan also found update_post incorrectly declares openWorldHint=false. The
operation can import third-party media and email external reviewers; a shared
annotation correction is ready in
https://github.com/awpthorp/posterly/pull/1335. Hosted and stdio annotation tests,
registry design, version parity, agent-surface checks, and the required
production build passed. It will take effect after merge, deployment, and
the npm release. The current live scan still uses 0.49.2.

The privacy assessment retry returned "We couldn't complete an automated
assessment of your privacy policy. Feel free to submit for additional review."
A current walkthrough, isolated reviewer access, execution of all eight cases,
and developer attestations still remain. No public review submission was made.

After connection, scan tools and resolve findings. Run all eight review cases
against the exact saved version and record evidence here. Enter reviewer access
in the secure form. Submission for review and publication are separate actions.
The authorized developer must complete legal and policy attestations.

Official instructions:
[Packaging](https://developers.openai.com/plugins/build/plugins),
[Submission](https://developers.openai.com/plugins/deploy/submission).
