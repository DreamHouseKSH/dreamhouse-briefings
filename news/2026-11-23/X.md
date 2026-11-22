# X 브리핑 — 2026-11-23 (월, KST 아침)

## 1. 샘 알트만 — OpenAI 사전학습 '퍼플렉시티' 전격 공개, 프론티어 모델 공통 상한선 제안
- **게시글:** https://x.com/sama/status/2124551594691932405
- **날짜:** 2026-11-22 (KST 2026-11-23 02:12) · 후속: [공통 상한선 인용](https://x.com/sama/status/2124551883130114403), [백악관 협약 연계](https://x.com/sama/status/2124558713646428663)

### 인용
> "This is the most important thing OpenAI has published in awhile. We are providing a lot of transparency into our pretraining progress and hope we can agree as a field to common limits. I think that would be very wise and help ensure safety and control."

최근 OpenAI가 공개한 것 중 가장 중요한 발표라며, 사전학습 진행 상황을 투명하게 공개한 만큼 AI 업계가 공통 상한선(common limits)에 합의해 안전과 통제를 확보하기를 바란다고 밝혔다. 이어 백악관 협약(White House Accords) 아래 랩들이 안전 표준을 세우기로 합의한 만큼, 퍼플렉시티(perplexity) 지표 논의가 그 목표를 앞당길 것이라고 덧붙였다.

### 해석
- **배경:** 같은 날 OpenAI 수석과학자 야쿠프 파호츠키(Jakub Pachocki)는 공식 블로그 글 「Perplexity and Intelligence」([원문](https://openai.com/index/perplexity-and-intelligence/))를 통해 GPT-3.5부터 최신 모델까지 내부 코드베이스 기준 로그 퍼플렉시티(cross-entropy loss) 추이를 공개했다. 로그 퍼플렉시티 ~0.76 도달 이후 수학 미해결 난제들이 연속 돌파됐으며, ~0.68~0.7 구간 진입 시 예측하지 못한 변혁적 능력이 출현하는 반면 사고의 사슬(CoT) 모니터링 등 기존 정렬 감사 기법은 오히려 무력화될 수 있다고 경고했다.
- **행간:** 경쟁사에게 자사 사전학습 진척도를 노출할 위험을 감수하고 수치를 공개한 것은, 2027년 초부터 AI가 사전학습 알고리즘 연구 자체를 가속하는 '재귀적 자기개선' 초입에 들어설 수 있다는 위기감의 표현이다. CoT 모니터의 후속 감시 기술이 확보될 때까지 특정 퍼플렉시티 임계치 이상으로 학습을 진행하지 말자는 '속도 조절 협약'을 경쟁 랩들에 공개 제안한 셈이다.
- **업계 영향:** 지금까지 각 랩이 비공개로 감춰온 사전학습 손실(loss) 곡선을 안전 규제의 공통 자(yardstick)로 삼자는 첫 공식 제안으로, Anthropic·Google DeepMind·xAI 등이 이에 호응해 교차 평가 표준 논의로 이어질지 주목된다.

### 논조·다른 시각
- **논조:** 산업 전반의 안전·통제 표준 합의를 촉구하는 진지하고 선제적인 어조.
- **논조 점검:** 연구소마다 평가 데이터셋과 학습 데이터 혼합이 달라 퍼플렉시티를 단순 비교하기 어렵고, 추론(CoT) 강화학습으로 인한 성능 향상은 퍼플렉시티 하락에 반영되지 않는다는 한계를 OpenAI 스스로도 인정했다. 또한 일각에서는 "자사만 멈추면 투자자에게 설명하기 어렵기 때문에 경쟁사도 함께 멈추게 하는 기준을 제안한 것"이라는 전략적 해석도 나온다.
- **다른 시각:** [OpenAI 공식 블로그](https://openai.com/index/perplexity-and-intelligence/), [State of AI 분석](https://www.thestateofai.com/news/sam-altman-openai-shared-ai-training-limits)

---

## 2. 얀 르쿤 — "Llama-4는 실망스러웠다": Meta 오픈 모델 정책 보류와 AMI Labs 창업 내막
- **게시글:** https://x.com/ylecun/status/2124623496915361866
- **날짜:** 2026-11-22 (KST 2026-11-23 06:58) · 후속: [오픈 파운데이션 모델 다양성론](https://x.com/ylecun/status/2124623848956170389)

### 인용
> "Llama-3 was good. Llama-4 was a disappointment because the team was under huge time pressure and had to be conservative. Then Mark rebooted the whole AI organization and the open model policy was temporarily put on hold. After that (but not entirely because of that), I left to start AMI Labs."

자신은 Llama의 기술 개발이 아니라 Llama-2의 공개를 주장하는 데 주로 관여했고 그것이 AI 산업을 점화시켰다고 회고했다. 이어 Llama-3는 좋았으나 Llama-4는 팀이 극심한 시간 압박 속에서 보수적으로 갈 수밖에 없어 실망스러웠으며, 이후 마크 저커버그가 AI 조직 전체를 재편하면서 오픈 모델 정책이 일시 보류되었고 그 뒤(전적인 이유는 아니지만) 자신이 Meta를 떠나 AMI Labs를 창업했다고 밝혔다.

### 해석
- **배경:** 튜링상 수상자인 얀 르쿤은 올해 초 Meta를 떠나 파리에 거점을 둔 월드 모델 스타트업 AMI Labs(Advanced Machine Intelligence)를 공동 창업해 35억 달러 기업가치로 10억 3,000만 달러를 투자받았다(TechCrunch·MIT Tech Review). Meta는 Scale AI 인수 및 AI 조직 대개편 이후 폐쇄형·상용 전략 쪽으로 무게중심을 옮긴 상태다.
- **행간:** 르쿤이 강조한 핵심은 '오픈 파운데이션 모델의 부재가 낳을 문화적·언어적 편향'이다. 미국 랩들이 일제히 폐쇄형으로 돌아서면서 현재 선도적인 오픈소스 모델은 사실상 중국계만 남았는데, 각국이 자국 언어·가치관·관심사에 맞는 AI 어시스턴트를 구축하려면 누구든 파인튜닝할 수 있는 개방형 기반 모델이 필수라는 주장이다.
- **업계 영향:** 미국 내 대표 오픈소스 진영이던 Meta의 정책 선회 이후, 오픈소스·월드 모델 기반의 '미국-중국 양강 구도 외 제3의 대안'을 표방하는 AMI Labs의 연구 성과와 오픈소스 공개 속도에 글로벌 스타트업·학계의 기대가 쏠리고 있다.

### 논조·다른 시각
- **논조:** Meta 시절 내부 사정을 담담하게 복기하면서도 오픈소스 AI 생태계의 필요성을 역설하는 소신 있는 어조.
- **논조 점검:** 르쿤이 주창하는 JEPA(Joint Embedding Predictive Architecture) 기반 월드 모델은 텍스트를 넘어 물리 세계를 이해하는 차세대 대안으로 꼽히지만, 당장 상용 제품에서 검증된 대규모 언어모델(LLM) 생태계를 대체하기까지는 상당한 연구와 시간이 더 필요하다는 신중론도 공존한다.
- **다른 시각:** [MIT Tech Review 인터뷰](https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/), [TechCrunch 보도](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/)

---

## 3. 기예르모 라우흐 — 무료 '스텔스 모델(ZDR)' 경고: "국가 주도 데이터 유출 통로"
- **게시글:** https://x.com/rauchg/status/2124595496849445079
- **날짜:** 2026-11-22 (KST 2026-11-23 05:06)

### 인용
> "These stealth models are mechanisms of industrial scale data exfiltration to nation state programs, I strongly suspect, and the Dragos research seems to confirm. Imagine explaining to your boss: sorry chief, I *had* to try this really cool ZDR free stealth model… all our secrets, customer data, and code are now in a different continent!"

무료 '스텔스 모델' 추론에 Zero Data Retention(ZDR·데이터 미보관)을 내걸어 수백만 조회수를 끄는 공급자들을 겨냥해, 이들이 실제로는 국가 주도 프로그램으로 데이터를 빼돌리는 산업 규모 유출 통로이며 Dragos의 보안 연구가 이를 뒷받침한다고 경고했다. Vercel AI Gateway는 이런 지름길 없이 실제 토큰 물량을 키워왔으며, 내일(현지시간) 신뢰·프라이버시·보안 기준을 한층 끌어올리는 방안을 공개하겠다고 예고했다.

### 해석
- **배경:** 보안 기업 Dragos(HD Moore 등)는 11월 19일 공개한 보고서([원문](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens))에서 지난 5개월간 약 200만 건의 프롬프트에 추적용 카나리 토큰(AWS 키·비밀 URL·Git 저장소 등)을 심어 AI 라우터·추론 마켓플레이스에 전송한 결과를 발표했다. 최소 3개 호스팅 공급자가 침해됐고, 저가 리셀러들이 로깅을 켜 프롬프트를 탈취했으며, 특히 미국 기반 공급자에 ZDR 플래그를 달아 보낸 프롬프트가 중국 AI 랩 스크래퍼로 넘어가거나 24일 뒤 중국 내부 메신저(Feishu) 대화방에 공유된 사례까지 포착됐다.
- **행간:** 11월 22일 AI 라우터 플랫폼 OpenRouter가 공급자 3곳을 퇴출하고 125개 엔드포인트의 ZDR 자격을 박탈한 직후 나온 발언으로, Vercel이 자사 AI Gateway의 무결성과 엔드포인트 검증 체계를 경쟁력으로 전면 부각하려는 포석이기도 하다.
- **업계 영향:** 개발자들이 비용 절감이나 신형 모델 테스트를 위해 검증되지 않은 저가 라우터·무료 스텔스 모델을 무심코 연동하던 관행에 제동이 걸리며, 기업용 AI 게이트웨이 시장에서 '네트워크 경로 실검증 및 ZDR 보증'이 핵심 조달 기준으로 부상할 전망이다.

### 논조·다른 시각
- **논조:** 무료·저가 추론 유혹에 빠진 개발자 생태계에 경종을 울리는 직설적이고 단호한 경고.
- **논조 점검:** Dragos 보고서가 지적한 유출 경로는 일부 저가 마켓플레이스 리셀러·침해된 호스팅 업체와 특정 우회 경로에 집중돼 있어, OpenRouter 등 중개 플랫폼 자체의 침해가 아님은 OpenRouter 측 공지에서도 확인된다. 다만 'ZDR 표시만 믿고' 사내 기밀·API 키를 라우팅하는 위험은 업계 전반의 실질적 취약점으로 드러났다.
- **다른 시각:** [Dragos 연구 보고서](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens), [OpenRouter 공식 공지](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/)

---

## 4. 빌 애크먼 — "주식은 싸다, 다만 수급·기술적 흐름이 시장을 지배할 뿐"
- **게시글:** https://x.com/BillAckman/status/2124531883987833082
- **날짜:** 2026-11-22 (KST 2026-11-23 00:54) · 후속: [지수 내 고품질·고성장 기업 비중 근거](https://x.com/BillAckman/status/2124547922645688823)

### 인용
> "Stocks are cheap. Technicals, however, rule the day."
> "It is cheap in light of the higher quality higher growth mix of companies that represent such a large share of the index."

현재 주식시장은 밸류에이션상 싸지만 단기적으로는 기술적 흐름(수급·차트)이 시장을 지배하고 있다고 진단했다. 이어 지수에서 큰 비중을 차지하는 기업들이 과거보다 훨씬 높은 품질과 고성장 구성을 갖추고 있다는 점을 감안하면 현재 주가 수준은 명백히 저평가 상태라고 강조했다.

### 해석
- **배경:** 최근 미국 증시 조정으로 S&P 500 지수가 7,000선 아래로 밀리면서 선행 PER이 16.4배(2022년 이후 최저)까지 내려왔고, 성장주와 가치주의 밸류에이션 멀티플이 2008년 금융위기 이후 처음으로 같은 수준까지 수렴했다(에드 야데니·NoFOMO 집계). NVIDIA 일간 RSI가 15 아래로 떨어지는 등 기술적 과매도 논쟁도 가열되고 있다.
- **행간:** 펀더멘털상 매수 적기라는 대형 헤지펀드 매니저의 시각을 밝히면서도, 당장의 낙폭 확대는 실적 악화가 아닌 레버리지 청산과 기술적 매도세 때문이므로 단기 변동성에 유의해야 한다는 메시지다.
- **업계 영향:** AI 빅테크 중심의 급락장 속에서 '실적 대비 과도한 조정(저가 매수 기회)' 진영과 'AI가 기존 이익-주가 공식을 깨고 있다'는 경계 진영 간의 월가 논쟁이 한층 뚜렷해졌다.

### 논조·다른 시각
- **논조:** 단기 수급 불안을 인정하면서도 펀더멘털 저평가를 확신하는 가치투자자 특유의 냉정한 어조.
- **논조 점검:** 같은 날 로이드 블랭크페인 전 골드만삭스 CEO는 X에서 "AI가 실적과 주가의 통상적인 관계를 바꾸고 있다. 그저 또 하나의 환각(hallucination)이길 바란다"며 신중론을 폈고, 다수 투자자들도 "선행 실적 추정치가 유지된다는 전제하에서만 싸다", "싼 주식은 더 싸질 수 있다"며 분할 매수나 관망으로 맞섰다.
- **다른 시각:** [NoFOMO 시장 요약 및 블랭크페인 반응](https://nofomo.top/story/3329-ackman-says-stocks-cheap-technicals-rule)
