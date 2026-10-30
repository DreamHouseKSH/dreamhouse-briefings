#!/usr/bin/env python3
"""Lightweight Sohee guards; no model download, model load or audio synthesis."""
import hashlib
import copy
import math
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('sohee', Path(__file__).with_name('build-daily-sohee.py'))
sohee = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sohee)
CHECK_SPEC = importlib.util.spec_from_file_location('check_sohee', Path(__file__).with_name('check-sohee-audio.py'))
validator = importlib.util.module_from_spec(CHECK_SPEC)
CHECK_SPEC.loader.exec_module(validator)
try:
    import numpy as np
except ImportError:
    np = None

class SoheeChecks(unittest.TestCase):
    def test_narration_hash_matches_existing_contract(self):
        data = {'slides': [{'narration': ['안녕하세요.', '두 번째.', '끝입니다.']}]}
        expected = hashlib.sha256(json.dumps([s['narration'] for s in data['slides']], ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(sohee.narration_hash(data), expected)
        data['slides'][0]['narration'][0] += ' 변경'
        self.assertNotEqual(sohee.narration_hash(data), expected)

    def test_identifier_pronunciation_preserves_values_and_ordinary_dates(self):
        self.assertEqual(sohee.speech_text('2026-109618·2026-109619'), '이천이십육 하이픈 십만구천육백십팔, 이천이십육 하이픈 십만구천육백십구')
        self.assertEqual(sohee.speech_text('2026-109618·2026-109619에 해당'), '이천이십육 하이픈 십만구천육백십팔, 이천이십육 하이픈 십만구천육백십구에 해당')
        ordinary='2026-10-30, 195.3조 원, 1억 5천만 달러'
        self.assertEqual(sohee.speech_text(ordinary), ordinary)
        source='식별번호 2026-109618'
        self.assertEqual(source, '식별번호 2026-109618')
        self.assertNotEqual(sohee.segment_key(source, 42), sohee.segment_key(source.replace('109618','109619'),42))

    def test_cache_key_is_stable_and_content_bound(self):
        key = sohee.segment_key('공개 대본', 42)
        self.assertEqual(key, sohee.segment_key('공개 대본', 42))
        self.assertNotEqual(key, sohee.segment_key('변경 대본', 42))
        self.assertNotEqual(key, sohee.segment_key('공개 대본', 43))
        with mock.patch.dict(sohee.SETTINGS, {'revision': 'different-revision'}):
            self.assertNotEqual(key, sohee.segment_key('공개 대본', 42))
        with mock.patch.dict(sohee.SETTINGS, {'padding_seconds': 0.4}):
            self.assertNotEqual(key, sohee.segment_key('공개 대본', 42))

    def test_existing_audio_or_metadata_is_preserved_before_importing_models(self):
        for existing in ['audio.mp3', 'audio.json']:
            with self.subTest(existing=existing), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                target = root / existing
                target.write_bytes(b'preserve this edition')
                with self.assertRaises(FileExistsError):
                    sohee.build({'slides': []}, '2026-10-30', root/'audio.mp3', root/'audio.json')
                self.assertEqual(target.read_bytes(), b'preserve this edition')
                self.assertEqual(len(list(root.iterdir())), 1)

    def test_publish_pair_success_and_competing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate, audio, metadata = root/'candidate.mp3', root/'audio.mp3', root/'audio.json'
            candidate.write_bytes(b'validated audio')
            info = {'source': '공개 대본', 'audio_sha256': sohee.sha(candidate)}
            sohee.publish_pair(candidate, info, audio, metadata)
            self.assertEqual(audio.read_bytes(), candidate.read_bytes())
            self.assertEqual(json.loads(metadata.read_text()), info)
            with self.assertRaises(FileExistsError):
                sohee.publish_pair(candidate, info, audio, metadata)
            self.assertEqual(audio.read_bytes(), b'validated audio')
            audio.unlink()
            metadata.write_text('other writer')
            with self.assertRaises(FileExistsError):
                sohee.publish_pair(candidate, info, audio, metadata)
            self.assertFalse(audio.exists())
            self.assertEqual(metadata.read_text(), 'other writer')
            self.assertEqual(candidate.read_bytes(), b'validated audio')

    def test_publish_pair_removes_partial_write_failures(self):
        real_open = Path.open
        class FailingWriter:
            def __init__(self, stream): self.stream = stream
            def __enter__(self): return self
            def __exit__(self, *args): self.stream.close()
            def write(self, data):
                self.stream.write(data[:2])
                raise OSError('simulated disk full after partial write')
        for fail_name in ['audio.mp3', 'audio.json']:
            with self.subTest(fail_name=fail_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                candidate, audio, metadata = root/'candidate.mp3', root/'audio.mp3', root/'audio.json'
                candidate.write_bytes(b'validated audio')
                def failing_open(path, mode='r', *args, **kwargs):
                    stream = real_open(path, mode, *args, **kwargs)
                    return FailingWriter(stream) if path.name == fail_name and mode in ['x', 'xb'] else stream
                with mock.patch.object(Path, 'open', failing_open), self.assertRaises(OSError):
                    sohee.publish_pair(candidate, {'source': '공개 대본'}, audio, metadata)
                self.assertFalse(audio.exists())
                self.assertFalse(metadata.exists())
                self.assertEqual(candidate.read_bytes(), b'validated audio')

    def test_sha_uses_file_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'sample'
            target.write_bytes(b'\x00\xffSohee')
            self.assertEqual(sohee.sha(target), hashlib.sha256(target.read_bytes()).hexdigest())

    @unittest.skipIf(np is None, 'numpy is optional for portable guards; run in the Sohee venv for waveform checks')
    def test_waveform_guards(self):
        sr = sohee.SETTINGS['sample_rate']
        good = np.full(sr, 0.1, dtype=np.float32)
        metrics = sohee.segment_metrics(good, sr, 12)
        self.assertEqual(metrics['samples'], sr)
        self.assertEqual(metrics['speech_seconds'], 1)
        bad = [np.array([], dtype=np.float32), np.zeros(sr), np.full(sr, float('nan')),
               np.full(sr, float('inf')), np.ones(sr), np.full(sr//2, 0.1),
               np.full(sr*80, 0.1), np.full((sr, 2), 0.1)]
        for wave in bad:
            with self.subTest(shape=wave.shape), self.assertRaises(ValueError):
                sohee.segment_metrics(wave, sr, 12)
        with self.assertRaises(ValueError):
            sohee.segment_metrics(good, 22050, 12)
        with self.assertRaises(ValueError):
            sohee.segment_metrics(good, sr, sohee.SETTINGS['max_new_tokens']-1)

class AudioValidationChecks(unittest.TestCase):
    def setUp(self):
        self.data = {'date': '2026-10-30', 'slides': [{'narration': ['처음', '끝']} ]}
        self.metadata = {'date': '2026-10-30', 'duration': 2.0,
            'cues': [{'slide': 0, 'step': 1, 'start': 0.0, 'end': 1.0},
                     {'slide': 0, 'step': 2, 'start': 1.0, 'end': 2.0}]}

    def test_cues_cover_exact_decoded_samples(self):
        expected, bounds = validator.validate_cues(self.data, self.metadata, 24000, 48000)
        self.assertEqual(expected, [(0, 1, '처음'), (0, 2, '끝')])
        self.assertEqual(bounds, [(0, 24000), (24000, 48000)])

    def test_cue_errors_are_not_accepted(self):
        changes = [lambda m: m['cues'].pop(),
                   lambda m: m['cues'][1].update(start=0.9),
                   lambda m: m['cues'][1].update(start=1.1),
                   lambda m: m['cues'][1].update(end=1.9),
                   lambda m: m['cues'][1].update(step=1),
                   lambda m: m['cues'][0].update(start=float('nan')),
                   lambda m: m.update(date='2026-10-29'),
                   lambda m: m.update(validation={'decoded_samples': 1})]
        for index, change in enumerate(changes):
            altered = copy.deepcopy(self.metadata)
            change(altered)
            with self.subTest(case=index), self.assertRaises(ValueError):
                validator.validate_cues(self.data, altered, 24000, 48000)
        with self.assertRaises(ValueError):
            validator.validate_cues(self.data, self.metadata, 24000, 47999)

    def test_signal_metrics_are_portable_and_reject_bad_signal(self):
        self.assertEqual(validator.waveform_metrics([0.1, -0.1])['nonzero'], 2)
        for bad in [[], [0.0] * 10, [float('nan')], [float('inf')], [1.0], [-1.1]]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validator.waveform_metrics(bad)

    def test_asr_similarity_is_a_review_heuristic(self):
        self.assertEqual(validator.similarity('안녕하세요. 오늘 브리핑!', '안녕하세요 오늘 브리핑'), 1.0)
        self.assertEqual(validator.similarity('OpenAI API', 'openai api'), 1.0)
        self.assertLess(validator.similarity('오늘은 브리핑을 시작합니다.', '전혀 다른 문장'), 0.75)
        self.assertLess(validator.similarity('12345', '54321'), 0.75)
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            validator.transcribe(Path(tmp)/'missing-model', [], 24000, [], [], {})

    def test_audio_hash_rejected_before_decoding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data, meta, audio = root/'data.json', root/'meta.json', root/'audio.mp3'
            data.write_text(json.dumps(self.data))
            self.metadata.update(text_sha256=sohee.narration_hash(self.data), audio_sha256='incorrect')
            meta.write_text(json.dumps(self.metadata)); audio.write_bytes(b'not decoded')
            with mock.patch.object(validator, 'decode') as decode, self.assertRaises(ValueError):
                validator.validate(data, audio, meta)
            decode.assert_not_called()

if __name__ == '__main__':
    unittest.main()
