# 심층 리서치 — 앤트로픽, 유료 플랜 기본 모델을 'Opus 5.5'로 전환

- **요청:** [#4](https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/4)
- **원래 기사:** [2026-11-16 AI · 2. 앤트로픽, 유료 플랜 기본 모델을 'Opus 5.5'로 전환 — "이제 'think hard'는 빼세요"](../news/2026-11-16/AI.md)
- **원문:** https://techprolonged.com/2026/11/opus-5-5-replaces-the-old-default-in-claudes-paid-plans/
- **작성:** 2026-11-17 07:32 KST

앤트로픽이 Pro·Max·Ultra·Team 플랜의 기본 모델을 Opus 5.5로 바꾼 것은 단순한 모델 교체가 아니라, "사용자가 모델을 고르고 프롬프트를 닦는 시대를 끝내겠다"는 선언에 가깝다. 회사의 내부 시험 수치는 그 방향을 뒷받침하지만, 핵심 수치 대부분이 앤트로픽 자체 평가라는 점은 분명히 짚고 넘어가야 한다.
{: .research-lead}

<div class="research-essay" markdown="1">

## 무슨 일이 있었나 — 기본값이 뒤집혔다

11월 12일 앤트로픽은 지식 업무용 모델 안내 문서를 공개하며 Opus 5.5가 Pro, Max, Ultra, Team 플랜의 기본 모델이 됐다고 밝혔다 ([Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work)). 이제 유료 사용자가 Claude를 열면 처음 선택된 모델이 가장 비싼 일반 라인업인 Opus 5.5다. 평소 Sonnet으로 일하고 큰 작업에만 Opus를 꺼내 쓰던 사용자는 따로 바꾸지 않는 한 큰 모델로 들어가게 된다.

전환과 함께 나온 지침이 더 눈길을 끈다. 앤트로픽은 프롬프트에서 "think hard", "think carefully" 같은 문구를 지우라고 권한다. Opus 5.5는 항상 추론이 켜져 있고, 요청 내용과 effort(모델이 답변에 쓰는 사고의 깊이를 조절하는 설정) 값을 보고 스스로 얼마나 생각할지 정하기 때문이다. 회사는 이 문구를 뺀 프롬프트로 시험한 결과 답변이 더 빨리 시작되고 품질 저하는 눈에 띄지 않았다고 밝혔다. 기본 effort인 Medium에서는 코딩·지식 업무 평가에서 전작 Opus 5의 High와 같거나 나았다는 것이 회사 설명이다 ([The Decoder](https://the-decoder.com/anthropic-says-outdated-prompting-habits-are-slowing-down-claude-opus-5-5/), 11-14).

## 왜 중요한가 — 프롬프트 요령의 시대가 저물고 있다

"think hard" 같은 문구는 약 1년 반 전, 추론 모델 초기에 사용자들이 모델의 성능을 억지로 끌어올리던 시절의 유산이다. The Decoder는 이번 지침이 "오늘날 표준이 된 적응형 추론 이전 시대의 습관 정리"라고 해석했다. 모델이 스스로 사고량을 조절하게 되면서, 사용자가 더 나은 답을 얻기 위해 외우던 주문들이 오히려 방해가 되는 단계에 온 것이다.

가격 구조 변화도 있다. 토큰당 가격은 Haiku 5.5가 입력 0.10달러·출력 0.50달러, Sonnet 5.5가 2달러·10달러, Opus 5.5가 4달러·20달러, Fable 5.2가 8달러·40달러(100만 토큰 기준, 회사 발표)다. 앤트로픽의 논리는 "더 똑똑한 모델은 더 적은 단계로 끝내니 실제 작업당 비용은 비례해 오르지 않는다"는 것이다. 회사가 든 예시에서, 가상의 인사 소프트웨어 회사 합병 건을 분석해 엑셀 모델과 임원용 발표 자료까지 만드는 작업에 Opus 5.5는 63분이 걸렸고 비용은 절반이었던 반면, Opus 5는 93분이 걸렸다. 다만 고가 모델은 플랜 사용 한도를 더 빨리 소진하고, Pro 플랜에서는 Fable 5.2가 한도가 아니라 별도 사용 크레딧을 쓴다는 조건이 붙는다 ([Tech Prolonged](https://techprolonged.com/2026/11/opus-5-5-replaces-the-old-default-in-claudes-paid-plans/), 11-14).

## 누가 어떻게 보나 — 회사의 자신감과 얼리 테스터의 호응

앤트로픽은 강점으로 문서·리서치·재무·차트 읽기를 꼽는다. 내부 연구 시험에서 기업의 실적 발표 자료를 저장된 웹 스냅샷 안에 숨겨 두고 보고서를 쓰게 한 뒤, 숫자나 인용이 하나라도 지어낸 것이면 탈락시키는 방식으로 채점했더니 18편 중 16편이 통과했다고 한다. 차트 읽기에서는 가장 낮은 effort 설정에서도 전작 Opus 5의 최고 설정보다 정확했다는 것이 회사 주장이다.

얼리 테스터의 인용도 공개됐다. 결제 기업 Ramp의 스태프 엔지니어 존 루엘라스는 "좋은 동료처럼 글을 쓰고 우리의 문체 규칙을 따른다"고 했고, 투자사 Walleye Capital의 프랭크 코라오는 Opus 5.5가 자사 지시문의 분(minute) 인덱싱이 하나 어긋난 것을 스스로 발견해 수정했다며 "이전까지 시험한 어떤 모델도 잡아내지 못한 것"이라고 평했다. 개발 도구 회사 Factory의 리쯔무 리는 "Medium effort에서 기본으로 쓸 첫 모델"이라며 Opus 5 High와 같은 수준에 출력 토큰을 20~25% 덜 썼다고 말했다. 모두 앤트로픽 문서에 실린 인용이며, 논조는 회사 발표와 얼리 테스터 모두 긍정적이다.

## 반론과 숨은 쟁점, 숫자 읽는 법

찾은 범위(The Decoder·Tech Prolonged·회사 문서)에서 명시적인 반론 기사는 없었다. 다만 구조적인 쟁점은 있다. 첫째, 63분 대 93분, 16/18 통과, 토큰 20~25% 절감은 전부 앤트로픽이 설계하고 채점한 시험이다. 독립 벤치마크가 아니므로 "회사 발표 기준"으로 읽어야 한다. 둘째, 기본값 전환은 사용자 경험 개선이자 동시에 매출 구조 개선이다. 고가 모델이 기본이 되면 한도 소진이 빨라지고, 사용량 과금으로 넘어가는 사용자가 늘 수 있다. "더 적은 단계로 끝낸다"는 주장이 맞아도, 작업마다 그 이득이 다르다는 점은 각자 확인할 문제다. 셋째, Sonnet 5.5를 Extra high나 Max로 올리면 작업당 비용이 Opus 5.5에 근접한다는 회사 계산은, 습관적으로 effort를 올리는 사용법 자체를 바꾸라는 메시지이기도 하다.

## 그래서 어떻게 보면 되나

이번 전환은 "모델 선택과 프롬프트 닦기"라는 사용자 숙제를 회사가 흡수하기 시작했다는 신호로 읽는 게 정확하다. 당장 실무에서 바꿀 것은 단순하다. Opus 5.5를 Medium에 두고, "think hard"를 지우고, 첫 메시지에 완성물의 모습을 적는 것이다. 다만 회사의 비용·품질 수치는 자사 시험이라는 꼬리표가 붙으므로, 자기 작업에서 한 번 비교해 보는 것이 어느 리뷰보다 정확하다. 이 판단이 바뀔 조건은 독립 벤치마크나 실사용 비용 데이터가 쌓여 회사 주장과 어긋날 때다.

</div>

---

<details class="research-refs" markdown="1">
<summary>참고 자료 — 핵심 수치 · 체크포인트 · 출처 목록</summary>

### 핵심 수치

| 수치·사실 | 출처 | 검증 여부 |
|---|---|---|
| Pro·Max·Ultra·Team 기본 모델 = Opus 5.5 | [Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) | 회사 발표 |
| "think hard" 제거 시 답변 시작 빨라지고 품질 저하 없음 | [The Decoder](https://the-decoder.com/anthropic-says-outdated-prompting-habits-are-slowing-down-claude-opus-5-5/) | 회사 시험 인용 |
| Opus 5.5 Medium = Opus 5 High 이상(코딩·지식 업무 평가) | [Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) | 회사 발표 |
| 가상 합병 분석 63분·비용 절반(Opus 5는 93분) | [Tech Prolonged](https://techprolonged.com/2026/11/opus-5-5-replaces-the-old-default-in-claudes-paid-plans/) | 회사 발표 인용 |
| 보고서 시험 18편 중 16편 통과(지어낸 수치 0건 조건) | [Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) | 회사 발표 |
| 토큰당 가격(입력/출력, 백만 토큰): Haiku 5.5 $0.10/$0.50 · Sonnet 5.5 $2/$10 · Opus 5.5 $4/$20 · Fable 5.2 $8/$40 | [Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) | 회사 발표 |
| Factory 리쯔무 리: 출력 토큰 20~25% 절감 | [Claude 공식 문서](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) | 회사 문서 인용 |

### 앞으로 볼 체크포인트

- 독립 벤치마크·사용자 비용 데이터: Medium 기본값의 실제 품질·비용 균형이 회사 주장과 맞는지
- Pro 플랜 한도 소진 속도: Opus 5.5 기본값 이후 한도 도달 불만이 느는지
- 경쟁사 대응: OpenAI·구글이 같은 방식(기본값 상향 + 프롬프트 지침 정리)으로 따라가는지

### 출처 목록

1. [Using Claude Opus 5.5 as your daily driver for knowledge work — Claude by Anthropic, 2026-11-12](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work)
2. [Anthropic says outdated prompting habits are slowing down Claude Opus 5.5 — The Decoder, 2026-11-14](https://the-decoder.com/anthropic-says-outdated-prompting-habits-are-slowing-down-claude-opus-5-5/)
3. [Opus 5.5 replaces the old default in Claude's paid plans — Tech Prolonged, 2026-11-14](https://techprolonged.com/2026/11/opus-5-5-replaces-the-old-default-in-claudes-paid-plans/)

</details>
