// Embedded unchanged in W7 Code nodes. Pure policy: no network or delivery transport.
// HOT partnership fit is distinct from an evidenced, currently advertised work request.
function qualifyProspects(leads, blacklist, queue, evidence, timestamp) {
  const now = new Date(timestamp), iso = now.toISOString();
  const policy = 'partner-fit-v1';
  const lower = x => String(x || '').toLowerCase().trim();
  const norm = x => lower(x).normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const free = new Set(['gmail.com','yahoo.fr','yahoo.com','hotmail.fr','hotmail.com','outlook.fr','outlook.com','live.fr','orange.fr','wanadoo.fr','free.fr','sfr.fr','laposte.net','icloud.com','gmx.fr','neuf.fr','bbox.fr']);
  const host = x => lower(x).replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];
  const company = l => { const d = host(l.site || l.domain || lower(l.email).split('@')[1]); return free.has(d) ? lower(l.email) : d; };
  const unpack = t => { try { return JSON.parse(t.payload || '{}'); } catch { return {}; } };
  const columns = ['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];
  const fields = r => Object.fromEntries(columns.map(k => [k, String(r[k] ?? '')]));
  const rows = [], decisions = [];
  for (const l of leads.filter(l => l.statut === 'nouveau' || Number(l.id) === 79)) {
    const email = lower(l.email), domain = email.split('@')[1] || '', key = 'prospect:' + company(l);
    const existing = queue.filter(t => t.task_key === key), old = existing[0], oldp = unpack(old || {});
    const decision = {lead_id:l.id, task_key:key, grade:'COLD', status:'held', reason:''};
    const deny = reason => { decision.reason = reason; };
    if (Number(l.id) === 79) deny('protected_lead_79');
    else if (l.date_envoi || l.date_reponse || l.date_relance || l.unsubscribe || l.blacklist) deny('contact_already_processed_or_stopped');
    else if (!/^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(email) || /^(no-?reply|postmaster|abuse)@/.test(email)) deny('invalid_contact');
    else if (blacklist.some(b => { const e = lower(b.email); return e && (e === email || (!free.has(domain) && e.split('@')[1] === domain)); })) deny('blacklist_or_unsubscribe');
    else if (leads.some(other => String(other.id) !== String(l.id) && (lower(other.email) === email || company(other) === company(l)))) deny('duplicate_contact_or_company');
    else if (queue.some(t => { const p = unpack(t); return (t.type === 'action' || String(t.task_key).startsWith('send:')) && (['send:outreach:','send:followup:'].some(prefix => t.task_key === prefix + company(l)) || [p.email,p.lead?.email,p.result?.email].some(e => lower(e) && lower(e) === email) || p.company === company(l)); })) deny('prior_or_uncertain_contact_action');
    if (existing.length > 1) { decision.reason = 'conflicting_prospect_records'; decisions.push(decision); continue; }
    // Human decisions are authoritative. Only the original W7 review state or this policy is automatic.
    const managed = !old || (old.source === 'W7' && old.status === 'needs_review' && !oldp.qualified_by && (oldp.qualification_policy === policy || old.next_action === 'Qualification humaine avant tout premier contact')) || (oldp.qualification_policy === policy && !oldp.qualified_by && ['approved','needs_review','held'].includes(old.status) && (old.next_action === 'W3: prochain cycle ouvré ; vérifications fraîches obligatoires' || old.next_action.startsWith('Revue humaine : ')));
    if (!managed) { decisions.push({...decision, status:old.status, grade:old.priority, reason:decision.reason || 'preserved_existing_decision'}); continue; }
    const e = evidence.find(e => lower(e.email) === email && host(e.site) === company(l)) || oldp.qualification_evidence;
    const text = norm(e?.text), age = e ? now - new Date(e.observed_at) : NaN;
    const local = /\bparis\b|ile[ -]de[ -]france|\b(?:75|77|78|91|92|93|94|95)\d{3}\b/.test(text);
    const role = /architect|maitri[sz]e d.?oeuvre|maitre d.?oeuvre|syndic|gestion locative|agence immobiliere|gestionnaire de biens|courtage.*travaux/.test(text);
    const interior = /renovat|rehabilit|appartement|amenagement interieur|chantier|parties communes|degats des eaux|travaux/.test(text);
    const contractor = /sous[ -]?trait|entreprises partenaires|reseau d.artisans/.test(text);
    const relevant = ['architecte','maitre_oeuvre','agence','syndic','courtier','gestionnaire'].includes(l.type) || (l.type === 'entreprise_generale' && contractor);
    const evidenceOK = e?.garder === true && e.email_observed === true && lower(e.email) === email && host(e.site) === company(l) && Number.isFinite(age) && age >= 0 && age <= 14 * 86400000;
    const professional = domain === company(l) || domain.endsWith('.' + company(l));
    const requestedWork = /(?:recherch(?:e|ons)|besoin|appel.{0,4}offres|consultation).{0,100}(?:sous.?trait|artisan|entreprise|travaux|renov)|(?:sous.?trait|artisan).{0,80}(?:recherch|partenair)/.test(text);
    if (!decision.reason) {
      if (e?.garder === false || !relevant) deny('irrelevant_or_competitor');
      else if (!evidenceOK) { decision.grade = 'WARM'; decision.status = 'needs_review'; deny('missing_or_stale_verified_source'); }
      else if (professional && local && role && interior) { decision.grade = 'HOT'; decision.status = 'approved'; decision.reason = 'verified_local_renovation_partner_fit'; }
      else { decision.grade = 'WARM'; decision.status = 'needs_review'; deny('uncertain_location_contact_or_project_fit'); }
    }
    const score = decision.grade === 'HOT' ? (requestedWork ? 100 : 90) : decision.grade === 'WARM' ? 60 : 0;
    const payload = {...oldp, email, company:company(l), entreprise:l.entreprise, site:l.site, type:l.type,
      ville:l.ville || '', departement:l.departement || '', location:[l.ville,l.departement].filter(Boolean).join(' '),
      source:l.source, source_url:e?.source_url || '', discovered_at:oldp.discovered_at || l.createdAt || iso,
      grade:decision.grade, score, opportunity_type:requestedWork ? 'evidenced_work_request' : 'b2b_partnership',
      qualification_policy:policy, qualified_at:iso, qualification_expires_at:evidenceOK ? new Date(new Date(e.observed_at).getTime() + 14 * 86400000).toISOString() : null,
      qualification_reason:decision.reason, qualification_evidence:e || null,
      evidence:decision.reason, auto_approved:decision.status === 'approved'};
    // Stable decisions produce no repeat writes; evidence expiry and safety changes still take effect.
    if (old && oldp.qualification_policy === policy && old.status === decision.status && old.priority === decision.grade && oldp.qualification_reason === decision.reason && JSON.stringify(oldp.qualification_evidence) === JSON.stringify(e || null)) { decisions.push(decision); continue; }
    rows.push(fields({task_key:key,type:'prospect',priority:decision.grade,source:'W7',owner:'W3',status:decision.status,
      created_at:old?.created_at || iso,last_action:iso,due_at:old?.due_at || iso,payload:JSON.stringify(payload),
      next_action:decision.status === 'approved' ? 'W3: prochain cycle ouvré ; vérifications fraîches obligatoires' : 'Revue humaine : ' + decision.reason}));
    decisions.push(decision);
  }
  return {rows, decisions};
}
