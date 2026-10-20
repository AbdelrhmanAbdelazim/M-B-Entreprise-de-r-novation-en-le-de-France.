import json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from mcp_verify import verify
from cloud_handoff import collect
class McpHandoffTests(unittest.TestCase):
 def test_publication_is_verified_without_a_false_chatgpt_connection_claim(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['mcp_revision'];verify(ROOT,entry);report=collect(ROOT);self.assertTrue(report['additional_mcp_published_verified']);release=json.loads((ROOT/'mcp-release.json').read_text());self.assertEqual(release['result'],'BLOCKED');self.assertEqual(release['chatgpt_origin_task_test'],'NOT_RUN')
 def test_changed_mcp_and_scoped_frontend_are_rejected(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['mcp_revision']
  for target in ['Codex MCP.json','ChatGPT ingress.json','revisions/mcp-20261019/ChatGPT ingress.before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions/mcp-20261019',r/'revisions/mcp-20261019')
    for name in ['Codex MCP.json','ChatGPT ingress.json']:shutil.copyfile(ROOT/name,r/name)
    verify(r,entry);p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
if __name__=='__main__':unittest.main()
