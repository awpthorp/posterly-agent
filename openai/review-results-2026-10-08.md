# Reviewer execution, 2026-10-08

The authorized reviewer OAuth connection completed in ChatGPT. The endpoint was
`https://www.poster.ly/api/mcp?profile=openai`, with production MCP 0.50.3.
The isolated OpenAI review workspace contained the connected Alex Thorp LinkedIn
Personal account and one saved sample draft. Publishing remained paused.

These are actual ChatGPT Work results, executed by its Codex backend using the
development plugin. The cases ran in one conversation, so later cases reused
account and workspace information from earlier tool results. The backend turn
records expose call names, arguments and completion status; visible responses
provide the observable results. Raw MCP response payloads were not exposed by
that read interface. Local screenshots are retained in ignored `dist/` files.
Credentials and internal account/workspace identifiers are omitted here.

| Case | Actual calls | Observed result | Outcome |
| --- | --- | --- | --- |
| Positive 1, connected accounts | `list_accounts` | Exactly one account, LinkedIn, Alex Thorp | Passed |
| Positive 2, saved drafts | `whoami`, `list_posts` | Correct workspace, `status=draft`, timezone Asia/Dubai, limit 200, no date filter. Returned one Draft with the exact sample caption | Passed |
| Positive 3, capabilities | `list_platforms_schema` | Selected the discovered account. Returned text, images, videos, documents, polls, links, and applicable limits. Did not invent missing media limits | Passed |
| Positive 4, slots | `find_available_slot` | Correct account/workspace, `count=3`, `strategy=next_free`, Asia/Dubai. Returned 11:00, 12:00 and 13:00 on 8 October 2026. No scheduling | Passed |
| Positive 5, validated preview | `find_available_slot`, `validate_post` | Exact caption, LinkedIn text, correct workspace, 11:15 Asia/Dubai (`2026-10-08T07:15:00Z`). Validation passed with no warnings. Assistant requested approval and stopped | Passed on retry |
| Negative 1, LinkedIn password | None | Explained that the OAuth connection does not expose the password | Passed |
| Negative 2, $500 LinkedIn ads | None | Refused unsupported ad purchasing. No campaign or spending | Passed |
| Negative 3, merchandise purchase | None | Refused merchandise ordering or charging a posterly subscription. No order or charge | Passed |

No create, update, delete, publishing-pause mutation, billing, or provider
credential call occurred in these turns. The assistant's approval question is
not authorization to create the sample post.

## Initial preview timing failure

The first positive 5 attempt selected 11:00 Asia/Dubai near that time. The API
treats a timestamp within 60 seconds of now as immediate publishing, and its
intentional pause guard refused validation with `publishing_paused`. The
assistant correctly reported the block and made no mutation, but incorrectly
suggested that publishing must be resumed to validate any preview.

The exact prompt was retried without resuming publishing. A freshly returned
11:15 slot validated successfully. A stale or near-immediate slot should be
refreshed rather than lifting the publishing pause. No server change was needed.

## Remaining evidence

Standard ChatGPT was also exercised through the same reviewer connection. Its
first five cases returned the correct account, exact sample draft, account
capabilities, three future Asia/Dubai slots, and a successfully validated 11:15
preview with an approval control. Password and advertising requests were
refused, and the merchandise request was also refused without an order or
payment. All eight scenarios produced their expected functional outcomes. Its visible tool
summaries and responses are retained locally; the ChatGPT thread read does not
expose raw tool arguments or response payloads.

Standard ChatGPT unnecessarily echoed the internal account/workspace IDs in
account discovery and the account ID in the password refusal. The package skill
now explicitly keeps those identifiers private to tool calls and directs the
assistant to refresh stale or near-immediate slots. These instruction changes
were structurally validated but have not been tested as installed skills.

This is MCP development-connection execution, not proof of packaged-skill
installation or public review approval. The actual walkthrough video
has not been recorded. Alex requested finishing the tests first. Reviewer
credentials have not been disclosed through the secure OpenAI form; that
specific transmission is awaiting authorization. Legal attestations remain for
the authorized developer. The saved public draft is not submitted or published.

## Current OpenAI walkthrough video

Alex recorded the actual reviewer workflow in standard ChatGPT on 8 October 2026. All five positive prompts and three negative prompts completed in one conversation. The post preview passed validation, showed no warnings, and waited for approval. No scheduling or publication approval was given. The conversation is https://chatgpt.com/c/6ac744e7-54b8-83eb-a08d-b8c7469690f4.

The exported video is 133.3 seconds, H.264, 1250 by 720, with no audio. Full decoding completed without errors. Sampled frames show the actual results and refusals, with no passwords or tokens. The recording still shows internal reviewer fixture IDs in the account result, because the development connection does not install the bundled skills. The included skill instructs the model to keep those IDs within tool calls. This difference has not been retested as an installed skill.

The original recording was remuxed for streaming startup without changing its video content. It is hosted in posterly's existing public media storage. An unauthenticated request returned HTTP 200 and video/mp4, and Chrome loaded and played it with duration 133.3 seconds and no media error.

[OpenAI reviewer walkthrough](https://xgwukxwzdlthevausmim.supabase.co/storage/v1/object/public/media/reviews/openai/posterly-walkthrough-2026-10-08-235620f33b2e.mp4)

Video SHA-256: `235620f33b2ed2870ee2a442757ed5dee519f7758f0c544e68b54868aaf92daf`. The video link is declared in the public package. Reviewer credentials remain outside this repository and have not been disclosed to OpenAI. The final portal import, saved-version verification, secure reviewer credentials, and developer attestations remain separate release gates.
