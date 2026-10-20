import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from inbound_video_verify import verify
from cloud_handoff import collect
TARGETS={"My workflow":"revisions/direct-social-20261020/My workflow.before.json","W10":"revisions/provider-readonly-20261020/W10.before.json"}
class InboundVideoHandoff(unittest.TestCase):
 def test_live_successor_is_exact_and_old_chain_still_verifies(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['inbound_video_revision'];p=verify(ROOT,entry,TARGETS);self.assertEqual(p['safe_runtime']['crm_execution_id'],'587');self.assertEqual(collect(ROOT)['inbound_video_revisions_verified'],4)
 def test_sources_are_exact_frozen_deployed_code(self):
  for name in ['inbound','video']:self.assertEqual((ROOT.parent/f'growth-engine/{name}.js').read_bytes(),(ROOT/f'revisions/inbound-video-20261020/{name}-source.js').read_bytes())
 def test_export_archive_and_source_tampering_fail(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['inbound_video_revision']
  for name in ['W2.json','W10.json','My workflow.json','revisions/inbound-video-20261020/AI Continuous Improvement.json','revisions/inbound-video-20261020/inbound-source.js']:
   with self.subTest(name=name),tempfile.TemporaryDirectory() as tmp:
    r=pathlib.Path(tmp);shutil.copytree(ROOT/'revisions/inbound-video-20261020',r/'revisions/inbound-video-20261020')
    for f in ['W2.json','W10.json','My workflow.json']:shutil.copyfile(ROOT/TARGETS.get(f.removesuffix('.json'),f),r/f)
    verify(r,entry);f=r/name;f.write_text(f.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
if __name__=='__main__':unittest.main()
