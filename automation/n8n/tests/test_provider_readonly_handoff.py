import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from provider_readonly_verify import verify
from cloud_handoff import collect
TARGETS={n:"revisions/social-intelligence-20261020/"+n+".before.json" for n in ["My workflow","W10","ChatGPT ingress"]}
class ProviderReadonlyHandoff(unittest.TestCase):
 def test_deployed_exact_successor_and_entire_predecessor_chain(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['provider_readonly_revision'],TARGETS);self.assertEqual(p['runtime']['credential_child_execution_id'],'614');self.assertEqual(collect(ROOT)['provider_readonly_revisions_verified'],3)
 def test_read_evidence_does_not_become_generation_or_publishing_authority(self):
  c=json.loads((ROOT/'continuation.json').read_text());e=verify(ROOT,c['provider_readonly_revision'],TARGETS)['provider_evidence'];self.assertTrue(e['meta']['user_identity_read']);self.assertEqual(e['meta']['accessible_page_count'],0);self.assertFalse(e['runway']['authentication_verified']);self.assertFalse(e['creatomate']['authentication_verified']);self.assertFalse(e['rendering_enabled']);self.assertFalse(e['publishing_enabled']);self.assertNotIn('user_identity',e['meta'])
 def test_export_source_or_predecessor_tamper_is_rejected(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['provider_readonly_revision']
  for target in ['W10.json','My workflow.json','ChatGPT ingress.json','provider-readonly.js','revisions/provider-readonly-20261020/video-provider-gates-source.js','revisions/provider-readonly-20261020/ChatGPT ingress.before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as tmp:
    r=pathlib.Path(tmp);shutil.copytree(ROOT/'revisions/provider-readonly-20261020',r/'revisions/provider-readonly-20261020')
    for f in ['W10.json','My workflow.json','ChatGPT ingress.json','provider-readonly.js']:shutil.copyfile(ROOT/TARGETS.get(f.removesuffix(".json"),f),r/f)
    verify(r,entry);f=r/target;f.write_text(f.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
if __name__=='__main__':unittest.main()
