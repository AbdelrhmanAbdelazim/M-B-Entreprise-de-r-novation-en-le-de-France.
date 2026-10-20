// Pure public-boundary logic. No credentials or HTTP transports are stored here.
function ingressHash(s){let a=2166136261,b=5381;for(const c of String(s)){a=Math.imul(a^c.charCodeAt(0),16777619);b=Math.imul(b,33)^c.charCodeAt(0);}return(a>>>0).toString(16).padStart(8,'0')+(b>>>0).toString(16).padStart(8,'0');}
function ingressError(code,error){return {code,response:{error}};}
function ingressParse(raw,mode){
 const h=raw.headers||{},b=mode==='status'?raw.query:raw.body;
 if(![h['x-n8n-api-key'],h['x-mb-mcp-key']].some(v=>typeof v==='string'&&v.trim()))return ingressError(401,'authentication_required');
 if(!b||typeof b!=='object'||Array.isArray(b))return ingressError(400,'json_object_required');
 const input={mode};
 if(mode==='command'){
  if(!String(h['content-type']||'').toLowerCase().startsWith('application/json'))return ingressError(415,'application_json_required');
  if(Object.keys(b).some(k=>!['task','source','request_id','route'].includes(k)))return ingressError(400,'unknown_request_field');
  if(b.source!=='chatgpt'||typeof b.task!=='string'||!b.task.trim()||b.task.length>12000)return ingressError(400,'invalid_task_or_source');
  input.task=b.task.trim();
  if(/\b(?:sk-(?:proj-|ant-)?[a-zA-Z0-9_-]{12,}|Bearer\s+\S+|(?:api[_-]?key|password|access_token)\s*[:=]\s*[^\s,;}]+)/i.test(input.task))return ingressError(400,'secret_bearing_task_rejected');
  if(b.route!==undefined&&!['technical','manager'].includes(b.route))return ingressError(400,'invalid_route');
  input.route=b.route||(/\b(codex|agent|workflow|w(?:[0-9]|10)|code|website|api|n8n|technical|debug|fix|review|reply only)\b|تعديل|راجع الموقع|برمج|تقني|إصلاح/i.test(input.task)?'technical':'manager');
  if(/\b(?:ads?|advertising|budget|campaign)\b|إعلان|ميزانية/i.test(input.task))input.route='manager';
  input.source='chatgpt';
 }
 const supplied=b.request_id??h['idempotency-key'];
 if(b.request_id&&h['idempotency-key']&&b.request_id!==h['idempotency-key'])return ingressError(400,'conflicting_idempotency_keys');
 const key=supplied??(mode==='command'?(h['x-mb-mcp-key']?'mcp-auto-':'auto-')+ingressHash('chatgpt|'+input.route+'|'+input.task):'');
 if(typeof key!=='string'||! /^[A-Za-z0-9][A-Za-z0-9._:-]{7,119}$/.test(key))return ingressError(400,'invalid_request_id');
 return {...input,request_id:key,task_key:'chatgpt:'+key};
}
function ingressPayload(row){try{return JSON.parse(row?.payload||'{}');}catch{return {};}}
function ingressView(row,request){
 const p=ingressPayload(row);
 if(!row?.type)return {code:404,response:{request_id:request.request_id,error:'request_not_found'}};
 if(request.task&&(p.instruction!==request.task||p.route!==request.route))return {code:409,response:{request_id:request.request_id,error:'request_id_already_bound_to_different_command'}};
 const done=row.status==='done'&&!!p.result;
 return {code:done?200:202,response:{request_id:request.request_id,codex_task_id:row.type==='agent_task'?row.task_key:null,task_id:row.task_key,status:row.status,result:done?p.result:null,error:p.error||null,ingress_execution_id:p.ingress_execution_id||null,manager_execution_id:p.manager_execution_id||null,status_url:'/webhook/mb-chatgpt/v1/status?request_id='+encodeURIComponent(request.request_id)}};
}
function ingressInitial(request,row,now,executionId){
 const technical=request.route==='technical';
 return {task_key:request.task_key,type:technical?'agent_task':'manager_request',priority:'WARM',source:'chatgpt',owner:technical?'Codex':'Manager',status:'ready',created_at:now,last_action:now,next_action:'Authenticated ChatGPT request accepted; Manager dispatch pending',due_at:now,payload:JSON.stringify({request_id:request.request_id,instruction:request.task,route:request.route,requested_by:'ChatGPT via Manager',scope:'existing_permissions_only_no_test_delivery',ingress_execution_id:String(executionId)})};
}
function ingressManagerContext(row){
 const p=ingressPayload(row),fromQueue=row.type==='manager_request';
 const r={request_id:row.request_id||p.request_id,task_key:row.task_key,task:fromQueue?p.instruction:row.task,route:fromQueue?p.route:row.route,source:row.source};
 if(r.source!=='chatgpt'||r.route!=='manager'||typeof r.task!=='string'||!r.task.trim()||r.task_key!=='chatgpt:'+r.request_id)throw new Error('INVALID_MANAGER_REQUEST_CONTEXT');
 return r;
}
function ingressManagerPending(queue){return queue.filter(r=>r.type==='manager_request'&&r.source==='chatgpt'&&r.status==='ready').sort((a,b)=>String(a.created_at).localeCompare(String(b.created_at))).slice(0,1);}

function ingressBridgeAuthorize(request,actualHash,expectedHash){
 const a=String(actualHash||'').toLowerCase(),b=String(expectedHash||'').toLowerCase();let diff=a.length^b.length;
 for(let i=0;i<64;i++)diff|=(a.charCodeAt(i)||0)^(b.charCodeAt(i)||0);
 if(diff!==0||!/^[0-9a-f]{64}$/.test(a))return ingressError(401,'authentication_failed');
 if(!String(request.request_id||'').startsWith('mcp-'))return ingressError(403,'mcp_request_namespace_required');
 if(request.mode==='command'&&request.route!=='technical')return ingressError(403,'mcp_key_technical_scope_only');
 return {limited_bridge_authenticated:true};
}
