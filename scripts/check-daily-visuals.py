#!/usr/bin/env python3
"""Read-only semantic-scene publication gate; never synthesizes audio.

Structural validation is necessary, not sufficient: editorial source verification
and rendered desktop/mobile inspection remain mandatory (WORKFLOW section 10).
"""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'cover', 'ownership', 'package', 'exports', 'engine', 'devices',
         'studio', 'memory', 'dictation', 'sandbox', 'voice-filter',
         'headless', 'vision', 'closing', 'metric-bars', 'process-flow',
         'architecture', 'compatibility', 'worktree-tree', 'timeline'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def validate(manifest, edition):
    require(isinstance(manifest, dict), 'manifest must be an object')
    require(type(manifest.get('schema_version')) is int and manifest['schema_version'] == 1,
            'schema_version must be 1')
    require(manifest.get('date') == edition['date'], 'date differs from edition')
    require(manifest.get('source_hashes') == edition['source_hashes'], 'source_hashes differ from edition')
    scenes = manifest.get('scenes')
    require(isinstance(scenes, list) and len(scenes) == len(edition['slides']),
            'scene count must match edition slide count')
    ids = set()
    items = {item['id']: item for item in edition['items']}
    for i, (scene, slide) in enumerate(zip(scenes, edition['slides'])):
        require(isinstance(scene, dict), f'scene {i + 1} must be an object')
        sid = scene.get('id')
        require(text(sid) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', sid) and sid not in ids,
                f'scene {i + 1}: missing/unsafe/duplicate id')
        ids.add(sid)
        kind = scene.get('type')
        require(isinstance(kind, str) and kind in TYPES, f'{sid}: unsupported scene type')
        for key in ('title', 'dek', 'alt', 'caption'):
            require(text(scene.get(key)), f'{sid}: {key} must be nonempty text')
        steps = scene.get('steps')
        require(isinstance(steps, list) and len(steps) == 3 and all(text(s) for s in steps),
                f'{sid}: exactly three textual steps required')
        refs = scene.get('source_ids')
        require(isinstance(refs, list) and all(isinstance(r, str) and r in items for r in refs),
                f'{sid}: unknown or malformed source_ids')
        require(len(refs) == len(set(refs)) and refs == slide.get('refs', []),
                f'{sid}: source_ids must match corresponding slide refs')
        if kind not in ('cover', 'closing'):
            require(bool(refs), f'{sid}: content scene needs a source')
        for ref in refs:
            require(text(items[ref].get('source')), f'{sid}: source URL missing')
        if kind in ('metric-bars', 'process-flow', 'architecture', 'compatibility'):
            require(text(scene.get('eyebrow')) and len(scene['eyebrow']) <= 40,
                    f'{sid}: concise eyebrow required (40 characters max)')
            require(text(scene.get('condition')) and len(scene['condition']) <= 28,
                    f'{sid}: concise visible condition required (28 characters max)')
        if kind == 'metric-bars':
            require(text(scene.get('unit')) and len(scene['unit']) <= 3,
                    f'{sid}: concise unit required')
            require(number(scene.get('scale_max')) and scene['scale_max'] > 0,
                    f'{sid}: explicit positive common scale required')
            rows = scene.get('metrics')
            require(isinstance(rows, list) and 2 <= len(rows) <= 3,
                    f'{sid}: two or three comparable metrics required')
            for row in rows:
                require(isinstance(row, dict) and text(row.get('label')) and len(row['label']) <= 18,
                        f'{sid}: metric label required (18 characters max)')
                require(number(row.get('value')) and row['value'] <= scene['scale_max'],
                        f'{sid}: metric value outside scale')
                require(len(str(row['value']) + scene['unit']) <= 8, f'{sid}: metric display too long')
                require(text(row.get('qualifier')) and len(row['qualifier']) <= 7,
                        f'{sid}: value qualifier required (7 characters max)')
            require(scene['unit'] in scene['caption'], f'{sid}: caption must state unit and measurement basis')
        if kind in ('process-flow', 'architecture'):
            rows = scene.get('nodes' if kind == 'process-flow' else 'layers')
            require(isinstance(rows, list) and 2 <= len(rows) <= 4,
                    f'{sid}: two to four semantic elements required')
            for row in rows:
                require(isinstance(row, dict) and text(row.get('label')) and len(row['label']) <= 20,
                        f'{sid}: element label required (20 characters max)')
                require(text(row.get('detail')) and len(row['detail']) <= 24,
                        f'{sid}: element detail required (24 characters max)')
                require(row.get('state') in ('observed', 'planned', 'concept'),
                        f'{sid}: each element must distinguish observed/planned/concept')
            if kind == 'architecture':
                require(text(scene.get('boundary')) and len(scene['boundary']) <= 26,
                        f'{sid}: explicit architecture boundary required')
        if kind == 'compatibility':
            if 'headings' in scene:
                require(isinstance(scene['headings'], list) and len(scene['headings']) == 3 and
                        all(text(h) and len(h) <= 12 for h in scene['headings']),
                        f'{sid}: headings must contain three short text labels')
            rows = scene.get('rows')
            require(isinstance(rows, list) and 2 <= len(rows) <= 4,
                    f'{sid}: two to four compatibility rows required')
            for row in rows:
                require(isinstance(row, dict), f'{sid}: row must be an object')
                for key in ('component', 'before', 'after'):
                    require(text(row.get(key)) and len(row[key]) <= 10,
                            f'{sid}: {key} required (10 characters max)')
                require(row.get('status') in ('changed', 'retained', 'preview'),
                        f'{sid}: explicit compatibility status required')
        if kind in ('worktree-tree', 'timeline'):
            for field, limit in [('eyebrow', 40), ('condition', 28)]:
                require(text(scene.get(field)) and len(scene[field]) <= limit,
                        f'{sid}: concise {field} required')
        if kind == 'worktree-tree':
            require(text(scene.get('root_label')) and len(scene['root_label']) <= 20,
                    f'{sid}: concise shared repository label required')
            branches = scene.get('branches')
            require(isinstance(branches, list) and 2 <= len(branches) <= 3,
                    f'{sid}: two or three distinct worktree branches required')
            for branch in branches:
                require(isinstance(branch, dict) and all(text(branch.get(k)) and len(branch[k]) <= 8
                        for k in ('label', 'directory')), f'{sid}: concise branch and directory labels required')
        if kind == 'timeline':
            tracks = scene.get('tracks')
            require(isinstance(tracks, list) and 2 <= len(tracks) <= 3,
                    f'{sid}: two or three semantic tracks required')
            for track in tracks:
                require(isinstance(track, dict) and text(track.get('label')) and len(track['label']) <= 10 and
                        text(track.get('content')) and len(track['content']) <= 18,
                        f'{sid}: concise track label/content required')
            require(text(scene.get('output')) and len(scene['output']) <= 22,
                    f'{sid}: explicit output required')
            require('개념' in scene['caption'] and ('길이' in scene['caption'] or '시간' in scene['caption']),
                    f'{sid}: timeline caption must disclose conceptual lengths/timing')
        if kind == 'sandbox' and 'labels' in scene:
            require(isinstance(scene['labels'], dict), f'{sid}: sandbox labels must be an object')
            for key, limit in [('eyebrow', 40), ('request', 10), ('agent', 10), ('target', 10), ('condition', 24)]:
                require(text(scene['labels'].get(key)) and len(scene['labels'][key]) <= limit,
                        f'{sid}: sandbox {key} label required')
        if kind == 'engine':
            require(text(scene.get('opencl_release')) and text(scene.get('hexagon_release')),
                    f'{sid}: engine releases must be explicit')
        if kind in ('cover', 'studio'):
            fields = ('news_count', 'github_count') if kind == 'cover' else ('role_count', 'skill_count')
            for field in fields:
                require(type(scene.get(field)) is int and scene[field] >= 0,
                        f'{sid}: {field} must be a nonnegative integer')
            if kind == 'cover':
                require(scene['news_count'] == edition['news_count'] and
                        scene['github_count'] == edition['github_count'],
                        f'{sid}: cover counts must match edition')
        if kind in ('ownership', 'exports'):
            key = 'segments' if kind == 'ownership' else 'bars'
            rows = scene.get(key)
            require(isinstance(rows, list) and len(rows) >= 2, f'{sid}: {key} must contain labeled values')
            require(text(scene.get('unit')), f'{sid}: numeric chart requires unit')
            for row in rows:
                require(isinstance(row, dict) and text(row.get('label')) and number(row.get('value')),
                        f'{sid}: chart values must be finite nonnegative numbers with labels')
                if 'growth' in row:
                    require(type(row['growth']) in (int, float) and math.isfinite(row['growth']),
                            f'{sid}: growth must be a finite number')
            if kind == 'ownership':
                require(scene['unit'] == '%' and abs(sum(r['value'] for r in rows) - 100) < .001,
                        f'{sid}: ownership shares must total 100 percent')
            else:
                require(scene['unit'] in scene['caption'], f'{sid}: export caption must state unit')
                require(max(r['value'] for r in rows) > 0, f'{sid}: chart scale must be positive')
    # A type count cannot prove meaning, but rejects the old single-template fallback.
    require(len({s['type'] for s in scenes}) >= min(4, len(scenes)),
            'scene variety gate failed; repeated generic layouts are not a completed edition')
    return len(scenes)


def check(date, root=ROOT):
    datetime.date.fromisoformat(date)
    key = 'day_' + date.replace('-', '')
    edition = json.loads((root / '_data' / f'{key}.json').read_text())
    path = root / '_data' / f'{key}_visuals.json'
    require(path.exists(), 'PENDING visual editorial plan: manifest missing')
    manifest = json.loads(path.read_text())
    count = validate(manifest, edition)
    for name, digest in edition['source_hashes'].items():
        source = (root / name).resolve()
        require(source.is_relative_to(root.resolve()), 'source path escapes repository')
        require(hashlib.sha256(source.read_bytes()).hexdigest() == digest,
                f'source changed: {name}')
    page = (root / 'daily' / f'{date}.html').read_text()
    front = page.split('---', 2)
    require(len(front) == 3 and re.search(r'^visual_key:\s*[\"\']?' + re.escape(key + '_visuals') + r'[\"\']?\s*$', front[1], re.M),
            'page visual_key must reference this manifest')
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('date', help='YYYY-MM-DD')
    args = parser.parse_args()
    try:
        count = check(args.date)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS {args.date}: {count} source-linked scenes; editorial and browser review still required')
    return 0


if __name__ == '__main__':
    sys.exit(main())
