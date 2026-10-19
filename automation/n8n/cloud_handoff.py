"""Offline Cloud handoff assembly: no network, workflow execution or live deployment."""
import argparse
import hashlib
import json
from pathlib import Path

from stage_patch import stage

ROOT = Path(__file__).resolve().parent
EXPECTED = {f'W{i}' for i in range(11)} | {'My workflow'}
PATCHED = {'W2', 'W3', 'W4', 'W6', 'W7', 'W9'}


def load(path):
    return json.loads(path.read_text())


def collect(root=ROOT):
    manifest = load(root / 'manifest.json')
    continuation = load(root / 'continuation.json')
    if set(manifest['workflows']) != EXPECTED:
        raise ValueError('The twelve-workflow production handoff is incomplete')
    revisions = {entry['workflow']: entry for entry in continuation['pending_revisions']}
    if set(revisions) != PATCHED or len(continuation['pending_revisions']) != len(PATCHED):
        raise ValueError('Pending revision inventory differs from the reviewed six-workflow handoff')
    reports = []
    identities = set()
    for name, record in sorted(manifest['workflows'].items()):
        blob = (root / (name + '.json')).read_bytes()
        if hashlib.sha256(blob).hexdigest() != record['public_sha256']:
            raise ValueError('A production snapshot changed without a matching handoff')
        workflow = json.loads(blob)
        if workflow['id'] != record['id'] or workflow['versionId'] != record['version_id'] or workflow['id'] in identities:
            raise ValueError('Workflow identity/version mismatch')
        identities.add(workflow['id'])
        candidate = workflow
        if name in revisions:
            entry = revisions[name]
            expected_path = 'pending/' + name + '.patch.json'
            if entry['path'] != expected_path:
                raise ValueError('Pending revision path differs from its reviewed location')
            patch_blob = (root / expected_path).read_bytes()
            if hashlib.sha256(patch_blob).hexdigest() != entry['sha256']:
                raise ValueError('Pending patch checksum changed; preserve the latest reviewed revision')
            patch = json.loads(patch_blob)
            if patch['workflow_name'] != name or entry['workflow_id'] != record['id']:
                raise ValueError('Pending patch is assigned to a different workflow')
            candidate = stage(workflow, patch)
        schedules = [interval['expression'] for node in workflow['nodes']
                     if node['type'] == 'n8n-nodes-base.scheduleTrigger'
                     for interval in node['parameters'].get('rule', {}).get('interval', [])
                     if interval.get('field') == 'cronExpression']
        reports.append({'workflow': name, 'id': workflow['id'], 'published_version_at_handoff': workflow['versionId'],
                        'last_recorded_active': record['last_verified_active'], 'current_live_state': 'not_verified',
                        'pending_patch': name in revisions, 'baseline_nodes': len(workflow['nodes']),
                        'candidate_nodes': len(candidate['nodes']), 'timezone': workflow['settings'].get('timezone'),
                        'retained_cron': schedules})
    tables = load(root / 'data-tables.json')['tables']
    table_ids = {table['id'] for table in tables}
    if len(table_ids) != len(tables):
        raise ValueError('Duplicate central table IDs in the handoff')
    for name in EXPECTED:
        workflow = load(root / (name + '.json'))
        for node in workflow['nodes']:
            reference = node['parameters'].get('dataTableId')
            if isinstance(reference, dict) and reference.get('value') not in table_ids:
                raise ValueError('Workflow references a table absent from the central-table handoff')
    return {'mode': 'offline_only', 'handoff_status': 'complete_for_cloud_continuation',
            'live_deployment': 'pending_api_access_and_runtime_validation',
            'workflow_count': len(reports), 'pending_patch_count': len(revisions),
            'baseline_and_patch_provenance': 'verified_for_local_assembly',
            'mac_required_for_continuation': False, 'workflow_execution_performed': False,
            'old_business_tests_repeated': False, 'workflows': reports,
            'existing_tables': [{'name': table['name'], 'id': table['id']} for table in tables],
            'next_step': 'Use live_status.py for GET-only API comparison when access returns; never deploy sanitized exports'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='Optional metadata-only JSON report')
    args = parser.parse_args()
    try:
        report = collect()
    except (ValueError, KeyError, AssertionError, OSError):
        parser.exit(1, 'Offline handoff incomplete or changed; inspect source/patch provenance. No live action performed.\n')
    if args.out:
        with args.out.open('x') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    print('OFFLINE_HANDOFF_OK: 12 existing workflow identities; 6 reviewed patch assemblies; 5 existing tables. No live execution. Mac not required for Cloud continuation.')


if __name__ == '__main__':
    main()
