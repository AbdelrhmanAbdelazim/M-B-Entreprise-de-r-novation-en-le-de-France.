// OpenAI Agents beta schema pinned in agents-api-schema.json. No secrets or network transports here.
function codexHash(text){let a=2166136261,b=5381;for(const c of String(text)){a=Math.imul(a^c.charCodeAt(0),16777619);b=Math.imul(b,33)^c.charCodeAt(0);}return(a>>>0).toString(16)+(b>>>0).toString(16);}
function codexUnpack(row){try{return JSON.parse(row?.payload||'{}');}catch{return {};}}
function codexSafe(text){return String(text||'').replace(/\b(?:sk-(?:proj-|ant-)?[a-zA-Z0-9_-]{12,}|Bearer\s+\S+|(?:api[_-]?key|password|access_token)\s*[:=]\s*[^\s,;}]+)/gi,'[REDACTED]').slice(0,16000);}
function codexRow(key,type,status,payload,now,previous){const columns=['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];const r={task_key:key,type,priority:previous?.priority||'WARM',source:'OpenAI Agents API',owner:'Codex',status,created_at:previous?.created_at||now,last_action:now,next_action:status==='done'?'Result retrieved; no repeat submission':'Inspect task status; never replay uncertain POST',due_at:now,payload:JSON.stringify(payload)};return Object.fromEntries(columns.map(k=>[k,String(r[k]??'')]));}
function codexSelect(queue,now,executionId,forcedKey=null){
  const jobs=queue.filter(r=>r.type==='agent_task'),stamp=Date.parse(now);
  const active=jobs.find(r=>['running','submitting'].includes(r.status)&&stamp-Date.parse(r.last_action)<15*60000);
  if(active)return null;
  const due=value=>{if(!value)return true;if(value.includes('T')&&Number.isFinite(Date.parse(value)))return Date.parse(value)<=stamp;return value.slice(0,19)<=new Date(now).toLocaleString('sv-SE',{timeZone:'Europe/Paris'}).slice(0,19);};
  const job=jobs.filter(r=>(!forcedKey||r.task_key===forcedKey)&&(['ready','uncertain'].includes(r.status)||(['running','submitting'].includes(r.status)&&stamp-Date.parse(r.last_action)>=15*60000))&&due(r.due_at)).sort((a,b)=>String(a.created_at).localeCompare(String(b.created_at)))[0];
  if(!job)return null;
  const p=codexUnpack(job),instruction=String(p.instruction||p.title||'').trim();
  const fingerprint=codexHash('gpt-6-astra|'+instruction);
  const base={...p,job_key:job.task_key,job,model:'gpt-6-astra',instruction,fingerprint,execution_id:String(executionId),started_at:now,deadline_at:new Date(stamp+240000).toISOString(),resume:['uncertain','running','submitting'].includes(job.status),resume_count:Number(p.resume_count||0)+(job.status==='ready'?0:1)};
  const prior=jobs.find(r=>r.task_key!==job.task_key&&r.status==='done'&&codexUnpack(r).fingerprint===fingerprint);
  if(prior)return {...base,...codexUnpack(prior),job_key:job.task_key,job,is_test:p.is_test===true,reused_from_task:prior.task_key,route:'finish',status:'done'};
  if(!instruction||instruction.length>12000||codexSafe(instruction)!==instruction)return {...base,route:'finish',status:'failed',error:'invalid_or_secret_bearing_instruction'};
  if(base.resume_count>3)return {...base,route:'finish',status:'needs_attention',error:'bounded_resume_limit_reached'};
  if(base.resume&&(!p.session_id||!Array.isArray(p.baseline_turn_ids)))return {...base,route:'finish',status:'needs_attention',error:'uncertain_pre_submission_state_requires_reconciliation'};
  const sessions=queue.filter(r=>r.task_key==='codex:session:manager'&&r.type==='agent_session');
  if(sessions.length>1)return {...base,route:'finish',status:'needs_attention',error:'conflicting_session_records'};
  return {...base,session_id:p.session_id||codexUnpack(sessions[0]).session_id||null,route:base.resume?'poll':'session'};
}
function codexResponse(value){const status=Number(value?.statusCode||0);let body=value?.body??value;if(typeof body==='string'){try{body=JSON.parse(body);}catch{body={};}}return{status,body,transport_error:!!value?.error};}
function codexStep(stage,value,ctx,now,iteration=1){
  const r=codexResponse(value),fail=(message,status='failed')=>({...ctx,route:'finish',status,error:codexSafe(message),http_status:r.status});
  if(stage==='session'){
    if(r.status===404)return {...ctx,session_id:null,route:'create'};
    if(r.transport_error||r.status>=400||!/^sess_[A-Za-z0-9_-]+$/.test(r.body.id||''))return fail('session_read_or_create_failed',r.transport_error?'uncertain':'failed');
    if(r.body.status!=='idle')return fail('session_not_idle:'+String(r.body.status),'needs_attention');
    if(ctx.session_id&&r.body.id!==ctx.session_id)return fail('session_identity_mismatch');
    return {...ctx,session_id:r.body.id,route:'baseline'};
  }
  if(stage==='baseline'){
    if(r.transport_error||r.status>=400||!Array.isArray(r.body.data))return fail('baseline_turn_read_failed');
    return {...ctx,baseline_turn_ids:r.body.data.map(t=>t.id),submitted_at:now,submission_key:'mb-codex:'+ctx.job_key,route:'submit'};
  }
  if(stage==='ack'){
    if(r.status===429&&iteration<=2)return {...ctx,route:'retry',retry_count:iteration};
    if(r.transport_error||!r.status||r.status>=500)return {...ctx,route:'poll',submission_uncertain:true};
    if(r.status<200||r.status>=300)return fail('event_submission_rejected:'+String(r.body.error?.message||r.status));
    return {...ctx,route:'poll',accepted_at:now};
  }
  if(stage==='turn'){
    if(Date.parse(now)>Date.parse(ctx.deadline_at)||iteration>24)return fail('completion_poll_deadline_exceeded','uncertain');
    if(r.transport_error||r.status===429||r.status>=500)return {...ctx,route:'wait',poll_count:iteration};
    if(r.status>=400||!Array.isArray(r.body.data))return fail('turn_read_failed','uncertain');
    const turns=r.body.data.filter(t=>t.session_id===ctx.session_id&&(!ctx.turn_id?!ctx.baseline_turn_ids.includes(t.id):t.id===ctx.turn_id));
    if(turns.length>1)return fail('ambiguous_new_turns_no_automatic_resubmission','needs_attention');
    const turn=turns[0];if(!turn)return {...ctx,route:'wait',poll_count:iteration};
    const next={...ctx,turn_id:turn.id,turn_status:turn.status,poll_count:iteration};
    if(turn.status==='completed')return {...next,route:'items'};
    if(['failed','cancelled'].includes(turn.status))return {...next,route:'finish',status:turn.status,error:codexSafe(turn.error?.message||turn.status)};
    if(turn.status==='waiting')return {...next,route:'finish',status:'needs_attention',error:'external_tool_or_approval_required_no_automatic_grant'};
    return {...next,route:'wait'};
  }
  if(stage==='items'){
    if(r.transport_error||r.status>=400||!Array.isArray(r.body.data))return fail('completed_turn_items_read_failed','uncertain');
    const messages=r.body.data.filter(i=>i.type==='message'&&i.role==='assistant'&&i.turn_id===ctx.turn_id&&i.status==='completed'&&i.phase==='final_answer');
    const text=messages.map(i=>(i.content||[]).filter(c=>c.type==='output_text').map(c=>c.text).join('')).reverse().join('\n').trim();
    if(!text)return fail('completed_turn_has_no_final_assistant_result','uncertain');
    if(ctx.is_test&&text!=='M&B Codex connected successfully')return fail('internal_test_final_text_mismatch');
    return {...ctx,route:'finish',status:'done',result:codexSafe(text),completed_at:now};
  }
  return fail('unknown_state');
}
function codexFinish(ctx,now){
  const previous=codexUnpack(ctx.job),notify=ctx.status!=='done'&&ctx.is_test!==true&&!previous.w0_reported;
  const p={instruction:ctx.instruction,model:ctx.model,fingerprint:ctx.fingerprint,is_test:ctx.is_test===true,session_id:ctx.session_id||null,turn_id:ctx.turn_id||null,turn_status:ctx.turn_status||null,status:ctx.status,started_at:ctx.started_at,submitted_at:ctx.submitted_at||null,accepted_at:ctx.accepted_at||null,completed_at:ctx.completed_at||null,last_checked_at:now,deadline_at:ctx.deadline_at,submission_key:ctx.submission_key||null,baseline_turn_ids:ctx.baseline_turn_ids||[],resume_count:ctx.resume_count||0,result:codexSafe(ctx.result),error:codexSafe(ctx.error),reused_from_task:ctx.reused_from_task||null,w0_reported:previous.w0_reported||notify,notify_w0:notify};
  const rows=[codexRow(ctx.job_key,'agent_task',ctx.status,p,now,ctx.job),codexRow('codex-log:'+ctx.job_key,'agent_log',ctx.status,{...p,instruction:undefined},now)];
  if(ctx.session_id)rows.push(codexRow('codex:session:manager','agent_session',ctx.status==='done'?'idle':['failed','cancelled'].includes(ctx.status)?'failed':'uncertain',{session_id:ctx.session_id,last_task_key:ctx.job_key,last_turn_id:ctx.turn_id||null,last_checked_at:now},now));
  return rows;
}
