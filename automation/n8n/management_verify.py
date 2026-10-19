"""Strict provenance of the Telegram/management repair; no external execution."""
import hashlib,json
NAMES={'W1','W5','W7','W9','My workflow'}
def verify(root,entry,manager_target="My workflow.json"):
 def read(p):return json.loads((root/p).read_text())
 path='revisions/management-20261019/verification.json';assert entry['path']==path
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256'];proof=read(path);assert set(proof['workflows'])==NAMES
 for source,digest in proof['changed_source_sha256'].items():assert hashlib.sha256((root/source).read_bytes()).hexdigest()==digest
 for name,p in proof['workflows'].items():
  before_path='revisions/management-20261019/'+name+'.before.json';after_path=manager_target if name=='My workflow' else name+'.json'
  for path,key in [(before_path,'before_sha256'),(after_path,'after_sha256')]:assert hashlib.sha256((root/path).read_bytes()).hexdigest()==p[key]
  old,new=read(before_path),read(after_path);assert old['id']==new['id']==p['id'] and old['versionId']==p['before_version_id'] and new['versionId']==p['published_version_id']
  assert old['settings']==new['settings'];nodes={n['id']:n for n in new['nodes']};assert len(nodes)==len(new['nodes'])
  for n in old['nodes']:
   a=nodes[n['id']];assert a.get('credentials')==n.get('credentials') and a.get('webhookId')==n.get('webhookId')
   if n['type']!='n8n-nodes-base.code':assert a['parameters']==n['parameters']
  if name=='W9':
   f={n['name']:n for n in new['nodes']};assert new['connections']['Message Telegram']['main'][0]==[{'node':'Gestion – autoriser','type':'main','index':0}]
   assert 'mgAuthorized(update' in f['Gestion – autoriser']['parameters']['jsCode']
   assert 'mgOperator' in f['Commande']['parameters']['jsCode']
   assert f['Gestion – enregistrer']['parameters']['operation']=='update'
   assert {c['keyName'] for c in f['Gestion – enregistrer']['parameters']['filters']['conditions']}=={'task_key','status','last_action'}
   assert 'applied=r.task_key' in f['Gestion – confirmer']['parameters']['jsCode']
   assert 'mgTelegramText(i.json.reply)' in f['Réponse']['parameters']['jsCode']
  elif name=='My workflow':
   s=next(n for n in new['nodes'] if n['name']=='Commande – traiter')['parameters']['jsCode'];assert 'mgOperator' in s and "if(!mgCompletion(t))return reply" in s and "else if(action==='done'){update.status='done'" not in s.split("const text=mgCommand(")[-1]
  elif name=='W1':
   s=next(n for n in new['nodes'] if n['name']=='Claude classification')['parameters']['jsCode'];assert "categorie:'recrutement'" in s
   s=next(n for n in new['nodes'] if n['name']=='Inbox – tâches')['parameters']['jsCode'];assert "'inbound_hr','WARM','Manager','needs_review'" in s
  elif name=='W7':assert any('e?.work_request?.verified===true' in n.get('parameters',{}).get('jsCode','') for n in new['nodes'])
 return proof
