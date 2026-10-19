"""Strict offline provenance and safety checks for the published ingress successor."""
import hashlib,json

def verify(root,entry):
 def read(path):return json.loads((root/path).read_text())
 path='revisions/ingress-20261019/verification.json';assert entry['path']==path
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256']
 p=read(path)
 for path,key in [('revisions/ingress-20261019/My workflow.before.json','before_sha256'),('revisions/ingress-20261019/My workflow.draft-before.json','draft_before_sha256'),('My workflow.json','after_sha256'),('ChatGPT ingress.json','ingress_sha256')]:
  assert hashlib.sha256((root/path).read_bytes()).hexdigest()==p[key]
 old=read('revisions/ingress-20261019/My workflow.before.json');new=read('My workflow.json');front=read('ChatGPT ingress.json');nodes={n['id']:n for n in new['nodes']}
 assert old['id']==new['id']==p['id']=='cKUyJSLOF69uXGnO' and new['versionId']==p['published_version_id']
 assert old['settings']==new['settings']
 for n in old['nodes']:
  a=nodes[n['id']];assert a.get('credentials')==n.get('credentials') and a.get('webhookId')==n.get('webhookId')
  if n['type']!='n8n-nodes-base.code':assert a['parameters']==n['parameters']
  elif a['parameters']!=n['parameters']:assert n['name'].startswith('Codex –') or n['name']=='Restaurer message original'
 for source,ports in old['connections'].items():
  for typ,groups in ports.items():
   for index,edges in enumerate(groups):assert all(e in new['connections'][source][typ][index] for e in edges)
 assert front['id']==p['ingress_id'] and front['versionId']==p['ingress_published_version_id']
 assert front['settings']['saveDataSuccessExecution']==front['settings']['saveDataErrorExecution']=='none'
 assert front['settings']['saveManualExecutions'] is False and front['settings']['saveExecutionProgress'] is False
 assert front['settings']['errorWorkflow']==new['settings']['errorWorkflow']
 f={n['name']:n for n in front['nodes']};auth=f['ChatGPT – vérifier accès']
 assert auth['parameters']['method']=='GET' and auth['parameters']['url'].endswith('/api/v1/workflows/cKUyJSLOF69uXGnO')
 assert auth['parameters']['headerParameters']['parameters']==[{'name':'X-N8N-API-KEY','value':'={{ $json.auth_header }}'}]
 assert 'h.statusCode===200' in f['ChatGPT – accès validé']['parameters']['jsCode']
 assert 'auth_header,...safe' in f['ChatGPT – accès validé']['parameters']['jsCode']
 assert f['ChatGPT – réserver clé']['parameters']['columns']['value']=={'task_key':"={{ $('ChatGPT – accès validé').first().json.task_key }}"}
 assert any(c['keyName']=='payload' and c['condition']=='isEmpty' for c in f['ChatGPT – accepter une seule fois']['parameters']['filters']['conditions'])
 # No path from a webhook to any Queue/Manager operation can bypass authentication verification.
 for start in [n['name'] for n in front['nodes'] if n['type']=='n8n-nodes-base.webhook']:
  seen=set();todo=[start]
  while todo:
   name=todo.pop()
   if name in seen or name==auth['name']:continue
   seen.add(name);assert f[name]['type'] not in ['n8n-nodes-base.dataTable','n8n-nodes-base.executeWorkflow']
   for groups in front['connections'].get(name,{}).values():
    for edges in groups:todo.extend(e['node'] for e in edges)
 assert not any('temporaire' in n['name'] for n in front['nodes']+new['nodes'])
 assert not any('is_test:true' in json.dumps(n['parameters']) for n in front['nodes'])
 return p
