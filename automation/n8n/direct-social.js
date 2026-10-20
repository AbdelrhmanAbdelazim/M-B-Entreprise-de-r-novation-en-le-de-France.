// Official-channel preparation only. No HTTP, token handling, uploads, spending or publishing.
// A credential slot is not an authenticated account or permission proof.
const DIRECT_SOCIAL_CHANNELS=['facebook','instagram','google_business_profile','tiktok','youtube_shorts','linkedin','pinterest','threads'];
function directSocialJSON(row){try{return JSON.parse(row?.payload||'{}');}catch{return {};}}
function directSocialChannel(value){return {Facebook:'facebook',Instagram:'instagram',Reels:'instagram',TikTok:'tiktok','YouTube Shorts':'youtube_shorts',LinkedIn:'linkedin',Pinterest:'pinterest',Threads:'threads','Google Business Profile':'google_business_profile'}[value]|| (DIRECT_SOCIAL_CHANNELS.includes(value)?value:null);}
function directSocialAudit(queue,timestamp){
 if(!Array.isArray(queue)||!Number.isFinite(Date.parse(timestamp)))throw new Error('DIRECT_SOCIAL_INVALID_INPUT');
 const contents=queue.filter(r=>r.type==='content'),publications=queue.filter(r=>r.type==='publication');
 return {status:'BLOCKED_AUTHORIZATION_NO_OFFICIAL_TRANSPORT',observed_at_utc:timestamp,transport_executed:false,model_calls:0,data_write_executed:false,
  content_drafts:contents.length,content_awaiting_review:contents.filter(r=>r.status!=='approved_draft').length,
  approved_media:contents.filter(r=>directSocialJSON(r).media?.approved===true).length,
  platforms:DIRECT_SOCIAL_CHANNELS.map(channel=>({channel,publishing_enabled:false,official_transport_installed:false,account_permission_verified:false,connection_evidence:'No authenticated official account verification has been recorded; credential slots alone do not count',integration_task_key:'integration:direct-social:'+channel})),
  metricool_observations:queue.filter(r=>r.type==='publication_observation').map(r=>({provider_post_id:directSocialJSON(r).provider_post_id,actual_state:'not_verified'})),
  protected_post_391473868:publications.some(r=>r.status==='uncertain'&&(r.task_key==='publish:hold:metricool:391473868'||directSocialJSON(r).provider_post_id==='391473868')),
  paid_spending_enabled:false,calendar_owner:'existing W10 due_at + Manager hourly coordinator; existing Metricool schedules remain untouched'};
}
function directSocialPlan(queue,timestamp,cutover){
 if(!Array.isArray(queue)||!Number.isFinite(Date.parse(timestamp))||!Number.isFinite(Date.parse(cutover))||Date.parse(cutover)>Date.parse(timestamp))throw new Error('DIRECT_SOCIAL_INVALID_INPUT');
 const now=new Date(timestamp),iso=now.toISOString(),out=[],known=new Set(queue.map(r=>r.task_key)),columns=['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];
 const row=(key,type,status,payload,due,next)=>Object.fromEntries(columns.map(k=>[k,String(({task_key:key,type,priority:'WARM',source:'Official direct social preparation',owner:'Manager',status,created_at:iso,last_action:iso,next_action:next,due_at:due,payload:JSON.stringify(payload)})[k]??'')]));
 for(const channel of DIRECT_SOCIAL_CHANNELS){const key='integration:direct-social:'+channel;if(!known.has(key)){out.push(row(key,'integration','needs_attention',{channel,official_only:true,publishing_enabled:false,transport_installed:false,permission_verified:false,authorization_required:true,no_spending:true},iso,'Bind company-owned developer application and OAuth through encrypted n8n credentials; verify read-only account/permission evidence. No public test or paid service.'));known.add(key);}}
 const normalize=s=>String(s||'').trim().replace(/\s+/g,' ').toLowerCase();
 const contents=queue.filter(r=>r.type==='content');
 for(const c of contents){
  const p=directSocialJSON(c),created=Date.parse(c.created_at),approval=p.publication_approval;
  // Never backfill an old draft or use a quality-review completion as publication consent.
  if(c.status!=='approved_draft'||!Number.isFinite(created)||created<Date.parse(cutover)||created>now.getTime()||String(c.task_key).includes('391473868')||JSON.stringify(p).includes('391473868'))continue;
  const revision=metricoolRevision(p);
  if(approval?.revision!==revision||!Number.isFinite(Date.parse(approval.approved_at))||Date.parse(approval.approved_at)>now.getTime()||Date.parse(approval.approved_at)<created)continue;
  const reviews=queue.filter(r=>r.type==='quality_review'&&directSocialJSON(r).target===c.task_key);if(!reviews.length||reviews.some(r=>r.status!=='done'))continue;
  const channels=[...new Set((Array.isArray(p.platforms)?p.platforms:[]).map(directSocialChannel).filter(Boolean))];
  for(const channel of channels){
   const key='publish:slot:'+c.task_key+':'+channel;if(known.has(key))continue;
   const related=queue.filter(r=>r.type==='publication'&&directSocialChannel(directSocialJSON(r).channel)===channel&&directSocialJSON(r).content_key===c.task_key);
   // Any existing provider slot/attempt/state is reconciled in place, never migrated or retried.
   if(related.length)continue;
   const sameCreative=contents.filter(r=>r.task_key!==c.task_key).filter(r=>{const x=directSocialJSON(r);return normalize(x.caption)===normalize(p.caption)&&normalize(x.cta)===normalize(p.cta)&&String(x.media?.url||'')===String(p.media?.url||'');});
   if(sameCreative.some(other=>queue.some(r=>r.type==='publication'&&directSocialJSON(r).content_key===other.task_key&&directSocialChannel(directSocialJSON(r).channel)===channel)))continue;
   const media=p.media,mediaOK=media?.approved===true&&media.rights_approved===true&&typeof media.asset_sha256==='string'&&/^[a-f0-9]{64}$/i.test(media.asset_sha256)&&/^https:\/\/[^\s@?#]+\//.test(media.url||'')&&['image','video'].includes(media.type);
   const reconciled=p.external_schedule_check?.verified===true&&p.external_schedule_check.revision===revision&&Number.isFinite(Date.parse(p.external_schedule_check.checked_at))&&Date.parse(p.external_schedule_check.checked_at)<=now.getTime()&&now-Date.parse(p.external_schedule_check.checked_at)<24*3600000&&p.external_schedule_check.no_existing_publication===true;
   const future=/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(c.due_at)&&c.due_at>now.toLocaleString('sv-SE',{timeZone:'Europe/Paris'}).slice(0,19);
   const reason=!reconciled?'metricool_and_platform_history_not_reconciled':!mediaOK?'approved_rights_and_media_hash_required':!future?'expired_or_invalid_schedule':'official_account_authorization_and_transport_missing';
   out.push(row(key,'publication','blocked_authorization',{provider:'official_direct',channel,content_key:c.task_key,revision,idempotency_key:key,scheduled_for:c.due_at,timezone:'Europe/Paris',variant:p.social_drafts?.[channel]||null,media:mediaOK?media:null,block_reason:reason,provider_post_id:null,attempt_id:null,automatic_retry:false,publishing_enabled:false,transport_installed:false},c.due_at,'No submission. Resolve '+reason+' through approved official adapter; preserve current calendar and uncertain holds.'));known.add(key);
  }
 }
 return out;
}
