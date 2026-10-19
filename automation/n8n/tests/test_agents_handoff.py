import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agents_verify import verify
from cloud_handoff import collect
class AgentsHandoffTests(unittest.TestCase):
 def test_published_provenance_and_preservation(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['agents_revision'],'revisions/ingress-20261019/My workflow.before.json' if c.get('ingress_revision') else 'My workflow.json');self.assertEqual(p['workflow'],'My workflow');self.assertEqual(collect(ROOT)['pending_patch_count'],0)
 def test_snapshot_or_archived_draft_tampering_is_rejected(self):
  after='revisions/ingress-20261019/My workflow.before.json' if (ROOT/'revisions/ingress-20261019').exists() else 'My workflow.json'
  for target in [after,'revisions/agents-20261019/My workflow.draft-before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions',r/'revisions');shutil.copyfile(ROOT/'My workflow.json',r/'My workflow.json');entry=json.loads((ROOT/'continuation.json').read_text())['agents_revision'];verify(r,entry,after)
    p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry,after)
if __name__=='__main__':unittest.main()
