#!/usr/bin/env python3
"""Public metadata/own-summary index and offline pre-publication duplicate review.

JSON editions are the durable source. No article fetching, third-party full text,
credentials, network, external libraries, or changes to news/presentation files.
"""
import argparse
from contextlib import contextmanager
import fcntl
import os
import tempfile
from datetime import date as Date
from difflib import SequenceMatcher
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata
from urllib.parse import unquote_plus, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 1
TRACKING = {'fbclid', 'gclid', 'dclid', 'msclkid', 'mc_cid', 'mc_eid', '_ga'}
SECRET_PARAMS = {'access_token', 'token', 'api_key', 'apikey', 'password', 'signature', 'sig'}
AUTO_FIELDS = {'entry_id', 'article_id', 'revision_id', 'briefing_date', 'category',
               'heading', 'title', 'summary', 'source_urls', 'canonical_urls',
               'publication_note', 'publisher_update_note', 'event_date_note',
               'archive_path', 'archive_url', 'section_sha256'}
EVENT_FIELDS = {'key', 'entities', 'date', 'action', 'core_facts'}
REVIEW_FIELDS = {'decision', 'matched_entries', 'reason', 'material_change', 'basis_sha256'}


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', value).casefold().split())


def canonical_url(url):
    """Conservative syntactic identity, never a claim about redirects/canonicals."""
    url = html.unescape(url.strip())
    if any(c.isspace() or ord(c) < 32 for c in url):
        raise ValueError('Source URL contains whitespace/control characters')
    part = urlsplit(url)
    if part.scheme.lower() not in {'http', 'https'} or not part.hostname:
        raise ValueError('Only absolute HTTP(S) source URLs are supported')
    if part.username is not None or part.password is not None:
        raise ValueError('Credential-bearing source URLs are forbidden')
    host = part.hostname.encode('idna').decode().lower()
    if ':' in host:
        host = '[' + host + ']'
    port = part.port  # Invalid/out-of-range ports are errors, not repaired.
    if port is not None and (part.scheme.lower(), port) not in {('http', 80), ('https', 443)}:
        host += ':' + str(port)
    # Do not decode/re-encode values: byte escapes, bare flags and query order can matter.
    query_parts = []
    for component in part.query.split('&'):
        raw_key = component.split('=', 1)[0]
        try:
            key = unquote_plus(raw_key, errors='strict').casefold()
        except UnicodeDecodeError:
            key = raw_key.casefold()
        if key in SECRET_PARAMS:
            raise ValueError('Potentially secret-bearing source query is forbidden')
        if not key.startswith('utm_') and key not in TRACKING:
            query_parts.append(component)
    return urlunsplit((part.scheme.lower(), host, part.path or '/', '&'.join(query_parts), ''))



def plain(text):
    text = re.sub(r'!\[[^\]]*\]\([^\n]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\n)]+\)', r'\1', text)
    text = re.sub(r'<[^>]+>|\{:[^}]+\}', '', text)
    return html.unescape(re.sub(r'[*`]', '', text)).strip()


def slug(text):
    # Same anchor convention as build-daily.py; preserve source heading numbers.
    text = re.sub(r'<[^>]*>', '', text).lower()
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', text)).strip('-')


def metadata(body, label):
    m = re.search(r'^- \*\*' + re.escape(label) + r':\*\*\s*(.+)$', body, re.M)
    return plain(m[1]) if m else None


def urls(text):
    result = []
    for match in re.finditer(r'https?://[^\s<>]+', text):
        value = match[0]
        prefix = text[:match.start()]
        if prefix.count('(') > prefix.count(')'):
            # Remove an enclosing Markdown/prose delimiter, retaining URL parentheses.
            depth = 0
            for offset, char in enumerate(value):
                if char == '(':
                    depth += 1
                elif char == ')':
                    if depth == 0:
                        value = value[:offset]
                        break
                    depth -= 1
        if value not in result:
            result.append(value)
    return result


def empty_review():
    return {'decision': 'pending', 'matched_entries': [], 'reason': '', 'material_change': '', 'basis_sha256': ''}


def parse_edition(root, day, origin='reviewed'):
    Date.fromisoformat(day)
    files = sorted((root / 'news' / day).glob('*.md'))
    if not files:
        raise ValueError('No news Markdown for ' + day)
    records, hashes = [], {}
    for path in files:
        source = path.read_text(encoding='utf-8')
        relative = path.relative_to(root).as_posix()
        hashes[relative] = sha(path.read_bytes())
        # Historical grouped articles use ### 4-1. / ### 4-2.; each is a source.
        headings = list(re.finditer(r'^#{2,3} ((\d+(?:-\d+)?)\. .+)$', source, re.M))
        parsed_sources = 0
        for i, match in enumerate(headings):
            body = source[match.end():headings[i + 1].start() if i + 1 < len(headings) else len(source)]
            meta = body.split('###')[0]
            primary = re.search(r'^- \*\*(?:원문|게시글):\*\*\s*(.+)$', meta, re.M)
            if not primary:
                # Permit only a genuinely empty parent grouping, never silently drop a story.
                if not body.strip() and i + 1 < len(headings) and headings[i + 1][2].startswith(match[2] + '-'):
                    continue
                raise ValueError(f'Missing primary source: {relative} / {match[1]}')
            parsed_sources += 1
            sources = urls(primary[1])
            if not sources:
                raise ValueError(f'Missing source URL: {relative} / {match[1]}')
            canonical = list(dict.fromkeys(canonical_url(u) for u in sources))
            summary = re.search(r'^### (?:요약|해석)\s*\n(.*?)(?=^### |\Z)', body, re.M | re.S)
            paragraphs = [plain(p) for p in re.split(r'\n\s*\n', summary[1].strip() if summary else (body if origin == 'legacy' else ''))
                          if p.strip() and not p.lstrip().startswith(('>', '!', '-', '<', '{:', '#'))]
            if not paragraphs:
                raise ValueError(f'Missing own summary: {relative} / {match[1]}')
            # Brief archive-authored excerpt, not a fetched publisher article.
            excerpt = paragraphs[0]
            title = re.sub(r'^\d+(?:-\d+)?\.\s*', '', match[1])
            records.append({
                'entry_id': f'{day}/{path.stem}/{match[2]}',
                'article_id': 'url-' + sha(canonical[0]),
                'revision_id': 'editorial-' + sha(normalized(title) + '\n' + normalized(excerpt)),
                'briefing_date': day, 'category': path.stem, 'heading': match[1],
                'title': title, 'summary': excerpt, 'source_urls': sources, 'canonical_urls': canonical,
                'publication_note': metadata(meta, '최초 게시') or metadata(meta, '날짜'),
                'publisher_update_note': metadata(meta, '원문 수정'),
                'event_date_note': metadata(meta, '사건·제공일'),
                'archive_path': relative, 'archive_url': '/' + relative[:-3] + '.html#' + slug(match[1]),
                'section_sha256': sha(match[1] + '\n' + body),
                'event': {'key': '', 'entities': [], 'date': None, 'action': '', 'core_facts': []},
                'review': {'decision': 'legacy-unreviewed', 'matched_entries': [],
                           'reason': '기존 공개 요약에서 색인만 생성. 원출처·시각·중복을 새로 검증하지 않음.',
                           'material_change': '', 'basis_sha256': ''} if origin == 'legacy' else empty_review(),
            })
        if parsed_sources != len(re.findall(r'^- \*\*(?:원문|게시글):\*\*', source, re.M)):
            raise ValueError('Unindexed article metadata/unnumbered heading: ' + relative)
    if not records:
        raise ValueError('No indexable articles for ' + day)
    return {'schema_version': SCHEMA, 'briefing_date': day, 'origin': origin,
            'source_hashes': hashes, 'records': records}


def directory(root):
    return root / 'article-index'


def edition_path(root, day):
    Date.fromisoformat(day)
    return directory(root) / 'editions' / (day + '.json')


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


@contextmanager
def edition_lock(root, day):
    Date.fromisoformat(day)
    locks = root / '.cache' / 'article-index-locks'
    locks.mkdir(parents=True, exist_ok=True)
    with (locks / (day + '.lock')).open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError('Another index writer is active for ' + day) from error
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def atomic_write(path, value, expected=None):
    """Durable complete JSON, exclusive creation or checked replacement under lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', prefix='.' + path.name + '.',
                                         dir=path.parent, delete=False) as out:
            temporary = Path(out.name)
            out.write(json_text(value))
            out.flush()
            os.fsync(out.fileno())
        if expected is None:
            os.link(temporary, path)  # Atomic exclusive creation, never overwrite.
        else:
            if path.read_text(encoding='utf-8') != expected:
                raise ValueError('Concurrent index change; stopped without overwriting')
            os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_new(path, value):
    atomic_write(path, value)


def load_config(root):
    config = json.loads((directory(root) / 'config.json').read_text(encoding='utf-8'))
    if set(config) != {'schema_version', 'legacy_through'} or config['schema_version'] != SCHEMA:
        raise ValueError('Unsupported index configuration')
    Date.fromisoformat(config['legacy_through'])
    return config


def validate(edition, config):
    if set(edition) != {'schema_version', 'briefing_date', 'origin', 'source_hashes', 'records'}:
        raise ValueError('Unknown/missing edition fields; keep this index public and minimal')
    if edition['schema_version'] != SCHEMA:
        raise ValueError('Unsupported schema version')
    day = edition['briefing_date']
    Date.fromisoformat(day)
    expected_origin = 'legacy' if day <= config['legacy_through'] else 'reviewed'
    if edition['origin'] != expected_origin:
        raise ValueError('Legacy exemption cannot be used for a new edition')
    seen = set()
    for record in edition['records']:
        if set(record) != AUTO_FIELDS | {'event', 'review'}:
            raise ValueError('Unknown/missing record fields: ' + str(record.get('entry_id')))
        if record['entry_id'] in seen or record['briefing_date'] != day:
            raise ValueError('Duplicate entry ID or mismatched date')
        seen.add(record['entry_id'])
        if set(record['event']) != EVENT_FIELDS or set(record['review']) != REVIEW_FIELDS:
            raise ValueError('Unknown/missing event or review fields')
        if record['canonical_urls'] != list(dict.fromkeys(canonical_url(u) for u in record['source_urls'])):
            raise ValueError('Canonical URLs disagree with sources')
        if record['article_id'] != 'url-' + sha(record['canonical_urls'][0]):
            raise ValueError('Invalid article ID')
        if record['revision_id'] != 'editorial-' + sha(normalized(record['title']) + '\n' + normalized(record['summary'])):
            raise ValueError('Invalid editorial revision ID')
        for key in ('key', 'action'):
            if not isinstance(record['event'][key], str):
                raise ValueError('Event key/action must be strings')
        if record['event']['date'] is not None:
            Date.fromisoformat(record['event']['date'])
        for value in (record['event']['entities'], record['event']['core_facts'], record['review']['matched_entries']):
            if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
                raise ValueError('Expected list of nonempty strings')
        for key in ('decision', 'reason', 'material_change', 'basis_sha256'):
            if not isinstance(record['review'][key], str):
                raise ValueError('Review values must be strings')
        if expected_origin == 'reviewed' and record['review']['decision'] not in {'pending', 'new', 'distinct', 'update'}:
            raise ValueError('Invalid review decision')
    if not seen:
        raise ValueError('Empty edition')


def load_editions(root, verify_sources=True):
    config = load_config(root)
    editions = []
    for path in sorted((directory(root) / 'editions').glob('*.json')):
        edition = json.loads(path.read_text(encoding='utf-8'))
        validate(edition, config)
        if path.name != edition['briefing_date'] + '.json':
            raise ValueError('Edition filename/date mismatch')
        if verify_sources:
            fresh = parse_edition(root, edition['briefing_date'], edition['origin'])
            if fresh['source_hashes'] != edition['source_hashes']:
                raise ValueError('Archive changed since indexing: ' + edition['briefing_date'] + '; review and refresh explicitly')
            if [{k: r[k] for k in AUTO_FIELDS} for r in fresh['records']] != [{k: r[k] for k in AUTO_FIELDS} for r in edition['records']]:
                raise ValueError('Index content differs from source: ' + edition['briefing_date'])
        editions.append(edition)
    expected = {p.name for p in (root / 'news').iterdir() if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.name) and list(p.glob('*.md'))}
    actual = {e['briefing_date'] for e in editions}
    if verify_sources and actual != expected:
        raise ValueError('Unindexed/missing news dates: ' + ', '.join(sorted(expected ^ actual)))
    return editions


def tokens(text):
    return set(re.findall(r'[a-z0-9가-힣][a-z0-9가-힣.+-]*', normalized(text))) - {'ai', 'the', 'new', '및', '공개', '발표', '출시'}


def candidate_matches(record, previous):
    matches = []
    for old in previous:
        if old['entry_id'] == record['entry_id']:
            continue
        reasons = []
        if set(record['canonical_urls']) & set(old['canonical_urls']):
            reasons.append('same_article_url')
        if normalized(record['summary']) == normalized(old['summary']):
            reasons.append('same_own_summary')
        event, other = record['event'], old['event']
        if event['key'] and normalized(event['key']) == normalized(other['key']):
            reasons.append('same_event_key')
        entities = {normalized(x) for x in event['entities']} & {normalized(x) for x in other['entities']}
        facts = {normalized(x) for x in event['core_facts']} & {normalized(x) for x in other['core_facts']}
        if facts or (entities and event['action'] and normalized(event['action']) == normalized(other['action']) and event['date'] and event['date'] == other['date']):
            reasons.append('event_facts_candidate')
        a, b = tokens(record['title']), tokens(old['title'])
        overlap = len(a & b) / max(1, len(a | b))
        similarity = SequenceMatcher(None, normalized(record['title']), normalized(old['title'])).ratio()
        if similarity >= .78 or (len(a & b) >= 3 and overlap >= .42):
            reasons.append('similar_title_candidate')
        if reasons:
            matches.append({'entry_id': old['entry_id'], 'title': old['title'], 'archive_url': old['archive_url'],
                            'reasons': reasons, 'editorial_revision_changed': old['revision_id'] != record['revision_id'],
                            'candidate_sha256': sha(json_text({k: old[k] for k in sorted(AUTO_FIELDS | {'event'})}))})
    return matches


def report_for(editions, day):
    previous, report = [], []
    for edition in editions:
        if edition['briefing_date'] > day:
            continue
        for record in edition['records']:
            if edition['briefing_date'] == day:
                report.append({'entry_id': record['entry_id'], 'title': record['title'],
                               'matches': candidate_matches(record, previous)})
            previous.append(record)
    if not report:
        raise ValueError('Missing indexed date: ' + day)
    return report


def review_basis(record, matches):
    return sha(json_text({'record': {k: record[k] for k in sorted(AUTO_FIELDS | {'event'})}, 'matches': matches}))


def gate(root, day):
    Date.fromisoformat(day)
    editions = load_editions(root)
    edition = next((e for e in editions if e['briefing_date'] == day), None)
    if not edition:
        raise ValueError('Run prepare for this date first')
    if edition['origin'] == 'legacy':
        return {'date': day, 'status': 'legacy-index-only', 'records': len(edition['records']),
                'note': 'Historical import is not a source/date/dedup verification.'}
    errors = []
    for record, item in zip(edition['records'], report_for(editions, day)):
        review, event, matches = record['review'], record['event'], item['matches']
        expected = {m['entry_id'] for m in matches}
        if review['basis_sha256'] != review_basis(record, matches):
            errors.append(record['entry_id'] + ': review stale or missing; use review after event/candidate inspection')
        if not event['key'].strip() or not event['entities'] or not event['action'].strip() or not event['core_facts']:
            errors.append(record['entry_id'] + ': event key/entities/action/core_facts required')
        if not review['reason'].strip() or review['decision'] == 'pending':
            errors.append(record['entry_id'] + ': explicit editorial decision/reason required')
        if set(review['matched_entries']) != expected:
            errors.append(record['entry_id'] + ': acknowledge every current candidate ID exactly (rerun candidates)')
        if matches and review['decision'] == 'new':
            errors.append(record['entry_id'] + ': candidates require distinct or update, not new')
        if any('same_article_url' in m['reasons'] or 'same_own_summary' in m['reasons'] for m in matches) and review['decision'] != 'update':
            errors.append(record['entry_id'] + ': same article/summary requires a material update or removal')
        if any('same_own_summary' in m['reasons'] for m in matches):
            errors.append(record['entry_id'] + ': unchanged own summary is not a material update')
        if review['decision'] == 'update' and (not matches or not review['material_change'].strip()):
            errors.append(record['entry_id'] + ': update needs matched prior entries and concrete new facts')
        if not matches and review['decision'] != 'new':
            errors.append(record['entry_id'] + ': no candidates; use new with investigation reason')
    if errors:
        raise ValueError('Pre-publication review blocked:\n' + '\n'.join(errors))
    return {'date': day, 'status': 'reviewed', 'records': len(edition['records']),
            'note': 'Editorial duplicate review passed; source/time verification and deployment are separate.'}


def prepare(root, day, refresh=False):
    with edition_lock(root, day):
        return _prepare(root, day, refresh)


def _prepare(root, day, refresh=False):
    config = load_config(root)
    path = edition_path(root, day)
    fresh = parse_edition(root, day, 'legacy' if day <= config['legacy_through'] else 'reviewed')
    if path.exists():
        if not refresh:
            raise ValueError('Edition exists; use --refresh only after reviewing source changes')
        original = path.read_text(encoding='utf-8')
        old = json.loads(original)
        validate(old, config)
        by_id = {r['entry_id']: r for r in old['records']}
        for record in fresh['records']:
            prior = by_id.get(record['entry_id'])
            if prior and all(prior[k] == record[k] for k in AUTO_FIELDS):
                record['event'], record['review'] = prior['event'], prior['review']
        if path.read_text(encoding='utf-8') != original:
            raise ValueError('Concurrent index change; stopped')
        # Refresh never modifies news or presentation source hashes. Changed entries need new review.
        atomic_write(path, fresh, expected=original)
    else:
        write_new(path, fresh)
    return {'date': day, 'records': len(fresh['records']), 'status': 'prepared; review before gate'}


def review_entry(root, day, entry_id, decision, reason, matched_entries, material_change=''):
    with edition_lock(root, day):
        return _review_entry(root, day, entry_id, decision, reason, matched_entries, material_change)


def _review_entry(root, day, entry_id, decision, reason, matched_entries, material_change=''):
    path = edition_path(root, day)
    original = path.read_text(encoding='utf-8')
    editions = load_editions(root)
    edition = next((e for e in editions if e['briefing_date'] == day), None)
    if not edition or edition['origin'] != 'reviewed':
        raise ValueError('Review command is for newly indexed editions only')
    record = next((r for r in edition['records'] if r['entry_id'] == entry_id), None)
    if record is None:
        raise ValueError('Unknown entry ID')
    matches = next(r['matches'] for r in report_for(editions, day) if r['entry_id'] == entry_id)
    if set(matched_entries) != {m['entry_id'] for m in matches}:
        raise ValueError('Supply --match once for every candidate; inspect candidates first')
    if not reason.strip():
        raise ValueError('A factual editorial reason is required')
    record['review'] = {'decision': decision, 'reason': reason, 'matched_entries': sorted(set(matched_entries)),
                        'material_change': material_change, 'basis_sha256': review_basis(record, matches)}
    atomic_write(path, edition, expected=original)
    return {'entry_id': entry_id, 'status': 'decision recorded; run gate for whole edition'}


def bootstrap(root, through):
    Date.fromisoformat(through)
    target = directory(root)
    if (target / 'config.json').exists() or (target / 'editions').exists():
        raise ValueError('Bootstrap is one-time; existing index will not be overwritten')
    days = sorted(p.name for p in (root / 'news').iterdir() if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.name))
    if not days or days[-1] != through:
        raise ValueError('Bootstrap cutoff must equal latest existing archive date')
    editions = [parse_edition(root, day, 'legacy') for day in days]
    for edition in editions:
        write_new(edition_path(root, edition['briefing_date']), edition)
    write_new(target / 'config.json', {'schema_version': SCHEMA, 'legacy_through': through})
    return {'status': 'historical-index-only', 'dates': len(editions), 'records': sum(len(e['records']) for e in editions)}


def rebuild_sqlite(root):
    """Disposable local cache only, no service and no additional dependencies."""
    editions = load_editions(root)
    target = root / '.cache' / 'article-index.sqlite3'
    target.parent.mkdir(exist_ok=True)
    with sqlite3.connect(target) as db:
        db.execute('BEGIN')
        db.execute('DROP TABLE IF EXISTS articles')
        db.execute('CREATE TABLE articles (entry_id TEXT PRIMARY KEY, article_id TEXT, revision_id TEXT, briefing_date TEXT, title TEXT, summary TEXT, event_key TEXT, canonical_url TEXT, record_json TEXT)')
        for edition in editions:
            for r in edition['records']:
                db.execute('INSERT INTO articles VALUES (?,?,?,?,?,?,?,?,?)',
                           (r['entry_id'], r['article_id'], r['revision_id'], r['briefing_date'], r['title'], r['summary'], r['event']['key'], r['canonical_urls'][0], json.dumps(r, ensure_ascii=False)))
        db.execute('CREATE INDEX IF NOT EXISTS article_url ON articles(article_id)')
        db.execute('CREATE INDEX IF NOT EXISTS article_event ON articles(event_key)')
    return {'status': 'rebuilt local disposable cache', 'path': str(target.relative_to(root))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    boot = sub.add_parser('bootstrap'); boot.add_argument('--through', required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('date'); prep.add_argument('--refresh', action='store_true')
    sub.add_parser('check')
    review = sub.add_parser('review'); review.add_argument('date'); review.add_argument('entry_id')
    review.add_argument('--decision', required=True, choices=['new', 'distinct', 'update'])
    review.add_argument('--reason', required=True); review.add_argument('--match', action='append', default=[])
    review.add_argument('--material-change', default='')
    for name in ('candidates', 'gate'):
        sub.add_parser(name).add_argument('date')
    search = sub.add_parser('search'); search.add_argument('query')
    sub.add_parser('sqlite')
    args = parser.parse_args()
    try:
        if args.command == 'bootstrap':
            result = bootstrap(ROOT, args.through)
        elif args.command == 'prepare':
            result = prepare(ROOT, args.date, args.refresh)
        elif args.command == 'review':
            result = review_entry(ROOT, args.date, args.entry_id, args.decision, args.reason, args.match, args.material_change)
        elif args.command == 'gate':
            result = gate(ROOT, args.date)
        elif args.command == 'sqlite':
            result = rebuild_sqlite(ROOT)
        else:
            editions = load_editions(ROOT)
            if args.command == 'check':
                result = {'status': 'index/source consistency verified', 'dates': len(editions), 'records': sum(len(e['records']) for e in editions)}
            elif args.command == 'candidates':
                result = report_for(editions, args.date)
            else:
                query = normalized(args.query)
                result = [{'entry_id': r['entry_id'], 'title': r['title'], 'archive_url': r['archive_url'], 'source_urls': r['source_urls']}
                          for e in editions for r in e['records'] if query in normalized(json.dumps(r, ensure_ascii=False))]
        print(json_text(result), end='')
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
