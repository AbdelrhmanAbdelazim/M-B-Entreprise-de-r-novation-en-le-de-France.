// Historical read-only evidence, never an authorization to render, upload or publish.
function mbVideoProviderRows(rows,evidence){
 const snapshots={
  observed_at_utc:evidence.observed_at_utc,
  execution_id:String(evidence.execution_id),
  meta:{identity_read:evidence.meta?.user_identity_read===true,page_verified:evidence.meta?.page_identity_verified===true,missing_scopes:evidence.meta?.missing_scopes||{},publisher_enabled:false},
  creatomate:{credential_present:evidence.creatomate?.credential_present===true,authentication_verified:evidence.creatomate?.authentication_verified===true,plan_verified:evidence.creatomate?.plan_verified===true,credits_verified:evidence.creatomate?.credits_verified===true},
  runway:{credential_present:evidence.runway?.credential_present===true,authentication_verified:evidence.runway?.authentication_verified===true,api_credits:evidence.runway?.api_credits??null,generation_enabled:false},
  evidence_is_historical:true,requires_fresh_preflight:true
 };
 const assets=new Map();
 const out=rows.map(item=>{
  const r=item.json;if(r?.type!=='content')return item;
  const p=JSON.parse(r.payload),v=p.video_draft;if(!v)return item;
  const blocks=['render_transport_disabled','no_render_spend_authorization','fresh_provider_auth_plan_and_credit_proof_required','per_asset_rights_and_http_review_required','openai_quality_review_and_human_approval_required','existing_publication_and_render_reconciliation_required'];
  const video={...v,provider_readiness:snapshots,status:'blocked_preflight_and_approval',render_enabled:false,publish_enabled:false,spending_authorized:false,
   preflight:{allowed:false,blocks,required_before_render:['stable_render_key_reserved','no_existing_or_uncertain_render','exact_content_revision_approved','all_media_rights_approved','all_media_https_and_sha256_verified','quality_review_passed','fresh_provider_authentication','plan_and_credit_cost_verified','explicit_render_spend_authorization'],never_retry_uncertain_submission:true},
   optional_runway:{...v.optional_runway,enabled:false,api_verified:snapshots.runway.authentication_verified,credit_balance:snapshots.runway.api_credits,reason:'Existing API credential read-only result is recorded; generation remains disabled regardless of balance.'}};
  const asset={...p,video_draft:video};assets.set(r.task_key,asset);return {json:{...r,payload:JSON.stringify(asset)}};
 });
 return out.map(item=>{
  if(item.json?.type!=='quality_review')return item;
  const p=JSON.parse(item.json.payload),asset=assets.get(p.target);return asset?{json:{...item.json,owner:'OpenAI',payload:JSON.stringify({...p,content:asset,video_review_required:true})}}:item;
 });
}
