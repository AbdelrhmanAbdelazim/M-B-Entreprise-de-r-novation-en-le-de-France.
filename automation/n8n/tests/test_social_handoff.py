"""Offline safety successor provenance; never submits social content."""
import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from social_verify import verify
from cloud_handoff import collect
class SocialHandoffTests(unittest.TestCase):
 def test_exact_single_node_successor_and_full_history_are_verified(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['social_revision'];proof=verify(ROOT,entry)
  self.assertEqual(proof['id'],'cKUyJSLOF69uXGnO');report=collect(ROOT);self.assertTrue(report['social_safety_revision_verified']);self.assertEqual(report['pending_patch_count'],0)
 def test_modified_safety_source_graph_or_predecessor_cannot_pass(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['social_revision']
  for target in ['social-publishing.js','My workflow.json','revisions/social-20261019/My workflow.before.json','revisions/social-20261019/verification.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions/social-20261019',r/'revisions/social-20261019')
    for f in ['social-publishing.js','My workflow.json']:shutil.copyfile(ROOT/f,r/f)
    verify(r,entry);p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
if __name__=='__main__':unittest.main()
