#!/usr/bin/env python3
"""Offline regression coverage for public JSON, dedup review, and cache rebuilding."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('article_index', Path(__file__).with_name('article-index.py'))
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)


def article(title='First product announcement', url='https://example.com/news/one', summary='Our own short summary of a verified announcement.', number='1'):
    return f'## {number}. {title}\n\n- **원문:** {url}\n- **날짜:** 2026-11-06 날짜만 확인\n\n### 요약\n\n{summary}\n\n### 논조·다른 시각\n\n- **기사 논조:** 중립\n'


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.news('2026-11-06', article())
        index.bootstrap(self.root, '2026-11-06')

    def news(self, day, body, category='IT'):
        path = self.root / 'news' / day / (category + '.md')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding='utf-8')
        return path

    def new(self, body=None):
        day = '2026-11-07'
        self.news(day, body or article('Completely unrelated topic', 'https://example.org/new', 'A different verified summary.'))
        index.prepare(self.root, day)
        path = index.edition_path(self.root, day)
        data = json.loads(path.read_text())
        data['records'][0]['event'] = {'key': 'example-product-launch-2026-11-07', 'entities': ['Example'],
                                      'date': None, 'action': 'launch', 'core_facts': ['A genuinely new capability.']}
        path.write_text(index.json_text(data))
        return day, data['records'][0]['entry_id']

    def approve(self, day, entry, decision='new', material=''):
        report = index.report_for(index.load_editions(self.root), day)
        matches = next(r['matches'] for r in report if r['entry_id'] == entry)
        index.review_entry(self.root, day, entry, decision, 'Inspected source and prior coverage.', [m['entry_id'] for m in matches], material)

    def test_canonical_tracking_fragment_case_ports(self):
        self.assertEqual(index.canonical_url('HTTPS://ExAmPle.com:443/item?id=2&utm_source=x#part'), 'https://example.com/item?id=2')
        self.assertEqual(index.canonical_url('http://example.com:80'), 'http://example.com/')

    def test_meaningful_url_differences_preserved(self):
        base = index.canonical_url('https://example.com/Item?id=2')
        for url in ['https://www.example.com/Item?id=2', 'https://example.com/item?id=2', 'https://example.com/Item?id=3', 'http://example.com/Item?id=2', 'https://example.com/Item/?id=2']:
            self.assertNotEqual(base, index.canonical_url(url))
        self.assertEqual(index.canonical_url('https://example.com/?a=2&a=1'), 'https://example.com/?a=2&a=1')

    def test_url_byte_escapes_flags_and_zero_port_stay_distinct(self):
        pairs = [('https://example.com:0/path', 'https://example.com/path'),
                 ('https://example.com/?x=%FF', 'https://example.com/?x=%FE'),
                 ('https://example.com/?flag', 'https://example.com/?flag='),
                 ('https://example.com/?x=%2f', 'https://example.com/?x=/')]
        for a, b in pairs:
            self.assertNotEqual(index.canonical_url(a), index.canonical_url(b))
        self.assertEqual(index.canonical_url('https://example.com/?x=%FF&utm_source=test'), 'https://example.com/?x=%FF')

    def test_markdown_url_parentheses_preserved(self):
        self.assertEqual(index.urls('[paper](https://example.com/wiki/Foo_(bar))'), ['https://example.com/wiki/Foo_(bar)'])
        self.assertEqual(index.urls('https://example.com/end. https://example.com/end)'), ['https://example.com/end.', 'https://example.com/end)'])
        self.assertEqual(index.urls('(보도 https://example.com/Foo_(bar))'), ['https://example.com/Foo_(bar)'])
        self.assertEqual(index.urls('<https://example.com/>'), ['https://example.com/'])

    def test_unsafe_urls_rejected(self):
        for url in ['javascript:alert(1)', 'https://name:secret@example.com/', 'https://example.com/?access_token=secret', 'https://example.com/a b']:
            with self.assertRaises(ValueError): index.canonical_url(url)

    def test_legacy_is_not_new_verification(self):
        data = index.load_editions(self.root)[0]
        self.assertEqual(data['records'][0]['publication_note'], '2026-11-06 날짜만 확인')
        self.assertIsNone(data['records'][0]['event']['date'])
        self.assertEqual(index.gate(self.root, '2026-11-06')['status'], 'legacy-index-only')
        self.assertEqual(data['records'][0]['review']['decision'], 'legacy-unreviewed')

    def test_parse_nested_legacy_without_summary_heading(self):
        self.news('2026-11-06', '## 4. Group\n\n### 4-1. One\n\n- **원문:** https://example.com/one\n\nOwn summary one.\n\n### 4-2. Two\n\n- **원문:** https://example.com/two\n\nOwn summary two.')
        records = index.parse_edition(self.root, '2026-11-06', 'legacy')['records']
        self.assertEqual([r['entry_id'] for r in records], ['2026-11-06/IT/4-1', '2026-11-06/IT/4-2'])

    def test_unnumbered_article_fails_not_silently_dropped(self):
        self.news('2026-11-06', article() + '\n## Unnumbered\n\n- **원문:** https://example.com/two\n\n### 요약\n\nSome more news.')
        with self.assertRaisesRegex(ValueError, 'Unindexed'): index.parse_edition(self.root, '2026-11-06')

    def test_pending_blocks_and_explicit_review_passes(self):
        day, entry = self.new()
        with self.assertRaisesRegex(ValueError, 'review stale'): index.gate(self.root, day)
        self.approve(day, entry)
        self.assertEqual(index.gate(self.root, day)['status'], 'reviewed')

    def test_same_url_editorial_revision_requires_material_update(self):
        day, entry = self.new(article('Product now available in Korea', 'https://example.com/news/one?utm_campaign=repeat', 'The product became available in Korea today.'))
        self.approve(day, entry, 'distinct')
        with self.assertRaisesRegex(ValueError, 'same article'): index.gate(self.root, day)
        self.approve(day, entry, 'update')
        with self.assertRaisesRegex(ValueError, 'concrete new facts'): index.gate(self.root, day)
        self.approve(day, entry, 'update', 'New public availability in Korea, distinct from earlier announcement.')
        self.assertEqual(index.gate(self.root, day)['status'], 'reviewed')
        records = [r for e in index.load_editions(self.root) for r in e['records']]
        self.assertEqual(records[0]['article_id'], records[1]['article_id'])
        self.assertNotEqual(records[0]['revision_id'], records[1]['revision_id'])

    def test_unchanged_summary_never_passes_as_update(self):
        day, entry = self.new(article())
        self.approve(day, entry, 'update', 'A vague claim of change cannot override identical summary.')
        with self.assertRaisesRegex(ValueError, 'unchanged own summary'): index.gate(self.root, day)

    def test_event_candidates_different_url_and_same_day(self):
        day, entry = self.new()
        self.news(day, article('Other coverage of launch', 'https://other.example/report', 'Another independent summary.'), 'AI')
        index.prepare(self.root, day, refresh=True)
        path = index.edition_path(self.root, day)
        data = json.loads(path.read_text())
        for record in data['records']:
            record['event']['key'] = 'same-public-event'
        path.write_text(index.json_text(data))
        report = index.report_for(index.load_editions(self.root), day)
        self.assertIn('same_event_key', report[1]['matches'][0]['reasons'])
        self.assertEqual(report[1]['matches'][0]['entry_id'], day + '/AI/1')

    def test_event_change_invalidates_review(self):
        day, entry = self.new(); self.approve(day, entry)
        path = index.edition_path(self.root, day); data = json.loads(path.read_text())
        data['records'][0]['event']['core_facts'].append('New fact added after approval.')
        path.write_text(index.json_text(data))
        with self.assertRaisesRegex(ValueError, 'review stale'): index.gate(self.root, day)

    def test_candidate_content_change_invalidates_review(self):
        day, entry = self.new(article('Product now available in Korea', summary='The product became available in Korea today.'))
        self.approve(day, entry, 'update', 'A new availability announcement.')
        old = index.edition_path(self.root, '2026-11-06'); data = json.loads(old.read_text())
        data['records'][0]['event']['core_facts'] = ['Historical context newly classified.']
        old.write_text(index.json_text(data))
        with self.assertRaisesRegex(ValueError, 'review stale'): index.gate(self.root, day)

    def test_missing_index_or_date_fails_closed(self):
        self.news('2026-11-07', article())
        with self.assertRaisesRegex(ValueError, 'Unindexed'): index.load_editions(self.root)
        index.edition_path(self.root, '2026-11-06').unlink()
        with self.assertRaisesRegex(ValueError, 'Unindexed'): index.load_editions(self.root)

    def test_source_change_requires_refresh_and_fresh_review(self):
        day, entry = self.new(); self.approve(day, entry)
        self.news(day, article('Changed source content', 'https://new.example/source', 'New summary after original review.'))
        with self.assertRaisesRegex(ValueError, 'Archive changed'): index.gate(self.root, day)
        index.prepare(self.root, day, refresh=True)
        self.assertEqual(json.loads(index.edition_path(self.root, day).read_text())['records'][0]['review']['decision'], 'pending')

    def test_refresh_is_deterministic_and_preserves_valid_review(self):
        day, entry = self.new(); self.approve(day, entry)
        path = index.edition_path(self.root, day); before = path.read_bytes()
        index.prepare(self.root, day, refresh=True)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(index.gate(self.root, day)['status'], 'reviewed')
        with self.assertRaisesRegex(ValueError, 'exists'): index.prepare(self.root, day)
        with self.assertRaisesRegex(ValueError, 'one-time'): index.bootstrap(self.root, '2026-11-07')

    def test_duplicate_ids_and_unexpected_fields_rejected(self):
        path = index.edition_path(self.root, '2026-11-06'); original = json.loads(path.read_text())
        bad = json.loads(json.dumps(original)); bad['records'].append(bad['records'][0]); path.write_text(index.json_text(bad))
        with self.assertRaisesRegex(ValueError, 'Duplicate'): index.load_editions(self.root)
        original['records'][0]['private_notes'] = 'not allowed'; path.write_text(index.json_text(original))
        with self.assertRaisesRegex(ValueError, 'Unknown/missing'): index.load_editions(self.root)

    def test_review_must_acknowledge_exact_candidates(self):
        day, entry = self.new(article())
        with self.assertRaisesRegex(ValueError, 'every candidate'):
            index.review_entry(self.root, day, entry, 'update', 'Reviewed.', [], 'Changed.')

    def test_new_date_cannot_claim_legacy_exemption(self):
        day, _ = self.new(); path = index.edition_path(self.root, day); data = json.loads(path.read_text())
        data['origin'] = 'legacy'; path.write_text(index.json_text(data))
        with self.assertRaisesRegex(ValueError, 'exemption'): index.gate(self.root, day)

    def test_sqlite_is_disposable_and_does_not_modify_sources(self):
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        index.rebuild_sqlite(self.root)
        db_path = self.root / '.cache/article-index.sqlite3'
        with sqlite3.connect(db_path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM articles').fetchone()[0], 1)
        db_path.unlink(); index.rebuild_sqlite(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_review_hash_independent_of_python_hash_seed(self):
        day, entry = self.new(); self.approve(day, entry)
        code = 'import importlib.util; from pathlib import Path; s=importlib.util.spec_from_file_location("i",' + repr(str(Path(index.__file__))) + '); i=importlib.util.module_from_spec(s); s.loader.exec_module(i); print(i.gate(Path(' + repr(str(self.root)) + '),"2026-11-07")["status"])'
        for seed in ('1', '2'):
            result = subprocess.run([sys.executable, '-c', code], env={'PYTHONHASHSEED': seed}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_checked_atomic_write_preserves_concurrent_change(self):
        path = index.edition_path(self.root, '2026-11-06')
        original = path.read_text(); edited = original + ' '
        path.write_text(edited)
        with self.assertRaisesRegex(ValueError, 'Concurrent'):
            index.atomic_write(path, {}, expected=original)
        self.assertEqual(path.read_text(), edited)
        self.assertEqual(list(path.parent.glob('.*.json.*')), [])

    def test_second_writer_fails_without_overwrite(self):
        day, entry = self.new()
        before = index.edition_path(self.root, day).read_bytes()
        with index.edition_lock(self.root, day):
            with self.assertRaisesRegex(ValueError, 'Another index writer'):
                index.prepare(self.root, day, refresh=True)
            with self.assertRaisesRegex(ValueError, 'Another index writer'):
                self.approve(day, entry)
        self.assertEqual(index.edition_path(self.root, day).read_bytes(), before)

    def test_new_presentation_requires_index_review(self):
        import shutil
        day, entry = self.new()
        scripts = self.root / 'scripts'; scripts.mkdir()
        shutil.copy(index.__file__, scripts / 'article-index.py')
        spec = importlib.util.spec_from_file_location('daily', Path(index.__file__).with_name('build-daily.py'))
        daily = importlib.util.module_from_spec(spec); spec.loader.exec_module(daily)
        daily.ROOT = self.root
        with self.assertRaisesRegex(ValueError, 'review stale'):
            daily.news_index_gate(day)
        self.approve(day, entry)
        snapshot = daily.news_index_gate(day)
        self.assertIn('article-index/editions/' + day + '.json', snapshot)
        self.assertIn('article-index/config.json', snapshot)

    def test_real_archive_coverage_is_byte_preserving(self):
        root = Path(index.__file__).resolve().parents[1]
        paths = list((root / 'news').glob('*/*.md')) + list((root / '_data').glob('day_*.json'))
        before = {p: index.sha(p.read_bytes()) for p in paths}
        editions = index.load_editions(root)
        self.assertEqual(sum(len(e['records']) for e in editions if e['briefing_date'] <= '2026-11-06'), 236)
        self.assertGreaterEqual(len(editions), 23)
        self.assertEqual(before, {p: index.sha(p.read_bytes()) for p in paths})


if __name__ == '__main__':
    unittest.main()
