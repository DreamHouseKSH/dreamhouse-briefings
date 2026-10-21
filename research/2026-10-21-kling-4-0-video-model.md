# 심층 리서치 — Kling 4.0 — '한 번에 30초'를 넘어 '연출'로 가는 비디오 모델

- **요청:** [#3](https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/3)
- **원래 기사:** [2026-10-19 모델 · 2. Kling 4.0 — 한 번에 30초 생성하는 중국발 비디오 모델 (글로벌 출시 발표 10/16)](../news/2026-10-19/모델.md)
- **원문:** https://aiparabellum.com/kling-4-ai-video-model/
- **작성:** 2026-10-21 09:40 KST

<!--
작성 규칙 요약 (상세: docs/WORKFLOW.md 8장 '산출물')
- 구성: 제목 → 리드(한두 문장) → 에세이 본문(소제목 3~5개, 약 1,500~3,000자) → 결론 문단 '그래서 어떻게 보면 되나' → 접힌 '참고 자료'.
- 본문은 이야기처럼 이어지는 산문. 표·글머리표 목록 금지. 무슨 일이 있었나 → 왜 중요한가 → 이해관계자별 시각 → 반론·숨은 쟁점 → 숫자 읽는 법 → 결론.
- 출처는 문장 안에 "매체 이름 + 짧은 링크"로만. 문단마다 링크 도배 금지(문단당 1~2개 정도). 전체 목록은 참고 자료에.
- 전문용어·줄임말은 처음 나올 때 괄호 안에 원어 전체 이름 + 쉬운 뜻:
    GA(General Availability, 누구나 쓸 수 있는 정식 출시)
    SKU(Stock Keeping Unit, 따로 값을 매겨 파는 판매 단위)
    MCP(Model Context Protocol, AI가 외부 도구·데이터에 붙는 표준 규격)
  원어가 없는 우리말 용어는 쉬운 뜻만. 두 번째부터는 줄임말만 써도 됨.
  새 줄임말은 반드시 _data/glossary.yml 에 추가(term·full·ko). 그러면 아래쪽·참고 자료에 다시 나와도
  사이트가 같은 '(원어, 쉬운 뜻)' 풀이를 자동으로 붙임(assets/js/glossary.js, WORKFLOW 3장 2번).
- 회사 발표 수치는 "회사 발표 기준"이라고 밝힘. 확인 못 한 건 "확인되지 않음".
- 출처 없는 일반론은 "예상 쟁점:" 라벨. 반론을 못 찾았으면 "찾은 반론 없음(검색 범위: …)".
- 전문 복제·번역 금지(인용은 한 문장 이내). 이미지는 원문 URL 핫링크만. 지어내기 금지.
- 본문 전체를 <div class="research-essay" markdown="1"> … </div> 로 감싸면 에세이용 줄 간격이 적용됨.
-->

Kling 4.0은 '한 번에 30초를 만든다'는 기록 자체보다, 10개 키프레임과 15개 멀티모달 레퍼런스, 그리고 MCP(Model Context Protocol, AI가 외부 도구·데이터에 붙는 표준 규격)와 커맨드라인 연동으로 '뽑기'가 아니라 '감독하기' 쪽으로 체급을 올렸다는 점이 본질이다. 다만 10-bit HDR(High Dynamic Range, 명암 표현 폭이 넓은 색상 규격)과 2분 연장, 개발자 API(프로그램끼리 기능을 주고받는 창구)는 아직 'coming soon' 상태이고, 성능 비교는 독립 벤치마크가 아니라 주관적 데모와 스폰서성 리뷰에 기대고 있다.
{: .research-lead}

<div class="research-essay" markdown="1">

## 두 단계로 풀린 30초 — Kling 4.0이 온 과정

이야기는 9월 28일에 시작된다. 콰이서우(快手, Kuaishou) 산하 Kling AI가 Kling 4.0을 발표하면서 같은 날 가벼운 티어인 Kling 4.0 Flash를 Ultra Yearly 구독자에게 먼저 풀었다. Flash는 720p 해상도·20초에 묶인 미리보기였고, 이때 올라온 'Kling 4.0 출시' 글 대부분은 사실 Flash를 찍은 것이었다. 정식 모델이 모든 사용자에게 열린 건 10월 15일, 발표의 글로벌 공식화는 10월 16일이었다. 이 두 단계 구조를 모르면 출시 초기의 혼란스러운 리뷰를 잘못 읽게 된다.

스펙을 한 문장으로 정리하면 이렇다. 단일 패스(한 번의 생성)로 최대 30초 분량을 내고, 타임라인 아무 곳에나 최대 10개의 키프레임(동작·장면 전환·카메라 리듬을 찍어 두는 지정 프레임)을 꽂을 수 있으며, 한 번에 최대 15개의 멀티모달 레퍼런스(이미지·영상·캐릭터·음성)를 섞어 참조한다. 멀티 레퍼런스 모드와 키프레임 모드는 한 작업에 혼용할 수 없다는 제한이 있다. 오디오는 스테레오로 나고 10개 이상 언어의 립싱크를 지원하며, 프롬프트는 최대 8000토큰까지 받는다. 출력은 720p·1080p·4K에 21:9 울트라와이드 비율까지 준비됐는데, 4K 자체는 Kling 3.0이 이미 지원하던 것이고 이번에 진짜 새로 붙는 건 10-bit HDR이라는 점을 구분해 둬야 한다 ([kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing)). HDR·2분 연장·개발자 API는 전부 'coming soon' 표기다.

## 왜 중요한가 — '길이'에서 '제어'로 넘어가는 AI 비디오

전작 Kling 3.0(15초)의 두 배, 구글 Veo 3.1의 기본 8초 대비 약 네 배. 숫자 자체도 크지만, 진짜 의미는 제작 경제학에 있다. 지금까지 AI 비디오는 짧은 클립 몇 개를 이어 붙이는 스티치(stitch) 작업이었고, 이어 붙일 때마다 인물 얼굴·조명·움직임이 조금씩 어긋나는 '드리프트'가 최대 적이었다. 스티치를 한 번이라도 걷어내면 쓸 만한 결과물의 비율, 즉 '걸림률'이 바뀐다. 30초는 광고 한 편, 제품 데모 한 컷, 대화 한 마디가 통째로 들어가는 길이다. 여기에 키프레임과 레퍼런스가 결합되면 작업 방식이 바뀐다. 더 이상 '랜덤 뽑기 후 고르기'가 아니라, 시작·중간·끝 프레임을 찍어 두고 인물과 제품을 고정시킨 채 움직임을 채우는 '연출'이 된다. 공식 태그라인 "You Call the Shots"가 그 선언이다.

또 하나 놓치면 안 되는 게 에이전트 연동이다. Kling 4.0은 웹 UI만 내놓은 게 아니라 MCP와 커맨드라인 도구도 같이 열었다. 생성 페이지에는 타임라인·캔버스·에이전트 기능이 붙었다. 이는 Kling이 인간 크리에이터뿐 아니라 에이전트 워크플로우에도 모델을 팔겠다는 뜻이다. AI 비디오의 경쟁축이 '어느 모델이 더 예쁜가'에서 '어느 파이프라인에 더 잘 박히는가'로 넘어가고 있다는 신호로 읽힌다 ([Medium](https://medium.com/@sophie.warren/kling-4-0-in-practice-what-kuaishous-4k-video-model-changes-for-creators-ef467c8d7cc1)).

## 누가 어떻게 보나 — 회사, 크리에이터, 경쟁사, 투자자

콰이서우는 자신 있게 숫자를 던진다. 사용자 1억 명 이상, 서비스 국가 224개국, 기업 고객 5만 곳, 연간 매출 약 5억 달러 — 전부 회사 발표 기준이다. 발표 다음 날인 10월 16일 콰이서우 주가는 3.99% 올랐고, 홍콩 기업공개(IPO, Initial Public Offering, 주식시장에 처음 상장)(2027년, 최소 10억 달러 목표) 보도까지 함께 돌았다 ([금융 뉴스](https://finance.biggo.com/news/2aad1bd2-a1f4-4cde-9860-3ff3a5f5db78)). 부산국제영화제 연계 패널에서는 김성수 감독의 AI 단편 '웜 트레인'이 Kling 4.0으로 제작된 사례로 소개됐다. 모델 출시를 '스튜디오급 제작이 가능하다'는 증명으로 쓰려는 셈이다.

크리에이터 진영의 반응은 대체로 뜨겁다. 테스터 Mark Kretschmann은 "AI 비디오의 또 다른 단계 변화"라고 불렀고, 리뷰어 Khazix는 출시 당일 "사람들에게 Kling이 필요하고, 경쟁이 필요하다"고 썼다 ([kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing)). ByteDance의 Seedance 2.5와 나란히 놓고 같은 프롬프트를 돌린 통제형 A/B도 올라왔는데, Kling이 움직임과 타격감에서 강하고 Seedance가 전반적으로 안정적이라는 주관적 평이 나왔다. 다만 이 비교의 다수가 정식이 아닌 Flash 티어로 돌려졌다는 한계가 있다.

반대편에선 신중한 목소리도 있다. 기술 리뷰 매체 AlexTech.ai는 30초와 스테레오 오디오의 진전은 인정하면서도, 경쟁 구도를 확 뒤집지는 못했다는 평가를 내렸다 ([AlexTech.ai](https://www.alextech.ai/en/news/kling-40-brings-30-second-video-and-stereo-audio-but-doesnt-pull-ahead/)). 원문 매체인 aiparabellum도 "출시 포스트는 증거가 아니다. 작은 테스트부터"라는 실무 조언을 붙였다 ([aiparabellum](https://aiparabellum.com/kling-4-ai-video-model/)). 경쟁사로 시선을 돌리면, 구도는 '중국 모델들의 서로 추격전'이 됐다. 출시를 "바이츠댄스를 쫓는 콰이서우 스핀오프"로 프레임한 외신 보도도 있었고, Sora 2가 2026년 상반기에 소비자·API 모두 문을 닫으면서 (laozhang.ai의 정리) 구도의 한 축은 아예 사라졌다.

## 반론과 숨은 쟁점 — 숫자를 어떻게 읽어야 하나

가장 먼저 짚을 건 '출시'의 정의다. 10월 15일에 열린 건 풀 모델의 소비자 접근이지, 광고된 전체 기능이 아니다. 10-bit HDR, 2분 연장, 개발자 API는 여전히 미출시이고, 출시 노트에 시스템 카드(system card, 모델의 능력·한계·위험을 기록한 공식 문서)도, 표준 벤치마크표도 없었다. 그러니 '30초 생성'이라는 능력 자체는 실재하지만, 그 품질의 객관적 좌표는 아직 없는 상태다. 독립 벤치마크가 공개되기 전까진 '누가 더 좋은가'라는 질문에 정답이 없다.

둘째, 데모를 조심해야 한다. 9월 말 얼리 액세스 기간에 올라온 공개 데모 중 상당수는 #ad 표기나 스폰서 초대가 붙어 있었다. 샘플 자체가 홍보 쪽으로 치우쳐 있다는 뜻이다. 정직한 리뷰어의 잣대는 그래서 더 귀하다. Medium의 리뷰는 10-bit HDR·4K·2분 연장을 "coming soon"으로 명확히 구분해 과장을 차단하는 식으로 썼다 ([Medium 리뷰](https://medium.com/@abirkhanabirkhan557/kling-4-0-launched-30-second-ai-video-keyframes-honest-review-ced1a01fb110)).

셋째, 가격 숫자를 읽는 법이다. 보고된 가격은 1080p 기준 초당 15크레딧, 720p 기준 초당 10크레딧이다. 30초 1080p 클립 한 개가 450크레딧, 한 테스터의 요금제 기준으로 약 16위안이다. 그런데 AI 비디오의 진짜 가격은 '클립 한 개당'이 아니라 '쓸 만한 클립 한 개당'이다. 한 샷을 세 번 돌려야 건지면 1,350크레딧이 된다. Kling 4.0의 재시도율(reroll rate, 쓸 만한 결과가 나올 때까지 돌린 횟수)은 아직 공개된 실측이 없으니, 450크레딧은 하한선으로만 읽어야 한다. 크레딧 1개월 소멸 정책 같은 실사용 변수도 기사 원문이 경고한 그대로다. 아카이브 기사에 적힌 사용자 수·매출 수치 역시 전부 회사 발표임을 다시 한 번 못 박는다.

## 그래서 어떻게 보면 되나

Kling 4.0은 '더 긴 영상 생성기'라기보다 '연출 도구'로의 이동을 알리는 이정표로 보는 게 정확하다. 30초 단일 패스, 10개 키프레임, 15개 레퍼런스, MCP·CLI 연동 — 이 조합은 광고·숏폼·제품 데모 같은 실무 파이프라인에 바로 얹을 수 있는 모양새를 갖췄다. 다만 지금은 '살 수 있는 출시'와 '광고된 출시'를 구분해야 하는 시점이다. HDR·2분 연장·API 타임라인이 열리기 전까진 납품 약속에 이 기능을 걸지 말 것, Flash로 찍은 데모와 풀 모델을 구분할 것, 그리고 무엇보다 직접 돌려볼 것. aiparabellum의 조언처럼 작은 테스트부터 시작해 20~30초 구간에서 인물이 무너지지 않는지, 재시도가 몇 번 필요한지를 재는 게 450크레딧이라는 숫자보다 백 배 유용하다. 이 판단이 바뀔 조건도 명확하다. 독립 벤치마크가 나오거나, HDR·API가 실제로 열리거나, Seedance 같은 경쟁 모델이 연출 제어에서 한 발 더 나아가는 순간, 지도는 다시 그려진다.

</div>

---

<details class="research-refs" markdown="1">
<summary>참고 자료 — 핵심 수치 · 체크포인트 · 출처 목록</summary>

### 핵심 수치

| 수치·사실 | 출처 | 검증 여부 |
|---|---|---|
| 단일 패스 최대 30초 (Kling 3.0의 15초의 2배) | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing), [Medium](https://medium.com/@abirkhanabirkhan557/kling-4-0-launched-30-second-ai-video-keyframes-honest-review-ced1a01fb110) | 회사 발표(공식 발표·출시 노트 기준), 테스터 실측과 일치 |
| 키프레임 최대 10개, 멀티모달 레퍼런스(Omni Reference) 최대 15개 | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing) | 회사 발표 기준 |
| 프롬프트 최대 8000토큰, 스테레오 오디오, 10개 이상 언어 립싱크 | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing), [AlexTech.ai](https://www.alextech.ai/en/news/kling-40-brings-30-second-video-and-stereo-audio-but-doesnt-pull-ahead/) | 회사 발표 기준 |
| 가격: 1080p 초당 15크레딧·720p 초당 10크레딧, 30초 1080p=450크레딧(약 16위안, 테스터 요금제 기준) | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing) | 독립 확인(테스터 실측 Khazix + 요금표 일치), 단 재시도율 미포함 |
| 10-bit HDR·2분 연장·개발자 API 미출시 ("coming soon") | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing), [Medium 리뷰](https://medium.com/@abirkhanabirkhan557/kling-4-0-launched-30-second-ai-video-keyframes-honest-review-ced1a01fb110) | 회사 발표(출시 노트 표기 기준) |
| 4K는 Kling 3.0부터 지원 — 4.0 신규 기능 아님 | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing) | 독립 확인 |
| 사용자 1억+·224개국·기업 고객 5만·연매출 약 5억 달러 | [금융 뉴스](https://finance.biggo.com/news/2aad1bd2-a1f4-4cde-9860-3ff3a5f5db78), [aiparabellum](https://aiparabellum.com/kling-4-ai-video-model/) | 회사 발표 |
| 콰이서우 주가 +3.99% (2026-10-16), 홍콩 IPO 2027년·최소 10억 달러 목표 보도 | [금융 뉴스](https://finance.biggo.com/news/2aad1bd2-a1f4-4cde-9860-3ff3a5f5db78) | 보도 인용(독립 미확인) |
| 시스템 카드·표준 벤치마크 미공개 | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing) | 독립 확인(출시 자료에 없음) |
| Seedance 2.5 대비: Kling=움직임 강함·Seedance=안정적 (주관적 A/B) | [kie.ai](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing) | 테스터 주관 평가(표준 테스트 아님), 대다수 Flash 기반 |

### 앞으로 볼 체크포인트

- Kling 공식 릴리스 노트: 10-bit HDR·2분 연장·개발자 API 출시 시점
- 독립 벤치마크(Artificial Analysis 등)의 Kling 4.0 품질·속도 측정
- 실사용자의 재시도율(reroll rate) 실측과 지역별 크레딧 환산가
- Seedance·Veo 3.1·Gemini Omni Flash 1.1 등 경쟁 모델의 연출 제어 기능 대응
- 콰이서우 홍콩 IPO 진행 상황 (모델 사업의 자금줄과 직결)

### 출처 목록

1. [Kling 4.0 AI 비디오 모델 출시 — aiparabellum, 2026-10-16](https://aiparabellum.com/kling-4-ai-video-model/)
2. [Kling 4.0 Release: 30s Clips, 10 Keyframes, Pricing — kie.ai, 2026-10-16경](https://kie.ai/blog/kling-4-0-release-analysis-30-second-clips-keyframes-pricing)
3. [Kling 4.0 Launched: 30-Second AI Video, Keyframes & Honest Review — Medium, 2026-10-19경](https://medium.com/@abirkhanabirkhan557/kling-4-0-launched-30-second-ai-video-keyframes-honest-review-ced1a01fb110)
4. [Kling 4.0 in Practice: What Kuaishou's 4K Video Model Changes for Creators — Medium, 2026-10-19경](https://medium.com/@sophie.warren/kling-4-0-in-practice-what-kuaishous-4k-video-model-changes-for-creators-ef467c8d7cc1)
5. [Kling 4.0 brings 30-second video and stereo audio, but doesn't pull ahead — AlexTech.ai, 2026-10-20](https://www.alextech.ai/en/news/kling-40-brings-30-second-video-and-stereo-audio-but-doesnt-pull-ahead/)
6. [Kling AI Unveils 4.0 Model With 30-Second Clips, Eyes Pro Film Market — 금융 뉴스, 2026-10-16](https://finance.biggo.com/news/2aad1bd2-a1f4-4cde-9860-3ff3a5f5db78)
7. [Best AI Video Generator 2026 — tech-insider.org, 2026-10-11경](https://tech-insider.org/best-ai-video-generator-2026/)
8. [Seedance 2.5 vs Veo 3.1 vs Gemini Omni: Which Fits Your Job — laozhang.ai 블로그, 2026-10-01경](https://blog.laozhang.ai/en/posts/seedance-2-vs-veo-3-vs-sora-2)
9. [Kling vs Veo 3 (2026): Which AI Video Generator Wins? — flowjam, 2026-08경](https://www.flowjam.com/blog/kling-vs-veo-3-2026)

</details>
