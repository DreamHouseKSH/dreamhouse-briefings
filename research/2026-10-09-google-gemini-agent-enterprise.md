# 심층 리서치 — 구글 기업용 Gemini agent, 실제로 뭐가 새롭고 뭐가 아직 미확인인가

- **요청:** [#1](https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/1)
- **원래 기사:** [2026-10-09 AI · 1. 구글 클라우드, 기업용 Gemini agent 공개](../news/2026-10-09/AI.md)
- **원문:** https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/
- **작성:** 2026-10-09 17:55 KST (2026-10-09 18:15 KST 에세이형으로 다시 씀)

구글이 Gemini를 대답하는 챗봇에서 자기 계정과 권한, 감사 기록을 가진 '업무용 AI 동료'로 바꾸겠다고 발표했어요. 설계는 분석가들에게 좋은 평가를 받았지만, 지금은 일부 기업만 쓰는 비공개 프리뷰라 '출시'보다는 '정식 출시 예고'에 가깝고, 가격과 신뢰성은 아직 확인되지 않았습니다.
{: .research-lead}

![구글 Gemini agent 행사 이미지 (TechCrunch/Google)](https://techcrunch.com/wp-content/uploads/2026/10/image_3.max-2100x2100_0CYZWqn.jpg?resize=1200,591)

이미지 출처: TechCrunch 원문 페이지 (원본 이미지 링크, 복제 저장 아님)
{: .research-credit}

<div class="research-essay" markdown="1">

## 챗봇에서 '목표를 맡기는 동료'로

구글은 10월 8일(현지 시각) Gemini at Work 2026 행사에서 'Gemini agent'를 공개했습니다. 에이전트(agent)는 사람이 한 단계씩 지시하는 대신 목표만 주면 스스로 계획을 세우고 메일·문서·데이터베이스 같은 도구를 써서 일을 끝내는 AI를 말해요. 토마스 쿠리안 구글 클라우드 CEO는 키노트 글([Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026))에서 이걸 "지시가 아니라 목표를 준다"는 말로 요약했습니다. 일을 맡기고 나중에 와서 완성된 결과를 받는다는 거죠.

가장 눈에 띄는 건 '코워커 에이전트'입니다. 필요한 역할을 설명하면 Gemini가 에이전트를 만들고, 그 에이전트는 자기 Workspace 계정과 `@agents.company.com` 메일 주소, 캘린더와 Drive를 받아 회사 조직도에 이름을 올립니다. 동료들은 사람한테 하듯 채팅방에 초대해서 일을 시키고, 에이전트가 한 행동은 사람이 아니라 에이전트 이름으로 감사 기록(audit trail, 누가 언제 무엇을 했는지 남기는 기록)에 쌓입니다. 연결 대상도 넓어요. Gmail·Docs 같은 구글 앱은 물론 Microsoft 365, Slack, Jira, Salesforce, Snowflake까지 붙고, MCP(Model Context Protocol, AI가 외부 도구·데이터에 붙는 표준 규격) 서버도 연결할 수 있다고 구글은 설명합니다. 모델도 고를 수 있어서, 지금은 Gemini 계열과 Anthropic의 Claude를 쓸 수 있고 다른 모델은 나중에 추가한다고 해요. 여기까지는 모두 회사 발표 내용입니다.

## 누가 쓸 수 있고, 얼마인가

결론부터 말하면 회사가 돈을 내고 쓰는 계정이 있어야 합니다. Gemini agent는 기업용 Gemini Enterprise 앱 안에 들어가는 기능이고, The Verge([기사](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise))는 "현재 기업 고객에게만 비공개 프리뷰(private preview, 구글이 고른 일부 고객만 먼저 써 보는 시험판)로 제공된다"고 밝혔어요. 그러니 유료 Workspace나 Google Cloud 기업 계정이 있어도 지금 당장 신청해서 쓸 수 있는 단계는 아닙니다. 개인 Gmail 계정으로 쓸 수 있다는 언급은 어떤 자료에도 없었고, 개인용으로는 5월에 나온 구독자용 'Gemini Spark' 에이전트가 Gemini 앱 안에 따로 있다고 The Verge는 설명합니다.

가격은 방식만 나왔습니다. Constellation Research([분석](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems))가 행사 뒤 분석가 세션 내용을 정리한 걸 보면, 따로 값을 매긴 추가 상품인 SKU(Stock Keeping Unit, 따로 값을 매겨 파는 판매 단위)나 애드온 없이 쓴 만큼 내는 종량제이고, Workspace 쪽 정확한 과금 방식은 나중에 공개합니다. 같은 자리에서 GA(General Availability, 누구나 쓸 수 있는 정식 출시)는 10월 말에서 11월 초쯤으로 예상됐어요. 정확한 단가나 어떤 Workspace 요금제에서 쓸 수 있는지는 아직 확인되지 않았습니다.

## 분석가들은 박수를 치면서도 숙제를 남겼다

반응은 대체로 호의적이었어요. Constellation의 홀거 뮐러는 기업이 이미 믿고 사 둔 LLM(Large Language Model, 대규모 언어 모델)을 그대로 쓰게 해 주는 개방형 접근이 매력이라고 봤고, HFS Research([평가](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/))는 이번 가을에 나온 범용 에이전트 가운데 가장 완성도가 높아 보인다며, 어느 모델 편도 들지 않는 '중립 통제판'이라는 자리를 차별점으로 꼽았습니다. Computerworld([기사](https://www.computerworld.com/article/4232827/google-wants-to-be-the-gatekeeper-for-enterprise-ai-agents.html))에 인용된 독립 분석가 카미 레비는 구글이 모델 성능보다 '기업 AI의 문지기'가 되려 한다고 해석했어요.

그런데 같은 사람들이 숙제도 분명히 짚었습니다. HFS는 실패율이나 결정성(같은 입력에 같은 결과가 나오는지) 같은 신뢰성 자료가 발표에 없다고 지적했고, 레비도 핵심 업무를 사고 없이 맡길 수 있을지는 별개 문제라고 했어요. TechTarget([기사](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound))에 나온 Omdia·Futurum 분석가들은 에이전트가 SAP나 마이크로소프트 환경에 들어갈 때 회사별 권한 정책을 어떻게 통과할지, 직원이 Claude 같은 비싼 모델을 고르면 토큰 비용을 누가 관리할지, 에이전트가 쌓은 맥락을 다른 플랫폼으로 옮길 수 있는지 같은 락인 문제를 물었습니다. Forbes는 모델·앱·에이전트가 모두 'Gemini'라는 같은 이름이라 헷갈린다고 꼬집었고요.

## '출시'와 '최초'라는 말, 그리고 숫자 읽는 법

원 기사인 TechCrunch는 이 소식을 출시(launch)로 다루면서 비공개 프리뷰라는 점은 거의 말하지 않았습니다. 하지만 실제로는 일부 고객만 쓰는 시험판이니 정식 출시 예고로 읽는 게 정확해요. '최초'라는 표현도 조심해야 합니다. 마이크로소프트가 약 2주 앞선 9월 25일에 자기 신원과 메일, 메모리를 가진 장기 실행 에이전트인 Copilot Autopilot을 먼저 내놨고, Info-Tech의 분석가는 새로운 범주가 아니라고 봤거든요.

숫자는 대부분 구글이 직접 낸 것입니다. 순다르 피차이가 말한 'Gemini 월간 이용자 10억 명 이상', 'Fortune 100의 약 90%가 Gemini Enterprise 사용'은 회사 발표 기준이고 독립 검증이 없어요. 특히 '사용'이 전사 도입인지 한 팀의 시험 사용인지 정의가 공개되지 않았습니다. 브라질 은행 Bradesco가 문서 검토를 1시간에서 5분으로 줄였다는 고객 사례도 구글이 고른 성공 사례라 대표성은 알 수 없어요. 토큰 단가가 2024년 이후 98% 내렸다는 말 역시 근거 수치는 공개되지 않았습니다.

## 그래서 어떻게 보면 되나

이번 발표는 '구글이 기업 업무용 AI의 운영판을 차지하겠다는 선언'으로 보면 됩니다. 에이전트마다 신원과 감사 기록을 붙이고 프로젝트별 지출 상한을 거는 설계, 경쟁사 모델까지 고를 수 있게 한 개방성은 분석가들도 인정하는 강점이에요. 다만 지금은 비공개 프리뷰라 개인은 물론이고 유료 Workspace 회사도 당장 쓰기 어렵고, 단가와 실패율이라는 가장 중요한 두 숫자가 비어 있습니다. 예상 쟁점: 에이전트가 자기 이름으로 메일을 보내고 문서를 고치는 구조라면, 잘못했을 때 책임이 에이전트를 만든 직원·관리자·구글 중 누구에게 있는지는 실제 사고 사례가 나와야 정리될 거예요. 10월 말에서 11월 초 GA 때 가격표와 지원 요금제, 그리고 초기 고객의 독립적인 후기가 나오면 그때 판단을 다시 하는 게 좋겠습니다.

</div>

---

<details class="research-refs" markdown="1">
<summary>참고 자료 — 핵심 수치 · 체크포인트 · 출처 목록</summary>

### 핵심 수치

| 수치·사실 | 출처 | 검증 여부 |
|---|---|---|
| 상태: 기업 고객 대상 비공개 프리뷰 | [The Verge](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise), [Constellation](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems) | 여러 매체 일치 |
| GA 예상: 10월 말~11월 초 | Constellation(분석가 세션) | 2차, 예상치 |
| 가격: 별도 SKU·애드온 없는 종량제, Workspace 과금 방식은 추후 공개 | Constellation, Forbes("가격 미공개") | 단가는 확인되지 않음 |
| 이용 조건: Gemini Enterprise 앱 안 기능(기업용 유료 계정) | The Verge, [Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026) | 개인 Gmail 지원 언급 없음 |
| 개인용 별도 에이전트: Gemini Spark(5월 출시, 구독자용) | The Verge | 2차 |
| 모델 선택: Gemini 계열 + Claude, 다른 모델 추후 | Google Cloud 블로그, [TechCrunch](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/) | 회사 발표 + 2차 일치 |
| Gemini 월간 이용자 10억 명 이상 | TechCrunch(피차이 발언) | 회사 발표, 독립 검증 없음 |
| Fortune 100의 약 90%가 Gemini Enterprise 사용 | Google Cloud 블로그 | 회사 발표, '사용' 정의 미공개 |
| 클라우드 고객 약 80%가 AI 제품 사용, 약 500곳이 1년간 각 1조 토큰 이상 처리 | Google Cloud 블로그, Constellation | 회사 발표 |
| 토큰 단가 2024년 이후 98% 하락 | Google Cloud 블로그 | 회사 주장, 근거 미공개 |
| Bradesco 문서 검토 1시간→5분, SOMPO 사내 에이전트 1만 개 이상 | Google Cloud 블로그 | 회사가 고른 사례 |
| PayPal 주당 1천만 건 멀티모델 요청 라우팅 | Google Cloud 블로그 | 회사 발표 |
| MS Copilot Autopilot 발표: 9월 25일 | [Forbes](https://www.forbes.com/sites/janakirammsv/2026/10/08/google-built-an-ai-coworker-and-gave-it-a-confusing-name/), TechTarget | 2차 |

### 앞으로 볼 체크포인트

- **10월 말~11월 초 GA:** 실제 출시 여부, 어떤 Workspace·Google Cloud 요금제에서 쓸 수 있는지, 한국 제공 여부.
- **가격표 공개:** 종량제 단가, Workspace 과금 방식, Claude를 고를 때 추가 비용.
- **신뢰성 자료:** 구글이 평가·실패율·사고 대응 자료를 내는지, 초기 고객의 독립 후기가 나오는지.
- **모델 선택지 확대:** '다른 비공개·오픈 모델'이 언제, 무엇으로 추가되는지.
- **업종별 버전:** 금융·법률은 프리뷰, 정부·헬스케어·리테일은 '곧 출시'(일정 미공개).
- **MS Autopilot·Agent 365와 비교:** 두 제품이 GA로 갈 때 가격과 통제 기능 차이.

### 출처 목록

1. [Welcome to Gemini at Work 2026: Introducing the Gemini agent — Google Cloud Blog(토마스 쿠리안 키노트), 2026-10-09](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026)
2. [Google Cloud introduces the Gemini agent — Google 블로그, 2026-10-08](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/)
3. [Google brings agentic AI to Gemini, starting with businesses — TechCrunch(Sarah Perez), 2026-10-08](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/)
4. [Google is launching a one-stop Gemini agent for your work tasks — The Verge(Emma Roth), 2026-10-08](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise)
5. [Google Cloud launches Gemini agent to work across enterprise systems — Constellation Research, 2026-10-08](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems)
6. [Google's workplace agent is out, but questions abound — TechTarget(Esther Shittu), 2026-10-08](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound)
7. [Google wants to be the gatekeeper for enterprise AI agents — Computerworld(Taryn Plumb), 2026-10](https://www.computerworld.com/article/4232827/google-wants-to-be-the-gatekeeper-for-enterprise-ai-agents.html)
8. [Pick Gemini agent when neutral model choice matters most — HFS Research, 2026-10-08](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/)
9. [Google Built An AI Coworker And Gave It A Confusing Name — Forbes(Janakiram MSV), 2026-10-08](https://www.forbes.com/sites/janakirammsv/2026/10/08/google-built-an-ai-coworker-and-gave-it-a-confusing-name/) (검색 결과 발췌로 확인, 본문 전체는 열람하지 못함)

</details>
