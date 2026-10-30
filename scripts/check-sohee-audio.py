#!/usr/bin/env python3
"""Validate staged/published narration with stdlib + FFmpeg; optional local-only ASR.
Exit 0: requested checks passed; 1: invalid audio/metadata or runtime error;
2: ASR differences require review (not proof of a synthesis error).
No model download, external audio transfer, or audio/source replacement is performed.
"""
import argparse
from array import array
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

os.environ['ORT_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['DO_NOT_TRACK']='1'


def sha(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def normalized(text):
    return re.sub(r'[^\w]', '', text.casefold(), flags=re.UNICODE).replace('_', '')


def similarity(expected, transcript):
    return difflib.SequenceMatcher(None, normalized(expected), normalized(transcript), autojunk=False).ratio()


def expected_cues(data):
    result = []
    for slide, entry in enumerate(data['slides']):
        for step, text in enumerate(entry['narration'], 1):
            if not isinstance(text, str) or not text.strip():
                raise ValueError('Empty or non-text narration')
            result.append((slide, step, text))
    if not result:
        raise ValueError('No narration cues')
    return result


def validate_cues(data, metadata, rate, frames):
    expected = expected_cues(data)
    cues = metadata['cues']
    if len(cues) != len(expected):
        raise ValueError('Cue count differs from narration')
    if metadata['date'] != data['date']:
        raise ValueError('Narration and metadata dates differ')
    duration = metadata['duration']
    if not isinstance(duration, (float, int)) or not math.isfinite(duration) or duration <= 0:
        raise ValueError('Invalid total duration')
    if round(duration * rate) != frames:
        raise ValueError('Decoded sample count differs from metadata duration')
    if metadata.get('validation', {}).get('decoded_samples', frames) != frames:
        raise ValueError('Decoded sample count differs from recorded validation')
    last = 0.0
    bounds = []
    for index, (cue, target) in enumerate(zip(cues, expected)):
        start, end = cue['start'], cue['end']
        if not all(isinstance(x, (float, int)) and math.isfinite(x) for x in [start, end]):
            raise ValueError(f'Non-finite cue boundary: {index + 1}')
        if (cue['slide'], cue['step']) != target[:2]:
            raise ValueError(f'Unexpected cue order: {index + 1}')
        # Stored six-decimal cue boundaries must refer to exactly adjacent samples.
        if abs(start - last) > 0.000001 or end <= start or start < 0:
            raise ValueError(f'Gap, overlap, or invalid cue boundary: {index + 1}')
        begin_frame, end_frame = round(start * rate), round(end * rate)
        if not 0 <= begin_frame < end_frame <= frames:
            raise ValueError(f'Cue outside decoded audio: {index + 1}')
        bounds.append((begin_frame, end_frame))
        last = end
    if abs(last - duration) > 0.000001 or bounds[-1][1] != frames:
        raise ValueError('Last cue does not end at final audio sample')
    return expected, bounds


def waveform_metrics(samples):
    if not samples or not all(math.isfinite(value) for value in samples):
        raise ValueError('Empty or non-finite waveform')
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    nonzero = sum(value != 0 for value in samples)
    clipped = sum(abs(value) >= 1.0 for value in samples)
    if not nonzero or rms < 0.002 or clipped:
        raise ValueError(f'Silent/too quiet or clipped cue: rms={rms}, peak={peak}, clipped={clipped}')
    return {'samples': len(samples), 'finite': True, 'nonzero': nonzero,
            'rms': round(rms, 8), 'peak': round(peak, 8), 'clipped_samples': clipped}


def decode(audio):
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
        'stream=sample_rate,channels,codec_name', '-of', 'json', str(audio)], text=True))
    stream = probe['streams'][0]
    rate = int(stream['sample_rate'])
    if stream['channels'] != 1 or rate <= 0:
        raise ValueError('Expected mono audio with positive sample rate')
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(audio),
        '-map', '0:a:0', '-f', 'f32le', '-acodec', 'pcm_f32le', '-'])
    samples = array('f')
    if len(raw) % 4:
        raise ValueError('Incomplete decoded float sample')
    samples.frombytes(raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    return rate, samples, stream['codec_name']


def transcribe(model_dir, samples, rate, expected, bounds, report):
    model_dir = Path(model_dir).resolve()
    if not model_dir.is_dir():
        raise ValueError('ASR model must be an existing local directory; downloads are not supported')
    import numpy as np
    import torch
    from scipy.signal import resample_poly
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    torch.set_num_threads(4)
    processor = WhisperProcessor.from_pretrained(str(model_dir), local_files_only=True)
    model = WhisperForConditionalGeneration.from_pretrained(str(model_dir), local_files_only=True)
    report['asr'] = {'model_directory_name': model_dir.name, 'model_type': 'Whisper',
                     'local_only': True, 'threshold': 0.75, 'flagged_cues': [],
                     'limitation': 'Similarity is a review aid, not an accuracy or naturalness score. Proper names, numbers and ASR errors require human review; a high score does not rule out omissions.'}
    divisor = math.gcd(rate, 16000)
    for index, ((_, _, text), (start, end)) in enumerate(zip(expected, bounds)):
        wave = np.asarray(samples[start:end], dtype=np.float32)
        if rate != 16000:
            wave = resample_poly(wave, 16000 // divisor, rate // divisor)
        # Whisper has a 30-second input window. Refuse silent truncation of longer cues.
        if len(wave) > 30 * 16000:
            report['cues'][index].update({'expected': text, 'transcript': None,
                'score': None, 'review_required': True, 'reason': 'Cue exceeds Whisper 30-second window; not transcribed'})
            report['asr']['flagged_cues'].append(index + 1)
            continue
        started = time.perf_counter()
        inputs = processor(wave, sampling_rate=16000, return_tensors='pt', return_attention_mask=True)
        with torch.inference_mode():
            ids = model.generate(inputs.input_features, attention_mask=inputs.attention_mask,
                                 language='korean', task='transcribe', max_new_tokens=440)
        transcript = processor.batch_decode(ids, skip_special_tokens=True)[0].strip()
        score = similarity(text, transcript)
        capped = ids.shape[-1] >= 440
        flagged = score < 0.75 or capped
        report['cues'][index].update({'expected': text, 'transcript': transcript,
            'score': round(score, 4), 'review_required': flagged,
            'asr_token_cap_suspected': capped, 'asr_seconds': round(time.perf_counter() - started, 3)})
        if flagged:
            report['asr']['flagged_cues'].append(index + 1)
        print(json.dumps({'asr_cue': index + 1, 'total': len(expected), 'score': round(score, 4),
                          'review_required': flagged}, ensure_ascii=False), flush=True)
    report['status'] = 'review_required' if report['asr']['flagged_cues'] else 'checks_passed'


def validate(data_path, audio, metadata_path, asr_model=None):
    data = json.loads(Path(data_path).read_text())
    metadata = json.loads(Path(metadata_path).read_text())
    text_hash = hashlib.sha256(json.dumps([s['narration'] for s in data['slides']], ensure_ascii=False).encode()).hexdigest()
    if metadata['text_sha256'] != text_hash:
        raise ValueError('Narration hash mismatch')
    audio_hash = sha(audio)
    if metadata['audio_sha256'] != audio_hash:
        raise ValueError('Audio hash mismatch')
    rate, samples, codec = decode(audio)
    if rate != metadata.get('validation', {}).get('sample_rate', rate):
        raise ValueError('Sample rate differs from metadata')
    expected, bounds = validate_cues(data, metadata, rate, len(samples))
    report = {'date': data['date'], 'status': 'checks_passed', 'audio_sha256': audio_hash,
        'text_sha256': text_hash, 'sample_rate': rate, 'decoded_samples': len(samples),
        'duration_seconds': len(samples)/rate, 'codec': codec, 'asr_performed': bool(asr_model),
        'limitations': ['No human listening, naturalness or speaker-identity verification.',
                       'Waveform/cue checks do not establish spoken-text completeness.'], 'cues': []}
    for index, ((slide, step, text), (start, end)) in enumerate(zip(expected, bounds)):
        report['cues'].append({'cue': index + 1, 'slide': slide, 'step': step,
                              **waveform_metrics(samples[start:end])})
    if asr_model:
        transcribe(asr_model, samples, rate, expected, bounds, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--audio', type=Path, required=True)
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--asr-model', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report and args.report.resolve() in {args.data.resolve(), args.audio.resolve(), args.metadata.resolve()}:
        parser.error('--report must not overwrite an input file')
    try:
        report = validate(args.data, args.audio, args.metadata, args.asr_model)
        code = 2 if report['status'] == 'review_required' else 0
    except Exception as error:
        report = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error)}
        code = 1
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded)
    print(encoded)
    return code

if __name__ == '__main__':
    raise SystemExit(main())
