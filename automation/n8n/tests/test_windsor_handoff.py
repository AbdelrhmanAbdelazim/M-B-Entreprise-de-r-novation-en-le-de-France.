import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from cloud_handoff import collect
from stage_patch import stage
class WindsorHandoffTests(unittest.TestCase):
 def copy_bundle(self,target):
  for name in ['commercial-email.js', 'social-publishing.js', 'management.js', 'qualification.js', 'Codex MCP.json', 'ChatGPT ingress.json', 'manifest.json','continuation.json','activation.json','data-tables.json','My workflow.json']+[f'W{i}.json' for i in range(11)]:shutil.copyfile(ROOT/name,target/name)
  for name in ['pending','revisions']:shutil.copytree(ROOT/name,target/name)
 def test_all_three_published_consumers_have_strict_before_patch_after_provenance(self):
  report=collect(ROOT);self.assertEqual(report['additional_verified_production_revisions'],3);self.assertEqual(report['pending_patch_count'],0)
  for name in ['W5','W8','W10']:
   directory=ROOT/'revisions/windsor-20261019';before=json.loads((directory/(name+'.before.json')).read_text());patch=json.loads((directory/(name+'.patch.json')).read_text());current_path=ROOT/'revisions/metricool-20261019'/(name+'.before.json');current=json.loads((current_path if current_path.exists() else ROOT/(name+'.json')).read_text());candidate=stage(before,patch)
   for key in ['id','name','nodes','connections','settings']:self.assertEqual(candidate[key],current[key])
 def test_changed_archive_and_missing_revision_refuse_false_handoff(self):
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory);self.copy_bundle(target);p=target/'revisions/windsor-20261019/W5.patch.json';p.write_text(p.read_text()+' ')
   with self.assertRaisesRegex(ValueError,'provenance'):collect(target)
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory);self.copy_bundle(target);p=target/'continuation.json';data=json.loads(p.read_text());data['production_revisions']=[];p.write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'requires all three'):collect(target)
if __name__=='__main__':unittest.main()
