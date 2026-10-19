import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const root=new URL('../',import.meta.url), policy=fs.readFileSync(new URL('qualification.js',root),'utf8');
const qualify=vm.runInNewContext(policy+';qualifyProspects');
const now='2026-10-19T09:00:00Z';
const lead={id:1001,email:'contact@partner.invalid',site:'partner.invalid',entreprise:'Synthetic partner',statut:'nouveau',type:'architecte',departement:'75'};
const evidence={email:lead.email,site:lead.site,garder:true,email_observed:true,text:'Architecte intérieur Paris 75011 rénovation appartement suivi de chantier',observed_at:'2026-10-16T12:30:00Z',source_url:'https://partner.invalid/'};
const call=({leads=[lead],blacklist=[],queue=[],sources=[evidence],time=now}={})=>qualify(leads,blacklist,queue,sources,time);
test('clear local renovation partnership is HOT and approved; no open tender is invented',()=>{const r=call().rows[0];assert.equal(r.status,'approved');assert.equal(r.priority,'HOT');assert.equal(JSON.parse(r.payload).opportunity_type,'b2b_partnership');});
test('uncertain evidence stays for human review',()=>{for(const changed of [{text:'Architecte Bordeaux rénovation'},{email_observed:false},{observed_at:'2026-09-01T00:00:00Z'},{garder:undefined}])assert.equal(call({sources:[{...evidence,...changed}]}).rows[0].status,'needs_review');});
test('free mailbox without professional domain match is held for human verification',()=>{const l={...lead,email:'synthetic@gmail.com'};assert.equal(call({leads:[l],sources:[{...evidence,email:l.email}]}).rows[0].status,'needs_review');});
test('irrelevant competitor, invalid contact, blacklist, duplicate and uncertain send are never approved',()=>{
 assert.equal(call({leads:[{...lead,type:'entreprise_generale'}]}).rows[0].status,'held');
 assert.equal(call({leads:[{...lead,email:'bad'}]}).rows[0].status,'held');
 assert.equal(call({blacklist:[{email:'stop@partner.invalid'}]}).rows[0].status,'held');
 assert.ok(call({leads:[lead,{...lead,id:1002}]}).rows.every(r=>r.status==='held'));
 assert.equal(call({queue:[{type:'action',task_key:'send:outreach:old.invalid',status:'uncertain',payload:JSON.stringify({lead:{email:lead.email}})}]}).rows[0].status,'held');
});
test('human decisions and conflicting prospect records remain authoritative',()=>{for(const status of ['approved','rejected','deferred','done'])assert.equal(call({queue:[{task_key:'prospect:partner.invalid',source:'W7',status,priority:'WARM',payload:'{}'}]}).rows.length,0);const old=call().rows[0];assert.equal(call({queue:[{...old,next_action:'Validé par le directeur'}]}).rows.length,0);assert.equal(call({queue:[old,{...old,status:'rejected'}]}).rows.length,0);});
test('backfill is idempotent; expiration revokes policy approval; lead 79 cannot be approved',()=>{const old=call().rows[0];assert.equal(call({queue:[old],sources:[]}).rows.length,0);assert.equal(call({queue:[old],sources:[],time:'2026-11-01T09:00:00Z'}).rows[0].status,'needs_review');assert.equal(call({leads:[{...lead,id:79}]}).rows[0].status,'held');});
const directory=process.env.N8N_ACTIVATION_FIXTURE_DIR;
if(directory){
 const docs=Object.fromEntries(['W3','W4','W7'].map(n=>[n,JSON.parse(fs.readFileSync(directory+'/'+n+'.json'))]));
 function gate(w,l,q,time=now){const code=docs[w].nodes.find(n=>n.name==='Garde commerciale').parameters.jsCode;class Clock extends Date{constructor(...args){super(...(args.length?args:[time]));}static now(){return new Date(time).getTime();}}
 const rows={'Un par un':[l],'Avant envoi – Leads':[l],'Avant envoi – Blacklist':[]};const item=json=>({json});
 return vm.runInNewContext('(()=>{'+code+'})()',{Date:Clock,$runIndex:0,$input:{all:()=>q.map(item)},$:n=>({item:item(rows[n][0]),all:()=>rows[n].map(item)})})[0].json.allowed;}
 test('qualification → W3 → one W4 follow-up, then stop; no transports',()=>{const approval=call().rows[0];assert.equal(gate('W3',lead,[approval]),true);const done={task_key:'send:outreach:partner.invalid',type:'action',status:'done',payload:JSON.stringify({kind:'outreach',lead})};assert.equal(gate('W3',lead,[approval,done]),false);const sent={...lead,statut:'envoye',date_envoi:'2026-10-19'};assert.equal(gate('W4',sent,[approval,done],'2026-10-26T09:00:00Z'),true);assert.equal(gate('W4',{...sent,date_reponse:'2026-10-22'},[approval,done],'2026-10-26T09:00:00Z'),false);assert.equal(gate('W4',sent,[approval,done,{...done,task_key:'send:followup:partner.invalid'}],'2026-10-26T09:00:00Z'),false);});
 test('both live candidate gates hard-block 79 and expired or changed-recipient approvals',()=>{const approval=call().rows[0];for(const w of ['W3','W4']){const l={...lead,...(w==='W4'?{statut:'envoye',date_envoi:'2026-10-01'}:{})};assert.equal(gate(w,{...l,id:79},[approval]),false);assert.equal(gate(w,{...l,email:'other@partner.invalid'},[approval]),false);assert.equal(gate(w,l,[approval],'2026-11-02T09:00:00Z'),false);}});
 test('explicit human qualification and approval can resolve uncertain/stale policy cases',()=>{const approval=call().rows[0], payload=JSON.parse(approval.payload);payload.qualified_by='operator_chat';payload.qualification_expires_at=null;const manual={...approval,payload:JSON.stringify(payload)};assert.equal(gate('W3',lead,[manual]),true);assert.equal(gate('W3',{...lead,id:79},[manual]),false);});
 test('new W7 discovery carries verified source evidence through Final into automatic approval',()=>{
  const w=docs.W7,item=json=>({json});const source={...evidence,host:lead.site,url:evidence.source_url,entreprise_titre:lead.entreprise,qualification_text:evidence.text,type:lead.type,departement:'75'};
  const inputs={Emails:[source],Leads:[],Blacklist:[],Requêtes:[{test:false,max:10}],'Radar – Queue':[]};
  const run=(name,input=[])=>vm.runInNewContext('(()=>{'+w.nodes.find(n=>n.name===name).parameters.jsCode+'})()',{Date,$input:{all:()=>input.map(item)},$:n=>({all:()=>inputs[n].map(item),first:()=>item(inputs[n][0])})});
  const result=run('Final',[{text:JSON.stringify({garder:true,type:'architecte',entreprise:'Synthetic partner'})}]);inputs.Final=[result[0].json];
  assert.equal(inputs.Final[0].qualification_evidence[0].email_observed,true);
  const approved=run('Radar – tâches prospects').filter(i=>i.json.type==='prospect');assert.equal(approved.length,1);assert.equal(approved[0].json.status,'approved');
  inputs.Final[0].test=true;assert.equal(run('Radar – tâches prospects').length,0);
 });
 test('persistent W7 backfill is reachable before research and uses identical reviewed policy',()=>{const w=docs.W7;assert.ok(w.connections['Radar – Queue'].main[0].some(x=>x.node==='Qualification – backlog'));for(const name of ['Qualification – backlog','Radar – tâches prospects'])assert.ok(w.nodes.find(n=>n.name===name).parameters.jsCode.includes(policy));});
}
