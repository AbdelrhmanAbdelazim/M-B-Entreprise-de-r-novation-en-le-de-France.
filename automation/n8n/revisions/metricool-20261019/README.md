# Metricool internal lifecycle — 19 October 2026

Current engine: all twelve workflows Published/Active. This release changes only Manager, W5 and W10; W7→qualification→W3→W4 and lead #79's no-resend guard remain unchanged. Before snapshots pin commit `bb33e46`; aggregate Code/node deltas and `continuation.json` preserve the full original→qualification→Windsor→Metricool provenance. Do not reapply historical patches over newer live versions.

## Verified access boundary

Social accounts are connected in Metricool according to the operator. Fresh hosted n8n inventory found seven existing credentials, none Metricool; no Metricool node/endpoint exists. Cloud observations show only n8n bindings and no callable Metricool tool. Windsor read access also remains unavailable. No provider request, publication, schedule, analytics read or authentication success is claimed. No accounts were reconnected. No external transport or guessed provider endpoint was installed.

**One user authorization action:** securely authorize the existing Metricool API connection in hosted n8n as a credential named `Metricool`, using the current account/token. Do not reconnect the social accounts or put any secret in chat. Once exposed, authenticated account discovery, exact API contract validation and transport installation can proceed; this credential alone is not proof that those steps have passed.

## Published internal behavior

- W10 drafts receive bounded channel adaptations for GBP, Facebook, Instagram/Reels and TikTok. Reels/Instagram share one target slot. No invented images or portfolio: video scripts are not approved media.
- Manager `/approve ID` for content binds the exact original revision. Existing human approval and quality review remain mandatory. Old approvals without a revision do not cause automatic publication. The seven real drafts remain `needs_review`.
- Hourly Manager creates one permanent `publish:metricool:<content-key>:<channel>` outbox slot only for exactly approved/reviewed content. It verifies discovered account/channel authorization, media and future local calendar. Blocked slots re-evaluate safely; expired slots do not cause catch-up publishing.
- States include blocked_authorization, blocked_channel, needs_assets, needs_schedule, ready, reserved, uncertain, scheduled, published, failed, held and cancel_requested. Provider state/ID and attempt IDs live in each payload. Existing attempted/uncertain/scheduled slots are never recreated or automatically reposted.
- `metricoolReserve` is a pure future-worker gate: fresh approval, review, selected account/channel, exact variant, schedule, aliases and prior attempts are checked before a reservation can be returned. A future authenticated worker must persist it before its one create request. No worker runs in this release. Atomic cross-execution locking/provider idempotency is not proved.
- Only an attempt-correlated, read-confirmed receipt can record a provider post ID and scheduled/published/failed state. Changed approvals hold unpublished work or request reconciliation for an already scheduled post; an external cancellation is never assumed. A parent draft becomes published only when all requested targets are read-confirmed.
- A confirmed failure is marked for error routing before a dedicated Code node throws under the existing W0 error setting. No W0 test notification was sent. New failures are observed on the existing hourly Manager cadence; provider transport remains absent.
- Fresh, bounded Metricool analytics can feed W10/W5 only when linked to known published provider IDs/accounts. Overlapping snapshots and Windsor copies are not summed. Missing data stays missing.
- Manager exposes a deduplicated summary/access task. Overdue radar/SEO/content jobs gain internal health alerts and resolve when completion is observed; no delivery workflow is replayed. Existing W0 catches workflow execution errors.

## Evidence and operating limits

`../../metricool-release.json` records exact live versions and captures. Sixteen isolated policy/workflow checks cover the lifecycle without transports. Four provenance checks validate the new release and its Windsor predecessor. Native Queue upserts/readback verified seven metadata-only adaptations plus one access task and one summary. No provider receipt, analytics snapshot or publication was fabricated. Repeating the actual backfill produces zero writes; original content, quality notes, budgets, statuses and delivery action rows are unchanged.

The future provider adapter must normalize actual runtime receipts as `type=publication_receipt`, `source=Metricool`, `status=done`, with publication_key, attempt_id, provider_post_id, provider_state, observed_at and confirmed_by_read. Analytics use `mb.metricool.analytics.v1`, explicit selected account/date window, zoned capture time and numeric post metrics. Neither contract is a substitute for authenticated provider readback. Existing native Growth Queue columns suffice; no table/schema/schedule/webhook was replaced.
