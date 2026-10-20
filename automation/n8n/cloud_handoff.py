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
    additional = continuation.get('production_revisions', [])
    if len({entry['workflow'] for entry in additional}) != len(additional):
        raise ValueError('Duplicate additional production revision')
    if additional and {entry['workflow'] for entry in additional} != {'W5', 'W8', 'W10'}:
        raise ValueError('Additional production revision inventory is incomplete or unexpected')
    followups = continuation.get('followup_revisions', [])
    if followups and (len(followups) != 3 or {r['workflow'] for r in followups} != {'My workflow','W5','W10'}):
        raise ValueError('Metricool follow-up revision inventory is incomplete or unexpected')
    provider = continuation.get('provider_readonly_revision')
    provider_names = set()
    if provider:
        from provider_readonly_verify import verify as verify_provider
        provider_names = set(verify_provider(root,provider)['workflows'])
    direct = continuation.get('direct_social_revision')
    direct_names = set()
    if direct:
        from direct_social_verify import verify as verify_direct
        direct_names = set(verify_direct(root,direct, {'My workflow':'revisions/provider-readonly-20261020/My workflow.before.json'} if provider else None)['workflows'])
    inbound = continuation.get('inbound_video_revision')
    inbound_names = set()
    if inbound:
        from inbound_video_verify import verify as verify_inbound
        inbound_targets = {'My workflow':'revisions/direct-social-20261020/My workflow.before.json'} if direct else {}
        if provider: inbound_targets['W10']='revisions/provider-readonly-20261020/W10.before.json'
        inbound_names = set(verify_inbound(root,inbound,inbound_targets or None)['workflows'])
    growth = continuation.get('growth_revision')
    growth_names = set()
    if growth:
        from growth_verify import verify as verify_growth
        growth_names = set(verify_growth(root, growth, {n:'revisions/inbound-video-20261020/'+n+'.before.json' for n in ['My workflow','W10']} if inbound else None)['workflows'])
    commercial = continuation.get('commercial_revision')
    commercial_names = set()
    if commercial:
        from commercial_verify import verify as verify_commercial
        commercial_names = set(verify_commercial(root, commercial)['workflows'])
    social = continuation.get('social_revision')
    if social:
        from social_verify import verify as verify_social
        verify_social(root, social, 'revisions/growth-20261020/My workflow.before.json' if growth else 'My workflow.json')
    management = continuation.get('management_revision')
    management_names = set()
    if management:
        from management_verify import verify as verify_management
        management_names = set(verify_management(root, management, 'revisions/social-20261019/My workflow.before.json' if social else 'My workflow.json')['workflows'])
    mcp = continuation.get('mcp_revision')
    if mcp:
        from mcp_verify import verify as verify_mcp
        verify_mcp(root, mcp, "revisions/provider-readonly-20261020/ChatGPT ingress.before.json" if provider else "ChatGPT ingress.json")
    ingress = continuation.get('ingress_revision')
    if ingress:
        from ingress_verify import verify as verify_ingress
        verify_ingress(root, ingress, 'revisions/mcp-20261019/ChatGPT ingress.before.json' if mcp else 'ChatGPT ingress.json', 'revisions/management-20261019/My workflow.before.json' if management else 'My workflow.json')
    agents = continuation.get('agents_revision')
    if agents:
        from agents_verify import verify
        verify(root, agents, 'revisions/ingress-20261019/My workflow.before.json' if ingress else 'My workflow.json')
    reports = []
    pending_count = 0
    deployed_count = 0
    identities = set()
    for name, record in sorted(manifest['workflows'].items()):
        blob = (root / (name + '.json')).read_bytes()
        if hashlib.sha256(blob).hexdigest() != record['public_sha256']:
            raise ValueError('A production snapshot changed without a matching handoff')
        workflow = json.loads(blob)
        if workflow['id'] != record['id'] or workflow['versionId'] != record['version_id'] or workflow['id'] in identities:
            raise ValueError('Workflow identity/version mismatch')
        identities.add(workflow['id'])
        historical = load(root / 'revisions/commercial-email-20261020' / (name + '.before.json')) if name in commercial_names else load(root / 'revisions/management-20261019' / (name + '.before.json')) if name in management_names else load(root / 'revisions/growth-20261020' / (name + '.before.json')) if name in growth_names else load(root / 'revisions/inbound-video-20261020' / (name+'.before.json')) if name in inbound_names else workflow
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
            if entry.get('status') == 'deployed':
                deployed_workflow = historical
                revision = entry.get('superseding_revision')
                if revision:
                    # Verify both immutable releases; never treat a newer version as permission to drift.
                    directory = root / 'revisions' / 'qualification-20261019'
                    if revision['path'] != 'revisions/qualification-20261019/' + name + '.patch.json':
                        raise ValueError('Unexpected superseding revision path')
                    before_blob = (directory / (name + '.before.json')).read_bytes()
                    revision_blob = (root / revision['path']).read_bytes()
                    if (hashlib.sha256(before_blob).hexdigest() != revision['before_sha256']
                            or hashlib.sha256(revision_blob).hexdigest() != revision['sha256']):
                        raise ValueError('Superseding revision provenance changed')
                    deployed_workflow = json.loads(before_blob)
                    revised = stage(deployed_workflow, json.loads(revision_blob))
                    if (revision['published_version_id'] != historical['versionId']
                            or any(revised.get(k) != historical.get(k) for k in ['id','name','nodes','connections','settings'])):
                        raise ValueError('Published workflow differs from its verified superseding revision')
                if entry.get('deployed_version_id') != deployed_workflow['versionId']:
                    raise ValueError('Deployed revision differs from the published baseline')
                nodes = {node['id']: node for node in deployed_workflow['nodes']}
                for change in patch['node_changes']:
                    if any(nodes.get(change['node_id'], {}).get('parameters', {}).get(k) != v for k, v in change['parameters'].items()):
                        raise ValueError('Published node differs from its deployed patch')
                for added in patch.get('add_nodes', []):
                    if nodes.get(added['id']) != added:
                        raise ValueError('Published added node differs from its deployed patch')
                for source, ports in patch.get('connection_changes', {}).items():
                    if deployed_workflow['connections'].get(source) != ports:
                        raise ValueError('Published graph differs from its deployed patch')
                deployed_count += 1
            else:
                candidate = stage(workflow, patch)
                pending_count += 1
        for entry in [r for r in additional if r['workflow'] == name]:
            directory = root / 'revisions' / 'windsor-20261019'
            if name not in {'W5', 'W8', 'W10'} or entry['path'] != 'revisions/windsor-20261019/' + name + '.patch.json':
                raise ValueError('Unexpected additional production revision')
            before_blob = (directory / (name + '.before.json')).read_bytes()
            patch_blob = (root / entry['path']).read_bytes()
            if (hashlib.sha256(before_blob).hexdigest() != entry['before_sha256']
                    or hashlib.sha256(patch_blob).hexdigest() != entry['sha256']):
                raise ValueError('Additional production revision provenance changed')
            revised = stage(json.loads(before_blob), json.loads(patch_blob))
            # A successor must retain the complete verified Windsor release as its pinned input.
            next_revision = next((r for r in followups if r['workflow'] == name), None)
            target = load(root / 'revisions/metricool-20261019' / (name + '.before.json')) if next_revision else workflow
            if (entry['published_version_id'] != target['versionId']
                    or any(revised.get(k) != target.get(k) for k in ['id','name','nodes','connections','settings'])):
                raise ValueError('Published workflow differs from additional production revision')
        for entry in [r for r in followups if r['workflow'] == name]:
            directory = root / 'revisions/metricool-20261019'
            if entry['path'] != 'revisions/metricool-20261019/' + name + '.patch.json':
                raise ValueError('Unexpected Metricool revision path')
            before_blob = (directory / (name + '.before.json')).read_bytes()
            patch_blob = (root / entry['path']).read_bytes()
            if (hashlib.sha256(before_blob).hexdigest() != entry['before_sha256']
                    or hashlib.sha256(patch_blob).hexdigest() != entry['sha256']):
                raise ValueError('Metricool revision provenance changed')
            revised = stage(json.loads(before_blob), json.loads(patch_blob))
            target = load(root / 'revisions/agents-20261019/My workflow.before.json') if agents and name == 'My workflow' else historical
            if (entry['published_version_id'] != target['versionId']
                    or any(revised.get(k) != target.get(k) for k in ['id','name','nodes','connections','settings'])):
                raise ValueError('Published workflow differs from Metricool revision')
        schedules = [interval['expression'] for node in workflow['nodes']
                     if node['type'] == 'n8n-nodes-base.scheduleTrigger'
                     for interval in node['parameters'].get('rule', {}).get('interval', [])
                     if interval.get('field') == 'cronExpression']
        reports.append({'workflow': name, 'id': workflow['id'], 'published_version_at_handoff': workflow['versionId'],
                        'last_recorded_active': record['last_verified_active'], 'current_live_state': 'not_verified',
                        'pending_patch': name in revisions and revisions[name].get('status') != 'deployed', 'baseline_nodes': len(workflow['nodes']),
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
    activation = load(root / 'activation.json') if (root / 'activation.json').exists() else None
    if activation and activation.get('latest_release') in {'windsor-release.json','metricool-release.json','agents-release.json','ingress-release.json','mcp-release.json','management-release.json','social-release.json','commercial-email-release.json','growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'} and len(additional) != 3:
        raise ValueError('Windsor publication evidence requires all three additional revisions')
    if activation and activation.get('latest_release') in {'metricool-release.json','agents-release.json','ingress-release.json','mcp-release.json','management-release.json','social-release.json','commercial-email-release.json','growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'} and len(followups) != 3:
        raise ValueError('Metricool publication evidence requires all three follow-up revisions')
    if activation and activation.get('latest_release') in {'agents-release.json','ingress-release.json','mcp-release.json','management-release.json','social-release.json','commercial-email-release.json','growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'} and not agents:
        raise ValueError('Agents release provenance is required')
    if activation and activation.get('latest_release') in {'ingress-release.json','mcp-release.json','management-release.json','social-release.json','commercial-email-release.json','growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'}:
        if not ingress:
            raise ValueError('Ingress release provenance is required')
        actual = load(root / 'ChatGPT ingress.json')
        recorded = activation.get('additional_ingress', {})
        if not recorded.get('active') or not recorded.get('published') or recorded.get('id') != actual['id'] or recorded.get('version_id') != actual['versionId'] or recorded.get('active_version_id') != actual['versionId']:
            raise ValueError('Ingress publication evidence differs from its export')
    if activation and activation.get('latest_release') in {'mcp-release.json','management-release.json','social-release.json','commercial-email-release.json','growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'}:
        if not mcp:
            raise ValueError('MCP publication provenance is required')
        actual = load(root / 'Codex MCP.json')
        recorded = activation.get('additional_mcp', {})
        if not recorded.get('active') or not recorded.get('published') or recorded.get('id') != actual['id'] or recorded.get('version_id') != actual['versionId'] or recorded.get('active_version_id') != actual['versionId']:
            raise ValueError('MCP publication evidence differs from its export')
    if activation and activation.get('latest_release') == 'management-release.json' and not management:
        raise ValueError('Management publication provenance is required')
    if activation and activation.get('latest_release') == 'social-release.json' and (not social or not management):
        raise ValueError('Social safety successor requires verified social and management provenance')
    if activation and activation.get('latest_release') == 'commercial-email-release.json' and (not commercial or not social or not management):
        raise ValueError('Commercial publication requires the full verified predecessor chain')
    if activation and activation.get('latest_release') in {'growth-release.json','inbound-video-release.json','direct-social-release.json','provider-readonly-release.json'} and (not growth or not commercial or not social or not management):
        raise ValueError('Growth successor requires the full verified predecessor chain')
    if activation and activation.get('latest_release') == 'provider-readonly-release.json' and (not provider or not direct or not inbound or not mcp):
        raise ValueError('Provider successor requires verified provider/direct/inbound/MCP provenance')
    published = bool(activation and activation.get('result') == 'LIVE' and deployed_count == len(PATCHED))
    if published:
        for entry in reports:
            recorded = activation['workflows'][entry['workflow']]
            if (not recorded.get('active') or not recorded.get('published')
                    or recorded['id'] != entry['id'] or recorded['version_id'] != entry['published_version_at_handoff']
                    or recorded['active_version_id'] != recorded['version_id']):
                raise ValueError('Publication evidence differs from the baseline')
            entry['last_verified_live_state'] = 'Published/Active at activation capture'
    return {'mode': 'offline_only', 'handoff_status': 'complete_for_cloud_continuation',
            'live_deployment': 'published_verified_at_capture' if published else 'pending_api_access_and_runtime_validation',
            'workflow_count': len(reports), 'pending_patch_count': pending_count,
            'reviewed_patch_count': len(revisions), 'deployed_patch_count': deployed_count,
            'additional_verified_production_revisions': len(additional),
            'metricool_verified_followup_revisions': len(followups),
            'additional_ingress_verified': bool(ingress),
            'additional_mcp_published_verified': bool(mcp),
            'management_revisions_verified': len(management_names),
            'social_safety_revision_verified': bool(social),
            'commercial_email_revisions_verified': len(commercial_names),
            'growth_revisions_verified': len(growth_names),
            'inbound_video_revisions_verified': len(inbound_names),
            'direct_social_revisions_verified': len(direct_names),
            'provider_readonly_revisions_verified': len(provider_names),
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
    print('OFFLINE_HANDOFF_OK: workflows=' + str(report['workflow_count']) + '; reviewed_patches=' + str(report['reviewed_patch_count'])
          + '; pending_patches=' + str(report['pending_patch_count']) + '; deployment=' + report['live_deployment']
          + '. No live execution. Mac not required for Cloud continuation.')


if __name__ == '__main__':
    main()
