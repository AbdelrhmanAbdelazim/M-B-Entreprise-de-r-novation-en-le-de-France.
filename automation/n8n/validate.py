"""Validate this handoff only; never execute a workflow or contact a provider."""
import hashlib
import json
import pathlib
import re

ROOT=pathlib.Path(__file__).resolve().parent
SECRET=re.compile(r'(?:sk-(?:proj|ant)-[A-Za-z0-9_-]{12,}|AIzaSy[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,})')

def check_document(d):
    assert not d.get('pinData') and not d.get('staticData'), 'Execution state must remain private'
    names={n['name'] for n in d['nodes']}
    assert len(names)==len(d['nodes']), 'Duplicate node names'
    for source,ports in d['connections'].items():
        assert source in names, 'Missing edge source'
        for groups in ports.values():
            for edges in groups:
                for e in edges:assert e['node'] in names, 'Missing edge destination'
    assert not SECRET.search(json.dumps(d)), 'Possible embedded secret; stop without printing it'
    for n in d['nodes']:
        for c in n.get('credentials',{}).values():assert c.get('id','').startswith('__EXISTING_'), 'Unredacted credential binding'
        if n.get('webhookId'):assert n['webhookId'].startswith('__PRIVATE_'), 'Unredacted webhook ID'
        p=n['parameters']
        if n['type'].endswith('.webhook'):assert p.get('path','').startswith('__PRIVATE_'), 'Unredacted webhook route'
        if '.telegram' in n['type'] and 'chatId' in p:
            assert str(p['chatId']).startswith(('=','__PRIVATE_')), 'Unredacted Telegram destination'
        body=p.get('jsonBody')
        if isinstance(body,str) and '{{' in body:
            assert '}}' not in body[body.find('{{')+2:body.rfind('}}')], 'Premature n8n expression delimiter'

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    expected={f'W{i}' for i in range(11)}|{'My workflow'}
    assert set(manifest['workflows'])==expected
    ids=set()
    for key,record in manifest['workflows'].items():
        path=ROOT/(key+'.json');blob=path.read_bytes()
        assert hashlib.sha256(blob).hexdigest()==record['public_sha256'], 'Snapshot checksum mismatch'
        d=json.loads(blob);check_document(d)
        assert d['id']==record['id'] and d['versionId']==record['version_id']
        assert d['id'] not in ids;ids.add(d['id'])
        assert d['settings'].get('errorWorkflow')==(None if key=='W0' else manifest['workflows']['W0']['id'])
    print('Handoff OK: 12 actual snapshot identities, checksums, graphs and redactions; no live tests repeated.')

if __name__=='__main__':main()
