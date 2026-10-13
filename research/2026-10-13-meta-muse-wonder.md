# 심층 리서치 — Meta Muse Wonder, '프론티어 복귀'는 진짜지만 가장 센 모델은 아직 손에 안 잡힌다

- **요청:** [#2](https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/2)
- **원래 기사:** [2026-10-13 모델 · 1. Meta, Muse Wonder·Muse Wonder Full 공개](../news/2026-10-13/모델.md)
- **원문:** https://about.fb.com/news/2026/10/introducing-muse-wonder-models/
- **작성:** 2026-10-13 13:55 KST

Meta가 처음으로 OpenAI·Anthropic 최상위 모델과 같은 줄에 설 만한 모델을 내놓은 건 독립 평가로도 확인됩니다. 다만 1등은 아니고(독립 종합 점수 56 대 Claude Opus 5.5의 58), 가장 센 Wonder Full은 API(Application Programming Interface, 프로그램끼리 기능을 주고받는 창구)로 못 쓰며, 개발자가 실제로 붙일 수 있는 일반 Wonder는 값이 Opus와 같은 프리미엄 구간이라 "성능은 따라잡았고, 쓸모와 값어치는 이제부터 증명"하는 단계로 보는 게 정확합니다.
{: .research-lead}

![Meta Muse Wonder 모델 발표 대표 이미지](https://about.fb.com/wp-content/uploads/2026/10/museWonder_socialShare.jpg?w=1200)

이미지 출처: Meta(about.fb.com) 원문 페이지 (원본 이미지 링크, 복제 저장 아님)
{: .research-credit}

<div class="research-essay" markdown="1">

## 무슨 일이 있었나 — Meta의 첫 '프론티어' 모델

10월 12일(미국 시간) Meta의 MSL(Meta Superintelligence Labs, 메타 초지능 연구소 — 스케일AI 창업자 알렉산더 왕이 이끄는 AI 조직)이 Muse Wonder와 Muse Wonder Full 두 모델을 공개했습니다. 회사 연구 블로그([Meta AI](https://research.meta.ai/blog/muse-wonder))는 이를 "개인·업무용 에이전트(목표를 받아 앱과 도구를 넘나들며 일을 끝까지 이어 가는 AI)에서 최고 성능"을 내는 모델이자 '개인 초지능'으로 가는 큰 도약이라고 소개했어요. 6주 전 나온 Muse Spark 1.3의 윗단을 맡는 모델로, 기가와트급 Prometheus 데이터센터(오하이오 중부에 올해 가동한 Meta의 대형 AI 학습 시설)에서 사전학습과 RL(Reinforcement Learning, 강화학습 — 잘한 행동에 보상을 줘서 배우게 하는 방식)을 키워 만들었다고 합니다. 입력은 텍스트·이미지·오디오·비디오를 받고 답은 텍스트로만 내며, 컨텍스트 창(context window, 한 번에 읽고 기억하며 처리할 수 있는 글의 양)은 약 100만 토큰입니다.

Meta가 앞세운 두 기능은 Active Memory와 Active Focus예요. 앞의 것은 대화가 바뀌어도 사용자에 관한 중요한 맥락을 기억했다가 필요할 때 꺼내 쓰는 능력이고, 뒤의 것은 막히면 다른 방법을 시도하고 중요한 행동 전에는 사용자에게 확인을 받는 끈기입니다. 왕은 CNBC([인터뷰](https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html))에서 식당 예약처럼 현실 작업의 장애물 앞에서 멈추지 않고 우회하도록 일부러 훈련했다고 했어요. 다만 두 기능이 정확히 어떤 구조로 구현됐는지는 공개 자료에서 확인되지 않았고, 성능 근거는 MemoryBench·FocusBench 같은 회사가 강조한 평가 점수가 대부분입니다.

## 왜 중요한가 — Llama의 Meta가 '닫힌 프리미엄'으로 돌아섰다

이번 발표의 진짜 의미는 점수보다 사업 방식의 전환에 있습니다. VentureBeat([분석](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api))가 짚었듯 Meta는 예전 Llama로 '내려받아 내 서버에서 돌리는 모델'을 대중화한 회사인데, Wonder는 두 모델 모두 가중치(weights, 모델이 학습으로 얻은 수십억 개 숫자 — 이게 있어야 직접 돌릴 수 있음)를 공개하지 않는 프로프라이어터리(proprietary, 회사가 독점하는 비공개) 모델입니다. 작은 Muse Glimmer는 Apache 2.0 라이선스(상업적 사용까지 자유로운 오픈소스 라이선스)로 풀었지만, 맨 꼭대기 모델은 셀프호스팅(self-hosting, 내 서버에 직접 설치해 쓰는 것)이 불가능합니다.

게다가 판매 경로가 셋으로 갈립니다. 일반 Wonder는 Meta Model API에서 입력 100만 토큰당 4달러, 출력 20달러(캐시된 입력은 0.20달러)에 팔리고, 더 센 Wonder Full은 코딩 에이전트 Muse Code의 월 50달러·200달러 구독에서만 쓸 수 있으며, 소비자용 Muse 앱에서 Wonder를 쓰려면 월 20달러나 100달러 구독이 필요하다고 CNBC는 전했습니다. CNBC가 기사 제목을 '사용자가 돈을 낼 의향이 있는지 시험하는 출시'로 잡은 이유가 여기 있어요. 광고 말고 AI로 직접 돈을 버는 길을 Meta가 처음 본격적으로 시험하는 셈입니다.

## 누가 어떻게 보나 — 독립 평가는 '진짜 상승', 시장은 '조심스러운 환영'

가장 무게 있는 제3자 시각은 독립 벤치마크 기관 Artificial Analysis([평가](https://artificialanalysis.ai/articles/muse-wonder))입니다. 자체 종합 지표인 Intelligence Index v4.3(추론·지식·코딩·업무 과제 10가지를 직접 돌려 합친 점수)에서 Wonder Full은 56, Wonder는 52를 받아 Spark 1.3의 48에서 각각 8점, 4점 올랐어요. 논조는 긍정이지만 단서가 분명합니다. 특히 Terminal-Bench 4.0(터미널 명령으로 실제 작업을 해내는 에이전트 시험)이 33%에서 57%로 뛰었고, 환각률(없는 사실을 지어내는 비율)이 23%로 최상위권 중 두 번째로 낮다고 했어요. 반면 지식 점수(AA-Omniscience)는 30으로 Opus 5.5(46)나 GPT-6 Astra(43)에 한참 못 미친다고 선을 그었습니다. 코딩 에이전트 지수에서는 Muse Code 안의 Wonder Full이 68로, Claude Code에서 돌린 Sonnet 5.5(68)와 같았습니다.

언론 논조는 대체로 중립에서 약한 긍정입니다. TechCrunch([기사](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder/))는 "Meta의 첫 프론티어 모델 시도"라 평하면서도 비교 점수가 Meta 자체 테스트라는 점을 적었고, 주가는 하루 3.4% 올랐다고 WSJ(Wall Street Journal, 미국 경제 일간지 월스트리트저널)가 보도했어요. 개발자 반응은 더 갈립니다. 인기 개발 유튜버 Theo(@theo)는 X에 "S등급: Opus 5.5, Muse Wonder"라는 순위를 올려 66만 회 넘게 노출됐지만, 같은 글 아래에는 Extra High 설정으로 써 봤는데 결과가 실망스러웠다는 개인 사용자 답글도 여럿 달렸습니다. 이런 SNS 반응은 표본이 작고 검증되지 않은 개인 경험이라 '분위기'로만 읽는 게 맞습니다.

## 반론과 숨은 쟁점, 숫자 읽는 법

첫 번째 쟁점은 Meta 비교표 자체의 신뢰도입니다. SiliconANGLE([기사](https://siliconangle.com/2026/10/12/meta-releases-muse-wonder-ai-models-built-to-run-personal-and-professional-agents/))에 따르면 모델 카드(모델 성능·한계·안전성 평가를 정리한 공식 문서)는 경쟁 모델 측정이 '최선의 노력' 수준이라 프롬프트와 도구가 최적화되지 않았을 수 있다고 스스로 경고하고, Wonder Full이 크게 앞선 SWE-Marathon(오래 걸리는 소프트웨어 프로젝트를 끝까지 해내는 시험, 57.5 대 46.3)도 "통제된 비교가 아니다"라고 적었습니다. 경쟁사 점수는 Codex·Claude Code 같은 각자의 하네스(harness, 모델을 감싸 도구 사용·실행을 관리하는 틀)로 낸 것이거든요. 그러니 회사 발표 기준 '최고' 항목들은 참고만 하고, 같은 조건에서 직접 돌린 Artificial Analysis 점수를 기준선으로 삼는 게 안전합니다. 그 기준으로도 Opus 5.5가 종합 점수·HealthBench Pro·OSWorld(실제 컴퓨터 화면을 조작해 과제를 푸는 시험)·ProgramBench에서 앞섭니다.

두 번째는 "가장 센 모델을 실제로 쓸 수 있느냐"입니다. 화제가 된 56점과 코딩 지수 68점은 Wonder Full 것인데, 이 모델은 Muse Code 구독 안에서만 돌아가요. 회사 서비스나 자동화 시스템에 붙일 수 있는 건 52점짜리 일반 Wonder뿐입니다. VentureBeat는 여기에 데이터 문제를 더했습니다. Muse Code 구독은 기본값이 Contributor 모드(입력한 프롬프트·코드·결과를 Meta가 모델 개선에 쓸 수 있는 방식)이고, 끄더라도 그 뒤 입력부터만 적용된다는 거예요. 제로 데이터 보존(요청·응답 내용을 저장하지 않는 옵션)은 심사를 거친 API 고객에게만 주어지고, 그 설정에서는 서버 쪽 대화 상태·파일 업로드·웹 검색이 빠진다고 합니다. 이는 Wonder가 내세우는 '오래 기억하는 에이전트'와 정면으로 부딪힐 수 있는 지점이에요.

세 번째는 값입니다. 왕은 CNBC에 API 가격이 OpenAI·Anthropic 선두 모델보다 "의미 있게 낮을 것"이라고 했지만, 실제 정가 4달러/20달러는 Claude Opus 5.5와 똑같습니다. 10달러/50달러인 GPT-6 Astra나 Claude Fable 5.1보다는 싸니 틀린 말은 아니지만, 비교 대상을 어디에 두느냐에 따라 다르게 들리는 말이죠. 더 중요한 건 토큰 단가가 아니라 작업당 비용입니다. Artificial Analysis 계산으로 Wonder는 과제 하나에 평균 4.52달러가 들어 Opus 5.5(5.98달러)보다는 싸지만 GPT-6 Astra(3.26달러), Gemini 4 Argon(1.99달러), GPT-6.1 Sol(0.72달러)보다 비싸고, 전작 Spark 1.3(1.60달러)의 2.8배입니다. 입력 토큰을 과제당 769만 개나 쓰는 탓이라, 긴 에이전트 작업에서는 캐시(이미 읽은 입력을 재사용해 싸게 처리하는 기능) 적중률이 실제 청구서를 좌우합니다.

마지막으로 안전성 보고서가 아직 다 나오지 않았습니다. Meta는 "가장 정렬이 잘 된(사람 의도대로 움직이도록 맞춘) 모델"이라고 했지만 전체 안전 보고서는 '곧' 낸다고만 했고, SiliconANGLE이 전한 모델 카드 내용에 따르면 안전장치를 끈 상태의 Wonder Full이 CBRN(Chemical, Biological, Radiological, Nuclear — 화학·생물·방사능·핵 무기 위험) 중 화학·생물 분야 고위험 기준에 닿을 가능성을 배제하지 않았습니다. 안전장치를 켠 상태에서는 '보통 이하'로 평가했다고 합니다.

## 그래서 어떻게 보면 되나

지금 판단은 이렇습니다. Meta가 '프론티어 경쟁에 다시 들어왔다'는 주장은 독립 평가로 뒷받침되는 진짜 뉴스예요. 6주 만에 종합 점수를 8점 올렸고, 장시간 코딩과 법률·업무 자동화 같은 에이전트 작업에서는 회사 발표와 독립 평가가 같은 방향을 가리킵니다. 하지만 "OpenAI·Anthropic을 이겼다"로 읽으면 과장입니다. 종합 1위는 여전히 Claude Opus 5.5이고, 화제의 고득점은 API로 못 쓰는 Wonder Full 것이며, 실제로 붙일 수 있는 Wonder는 Opus와 같은 값에 지식 점수는 낮고 작업당 비용은 중간 이상입니다.

기억할 건 세 가지예요. 비교할 때는 Wonder(API)와 Wonder Full(Muse Code 전용)을 반드시 나눠 볼 것, 벤치마크 표에서는 Meta 자체 측정과 제3자 측정을 구분할 것, 그리고 Muse Code에 민감한 코드를 넣기 전에 Contributor 모드부터 끌 것. 판단이 바뀔 조건은 Wonder Full이 API로 풀리고 가격이 붙는 순간, 전체 안전 보고서가 나와 모델 카드의 단서들이 풀리는 순간, 그리고 다음 분기 실적에서 Muse 구독자 수나 API 매출 같은 실제 채택 숫자가 나오는 순간입니다. 그 전까지는 "성능은 증명, 사업성과 실사용 신뢰도는 미증명"이라는 정도로 보는 게 맞습니다.

</div>

---

<details class="research-refs" markdown="1">
<summary>참고 자료 — 핵심 수치 · 체크포인트 · 출처 목록</summary>

### 핵심 수치

| 수치·사실 | 출처 | 검증 여부 |
|---|---|---|
| Intelligence Index v4.3: Wonder Full 56, Wonder 52, Spark 1.3 48, Opus 5.5 58, GPT-6 Astra 53 | [Artificial Analysis](https://artificialanalysis.ai/articles/muse-wonder) | 독립 확인(제3자 직접 측정) |
| Terminal-Bench 4.0: Wonder Full 33%→57% (Spark 1.3 대비) | [Artificial Analysis](https://artificialanalysis.ai/articles/muse-wonder) | 독립 확인 |
| 코딩 에이전트 지수: Wonder Full(Muse Code) 68, Wonder 63, Claude Code+Sonnet 5.5 68 | [Artificial Analysis](https://artificialanalysis.ai/articles/muse-wonder) | 독립 확인 |
| 환각률: Wonder Full 23%(Spark 1.3 33%), AA-Omniscience 30 vs Opus 5.5 46 | [Artificial Analysis](https://artificialanalysis.ai/articles/muse-wonder) | 독립 확인 |
| 작업당 비용: Wonder 4.52달러, Opus 5.5 5.98달러, GPT-6 Astra 3.26달러, GPT-6.1 Sol 0.72달러, Spark 1.3 1.60달러 | [Artificial Analysis](https://artificialanalysis.ai/articles/muse-wonder) | 독립 추정(자체 과제 기준) |
| API 정가: 입력 4달러·출력 20달러·캐시 입력 0.20달러(100만 토큰당), 웹 검색 1,000회당 2.50달러 | [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api) | 회사 발표(공식 가격표) |
| Wonder Full: Muse Code 월 50달러(Power)·200달러(Maximum) 구독 전용, API 미제공 | [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api), [CNBC](https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html) | 회사 발표 |
| Muse 앱에서 Wonder 사용: 월 20달러·100달러 구독 필요 | [CNBC](https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html) | 언론 보도 |
| SWE-Marathon: Wonder Full 57.5 vs Opus 5.5 46.3 (통제된 비교 아님) | [SiliconANGLE](https://siliconangle.com/2026/10/12/meta-releases-muse-wonder-ai-models-built-to-run-personal-and-professional-agents/) | 회사 발표(모델 카드 단서 포함) |
| ProgramBench: Opus 5.5 70.5% vs Wonder Full 59% | [SiliconANGLE](https://siliconangle.com/2026/10/12/meta-releases-muse-wonder-ai-models-built-to-run-personal-and-professional-agents/) | 회사 발표(모델 카드) |
| 컨텍스트 창 약 100만 토큰, API 분당 3,000요청·400만 토큰 한도 | [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api) | 회사 발표 |
| 발표일 Meta 주가 3.4% 상승(Reuters는 장중 약 4%) | [WSJ](https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-10-12-2026/card/meta-says-new-ai-model-will-make-muse-agent-smarter-stock-rises-I5TGdjAIpWKaMzOxkv1W), [Reuters/StreetInsider](https://www.streetinsider.com/Reuters/Meta+releases+Muse+Wonder+AI+models+to+challenge%C2%A0Anthropic+and+OpenAI/27175156.html) | 언론 보도 |
| Active Memory·Active Focus 내부 구조 | — | 확인되지 않음(공개 자료에 설명 없음) |

### 앞으로 볼 체크포인트

- Wonder Full의 API 개방 여부와 토큰 가격 — 열리면 '쓸 수 있는 최고 모델' 비교가 다시 짜임
- Meta 전체 안전 보고서 공개 — 모델 카드의 화학·생물 위험 단서와 사이버 평가(ExploitGym) 해석이 구체화되는지
- Muse 앱에 Wonder가 실제로 들어간 뒤 사용자 반응, 그리고 Muse 개인 메시지 접근 논란(CNBC 보도)이 다시 불거지는지
- 다음 분기 실적에서 Muse 구독자 수·Model API 매출 등 채택 지표가 공개되는지
- Artificial Analysis 외 다른 독립 평가(LMArena 등)에서의 순위와, 실제 장시간 에이전트 작업의 캐시 적중률·작업당 비용 사례

### 출처 목록

1. [Muse Wonder: A Frontier Model For Personal & Professional AI Agents — Meta AI 연구 블로그, 2026-10-12](https://research.meta.ai/blog/muse-wonder)
2. [Introducing Muse Wonder models — Meta Newsroom(원문), 2026-10-12](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/) (이번 확인 때 접속 차단(403)으로 연구 블로그·보도로 대조)
3. [Muse Wonder and Muse Wonder Full: a material jump in intelligence over previous Meta models — Artificial Analysis, 2026-10-12](https://artificialanalysis.ai/articles/muse-wonder)
4. [Meta's new Muse Wonder and Muse Wonder Full models achieve frontier performance, but only the weaker one is available via API — VentureBeat, 2026-10-12](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api)
5. [Meta releases its first frontier model, Muse Wonder — TechCrunch, 2026-10-12](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder/)
6. [Meta releases Muse Wonder AI models built to run personal and professional agents — SiliconANGLE, 2026-10-12](https://siliconangle.com/2026/10/12/meta-releases-muse-wonder-ai-models-built-to-run-personal-and-professional-agents/)
7. [Meta debuts Muse Wonder AI model in latest test of users' willingness to pay — CNBC, 2026-10-12](https://www.cnbc.com/2026/10/12/meta-muse-wonder-ai-model-agent.html)
8. [Meta releases Muse Wonder AI models to challenge Anthropic and OpenAI — Reuters(StreetInsider 전재), 2026-10-12](https://www.streetinsider.com/Reuters/Meta+releases+Muse+Wonder+AI+models+to+challenge%C2%A0Anthropic+and+OpenAI/27175156.html)
9. [Meta Says New AI Model Will Make Muse Agent Smarter; Stock Rises — WSJ, 2026-10-12](https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-10-12-2026/card/meta-says-new-ai-model-will-make-muse-agent-smarter-stock-rises-I5TGdjAIpWKaMzOxkv1W)
10. [Theo(@theo)의 모델 순위 게시물 — X, 2026-10-13 KST](https://x.com/theo/status/2109724741234028639) (개인 의견)

</details>
