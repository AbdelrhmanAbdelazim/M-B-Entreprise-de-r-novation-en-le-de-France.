"""Verify the immutable queue-only direct-social successor; never provider requests."""
import json,hashlib,copy

def verify(root,entry,targets=None):
 path='revisions/direct-social-20261020/verification.json'
 def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
 assert entry['path']==path and entry['sha256']==sha(path)
 proof=json.loads((root/path).read_text());assert set(proof['workflows'])=={'My workflow','AI Continuous Improvement'}
 assert proof['source']['path']=='direct-social.js' and proof['source']['sha256']==sha('direct-social.js');source=(root/'direct-social.js').read_text()
 for name,p in proof['workflows'].items():
  assert p['before']=='revisions/direct-social-20261020/'+name+'.before.json'
  assert p['after']==('My workflow.json' if name=='My workflow' else 'revisions/direct-social-20261020/AI Continuous Improvement.json')
  after=(targets or {}).get(name,p['after'])
  assert sha(p['before'])==p['before_sha256'] and sha(after)==p['after_sha256']
  old=json.loads((root/p['before']).read_text());new=json.loads((root/after).read_text());assert old['id']==new['id']==p['id'] and old['versionId']==p['before_version_id'] and new['versionId']==p['published_version_id'] and new['active']
  assert old['settings']==new['settings'];a={n['name']:n for n in old['nodes']};b={n['name']:n for n in new['nodes']}
  if name=='My workflow':
   assert set(a)==set(b) and old['connections']==new['connections']
   allowed={'Coordination – plan','Growth – diagnostic sûr ?','Growth – contexte isolé'}
   for key,n in a.items():
    if key not in allowed:assert n==b[key]
    else:assert {**b[key],'parameters':n['parameters']}==n
   needle='socialPublishingGate(q,metricoolQueuePlan(q,iso()),iso(),"2026-10-19T19:31:39.404290+00:00").map(jq)'
   repl='socialPublishingGate(q,metricoolQueuePlan(q,iso()).filter(r=>r.type===\'publication\'&&q.some(t=>t.type===\'publication\'&&t.task_key===r.task_key)),iso(),"2026-10-19T19:31:39.404290+00:00").map(jq),directSocialPlan(q,iso(),'+json.dumps(proof['cutover'])+').map(jq)'
   assert needle in a['Coordination – plan']['parameters']['jsCode']
   assert b['Coordination – plan']['parameters']['jsCode']==source+'\n'+a['Coordination – plan']['parameters']['jsCode'].replace(needle,repl)
   assert b['Growth – contexte isolé']['parameters']['jsCode']=="if($('ChatGPT – contexte Manager').first().json.task==='/social-preflight-safe')return [{json:{social_audit:true}}];\n"+a['Growth – contexte isolé']['parameters']['jsCode']
   assert b['Growth – diagnostic sûr ?']['parameters']['conditions']['conditions'][0]['leftValue']=="={{ ['/growth-audit-safe','/growth-ingest-safe','/social-preflight-safe'].includes($('ChatGPT – contexte Manager').first().json.task) }}"
  else:
   assert set(b)-set(a)=={'Social – diagnostic sûr ?','Social – Queue lecture seule','Social – état sans publication'}
   for key,n in a.items():assert n==b[key]
   for key,edges in old['connections'].items():
    if key!='Improvement – diagnostic interne':assert edges==new['connections'][key]
   assert new['connections']['Improvement – diagnostic interne']['main'][0][0]['node']=='Social – diagnostic sûr ?'
   assert new['connections']['Social – diagnostic sûr ?']['main'][1][0]['node']=='CRM – requête interne ?'
   assert b['Social – Queue lecture seule']['parameters']['operation']=='get' and b['Social – Queue lecture seule']['parameters']['dataTableId']['value']=='aqPFAT3TBwLGhlIj' and b['Social – Queue lecture seule']['executeOnce']
   for key in set(b)-set(a):assert not b[key].get('credentials') and b[key]['type'] in {'n8n-nodes-base.code','n8n-nodes-base.if','n8n-nodes-base.dataTable'}
   assert b['Social – état sans publication']['parameters']['jsCode'].startswith((root/'metricool.js').read_text()+'\n'+source)
 return proof
