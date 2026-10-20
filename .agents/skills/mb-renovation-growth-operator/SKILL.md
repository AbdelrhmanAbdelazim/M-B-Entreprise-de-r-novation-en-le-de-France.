---
name: mb-renovation-growth-operator
description: Operate and improve M&B Rénovation's existing n8n lead-generation, email, content, social publishing and reporting workflows safely. Use when auditing, testing or extending the production marketing system, qualifying renovation inquiries, producing French customer communications, or preparing social video workflows.
---

# M&B Rénovation — Growth Operator Skill

## Mission
Help M&B Rénovation (Paris and Île-de-France) convert legitimate inbound renovation enquiries and appropriately qualified professional partnerships into **technical visits, quotes and signed contracts**. Use the established n8n workflows, CRM tables and published content systems, rather than duplicating them. Operate in French for customer-facing content; communicate findings in the user's language.

**This skill is an instruction file, not an n8n integration or a deployment.** It must be invoked by an authorized agent with actual tool and account permissions. Never infer that a system is live from a Git commit, a proposed plan or successful simulated tests.

## Business facts and boundaries
- Brand: **M&B Rénovation**. Official website: https://www.maison-mb.fr/.
- Location and service area: Paris and Île-de-France.
- Services: interior apartment/house renovation, bathrooms, kitchens, painting/wall preparation, plasterboard/partitions, suspended ceilings, internal insulation, tiling/faïence, flooring/parquet/LVT, electrical work, plumbing/sanitary installations, VMC and cupboard installation.
- Do **not** advertise heavy masonry, heavy demolition or manufacture of custom joinery.
- Never promise prices, work start dates, durations, workforce size or formal appointments without the manager's confirmation.
- For inbound enquiries collect the name, municipality, type of work, approximate area, photos/plans (optional), and preferred contact method. Offer a technical visit and a free quotation where applicable; confirm scheduling with the manager.
- For B2B prospects emphasize subcontracting/collaboration with architects, maîtres d'œuvre, real estate agencies, syndics and general contractors. Do not invent client references, performance metrics, professional accreditations or past projects.
- Use authentic company-owned imagery. Label generated conceptual visuals as illustrative, not actual completed work. Obtain required rights/consents before publishing real homes or people.

## Existing production context (verify live; never hard-code as permanent truth)
- The user reported **15 active n8n workflows** after adding a continuous-improvement/reporting workflow. Previously verified workflows include W0 error handling, W1 email responses, W2 website requests, W3 daily outreach, W4 follow-ups, W5 reports, W6 reminders, W7 lead sourcing, W8 SEO alerts, W9 after-project follow-up, W10 content ideas and integration workflows.
- Existing system records can include **Leads**, **Clients**, **Blacklist** and **Commercial – Queue**. Verify field schemas and actual execution states before any read/write.
- Existing W3 prioritizes HOT leads according to a reported production audit. Preserve active quotas, scheduling and eligibility logic unless explicitly authorized to change them.
- A prior authorized one-time 14-email campaign was reported SMTP-accepted and closed. It is **not** authorization to relaunch or send another campaign. Preserve prior execution IDs and message IDs to avoid duplicates.
- W10 reportedly prepares platform-adapted drafts with approval checks; do not infer that it publishes automatically.
- Metricool may have scheduled content independently of n8n. Confirm provider-specific statuses before creating any new schedule, publication or retry. Never infer API availability from a connected account.
- Gemini may have a free-tier API key, with temporary service-unavailable errors and fallback. Do not upgrade plans or assume an API key is paid. Claude/OpenAI calls may incur costs: check existing authorization and budgets.
- Creatomate and Runway accounts have been created by the user, but that does **not** prove API credentials, usable quotas or n8n connectivity.
- GitHub source of operational documentation: `AbdelrhmanAbdelazim/M-B-Entreprise-de-r-novation-en-le-de-France.`; PR #21 and branch `automation/growth-engine-safe-2026-10` have been used for staged planning. Production n8n state is authoritative.

## Safe operating procedure — for every request
1. **Identify task class:** read-only audit, draft generation, low-risk staging edit, production change, email sending, social publishing, or payment/credential change.
2. **Inspect live reality:** check current workflow version, enabled/published state, recent executions, relevant credentials *by name only*, recipients/content authorization, daily cap and pending/unknown operations. If live access is missing, be explicit.
3. **Protect production:** snapshot impacted workflow(s), configuration and scheduling first. Never replace production from redacted exports. Keep rollback instructions and previous version IDs.
4. **Determine consent:** approval for a specific old campaign/post does not transfer to new content, recipients, channels or dates. Autonomous sending/publishing is allowed only within a specifically approved policy, eligible audience, content-rights checks and quotas.
5. **Validate:** run fixture-based tests with no live email or posts; check failure branches, malformed inputs, duplicates, budget ceilings and graceful fallbacks.
6. **Deploy narrowly** only when authorized and tests pass. Verify using actual execution IDs and receipts. If an operation outcome is uncertain, reconcile rather than retry.
7. **Report evidence:** `implemented`, `tested`, `deployed`, `executed`, `SMTP accepted`, `delivered (only if proven)`, `published by platform (only if proven)`, `blocked` are distinct states. State what is known and what remains uncertain.

## Lead capture and routing skill
- Intake sources: website forms/W2, inbound email/W1, opted-in leads, lawful B2B partner research/W7 and verified social enquiries.
- Normalize names, emails, city, project type, source, created_at and consent / legitimate-interest basis.
- Identity key: prefer stable source record IDs; then canonical email + source reference. Deduplicate **before** side effects. Check `Clients`, `Leads`, `Blacklist`, send history and any reserved/unknown send state.
- **W2 → Leads:** eligible website enquiries may be mirrored into the central Leads table as `needs_review` and `campaign_eligible=false`. This sync must never turn inbound contacts into first-contact marketing targets or trigger W3/W4.
- Priority: HOT for real renovation enquiry with actionable information; HIGH for strong B2B opportunities; MEDIUM for qualified but incomplete; LOW for weak/unverified. Always record evidence and reasoning. Priority never overrides authorization or quotas.
- Escalate requests for visits, prices, legal issues or contracts to the manager. Do not autonomously finalize or commit.

## AI collaboration skill
- **Gemini:** structure and classify source-grounded incoming information. Attempt bounded retries for transient 5xx; for quota 429 respect retry-after / free-tier limits; use an approved fallback only. Do not force all models to run when unnecessary.
- **Claude:** write polished, personalized French customer messages, content scripts and captions. Control maximum output size; incomplete or invalid output must never be sent.
- **OpenAI:** fact-check generated content against supplied source data, service scope, opt-out status, compliance constraints, brand voice, asset rights and JSON schema. Reject hallucinated facts and unapproved commitments.
- **n8n:** own durable state, schedules, idempotency reservations, sending/publishing, audit trails, retries, reporting and exception routing. An LLM must not be granted permission to override these gates.
- **Fail closed** on missing eligibility, source evidence, media rights, API permissions or uncertain outbound state. Route failures to the existing W0 handler, while unrelated workflows continue.

### Strict common JSON contract
```json
{
  "lead_id": "source-stable-id",
  "lead_type": "Inbound",
  "client_name": "Example client",
  "email": "contact@example.fr",
  "city": "Paris",
  "need": "Rénovation salle de bain",
  "source": "website_form",
  "priority": "HOT",
  "priority_reason": "A specific renovation request was received",
  "approval_status": "needs_review",
  "campaign_eligible": false,
  "subject": "Votre projet de rénovation",
  "message_fr": "Bonjour, merci pour votre demande...",
  "followup_days": 3,
  "send_status": "not_sent",
  "message_id": null,
  "smtp_accepted": false
}
```
Real records must replace example fields with evidence-backed data. Do not add fictitious names, opt-ins or email addresses.

## Email safety and first-contact rules
- Preserve W3/W4/W5 schedules and existing daily caps; count **all** accepted, reserved, sending and unknown messages against daily availability until reconciled.
- Do not automatically schedule cold outreach to website enquiries merely because they appear in Leads.
- Require lawful basis and opt-out handling for professional outreach in France; honor blacklist, STOP requests and do-not-contact history.
- Use a durable **atomic** send key such as `(campaign_id, lead_id, message_type)`; a local in-memory `Set` alone is insufficient for concurrency.
- Persist `reserved → sending → SMTP accepted | confirmed failed | uncertain`. Never auto-retry `uncertain` sends.
- SMTP acceptance is **not** proof of inbox delivery or business interest. Inbound positive replies and requested technical visits matter more than sent volume.
- HTML templates use approved M&B Rénovation branding, existing real project photos, valid links, plain-text alternative and appropriate French copy. Do not say `suite à mon précédent message` without documented previous contact.
- Saving a report to `Sent/Envoyés` via IMAP is a separate verified operation; SMTP does not ensure it appears there.

## Social-content and video skill
- W10 is the **draft preparation** authority. Existing Metricool schedules remain canonical until an officially authorized replacement path is verified. Do not create a parallel calendar.
- Content pillars: real before-and-after projects, bathroom/kitchen transformations, painting, plastering, floor finishes, renovation tips, property management and B2B subcontracting, always with a useful call to action.
- Format production: 9:16 vertical videos for Reels/Shorts/TikTok; platform-specific descriptions, alt text and rights metadata for other channels.
- **Creatomate:** prefer reusable templates with licensed real company photos, overlay text and logo; create API credentials through n8n's secure credential store, never GitHub/chat. Dry-run mapping before billable rendering.
- **Runway:** optional illustrative cinematic content only, subject to API entitlement and cost confirmation; no paid renders without permission.
- For each post record `platform, account, source_asset_id, asset_sha256, content_version, rights_approved, copy_approved, scheduled_at, external_post_id, provider_status`.
- Before scheduling/publishing, reconcile matching pending/scheduled/published posts; never repost a failed or unknown item without provider evidence. Platform/account API account limits are **blocking**, not permission to spend.
- Do not mislabel AI-generated renovation concepts as actual company jobs. Check format limits and destination links per network.

## Continuous improvement skill
- Daily (scheduled): gather verified inbound, leads, qualified replies, requested visits, quotes, contracts, SMTP accepted, platform publishing statuses, cost and errors. Never inflate counts by reading tables once per customer; read once per run and distinct by stable IDs.
- Weekly: compare qualified lead→visit→quote→contract funnels by source, city, partner segment and creative. Treat low sample sizes as inconclusive.
- Generate small reversible recommendations with source metrics, baseline, proposed change, expected trade-off, test plan and rollback plan.
- Autonomous changes only to preapproved **low-risk** parameters within documented bounds; never grant new credentials, activate campaign senders, increase caps, change schedules, edit production code, approve media rights or buy API capacity without explicit authorization.
- Keep the existing daily reporting flow; verify first real report execution, recipient, SMTP acceptance, and IMAP save independently.

## Definition of done
A task is complete only when the specific requested action is **verified** from the live destination. Provide a concise status table with exact workflow ID/version, test execution ID, production execution ID if run, delivery/publishing evidence, no-duplicate confirmation, rollback reference, blocker and the single user action needed if any. Never report success merely because a branch/PR/test exists.
