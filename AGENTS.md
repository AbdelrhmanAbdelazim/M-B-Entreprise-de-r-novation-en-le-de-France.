# M&B Rénovation — Codex Instructions

## Project
This repository contains the official website of M&B Rénovation:
https://www.maison-mb.fr/

The site uses Jekyll and GitHub Pages.

## Primary objective
Improve the website to generate qualified renovation leads in Paris and Île-de-France while preserving stability, SEO, existing URLs, and the current design.

## Brand
Use the brand consistently:
M&B Rénovation

Positioning:
Entreprise & Artisan Rénovation Paris / Île-de-France.
Interior renovation and subcontracting.

## Services
The company provides:
- Apartment and house renovation
- Bathroom renovation
- Kitchen renovation
- Electricity
- Plumbing
- Plastering and partitions
- False ceilings
- Interior insulation
- Tiling and faience
- Painting and wall preparation
- Parquet and flooring
- LVT flooring
- Cupboard installation
- VMC

Do not claim services that the company does not provide, including heavy demolition or custom-made joinery.

## Working rules
Before modifying the repository:

1. Inspect the existing implementation.
2. Preserve working URLs and redirects.
3. Preserve existing SEO improvements.
4. Preserve responsive/mobile behavior.
5. Do not create duplicate or doorway SEO pages.
6. Do not invent company information, certifications, guarantees, reviews, projects, prices, or services.
7. Do not change legal information unless explicitly requested.
8. Do not delete existing content unless necessary and justified.
9. Prefer small, reversible changes.
10. Never expose API keys, credentials, tokens, passwords, or secrets.

## Validation
Before proposing or publishing changes:

- Build the Jekyll site successfully.
- Check internal links.
- Check navigation.
- Check mobile layout.
- Check metadata and canonical URLs.
- Check sitemap integrity.
- Check structured data when affected.
- Avoid duplicate titles and meta descriptions.

Do not claim validation passed unless it was actually executed.

## Git safety
Do not modify main blindly.

For substantial changes:
- inspect first;
- make the smallest necessary change;
- test it;
- clearly report what changed.

Do not merge, deploy, publish, or make destructive changes unless explicitly authorized.

## Business priority
When several technically valid options exist, prefer the option most likely to improve:
1. qualified leads;
2. quote requests;
3. phone/WhatsApp contacts;
4. local SEO visibility;
5. trust and conversion;
6. partnerships with architects, property managers, real-estate agencies, syndics and contractors.

Do not sacrifice site quality or search-engine compliance for short-term SEO tactics.

## n8n / Growth Engine continuation

For automation tasks, read `CLOUD_RESUME.md` and `automation/n8n/STATUS.md` first. The latest reviewed work is on `codex/growth-engine-883e99b`; preserve newer remote work and user changes when selecting a checkout. Keep the twelve production baseline exports distinct from `automation/n8n/pending/` deltas.

Use existing isolated checkouts, not new worktrees unless requested. Cloud handoff tools need only Python standard library, not a Mac or website build. Retain successful tests recorded in STATUS; rerun only those directly affected by new changes. Never import redacted workflow exports over production. No real customer test messages, public test posts or ad spending. API timeout is not a reason to replace credentials, modify the server, reset workflow versions or stop independent local work. Record live deployment as pending until current versions and isolated runtime checks are available.

## ChatGPT operational ingress

For operational commands that the user wants routed through Manager/Codex, use `automation/n8n/ingress.py` with the existing `N8N_BASE_URL` and `N8N_API_KEY` bindings. Read the latest STATUS and `ingress-openapi.json` first. Submit a UTF-8 private task file with a stable request ID; on timeout poll/retry that same ID. Read the actual final result before reporting completion. The caller helper generates a UUID when absent and preserves it across bounded retries. Do not ask the user to copy prompts, IDs or secrets into n8n. Keep private task files outside Git.

The ingress is authenticated; never publish the key, weaken the gate or turn on ingress execution-payload saving. Respect existing delivery approvals, blacklists, deduplication, lead #79 and paid-ad restrictions. A remote Agent text response is not evidence of a workflow/repository mutation: verify actual deployed state whenever a command requires a change. The hosted Agent currently has no external tools/vaults; do not fabricate those permissions. Ordinary ChatGPT Action/MCP registration is separate from this Codex environment's HTTP access.

## Ordinary ChatGPT MCP connection

The hosted MCP server and connection details are in `automation/n8n/mcp-connect.json`. Read `mcp-release.json`: server publication is verified, ordinary ChatGPT account registration/consent and an actual ChatGPT-origin task are still pending. Never change that status based only on a shell HTTP request or the historical ingress proof. When the user reports connecting the app, inspect the actual tool availability for `submit_codex_task` and `get_codex_task_status`; only a real invocation from the connected ChatGPT context can satisfy the client test. Do not impersonate account consent or promise to bypass ChatGPT write-tool approvals. The independent bridge credential stays encrypted in n8n; do not request, export or replace it.
