import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from cloud_handoff import collect
from stage_patch import stage
class MetricoolHandoffTests(unittest.TestCase):
 def test_strict_successor_chain_matches_all_three_current_workflows(self):
  report=collect(ROOT);self.assertEqual(report['metricool_verified_followup_revisions'],3);self.assertEqual(report['additional_verified_production_revisions'],3);self.assertEqual(report['pending_patch_count'],0)
  for name in ['My workflow','W5','W10']:
   directory=ROOT/'revisions/metricool-20261019';before=json.loads((directory/(name+'.before.json')).read_text());patch=json.loads((directory/(name+'.patch.json')).read_text());current=json.loads((ROOT/(name+'.json')).read_text());candidate=stage(before,patch)
   for key in ['id','name','nodes','connections','settings']:self.assertEqual(candidate[key],current[key])
 def test_changed_metricool_patch_cannot_be_reported_as_verified(self):
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory)
   for name in ['manifest.json','continuation.json','activation.json','data-tables.json','My workflow.json']+[f'W{i}.json' for i in range(11)]:shutil.copyfile(ROOT/name,target/name)
   for name in ['pending','revisions']:shutil.copytree(ROOT/name,target/name)
   p=target/'revisions/metricool-20261019/My workflow.patch.json';p.write_text(p.read_text()+' ')
   with self.assertRaisesRegex(ValueError,'Metricool revision provenance'):collect(target)
if __name__=='__main__':unittest.main()
