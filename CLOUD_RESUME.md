# Continue M&B Growth Engine from Codex Cloud / phone

## Where the complete current work is saved

Branch: **`codex/growth-engine-883e99b`**. Production baseline on `main`: `883e99b`. First reviewed patch checkpoint: `b3b5d4a`. Continue from the latest commit on the continuation branch, not from the older `main` exports alone. This branch is intentionally not merged or deployed by the continuation task.

The complete non-secret handoff is in GitHub. n8n runs on its hosted server, not on the Mac. No Mac path, browser session, terminal process, private file or credential exported from the Mac is required for Cloud continuation. Cloud already has the existing n8n environment bindings; their availability does not prove that the server accepts them. The last authenticated API list attempt timed out after 20 seconds. Do not create a replacement key because of a timeout.

## Start a later task

1. Select this repository and **the continuation branch** in Codex Cloud. If an existing checkout is used, inspect local changes and the remote branch before switching; never reset or overwrite user work. Existing tasks are isolated; do not create worktrees unless requested.
2. Read `AGENTS.md`, `automation/n8n/STATUS.md`, `automation/n8n/continuation.json`, and `automation/n8n/pending/README.md`.
3. Read `automation/n8n/cloud-readiness.json` for the completed offline assembly result. Retain documented successful tests; rerun only checks directly affected by later changes.
4. Continue local work if n8n times out. Keep production exports and six pending patches separate. Do not replace the original IDs, bindings, webhook routes or deployed workflow versions with redacted files.
5. Commit and push new reviewed work to this branch; update STATUS and evidence. Do not merge into `main`, publish the site, send test customer messages or spend advertising budget.

## Portable tools, from repository root

All handoff/connection tools use Python 3 standard library only. No Jekyll, React, npm install, n8n installation, local Docker daemon or Mac is needed.

**Offline assembly**, when the artifacts have changed or their provenance needs checking:

```sh
python3 automation/n8n/cloud_handoff.py
```

This composes all six reviewed deltas in memory against the twelve original workflow identities, verifies provenance, and reports schedules/table reuse. It neither executes workflow Code nor writes to n8n. It does not repeat the old provider/content/SEO business tests.

**READ-ONLY live check**, when API access is to be retried:

```sh
python3 automation/n8n/live_status.py --timeout 20
```

This uses the existing `N8N_BASE_URL` and `N8N_API_KEY` environment bindings. It sends GET only to the documented inventory endpoint, paginates, and compares ID/name/active state with GitHub. It does not fetch customer rows, execute nodes, trigger webhooks, change settings or deploy. It follows no redirects with the key, preserves proxy/CA verification, retries nothing automatically, and prints no secret or response body. Optional metadata reports must stay under ignored `automation/n8n/private-live/`.

After CONNECTED, use the already supplied read-only `snapshot.py` to fetch current versions. Compare fresh live state before touching a workflow; a differing version requires reviewing/rebasing the minimal delta. Use `stage_patch.py` only for private local preparation. A redacted candidate remains non-deployable even if local checks pass.

## What remains after local completion

- Live inventory/version reconciliation, recent W7/report execution inspection, isolated node/mapping/concurrency validation, applying the six changes to the existing IDs, and read-back of newly published exports require the n8n API/runtime.
- Strict transactional uniqueness/exactly-once SMTP has not been proved; never automatically retry uncertain deliveries.
- Social publishing, CMS and Search Console still require their actual authorized connections; drafts remain drafts. These account integrations are separate from the API timeout.
- Customer test sends, public test posts and paid advertising are prohibited. Paid campaigns or budget changes require explicit approval.

**Mac shutdown:** the saved code, patches and handoff are independent of the Mac. Closing it does not establish current n8n host health or guarantee 24/7 execution; that still requires live verification. Unrelated unsaved Mac work is outside this handoff.
