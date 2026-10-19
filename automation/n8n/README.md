# Portable n8n continuation bundle

Start with [STATUS.md](STATUS.md), then [manifest.json](manifest.json) and [data-tables.json](data-tables.json). Read the repository root AGENTS.md. These are the last verified actual production exports, sanitized for this public repository. They are not fresh live exports after the documented host outage and are not directly deployable until private bindings are restored from the same existing live workflows.

## Cloud setup

Python3 standard library only; no Mac paths, local browser, npm install, React app or Jekyll build is needed to read/validate this bundle. Existing successful business tests must not be repeated merely for handoff.

Set the environment variables named in `.env.example` through the Cloud environment secret/configuration UI. Do not commit a populated .env. N8N_API_KEY authorizes API reads; its presence alone is not proof of access. Allow HTTPS to the documented n8n host in the Cloud environment network settings; preserve proxy and CA trust. Runtime configuration/network readiness must be verified in the actual Cloud session. Local GitHub authentication does not authenticate to n8n.

```
python3 automation/n8n/validate.py
python3 automation/n8n/snapshot.py --out automation/n8n/private-live
```

The first command validates this new handoff artifact offline. The second is read-only and must only run once the host and Cloud access are healthy. It sends GET requests for the twelve existing workflow IDs and saves sanitized snapshots with provenance; it cannot execute, create, update, activate, publish or delete a workflow, send messages or spend money. Redirects are not followed with the API key. Never replace a deployed workflow from these redacted copies. Pull fresh live bindings, inspect a minimal diff, keep the same workflow IDs, and explicitly review any future write operation.

No provider API keys, operational credential IDs, Telegram destinations, webhook routes, customer table rows or browser sessions are stored here. Existing credential types/names and workflow/data-table IDs describe dependencies; placeholders do not create credentials. Redacted JSON paths are in manifest. Full original table schemas other than the verified Growth Queue contract must be read from n8n; do not recreate them from guesses.

The n8n server returned500/504 during this handoff. Control from Cloud is therefore not yet demonstrated. Once network policy and the secret binding are ready and the host responds, a Cloud task can continue directly from GitHub without this Mac. The website/mb/React setup is independent and should not block this automation work.

## Continuation from commit 883e99b

Latest Cloud findings and pending changes are in [STATUS.md](STATUS.md), [continuation.json](continuation.json) and [pending/README.md](pending/README.md). The historical 500/504 observation above is not a current host-health conclusion: the Cloud request was denied by its proxy before reaching the host. Secure n8n requirements were saved to the environment draft but are not configured/applied in the running instance.

The original twelve exports remain the production baseline. Pending patches and `stage_patch.py` provide tested local deltas with version/node/graph guards, not published changes. Only the new changed behavior was tested; successful model/content/SEO business tests from the prior session were retained.
