// Internal CRM linkage only: no model calls, transport, outbound approval or follow-up reset.
function inboundJSON(row){try{return JSON.parse(row?.payload||'{}');}catch{return {};}}
function inboundEmail(value){const s=String(value||'').trim(),m=s.match(/^[^<>]*<([^<>]+)>$/);return String(m?m[1]:s).trim().toLowerCase();}
function inboundNormalize(input){
 const ids={'EvDz4KtOEgIYKh7Q':'email','YjzC3pFzYRR7d2an':'website','fixture':'fixture'};
 if(input.crm_ingest!==true||!ids[input.source_workflow_id]||!Array.isArray(input.events))throw new Error('INBOUND_INVALID_INTERNAL_CONTEXT');
 const dry=input.source_workflow_id==='fixture'||input.crm_dry_run===true;
 return input.events.slice(0,25).filter(r=>['inbound_sales','website_lead'].includes(r?.type)).map(r=>{const p=inboundJSON(r),email=inboundEmail(p.email||p.from);return {source:ids[input.source_workflow_id],dry_run:dry,source_workflow_id:input.source_workflow_id,parent_execution_id:String(input.parent_execution_id||''),client_id:p.client_id||null,client_date:p.client_date||null,contact_name:String(p.nom||'').slice(0,200),original_source:String(p.original_source||p.source||'').slice(0,100),task_key:r.task_key,task_id:r.id,task_status:r.status,task_created_at:r.created_at||r.createdAt,task_payload:r.payload,email,company:String(p.company||p.entreprise||'').slice(0,200),ville:String(p.ville||'').slice(0,200),category:String(p.category||''),text:[p.subject,p.summary,p.projet].filter(Boolean).join('\n').slice(0,4000),project:String(p.projet||'').slice(0,2000)};});
}
function inboundPlan(event,leads,blacklist,queue){
 const result={...event,operation:'held',priority:'WARM',intent:'uncertain',next_action:'Human review; no automatic reply, quote, price, appointment or campaign'};
 const valid=/^[^\s@<>;,]+@[^\s@<>;,]+\.[a-z]{2,}$/i.test(event.email)&&event.email.length<=254;
 if(!valid||(!event.dry_run&&(/\.(test|invalid)$/i.test(event.email)||/@example\.(com|org|net)$/i.test(event.email))))return {...result,reason:'invalid_or_synthetic_contact'};
 const domain=event.email.split('@')[1],free=new Set(['gmail.com','yahoo.fr','yahoo.com','hotmail.fr','hotmail.com','outlook.fr','outlook.com','live.fr','orange.fr','wanadoo.fr','free.fr','sfr.fr','laposte.net','icloud.com','gmx.fr','neuf.fr','bbox.fr']);
 if(blacklist.some(r=>{const b=inboundEmail(r.email);return b===event.email||b===domain||(!free.has(domain)&&b.split('@')[1]===domain);}))return {...result,reason:'blacklist_or_suppression'};
 const text=event.text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 if(/recrutement|candidature|alternance|stage\b|curriculum|unsubscribe|desinscri|ne me contact|ne plus contact|stop\b|automatic reply|reponse automatique|auto.?submitted/.test(text)||['recrutement','refus','desinscription','auto_reply'].includes(event.category))return {...result,reason:'recruitment_optout_or_automated_message'};
 const service=/renov|peintur|plomber|electric|carrel|parquet|salle de bain|cuisine|appartement|degats? des? eaux|travaux|تجديد|حمام|سباكة|كهرباء|دهان|مطبخ|شقة/.test(text),request=/devis|visite|rendez.?vous|souhait|besoin|projet|interess|demande|request|معاينة|عرض سعر|أريد|اريد|أرغب|ارغب|طلب|مشروع|احتاج|أحتاج/.test(text)||['demande_devis','interesse'].includes(event.category);
 if(!service&&!['demande_devis','interesse','demande_documents'].includes(event.category))return {...result,reason:'uncertain_or_irrelevant_inquiry'};
 const local=/paris|ile.de.france|باريس|\b(?:75|77|78|91|92|93|94|95)(?:\d{3})?\b/i.test((event.ville+' '+text).normalize('NFD').replace(/[\u0300-\u036f]/g,''));
 const intent=/devis|عرض سعر/.test(text)||event.category==='demande_devis'?'quote_request':/visite|rendez.?vous|معاينة/.test(text)?'site_visit_request':/partenariat|sous.trait|collabor/.test(text)?'partnership':'general_inquiry';
 const matches=leads.filter(l=>inboundEmail(l.email)===event.email);if(matches.length>1)return {...result,reason:'duplicate_lead_identity'};
 const existing=matches[0];if(existing&&/blacklist|desinscri|unsubscribe|refus|oppose|opt.?out/i.test(String(existing.statut)))return {...result,reason:'existing_contact_suppressed'};const key='crm:inbound:'+event.email;const reservations=queue.filter(r=>r.task_key===key);
 const safe={...result,priority:request&&local?'HOT':'WARM',intent,lead_id:existing?.id||null,existing_lead:existing||null,claim_key:key};
 if(existing?.id===79)return {...safe,reason:'lead79_protected_no_mutation',operation:'link_existing'};
 if(existing)return {...safe,operation:'link_existing',reason:'existing_contact_preserved'};
 if(reservations.length)return {...safe,reason:'prior_or_uncertain_CRM_reservation_no_retry'};
 return {...safe,operation:'create',reason:'relevant_inbound_held_from_cold_outreach',lead:{email:event.email,entreprise:event.company,type:'inbound',ville:event.ville,departement:'',site:'',source:'inbound:'+event.source,statut:'needs_review',variante:'A',date_envoi:'',date_relance:'',date_reponse:'',message_id:'',sujet:''}};
}
function inboundLinkedTask(plan,lead,execution){
 if(!lead?.id||inboundEmail(lead.email)!==plan.email)throw new Error('INBOUND_LEAD_PROOF_MISMATCH');
 const p=inboundJSON({payload:plan.task_payload});return {task_key:plan.task_key,priority:plan.priority,payload:JSON.stringify({...p,crm_link:{state:'linked',lead_id:lead.id,source:plan.source,source_workflow_id:plan.source_workflow_id,dry_run:plan.dry_run===true,relevant_inquiry:true,intent:plan.intent,received_at:plan.task_created_at||null,client_id:plan.client_id,client_date:plan.client_date,service:plan.project,city:plan.ville,priority:plan.priority,original_source:plan.original_source,observed_at:new Date().toISOString(),execution_id:String(execution),outbound_campaign_approved:false,followup_requires_human_review:true}}),next_action:'Inbound linked to Leads #'+lead.id+'; review request and prepare reply/visit. No automatic customer send, quote or booked appointment.'};
}

function inboundFollowupStop(lead,queue){return queue.some(row=>{if(!['inbound_sales','website_lead'].includes(row.type))return false;const p=inboundJSON(row),link=p.crm_link;return link?.state==='linked'&&link.dry_run===false&&link.relevant_inquiry===true&&['EvDz4KtOEgIYKh7Q','YjzC3pFzYRR7d2an'].includes(link.source_workflow_id)&&/^\d+$/.test(String(link.execution_id))&&String(link.lead_id)===String(lead?.id)&&inboundEmail(p.email||p.from)===inboundEmail(lead?.email);});}
