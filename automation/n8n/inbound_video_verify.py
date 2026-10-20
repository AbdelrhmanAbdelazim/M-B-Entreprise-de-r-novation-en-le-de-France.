"""Verify immutable inbound/video successor without any remote operations."""
import hashlib,json

def verify(root,entry):
 path='revisions/inbound-video-20261020/verification.json'
 assert entry['path']==path
 def digest(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
 assert digest(path)==entry['sha256'];proof=json.loads((root/path).read_text())
 assert set(proof['workflows'])=={'W2','My workflow','W10','AI Continuous Improvement'}
 sources={}
 for name,p in proof['sources'].items():
  assert p['path']=='revisions/inbound-video-20261020/'+name+'-source.js' and digest(p['path'])==p['sha256'];sources[name]=(root/p['path']).read_text()
 assert set(sources)=={'inbound','video'}
 for name,p in proof['workflows'].items():
  assert p['before']=='revisions/inbound-video-20261020/'+name+'.before.json'
  assert p['after']==('revisions/inbound-video-20261020/AI Continuous Improvement.json' if name=='AI Continuous Improvement' else name+'.json')
  assert digest(p['before'])==p['before_sha256'] and digest(p['after'])==p['after_sha256']
  old=json.loads((root/p['before']).read_text());new=json.loads((root/p['after']).read_text())
  assert old['id']==new['id']==p['id'] and old['versionId']==p['before_version_id'] and new['versionId']==p['published_version_id']
  assert new['active'] and old['settings']==new['settings'];a={n['name']:n for n in old['nodes']};b={n['name']:n for n in new['nodes']};assert set(a)<=set(b)
  allowed={'W2':{'Site – tâche commerciale'},'My workflow':{'Growth – diagnostic sûr ?','Growth – contexte isolé'},'W10':{'Contenu – calendrier'},'AI Continuous Improvement':set()}[name]
  for key,node in a.items():
   assert node.get('credentials')==b[key].get('credentials') and node['id']==b[key]['id']
   if key not in allowed:assert node==b[key],(name,key)
  if name=='W10':
   assert set(a)==set(b) and old['connections']==new['connections']
   assert b['Contenu – calendrier']['parameters']['jsCode']==sources['video']+'\nreturn mbVideoRows((()=>{\n'+a['Contenu – calendrier']['parameters']['jsCode']+'\n})());\n'
  if name=='W2':
   assert set(b)-set(a)=={'CRM – transmettre demande','CRM – lier sans envoi'}
   assert b['Site – tâche commerciale']['parameters']['jsCode']==a['Site – tâche commerciale']['parameters']['jsCode'].replace('{client_id:$json.id,email:c.email','{client_id:$json.id,client_date:c.date,nom:c.nom,original_source:c.source,email:c.email')
   assert b['CRM – lier sans envoi']['parameters']['workflowId']['value']==proof['workflows']['AI Continuous Improvement']['id']
   for source,ports in old['connections'].items():
    if source!='Site – tâche sauvegardée':assert new['connections'][source]==ports
   assert new['connections']['Site – tâche sauvegardée']['main'][0][:-1]==old['connections'].get('Site – tâche sauvegardée',{'main':[[]]})['main'][0]
  if name=='My workflow':
   assert set(a)==set(b) and old['connections']==new['connections']
   prep=b['Growth – contexte isolé']['parameters']['jsCode'];assert "crm_dry_run" in prep and 'fixture' in prep and '/growth-ingest-safe' in prep
  if name=='AI Continuous Improvement':
   for node in new['nodes']:
    if node['name'] in a:continue
    assert not node.get('credentials') and node['type'] in {'n8n-nodes-base.code','n8n-nodes-base.dataTable','n8n-nodes-base.if','n8n-nodes-base.splitInBatches'}
    if node['type'].endswith('.dataTable'):assert node['parameters']['dataTableId']['value'] in {'aqPFAT3TBwLGhlIj','ns20LV2q6otiEP3X','NE0QU8afBFipimhW'}
   for source,ports in old['connections'].items():
    if source!='Improvement – diagnostic interne':assert new['connections'][source]==ports
   assert b['CRM – plan']['parameters']['jsCode'].startswith(sources['inbound'])
   assert "statut:'needs_review'" in sources['inbound'] and "input.source_workflow_id==='fixture'||input.crm_dry_run===true" in sources['inbound']
   assert 'CRM_NO_WRITE_IN_FIXTURE' in b['CRM – réservation']['parameters']['jsCode']
 return proof
