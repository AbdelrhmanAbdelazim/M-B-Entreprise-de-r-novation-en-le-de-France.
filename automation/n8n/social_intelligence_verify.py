"""Immutable five-workflow social-intelligence successor; offline, no network/delivery."""
import hashlib,json

def verify(root,entry):
 path='revisions/social-intelligence-20261020/verification.json'
 def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
 assert entry['path']==path and entry['sha256']==sha(path);proof=json.loads((root/path).read_text())
 assert set(proof['workflows'])=={'My workflow','ChatGPT ingress','W7','W10','AI Continuous Improvement'}
 sources={}
 for name,p in proof['sources'].items():
  assert p['path'].startswith('revisions/social-intelligence-20261020/') and p['sha256']==sha(p['path']);sources[name]=(root/p['path']).read_text()
 assert set(sources)=={'integration-diagnostics','social-intelligence','workspace-embedded'}
 # The deployed Manager includes an earlier full pure-module snapshot. Its used workspace policy is exact.
 for name in ['siJSON','siWorkspacePlan']:
  def function(text,name):
   start=text.index('function '+name+'(');end=text.find('\nfunction ',start+1);return text[start:end if end!=-1 else len(text)].rstrip()
  assert function(sources['workspace-embedded'],name)==function(sources['social-intelligence'],name)
 docs={}
 allowed={'My workflow':{'Growth – diagnostic sûr ?','Growth – contexte isolé','Coordination – plan'},'ChatGPT ingress':{'Meta – identité lecture','Meta – identité sûre','Runway – résultat sûr','Provider – contexte sans secret','Provider – résultat public'},'W7':{'Requêtes','URLs','Emails','Final','Radar – tâches prospects','Qualification – backlog'},'W10':{'Contenu – calendrier'},'AI Continuous Improvement':{'Contexte sûr','Avant SMTP – garde','Mesures factuelles','Rapport factuel'}}
 changed_edges={'My workflow':set(),'ChatGPT ingress':{'Runway – résultat sûr'},'W7':{'Radar – Queue'},'W10':set(),'AI Continuous Improvement':{'Improvement – diagnostic interne','Contexte sûr','Mesures factuelles'}}
 for name,p in proof['workflows'].items():
  assert p['before']=='revisions/social-intelligence-20261020/'+name+'.before.json'
  assert p['after']==('revisions/social-intelligence-20261020/AI Continuous Improvement.json' if name=='AI Continuous Improvement' else name+'.json')
  assert sha(p['before'])==p['before_sha256'] and sha(p['after'])==p['after_sha256']
  a=json.loads((root/p['before']).read_text());b=json.loads((root/p['after']).read_text());docs[name]=(a,b)
  assert a['id']==b['id']==p['id'] and a['versionId']==p['before_version_id'] and b['versionId']==p['published_version_id'] and b['active']
  assert a['settings']==b['settings'] and b['settings']['errorWorkflow']=='4O2ZR1JpDOgJZOLw'
  old={n['name']:n for n in a['nodes']};new={n['name']:n for n in b['nodes']};assert set(old)<=set(new)
  for key,node in old.items():
   if key not in allowed[name]:assert node==new[key],(name,key)
   else:assert {**new[key],'parameters':node['parameters']}==node
  for key,edges in a['connections'].items():
   if key not in changed_edges[name]:assert edges==b['connections'][key],(name,key)
  if name=='My workflow':
   assert set(old)==set(new)
   code=old['Coordination – plan']['parameters']['jsCode'].replace('return out.concat(','return out.concat(siWorkspacePlan(q,iso()).map(jq),')
   assert new['Coordination – plan']['parameters']['jsCode']==sources['workspace-embedded']+'\n'+code
   assert new['Growth – contexte isolé']['parameters']['jsCode']=="if($('ChatGPT – contexte Manager').first().json.task==='/social-intelligence-safe')return [{json:{social_intelligence_readonly:true}}];\n"+old['Growth – contexte isolé']['parameters']['jsCode']
  elif name=='ChatGPT ingress':
   assert len(set(new)-set(old))==6
   assert all(b['settings'][k]=='none' for k in ['saveDataErrorExecution','saveDataSuccessExecution'])
   assert b['settings']['saveManualExecutions'] is False and b['settings']['saveExecutionProgress'] is False
   assert new['Telegram – chat lecture seule']['parameters']['operation']=='get' and new['Telegram – chat lecture seule']['parameters']['resource']=='chat'
   for key in ['Creatomate – projet lecture officielle','BOAMP – métadonnées officielles']:assert new[key]['parameters']['method']=='GET' and not new[key]['parameters'].get('sendBody')
   assert new['Creatomate – projet lecture officielle']['parameters']['url']=='https://api.creatomate.com/v1/projects/data'
   assert b['connections']['Runway – résultat sûr']['main'][0][0]['node']=='Creatomate – projet lecture officielle'
   assert new['Provider – résultat public']['parameters']['jsCode'].endswith("return [{json:{output:JSON.stringify(siProviderFinal($json))}}];")
  elif name=='W7':
   assert len(set(new)-set(old))==4
   assert b['connections']['Radar – Queue']['main'][0][:-1]==a['connections']['Radar – Queue']['main'][0]
   assert new['Requêtes']['parameters']['jsCode']==sources['social-intelligence']+'\nreturn siRadarQueries((()=>{\n'+old['Requêtes']['parameters']['jsCode']+'\n})());\n'
   assert old['Qualification – backlog']['parameters']['jsCode'] in new['Qualification – backlog']['parameters']['jsCode']
   expected=sources['social-intelligence']+'\n'+old['Radar – tâches prospects']['parameters']['jsCode'].replace('const out=result.rows.map(jq);','const out=siEnrichQualification(result.rows,iso()).map(jq);')
   assert new['Radar – tâches prospects']['parameters']['jsCode']==expected
   http=new['BOAMP – opportunités officielles'];assert http['executeOnce'] and http['parameters']['method']=='GET' and http['parameters']['url']=='https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records'
   assert 'type_marche="TRAVAUX"' in next(x['value'] for x in http['parameters']['queryParameters']['parameters'] if x['name']=='where')
   assert new['BOAMP – sauvegarder revue']['parameters']['dataTableId']['value']=='aqPFAT3TBwLGhlIj'
   assert new['BOAMP – sauvegarder revue']['parameters']['operation']=='upsert'
   alert=new['BOAMP – alerte HOT réservée']['parameters']['jsCode'];assert "$execution.mode!=='production'" in alert and ".isExecuted!==true" in alert
  elif name=='W10':
   assert set(old)==set(new) and a['connections']==b['connections'];s=old['Contenu – calendrier']['parameters']['jsCode'];pos=s.rfind('})(),')+len('})(),');_,end=json.JSONDecoder().raw_decode(s[pos:]);expected=s[:pos]+json.dumps(proof['provider_evidence'],ensure_ascii=False,separators=(',',':'))+s[pos+end:];assert new['Contenu – calendrier']['parameters']['jsCode']==expected
  else:
   assert len(set(new)-set(old))==13
   guard=new['Contexte sûr']['parameters']['jsCode'];assert "$execution.mode==='production'" in guard and ".isExecuted===true" in guard
   assert "$execution.mode!=='production'" in new['Avant SMTP – garde']['parameters']['jsCode'] and ".isExecuted===true" in new['Avant SMTP – garde']['parameters']['jsCode']
   assert b['connections']['Mesures factuelles']['main'][0][0]['node']=='Improvement – diagnostic sans modèles ?'
   assert b['connections']['Improvement – diagnostic sans modèles ?']['main'][0][0]['node']=='Improvement – audit zéro modèle'
   assert 'Improvement – audit zéro modèle' not in b['connections']
   assert b['connections']['Improvement – diagnostic sans modèles ?']['main'][1]==a['connections']['Mesures factuelles']['main'][0]
   assert new['Provider – lecture journalière']['parameters']['workflowId']['value']==proof['workflows']['ChatGPT ingress']['id']
   for key in set(new)-set(old):assert not new[key].get('credentials')
   assert new['Intelligence – résultat sans transport']['parameters']['jsCode'].startswith(sources['social-intelligence'])
 rt=proof['runtime'];assert rt['native_zero_model_test']['status']=='verified_read_only_audit' and rt['native_zero_model_test']['dry_run'] is True and rt['native_zero_model_test']['model_calls']==[] and rt['native_zero_model_test']['transport_executed'] is False
 assert rt['boamp_actual_review_rows']==[196,197,198,199,200] and rt['customer_sends']==rt['renders']==rt['public_posts']==0
 act=json.loads((root/'activation.json').read_text());assert act['additional_improvement']['version_id']==proof['workflows']['AI Continuous Improvement']['published_version_id']
 return proof
