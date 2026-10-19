# Reviewed changes pending live access

These six minimal patches continue production commit `883e99b`. They are **not deployed workflow exports**, new workflows or a replacement for the twelve public production snapshots. Original files, IDs, versions, credentials, webhooks, provider ordering, schedules and W0 remain unchanged.

| Existing workflow | Implemented offline change |
| --- | --- |
| W2 | Read the existing Blacklist immediately before the acknowledgement gate; suppress opted-out recipients without changing website intake or its webhook. |
| W3 | Require exactly one valid HOT/WARM approval; prioritize HOT during selection; make legacy temporary test mode return no email recipients; refuse ambiguous/previous delivery or pending follow-up matched by company or recipient aliases. |
| W4 | Recheck approved HOT/WARM status; refuse ambiguous original outreach, pending/previous follow-up and recipient aliases. |
| W6 | Reserve one management reminder per Paris day in existing Growth Queue before Telegram; record success afterwards; retain reservation on uncertain outcome. |
| W7 | Fail to W0 on source errors, malformed response shape or missing batch responses, rather than falsely completing a zero-result cycle; retain genuine empty cycles; persist location, source URL and opportunity type; use only the extracted website passage as demand evidence. |
| W9 | Read the existing Blacklist immediately before the final delivery guard; reject opt-outs and stale recipient addresses. |

## Focused new verification

```
node --test automation/n8n/tests/growth-regressions.test.mjs
python3 -m unittest discover -s automation/n8n/tests -p 'test_*.py' -v
```

22 behavioral checks and 6 patch-integrity/graph checks passed. These execute only local Code with synthetic `.invalid` records, a fixed clock and in-memory table snapshots. They cannot call SMTP, Telegram, models, advertising or n8n. Tests demonstrate that qualified contacts and real empty search responses still pass. Targeted baseline runs demonstrate 17 failing new cases in the original exported code; this does not invalidate previously documented successful tests.

The Python tests verify preserved workflow/node/credential/webhook/schedule identities; fresh blacklist/reservation edges; refusal of changed versions/nodes/graphs; and refusal to duplicate the W9 node. An end-to-end CLI staging check also succeeded with ignored output. They do **not** prove live n8n node execution or atomic Data Table uniqueness.

## Safe staging after obtaining fresh state

First use the existing read-only `snapshot.py` with secure environment bindings. Inspect fresh live workflow IDs, active/published versions and recent production results. Do not execute production webhooks to test access. Do not paste API keys in chat or Git. A newer live version is a rebase requirement, not permission to overwrite it with these exports.

For a local review candidate (no n8n write):

```
python3 automation/n8n/stage_patch.py --workflow W9 \
  --snapshot automation/n8n/private-live/W9.json \
  --out automation/n8n/private-live/staged/W9-review.json
```

The tool refuses output outside `private-live`, existing output files and version/node/graph drift. It preserves any private bindings in the supplied snapshot. If input is sanitized, output remains sanitized and **must not be imported over production**. The original `versionId` remains a precondition, not a new published version. Apply only the reviewed changes to the same existing workflow after fresh private bindings and live state are verified. Never import a candidate as another workflow or blindly PUT the full export.

No live patch tool, activation, trigger or deployment runs from this command. For added Data Table nodes, validate the real n8n mapping and graph in isolated copies with notification/customer-send nodes disconnected before updating existing production IDs. Internal manager reminders also remain test sinks during verification. Keep error workflows, subworkflows and AI tools under the same isolation.

## Remaining concurrency limit

A Data Table read followed by upsert is not a transactional claim. These changes reject duplicate/conflicting approval rows and previously reserved/uncertain sends, but do not claim strict exactly-once SMTP under simultaneous executions or after a crash between delivery and logging. Existing table schemas/uniqueness and n8n execution concurrency controls require live inspection. Do not invent a new database/table, clear uncertain reservations or resend automatically as a workaround. Pending actions need human delivery reconciliation.
