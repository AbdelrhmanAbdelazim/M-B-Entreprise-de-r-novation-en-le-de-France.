"""Verify native read-only credential probes and transport-free future video guards."""
import hashlib,json

def verify(root,entry):
 path='revisions/provider-readonly-20261020/verification.json'
 def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
 assert entry['path']==path and entry['sha256']==sha(path)
 proof=json.loads((root/path).read_text());assert set(proof['workflows'])=={'My workflow','ChatGPT ingress','W10'}
 sources={}
 for name,p in proof['sources'].items():
  assert p['path']=='revisions/provider-readonly-20261020/'+name+'-source.js' and p['sha256']==sha(p['path']);sources[name]=(root/p['path']).read_text()
 assert set(sources)=={'provider-readonly','video-provider-gates'}
 assert sources['provider-readonly']==(root/'provider-readonly.js').read_text()
 docs={}
 for name,p in proof['workflows'].items():
  assert p['before']=='revisions/provider-readonly-20261020/'+name+'.before.json' and p['after']==name+'.json'
  assert sha(p['before'])==p['before_sha256'] and sha(p['after'])==p['after_sha256']
  a=json.loads((root/p['before']).read_text());b=json.loads((root/p['after']).read_text());docs[name]=(a,b)
  assert a['id']==b['id']==p['id'] and a['versionId']==p['before_version_id'] and b['versionId']==p['published_version_id'] and b['active']
  assert a['settings']==b['settings'] and b['settings']['errorWorkflow']=='4O2ZR1JpDOgJZOLw'
  old={n['name']:n for n in a['nodes']};new={n['name']:n for n in b['nodes']}
  assert set(old)<=set(new)
  allowed={'My workflow':{'Growth – diagnostic sûr ?','Growth – contexte isolé'},'ChatGPT ingress':set(),'W10':{'Contenu – calendrier'}}[name]
  for key,node in old.items():
   if key not in allowed:assert node==new[key],(name,key)
   else:assert {**new[key],'parameters':node['parameters']}==node
  for key,edges in a['connections'].items():
   if name=='My workflow' and key=='Growth – contexte isolé':continue
   assert edges==b['connections'][key],(name,key)
  if name=='W10':
   assert set(old)==set(new) and a['connections']==b['connections']
   evidence=json.dumps(proof['provider_evidence'],ensure_ascii=False,separators=(',',':'))
   assert new['Contenu – calendrier']['parameters']['jsCode']==sources['video-provider-gates']+'\nreturn mbVideoProviderRows((()=>{\n'+old['Contenu – calendrier']['parameters']['jsCode']+'\n})(),'+evidence+');\n'
  elif name=='ChatGPT ingress':
   assert all(b['settings'][k] is False for k in ['saveExecutionProgress','saveManualExecutions'])
   assert all(b['settings'][k]=='none' for k in ['saveDataErrorExecution','saveDataSuccessExecution'])
   added=set(new)-set(old);assert len(added)==26
   http=[new[k] for k in added if new[k]['type']=='n8n-nodes-base.httpRequest'];assert len(http)==8
   for n in http:
    p=n['parameters'];assert p['method']=='GET' and not p.get('sendBody') and not p.get('jsonBody')
    assert p['authentication']=='genericCredentialType' and p['genericAuthType'] in {'oAuth2Api','httpHeaderAuth'}
    assert p['options']['redirect']['redirect']['followRedirects'] is False and p['options']['timeout']==8000
    assert p['options']['response']['response']=={'fullResponse':True,'neverError':True,'responseFormat':'json'}
    assert n['onError']=='continueRegularOutput'
    assert set(n['credentials'])=={p['genericAuthType']}
    assert all(v['id'].startswith('__EXISTING_') for v in n['credentials'].values())
   assert set(new[k]['type'] for k in added)<={'n8n-nodes-base.httpRequest','n8n-nodes-base.executeWorkflowTrigger','n8n-nodes-base.code','n8n-nodes-base.if','n8n-nodes-base.dataTable'}
   assert new['Provider – Queue sûre']['parameters']['operation']=='get'
   assert new['Provider – Queue sûre']['parameters']['dataTableId']['value']=='aqPFAT3TBwLGhlIj'
   assert new['Provider – résultat public']['parameters']['jsCode']==sources['provider-readonly']+'\nreturn [{json:{output:JSON.stringify(pvFinal($json))}}];'
   assert new['Runway – organisation lecture']['parameters']['url']=='https://api.dev.runwayml.com/v1/organization'
   assert new['Creatomate – rendu lecture']['parameters']['url']=="={{ 'https://api.creatomate.com/v1/renders/'+$json.creatomate.render_id }}"
  else:
   assert set(new)-set(old)=={'Provider – connexion demandée ?','Provider – lecture protégée'}
   assert new['Growth – contexte isolé']['parameters']['jsCode']=="if($('ChatGPT – contexte Manager').first().json.task==='/provider-connections-readonly')return [{json:{provider_readonly:true,source:'mb-manager-readonly'}}];\n"+old['Growth – contexte isolé']['parameters']['jsCode']
   assert new['Provider – lecture protégée']['parameters']['workflowId']['value']==proof['workflows']['ChatGPT ingress']['id']
   assert b['connections']['Provider – connexion demandée ?']['main'][1][0]['node']=='Growth – audit sans transport'
 assert proof['runtime']['status']=='success' and proof['runtime']['generation_calls']==proof['runtime']['publish_calls']==0
 assert proof['provider_evidence']['rendering_enabled'] is False and proof['provider_evidence']['publishing_enabled'] is False
 assert 'user_identity' not in proof['provider_evidence']['meta']
 return proof
