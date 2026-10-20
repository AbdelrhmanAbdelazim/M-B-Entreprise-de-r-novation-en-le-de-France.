import json,pathlib,sys,tempfile,shutil,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from direct_social_verify import verify
from cloud_handoff import collect
class DirectSocialHandoff(unittest.TestCase):
 def test_exact_successor_and_full_prior_chain(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['direct_social_revision']);self.assertEqual(p['runtime']['diagnostic_execution_id'],'601');self.assertEqual(collect(ROOT)['direct_social_revisions_verified'],2)
 def test_no_credential_or_external_transport_is_claimed(self):
  p=json.loads((ROOT/'direct-social-release.json').read_text());self.assertEqual(p['new_credential_count'],0);self.assertFalse(p['official_publish_transport_installed']);self.assertFalse(p['actual_official_platform_permissions_verified']);self.assertEqual(p['production_active'],15)
 def test_current_graph_source_and_before_tampering_fail(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['direct_social_revision']
  for name in ['My workflow.json','direct-social.js','revisions/direct-social-20261020/AI Continuous Improvement.json','revisions/direct-social-20261020/My workflow.before.json']:
   with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
    p=pathlib.Path(temp);shutil.copytree(ROOT/'revisions/direct-social-20261020',p/'revisions/direct-social-20261020')
    for f in ['My workflow.json','direct-social.js','metricool.js']:shutil.copyfile(ROOT/f,p/f)
    verify(p,entry);f=p/name;f.write_text(f.read_text()+' ')
    with self.assertRaises(AssertionError):verify(p,entry)
if __name__=='__main__':unittest.main()
