"""Offline verification of the narrowly scoped, already-published Agents integration."""
import hashlib,json

def verify(root,entry):
 def read(path):return json.loads((root/path).read_text())
 path='revisions/agents-20261019/verification.json'
 assert entry['path']==path
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256']
 p=read(path);directory='revisions/agents-20261019/'
 for path,key in [(directory+'My workflow.before.json','before_sha256'),(directory+'My workflow.draft-before.json','draft_before_sha256'),('My workflow.json','after_sha256')]:
  assert hashlib.sha256((root/path).read_bytes()).hexdigest()==p[key]
 old=read(directory+'My workflow.before.json');draft=read(directory+'My workflow.draft-before.json');new=read('My workflow.json')
 assert old['id']==draft['id']==new['id']==p['id']=='cKUyJSLOF69uXGnO'
 assert new['versionId']==p['published_version_id']
 assert old['settings']==draft['settings']==new['settings']
 nodes={n['id']:n for n in new['nodes']};original={n['id']:n for n in draft['nodes']}
 assert len(nodes)==len(new['nodes']) and set(original)<=set(nodes)
 changed=[]
 for ident,n in original.items():
  actual=nodes[ident]
  assert actual.get('credentials')==n.get('credentials') and actual.get('webhookId')==n.get('webhookId')
  if actual!=n:
   changed.append(ident)
   if n['name']=='HTTP Request':
    assert ident=='29958e7d-9b45-4e55-afc3-28b56394a911' and actual['name']=='Codex – envoyer événements'
    assert actual['credentials']['openAiApi']['name']=='OpenAI account 2'
   else:
    assert n['name'] in ['AI Agent','AI Agent — Claude dernier secours']
    assert actual['parameters']['options']['systemMessage'].startswith(n['parameters']['options']['systemMessage'])
    a=json.loads(json.dumps(actual));a['parameters']['options']['systemMessage']=n['parameters']['options']['systemMessage'];assert a==n
 assert sorted(changed)==sorted(p['changed_existing_nodes'])
 assert sorted(set(nodes)-set(original))==sorted(p['added_nodes'])
 # Every existing edge remains; only additive branches/tools are permitted.
 for source,ports in draft['connections'].items():
  for typ,groups in ports.items():
   for i,edges in enumerate(groups):
    assert all(e in new['connections'][source][typ][i] for e in edges)
 assert not any('temporaire' in n['name'] or n['name'].startswith('Codex – test') for n in new['nodes'])
 for n in new['nodes']:
  if n['type']=='n8n-nodes-base.httpRequest' and n['name'].startswith('Codex –'):
   assert 'https://api.openai.com/v1/agents/sessions' in n['parameters']['url']
 for name in ['codex_technical_task','codex_task_status']:
  assert {e['node'] for e in new['connections'][name]['ai_tool'][0]}=={'AI Agent','AI Agent — Claude dernier secours'}
 return p
