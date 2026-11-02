#!/usr/bin/env python3
"""Offline manifest regression tests. No synthesis, network, or file changes."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('visuals', ROOT / 'scripts/check-daily-visuals.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class VisualGateTests(unittest.TestCase):
    def setUp(self):
        self.edition = json.loads((ROOT / '_data/day_20261102.json').read_text())
        self.manifest = json.loads((ROOT / '_data/day_20261102_visuals.json').read_text())

    def rejects(self, edit):
        altered = copy.deepcopy(self.manifest)
        edit(altered)
        with self.assertRaises(ValueError):
            v.validate(altered, self.edition)

    def test_current_edition_14_scenes(self):
        self.assertEqual(v.validate(self.manifest, self.edition), 14)

    def test_count(self):
        self.rejects(lambda m: m['scenes'].pop())

    def test_stale_source(self):
        self.rejects(lambda m: m.update(source_hashes={}))

    def test_source_mapping(self):
        self.rejects(lambda m: m['scenes'][1].update(source_ids=['g1']))

    def test_unknown_source(self):
        self.rejects(lambda m: m['scenes'][1].update(source_ids=['missing']))

    def test_three_steps(self):
        self.rejects(lambda m: m['scenes'][1].update(steps=['one']))

    def test_caption_and_accessibility(self):
        for key in ('caption', 'alt', 'title', 'dek'):
            with self.subTest(key=key):
                self.rejects(lambda m: m['scenes'][1].update({key: ''}))

    def test_unique_ids(self):
        self.rejects(lambda m: m['scenes'][1].update(id='scene-1'))

    def test_generic_fallback_rejected(self):
        self.rejects(lambda m: m['scenes'][1].update(type='orbit'))
        self.rejects(lambda m: [s.update(type='cover') for s in m['scenes']])

    def test_numeric_chart_units(self):
        for i in (1, 3):
            with self.subTest(scene=i):
                self.rejects(lambda m: m['scenes'][i].pop('unit'))

    def test_numeric_chart_labels_and_values(self):
        self.rejects(lambda m: m['scenes'][1]['segments'][0].update(label=''))
        for bad in (-1, float('nan'), float('inf'), True, '49'):
            with self.subTest(value=bad):
                self.rejects(lambda m: m['scenes'][1]['segments'][0].update(value=bad))

    def test_ownership_total(self):
        self.rejects(lambda m: m['scenes'][1]['segments'][0].update(value=50))

    def test_export_unit_caption(self):
        self.rejects(lambda m: m['scenes'][3].update(caption='수출 금액'))

    def test_cover_and_studio_counts(self):
        self.rejects(lambda m: m['scenes'][0].pop('news_count'))
        self.rejects(lambda m: m['scenes'][0].update(github_count=99))
        self.rejects(lambda m: m['scenes'][6].pop('role_count'))
        self.rejects(lambda m: m['scenes'][6].update(skill_count=True))

    def test_engine_releases(self):
        self.rejects(lambda m: m['scenes'][4].pop('opencl_release'))

    def test_existing_audio_contract_unchanged(self):
        import hashlib
        track = json.loads((ROOT / '_data/day_20261102_audio.json').read_text())
        narration = [s['narration'] for s in self.edition['slides']]
        self.assertEqual(track['text_sha256'], hashlib.sha256(json.dumps(narration, ensure_ascii=False).encode()).hexdigest())
        self.assertEqual(len(track['cues']), 42)
        for i, cue in enumerate(track['cues']):
            self.assertEqual((cue['slide'], cue['step']), (i // 3, i % 3 + 1))
            self.assertGreater(cue['end'], cue['start'])
            if i:
                self.assertAlmostEqual(cue['start'], track['cues'][i - 1]['end'], places=3)
        audio = ROOT / 'assets/audio/2026-11-02-narration.mp3'
        self.assertEqual(hashlib.sha256(audio.read_bytes()).hexdigest(), track['audio_sha256'])
        self.assertEqual(track['audio_sha256'], 'c93407e6b6c944e28526c3a3b3ed2bf586ad170bc714e43c7df3b20be41aaa25')


if __name__ == '__main__':
    unittest.main()
