"""Validate a normalized Windsor export; optionally upsert analytics only into existing Growth Queue.

No provider API, advertising, publishing, workflow execution or credentials endpoint is used.
This bridge does not establish an automatic Windsor connection. Default: offline validation.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import ssl
import urllib.parse
import urllib.request

from live_status import NoRedirect, origin

TABLE = 'aqPFAT3TBwLGhlIj'
METRICS = {
    'search_console': {'clicks', 'impressions', 'position'},
    'ga4': {'sessions', 'users', 'key_events'},
    'gbp': {'impressions', 'website_clicks', 'calls', 'directions'},
    'google_ads': {'impressions', 'clicks', 'cost', 'conversions'},
    'meta_ads': {'impressions', 'clicks', 'cost', 'conversions'},
    'instagram': {'reach', 'impressions', 'engagements', 'profile_views'},
}
SECRET = re.compile(r'api[_-]?key|access[_-]?token|bearer\s|sk-(?:proj|ant)-|[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', re.I)


def prepare(payload, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    allowed = {'schema', 'channel', 'account', 'period_start', 'period_end', 'captured_at', 'metrics', 'currency', 'pages', 'posts'}
    if not isinstance(payload, dict) or set(payload) - allowed or payload.get('schema') != 'mb.windsor.v1':
        raise ValueError('Unsupported normalized export contract')
    channel = payload.get('channel')
    if channel not in METRICS:
        raise ValueError('Unsupported channel')
    account = payload.get('account')
    if not isinstance(account, str) or not account or len(account) > 120 or SECRET.search(account):
        raise ValueError('Non-secret selected account label required')
    try:
        if any(not isinstance(payload.get(k), str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', payload[k]) for k in ['period_start','period_end']):
            raise ValueError('ISO date required')
        if not isinstance(payload.get('captured_at'), str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', payload['captured_at']):
            raise ValueError('Zoned ISO timestamp required')
        start, end = (dt.date.fromisoformat(payload[k]) for k in ['period_start', 'period_end'])
        captured = dt.datetime.fromisoformat(payload['captured_at'].replace('Z', '+00:00'))
        if captured.tzinfo is None:
            raise ValueError('Timezone required')
    except (KeyError, ValueError, TypeError, AttributeError):
        raise ValueError('Invalid reporting window/capture timestamp') from None
    if start > end or end > now.date() or captured > now or now-captured > dt.timedelta(hours=72) or now.date()-end > dt.timedelta(days=8):
        raise ValueError('Future or stale data cannot be imported')
    def numeric(value):
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    values = payload.get('metrics')
    if not isinstance(values, dict) or not values or set(values) - METRICS[channel] or not all(numeric(v) for v in values.values()):
        raise ValueError('Unknown, negative, nonnumeric or missing metrics; map actual Windsor fields explicitly')
    if 'cost' in values and not re.fullmatch('[A-Z]{3}', payload.get('currency', '')):
        raise ValueError('Historical spend requires its actual currency')
    for group, limit, keys in [('pages', 100, {'url','clicks','impressions','position','sessions','key_events'}), ('posts', 30, {'title','reach','impressions','engagements','clicks'})]:
        rows = payload.get(group, [])
        if not isinstance(rows, list) or len(rows) > limit:
            raise ValueError('Dimension row limit exceeded')
        for row in rows:
            if not isinstance(row, dict) or set(row) - keys or not all(numeric(v) for k,v in row.items() if k not in ['url','title']):
                raise ValueError('Invalid dimension contract')
            if group == 'pages' and not re.fullmatch(r'https://(?:www\.)?maison-mb\.fr(?:/[^\s?#]*)?', row.get('url', '')):
                raise ValueError('Only existing first-party page URLs without query or fragment are accepted')
            if group == 'posts' and (not isinstance(row.get('title'), str) or not row['title'] or len(row['title']) > 160 or SECRET.search(row['title'])):
                raise ValueError('Post title must be bounded and contain no contact/authentication data')
    # Deterministic identity: same account/window replaces a snapshot, never sums overlapping reports.
    identity = hashlib.sha256(account.encode()).hexdigest()[:16]
    key = 'analytics:windsor:' + channel + ':' + identity + ':' + str(start) + ':' + str(end)
    stamp = now.isoformat()
    return {'task_key':key,'type':'analytics_snapshot','priority':'WARM','source':'Windsor.ai','owner':'W5','status':'done',
            'created_at':stamp,'last_action':stamp,'next_action':'Read-only analytics for W5/W8/W10; no publishing or ad changes',
            'due_at':stamp,'payload':json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))}


def apply(row):
    base = origin(os.environ['N8N_BASE_URL'].rstrip('/'))
    opener = urllib.request.build_opener(NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    def request(path, body=None):
        headers = {'X-N8N-API-KEY':os.environ['N8N_API_KEY'],'Accept':'application/json'}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(base+'/api/v1'+path,headers=headers,data=None if body is None else json.dumps(body).encode(),method='GET' if body is None else 'POST')
        with opener.open(req,timeout=25) as response:
            return json.load(response)
    filt = {'type':'and','filters':[{'columnName':'task_key','condition':'eq','value':row['task_key']}]}
    path = '/data-tables/'+TABLE+'/rows'
    previous = request(path+'?'+urllib.parse.urlencode({'limit':100,'filter':json.dumps(filt)}))
    if previous.get('nextCursor') or len(previous['data']) > 1:
        raise ValueError('Conflicting snapshot rows; inspect without overwriting')
    if previous['data']:
        old = previous['data'][0]
        if old.get('type') != 'analytics_snapshot' or old.get('source') != 'Windsor.ai':
            raise ValueError('Existing row identity conflict')
        oldp, newp = json.loads(old['payload']), json.loads(row['payload'])
        if oldp == newp:
            return 'unchanged'
        if dt.datetime.fromisoformat(oldp['captured_at'].replace('Z','+00:00')) > dt.datetime.fromisoformat(newp['captured_at'].replace('Z','+00:00')):
            raise ValueError('Older export must not replace newer data')
        row['created_at'] = old['created_at']
    # Never blindly retry a timed-out write. Next invocation reads before considering another write.
    result = request(path+'/upsert', {'filter':filt,'data':row,'returnData':True})
    verified = request(path+'?'+urllib.parse.urlencode({'limit':100,'filter':json.dumps(filt)}))
    if not isinstance(result,list) or len(result)!=1 or len(verified['data'])!=1 or any(verified['data'][0].get(k)!=v for k,v in row.items()):
        raise ValueError('Snapshot write requires inspection; no automatic retry')
    return 'upserted_and_readback_verified'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True,help='Private normalized JSON export; never an API key or authenticated URL')
    parser.add_argument('--apply',action='store_true',help='Write only the validated analytics snapshot to existing Growth Queue')
    args = parser.parse_args()
    try:
        row = prepare(json.loads(args.input.read_text()))
        result = apply(row) if args.apply else 'offline_valid_no_write'
    except Exception as exc:
        # Network errors can contain request URLs; never print provider bodies or secret-bearing text.
        parser.exit(1,'Windsor import stopped: '+type(exc).__name__+'; no automatic retry. Inspect private input and connection configuration.\n')
    print('WINDSOR_IMPORT: '+result+'; channel='+json.loads(row['payload'])['channel'])


if __name__ == '__main__':
    main()
