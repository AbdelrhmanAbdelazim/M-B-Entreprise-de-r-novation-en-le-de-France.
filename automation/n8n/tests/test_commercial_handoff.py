import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from commercial_verify import verify
from cloud_handoff import collect
class CommercialHandoffTests(unittest.TestCase):
 def test_two_workflow_successor_and_predecessors_are_verified(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['commercial_revision']);self.assertEqual(set(p['workflows']),{'W3','W4'});r=collect(ROOT);self.assertEqual(r['commercial_email_revisions_verified'],2);self.assertEqual(r['pending_patch_count'],0)
 def test_changed_formatter_graph_or_archive_cannot_pass(self):
  c=json.loads((ROOT/'continuation.json').read_text())['commercial_revision']
  for target in ['commercial-email.js','W3.json','W4.json','revisions/commercial-email-20261020/W3.before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions/commercial-email-20261020',r/'revisions/commercial-email-20261020')
    for f in ['commercial-email.js','W3.json','W4.json']:shutil.copyfile(ROOT/f,r/f)
    verify(r,c);p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,c)
if __name__=='__main__':unittest.main()
