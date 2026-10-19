"""Read-only n8n export from Cloud. No execution, write or activation API exists here."""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from sanitize import sanitize
from validate import check_document

ROOT=pathlib.Path(__file__).resolve().parent
HOST='navajowhite-cormorant-668337.hostingersite.com'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=pathlib.Path,default=ROOT/'private-live')
    args=parser.parse_args()
    base=os.environ.get('N8N_BASE_URL','').rstrip('/')
    key=os.environ.get('N8N_API_KEY','')
    u=urllib.parse.urlsplit(base)
    if u.scheme!='https' or u.hostname!=HOST or u.port not in [None,443] or u.username or u.password or u.query or u.fragment or u.path:
        sys.exit('Configure N8N_BASE_URL as the documented HTTPS origin, without credentials or paths.')
    if not key:sys.exit('N8N_API_KEY is not bound in this Cloud environment; do not paste it into Git or chat.')
    target=args.out.resolve()
    if target==ROOT or ROOT in target.parents and target!=ROOT/'private-live':
        sys.exit('Use the ignored private-live directory or an output directory outside the repository bundle.')
    manifest=json.loads((ROOT/'manifest.json').read_text()); snapshots={}
    opener=urllib.request.build_opener(NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    for name,record in manifest['workflows'].items():
        request=urllib.request.Request(base+'/api/v1/workflows/'+urllib.parse.quote(record['id'],safe=''),headers={'X-N8N-API-KEY':key,'Accept':'application/json'},method='GET')
        try:
            with opener.open(request,timeout=25) as response:raw=json.load(response)
        except urllib.error.HTTPError as exc:
            sys.exit(f'Read-only export blocked at {name}: HTTP {exc.code}. No n8n changes made; no partial bundle written.')
        except (urllib.error.URLError,TimeoutError,ValueError):
            sys.exit(f'Read-only export unavailable at {name}. Check host health, enforced network policy and CA trust. No response secrets printed.')
        if raw.get('id')!=record['id']:sys.exit('Workflow identity mismatch; no output written.')
        clean,paths=sanitize(raw);check_document(clean)
        snapshots[name]=(raw,clean,paths)
    target.mkdir(parents=True,exist_ok=True)
    evidence={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'GET only; sanitized snapshots','workflows':{}}
    for name,(raw,clean,paths) in snapshots.items():
        text=json.dumps(clean,ensure_ascii=False,indent=2)+'\n'
        (target/(name+'.json')).write_text(text)
        evidence['workflows'][name]={'id':raw['id'],'version_id':raw.get('versionId'),'active':raw.get('active'),'sha256':hashlib.sha256(text.encode()).hexdigest(),'redacted_paths':paths}
    (target/'capture.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print('Read-only snapshot complete: 12 workflows, no executions or remote changes. Compare capture.json before further work.')

if __name__=='__main__':main()
