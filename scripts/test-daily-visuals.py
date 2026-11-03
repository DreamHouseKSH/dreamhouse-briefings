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

    def semantic_scene(self, kind, **fields):
        m = copy.deepcopy(self.manifest)
        m['scenes'][1].update(type=kind, eyebrow='SOURCE / TEST', condition='조건 확인', **fields)
        return m

    def test_metric_bars_and_scale(self):
        m = self.semantic_scene('metric-bars', unit='%', scale_max=100,
            metrics=[{'label': '부하 편차 감소', 'value': 34, 'qualifier': '최대'},
                     {'label': '집중 부하 감소', 'value': 16, 'qualifier': '최대'}], caption='회사 실증 기준 감소율 %')
        self.assertEqual(v.validate(m, self.edition), 14)
        for bad in (0, -1, float('nan'), 30, True):
            n = copy.deepcopy(m); n['scenes'][1]['scale_max'] = bad
            with self.assertRaises(ValueError): v.validate(n, self.edition)
        m['scenes'][1]['metrics'][0]['qualifier'] = ''
        with self.assertRaises(ValueError): v.validate(m, self.edition)

    def test_semantic_flows_and_boundaries(self):
        nodes = [{'label': '실제 망', 'detail': '관측 자료', 'state': 'observed'},
                 {'label': '가상 검증', 'detail': '디지털 트윈', 'state': 'concept'},
                 {'label': '확대 적용', 'detail': '후속 계획', 'state': 'planned'}]
        for kind, key in [('process-flow', 'nodes'), ('architecture', 'layers')]:
            m = self.semantic_scene(kind, **{key: copy.deepcopy(nodes)}, boundary='검증된 실행 범위')
            self.assertEqual(v.validate(m, self.edition), 14)
            m['scenes'][1][key][0]['state'] = 'complete-and-safe'
            with self.assertRaises(ValueError): v.validate(m, self.edition)
        m = self.semantic_scene('architecture', layers=nodes, boundary='')
        with self.assertRaises(ValueError): v.validate(m, self.edition)

    def test_compatibility_limits_and_preview(self):
        rows = [{'component': 'CUDA', 'before': '12.9', 'after': '13.0', 'status': 'changed'},
                {'component': 'vLLM', 'before': 'v0.32.0', 'after': 'v0.33.0rc3', 'status': 'preview'}]
        m = self.semantic_scene('compatibility', rows=rows, headings=['항목', '문서 A', '문서 B'])
        self.assertEqual(v.validate(m, self.edition), 14)
        m['scenes'][1]['rows'][0]['after'] = 'a' * 11
        with self.assertRaises(ValueError): v.validate(m, self.edition)

    def test_worktree_and_timeline(self):
        m = self.semantic_scene('worktree-tree', root_label='공통 Git 기록', branches=[
            {'label': 'branch A', 'directory': '작업 폴더 A'},
            {'label': 'branch B', 'directory': '작업 폴더 B'}])
        self.assertEqual(v.validate(m, self.edition), 14)
        m['scenes'][1]['branches'].append({'label': 'branch C', 'directory': '작업 폴더 C'})
        self.assertEqual(v.validate(m, self.edition), 14)
        m['scenes'][1]['branches'][0]['directory'] = 'x' * 9
        with self.assertRaises(ValueError): v.validate(m, self.edition)
        m = self.semantic_scene('timeline', output='영상 출력', caption='개념도: 길이는 실제 재생 시간이 아님',
            tracks=[{'label': 'HTML', 'content': '장면 구조'}, {'label': 'CSS', 'content': '스타일과 움직임'}])
        self.assertEqual(v.validate(m, self.edition), 14)
        m['scenes'][1]['caption'] = '실제 영상'
        with self.assertRaises(ValueError): v.validate(m, self.edition)

    def test_sandbox_optional_labels(self):
        m = self.semantic_scene('sandbox', labels={'eyebrow': 'DESKTOP / PERMISSIONS',
            'request': '요청', 'agent': '도구', 'target': '컴퓨터', 'condition': '권한은 별도 확인'})
        self.assertEqual(v.validate(m, self.edition), 14)
        del m['scenes'][1]['labels']['target']
        with self.assertRaises(ValueError): v.validate(m, self.edition)

    def test_previous_rendering_branches_preserved(self):
        # New branches are additive; previous edition still uses only original types.
        self.assertFalse({'metric-bars', 'process-flow', 'architecture', 'compatibility'} &
                         {s['type'] for s in self.manifest['scenes']})

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
