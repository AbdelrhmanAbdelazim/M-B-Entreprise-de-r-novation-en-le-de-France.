// Provider boundary: pure queue logic. No HTTP, credentials, uploads, publishing or ads.
function metricoolRevision(p) {
  const text = JSON.stringify([p.titre,p.caption,p.cta,p.hashtags,p.video_script,p.platforms,p.media || null]);
  let a=2166136261,b=5381;for(const c of text){a=Math.imul(a^c.charCodeAt(0),16777619);b=Math.imul(b,33)^c.charCodeAt(0);}
  return (a>>>0).toString(16).padStart(8,'0')+(b>>>0).toString(16).padStart(8,'0');
}
function metricoolVariants(p) {
  const caption=String(p.caption || '').trim(),cta=String(p.cta || 'Contactez M&B Rénovation : https://www.maison-mb.fr/').trim();
  const tags=[...new Set((String(p.hashtags || '').match(/#[\p{L}\p{N}_]+/gu)||[]))].slice(0,20).join(' ');
  const text=[caption,cta].filter(Boolean).join('\n\n');
  return {
    google_business_profile:{format:'update',text:text.slice(0,1500),website:'https://www.maison-mb.fr/'},
    facebook:{format:p.media?.type==='video'?'video':p.media?.type==='image'?'image':'text',text:[text,tags].filter(Boolean).join('\n\n').slice(0,5000)},
    instagram:{format:p.media?.type==='video'?'reel':'image',text:[text,tags].filter(Boolean).join('\n\n').slice(0,2200),media_required:true},
    tiktok:{format:'video',text:[text,tags].filter(Boolean).join('\n\n').slice(0,2200),media_required:true},
  };
}
function metricoolQueuePlan(queue,timestamp) {
  const now=new Date(timestamp),iso=now.toISOString(),paris=d=>d.toLocaleString('sv-SE',{timeZone:'Europe/Paris'}).slice(0,19);
  const unpack=r=>{try{return JSON.parse(r.payload||'{}');}catch{return {};}};
  const columns=['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];
  const fields=r=>Object.fromEntries(columns.map(k=>[k,String(r[k]??'')]));
  const make=(key,type,status,payload,next,old=null)=>fields({task_key:key,type,priority:old?.priority || 'WARM',source:'Metricool bridge',owner:type==='publication'?'Metricool':'Manager',status,created_at:old?.created_at || iso,last_action:iso,next_action:next,due_at:old?.due_at || iso,payload:JSON.stringify(payload)});
  const out=[],known=new Set(queue.map(r=>r.task_key));
  const access=queue.filter(r=>r.task_key==='integration:metricool:connection'&&r.source==='Metricool'&&r.status==='done');
  const config=access.length===1?unpack(access[0]):{};
  const authorized=config.read_verified===true&&config.write_verified===true&&typeof config.account_id==='string'&&config.account_id.length>0&&Date.parse(config.verified_at)<=now.getTime()&&now-Date.parse(config.verified_at)<=24*3600000;
  const eligibility=(content,p,channel)=>{
    const media=p.media,mediaOK=media?.approved===true&&/^https:\/\/[^\s@?#]+\//.test(media.url||'')&&['image','video'].includes(media.type);
    if(!authorized)return {status:'blocked_authorization',reason:'Expose existing Metricool API authorization to hosted n8n; accounts remain connected',media:mediaOK?media:null};
    if(!Array.isArray(config.channels)||!config.channels.includes(channel))return {status:'blocked_channel',reason:'Channel not confirmed by actual Metricool account discovery',media:mediaOK?media:null};
    if((channel==='instagram'&&!mediaOK)||(channel==='tiktok'&&(!mediaOK||media.type!=='video')))return {status:'needs_assets',reason:'Approved real project media required; scripts and briefs are not media',media:null};
    if(!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(content.due_at)||content.due_at<=paris(now))return {status:'needs_schedule',reason:'Expired/invalid calendar slot; never publish a catch-up automatically',media:mediaOK?media:null};
    return {status:'ready',reason:'Await authenticated Metricool transport and fresh approval/duplicate reconciliation',media:mediaOK?media:null};
  };
  const mapping={Instagram:'instagram',Reels:'instagram',Facebook:'facebook',TikTok:'tiktok','Google Business Profile':'google_business_profile'};
  for(const content of queue.filter(r=>r.type==='content')) {
    const p=unpack(content),revision=metricoolRevision(p),variants=metricoolVariants(p);
    if(!p.metricool || p.metricool.revision!==revision)out.push(fields({...content,last_action:iso,payload:JSON.stringify({...p,metricool:{revision,variants,bridge:'internal_queue_only_until_verified_API_authorization'}})}));
    if(content.status!=='approved_draft'||p.publication_approval?.revision!==revision)continue;
    const reviews=queue.filter(t=>t.type==='quality_review'&&unpack(t).target===content.task_key);
    if(!reviews.length||reviews.some(t=>t.status!=='done'))continue;
    const channels=[...new Set((Array.isArray(p.platforms)?p.platforms:[]).map(x=>mapping[x]).filter(Boolean))];
    for(const channel of channels) {
      const key='publish:metricool:'+content.task_key+':'+channel;
      // One permanent slot per content/channel. Any attempt, provider ID or uncertain result is reconciled, never recreated.
      if(known.has(key))continue;
      const {status,reason,media}=eligibility(content,p,channel);
      out.push(make(key,'publication',status,{content_key:content.task_key,channel,revision,idempotency_key:key,account_id:authorized?config.account_id:null,variant:variants[channel],media,scheduled_for:content.due_at,timezone:'Europe/Paris',provider_post_id:null,attempt_id:null,provider_state:null},reason));known.add(key);
    }
  }
  // Only a correlated read-confirmed receipt may advance actual provider state.
  for(const publication of queue.filter(r=>r.type==='publication')) {
    if(queue.filter(r=>r.task_key===publication.task_key).length!==1)continue;
    const p=unpack(publication),parent=queue.find(r=>r.task_key===p.content_key&&r.type==='content'),cp=unpack(parent||{});
    const receipts=queue.filter(r=>r.type==='publication_receipt'&&r.source==='Metricool'&&r.status==='done').map(unpack)
      .filter(r=>r.publication_key===publication.task_key&&r.confirmed_by_read===true&&typeof r.provider_post_id==='string'&&r.provider_post_id&&p.attempt_id&&r.attempt_id===p.attempt_id&&['scheduled','published','failed'].includes(r.provider_state)&&Number.isFinite(Date.parse(r.observed_at))&&Date.parse(r.observed_at)<=now.getTime()&&(!p.provider_post_id||p.provider_post_id===r.provider_post_id)&&(!p.last_provider_observation||Date.parse(r.observed_at)>Date.parse(p.last_provider_observation)))
      .sort((a,b)=>Date.parse(b.observed_at)-Date.parse(a.observed_at));
    const receipt=receipts[0];
    if(receipt&&['reserved','uncertain','scheduled','published','failed','cancel_requested'].includes(publication.status)&&!(p.provider_state==='published'&&receipt.provider_state!=='published')) {
      out.push(make(publication.task_key,'publication',receipt.provider_state,{...p,provider_post_id:receipt.provider_post_id,provider_state:receipt.provider_state,last_provider_observation:receipt.observed_at},receipt.provider_state==='failed'?'Provider-confirmed failure; W0 route and human reconciliation, no automatic repost':'Metricool state confirmed by read; no duplicate submission',publication));continue;
    }
    if(!parent||parent.status!=='approved_draft'||cp.publication_approval?.revision!==metricoolRevision(cp)||p.revision!==metricoolRevision(cp)) {
      if(!['published','failed','cancel_requested','held'].includes(publication.status))out.push(make(publication.task_key,'publication',p.provider_post_id?'cancel_requested':'held',{...p,stop_requested:true},p.provider_post_id?'Approval withdrawn/changed; reconcile cancellation in Metricool, never assume cancelled':'Approval withdrawn/changed; no submission',publication));
    } else if(['blocked_authorization','blocked_channel','needs_assets','needs_schedule','ready'].includes(publication.status)&&!p.attempt_id&&!p.provider_post_id){const e=eligibility(parent,cp,p.channel);if(e.status!==publication.status||p.scheduled_for!==parent.due_at)out.push(make(publication.task_key,'publication',e.status,{...p,media:e.media,scheduled_for:parent.due_at,account_id:authorized?config.account_id:null},e.reason,publication));
    } else if(['reserved','uncertain'].includes(publication.status)&&now-Date.parse(publication.last_action)>2*3600000&&publication.status!=='uncertain')out.push(make(publication.task_key,'publication','uncertain',p,'Attempt outcome unknown; read Metricool before any retry, never resend automatically',publication));
  }
  for(const parent of queue.filter(r=>r.type==='content'&&r.status==='approved_draft')){const p=unpack(parent),channels=[...new Set((Array.isArray(p.platforms)?p.platforms:[]).map(x=>mapping[x]).filter(Boolean))];const pubs=channels.map(channel=>queue.find(r=>r.task_key==='publish:metricool:'+parent.task_key+':'+channel&&r.type==='publication'));if(channels.length&&pubs.every(r=>r&&r.status==='published'&&unpack(r).provider_post_id&&unpack(r).revision===metricoolRevision(p)))out.push(fields({...parent,status:'published',last_action:iso,next_action:'All requested channels read-confirmed published in Metricool',payload:JSON.stringify({...p,publication_ids:Object.fromEntries(pubs.map(r=>[unpack(r).channel,unpack(r).provider_post_id])),published_verified_at:iso})}));}
  // Existing scheduled jobs that never started must be visible, not only old running jobs.
  const limit=paris(new Date(now.getTime()-3*3600000));
  for(const job of queue.filter(r=>['radar_run','seo_scan','content_batch'].includes(r.type)&&r.status==='ready'&&r.due_at&&r.due_at.slice(0,19).replace('T',' ')<=limit)) {
    const key='health:overdue:'+job.task_key;
    if(!known.has(key)){out.push(make(key,'health_alert','needs_attention',{workflow:job.owner,target:job.task_key,reason:'scheduled_job_not_completed',observed_at:iso},'Inspect scheduled execution and W0/Journal; do not replay delivery workflows'));known.add(key);}
  }
  const blockedKey='integration:metricool:read-write-access';
  if(!authorized&&!known.has(blockedKey))out.push(make(blockedKey,'integration','needs_attention',{provider:'Metricool',accounts_connected_operator_confirmed:true,API_read_verified:false,API_write_verified:false},'Authorize existing Metricool API connection in hosted n8n; never send tokens in chat'));
  for(const alert of queue.filter(r=>r.type==='health_alert'&&r.status==='needs_attention')){const p=unpack(alert),job=queue.find(r=>r.task_key===p.target);if(p.reason==='scheduled_job_not_completed'&&job?.status==='done')out.push(fields({...alert,status:'done',last_action:iso,next_action:'Scheduled job completion observed; no replay performed'}));}
  const states=Object.fromEntries(['blocked_authorization','blocked_channel','needs_assets','needs_schedule','ready','reserved','uncertain','scheduled','published','failed','cancel_requested'].map(status=>[status,queue.filter(r=>r.type==='publication'&&r.status===status).length]));
  const summary={API_authorization_read_write_verified:authorized,publication_states:states,content_waiting_approval:queue.filter(r=>r.type==='content'&&r.status==='needs_review').length,verified_social_feedback_available:metricoolFeedback(queue,iso).length>0};const previous=queue.find(r=>r.task_key==='metricool:summary');if(!previous||JSON.stringify(unpack(previous))!==JSON.stringify(summary))out.push(make('metricool:summary','integration_report','done',summary,'Read-only Manager summary; external Metricool transport not installed',previous));
  return [...new Map(out.map(r=>[r.task_key,r])).values()];
}
function metricoolFeedback(queue,timestamp) {
  const now=new Date(timestamp),out=[];const unpack=r=>{try{return JSON.parse(r.payload||'{}');}catch{return {};}};
  const date=x=>{if(typeof x!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(x))return false;const d=new Date(x+'T00:00:00Z');return Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===x;};
  const publications=queue.filter(r=>r.type==='publication'&&r.status==='published').map(unpack);
  for(const row of queue.filter(r=>r.type==='analytics_snapshot'&&r.source==='Metricool'&&r.status==='done')) {
    const p=unpack(row),captured=Date.parse(p.captured_at);
    if(p.schema!=='mb.metricool.analytics.v1'||!Number.isFinite(captured)||captured>now.getTime()||now-captured>72*3600000||!date(p.period_start)||!date(p.period_end)||p.period_start>p.period_end||p.period_end>now.toISOString().slice(0,10)||now-new Date(p.period_end+'T00:00:00Z')>8*86400000||!Array.isArray(p.posts))continue;
    const posts=p.posts.slice(0,100).filter(post=>publications.some(pub=>pub.provider_post_id===post.provider_post_id&&pub.channel===post.channel&&pub.account_id===p.account_id)&&['reach','impressions','engagements','clicks'].every(k=>post[k]===undefined||(typeof post[k]==='number'&&Number.isFinite(post[k])&&post[k]>=0)))
      .map(post=>({provider_post_id:post.provider_post_id,channel:post.channel,...Object.fromEntries(['reach','impressions','engagements','clicks'].filter(k=>post[k]!==undefined).map(k=>[k,post[k]]))}));
    if(posts.some(p=>['reach','impressions','engagements','clicks'].some(k=>p[k]!==undefined)))out.push({captured_at:p.captured_at,period_start:p.period_start,period_end:p.period_end,posts:[...new Map(posts.filter(p=>['reach','impressions','engagements','clicks'].some(k=>p[k]!==undefined)).map(p=>[p.channel+':'+p.provider_post_id,p])).values()]});
  }
  // One newest snapshot: never add overlapping periods or Windsor copies of these same posts.
  return out.sort((a,b)=>Date.parse(b.captured_at)-Date.parse(a.captured_at)).slice(0,1);
}

// Future authenticated worker must persist this reservation before its first create request.
// This is a guard, not a claim of atomic locking or a provider request/idempotency capability.
function metricoolReserve(queue,key,timestamp) {
  const unpack=r=>{try{return JSON.parse(r.payload||'{}');}catch{return {};}};
  const rows=queue.filter(r=>r.type==='publication'&&r.task_key===key),now=new Date(timestamp);
  if(rows.length!==1)return {allowed:false,reason:'missing_or_conflicting_publication'};
  const row=rows[0],p=unpack(row),content=queue.find(r=>r.type==='content'&&r.task_key===p.content_key),cp=unpack(content||{});
  if(row.status!=='ready'||p.attempt_id||p.provider_post_id||p.stop_requested)return {allowed:false,reason:'prior_attempt_or_not_ready'};
  if(!content||content.status!=='approved_draft'||cp.publication_approval?.revision!==metricoolRevision(cp)||p.revision!==metricoolRevision(cp))return {allowed:false,reason:'approval_changed'};
  const config=queue.filter(r=>r.task_key==='integration:metricool:connection'&&r.source==='Metricool'&&r.status==='done');
  const a=config.length===1?unpack(config[0]):{};
  if(a.read_verified!==true||a.write_verified!==true||a.account_id!==p.account_id||!Array.isArray(a.channels)||!a.channels.includes(p.channel)||!Number.isFinite(Date.parse(a.verified_at))||Date.parse(a.verified_at)>now.getTime()||now-Date.parse(a.verified_at)>24*3600000)return {allowed:false,reason:'unverified_account_or_channel'};
  const reviews=queue.filter(r=>r.type==='quality_review'&&unpack(r).target===content.task_key);
  if(!reviews.length||reviews.some(r=>r.status!=='done'))return {allowed:false,reason:'quality_review_not_complete'};
  if(p.scheduled_for!==content.due_at||JSON.stringify(p.variant)!==JSON.stringify(metricoolVariants(cp)[p.channel]))return {allowed:false,reason:'schedule_or_variant_changed'};
  const expected=metricoolQueuePlan(queue,timestamp).find(r=>r.task_key===key);
  if(expected&&expected.status!=='ready')return {allowed:false,reason:expected.status};
  if(queue.some(r=>r.type==='publication'&&r.task_key!==key&&unpack(r).content_key===p.content_key&&unpack(r).channel===p.channel))return {allowed:false,reason:'duplicate_target'};
  return {allowed:true,row:{...row,status:'reserved',last_action:now.toISOString(),next_action:'Persist reservation, then one authenticated request; uncertain result requires read reconciliation',payload:JSON.stringify({...p,attempt_id:key+':'+now.toISOString(),reserved_at:now.toISOString()})}};
}
