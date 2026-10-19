# M&B n8n — published production handoff

**LIVE at the latest verified capture.** Read [STATUS.md](STATUS.md), [activation.json](activation.json), [manifest.json](manifest.json) and [data-tables.json](data-tables.json). All twelve expected workflows were read from authenticated hosted n8n after publication and confirmed Active with matching saved/published versions. A thirteenth unrelated workflow is untouched.

The current W0–W10 and My workflow files are sanitized projections of those actual published definitions. Operational credential IDs, Telegram destinations, webhook routes and execution data remain private. They preserve business logic and workflow IDs but are **not directly deployable over production** until fresh private bindings are retained from live n8n. Never import these files as duplicates.

All six reviewed deltas have been deployed. The files under [pending/](pending/README.md) remain unchanged historical patch artifacts; they are not an outstanding deployment queue. `activation.json` records exact before/after versions and patch hashes. Their original strict version guards correctly refuse to overwrite current published versions.

## Phone / Cloud continuation

Select branch `codex/growth-engine-883e99b`, then read [CLOUD_RESUME.md](../../CLOUD_RESUME.md) and repository AGENTS.md. No Mac session, local browser, npm install, Jekyll build or React app is required. The tools use Python 3 standard library.

- `python3 automation/n8n/live_status.py --timeout 20`: GET-only bounded live inventory check and comparison. Uses existing secure Cloud bindings, preserves proxy/CA trust, follows no redirects with the key, and prints no secrets.
- `python3 automation/n8n/snapshot.py --out automation/n8n/private-live`: read-only full export to the ignored directory when a fresh capture is needed.
- `python3 automation/n8n/cloud_handoff.py`: offline provenance/publication check, when artifacts change. It recognizes deployed patches without reapplying them, makes no network request and executes no nodes.
- `stage_patch.py`: local candidate preparation for a reviewed new change only. Archived deltas are deliberately stale against the new baseline; never weaken their version guards to reapply them.

Retain successful tests in STATUS; rerun only checks affected by later changes. Never test via real customer email, Telegram, public posts or advertising. Social drafts remain drafts until real account connections and human approval exist. No advertising budget has been enabled.

## Evidence boundaries

Twenty isolated activation acceptance checks passed against fresh live candidate Code with synthetic fixtures and no transports. Live pre/post graph, schema, identity, binding and publication checks passed. Native Data Table writes and real message delivery were not manually triggered. Strict transactional exactly-once SMTP is not proved by read-then-upsert reservations. Do not automatically resend uncertain actions.
