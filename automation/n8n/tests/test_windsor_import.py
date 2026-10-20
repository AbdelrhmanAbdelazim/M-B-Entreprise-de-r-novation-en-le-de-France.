import copy
import datetime as dt
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from windsor_import import prepare, apply
NOW=dt.datetime(2026,10,19,10,tzinfo=dt.timezone.utc)
SAMPLE={'schema':'mb.windsor.v1','channel':'search_console','account':'maison-mb.fr','period_start':'2026-09-20','period_end':'2026-10-18','captured_at':'2026-10-19T09:00:00Z','metrics':{'clicks':20,'impressions':1000,'position':8}}
class WindsorImportTests(unittest.TestCase):
 def test_deterministic_snapshot_identity_is_separate_from_contact_actions(self):
  a=prepare(SAMPLE,NOW);b=prepare({**SAMPLE,'metrics':{'clicks':22}},NOW)
  self.assertEqual(a['task_key'],b['task_key']);self.assertTrue(a['task_key'].startswith('analytics:windsor:search_console:'))
  self.assertEqual(a['type'],'analytics_snapshot');self.assertEqual(a['source'],'Windsor.ai');self.assertEqual(a['status'],'done')
 def test_explicit_channel_and_metric_contract_rejects_unauthorized_or_unknown_fields(self):
  for p in [{**SAMPLE,'api_key':'never-store'},{**SAMPLE,'channel':'ad_campaign_create'},{**SAMPLE,'metrics':{'budget':20}},{**SAMPLE,'metrics':{'clicks':True}},{**SAMPLE,'metrics':{'clicks':-1}},{**SAMPLE,'metrics':{'clicks':float('nan')}}]:
   with self.assertRaises(ValueError):prepare(p,NOW)
 def test_stale_future_invalid_dates_and_unzoned_capture_are_rejected(self):
  for change in [{'period_start':'20260920'},{'captured_at':'20261019T090000Z'},{'period_start':'2026-10-20'},{'period_end':'2026-99-99'},{'captured_at':'2026-10-19T11:00:00Z'},{'captured_at':'2026-10-19T09:00:00'},{'captured_at':'2026-10-10T09:00:00Z'}]:
   with self.assertRaises(ValueError):prepare({**SAMPLE,**change},NOW)
 def test_no_secrets_contact_data_or_third_party_fetch_targets_are_imported(self):
  for change in [{'account':'Bearer private'},{'pages':[{'url':'http://169.254.169.254/','clicks':20}]},{'pages':[{'url':'https://www.maison-mb.fr.evil.invalid/','clicks':20}]},{'posts':[{'title':'customer@invalid.test'}]}]:
   with self.assertRaises(ValueError):prepare({**SAMPLE,**change},NOW)
 def test_ad_cost_is_historical_reporting_and_requires_currency(self):
  payload={**SAMPLE,'channel':'meta_ads','metrics':{'cost':12}}
  with self.assertRaises(ValueError):prepare(payload,NOW)
  self.assertEqual(json.loads(prepare({**payload,'currency':'EUR'},NOW)['payload'])['metrics']['cost'],12)
 def fake_apply(self,old=None):
  store=[] if old is None else [copy.deepcopy(old)];requests=[]
  class Opener:
   def open(self,request,timeout):
    requests.append((request.method,request.full_url))
    if request.method=='GET':return io.BytesIO(json.dumps({'data':store,'nextCursor':None}).encode())
    self_body=json.loads(request.data);store[:]=[{'id':9001,**self_body['data']}];return io.BytesIO(json.dumps(store).encode())
  env={'N8N_BASE_URL':'https://navajowhite-cormorant-668337.hostingersite.com','N8N_API_KEY':'synthetic-key'}
  with patch.dict('os.environ',env),patch('urllib.request.build_opener',return_value=Opener()):result=apply(prepare(SAMPLE,NOW))
  return result,requests,store
 def test_only_existing_queue_is_written_and_response_is_independently_read_back(self):
  result,requests,store=self.fake_apply();self.assertEqual(result,'upserted_and_readback_verified');self.assertEqual([x[0] for x in requests],['GET','POST','GET'])
  self.assertTrue(all('/api/v1/data-tables/aqPFAT3TBwLGhlIj/rows' in path for _,path in requests));self.assertFalse(any('/workflows/' in path or '/credentials' in path for _,path in requests))
 def test_identical_data_is_noop_and_original_creation_date_is_preserved(self):
  old=prepare(SAMPLE,NOW);result,requests,_=self.fake_apply(old);self.assertEqual(result,'unchanged');self.assertEqual(len(requests),1)
  older={**old,'created_at':'2026-10-18T00:00:00Z','payload':json.dumps({**SAMPLE,'captured_at':'2026-10-18T09:00:00Z'})};_,_,store=self.fake_apply(older);self.assertEqual(store[0]['created_at'],older['created_at'])
 def test_newer_live_data_must_not_be_overwritten(self):
  old=prepare({**SAMPLE,'captured_at':'2026-10-19T09:30:00Z'},NOW)
  with self.assertRaisesRegex(ValueError,'Older export'):self.fake_apply(old)
if __name__=='__main__':unittest.main()
