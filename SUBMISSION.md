# posterly distribution releases

## Current package

The Claude, Cursor, and Gemini CLI packages use version 1.3.3 and pin `posterly-mcp-server@0.50.3`. CLI fallbacks pin `@posterly/cli@0.1.5`. The OpenAI package has its own version and release process under `openai/`.

Run from this repository root before every release:

```bash
node scripts/validate-template.mjs
node scripts/validate-distribution.mjs
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Keep the three posterly skill copies identical and the two setup skill copies identical. Raise plugin versions together when changing these shared packages. Update the package pins and `registry/server.json` only after the corresponding MCP version is published on npm and deployed. Do not add broad shell pre-approvals to a skill.

## Claude

Use the existing records at https://claude.ai/directory/manage. The plugin records previously needed changes because package launchers were unpinned. The hosted MCP connector was in review as of 2026-10-08. Local stdio runs in Claude Code and Cowork; web chat uses the separately submitted hosted connector at https://www.poster.ly/api/mcp.

Merge fixes, then use **Check for new commits** on a non-rejected record. A rejected record needs **Resubmit for review** on its Review tab. Verify the scanner is reading the new commit before claiming any finding has cleared. Do not create a duplicate submission or withdraw a record just to refresh it.

Verification has no separate application: Anthropic decides whether to escalate a connector to deeper testing. A pending review is not approval or verification. Follow https://claude.com/docs/plugins/submit and https://claude.com/docs/connectors/verification.

## Cursor

Submitted 2026-08-12. Receipt: "We've received your submission. We'll follow up at marketplace-publishing@cursor.com once we review your plugin." The logged-in publisher portal showed a new application form, without the older receipt's status, on 2026-10-08. Do not duplicate the application until the publisher identity or original submission has been resolved.

The submitted organization and handle were `posterly`; website https://www.poster.ly; repository https://github.com/awpthorp/posterly-agent. The prepared plugin remains in `plugins/posterly/`.

## Gemini CLI

The root `gemini-extension.json` exposes the pinned MCP server and requests an API key as a sensitive setting. Install using:

```bash
gemini extensions install https://github.com/awpthorp/posterly-agent
```

Add the `gemini-cli-extension` GitHub topic after merging. Google's gallery crawls public tagged repositories daily and lists packages that pass its validation. Tagging does not prove listing. See https://geminicli.com/docs/extensions/releasing/.

## Official MCP Registry

`registry/server.json` is the public release metadata copied from the MCP server's canonical metadata in the main app. The **Publish MCP Registry** workflow validates and publishes it using GitHub OIDC. It runs manually, with no long-lived GitHub or registry secret.

After merging a metadata update:

```bash
gh workflow run publish-registry.yml --repo awpthorp/posterly-agent
```

Verify the exact version appears as latest in the public registry API. Keep old release history. Do not npm publish from this wrapper repository.

## Further directories

- Cline requires a real installation test with Cline using only the README or `llms-install.md`, plus a 400 by 400 PNG. Complete that test before attesting it on a submission issue.
- ClawHub requires MIT-0 licensing for published skills. Agree on that license before publishing a copy; the repository currently uses MIT.
- Muse needs business verification and reviewer access. No submission history was visible under the personal login on 2026-10-08. Resolve the original publisher identity before submitting again.
- Glama and Smithery already have public listings; update existing records rather than creating duplicates.

Never commit API keys, reviewer credentials, private logs, or customer data. Reviewer access for one directory does not authorize sharing credentials with another.
