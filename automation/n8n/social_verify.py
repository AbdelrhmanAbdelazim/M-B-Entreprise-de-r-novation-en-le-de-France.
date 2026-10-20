"""Verify the single-node social safety successor, never provider publishing."""
import hashlib,json

def verify(root,entry,after_path="My workflow.json"):
 path='revisions/social-20261019/verification.json'
 assert entry['path']==path and hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256']
 p=json.loads((root/path).read_text())
 for name,key in [('revisions/social-20261019/My workflow.before.json','before_sha256'),(after_path,'after_sha256'),('social-publishing.js','source_sha256')]:
  assert hashlib.sha256((root/name).read_bytes()).hexdigest()==p[key]
 old=json.loads((root/'revisions/social-20261019/My workflow.before.json').read_text());new=json.loads((root/after_path).read_text())
 assert old['id']==new['id']==p['id'] and old['versionId']==p['before_version_id'] and new['versionId']==p['published_version_id']
 for key in ['name','connections','settings']:assert old[key]==new[key]
 assert len(old['nodes'])==len(new['nodes']);nodes={n['id']:n for n in new['nodes']};assert len(nodes)==len(new['nodes'])
 changed=[]
 for n in old['nodes']:
  a=nodes[n['id']]
  if a!=n:
   changed.append(n['name']);assert {**a,'parameters':n['parameters']}==n
   assert list(a['parameters'])==list(n['parameters'])==['jsCode']
   source=(root/'social-publishing.js').read_text();code=a['parameters']['jsCode']
   assert code==source+'\n'+n['parameters']['jsCode'].replace('metricoolQueuePlan(q,iso()).map(jq)','socialPublishingGate(q,metricoolQueuePlan(q,iso()),iso(),'+json.dumps(p['cutover'])+').map(jq)')
 assert changed==['Coordination – plan']
 assert "incident='391473868'" in source and 'verified_publishers:[]' in source
 return p
