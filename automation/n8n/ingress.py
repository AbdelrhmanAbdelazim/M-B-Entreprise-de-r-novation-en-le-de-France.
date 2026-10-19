"""Authenticated ChatGPT/Codex Cloud client for the hosted production ingress.
Uses existing N8N_BASE_URL/N8N_API_KEY bindings. Never exports credentials.
"""
import argparse,json,os,pathlib,ssl,time,urllib.error,urllib.parse,urllib.request,uuid
from live_status import origin,NoRedirect

COMMAND='/webhook/mb-chatgpt/v1/commands'
STATUS='/webhook/mb-chatgpt/v1/status'

def call(method,path,body=None,*,attempts=2):
 base=origin(os.environ.get('N8N_BASE_URL','').rstrip('/'))
 key=os.environ.get('N8N_API_KEY')
 if not key:raise RuntimeError('Existing N8N_API_KEY binding unavailable; never paste it into chat')
 headers={'X-N8N-API-KEY':key,'Accept':'application/json'}
 if body is not None:headers['Content-Type']='application/json'
 opener=urllib.request.build_opener(NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
 for attempt in range(attempts):
  req=urllib.request.Request(base+path,headers=headers,data=None if body is None else json.dumps(body,ensure_ascii=False).encode(),method=method)
  try:
   with opener.open(req,timeout=20) as response:return response.status,json.load(response)
  except urllib.error.HTTPError as error:
   if error.code in [429,500,502,503,504] and attempt+1<attempts:time.sleep(1);continue
   # Only expose the bounded public API contract, never raw HTTP error bodies or headers.
   try:data=json.load(error)
   except (ValueError,TypeError):data={'error':'ingress_http_failure'}
   return error.code,{k:v for k,v in data.items() if k in ['request_id','error','status']}
  except (urllib.error.URLError,TimeoutError):
   if attempt+1<attempts:time.sleep(1);continue
   raise RuntimeError('Ingress transport unavailable; retry the SAME request_id; acceptance may be uncertain') from None

def submit(task,request_id=None,route=None):
 payload={'task':task,'source':'chatgpt','request_id':request_id or 'chatgpt-'+uuid.uuid4().hex}
 if route:payload['route']=route
 try:code,result=call('POST',COMMAND,payload)
 except RuntimeError as error:raise RuntimeError(str(error)+'; request_id='+payload['request_id']) from None
 return code,result,payload['request_id']

def status(request_id):return call('GET',STATUS+'?'+urllib.parse.urlencode({'request_id':request_id}))

def main():
 p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='operation',required=True)
 post=s.add_parser('submit');post.add_argument('--task-file',type=pathlib.Path,required=True);post.add_argument('--request-id');post.add_argument('--route',choices=['technical','manager']);post.add_argument('--wait',type=int,default=0)
 poll=s.add_parser('status');poll.add_argument('request_id');a=p.parse_args()
 try:
  if a.operation=='status':code,result=status(a.request_id)
  else:
   code,result,key=submit(a.task_file.read_text(),a.request_id,a.route)
   deadline=time.monotonic()+min(max(a.wait,0),360)
   while code==202 and time.monotonic()<deadline and result.get('status') not in ['failed','cancelled','needs_attention','uncertain']:
    time.sleep(min(5,max(0,deadline-time.monotonic())));code,result=status(key)
  print(json.dumps({'http_status':code,**result},ensure_ascii=False));return 0 if code in [200,202] and result.get('status') not in ['failed','cancelled','needs_attention','uncertain'] else 1
 except (RuntimeError,ValueError) as error:p.exit(1,str(error)+'\n')
if __name__=='__main__':raise SystemExit(main())
