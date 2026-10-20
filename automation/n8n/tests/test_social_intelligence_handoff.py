import json,pathlib,sys,unittest,tempfile,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from social_intelligence_verify import verify
from cloud_handoff import collect
class SocialIntelligenceHandoff(unittest.TestCase):
 def test_exact_live_successor_and_full_pinned_chain(self):
  e=json.loads((ROOT/'continuation.json').read_text())['social_intelligence_revision'];p=verify(ROOT,e);self.assertEqual(p['runtime']['native_zero_model_test']['execution_id'],'638');self.assertEqual(collect(ROOT)['social_intelligence_revisions_verified'],5)
 def test_actual_contact_scopes_and_no_cost_generation_authorization(self):
  e=json.loads((ROOT/'continuation.json').read_text())['social_intelligence_revision'];p=verify(ROOT,e);s=p['provider_evidence'];self.assertTrue(s['creatomate']['authentication_verified']);self.assertEqual(s['meta']['accessible_page_count'],0);self.assertFalse(s['runway']['authentication_verified']);self.assertTrue(s['telegram']['owner_chat_read_verified']);self.assertEqual(p['runtime']['boamp_actual_review_rows'],[196,197,198,199,200]);self.assertFalse(s['rendering_enabled']);self.assertIsNone(p['runtime']['legacy_audit_billed_cost'])
 def test_modified_source_archive_or_current_workflow_is_rejected(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['social_intelligence_revision']
  for name in ['W7.json','W10.json','ChatGPT ingress.json','My workflow.json','revisions/social-intelligence-20261020/AI Continuous Improvement.json','revisions/social-intelligence-20261020/social-intelligence-source.js']:
   with self.subTest(name=name),tempfile.TemporaryDirectory() as tmp:
    r=pathlib.Path(tmp);shutil.copytree(ROOT/'revisions/social-intelligence-20261020',r/'revisions/social-intelligence-20261020')
    for f in ['W7.json','W10.json','My workflow.json','ChatGPT ingress.json','activation.json']:shutil.copyfile(ROOT/f,r/f)
    verify(r,entry);p=r/name;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
if __name__=='__main__':unittest.main()
