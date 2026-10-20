"""Verify the exact growth successor and its archived observer; no remote operations."""
import copy,hashlib,json

def verify(root,entry,targets=None):
 path='revisions/growth-20261020/verification.json'
 assert entry['path']==path and hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256']
 proof=json.loads((root/path).read_text());assert set(proof['workflows'])=={'My workflow','W10'}
 def load(p):return json.loads((root/p).read_text())
 def edge(n):return {'node':n,'type':'main','index':0}
 def link(w,name,success,failure=None):w['connections'][name]={'main':[[edge(success)]]+([[edge(failure)]] if failure else [])}
 for name,p in proof['workflows'].items():
  before='revisions/growth-20261020/'+name+'.before.json';after=(targets or {}).get(name,name+'.json')
  assert hashlib.sha256((root/before).read_bytes()).hexdigest()==p['before_sha256']
  assert hashlib.sha256((root/after).read_bytes()).hexdigest()==p['after_sha256']
  old,new=load(before),load(after);assert old['id']==new['id']==p['id'] and old['versionId']==p['before_version_id'] and new['versionId']==p['published_version_id']
  expected=copy.deepcopy(old)
  if name=='W10':
   expected['connections']['Boucle résilience 7 idées']['main'][1]=[edge('Claude : 7 idées')]
   routes=[('Claude : 7 idées','Valider Claude 7 idées','OpenAI 7 idées'),('Valider Claude 7 idées','Boucle résilience 7 idées','OpenAI 7 idées'),('OpenAI 7 idées','Valider OpenAI 7 idées','Gemini 7 idées'),('Valider OpenAI 7 idées','Boucle résilience 7 idées','Gemini 7 idées'),('Gemini 7 idées','Valider Gemini 7 idées',None),('Valider Gemini 7 idées','Boucle résilience 7 idées',None)]
   prompt=next(n for n in expected['nodes'] if n['name']=='Préparer 7 idées')['parameters']['assignments']['assignments'][0];assert '(avis Google 5/5)' in prompt['value'];prompt['value']=prompt['value'].replace(' (avis Google 5/5)','')
   content_source=proof['content_source'];assert content_source['path']=='revisions/growth-20261020/content-source.js';source=(root/content_source['path']).read_text();assert hashlib.sha256(source.encode()).hexdigest()==content_source['sha256']
   calendar=next(n for n in expected['nodes'] if n['name']=='Contenu – calendrier');calendar['parameters']['jsCode']=source+'\nreturn growthAdaptContentRows((()=>{\n'+calendar['parameters']['jsCode']+'\n})());\n'
  else:
   added=[n for n in new['nodes'] if n['id'] not in {n['id'] for n in old['nodes']}];assert [n['name'] for n in added]==['Growth – diagnostic sûr ?','Growth – contexte isolé','Growth – audit sans transport']
   assert all(not n.get('credentials') and not n.get('disabled') for n in added)
   assert added[0]['parameters']['conditions']['conditions'][0]['leftValue']=="={{ $('ChatGPT – contexte Manager').first().json.task === '/growth-audit-safe' }}"
   assert added[1]['parameters']['jsCode']=="return [{json:{audit_safe:true,request_id:$('ChatGPT – contexte Manager').first().json.request_id}}];"
   assert added[2]['parameters']['workflowId']['value']==proof['new_workflow']['id'] and added[2]['parameters']['options']['waitForSubWorkflow'] is True
   expected['nodes']+=copy.deepcopy(added)
   expected['connections']['ChatGPT – réserver Manager']={'main':[[edge('Growth – diagnostic sûr ?')]]}
   expected['connections']['Growth – diagnostic sûr ?']={'main':[[edge('Growth – contexte isolé')],[edge('ChatGPT – message Manager')]]}
   link(expected,'Growth – contexte isolé','Growth – audit sans transport');link(expected,'Growth – audit sans transport','ChatGPT – résultat Manager')
   expected['connections']['Boucle résilience Revue']['main'][1]=[edge('OpenAI Revue')]
   routes=[('OpenAI Revue','Valider OpenAI Revue','Gemini Revue'),('Valider OpenAI Revue','Boucle résilience Revue','Gemini Revue'),('Gemini Revue','Valider Gemini Revue','Claude Revue'),('Valider Gemini Revue','Boucle résilience Revue','Claude Revue'),('Claude Revue','Valider Claude Revue',None),('Valider Claude Revue','Boucle résilience Revue',None)]
  for node,success,failure in routes:
   link(expected,node,success,failure);next(n for n in expected['nodes'] if n['name']==node)['onError']='continueErrorOutput' if failure else 'stopWorkflow'
  for key in ['id','name','nodes','connections','settings']:assert expected[key]==new[key],(name,key)
 p=proof['new_workflow'];assert p['snapshot']=='revisions/growth-20261020/AI Continuous Improvement.json';assert p['source_path']=='revisions/growth-20261020/improvement-source.js'
 assert hashlib.sha256((root/p['snapshot']).read_bytes()).hexdigest()==p['sha256']
 assert hashlib.sha256((root/p['source_path']).read_bytes()).hexdigest()==proof['source_sha256']==p['source_sha256']
 new=load(p['snapshot']);assert new['id']==p['id'] and new['versionId']==p['published_version_id'] and new['active']
 assert new['settings']['errorWorkflow']=='4O2ZR1JpDOgJZOLw' and new['settings']['timezone']=='Europe/Paris'
 assert len([n for n in new['nodes'] if n['type'].endswith('.emailSend')])==1
 for node in new['nodes']:
  if node['type'].endswith('.scheduleTrigger'):assert not node.get('disabled') and node['parameters']['rule']['interval']==[{'field':'cronExpression','expression':'15 18 * * *'}]
  if node['type'].endswith('.dataTable') and node['parameters'].get('operation')=='get':assert node.get('executeOnce') is True
  if node['type'].endswith('.httpRequest'):assert node['parameters']['url'].startswith(('https://api.openai.com/','https://api.anthropic.com/','https://generativelanguage.googleapis.com/')) and node.get('retryOnFail') is False
 return proof
