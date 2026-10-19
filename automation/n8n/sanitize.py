import copy, re

def sanitize(document):
    """Remove operational bindings and execution data, never change business logic."""
    d=copy.deepcopy(document); replacements={}; changes=[]
    for n in d['nodes']:
        for kind,cred in n.get('credentials',{}).items():
            if cred.get('id'):replacements[str(cred['id'])]='__EXISTING_'+kind.upper()+'_CREDENTIAL_ID__'
        p=n.get('parameters',{})
        if n.get('webhookId'):replacements[n['webhookId']]='__PRIVATE_'+str(n['id']).replace('-','_')+'_WEBHOOK_ID__'
        if n['type'].endswith('.webhook') and isinstance(p.get('path'),str):
            replacements[p['path']]='__PRIVATE_'+str(n['id']).replace('-','_')+'_WEBHOOK_PATH__'
        if '.telegram' in n['type'] and p.get('chatId') is not None and not str(p['chatId']).startswith('='):
            replacements[str(p['chatId'])]='__PRIVATE_TELEGRAM_CHAT_ID__'
    def walk(v,path):
        if isinstance(v,dict):return {k:walk(x,path+'/'+str(k)) for k,x in v.items()}
        if isinstance(v,list):return [walk(x,path+'/'+str(i)) for i,x in enumerate(v)]
        if isinstance(v,str):
            old=v
            for source,target in sorted(replacements.items(),key=lambda p:-len(p[0])):
                if source:v=v.replace(source,target)
            if v!=old:changes.append(path)
        elif isinstance(v,int) and str(v) in replacements:
            changes.append(path);return replacements[str(v)]
        return v
    for key in ['pinData','staticData']:
        if key in d:d.pop(key);changes.append('/'+key)
    if isinstance(d.get('meta'),dict) and 'instanceId' in d['meta']:
        d['meta'].pop('instanceId');changes.append('/meta/instanceId')
    d=walk(d,'')
    return d, sorted(set(changes))
