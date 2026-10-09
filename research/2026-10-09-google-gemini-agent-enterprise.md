# 심층 리서치 — 구글 기업용 Gemini agent, 실제로 뭐가 새롭고 뭐가 아직 미확인인가

- **요청:** [#1](https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/1)
- **원래 기사:** [2026-10-09 AI · 1. 구글 클라우드, 기업용 Gemini agent 공개](../news/2026-10-09/AI.md)
- **원문:** https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/
- **작성:** 2026-10-09 17:55 KST

![구글 Gemini agent 행사 이미지 (TechCrunch/Google)](https://techcrunch.com/wp-content/uploads/2026/10/image_3.max-2100x2100_0CYZWqn.jpg?resize=1200,591)

> 출처: TechCrunch 원문 페이지 — 원본 이미지 링크(복제 저장 아님)

## 한 줄 결론

구글은 Gemini를 "대답하는 챗봇"에서 **자기 계정·권한·감사 기록을 가진 업무용 에이전트**로 바꾸겠다고 발표했고, 설계(모델 선택 개방·에이전트 신원·지출 상한)는 분석가들에게 대체로 좋은 평가를 받았습니다. 다만 지금은 **비공개 프리뷰(private preview, 일부 고객만 쓰는 시험판)** 단계라 가격·실제 신뢰성(얼마나 실수 없이 일하는지)·다른 회사 시스템과의 권한 연동은 **아직 확인되지 않았습니다.** "출시"라기보다 "정식 출시 예고 + 시험판 공개"로 보는 게 정확합니다.

## 배경

- **에이전트(agent):** 사람이 한 단계씩 시키는 대신 목표만 주면 스스로 계획을 세우고 도구(메일, 문서, DB 등)를 써서 일을 끝내는 AI. 2026년 들어 업계 경쟁 축이 챗봇에서 에이전트로 옮겨가고 있습니다.
- 구글은 2026-10-08(현지) **Gemini at Work 2026** 행사에서 이를 발표했습니다. 토마스 쿠리안 구글 클라우드 CEO의 키노트 요약이 1차 자료입니다([Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026)).
- 소비자 쪽에는 이미 5월에 별도 앱 화면의 **Gemini Spark** 에이전트가 있었고, 이번 것은 기업용 **Gemini Enterprise** 앱 안에 들어가는 통합 에이전트입니다([The Verge](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise)).
- 경쟁 맥락: 마이크로소프트는 약 2주 앞선 9월 25일 Copilot을 **Autopilot**(자체 Entra ID 신원·메일·메모리를 가진 장기 실행 에이전트) 중심으로 재편했고, Meta는 9월 소비자용 **Muse** 에이전트를 냈습니다([Forbes](https://www.forbes.com/sites/janakirammsv/2026/10/08/google-built-an-ai-coworker-and-gave-it-a-confusing-name/), [TechTarget](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound)).

## 핵심 사실과 수치 (출처별)

| 사실·수치 | 출처 | 비고(1차/2차, 이해관계) |
|---|---|---|
| "지시가 아니라 목표(objectives)를 준다" — 계획·스킬·도구 사용·사내 시스템 연결 후 완성된 결과물 반환 | [Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026) | 1차, 회사 발표 |
| 모델 선택: 현재 Gemini 계열 + Anthropic Claude, 향후 다른 비공개·오픈 모델 추가 예정 | 같은 곳, [TechCrunch](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/) | 1차 + 2차 일치 |
| 연결 대상: Workspace, Microsoft 365·Teams, Slack, Confluence, Git, Jira, Salesforce, ServiceNow, BigQuery, Databricks, Postgres, Snowflake, 데스크톱 파일, 사내외 **MCP(Model Context Protocol, AI가 외부 도구·데이터에 붙는 표준 규격)** 서버 | Google Cloud 블로그 | 1차, 회사 발표 |
| 코워커 에이전트: 자체 Workspace 계정, `@agents.company.com` 메일, 캘린더·Drive, 조직도 등록. 공유받은 것만 볼 수 있고, 행동은 사람 대신 에이전트 이름으로 감사 기록(audit trail)에 남음 | Google Cloud 블로그, The Verge | 1차 + 2차 일치 |
| 보안: 에이전트마다 암호학적으로 증명된 신원, 최소 권한, **Agent Sandbox(격리된 실행 공간)**, 모든 트래픽이 지나는 **Agent Gateway(AI용 네트워크 방화벽)** 에 정책을 한 번 쓰면 전 에이전트에 적용 | Google Cloud 블로그 | 1차, 회사 발표. 실효성 독립 검증 없음 |
| 비용: 다중 모델 조합, 스마트 라우팅(작업별로 싼 모델 자동 배정), 프로젝트별 **실시간 지출 상한** — 상한 도달 시 에이전트 일시정지 | Google Cloud 블로그, Forbes | 1차 + 2차 |
| 토큰 단가는 2024년 이후 98% 하락했지만 사용량이 폭증 | Google Cloud 블로그 | 회사 주장, 근거 수치 미공개 |
| 피차이: Gemini 월간 활성 이용자 10억 명 이상 | [TechCrunch](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/) | 행사 발언(회사 발표 기준). 독립 검증 없음 |
| Fortune 100의 약 90%가 Gemini Enterprise 사용, 클라우드 고객 약 80%가 AI 제품 사용, 약 500개 고객이 지난 1년 각 1조 토큰 이상 처리 | Google Cloud 블로그, [Constellation Research](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems) | 회사 발표 기준. "사용"의 정의(전사 도입인지 일부 팀인지) 미공개 |
| 상태: 비공개 베타/프리뷰. 정식 출시(GA) 10월 말~11월 초 예상 | Constellation(분석가 세션), The Verge, Forbes | 2차, 여러 매체 일치 |
| 가격: 별도 SKU·애드온 없이 사용량 기반. Workspace용 정확한 과금 방식은 추후 공개 | Constellation, Forbes("가격 미공개") | 2차. **확정 가격은 확인되지 않음** |
| 업종 특화: 금융·법률 프리뷰, 정부·헬스케어·리테일 예정. 금융판은 FactSet·LSEG·S&P Global·SEC 공시 데이터 연동, CME그룹·도이체방크 사용 | Google Cloud 블로그 | 1차, 회사 발표 |
| 초기 테스터: On, Shopify, PayPal(PayPal은 주당 1천만 건 멀티모델 요청을 라우팅한다고 소개) | Google Cloud 블로그, TechCrunch | 회사 발표 기준 |
| 고객 성과 예: Bradesco 문서 검토 1시간→5분, SOMPO 사내 에이전트 1만 개 이상 등 | Google Cloud 블로그 | 회사가 고른 사례(선별 편향 가능), 독립 검증 없음 |

## 이해관계자별 입장과 논조

- **구글(발표 주체):** "업무는 이제 프롬프트 창에서 시작한다", 에이전트와 모델은 별개 선택이며 최신 최강 모델은 몇 달마다 바뀌니 선택지를 열어둬야 한다는 논리 — 논조: 긍정 ([Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026))
- **TechCrunch(원 기사):** 구글 발표와 피차이 수치를 중심으로 기능을 정리, 비공개 프리뷰라는 점은 거의 다루지 않음 — 논조: 긍정 ([TechCrunch](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- **The Verge:** 기능 소개 위주지만 "현재는 기업 고객 대상 비공개 프리뷰"라고 명시 — 논조: 중립 ([The Verge](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise))
- **Constellation Research(홀거 뮐러):** 이미 계약한 LLM을 자동화에 그대로 쓰게 하는 개방형 접근이 매력적 — 논조: 긍정 ([Constellation](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems))
- **독립 분석가 카미 레비:** 구글은 모델 우위가 아니라 "새 기업 운영체제의 문지기(gatekeeper)"가 되려 한다. 신원·감사 기록·책임 소재 논의는 구글이 앞선다고 평가하면서도, 핵심 업무를 "사고 없이" 맡길 수 있을지는 별개 문제라고 지적 — 논조: 혼재 ([Computerworld](https://www.computerworld.com/article/4232827/google-wants-to-be-the-gatekeeper-for-enterprise-ai-agents.html))
- **Info-Tech 마흐무드 라민:** 새로운 범주는 아니다(OpenAI·Anthropic·MS·Meta도 멀티에이전트 보유). 반복 업무·정보 종합에 강점, 거버넌스(통제) 강제가 필수 — 논조: 중립 (같은 기사)
- **Omdia 마크 베큐 / Futurum 데이비드 니컬슨 / Tekonyx 시드 낙:** 방향은 맞지만 회사별 접근 권한, 구글 밖(SAP·Salesforce·Oracle) 데이터, 토큰 비용 관리 부담, 락인이 문제. 첫 시도에서 바로 성공하긴 어렵다 — 논조: 혼재 ([TechTarget](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound))
- **HFS Research:** 가을에 나온 범용 에이전트 중 가장 완성도 높아 보이고 "중립적 통제판(스위스)" 포지션이 차별점. 단 비용·신뢰성·쌓인 맥락의 소유권이 미지수 — 논조: 혼재 ([HFS Research](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/))
- **Forbes(자나키람 MSV):** 기능은 "AI 동료"지만 제품 이름이 그냥 'Gemini'라 모델·앱·에이전트가 헷갈린다고 지적, 마이크로소프트가 2주 먼저 같은 아이디어를 냈다고 비교 — 논조: 혼재 ([Forbes](https://www.forbes.com/sites/janakirammsv/2026/10/08/google-built-an-ai-coworker-and-gave-it-a-confusing-name/))
- **경쟁사(마이크로소프트):** 이번 발표에 대한 공식 반응은 찾지 못함. 비교 대상은 9/25 발표된 Copilot Autopilot·Agent 365(에이전트 신원·접근·비용 관리판).

## 반론과 쟁점

- **"출시"인가 "예고"인가:** 원 기사는 출시(launch)로 썼지만, 실제로는 비공개 프리뷰이고 GA는 10월 말~11월 초 예상 ([Constellation](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems), [The Verge](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise)).
- **신뢰성 근거 부재:** 평가(evals)·테스트·결정성(같은 입력에 같은 결과)·실패율 자료가 발표에 없음. 스킬이 "재사용 가능한 모듈형 프롬프트" 수준이라 규제 업무엔 약해 보인다는 지적 ([HFS Research](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/)).
- **권한은 벤더가 아니라 회사가 정한다:** 에이전트가 SAP나 MS 환경에 접근하려 할 때 사내 권한 정책을 어떻게 통과할지 불분명. "보안이 생산성을 깎는" 구조를 에이전트가 어떻게 다룰지 의문 ([TechTarget](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound)).
- **비용 책임 전가:** 사용자가 Claude 같은 비싼 모델을 고를 수 있으면 직원 모두가 토큰 비용까지 신경 써야 함 (같은 기사). 구글은 지출 상한·라우팅으로 답하지만 단가가 공개되지 않아 검증 불가.
- **락인·맥락 소유권:** 에이전트가 쌓는 메모리·맥락을 누가 소유하고 다른 플랫폼으로 옮길 수 있는지 미정 ([HFS Research](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/), [TechTarget](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound)).
- **"최초" 주장:** TechTarget은 구글을 "업무 흐름에 연결되는 에이전트를 낸 첫 프런티어 AI 기업"이라 썼지만, 같은 기사와 Forbes가 MS Autopilot(9/25)을 먼저 언급하고 Info-Tech는 새 범주가 아니라고 봄 — "최초" 표현은 정의에 따라 달라짐 ([Computerworld](https://www.computerworld.com/article/4232827/google-wants-to-be-the-gatekeeper-for-enterprise-ai-agents.html)).
- 예상 쟁점: 에이전트가 자기 이름으로 메일을 보내고 문서를 고치는 구조에서, 잘못된 행동의 법적·업무상 책임이 에이전트를 만든 직원·관리자·구글 중 누구에게 있는지는 실제 사고 사례가 나와야 정리될 문제입니다(출처 없는 일반론).

## 앞으로 볼 체크포인트

- **2026년 10월 말~11월 초** — 정식 출시(GA) 여부와 범위(어떤 Workspace 요금제에서 쓸 수 있는지).
- **가격표 공개 시점** — 사용량 기반 단가, Workspace 과금 방식, Claude 선택 시 추가 비용.
- **신뢰성 자료** — 구글이 평가·실패율·사고 대응 자료를 내는지, 초기 고객의 독립적인 후기가 나오는지.
- **모델 피커 확대** — "다른 비공개·오픈 모델"이 실제로 언제, 어떤 모델로 추가되는지.
- **정부·헬스케어·리테일 버전** — "곧 출시"로만 언급, 일정 미공개.
- **마이크로소프트 Autopilot·Agent 365와의 비교** — 두 프리뷰가 GA로 갈 때 가격·통제 기능 차이.
- **차기 Alphabet 실적 발표** — 클라우드 매출과 AI 사용량 수치에 이번 에이전트가 어떻게 언급되는지(날짜는 확인되지 않음).

## 출처 목록

1. [Welcome to Gemini at Work 2026: Introducing the Gemini agent — Google Cloud Blog(토마스 쿠리안 키노트), 2026-10-09](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026)
2. [Google Cloud introduces the Gemini agent — Google 블로그, 2026-10-08](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/)
3. [Google brings agentic AI to Gemini, starting with businesses — TechCrunch(Sarah Perez), 2026-10-08](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/)
4. [Google is launching a one-stop Gemini agent for your work tasks — The Verge(Emma Roth), 2026-10-08](https://www.theverge.com/tech/1007904/google-gemini-ai-agent-enterprise)
5. [Google Cloud launches Gemini agent to work across enterprise systems — Constellation Research, 2026-10-08](https://www.constellationr.com/index%2ephp/insights/news/google-cloud-launches-gemini-agent-work-across-enterprise-systems)
6. [Google's workplace agent is out, but questions abound — TechTarget(Esther Shittu), 2026-10-08](https://www.techtarget.com/ai/news/366651779/Googles-workplace-agent-is-out-but-questions-abound)
7. [Google wants to be the gatekeeper for enterprise AI agents — Computerworld(Taryn Plumb), 2026-10](https://www.computerworld.com/article/4232827/google-wants-to-be-the-gatekeeper-for-enterprise-ai-agents.html)
8. [Pick Gemini agent when neutral model choice matters most — HFS Research, 2026-10-08](https://www.hfsresearch.com/quicktakes/pick-gemini-agent-when-neutral-model-choice-matters-most/)
9. [Google Built An AI Coworker And Gave It A Confusing Name — Forbes(Janakiram MSV), 2026-10-08](https://www.forbes.com/sites/janakirammsv/2026/10/08/google-built-an-ai-coworker-and-gave-it-a-confusing-name/) (검색 결과 발췌로 확인, 본문 전체는 열람하지 못함)
