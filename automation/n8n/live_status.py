"""Bounded GET-only n8n inventory probe. Never execute workflows or print credentials."""
import argparse
import datetime
import json
import os
from pathlib import Path
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
HOST = 'navajowhite-cormorant-668337.hostingersite.com'
MAX_BYTES = 2 * 1024 * 1024


class ProbeBlocked(Exception):
    """Safe diagnostic text only, without response bodies or headers."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def origin(base):
    try:
        u = urllib.parse.urlsplit(base)
        valid = (u.scheme == 'https' and u.hostname == HOST and u.port in (None, 443)
                 and not (u.username or u.password or u.path or u.query or u.fragment))
    except ValueError:
        valid = False
    if not valid:
        raise ProbeBlocked('N8N_BASE_URL must be the documented HTTPS origin, without paths or credentials')
    return base


def inventory(base, key, opener=None, timeout=20, max_pages=20):
    origin(base)
    if not key:
        raise ProbeBlocked('N8N_API_KEY is not available in the Cloud runtime; use the existing secure binding')
    if not 0 < timeout <= 30 or not 0 < max_pages <= 20:
        raise ProbeBlocked('Probe limits exceeded')
    if opener is None:
        opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    rows = []
    cursors = set()
    ids = set()
    cursor = None
    deadline = time.monotonic() + 60
    for _ in range(max_pages):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProbeBlocked('n8n inventory exceeded its 60-second total request budget')
        query = {'limit': 100}
        if cursor:
            query['cursor'] = cursor
        request = urllib.request.Request(base + '/api/v1/workflows?' + urllib.parse.urlencode(query),
                                         headers={'Accept': 'application/json', 'X-N8N-API-KEY': key}, method='GET')
        try:
            with opener.open(request, timeout=min(timeout, remaining)) as response:
                blob = response.read(MAX_BYTES + 1)
                if len(blob) > MAX_BYTES:
                    raise ProbeBlocked('Workflow-list response exceeded the safe size limit')
                data = json.loads(blob)
        except urllib.error.HTTPError as exc:
            reason = {401: 'authentication not accepted; verify the existing binding and its API permissions',
                      403: 'access denied; verify proxy/host authorization',
                      429: 'API rate limit; no automatic retry'}.get(exc.code, 'API response unsuccessful')
            raise ProbeBlocked('n8n API HTTP ' + str(exc.code) + ': ' + reason) from None
        except urllib.error.URLError as exc:
            if 'Tunnel connection failed: 403' in str(exc.reason):
                reason = 'proxy CONNECT 403 before reaching the n8n origin'
            elif isinstance(exc.reason, TimeoutError):
                reason = 'n8n API timeout'
            elif isinstance(exc.reason, ssl.SSLError):
                reason = 'TLS trust/handshake failed; verification remains enabled'
            else:
                reason = 'network connection failed'
            raise ProbeBlocked(reason) from None
        except TimeoutError:
            raise ProbeBlocked('n8n API timeout') from None
        except ssl.SSLError:
            raise ProbeBlocked('TLS trust/handshake failed; verification remains enabled') from None
        except (ValueError, UnicodeError):
            raise ProbeBlocked('n8n API returned invalid JSON') from None
        if not isinstance(data, dict) or not isinstance(data.get('data'), list):
            raise ProbeBlocked('n8n API returned an unexpected inventory schema')
        for entry in data['data']:
            if (not isinstance(entry, dict) or not isinstance(entry.get('id'), str)
                    or not entry['id'] or not isinstance(entry.get('name'), str)
                    or not isinstance(entry.get('active'), bool)):
                raise ProbeBlocked('Workflow identity/name/active state unavailable')
            if entry['id'] in ids:
                raise ProbeBlocked('Duplicate workflow ID in paginated inventory; incomplete comparison')
            ids.add(entry['id'])
            rows.append({field: entry[field] for field in ['id', 'name', 'active']})
        cursor = data.get('nextCursor')
        if not cursor:
            return rows
        if not isinstance(cursor, str) or cursor in cursors:
            raise ProbeBlocked('Invalid or repeated inventory pagination cursor')
        cursors.add(cursor)
    raise ProbeBlocked('Inventory exceeds page limit; no partial success reported')


def compare(rows, manifest):
    actual = {row['id']: row for row in rows}
    expected = manifest['workflows']
    differences = []
    for label, record in expected.items():
        live = actual.get(record['id'])
        if live is None:
            differences.append({'workflow': label, 'difference': 'missing_from_api'})
            continue
        if live['name'] != record['name']:
            differences.append({'workflow': label, 'difference': 'name_changed'})
        if live['active'] != record['last_verified_active']:
            differences.append({'workflow': label, 'difference': 'active_changed', 'active': live['active']})
    expected_ids = {record['id'] for record in expected.values()}
    return {'workflow_count': len(rows), 'expected_count': len(expected),
            'matched_ids': len(expected_ids & actual.keys()), 'extra_count': len(actual.keys() - expected_ids),
            'differences': differences}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout', type=float, default=20)
    parser.add_argument('--out', type=Path, help='Optional metadata-only report under ignored private-live')
    args = parser.parse_args()
    if args.out and (ROOT / 'private-live') not in args.out.resolve().parents:
        parser.error('Reports must remain in ignored automation/n8n/private-live')
    base = os.environ.get('N8N_BASE_URL', '').rstrip('/')
    key = os.environ.get('N8N_API_KEY', '')
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'mode': 'GET only',
              'environment': {'N8N_BASE_URL_present': bool(base), 'N8N_API_KEY_present': bool(key)}}
    try:
        rows = inventory(base, key, timeout=args.timeout)
        manifest = json.loads((ROOT / 'manifest.json').read_text())
        report.update(result='CONNECTED', comparison=compare(rows, manifest))
    except ProbeBlocked as exc:
        report.update(result='BLOCKED', reason=str(exc))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    if report['result'] == 'CONNECTED':
        c = report['comparison']
        print('CONNECTED: workflows=' + str(c['workflow_count']) + '; expected_matched=' + str(c['matched_ids'])
              + '; differences=' + str(len(c['differences'])) + '; extra=' + str(c['extra_count']))
    else:
        print('BLOCKED: ' + report['reason'])
    return 0 if report['result'] == 'CONNECTED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
