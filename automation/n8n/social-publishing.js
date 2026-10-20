// Safety-only bridge for the exposed runtime: no authenticated official publisher exists here.
// Never infer write permission from Windsor, a Metricool account, or Queue approval.
function socialPublishingGate(queue, legacyRows, timestamp, cutover) {
  const now=new Date(timestamp),iso=now.toISOString(),start=Date.parse(cutover);
  if(!Number.isFinite(start)||start>now.getTime())throw new Error('SOCIAL_INVALID_POLICY_CUTOVER');
  const incident='391473868',holdKey='publish:hold:metricool:'+incident;
  const unpack=r=>{try{return JSON.parse(r?.payload||'{}');}catch{return {};}};
  const columns=['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];
  const fields=r=>Object.fromEntries(columns.map(k=>[k,String(r[k]??'')]));
  const matches=r=>String(r.task_key||'').includes(incident)||String(r.payload||'').includes(incident);
  const old=key=>queue.find(r=>r.task_key===key);
  const unique=key=>queue.filter(r=>r.task_key===key).length<=1;
  const out=new Map();
  const emit=row=>{if(!unique(row.task_key))return;const before=old(row.task_key);if(before&&columns.filter(k=>k!=='last_action').every(k=>String(before[k]??'')===String(row[k]??'')))return;out.set(row.task_key,fields(row));};
  const record=(key,type,status,payload,next,source='Social publishing guard')=>{const before=old(key);return {...before,task_key:key,type,priority:before?.priority||'WARM',owner:'Manager',source,status,created_at:before?.created_at||iso,last_action:iso,due_at:before?.due_at||iso,next_action:next,payload:JSON.stringify(payload)};};
  const futureApproved=content=>{
    const p=unpack(content),at=Date.parse(content?.created_at),approved=Date.parse(p.publication_approval?.approved_at);
    return content?.type==='content'&&content.status==='approved_draft'&&Number.isFinite(at)&&at>=start&&at<=now.getTime()&&Number.isFinite(approved)&&approved>=start&&approved<=now.getTime()&&p.publication_approval?.revision===metricoolRevision(p)&&queue.some(r=>r.type==='quality_review'&&unpack(r).target===content.task_key)&&!queue.some(r=>r.type==='quality_review'&&unpack(r).target===content.task_key&&r.status!=='done');
  };
  for(const row of legacyRows){
    if(row.task_key===holdKey)continue; // Legacy orphan reconciliation must never cancel/reset this hold.
    if(row.type!=='publication'){emit(row);continue;}
    const p=unpack(row),before=old(row.task_key),parent=queue.find(r=>r.task_key===p.content_key&&r.type==='content');
    if(matches(row)||matches(parent||{}))continue;
    // No migration/catch-up of older drafts, including ones approved later.
    if(!before&&!futureApproved(parent))continue;
    if(['ready','blocked_authorization','blocked_channel','needs_assets','needs_schedule'].includes(row.status)&&!p.attempt_id&&!p.provider_post_id){
      emit({...row,status:futureApproved(parent)?'blocked_authorization':'held',last_action:iso,next_action:'No submission: Metricool quota reported; official API publishing authorization/transport not exposed. No upgrade or automatic catch-up.',payload:JSON.stringify({...p,block_reason:futureApproved(parent)?'metricool_limit_no_verified_official_publisher':'pre_cutover_or_unapproved_content',automatic_retry:false})});
    }else emit(row); // Preserve actual read-confirmed receipts; never generate or fabricate one.
  }
  for(const row of queue.filter(r=>r.type==='publication'&&r.task_key!==holdKey)){
    const p=unpack(row),parent=queue.find(r=>r.task_key===p.content_key&&r.type==='content');
    if(matches(row)||matches(parent||{}))emit({...row,status:'uncertain',last_action:iso,next_action:'Permanent no-resend hold for391473868; platform read reconciliation required, never retry or auto-cancel.',payload:JSON.stringify({...p,stop_requested:true,automatic_retry:false,incident_id:incident})});
    else if(!out.has(row.task_key)&&row.status==='ready'&&!p.attempt_id&&!p.provider_post_id)emit({...row,status:'blocked_authorization',last_action:iso,next_action:'Official publisher not authorized in this runtime; no submission or paid Metricool upgrade.',payload:JSON.stringify({...p,block_reason:'metricool_limit_no_verified_official_publisher',automatic_retry:false})});
  }
  const previous=old(holdKey),p=unpack(previous);
  emit(record(holdKey,'publication','uncertain',{...p,provider:'Metricool',provider_post_id:incident,incident_id:incident,stop_requested:true,automatic_retry:false,reported_failed_platform_count:5,evidence_source:'operator_report',platform_final_state_verified:false,platforms_not_inferred:true},'Permanent no-resend reservation. Final platform outcomes unknown; read reconciliation only, no repost or cancellation.'));
  const accessKey='integration:metricool:read-write-access',access=old(accessKey);
  if(access)emit({...access,status:'needs_attention',last_action:iso,next_action:'Metricool account limit reported. Do not purchase, upgrade or retry publishing; use separately authorized official platform APIs only.',payload:JSON.stringify({...unpack(access),account_limit_operator_reported:true,upgrade_authorized:false,publishing_retry_authorized:false})});
  emit(record('integration:social:official-publishing','integration','needs_attention',{policy:'mb.social.safety.v1',future_content_created_after:cutover,platforms:['facebook','instagram','google_business_profile','tiktok'],verified_publishers:[],official_publishing_transport_installed:false,authorization_state:'not_exposed_to_current_runtime',metricool_account_limit_operator_reported:true,windsor_is_publisher:false,public_test_posts_allowed:false,paid_spend_allowed:false},'Authorize official platform publishing access in hosted n8n through secure OAuth. No public test, no account reconnection, no credentials in chat.'));
  return [...out.values()];
}
