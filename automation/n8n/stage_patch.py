"""Prepare a local workflow candidate; never contact n8n or deploy redacted exports."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path

from sanitize import sanitize
from validate import check_document

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def stage(document, patch):
    """Apply only reviewed node/code/edge deltas, preserving fresh private bindings."""
    if patch.get('format_version') != 1:
        raise ValueError('Unsupported patch format')
    if document.get('id') != patch['workflow_id'] or document.get('versionId') != patch['base_version_id']:
        raise ValueError('Workflow ID/version changed: inspect fresh live state and rebase the patch')
    clean, _ = sanitize(document)
    check_document(clean)
    if digest(clean['connections']) != patch['expected_graph_sha256']:
        raise ValueError('Workflow graph changed: do not overwrite newer work')
    result = copy.deepcopy(document)
    original = {n['id']: n for n in clean['nodes']}
    targets = {n['id']: n for n in result['nodes']}
    changed_ids = set()
    for change in patch['node_changes']:
        node_id = change['node_id']
        if node_id in changed_ids or node_id not in original:
            raise ValueError('Duplicate or missing patch target')
        changed_ids.add(node_id)
        if digest(original[node_id]) != change['expected_node_sha256']:
            raise ValueError('Target node changed: inspect before rebasing')
        if set(change['parameters']) != {'jsCode'} or targets[node_id]['type'] != 'n8n-nodes-base.code':
            raise ValueError('Patch may change only reviewed Code parameters')
        targets[node_id]['parameters'].update(change['parameters'])
    names = {n['name'] for n in result['nodes']}
    for node in patch.get('add_nodes', []):
        if node['id'] in targets or node['name'] in names:
            raise ValueError('New node ID/name already exists')
        if node.get('credentials'):
            raise ValueError('New nodes must not create credential bindings')
        if node['type'] == 'n8n-nodes-base.dataTable':
            table = node['parameters']['dataTableId']['value']
            operation = node['parameters'].get('operation')
            if (operation, table) not in [('get', 'NE0QU8afBFipimhW'), ('upsert', 'aqPFAT3TBwLGhlIj')]:
                raise ValueError('Only existing Blacklist reads and Growth Queue reservations are permitted')
        elif node['type'] != 'n8n-nodes-base.code':
            raise ValueError('Only local Code and existing-table nodes may be added')
        result['nodes'].append(copy.deepcopy(node))
        targets[node['id']] = node
        names.add(node['name'])
    result['connections'].update(copy.deepcopy(patch.get('connection_changes', {})))
    sanitized, _ = sanitize(result)
    check_document(sanitized)
    # Keep the original version as a precondition, not a claim of publication.
    # IDs, credentials, webhooks, settings, activation state and schedules are unchanged.
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workflow', choices=['W2', 'W3', 'W4', 'W6', 'W7', 'W9'], required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    private = ROOT / 'private-live'
    if private not in out.parents:
        parser.error('Output must stay under ignored automation/n8n/private-live; never overwrite public snapshots')
    try:
        patch = json.loads((ROOT / 'pending' / (args.workflow + '.patch.json')).read_text())
        document = json.loads(args.snapshot.read_text())
        result = stage(document, patch)
        out.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
    except (OSError, ValueError, KeyError, AssertionError):
        parser.exit(1, 'Staging refused: inspect identity, version, node/graph drift and output path. No n8n changes made.\n')
    print('Local candidate staged only; not deployed. Preserve fresh bindings and inspect before any live write. Redacted input remains non-deployable.')


if __name__ == '__main__':
    main()
