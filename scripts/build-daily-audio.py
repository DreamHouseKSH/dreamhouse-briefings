#!/usr/bin/env python3
"""Build one continuous Korean narration using the installed macOS Yuna voice.
No API, account, network, voice download, or private text is used.
"""
import hashlib,json,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'_data/day_20261027.json').read_text())
out=root/'assets/audio';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='dh-narration-') as folder:
    work=Path(folder);cues=[];files=[];position=0.0
    for slide_index,slide in enumerate(data['slides']):
        for step,text in enumerate(slide['narration'],1):
            n=len(cues);source=work/f'{n:02}.aiff';wave=work/f'{n:02}.wav'
            subprocess.run(['say','-v','Yuna','-r','185','-o',str(source),text],check=True)
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-af','apad=pad_dur=0.20','-ar','22050','-ac','1',str(wave)],check=True)
            duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(wave)],text=True))
            cues.append({'slide':slide_index,'step':step,'start':round(position,6),'end':round(position+duration,6)})
            position+=duration;files.append(wave)
    manifest=work/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in files))
    audio=out/'2026-10-27-narration.mp3'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c:a','libmp3lame','-b:a','96k',str(audio)],check=True)
    info={'date':'2026-10-27','source':'Existing public slide narration; locally generated with installed macOS Yuna voice','text_sha256':hashlib.sha256(json.dumps([s['narration'] for s in data['slides']],ensure_ascii=False).encode()).hexdigest(),'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'duration':round(position,6),'cues':cues}
    (root/'_data/day_20261027_audio.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'file':str(audio),'bytes':audio.stat().st_size,'seconds':position,'sentences':len(cues)},ensure_ascii=False))
