"""Offline provenance for the OAuth MCP publication, never a ChatGPT registration claim."""
import hashlib,json

def verify(root,entry):
 def read(p):return json.loads((root/p).read_text())
 path='revisions/mcp-20261019/verification.json';assert entry['path']==path
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==entry['sha256']
 proof=read(path)
 for p,key in [('revisions/mcp-20261019/ChatGPT ingress.before.json','front_before_sha256'),('ChatGPT ingress.json','front_after_sha256'),('Codex MCP.json','mcp_sha256')]:assert hashlib.sha256((root/p).read_bytes()).hexdigest()==proof[key]
 old=read('revisions/mcp-20261019/ChatGPT ingress.before.json');front=read('ChatGPT ingress.json');server=read('Codex MCP.json');nodes={n['id']:n for n in front['nodes']}
 assert old['id']==front['id']==proof['front_id'] and front['versionId']==proof['front_published_version_id']
 assert server['id']==proof['mcp_id'] and server['versionId']==proof['mcp_published_version_id']
 assert old['settings']==front['settings']
 for n in old['nodes']:
  a=nodes[n['id']];assert a.get('credentials')==n.get('credentials') and a.get('webhookId')==n.get('webhookId')
  if n['type']!='n8n-nodes-base.code':assert a['parameters']==n['parameters']
 for source,ports in old['connections'].items():
  if source=='ChatGPT – requête valide ?':continue
  assert front['connections'][source]==ports
 f={n['name']:n for n in front['nodes']}
 crypto=f['ChatGPT – empreinte clé MCP'];assert crypto['parameters']=={'action':'hash','type':'SHA256','value':'={{ $json.bridge_key }}','dataPropertyName':'bridge_key_hash','encoding':'hex','binaryData':False}
 gate=f['ChatGPT – valider clé limitée']['parameters']['jsCode'];assert proof['bridge_key_sha256'] in gate and "mcp_key_technical_scope_only" in gate and "mcp_request_namespace_required" in gate
 assert "auth_header,bridge_key,...safe" in f['ChatGPT – accès validé']['parameters']['jsCode']
 assert front['connections']['ChatGPT – clé MCP ?']['main'][1]==[{'node':'ChatGPT – vérifier accès','type':'main','index':0}]
 assert front['connections']['ChatGPT – valider clé limitée']['main'][0]==[{'node':'ChatGPT – accès validé','type':'main','index':0}]
 assert len(server['nodes'])==3
 trigger=next(n for n in server['nodes'] if n['type']=='@n8n/n8n-nodes-langchain.mcpTrigger')
 assert trigger['typeVersion']>=2 and trigger['parameters']['authentication']=='n8nOAuth2' and trigger['parameters']['requireExecuteAccess'] is True
 tools={n['name']:n for n in server['nodes'] if n['type']=='n8n-nodes-base.httpRequestTool'};assert set(tools)=={'submit_codex_task','get_codex_task_status'}
 for name,node in tools.items():
  p=node['parameters'];assert p['authentication']=='genericCredentialType' and p['genericAuthType']=='httpHeaderAuth'
  assert node['credentials']['httpHeaderAuth']['name']==proof['bridge_credential_name']
  assert server['connections'][name]['ai_tool'][0]==[{'node':trigger['name'],'type':'ai_tool','index':0}]
  assert p['url']=='https://navajowhite-cormorant-668337.hostingersite.com/webhook/mb-chatgpt/v1/'+('commands' if name=='submit_codex_task' else 'status')
  assert p['method']==('POST' if name=='submit_codex_task' else 'GET')
  assert p['options']['redirect']['redirect']['followRedirects'] is False
 for w in [server,front]:
  assert w['settings']['saveDataSuccessExecution']==w['settings']['saveDataErrorExecution']=='none'
  assert w['settings']['saveManualExecutions'] is False and w['settings']['saveExecutionProgress'] is False
  assert w['settings']['errorWorkflow']=='4O2ZR1JpDOgJZOLw'
 return proof
