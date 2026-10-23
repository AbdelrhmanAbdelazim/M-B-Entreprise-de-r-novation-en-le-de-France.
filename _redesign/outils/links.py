import os,re,sys,html
from urllib.parse import urljoin,urlparse,unquote
root=sys.argv[1]; files=[]
for d,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.html'): files.append(os.path.join(d,f))
ids={}
def url_of(f):
    p='/'+os.path.relpath(f,root); return p[:-10] if p.endswith('index.html') else p
for f in files:
    ids[url_of(f)]=set(re.findall(r'\sid="([^"]+)"',open(f,errors='ignore').read()))
broken=[];anch=[];n=0
for f in files:
    s=open(f,errors='ignore').read(); u=url_of(f)
    for m in re.findall(r'(?:href|src)="([^"]+)"',s):
        m=html.unescape(m)
        if m.startswith(('http','mailto:','tel:','data:','javascript:','//','{{')): continue
        n+=1; full=urljoin('https://x'+u,m); pu=urlparse(full); path=unquote(pu.path)
        t=os.path.join(root,path.lstrip('/'))
        ok=os.path.isfile(t) or os.path.isfile(os.path.join(t,'index.html')) or os.path.isfile(t+'.html')
        if not ok: broken.append((u,m)); continue
        if pu.fragment:
            key=path if path.endswith('/') or '.' in path.split('/')[-1] else path+'/'
            key=key.replace('index.html','')
            if pu.fragment not in ids.get(key,ids.get(path,set())): anch.append((u,m))
print(root,'pages',len(files),'liens internes',n,'cassés',len(broken),broken[:10],'ancres cassées',len(anch),anch[:10])
