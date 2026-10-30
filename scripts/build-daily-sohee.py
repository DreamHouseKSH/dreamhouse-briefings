#!/usr/bin/env python3
"""CPU-only official Sohee synthesis. Staged output only; no service or credentials.
Install pinned dependencies using docs/SOHEE-CLOUD.md. Existing outputs are refused.
"""
import argparse, hashlib, json, os, re, resource, shutil, subprocess, tempfile, time
from pathlib import Path
# Opt out before any ML dependency initializes (official ONNX Runtime process-lifetime switch).
os.environ['ORT_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['DO_NOT_TRACK']='1'
MODEL = 'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice'
REVISION = '0c0e3051f131929182e2c023b9537f8b1c68adfe'
INSTRUCTION = '차분하고 따뜻한 목소리로 자연스럽게 말해주세요.'
SETTINGS = {'model': MODEL, 'revision': REVISION, 'speaker': 'Sohee', 'language': 'Korean', 'instruct': INSTRUCTION,
            'dtype': 'bfloat16', 'attention': 'sdpa', 'threads': 4, 'sample_rate': 24000, 'padding_seconds': 0.2,
            'max_new_tokens': 1024, 'qwen_tts': '0.1.1', 'torch': '2.15.0+cpu'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def narration_hash(data): return hashlib.sha256(json.dumps([s['narration'] for s in data['slides']],ensure_ascii=False).encode()).hexdigest()
def korean_integer(value):
    def group(n):
        out=''
        for unit,label in [(1000,'천'),(100,'백'),(10,'십'),(1,'')]:
            digit,n=divmod(n,unit)
            if digit:out+=('' if digit==1 and unit>1 else '공일이삼사오육칠팔구'[digit])+label
        return out
    high,low=divmod(value,10000)
    return (group(high)+'만' if high else '')+group(low) if value else '공'

def speech_text(text):
    # Pronunciation only. The original transcript remains the source of truth.
    mapping={'Palo Alto Networks':'팔로 알토 네트웍스','Unit 42':'유닛 포티 투',
             'PHP2Shell':'피에이치피 투 셸','PAN-OS':'팬 오에스',
             'CVE(Common Vulnerabilities and Exposures,':'씨브이이, 커먼 벌너러빌리티스 앤드 익스포저스,',
             'PHP':'피에이치피','Mistral':'미스트랄','Large 4':'라지 포','Le Chonk':'르 촌크'}
    for source,target in mapping.items():text=text.replace(source,target)
    pattern=r'(?<![0-9])[0-9]{4}-[0-9]{4,6}(?![0-9])'
    if re.search(pattern,text):
        text=re.sub(pattern,lambda m:' 하이픈 '.join(korean_integer(int(p)) for p in m.group().split('-')),text)
        text=text.replace('·',', ')
    return text
def segment_key(text, seed):
    payload={'text':text,'seed':seed,**SETTINGS}
    spoken=speech_text(text)
    if spoken!=text:payload['spoken_text']=spoken
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def segment_metrics(wave, sr, frames):
    import numpy as np
    wave=np.asarray(wave)
    if sr != SETTINGS['sample_rate'] or wave.ndim != 1 or not len(wave) or not np.isfinite(wave).all(): raise ValueError('Invalid waveform shape/rate/values')
    duration=len(wave)/sr; peak=float(np.abs(wave).max()); rms=float(np.sqrt(np.mean(wave**2)))
    if not .5 < duration < 80 or rms < .002 or peak >= 1 or frames >= SETTINGS['max_new_tokens']-1:
        raise ValueError(f'Suspected silence, clipping, runaway or token truncation: duration={duration}, rms={rms}, peak={peak}, frames={frames}')
    return {'speech_seconds':duration,'samples':len(wave),'rms':rms,'peak':peak,'codec_frames':frames,'finite':True}
def publish_pair(candidate,info,audio,metadata):
    """Create both outputs without overwriting; remove only files created by this call on failure."""
    created=[]
    try:
        with Path(audio).open('xb') as output:
            created.append(Path(audio));output.write(Path(candidate).read_bytes())
        with Path(metadata).open('x') as output:
            created.append(Path(metadata));output.write(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    except Exception:
        for path in created:path.unlink()
        raise

def build(data, date, audio, metadata, model_dir=None, work_dir=None):
    audio,metadata=Path(audio),Path(metadata)
    if audio.exists() or metadata.exists(): raise FileExistsError('Existing outputs preserved; generate into a new staging directory')
    if data.get('date')!=date or not data.get('slides'):raise ValueError('Date mismatch or empty briefing')
    if any(len(s.get('narration',[]))!=3 or any(not isinstance(t,str) or not t.strip() for t in s['narration']) for s in data['slides']):raise ValueError('Each slide needs three nonempty narration cues')
    for binary in ['ffmpeg','ffprobe']:
        if not shutil.which(binary): raise RuntimeError(binary+' is required')
    import importlib.metadata
    for package,version in [('qwen-tts','0.1.1'),('torch','2.15.0+cpu'),('transformers','4.57.3'),('accelerate','1.12.0')]:
        if importlib.metadata.version(package)!=version: raise RuntimeError(f'Expected {package}=={version}; use the tested isolated environment')
    import torch, numpy as np, soundfile as sf
    from qwen_tts import Qwen3TTSModel
    if model_dir is None:
        from huggingface_hub import snapshot_download
        model_dir=snapshot_download(MODEL,revision=REVISION,allow_patterns=['*.json','*.txt','*.safetensors','speech_tokenizer/*'])
    model_dir=Path(model_dir)
    if not (model_dir/'model.safetensors').is_file(): raise ValueError('Missing official model weights')
    # Explicit local override must be the official pinned snapshot, not an arbitrary model.
    official_hashes={'model.safetensors':'38b1d5971bdbd982b561cccec982669a53b0537c3cf5e9bd4778ed07bb2f5137',
                     'speech_tokenizer/model.safetensors':'836b7b357f5ea43e889936a3709af68dfe3751881acefe4ecf0dbd30ba571258'}
    official_hashes.update({'preprocessor_config.json': 'efdde1022ea9d76928bf7a9cd53139138f5ba2e466e837f08f6105ab1af1c119', 'tokenizer_config.json': 'dc3c31c3bdaedd5016382bb3cbe07323026775ad51f5a4fb564505992ae4a670', 'generation_config.json': 'f1b90b4513f3b34c62851049e2492d7b4c5940daf1276f89c82b8ef04127f3aa', 'vocab.json': 'ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910', 'config.json': '17a07f527a1c25ea30b4e023a184482a23d3e279d697b1dc81b1bde498d29cf9', 'merges.txt': '599bab54075088774b1733fde865d5bd747cbcc7a547c5bc12610e874e26f5e3', 'speech_tokenizer/configuration.json': '6bc26d64eb5024b4d1dab5a52371958b429256d6c9d59787f1f5294a54e0cebd', 'speech_tokenizer/preprocessor_config.json': 'fcb3805e597e786d4067706e602f6688524640f8d3396790e2e09b5942fcbdfb', 'speech_tokenizer/config.json': 'ee65bb901c876664ab8707c487157aa1a6ee57c65969b28fb5ec9dc211e68167'})
    for name,expected in official_hashes.items():
        if sha(model_dir/name)!=expected: raise ValueError('Not the pinned official weights: '+name)
    torch.set_num_threads(SETTINGS['threads'])
    started=time.perf_counter(); model=Qwen3TTSModel.from_pretrained(str(model_dir),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
    load_seconds=time.perf_counter()-started
    # Record returned codec length to reject a sample that exhausted its generation cap.
    original=model.model.generate; observed={}
    def measured_generate(*args,**kwargs):
        result=original(*args,**kwargs);observed['frames']=len(result[0][0]);return result
    model.model.generate=measured_generate
    temporary=None
    if work_dir is None: temporary=tempfile.TemporaryDirectory(prefix='dh-sohee-');work_dir=temporary.name
    work=Path(work_dir);work.mkdir(parents=True,exist_ok=True)
    cues=[];files=[];reports=[];cache_hits=0;position_samples=0;total_started=time.perf_counter()
    try:
        for slide,entry in enumerate(data['slides']):
            for step,text in enumerate(entry['narration'],1):
                index=len(cues); seed=42+index; key=segment_key(text,seed);wave_path=work/f'{index:03}-{key[:12]}.wav';report_path=wave_path.with_suffix('.json')
                cached=wave_path.exists() and report_path.exists()
                if cached:
                    cache_hits+=1
                    report=json.loads(report_path.read_text())
                    if report['key']!=key or report['audio_sha256']!=sha(wave_path):raise ValueError('Segment cache changed; review '+str(wave_path))
                    wave,sr=sf.read(wave_path,dtype='float32')
                    segment_metrics(wave[:report['samples']],sr,report['codec_frames'])
                else:
                    for attempt in range(2):
                        torch.manual_seed(seed+10000*attempt);t=time.perf_counter()
                        waves,sr=model.generate_custom_voice(text=speech_text(text),language='Korean',speaker='Sohee',instruct=INSTRUCTION,max_new_tokens=SETTINGS['max_new_tokens'])
                        wave=np.asarray(waves[0],dtype='float32')
                        try:metrics=segment_metrics(wave,sr,observed['frames'])
                        except ValueError:
                            if attempt:raise
                            continue
                        wave=np.concatenate([wave,np.zeros(round(sr*SETTINGS['padding_seconds']),dtype='float32')])
                        sf.write(wave_path,wave,sr,subtype='PCM_16')
                        report={'key':key,'text':text,'spoken_text':speech_text(text),'seed':seed+10000*attempt,'attempt':attempt+1,'generation_seconds':time.perf_counter()-t,
                                'audio_sha256':sha(wave_path),'slide':slide,'step':step,**metrics}
                        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');break
                end=position_samples+len(wave)
                cues.append({'slide':slide,'step':step,'start':round(position_samples/sr,6),'end':round(end/sr,6)})
                position_samples=end;files.append(wave_path);reports.append(report)
                print(json.dumps({'segment':index+1,'total':sum(len(s['narration']) for s in data['slides']), 'seconds':round(len(wave)/sr,3),'generation_seconds':round(report['generation_seconds'],2),'cached':cached},ensure_ascii=False),flush=True)
        # Concatenate PCM samples directly: no per-segment MP3 encoder delay can move cue boundaries.
        full=work/'narration.wav'
        with sf.SoundFile(full,'w',samplerate=sr,channels=1,subtype='PCM_16') as out:
            for path in files:out.write(sf.read(path,dtype='float32')[0])
        audio.parent.mkdir(parents=True,exist_ok=True);metadata.parent.mkdir(parents=True,exist_ok=True)
        candidate=work/'candidate.mp3'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(full),'-c:a','libmp3lame','-b:a','96k','-f','mp3',str(candidate)],check=True)
        decoded=work/'decoded-final.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(candidate),str(decoded)],check=True)
        decoded_info=sf.info(decoded)
        if decoded_info.frames!=position_samples or decoded_info.samplerate!=sr:raise ValueError('MP3 decoded sample count does not match cues')
        info={'date':date,'source':'Existing public archive narration; generated in Linux cloud with official Qwen3-TTS Sohee (CPU)',
              'pronunciation_policy':'Selected technical names use Korean pronunciation and long numeric identifiers use exact-value Korean number reading; public narration unchanged',
              'spoken_text_sha256':hashlib.sha256(json.dumps([[speech_text(t) for t in s['narration']] for s in data['slides']],ensure_ascii=False).encode()).hexdigest(),
              'backend':'sohee','model':MODEL,'model_revision':REVISION,'license':'Apache-2.0','settings':SETTINGS,
              'text_sha256':narration_hash(data),'audio_sha256':sha(candidate),'duration':round(position_samples/sr,6),'cues':cues,
              'validation':{'sample_rate':sr,'decoded_samples':decoded_info.frames,'segments':len(reports),'token_cap_exhausted':False,
                            'load_seconds':round(load_seconds,3),'run_seconds':round(time.perf_counter()-total_started,3),
                            'synthesis_seconds':round(sum(r['generation_seconds'] for r in reports),3),'cache_hits':cache_hits,
                            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
        (work/'segments-report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
        publish_pair(candidate,info,audio,metadata)
        return info
    finally:
        if temporary:temporary.cleanup()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('date');p.add_argument('--data',type=Path,required=True);p.add_argument('--audio',type=Path,required=True);p.add_argument('--metadata',type=Path,required=True);p.add_argument('--model-dir',type=Path);p.add_argument('--work-dir',type=Path)
    a=p.parse_args();print(json.dumps(build(json.loads(a.data.read_text()),a.date,a.audio,a.metadata,a.model_dir,a.work_dir),ensure_ascii=False))
