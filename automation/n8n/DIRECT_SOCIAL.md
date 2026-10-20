## Current Meta read-only evidence — 20 October2026

The existing shared OAuth credential now successfully authenticates the user: native613→614 read Graphv26 identity, actual permissions and complete Pages list. Actual grants: pages_show_list, pages_read_engagement, public_profile. Pages list is empty; company Facebook Page ID and linked Instagram remain unverified. Missing: pages_manage_posts, instagram_basic, instagram_content_publish. No Page token provisioning or publishing transport was enabled. Review those scopes and complete company Page/IG consent through the existing credential; account Connected is insufficient. Other platforms and existing uncertain/scheduled Metricool items remain at their documented boundaries. See provider-readonly-release.json; prior release notes below are historical.

# Direct official publishing — actual deployment boundary

The existing Manager now prepares future official-channel publication intents, using W10's existing calendar/approval state. It no longer creates **new Metricool publication slots**. Legacy Metricool receipt/state reconciliation remains available for existing slots; no Metricool item was submitted, changed, cancelled or retried. The sole publication table is still the existing typed Growth Queue. This is a queue/preflight deployment, **not a working platform publishing transport**.

Native protected command `/social-preflight-safe` via the existing authenticated ingress ran Manager600→observer601 and returned the actual14 W10 drafts awaiting review, zero approved media, eight authorization boundaries, the four unknown Metricool schedule observations and protected391473868. The child read Queue only: no model, SMTP, Telegram, platform HTTP or data write. New internal integration tasks183–190 were separately saved through the existing table API; they grant no permission. Existing schedules, W0 routing and all15 Published/Active workflows were reread after deployment. Only Manager and the observer's internal diagnostic branch changed.

## Safe lifecycle

- W10 owns content/due_at and its existing human/revision/quality review gates.
- New provider-neutral keys use `publish:slot:<content_key>:<channel>`; any prior provider slot for the same content/channel prevents a second slot, regardless of provider/status. Matching copied creative is checked too. No database atomic uniqueness guarantee is claimed.
- Pre-cutover and pending-review drafts are not automatically backfilled. Existing14 drafts and all publication/observation rows were verified byte-for-byte unchanged.
- Media rights approval, media fingerprint, fresh external schedule reconciliation and valid future calendar are checked. All new intents remain blocked because no official account/transport has been authenticated or installed. Filling a credential must not silently enable publishing.
- No existing unknown/failed item is automatically retried.391473868 stays uncertain/permanently reserved. The four other post IDs remain unknown because Metricool API authorization is absent; accounts connected in a UI are insufficient proof.
- Every actual future adapter must reserve durably before create, correlate real account/post/container IDs, poll boundedly, record provider receipts/readback, hold ambiguous outcomes without retry, and route final errors to W0. This transport is **not installed** by the current release. No rendered video, media URL/rights proof, social account inventory or post success is fabricated.

## OAuth setup and review

`direct-social-connections.json` contains service setup portals, requested scopes for review, native n8n callback and read-only preflight contracts. Meta Graph v26 matches the official SDK source inspected. Native GBP/YouTube/LinkedIn credential schemas are available in this n8n, but no authorized account binding exists. YouTube scope configuration should avoid broad partner/audit defaults. TikTok requires its client_key-compatible OAuth and actual Content Posting entitlement; no such native adapter schema was available. Pinterest/Threads need separately verified official OAuth bindings. No ordinary ChatGPT registration/permission is created here.

**Automatic approval review rejected creating persistent publishing OAuth credentials before explicit account/scope consent. No credential-create command executed.** No workaround or indirect credential creation was attempted. All eleven existing credential metadata entries were reread unchanged. The safe alternative is configuration review only; no secret placeholders were deployed as real authorization.

First Meta prerequisite: company-owned developer application at https://developers.facebook.com/apps/ with the documented callback and Facebook/Instagram publishing use cases. Its client configuration and user consent must be handled through encrypted n8n credential UI; never chat/Git/Queue. The proposed empty Meta credential and scopes are reviewable in the configuration file; explicit approval is needed before retrying the rejected credential creation. Native n8n must generate OAuth state. No usable consent URL exists before a real registered client binding, so no fake authorization link is supplied. Target Page token provisioning must remain encrypted and must not appear in saved Manager executions.

Each other platform needs its own applicable developer-product entitlement and account consent; a Meta consent cannot authorize Google/TikTok/LinkedIn/Pinterest/Threads. Existing14 content drafts also require actual editorial/media approval and history reconciliation before any publication.

## Verification and rollback

Twelve isolated direct-social tests cover closed gates, unchanged pending/old drafts, alias/copy/provider deduplication, revision/review checks, replay and protected unknown states. Full live-Queue Code-node replay verified8 blocked integration tasks and0 publication intents. Native600/601 succeeded. Three new direct successor checks and directly affected prior-chain/portable handoff checks passed; the copied test bundle was corrected to include the two newly required source files. Old successful business/model tests were not repeated.

Immutable native-derived public backups and exact reconstruction proof: `revisions/direct-social-20261020/`. They are redacted, **never import them**. Private native backups are ignored under private-live/direct-social-20261020. A rollback must use fresh version preconditions and revert only the two verified graph deltas, retaining IDs/credentials/settings/schedules/tables and uncertainty holds. Do not delete data or recreate workflows. The separate known observer daily-report dry_run defect was not repaired by this social task.
