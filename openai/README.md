# posterly for OpenAI

The OpenAI package lives in `openai/posterly-openai/`. It adapts this repository's
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
to reviewers; subscription management tools are excluded from the OpenAI profile.

## Review preparation

Five positive and three negative cases are in `plugin.json`. They cover account
discovery, saved draft retrieval, account-specific platform requirements,
timezone-aware slots, a validated post preview, and three unsupported requests.
All cases remain **Not run** against the reviewer connection as of 2026-10-08.
The draft-retrieval case uses the actual saved fixture. No queued post is required
for these read and validation cases; do not schedule a real public test post.
The standard hosted catalog retains 61 tools. The replacement submission
connection discovered the 92-operation OpenAI profile with the required boolean
annotations. Discovery is not authenticated case execution.

The existing posterly development connection also successfully returned
`whoami`, `list_accounts`, and `list_platforms` on 2026-10-07. Those read-only
checks used the author's existing account, not the isolated reviewer account,
and do not count as saved-version review case results. At Alex's request, further
read-only developer checks used his existing Alex Thorp LinkedIn connection:
three Asia/Dubai slots returned, its scheduled-post filter was empty, and the
sample text post validated successfully for 2026-10-08 at 08:00 Asia/Dubai.
Validation was a dry run; no post was created or published. These checks use
the existing development connector, not an isolated saved-version reviewer run.

A dedicated `openai-review@poster.ly` account and isolated `OpenAI review`
workspace were created on 2026-10-07. Password sign-in and absence of MFA were
verified, including password sign-in through the actual browser dashboard.
The normal browser onboarding was completed with name OpenAI and timezone
Asia/Dubai, skipping social connection and first-post creation for now.
Complimentary Pro and API access run through 2027-01-05. Credentials
are stored outside the repository in a local mode-0600 file, and have not been
shared with OpenAI. On 2026-10-08, Alex completed the normal LinkedIn Personal
connection flow. The reviewer workspace now shows Alex Thorp as active. It is a
real personal destination, so do not publish sample content there. Publishing
was paused only in OpenAI review at 10:29 Asia/Dubai. A sample LinkedIn draft
was saved with caption "OpenAI review sample draft. This content is for
integration testing." No provider tokens were copied and no public post was made.

Complete the reviewer fixture with:

- Active comped subscription and API entitlement for the review period.
- Password sign-in without MFA, mailbox codes, or private network access.
- A connected test LinkedIn account and its normal account permissions.
- The existing sample draft and workspace publishing pause. Leave publishing
  paused throughout the walkthrough and review.

Use only the authorized isolated reviewer workspace. Avoid sharing a real
customer's workspace. Do not resume publishing or create public test content.
Store the password and reviewer instructions only in OpenAI's secure Review
details form. Do not put them in this repository, the ZIP, or public URLs.

## Record the walkthrough

The existing `https://www.poster.ly/videos/mcp-api-demo.mp4` shows an older
Claude workflow. It is reference material, not evidence for this OpenAI version.

Use a development plugin connection to `/api/mcp?profile=openai` in ChatGPT
and the dedicated reviewer account. The original consolidated development
connection is preserved. A matching OpenAI review test connection was created on 2026-10-08 as
`plugin_asdk_app_6ac73a3b5a948191adc4ca85a76d9b29`. Its reviewer OAuth grant
is pending; no case execution is claimed. The recipient and six requested
scopes match the existing ChatGPT connector. Approve only the intended
reviewer connection, not an unrelated account. Start the user's screen recorder with only that
window visible. Demonstrate:

1. OAuth connection and account discovery using positive case 1.
2. Saved draft results using case 2, including the exact sample caption.
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

The first authenticated scan on 2026-10-07 flagged 15 tools. Eleven findings
require callable operations to be exposed separately, two require truthful
openWorldHint annotations (update_post and submit_product_feedback), and three
require further manual review (connect_account, update_post, resume_subscription).
update_post has two findings. The initial summary incorrectly described all
findings as manual review; the complete report was subsequently inspected.

Version 1.1.0 targets `/api/mcp?profile=openai`. Main app PR
https://github.com/awpthorp/posterly/pull/1335 adds this profile: 92 fixed
operations derived from the existing registry, with no generic dispatcher or
legacy alias fallback. The normal hosted 61-tool and stdio 64-tool catalogs
remain consolidated. Direct credential entry, credential administration,
webhooks, and subscription management are excluded from this public profile.
Both annotation corrections apply to the shared catalog. Existing REST access
checks and preview confirmations continue to enforce permissions and approval.

MCP 0.50.0 is deployed in production from merged PR 1335, commit
020f42af7464b15287cd88703f3eeb9a396619e7, Vercel deployment
dpl_6brybX39mbdvRHUs1EysSSusxrvZ. All GitHub checks and approval/security checks
passed. The npm trusted-publishing workflow also published 0.50.0 and the
published-version check passed.

OpenAI rejected changing the existing draft's MCP URL. It also rejected changing
transport headers, and the generic upload automatically reused the existing
package identity. The OpenAI-only package and MCP key are therefore
`posterly-openai`; the customer-facing display name remains `posterly` and the
publisher remains Grassroots Marketing LLC. The existing unpublished 1.0.2 draft
is retained as a backup. A separate public submission is required for this
server profile. The header extension PR 1336 was closed without merging because
it did not address this portal restriction.

A replacement version 1.1.0 was uploaded on 2026-10-07 after the Mac was unlocked.
The saved plugin is `plugin_asdk_app_6ac675cfa8a0819197c6cd0f08b7d264`, draft
`appsub_6ac675cfa8d0819184bd1d644e4b7c15`. Its public developer is Grassroots
Marketing LLC and its package name is `posterly-openai`. The setup dialog
retains the exact URL `https://www.poster.ly/api/mcp?profile=openai`, even though
the summary displays only the URL without query parameters. OAuth authorization
and domain verification passed, MCP configuration is Configured, and discovery
returned all 92 operations. The source identity change was merged in agent
repository PR 5, commit e885d25173b562fb7918db18a07d5d58bdb2550d.

The replacement scan cleared the original dispatcher, annotation, and manual
tool findings. It returned seven new duplicate-name findings for the three post
status variants and four approval variants. OpenAI imports annotation titles as
display names, and these variants shared titles. Main app PR 1337 appends their
fixed status or approval action to the title and adds a unique-title regression
assertion. All checks passed and PR 1337 merged at
90e340946b9d15c0cc9c50027ca77a36543cecdd. MCP 0.50.1 is live on production
deployment dpl_DLJcuRU78umMZFm6QRJAs3SxajVQ and on npm, verified by the published
version check. The complete initial replacement findings are saved locally in
`dist/openai-profile-findings.json`.

The 0.50.1 rescan cleared duplicate names, but returned description findings for
create_connect_session and create_post, plus further manual review for
update_post_status_scheduled. The two descriptions still referenced consolidated
selectors; the profile must use its own separately declared operation names,
including nested schema descriptions. A follow-up fix shipped on 2026-10-08 in main app PR 1338,
https://github.com/awpthorp/posterly/pull/1338, merge commit
6b4f56608a0288983da644f28872499b1a16a2a6. MCP 0.50.2 clarifies the
connection handoff and immediate versus scheduled publication, and updates
description references on copied schemas without mutating the consolidated
definitions. All GitHub checks passed. Production deployment
dpl_E4UbgWBnqwVAGLrc1vHdeDi6Kpo2 was verified READY. The trusted npm workflow
published 0.50.2 and the published-version check passed. The earlier GitHub
write failures recovered; they no longer block release work.

The 0.50.2 scan at 2026-10-08 10:28:26 Asia/Dubai cleared create_connect_session
and create_post findings. Seven fixed status/approval variants now have
description findings: six advertise capabilities beyond their fixed action,
and request_changes has unclear copy. update_post_status_scheduled also
retains its separate further-review finding. Actual dialog messages are saved
locally in `dist/openai-profile-findings-0.50.2.json`, with a screenshot in
`dist/openai-profile-scan-0.50.2.png`. The clipboard copy action returned an old
report, so the current messages were captured from each tool's reviewed dialog.

Main app PR 1339, https://github.com/awpthorp/posterly/pull/1339, provides
operation-specific titles and descriptions, acknowledges external side effects
for status changes, and verifies fixed selector dispatch and rejected overrides.
MCP 0.50.3 passed focused profile tests, TypeScript, build/parity, annotations,
golden contracts, aliases, tool design, and the production build locally.
All GitHub checks passed and PR 1339 merged at
69e6cfc1f338ed38d0b428b7db4ec4f13201b981. Production deployment
dpl_2XegtbKaFQt6rPodbqM3XBUzw7fZ was verified READY, and the hosted MCP
status returned 0.50.3. OpenAI's subsequent scan reports "No issues found in
the latest MCP scan." All tool findings, including the prior scheduling
further-review flag, cleared. Proof is saved locally in
`dist/openai-profile-scan-0.50.3.png`; the findings record is
`dist/openai-profile-findings-0.50.3.json`. The trusted npm workflow 37739196143 published 0.50.3. After registry
processing, the published-version check passed and the latest tag was
verified as 0.50.3. Both hosted and npm releases are complete.

LinkedIn connection, a saved draft, and the workspace publishing pause are
verified. ChatGPT reviewer OAuth approval is pending. The draft source version
1.1.2 updates test fixtures accordingly; it has no demo URL and has not been
uploaded. The portal remains on 1.1.0, unsubmitted and unpublished.

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
