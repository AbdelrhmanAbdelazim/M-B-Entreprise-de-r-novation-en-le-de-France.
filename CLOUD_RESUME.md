# Continue M&B Growth Engine from Codex Cloud / phone

## Where the complete current work is saved

Branch: **`codex/growth-engine-883e99b`**. Production baseline on `main`: `883e99b`. First reviewed patch checkpoint: `b3b5d4a`. Continue from the latest commit on the continuation branch, not from the older `main` exports alone. This branch is intentionally not merged or deployed by the continuation task.

The complete non-secret handoff is in GitHub. n8n runs on its hosted server, not on the Mac. No Mac path, browser session, terminal process, private file or credential exported from the Mac is required for Cloud continuation. Cloud already has the existing n8n environment bindings; their availability does not prove that the server accepts them. The latest authenticated inventory and definition reads succeeded: all twelve expected workflows are Published/Active, and the six saved patches are deployed. See automation/n8n/activation.json for the exact captured versions. No replacement key was created.

## Start a later task

1. Select this repository and **the continuation branch** in Codex Cloud. If an existing checkout is used, inspect local changes and the remote branch before switching; never reset or overwrite user work. Existing tasks are isolated; do not create worktrees unless requested.
2. Read `AGENTS.md`, `automation/n8n/STATUS.md`, `automation/n8n/continuation.json`, and `automation/n8n/pending/README.md`.
3. Read `automation/n8n/cloud-readiness.json` for the completed offline assembly result. Retain documented successful tests; rerun only checks directly affected by later changes.
4. Continue local work if n8n times out. Keep current published exports and the six archived deployed patches separate; do not reapply those patches. Do not replace the original IDs, bindings, webhook routes or deployed workflow versions with redacted files.
5. Commit and push new reviewed work to this branch; update STATUS and evidence. Do not merge into `main`, publish the site, send test customer messages or spend advertising budget.

## Portable tools, from repository root

All handoff/connection tools use Python 3 standard library only. No Jekyll, React, npm install, n8n installation, local Docker daemon or Mac is needed.

**Offline assembly**, when the artifacts have changed or their provenance needs checking:

```sh
python3 automation/n8n/cloud_handoff.py
```

This verifies the twelve current published identities, publication evidence and six deployed deltas without applying them again, and reports schedules/table reuse. It neither executes workflow Code nor writes to n8n. It does not repeat the old provider/content/SEO business tests.

**READ-ONLY live check**, when API access is to be retried:

```sh
python3 automation/n8n/live_status.py --timeout 20
```

This uses the existing `N8N_BASE_URL` and `N8N_API_KEY` environment bindings. It sends GET only to the documented inventory endpoint, paginates, and compares ID/name/active state with GitHub. It does not fetch customer rows, execute nodes, trigger webhooks, change settings or deploy. It follows no redirects with the key, preserves proxy/CA verification, retries nothing automatically, and prints no secret or response body. Optional metadata reports must stay under ignored `automation/n8n/private-live/`.

When a new change requires fresh state, use the already supplied read-only `snapshot.py` to fetch current versions. Compare fresh live state before touching a workflow; a differing version requires reviewing/rebasing the minimal delta. Use `stage_patch.py` only for private local preparation. A redacted candidate remains non-deployable even if local checks pass.

## Published release and remaining operating limits

All twelve expected workflows were independently read back Active/Published after the six saved deltas were published on their existing IDs. Current exports and exact versions are recorded in `automation/n8n/activation.json` and manifest. The API timeout is resolved at that capture. The unrelated thirteenth workflow was not modified.

There is no pending saved patch to activate. Future changes must start from these latest published exports and fresh private live bindings, not the older `883e99b` version or the archived patch preconditions. Original before-release fixtures remain in Git history solely for regression comparison.

- Strict transactional uniqueness/exactly-once SMTP has not been proved; never automatically retry uncertain deliveries.
- Social publishing, CMS and Search Console still require actual authorized connections; drafts remain drafts.
- No real customer test sends, public test posts or ad spending are permitted. Paid campaigns or budget changes require explicit approval.
- Native Data Table operation execution and actual delivery were not manually triggered; release tests used synthetic local fixtures without delivery/model transports.

**Mac shutdown:** yes for this saved project and hosted automation. n8n and the existing Cloud bindings operate independently of the Mac. Publication is verified at the recorded capture; future availability still depends on the hosted server and connected services. Unrelated unsaved Mac work is outside this handoff.
