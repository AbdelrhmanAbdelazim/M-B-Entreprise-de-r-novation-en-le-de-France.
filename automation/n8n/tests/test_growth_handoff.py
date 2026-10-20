import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from growth_verify import verify
from cloud_handoff import collect
class GrowthHandoffTests(unittest.TestCase):
 def test_exact_two_workflow_successor_and_single_observer(self):
  c=json.loads((ROOT/'continuation.json').read_text());p=verify(ROOT,c['growth_revision']);self.assertEqual(set(p['workflows']),{'W10','My workflow'});self.assertEqual(collect(ROOT)['growth_revisions_verified'],2)
 def test_modified_graph_archive_or_sources_cannot_pass(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['growth_revision']
  for f in ['My workflow.json','W10.json','revisions/growth-20261020/My workflow.before.json','revisions/growth-20261020/AI Continuous Improvement.json','revisions/growth-20261020/improvement-source.js','revisions/growth-20261020/content-source.js']:
   with self.subTest(file=f),tempfile.TemporaryDirectory() as tmp:
    p=pathlib.Path(tmp);shutil.copytree(ROOT/'revisions/growth-20261020',p/'revisions/growth-20261020')
    for name in ['My workflow.json','W10.json']:shutil.copyfile(ROOT/name,p/name)
    verify(p,entry);target=p/f;target.write_text(target.read_text()+' ')
    with self.assertRaises(AssertionError):verify(p,entry)
 def test_public_sources_match_frozen_deployed_code(self):
  for source,frozen in [('improvement.js','improvement-source.js'),('content-drafts.js','content-source.js')]:self.assertEqual((ROOT.parent/'growth-engine'/source).read_bytes(),(ROOT/'revisions/growth-20261020'/frozen).read_bytes())
if __name__=='__main__':unittest.main()
