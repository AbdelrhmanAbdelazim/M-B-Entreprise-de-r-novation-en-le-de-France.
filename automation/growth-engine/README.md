# M&B Rénovation — Growth Engine, production-safe rollout

Status: **SPECIFICATION / NOT DEPLOYED**. This branch is intentionally isolated; no production workflow was changed by this file.

## Verified operational baseline (2026-10-20)
- n8n has 14 workflows (W0–W10 and integration workflows). Preserve the existing production timers, W3 daily email, W4 follow-up, W7 leads, W1 inbound responses, W0 error logging.
- User/Codex reported 14 SMTP-accepted messages for the approved single-use campaign, and SMTP acceptance of report during execution 527. Verify temporary campaign has been disabled; never assume inbox delivery.
- Metricool connected brand ID **7298712** under brand label `MohamedAbdelrahman90` (verify company ownership/branding before publication). Reported network connections: Facebook, Instagram, Threads, LinkedIn, Pinterest, TikTok, GBP and YouTube. **Do not infer API publishing entitlement from listed connections.**
- Metricool API inspection shows already-scheduled `autoPublish:true` PENDING items: post 391473955 on Oct 20 at 18:00 Paris; 391474031 on Oct 21 at 18:00; 391474116 on Oct 22 at 18:00; 397725911 on Oct 22 at 20:30. These are NOT confirmed published. Check provider-specific statuses before retries. Previous post 391473868 encountered Metricool account limit; never blindly retry or reschedule.
- Existing GitHub n8n JSON files are redacted backups. Do not import them over production or mistake a Git commit for a deployment.

## Target architecture (reuse, do not duplicate)
```
Inbound email / website / consented leads -> Normalize -> Identity/deduplication
 -> Gemini classify -> Claude draft (fallback to permitted model)
 -> OpenAI quality/compliance policy gate -> existing W1 or W3/W4
 -> SMTP/IMAP receipts -> CRM outcomes -> daily metrics
                                   |
Owned media -> approved asset library -> Content plan -> platform validator
 -> Metricool schedule inventory -> unique post key -> existing scheduler
 -> provider status reconciliation -> weekly analytics
                                   |
Every day: read-only measurements -> suggestions -> sandbox tests
 -> low-risk, allowlisted configuration changes only
 -> alert / manual approval required for production workflow or account permission changes
```

## Invariants / safety
1. No new outbound campaign, follower messaging, cold scraping, or platform publishing unless recipients/assets are eligible and authorization is confirmed.
2. `lead_id + campaign_id + first_contact` is unique; reserve atomically before sending. Mark accepted only on SMTP evidence; uncertain outcome means manual reconciliation, not retry.
3. Global daily email quota counts W3, W4, one-off sends, and pending runs. A historical campaign approval is not perpetual consent for new campaigns.
4. `platform + account + asset_fingerprint + normalized_copy + planned_date` is a unique scheduled-post key; inspect Metricool scheduled and published statuses before creating or retrying.
5. Every channel honors its individual permissions, content format, API limits, and policy rules. Unavailable / account-limited channels should PAUSE with a visible reason, never trigger paid upgrades.
6. Messages are reviewed against source evidence; do not invent renovations, customer testimonials, authorizations, before/after imagery, prices, work durations, qualifications, or guarantees.
7. Automate analysis and safe tests 24/7, not indiscriminate sending 24/7. Never alter W3/W4 timers or active production workflows without backup and rollback.
8. Never publish code, credentials, tokens, personal lead data, or SMTP recipient lists to this repository.

## Execution stages and acceptance criteria

### Phase 0 — Inventory and preserve production
- Read n8n live workflow IDs, publication state, current failure history and credential *names*, plus production SMTP and reply tracking.
- List Metricool scheduled items, provider-specific statuses and rate/account-limit restrictions; confirm the user's business channels rather than trusting brand label.
- Capture backups/versions and schedule snapshots; create a deployment manifest with exact rollback references.
- Pass only when historical 14-email campaign is reconciled and its one-off sender cannot run again.

### Phase 1 — Lead pipeline
- Reuse W1/W2/W3/W4/W7. Normalize inbound leads and deduplicate company and recipient domains before generation.
- Gemini extracts contact type, location, trade requirement, source, priority and evidence; Claude creates channel-specific French HTML/plaintext; OpenAI independently checks facts, tone, opt-outs and consent.
- Route qualified eligible inbound replies; respect French commercial prospecting/privacy constraints on outbound B2B.
- Gate uncertain or sensitive replies (prices, contracts, booked start dates) for human review.
- Test 20 fixture scenarios: opt-out, duplicate, invalid email, unknown consent, prior send, empty queue, API errors, model hallucination, and HOT priority.

### Phase 2 — Social publishing without duplicate calendars
- Keep existing Metricool schedule as canonical. Validate existing items before generating additional posts.
- Content pillars: authenticated project before/after, renovation education, bathroom/kitchen/painting/flooring tips, B2B subcontracting case studies, testimonials with consent.
- Only use user-owned/licensed media and authorized customer photographs; respect restrictions for people and private homes.
- Each content candidate records image/video asset URI, provenance and rights, captions in French, network eligibility, target URL and UTM campaign.
- Per-network formats and provider status verification. On account-limit failure: pause and report; no automatic spending or blind retry.
- Start with a short controlled pilot on already-authorized accounts, using existing drafts/schedules. Do not create a second post for content already pending.

### Phase 3 — Conversion and reporting
- Attribute inbound leads through verified links, web forms, WhatsApp and business email where possible.
- Track qualified leads -> technical site visits requested -> quotations -> signed contracts; platform reach is a secondary KPI.
- Daily email to the business owner with new qualified leads, actions, SMTP receipts, failures and pending social posts; weekly channel and opportunity report.
- Exclude secrets and private recipient lists from GitHub logs. Confirm report delivery separately from SMTP acceptance.

### Phase 4 — Continuous improvement
- Daily automated read-only evaluations; weekly propose small changes to ranking/content/messages with baseline vs candidate comparisons.
- Version templates and prompt settings; keep a last-known-good rollback.
- Allow autonomous changes only to approved low-risk configuration values within ceilings. Any workflow edits, new channels, extra spend, policy rules, credentials, publication account changes or quota raises require explicit approval.
- Canary/test without customer messages before changing production. Stop/rollback when error rate worsens or duplicate risk occurs.

## Codex/n8n deployment runbook
1. Confirm exact current n8n state and platform permissions via live tools.
2. Create a staging copy of changed components without changing production behavior.
3. Run deterministic fixture tests and inspect execution outputs.
4. Seek approval for any new real outbound/publication beyond prior limited authorizations.
5. Apply bounded, reversible production changes, verify version IDs, and monitor.
6. Report what was actually deployed vs prepared. **Never call this blueprint a live or fully autonomous system.**
