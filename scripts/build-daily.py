#!/usr/bin/env python3
"""Build a complete dated motion deck from the existing news + GitHub archive.
Standard library only. No model, API, credentials, network or news invention.
--audio uses the existing installed macOS Yuna route. --check is portable.
"""
import argparse,hashlib,html,importlib.util,json,re,tempfile,os
from pathlib import Path
from datetime import date as Date
ROOT=Path(__file__).resolve().parents[1]
VERSION=1

def plain(text):
    text=re.sub(r'!\[[^\]]*\]\([^\n]+\)','',text)
    text=re.sub(r'\[([^\]]+)\]\([^\n)]+\)',r'\1',text)
    text=re.sub(r'<[^>]+>|\{:[^}]+\}','',text)
    return html.unescape(re.sub(r'[*`#]','',text)).strip()
def paragraphs(text):
    return [plain(p) for p in re.split(r'\n\s*\n',text) if plain(p) and not p.lstrip().startswith(('>','-','!','<','{:'))]
def first(text):
    return re.split(r'(?<=[.!?。])\s+',text.strip())[0]
def slug(text):
    text=re.sub(r'<[^>]*>','',text).lower()
    return re.sub(r'\s','-',re.sub(r'[^\w\s-]','',text)).strip('-')
def digest(files):
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
def inputs(date):
    files=sorted((ROOT/'news'/date).glob('*.md')); github=ROOT/'github'/f'{date}.md'
    if not files or not github.exists():raise FileNotFoundError('News and GitHub must both be complete before generating this date')
    return files+[github]
def section(body,name):
    m=re.search(r'^### '+name+r'\s*\n(.*?)(?=^### |\Z)',body,re.M|re.S)
    return m.group(1).strip() if m else ''
def make(date):
    files=inputs(date);items=[];slides=[];notices=[]
    for p in files[:-1]:
        src=p.read_text();notice=re.search(r'^> (.+)',src,re.M)
        if notice:notices.append(p.stem+': '+plain(notice[1]))
        matches=list(re.finditer(r'^## (\d+\. .+)$',src,re.M))
        if not matches:raise ValueError('No numbered news found: '+str(p))
        for j,m in enumerate(matches):
            title=m[1];body=src[m.end():matches[j+1].start() if j+1<len(matches) else len(src)]
            summary=paragraphs(section(body,'요약') or section(body,'해석'))
            if not summary:raise ValueError('Missing summary: '+title)
            links=re.findall(r'https://[^\s)<>]+',body.split('###')[0])
            if not links:raise ValueError('Missing source: '+title)
            caveat=re.search(r'^- \*\*논조 점검:\*\* (.+)',body,re.M)
            caveat=plain(caveat[1]) if caveat else '적용 조건과 검증 한계는 상세 기사에서 함께 확인하세요.'
            if p.stem=='X':
                access=re.search(r'^- \*\*접근 상태:\*\* (.+)',body,re.M)
                if access:caveat=plain(access[1])+' '+caveat
            identity='n'+str(len(items)+1)
            item={'id':identity,'field':p.stem,'title':title,'short':re.sub(r'^\d+\. ','',title),'summary':summary[0],
                  'metadata':plain(body.split('###')[0]),'detail':f'/news/{date}/{p.stem}.html#'+slug(title),'source':links[0],'sources':links,'caveat':caveat}
            items.append(item)
            points=[first(summary[0]),first(summary[1]) if len(summary)>1 else '구체적인 적용 범위와 후속 계획은 상세 기사에서 확인할 수 있습니다.',first(caveat)]
            slides.append({'kicker':p.stem+' / '+date,'title':item['short'],'intro':points[0], 'nodes':['발표 내용','적용 범위','검증 범위'],
                           'labels':points,'kind':'shield' if '보안' in title else 'matrix','refs':[identity],
                           'note':caveat,'narration':[points[0],points[1],'여기서 확인할 한계입니다. '+points[2]]})
    news_count=len(items);github=files[-1].read_text();note=re.search(r'^> (.+)',github,re.M)
    if note:notices.append('GitHub: '+plain(note[1]))
    for match in re.finditer(r'<article\b[^>]*data-repo="([^"]+)"[^>]*>(.*?)</article>',github,re.S):
        repo,body=match.groups();title=repo;identity='g'+str(len(items)-news_count+1)
        def part(name):
            m=re.search(r'\*\*'+name+r'\*\*\s*[—–-]\s*(.*?)(?=\n\n|\Z)',body,re.S)
            if not m:raise ValueError('Missing '+name+' for '+repo)
            return plain(m[1])
        what,how,warn,why=part('무엇인가'),part('어떻게 쓰나'),part('주의할 점'),part('왜 지금 뜨나')
        item={'id':identity,'field':'GitHub','title':title,'short':repo,'summary':what,
              'detail':f'/github/{date}.html#'+repo.lower().replace('/','-'),'source':'https://github.com/'+repo,'caveat':warn,'trend':why}
        items.append(item)
        points=[first(what),first(how),first(warn)]
        slides.append({'kicker':'GITHUB / '+date,'title':repo,'intro':first(why),'nodes':['기능','사용 방법','주의점'],
                       'labels':points,'kind':'shield' if 'security' in repo.lower() else 'orbit','refs':[identity],
                       'note':first(warn),'narration':['다음은 '+repo.replace('/','의 ')+'입니다. '+points[0],points[1],points[2]]})
    gh_count=len(items)-news_count
    if not gh_count:raise ValueError('No GitHub cards found')
    intro={'kicker':'THE DAILY / '+date,'title':date+'\n하루 전체 브리핑','intro':f'뉴스 {news_count}건과 GitHub {gh_count}개 카드를 함께 읽습니다. 관계도는 원문 요약을 구조화한 편집 해설이며 인과관계나 정량 통계가 아닙니다.',
           'nodes':['뉴스','개발 도구','확인점'],'labels':[f'아카이브 뉴스 {news_count}건',f'GitHub 카드 {gh_count}개','조건·출처·검증 한계'],'kind':'orbit','refs':[],
           'narration':[f'{date[5:7]}월 {date[8:10]}일 하루 브리핑을 시작하겠습니다. 오늘 아카이브의 뉴스 {news_count}건을 차례로 살펴보겠습니다.',f'이어서 깃허브 도구 {gh_count}개를 기능과 사용 방법, 주의점으로 나눠 설명하겠습니다.','발표와 계획, 실제로 확인된 결과는 구분해서 읽어 주세요. 모든 항목의 상세 기사와 원문은 아래 목차에 연결했습니다.']}
    end={'kicker':'READ / VERIFY / FOLLOW UP','title':'사실과 조건을 나누고\n원문으로 확인하세요.','intro':f'뉴스 {news_count}건·GitHub {gh_count}개를 모두 연결했습니다. 자동 발표 후에도 정적 목차와 날짜별 상세 기사로 돌아갈 수 있습니다.',
         'nodes':['발표 사실','남은 조건','상세 원문'],'labels':['발표값·회사 주장 구분','계획·미확인 범위 확인','논조와 다른 시각까지 읽기'],'kind':'matrix','refs':[],
         'narration':['오늘의 전체 항목을 살펴봤습니다. 발표된 수치와 계획을 이미 완료된 결과로 바꿔 읽지 않는 것이 중요합니다.','도구의 인기나 모델의 자체 평가가 실제 작업의 품질과 안전성을 보장하는 것은 아닙니다.','아래 전체 목차에서 각 항목의 원문과 상세 기사, 검증 한계를 다시 확인하실 수 있습니다. 오늘 발표를 마칩니다.']}
    return {'date':date,'generator_version':VERSION,'source_hashes':digest(files),'news_count':news_count,'github_count':gh_count,
            'scope':f'뉴스 {news_count}건 · GitHub {gh_count}개 카드. 기존 공개 아카이브에서 생성했습니다. 원문의 날짜·조사 구간·회사 주장·미확인 범위는 아래 수집 안내와 상세 기사에서 확인하세요. 도형은 편집 해설입니다.',
            'notices':notices,'items':items,'slides':[intro]+slides+[end]}

def paths(date):
    key=date.replace('-','')
    return [ROOT/f'_data/day_{key}.json',ROOT/f'daily/{date}.html',ROOT/f'assets/audio/{date}-narration.mp3',ROOT/f'_data/day_{key}_audio.json']
def check(date):
    data_path,page,audio,meta=paths(date)
    for p in [data_path,page,audio,meta]:
        if not p.is_file():raise ValueError('Missing published component: '+str(p.relative_to(ROOT)))
    data=json.loads(data_path.read_text());info=json.loads(meta.read_text())
    if 'source_hashes' in data:
        if data['source_hashes']!=digest(inputs(date)):raise ValueError('Archive changed; stop and review existing edition instead of overwriting it')
        fresh=make(date)
        if data!=fresh:raise ValueError('Generated data differs from current parser; review before changing an existing edition')
    assert info['date']==date
    assert info['text_sha256']==hashlib.sha256(json.dumps([s['narration'] for s in data['slides']],ensure_ascii=False).encode()).hexdigest()
    assert info['audio_sha256']==hashlib.sha256(audio.read_bytes()).hexdigest()
    assert len(info['cues'])==len(data['slides'])*3
    last=0
    for i,c in enumerate(info['cues']):
        assert c['slide']==i//3 and c['step']==i%3+1 and abs(c['start']-last)<0.001 and c['end']>c['start']
        last=c['end']
    assert abs(info['duration']-last)<0.001
    return {'date':date,'items':len(data['items']),'slides':len(data['slides']),'seconds':info['duration'],'status':'verified'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('date');p.add_argument('--audio',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--if-ready',action='store_true');p.add_argument('--plan',type=Path,help='Portable HTML/JSON preview directory; no audio or publication');args=p.parse_args()
    Date.fromisoformat(args.date)
    if args.check:print(json.dumps(check(args.date)));return
    try:data=make(args.date)
    except FileNotFoundError:
        if args.if_ready:print('PENDING: both completed news and GitHub are required');return
        raise
    key=args.date.replace('-','')
    page_text=f'---\nlayout: default\ntitle: 하루 발표 — {args.date}\ndaily: true\nbriefing_date: "{args.date}"\nedition_key: day_{key}\naudio_key: day_{key}_audio\n---\n{{% include daily-deck.html %}}\n'
    if args.plan:
        args.plan.mkdir(parents=True,exist_ok=True)
        for name,text in [(f'day_{key}.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n'),(f'{args.date}.html',page_text)]:
            with (args.plan/name).open('x') as output:output.write(text)
        print(json.dumps({'date':args.date,'status':'HTML/JSON preview only; no audio generated','items':len(data['items'])}));return
    targets=paths(args.date)
    if any(x.exists() for x in targets):print(json.dumps(check(args.date)));return
    if not args.audio:raise ValueError('Use --audio to build all components together; partial silent editions are not published')
    module=importlib.util.spec_from_file_location('audio_builder',ROOT/'scripts/build-daily-audio.py');audio_builder=importlib.util.module_from_spec(module);module.loader.exec_module(audio_builder)
    with tempfile.TemporaryDirectory(prefix='dh-edition-') as folder:
        work=Path(folder);staged=[work/str(i) for i in range(4)]
        staged[0].write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        key=args.date.replace('-','')
        staged[1].write_text(page_text)
        audio_builder.build(data,args.date,staged[2],staged[3])
        if data['source_hashes']!=digest(inputs(args.date)):raise ValueError('Source changed during generation; stopped without writing')
        if any(x.exists() for x in targets):raise ValueError('Another writer created this date; stopped without overwriting')
        created=[]
        try:
            for source,target in zip(staged,targets):
                target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as out:out.write(source.read_bytes())
                created.append(target)
        except Exception:
            for target in created:target.unlink()
            raise
    print(json.dumps(check(args.date)))
if __name__=='__main__':main()
