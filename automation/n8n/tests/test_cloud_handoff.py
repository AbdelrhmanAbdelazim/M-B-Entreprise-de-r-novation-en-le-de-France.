"""New Cloud-only continuation/connection tests; never use a live transport."""
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cloud_handoff import collect
from live_status import HOST, NoRedirect, ProbeBlocked, compare, inventory

BASE = 'https://' + HOST
TEST_KEY = 'synthetic-auth-fixture-not-a-real-key'


class Transport:
    def __init__(self, pages):
        self.pages = iter(pages)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        result = next(self.pages)
        if isinstance(result, Exception):
            raise result
        return io.BytesIO(json.dumps(result).encode())


def entry(identity, name='Synthetic workflow', active=True):
    return {'id': identity, 'name': name, 'active': active}


class ReadOnlyProbeTests(unittest.TestCase):
    def test_successful_paginated_get_returns_only_inventory_metadata(self):
        first = entry('first'); first['privateExecutionData'] = 'do-not-retain'
        transport = Transport([{'data': [first], 'nextCursor': 'next cursor/?'}, {'data': [entry('second', active=False)]}])
        result = inventory(BASE, TEST_KEY, transport)
        self.assertEqual(len(result), 2)
        self.assertFalse(result[1]['active'])
        self.assertNotIn('privateExecutionData', result[0])
        for request, timeout in transport.requests:
            self.assertEqual(request.get_method(), 'GET')
            self.assertTrue(request.full_url.startswith(BASE + '/api/v1/workflows?'))
            self.assertIsNone(request.data)
            self.assertLessEqual(timeout, 20)
            self.assertEqual(request.get_header('X-n8n-api-key'), TEST_KEY)
        self.assertIn('cursor=next+cursor%2F%3F', transport.requests[1][0].full_url)

    def test_no_redirect_can_forward_the_api_key(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.invalid'))

    def test_rejects_untrusted_origin_and_missing_binding_before_any_request(self):
        for base in ['http://' + HOST, 'https://other.invalid', BASE + '/webhook', 'https://user@' + HOST, BASE + '?token=fixture']:
            with self.assertRaises(ProbeBlocked): inventory(base, TEST_KEY, Transport([]))
        with self.assertRaisesRegex(ProbeBlocked, 'N8N_API_KEY'):
            inventory(BASE, '', Transport([]))

    def test_timeout_is_a_blocker_without_retry(self):
        transport = Transport([TimeoutError('private transport context ' + TEST_KEY)])
        with self.assertRaisesRegex(ProbeBlocked, '^n8n API timeout$'):
            inventory(BASE, TEST_KEY, transport)
        self.assertEqual(len(transport.requests), 1)

    def test_401_response_does_not_leak_secret_or_response_body(self):
        exc = urllib.error.HTTPError(BASE + '?private=' + TEST_KEY, 401, TEST_KEY, {}, io.BytesIO(TEST_KEY.encode()))
        with self.assertRaises(ProbeBlocked) as caught:
            inventory(BASE, TEST_KEY, Transport([exc]))
        self.assertIn('401', str(caught.exception))
        self.assertNotIn(TEST_KEY, str(caught.exception))

    def test_proxy_denial_is_distinct_from_origin_authentication(self):
        exc = urllib.error.URLError(OSError('Tunnel connection failed: 403 Forbidden'))
        with self.assertRaisesRegex(ProbeBlocked, 'proxy CONNECT 403'):
            inventory(BASE, TEST_KEY, Transport([exc]))

    def test_missing_states_and_duplicate_ids_are_not_reported_connected(self):
        for rows in [[{'id': 'x', 'name': 'unknown state'}], [entry('x'), entry('x')]]:
            with self.assertRaises(ProbeBlocked): inventory(BASE, TEST_KEY, Transport([{'data': rows}]))

    def test_repeated_cursor_and_page_cap_are_blockers_not_partial_success(self):
        with self.assertRaisesRegex(ProbeBlocked, 'repeated'):
            inventory(BASE, TEST_KEY, Transport([{'data': [], 'nextCursor': 'same'}, {'data': [], 'nextCursor': 'same'}]))
        with self.assertRaisesRegex(ProbeBlocked, 'page limit'):
            inventory(BASE, TEST_KEY, Transport([{'data': [], 'nextCursor': 'more'}]), max_pages=1)

    def test_exact_identity_comparison_detects_renames_state_changes_and_missing_workflows(self):
        manifest = {'workflows': {'W0': {'id': 'zero', 'name': 'Original W0', 'last_verified_active': True},
                                  'W1': {'id': 'one', 'name': 'Original W1', 'last_verified_active': True}}}
        result = compare([entry('zero', 'Renamed W0', False), entry('extra')], manifest)
        self.assertEqual(result['matched_ids'], 1)
        self.assertEqual(result['extra_count'], 1)
        self.assertEqual({d['difference'] for d in result['differences']}, {'missing_from_api', 'name_changed', 'active_changed'})


class OfflineAssemblyTests(unittest.TestCase):
    def copy_bundle(self, target):
        for name in ['social-publishing.js', 'management.js', 'qualification.js', 'Codex MCP.json', 'ChatGPT ingress.json', 'manifest.json', 'continuation.json', 'data-tables.json', 'My workflow.json', 'activation.json'] + [f'W{i}.json' for i in range(11)]:
            shutil.copyfile(ROOT / name, target / name)
        (target / 'pending').mkdir()
        for source in (ROOT / 'pending').glob('*.patch.json'):
            shutil.copyfile(source, target / 'pending' / source.name)
        shutil.copytree(ROOT / 'revisions', target / 'revisions')

    def test_full_twelve_workflow_six_patch_assembly_needs_no_mac_or_credentials(self):
        report = collect(ROOT)
        self.assertEqual(report['workflow_count'], 12)
        self.assertEqual(report['pending_patch_count'], 0)
        self.assertEqual(report['deployed_patch_count'], 6)
        self.assertEqual(len(report['existing_tables']), 5)
        self.assertFalse(report['mac_required_for_continuation'])
        self.assertFalse(report['workflow_execution_performed'])
        self.assertEqual(report['live_deployment'], 'published_verified_at_capture')
        self.assertTrue(all(w['current_live_state'] == 'not_verified' for w in report['workflows']))

    def test_resume_is_portable_to_a_different_checkout_path(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.copy_bundle(target)
            report = collect(target)
            self.assertEqual(report['workflow_count'], 12)
            self.assertEqual(next(w for w in report['workflows'] if w['workflow'] == 'W7')['retained_cron'], ['10 6,10,14,18 * * *'])

    def test_changed_patch_checksum_prevents_unreviewed_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory); self.copy_bundle(target)
            patch = target / 'pending/W3.patch.json'
            patch.write_text(patch.read_text() + '\n')
            with self.assertRaisesRegex(ValueError, 'checksum'): collect(target)

    def test_incomplete_revision_inventory_is_not_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory); self.copy_bundle(target)
            path = target / 'continuation.json'; data = json.loads(path.read_text())
            data['pending_revisions'].pop(); path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'six-workflow'): collect(target)


if __name__ == '__main__':
    unittest.main()
