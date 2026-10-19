"""Post-activation provenance checks; no live connection or workflow execution."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cloud_handoff import collect
from stage_patch import stage


class PublishedHandoffTests(unittest.TestCase):
    def test_archived_patches_are_recognized_without_reapplying_or_duplicating_nodes(self):
        report = collect(ROOT)
        self.assertEqual(report['pending_patch_count'], 0)
        self.assertEqual(report['deployed_patch_count'], 6)
        self.assertEqual(report['live_deployment'], 'published_verified_at_capture')
        for entry in report['workflows']:
            self.assertEqual(entry['baseline_nodes'], entry['candidate_nodes'])

    def test_old_patch_refuses_to_overwrite_the_new_published_version(self):
        for name in ['W2', 'W3', 'W4', 'W6', 'W7', 'W9']:
            with self.assertRaisesRegex(ValueError, 'ID/version changed'):
                stage(json.loads((ROOT / (name + '.json')).read_text()), json.loads((ROOT / 'pending' / (name + '.patch.json')).read_text()))

    def test_pre_activation_fixtures_remain_recoverable_from_immutable_git_history(self):
        original = json.loads(subprocess.check_output(['git', 'show', '883e99b9a859fef687f5ffe997e999328c43e384:automation/n8n/W9.json'], cwd=ROOT.parents[1], text=True))
        patch = json.loads((ROOT / 'pending/W9.patch.json').read_text())
        candidate = stage(original, patch)
        self.assertEqual(len(candidate['nodes']), len(original['nodes']) + 1)

    def test_mismatched_publication_evidence_prevents_a_false_live_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for name in ['manifest.json', 'continuation.json', 'data-tables.json', 'activation.json', 'My workflow.json'] + [f'W{i}.json' for i in range(11)]:
                shutil.copyfile(ROOT / name, target / name)
            shutil.copytree(ROOT / 'pending', target / 'pending')
            shutil.copytree(ROOT / 'revisions', target / 'revisions')
            path = target / 'activation.json'; data = json.loads(path.read_text())
            data['workflows']['W3']['active'] = False; path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'Publication evidence'):
                collect(target)

    def test_qualification_revision_preserves_both_immutable_patch_chains(self):
        report = collect(ROOT)
        self.assertEqual(report['pending_patch_count'], 0)
        continuation = json.loads((ROOT / 'continuation.json').read_text())
        for name in ['W3', 'W4', 'W7']:
            entry = next(x for x in continuation['pending_revisions'] if x['workflow'] == name)
            revision = entry['superseding_revision']
            before = json.loads((ROOT / 'revisions/qualification-20261019' / (name + '.before.json')).read_text())
            staged = stage(before, json.loads((ROOT / revision['path']).read_text()))
            current = json.loads((ROOT / (name + '.json')).read_text())
            for key in ['id', 'name', 'nodes', 'connections', 'settings']:
                self.assertEqual(staged[key], current[key])
            self.assertEqual(current['versionId'], revision['published_version_id'])


if __name__ == '__main__':
    unittest.main()
