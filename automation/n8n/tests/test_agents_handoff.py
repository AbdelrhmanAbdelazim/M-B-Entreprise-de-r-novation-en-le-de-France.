import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agents_verify import verify
from cloud_handoff import collect
class AgentsHandoffTests(unittest.TestCase):
 def test_published_provenance_and_preservation(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['agents_revision']);self.assertEqual(p['workflow'],'My workflow');self.assertEqual(collect(ROOT)['pending_patch_count'],0)
 def test_snapshot_or_archived_draft_tampering_is_rejected(self):
  for target in ['My workflow.json','revisions/agents-20261019/My workflow.draft-before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions/agents-20261019',r/'revisions/agents-20261019');shutil.copyfile(ROOT/'My workflow.json',r/'My workflow.json');p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,json.loads((ROOT/'continuation.json').read_text())['agents_revision'])
if __name__=='__main__':unittest.main()
