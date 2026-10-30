#!/usr/bin/env python3
"""Continuous narration from public JSON, using installed macOS Yuna only."""
import argparse, hashlib, json, shutil, subprocess, tempfile
from pathlib import Path

def build(data, date, audio, metadata):
    if not shutil.which('say') or not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('Installed macOS say/Yuna, ffmpeg and ffprobe are required; no audio was generated')
    with tempfile.TemporaryDirectory(prefix='dh-narration-') as folder:
        work=Path(folder); cues=[]; files=[]; position=0.0
        for slide_index,slide in enumerate(data['slides']):
            for step,text in enumerate(slide['narration'],1):
                n=len(cues); source=work/f'{n:03}.aiff'; wave=work/f'{n:03}.wav'
                subprocess.run(['say','-v','Yuna','-r','185','-o',str(source),text],check=True)
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-af','apad=pad_dur=0.20','-ar','22050','-ac','1',str(wave)],check=True)
                duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(wave)],text=True))
                if duration<=0: raise RuntimeError('Empty audio segment')
                cues.append({'slide':slide_index,'step':step,'start':round(position,6),'end':round(position+duration,6)})
                position+=duration; files.append(wave)
        manifest=work/'concat.txt'; manifest.write_text(''.join("file '"+str(p)+"'\n" for p in files))
        subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c:a','libmp3lame','-b:a','96k','-f','mp3',str(audio)],check=True)
        info={'date':date,'source':'Existing public archive narration; locally generated with installed macOS Yuna voice',
              'text_sha256':hashlib.sha256(json.dumps([s['narration'] for s in data['slides']],ensure_ascii=False).encode()).hexdigest(),
              'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'duration':round(position,6),'cues':cues}
        metadata.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
        return info

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('date',help='YYYY-MM-DD');parser.add_argument('--data',type=Path);parser.add_argument('--audio',type=Path);parser.add_argument('--metadata',type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1];key=args.date.replace('-','')
    data=args.data or root/f'_data/day_{key}.json';audio=args.audio or root/f'assets/audio/{args.date}-narration.mp3';metadata=args.metadata or root/f'_data/day_{key}_audio.json'
    if audio.exists() or metadata.exists():parser.error('Existing audio/metadata preserved; review before replacing')
    audio.parent.mkdir(parents=True,exist_ok=True)
    info=build(json.loads(data.read_text()),args.date,audio,metadata)
    print(json.dumps({'date':args.date,'seconds':info['duration'],'cues':len(info['cues'])}))
