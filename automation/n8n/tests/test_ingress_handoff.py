import json,pathlib,shutil,sys,tempfile,unittest,urllib.error
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from ingress_verify import verify
from cloud_handoff import collect
import ingress
class IngressHandoffTests(unittest.TestCase):
 def test_published_ingress_chain_preserves_original_engine(self):
  verify(ROOT,json.loads((ROOT/'continuation.json').read_text())['ingress_revision']);self.assertEqual(collect(ROOT)['pending_patch_count'],0)
 def test_changed_ingress_or_archived_input_is_rejected(self):
  entry=json.loads((ROOT/'continuation.json').read_text())['ingress_revision']
  for target in ['ChatGPT ingress.json','My workflow.json','revisions/ingress-20261019/My workflow.draft-before.json']:
   with self.subTest(target=target),tempfile.TemporaryDirectory() as directory:
    r=pathlib.Path(directory);shutil.copytree(ROOT/'revisions/ingress-20261019',r/'revisions/ingress-20261019')
    for name in ['ChatGPT ingress.json','My workflow.json']:shutil.copyfile(ROOT/name,r/name)
    verify(r,entry);p=r/target;p.write_text(p.read_text()+' ')
    with self.assertRaises(AssertionError):verify(r,entry)
 def test_uncertain_submit_exposes_only_safe_correlation_for_resume(self):
  with patch.object(ingress,'call',side_effect=RuntimeError('transport unavailable')):
   with self.assertRaisesRegex(RuntimeError,'request_id=request-fixture-001'):ingress.submit('safe task','request-fixture-001','technical')
 def test_retry_reuses_the_identical_submission_body(self):
  seen=[]
  class Response:
   status=202
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def read(self):return b'{"status":"ready"}'
  class Opener:
   def open(self,request,timeout):
    seen.append(request.data)
    if len(seen)==1:raise urllib.error.URLError('fixture timeout')
    return Response()
  with patch.dict('os.environ',{'N8N_BASE_URL':'https://navajowhite-cormorant-668337.hostingersite.com','N8N_API_KEY':'fixture-only'}),patch.object(ingress.urllib.request,'build_opener',return_value=Opener()),patch.object(ingress.time,'sleep'):
   code,result,key=ingress.submit('safe task','request-fixture-001','technical')
  self.assertEqual(code,202);self.assertEqual(len(seen),2);self.assertEqual(seen[0],seen[1]);self.assertEqual(json.loads(seen[0])['request_id'],key)
if __name__=='__main__':unittest.main()
