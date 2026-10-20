"""New offline patch guard tests; no workflow/provider/network execution."""
import copy
import json
from pathlib import Path
import sys
import unittest
import subprocess

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stage_patch import stage


class StagePatchTests(unittest.TestCase):
    def setUp(self):
        self.documents = {name: json.loads(subprocess.check_output(['git', 'show', '883e99b9a859fef687f5ffe997e999328c43e384:automation/n8n/' + name + '.json'], cwd=ROOT.parents[1], text=True)) for name in ['W2', 'W3', 'W4', 'W6', 'W7', 'W9']}  # Immutable pre-activation fixtures, never used for live deployment
        self.patches = {name: json.loads((ROOT / 'pending' / (name + '.patch.json')).read_text()) for name in self.documents}

    def test_changes_preserve_existing_bindings_ids_schedules_and_activation(self):
        for name, original in self.documents.items():
            result = stage(original, self.patches[name])
            self.assertEqual(original['id'], result['id'])
            self.assertEqual(original.get('settings'), result.get('settings'))
            self.assertEqual(original.get('active'), result.get('active'))
            old = {n['id']: n for n in original['nodes']}
            new = {n['id']: n for n in result['nodes']}
            for node_id, node in old.items():
                actual = new[node_id]
                for key in set(node) - {'parameters'}:
                    self.assertEqual(node[key], actual[key], (name, node_id, key))
                if node['type'] != 'n8n-nodes-base.code':
                    self.assertEqual(node['parameters'], actual['parameters'])
            self.assertEqual(len(result['nodes']) - len(original['nodes']), {'W2': 1, 'W9': 1, 'W6': 4}.get(name, 0))

    def test_stale_version_node_or_graph_is_refused(self):
        for field in ['version', 'node', 'graph']:
            d = copy.deepcopy(self.documents['W7'])
            if field == 'version': d['versionId'] = 'newer-production-version'
            if field == 'node': next(n for n in d['nodes'] if n['name'] == 'URLs')['parameters']['jsCode'] += '\n// newer work'
            if field == 'graph': d['connections'].pop('Oxylabs AI Search')
            with self.assertRaises(ValueError): stage(d, self.patches['W7'])

    def test_w9_fresh_blacklist_is_on_the_actual_path_to_the_final_gate(self):
        result = stage(self.documents['W9'], self.patches['W9'])
        path = result['connections']
        self.assertEqual(path['Chantier – Clients frais']['main'][0][0]['node'], 'Chantier – Blacklist fraîche')
        self.assertEqual(path['Chantier – Blacklist fraîche']['main'][0][0]['node'], 'Chantier – Queue fraîche')
        self.assertEqual(path['Chantier – Queue fraîche']['main'][0][0]['node'], 'Chantier – garde')

    def test_w2_blacklist_and_w6_reservation_are_on_the_actual_send_paths(self):
        w2 = stage(self.documents['W2'], self.patches['W2'])
        self.assertEqual(w2['connections']['Telegram']['main'][0][0]['node'], 'Site – Blacklist fraîche')
        self.assertEqual(w2['connections']['Site – Blacklist fraîche']['main'][0][0]['node'], 'Accusé ?')
        w6 = stage(self.documents['W6'], self.patches['W6'])
        path = ['Vérifier échéances', 'Rappels – réserver', 'Rappels – restaurer', 'Telegram', 'Rappels – résultat', 'Rappels – enregistrer']
        for source, target in zip(path, path[1:]):
            self.assertEqual(w6['connections'][source]['main'][0][0]['node'], target)
        reservation = next(n for n in w6['nodes'] if n['name'] == 'Rappels – réserver')['parameters']
        self.assertEqual(reservation['filters']['conditions'][0]['keyValue'], '={{ $json._reservation.task_key }}')
        self.assertEqual(reservation['columns']['value']['task_key'], '={{ $json._reservation.task_key }}')

    def test_private_binding_changes_are_preserved_instead_of_replaced_from_public_export(self):
        d = copy.deepcopy(self.documents['W9'])
        node = next(n for n in d['nodes'] if n['name'] == 'Email client')
        node['credentials']['smtp']['id'] = 'synthetic-private-binding'
        result = stage(d, self.patches['W9'])
        self.assertEqual(next(n for n in result['nodes'] if n['name'] == 'Email client')['credentials'], node['credentials'])

    def test_reapplying_w9_cannot_duplicate_its_node(self):
        first = stage(self.documents['W9'], self.patches['W9'])
        with self.assertRaises(ValueError): stage(first, self.patches['W9'])


if __name__ == '__main__':
    unittest.main()
