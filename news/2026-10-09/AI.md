# AI 브리핑 — 2026-10-09 (금, KST 아침)

> 10월 9일 아침 브리핑으로 전달된 AI 기업·제품·정책 소식 요약 아카이브입니다. 기사 전문이 아니라 요약이며, 자세한 내용은 각 원문 링크를 확인하세요.

---

## 1. 구글 클라우드, 기업용 Gemini agent 공개 — 목표만 주면 계획·도구·시스템 연동까지

- **원문:** https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/
- **분야:** AI · 제품/엔터프라이즈
- **날짜:** 2026-10-08

### 미디어

![구글 Gemini agent 행사 이미지 (TechCrunch/Google)](https://techcrunch.com/wp-content/uploads/2026/10/image_3.max-2100x2100_0CYZWqn.jpg?resize=1200,591)

> 출처: 원문 페이지 (TechCrunch) — 원본 이미지 링크(복제 저장 아님)

### 요약

구글이 8일 Gemini at Work 2026에서 **Gemini agent(질문에 답하는 것을 넘어 업무를 대신 수행하는 통합 에이전트)** 를 기업 대상으로 먼저 공개했습니다. 순다르 피차이 CEO는 Gemini 월간 활성 이용자가 10억 명 이상, Fortune 100의 약 90%가 Gemini Enterprise를 쓴다고 밝혔고, 보안·규모·성능 문제를 먼저 풀기 위해 **B2B(기업) 우선 후 소비자 확대** 순서를 택했다고 설명했습니다.

에이전트는 “지시”가 아니라 **목표(objective)** 를 받아 계획을 세우고, 스킬·도구를 쓰며 Workspace·Microsoft 365·Slack·Jira·Confluence·Git·BigQuery·Databricks·Postgres·Snowflake 등 내부 시스템에 연결합니다. 기본은 작업에 맞는 모델을 자동 선택하고, 사용자가 Anthropic **Claude** 등 제3자 모델을 고를 수도 있으며 향후 오픈소스·프라이빗 모델로 확대 예정입니다. **MCP(Model Context Protocol, 도구·데이터 연결 표준)** 서버와도 연동됩니다.

에이전트는 자체 Workspace 계정·이메일·감사 추적을 갖고, 모바일·데스크톱·CLI·ServiceNow 등에서 호출할 수 있습니다. On·Shopify·PayPal 등이 초기 테스터였고, 멀티모델 오케스트레이션·스마트 라우팅·실시간 **지출 상한(spend cap)** 으로 비용 통제를 강조했습니다. 구글 블로그 요약: https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/

**시사점:** 대화형 챗봇에서 “동료처럼 일하는 에이전트”로 엔터프라이즈 AI 경쟁 축이 옮겨가고 있습니다. Claude를 모델 피커에 넣은 점도 멀티벤더 전략도 눈에 띕니다.

---

## 2. Anthropic, OSS Scanner 공개 — 오픈소스 취약점 스캔을 옵트인·무료로

- **원문:** https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source
- **분야:** AI · 보안/오픈소스
- **날짜:** 2026-10-08

### 미디어

![Anthropic OSS Scanner 관련 이미지](https://www-cdn.anthropic.com/images/4zrzovbb/website/6d4a0d28992ade92d6fa63646fd9c9d318245c6c-2400x1260.jpg)

> 출처: 원문 페이지 (Anthropic) — 원본 이미지 링크(복제 저장 아님)

### 요약

Anthropic이 **Project Glasswing(클로드로 취약점을 찾는 내부·파트너 보안 프로그램)** 경험을 바탕으로, 오픈소스 프로젝트가 신청하면 최강 모델로 주기적 보안 스캔을 **무료**로 받는 **OSS Scanner**를 8일 공개했습니다. Google **OSS-Fuzz(퍼저로 OSS를 자동 검사하는 프로젝트)** 에 영감을 받았다고 밝혔습니다. 기업용 Claude Security와 달리 OSS 유지보수 팀을 대상으로 합니다.

회사 발표 기준 CyberGym 벤치마크에서 LLM의 취약점 발견율이 작년 초 20% 미만에서 올해 85% 이상으로 올랐고, 최근 6개월간 후보 취약점 2만 9,000건 이상을 찾았으나 사람이 검토한 것은 약 6,000건에 그쳤습니다. OSS Scanner 출력은 **사람 검수 없이 모델 생성**이라 오탐·부정확 보고가 있을 수 있다고 명시했고, Claude Mythos 등 최강 모델을 사용합니다. 조기 검증에서 고·치명 97건 중 85건(88%)이 기존 CVD(조정 취약점 공개) 기준을 통과했다고 밝혔습니다. PostgreSQL·OpenSSL·wolfSSL·HotCRP 유지보수자들의 긍정적 피드백도 인용됐습니다.

신청은 GitHub 템플릿 PR로 하며, OSS-Fuzz와 유사한 “인프라·사용자 보안에 중대한 영향” 기준을 적용합니다. 이와 별도로 Cyber Verification Program·Claude for OSS(Max 20x 무료 구독)도 언급됐습니다.

**시사점:** AI가 방어 측 취약점 발굴 속도를 공격자 쪽과 맞추려는 움직임입니다. 옵트인·무검수 리포트라는 전제를 유지보수자가 이해하고 쓰는 게 중요합니다.

---

## 3. Anthropic, DOE Genesis Mission에 3년간 1억 5천만 달러 지원

- **원문:** https://www.anthropic.com/news/genesis-mission-commitment
- **분야:** AI · 정책/과학
- **날짜:** 2026-10-08

### 미디어

![Anthropic Genesis Mission 관련 OG 일러스트](https://www.anthropic.com/api/opengraph-illustration?name=Object%20DoubleHelix&backgroundColor=heather)

> 출처: 원문 페이지 (Anthropic) — 원본 이미지 링크(복제 저장 아님)

### 요약

Anthropic이 미국 **에너지부(DOE)** 주도 **Genesis Mission(국가 연구소·산업·학계가 AI로 과학·에너지·안보 돌파를 가속하려는 연방 이니셔티브)** 에 앞으로 3년간 **1억 5천만 달러**를 투입한다고 8일 발표했습니다. 자금은 NASA·NIH·NSF 등 미션 참여 **15개 이상 기관**에 Claude를 제공하는 데 쓰입니다. 백악관 OSTP의 “Science: A New Golden Age” 서밋에서 발표했습니다.

구체적으로는 (1) 수백 개 Genesis 연구 프로젝트에 Claude·Claude Code·API 크레딧 제공, (2) 핵융합·양자컴퓨팅 등 우선 과학 과제에서 기관·국립연구소와 협력, (3) 과학자 온보딩·교육·기술 지원입니다. 지난해 12월 DOE 파트너십 이후 국립연구소에 Claude를 들여온 연장선이며, 올해 출시한 Claude Science·학술 과학자용 1만 좌석·AI for Science 크레딧·**Model Hardware Standard(실험실 장비를 AI 에이전트가 안전하게 다루기 위한 공통 규격)** 프리뷰와도 맞닿아 있습니다.

**시사점:** 민간 프론티어 랩이 연방 과학 미션에 대규모 크레딧·도구를 넣는 사례입니다. 실제 과제 선정과 성과 공개가 다음 관전 포인트입니다.

---

## 4. OpenAI, GPT-6.1 Sol Ultrafast 모드 롤아웃 — API·Codex·ChatGPT Work

- **원문:** https://community.openai.com/t/ultrafast-is-rolling-out-today-for-gpt-6-1-sol-in-the-api-codex-and-chatgpt-work/1404475
- **분야:** AI · 제품/API
- **날짜:** 2026-10-08

### 미디어

![OpenAI Ultrafast 발표 관련 이미지](https://us1.discourse-cdn.com/openai1/optimized/4X/1/0/f/10fae24328d2dac79ba851ee3adbb3aaa443b4b4_2_1024x576.jpeg)

> 출처: 원문 페이지 (OpenAI Developer Community) — 원본 이미지 링크(복제 저장 아님)

### 요약

OpenAI가 8일(UTC) **GPT-6.1 Sol**에 **Ultrafast(초저지연 서빙 티어)** 모드를 API·Codex·ChatGPT Work에 롤아웃한다고 개발자 커뮤니티에 공지했습니다. 회사 표현으로는 Sol Standard 대비 최대 약 8배 빠르고, 지능은 Astra에 가깝다고 합니다. API 가격은 입력 100만 토큰당 12달러·출력 60달러로, Astra의 약 1.2배 수준이라고 밝혔습니다.

용도로는 장애 디버깅, 앱을 탐색하는 에이전트, 초 단위가 중요한 라이브 경험 등을 꼽았습니다. Codex·ChatGPT Work에서는 Pro 500·자격 있는 사용량 기반 Enterprise·크레딧 기반 Edu에서 쓰며, Enterprise는 관리자 활성화가 필요합니다. Ultrafast는 지원 전 지역에서 이용 가능하고 미국·EU **데이터 레지던시(데이터가 특정 지역에만 머무르게 하는 설정)** 를 지원하며, GPT-6.1 Sol Fast·GPT-6 Luna Fast에도 EU 레지던시를 추가했다고 합니다.

**시사점:** “더 똑똑한 모델”보다 “같은 계열을 훨씬 빠르게” 파는 속도 티어 경쟁이 본격화됐습니다. 비용(Astra의 1.2배) 대비 지연 이득이 워크로드에 맞는지가 선택 기준입니다.
