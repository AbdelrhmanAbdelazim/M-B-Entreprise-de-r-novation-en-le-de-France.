// Pure read-only evidence checks; no HTTP, token handling, publishing or ads.
const META_SCOPES={facebook:['pages_show_list','pages_read_engagement','pages_manage_posts'],instagram:['pages_show_list','pages_read_engagement','instagram_basic','instagram_content_publish']};
function metaOAuthSettings(base,version){
 const url=new URL(base);if(url.protocol!=='https:'||url.username||url.password||url.search||url.hash||url.pathname!=='/'||url.hostname!=='navajowhite-cormorant-668337.hostingersite.com')throw new Error('META_INVALID_CALLBACK_ORIGIN');
 if(!/^v\d+\.0$/.test(version))throw new Error('META_INVALID_API_VERSION');
 return {type:'oAuth2Api',data:{grantType:'authorizationCode',authUrl:'https://www.facebook.com/'+version+'/dialog/oauth',accessTokenUrl:'https://graph.facebook.com/'+version+'/oauth/access_token',scope:[...new Set([...META_SCOPES.facebook,...META_SCOPES.instagram])].join(','),authentication:'body',authQueryParameters:'response_type=code',allowedHttpRequestDomains:'domains',allowedDomains:'graph.facebook.com',ignoreSSLIssues:false},redirect_uri:url.origin+'/rest/oauth2-credential/callback',client_binding_required:['clientId','clientSecret'],authorization_url:null,state_owner:'native n8n OAuth credential flow; never invent state or client identifiers'};
}
function metaPreflightRequests(pageId,igId){
 if(pageId&&!/^\d+$/.test(String(pageId)))throw new Error('META_VERIFIED_PAGE_ID_REQUIRED');
 if(igId&&!/^\d+$/.test(String(igId)))throw new Error('META_INVALID_INSTAGRAM_ID');
 return [{method:'GET',path:'/debug_token',credential:'encrypted_app_credential',sensitive_parameter:'input_token',input_from:'encrypted_user_credential',save_response:false},{method:'GET',path:'/me/permissions',credential:'user_oauth',paginate:true},{method:'GET',path:'/me/accounts',query:{fields:'id,name,tasks,instagram_business_account{id,username}'},credential:'user_oauth',paginate:true},...(pageId?[{method:'GET',path:'/me',query:{fields:'id,name'},credential:'encrypted_page_token'}]:[]),...(igId?[{method:'GET',path:'/'+igId,query:{fields:'id,username'},credential:'encrypted_page_token'},{method:'GET',path:'/'+igId+'/content_publishing_limit',query:{fields:'config,quota_usage'},credential:'encrypted_page_token'}]:[])];
}
function metaEvaluatePreflight(e,expected,timestamp){
 const now=Date.parse(timestamp),maxAge=15*60000,ok=r=>r?.http_status===200&&!r.body?.error&&Number.isFinite(Date.parse(r.observed_at))&&Date.parse(r.observed_at)<=now&&now-Date.parse(r.observed_at)<=maxAge;
 const result={facebook:{permissions_verified:false,reasons:[]},instagram:{permissions_verified:false,reasons:[]},publishing_enabled:false,actual_publication_verified:false};
 const deny=(channel,reason)=>result[channel].reasons.push(reason);
 if(!Number.isFinite(now)||!/^\d+$/.test(expected?.app_id||'')||!/^\d+$/.test(expected?.page_id||'')){for(const channel of ['facebook','instagram'])deny(channel,'missing_verified_app_or_page_identity');return result;}
 const dbg=e?.user_debug?.body?.data,expiry=dbg?.expires_at,accessExpiry=dbg?.data_access_expires_at;
 const userValid=ok(e?.user_debug)&&dbg?.is_valid===true&&String(dbg.app_id)===expected.app_id&&typeof expiry==='number'&&(expiry===0||expiry*1000>now)&&typeof accessExpiry==='number'&&(accessExpiry===0||accessExpiry*1000>now);
 const permissions=ok(e?.permissions)&&e.permissions.complete===true&&Array.isArray(e.permissions.body?.data)?e.permissions.body.data:[];
 const accounts=ok(e?.accounts)&&e.accounts.complete===true&&Array.isArray(e.accounts.body?.data)?e.accounts.body.data:[];
 const pages=accounts.filter(p=>String(p?.id)===expected.page_id),page=pages.length===1?pages[0]:null;
 for(const channel of ['facebook','instagram']){
  if(!userValid)deny(channel,'invalid_expired_unverified_or_wrong_app_token');
  if(!ok(e?.permissions)||e.permissions.complete!==true)deny(channel,'permissions_not_read_or_incomplete');
  for(const scope of META_SCOPES[channel]){
   if(!permissions.some(p=>p?.permission===scope&&p.status==='granted')||!(Array.isArray(dbg?.scopes)&&dbg.scopes.includes(scope)))deny(channel,'scope_not_granted:'+scope);
   if(dbg?.granular_scopes!==undefined&&!Array.isArray(dbg.granular_scopes))deny(channel,'granular_grant_schema_invalid');
   const granular=(Array.isArray(dbg?.granular_scopes)?dbg.granular_scopes:[]).filter(g=>g?.scope===scope);
   if(granular.some(g=>!Array.isArray(g.target_ids)||!g.target_ids.map(String).some(id=>id===expected.page_id||(scope.startsWith('instagram_')&&id===expected.ig_id))))deny(channel,'page_not_in_granular_grant:'+scope);
  }
  if(!ok(e?.accounts)||e.accounts.complete!==true||!page)deny(channel,'page_not_uniquely_discovered');
  if(!Array.isArray(page?.tasks)||!page.tasks.some(t=>['CREATE_CONTENT','MANAGE'].includes(t)))deny(channel,'page_create_content_task_not_granted');
  if(!ok(e?.page_identity)||String(e.page_identity.body?.id)!==expected.page_id)deny(channel,'page_credential_not_verified_for_target');
 }
 const linked=page?.instagram_business_account?.id;
 if(!/^\d+$/.test(expected.ig_id||'')||String(linked)!==expected.ig_id)deny('instagram','instagram_not_linked_to_selected_page');
 if(!ok(e?.instagram_identity)||String(e.instagram_identity.body?.id)!==expected.ig_id)deny('instagram','instagram_identity_not_verified');
 const limit=ok(e?.instagram_limit)&&Array.isArray(e.instagram_limit.body?.data)?e.instagram_limit.body.data[0]:null;
 if(!limit||!Number.isInteger(limit.quota_usage)||limit.quota_usage<0||!Number.isInteger(limit.config?.quota_total)||limit.config.quota_total<=0||limit.quota_usage>=limit.config.quota_total)deny('instagram','publishing_quota_not_verified_or_exhausted');
 for(const channel of ['facebook','instagram'])result[channel].permissions_verified=result[channel].reasons.length===0;
 return result; // Permission evidence never enables a missing transport or claims a public post succeeded.
}
