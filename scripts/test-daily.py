#!/usr/bin/env python3
"""Content completeness and reproducible publication checks (no synthesis)."""
import importlib.util,json,subprocess,tempfile,unittest,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('daily',Path(__file__).with_name('build-daily.py'));daily=importlib.util.module_from_spec(spec);spec.loader.exec_module(daily)
class DailyChecks(unittest.TestCase):
    def test_every_archive_item_and_card(self):
        for date,counts in [('2026-10-28',(11,10)),('2026-10-29',(11,10)),('2026-10-30',(5,7))]:
            data=daily.make(date)
            self.assertEqual((data['news_count'],data['github_count']),counts)
            ids={x['id'] for x in data['items']}
            self.assertEqual(len(ids),sum(counts))
            self.assertEqual({x for s in data['slides'] for x in s['refs']},ids)
            self.assertTrue(all(len(s['nodes'])==len(s['labels'])==len(s['narration'])==3 for s in data['slides']))
            self.assertTrue(all('/'+date in i['detail'] and i['source'].startswith('https://') for i in data['items']))
    def test_reproducible_without_audio_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ['first','second']:
                subprocess.run([sys.executable,str(Path(daily.__file__)),'2026-10-30','--plan',directory+'/'+name],check=True,env={'PATH':'/nonexistent'},capture_output=True)
            for p in (Path(directory)/'first').iterdir():
                self.assertEqual(p.read_bytes(),(Path(directory)/'second'/p.name).read_bytes())
    def test_missing_input_is_not_a_completed_edition(self):
        with self.assertRaises(FileNotFoundError):daily.make('2000-01-01')
    def test_all_complete_editions_and_audio_checksums(self):
        for date in ['2026-10-27','2026-10-28','2026-10-29','2026-10-30']:self.assertEqual(daily.check(date)['status'],'verified')
    def test_preserves_existing_edition(self):
        paths=daily.paths('2026-10-28');before={p:p.read_bytes() for p in paths}
        subprocess.run([sys.executable,str(Path(daily.__file__)),'2026-10-28','--audio'],check=True,capture_output=True)
        self.assertEqual(before,{p:p.read_bytes() for p in paths})
if __name__=='__main__':unittest.main()
