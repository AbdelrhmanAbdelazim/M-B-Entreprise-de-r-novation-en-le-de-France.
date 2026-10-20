"""Exact two-workflow formatter successor; no email delivery."""
import hashlib,json,copy
NAMES={'W3','W4'}
def verify(root,entry):
 path='revisions/commercial-email-20261020/verification.json';assert entry['path']==path and hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256'];p=json.loads((root/path).read_text());assert set(p['workflows'])==NAMES
 source=(root/'commercial-email.js').read_text();assert hashlib.sha256(source.encode()).hexdigest()==p['source_sha256']
 for name,r in p['workflows'].items():
  before_path='revisions/commercial-email-20261020/'+name+'.before.json';after_path=name+'.json'
  for f,key in [(before_path,'before_sha256'),(after_path,'after_sha256')]:assert hashlib.sha256((root/f).read_bytes()).hexdigest()==r[key]
  old=json.loads((root/before_path).read_text());new=json.loads((root/after_path).read_text());expected=copy.deepcopy(old)
  for n in expected['nodes']:
   if n['name']=='Construire email':n['parameters']['jsCode']=source+'\nreturn {json:renderCommercialEmail($json,'+json.dumps('outreach' if name=='W3' else 'followup')+')};\n'
   if n['name']=='Email texte (B)':n['parameters'].update(emailFormat='both',html='={{ $json.html }}')
   if name=='W4' and n['name']=='Garde commerciale':
    needle="allowed=allowed&&Number(lead?.id)!==79;";n['parameters']['jsCode']=n['parameters']['jsCode'].replace(needle,needle+"\nallowed=allowed&&typeof lead?.message_id==='string'&&lead.message_id.trim().length>0; // A follow-up requires recorded SMTP/message proof.\n")
  assert old['id']==new['id']==r['id'] and old['versionId']==r['before_version_id'] and new['versionId']==r['published_version_id']
  for k in ['id','name','nodes','connections','settings']:assert expected[k]==new[k]
 return p
