# AGENTS.md — DreamHouse 브리핑 아카이브 핸드오프

이 파일은 이 저장소를 이어서 다루는 **모든 DreamHouse / Grok Bot 에이전트**를 위한 1차 안내서입니다. 작업 전에 반드시 읽고, 상세 규칙은 [`docs/WORKFLOW.md`](docs/WORKFLOW.md)를 따르세요.

## 이 저장소는 무엇인가

- 사용자(성현 김)에게 평일 아침 전달되는 **IT·AI·모델·엔진 뉴스 브리핑**과 **GitHub 트렌드 브리핑**을 날짜별로 쌓는 아카이브입니다. 저장소는 **public**이고, 내용은 **GitHub Pages로 인터넷에 공개(운영 중)** 됩니다 → https://dreamhouseksh.github.io/dreamhouse-briefings/ (사용자 승인, 2026-10-06)
- 저장소: https://github.com/DreamHouseKSH/dreamhouse-briefings (public, 기본 브랜치 `main`)
- 박스(box) 작업 경로: `/workspace/dreamhouse-briefings` — 없으면 `gh repo clone DreamHouseKSH/dreamhouse-briefings`
- gh 인증 계정: **DreamHouseKSH** (박스에 이미 로그인됨, `gh auth status`로 확인). 다른 계정으로 push하지 마세요.

## 가장 중요한 규칙 5가지

1. **전문 복제·번역 금지.** 기사 본문을 통째로 옮기거나 번역하지 않습니다. 항상 "넉넉한 한국어 요약 + 원문 링크". **이미지는 저장소에 저장하지 않고** 원문의 og:image/대표 이미지 URL을 `### 미디어` 섹션에 핫링크만(+ `> 출처:` 줄). 없으면 섹션 생략.
2. **기술 용어는 괄호로 풀어쓰기.** 예: `MoE(Mixture of Experts, 전문가 혼합 — 일부 하위 네트워크만 골라 계산하는 구조)`.
3. **사실을 지어내지 않기.** 브리핑(또는 그 원문)에 있는 사실만 씁니다. 표현은 풀어 써도 되지만 수치·날짜·주장은 원문 그대로. 회사 자체 발표 수치는 "회사 발표 기준"이라고 표시.
4. **시간은 KST(Asia/Seoul).** 파일 날짜·문서 내 시각 모두 KST 기준. UTC로 표시된 원문 시각은 변환해서 적습니다.
5. **`main`에 직접 커밋·push** 하되, force-push·히스토리 재작성은 사용자 승인 없이 하지 않습니다.

## 파일 레이아웃 (요약)

```
news/YYYY-MM-DD/IT.md      # IT 산업·반도체·보안
news/YYYY-MM-DD/AI.md      # AI 기업·투자·제품
news/YYYY-MM-DD/모델.md     # 신규 모델 발표
news/YYYY-MM-DD/엔진.md     # 추론 엔진(vLLM, llama.cpp, SGLang, Ollama…) — 소식 없으면 파일 생략
github/YYYY-MM-DD.md       # GitHub 트렌드 (카테고리별 표 + 별 증가량)
templates/news-item.md     # 뉴스 항목 템플릿
docs/WORKFLOW.md           # 상세 운영 규칙
docs/index.md              # 문서 허브 (사이트 /docs/)
_data/highlights.yml       # 날짜별 하이라이트 한 줄 (새 날짜 추가 시 갱신!)
_config.yml, _layouts/, _includes/, assets/, index.html, archive.html, category/  # Pages 사이트
```

## 매일 해야 할 일 (체크리스트)

1. `cd /workspace/dreamhouse-briefings && git pull --ff-only`
2. 아침 루틴에서 전달된 브리핑 내용으로 `news/<오늘>/*.md`, `github/<오늘>.md` 작성 (템플릿·스타일은 WORKFLOW 참고). 각 항목 원문의 `og:image` 를 찾아 `### 미디어` 에 핫링크(WORKFLOW 3·4장)
3. `_data/highlights.yml` 맨 위에 오늘 날짜 하이라이트 추가 (날짜 목록·분야 링크는 사이트가 폴더에서 **자동 생성**하므로 목차 표 편집 불필요)
4. `git add -A && git commit -m "briefings: YYYY-MM-DD news + github trends" && git push origin main`

## 실행 시각 (KST, 평일)

| 루틴 | 시각 | 결과물 |
|---|---|---|
| 뉴스 브리핑 아카이브 | **08:01** | `news/YYYY-MM-DD/` |
| GitHub 트렌드 아카이브 | **08:06** | `github/YYYY-MM-DD.md` |
| (엔진 다이제스트) | 정오 무렵 전달분 | `news/YYYY-MM-DD/엔진.md` 에 추가/갱신 |

## 열람 방법 (GitHub Pages — 공개)

- **사이트(운영 중):** https://dreamhouseksh.github.io/dreamhouse-briefings/ — 브랜치 `main` / 폴더 `/`(루트), GitHub 기본 Jekyll 빌드. push 후 1~2분 내 반영.
- ⚠️ **사이트와 저장소 모두 인터넷 전체 공개**입니다. 요약·원문 링크 원칙(저작권)을 더 엄격히 지키고, 공개되면 안 되는 메모·개인정보는 커밋하지 마세요.
- push 후 빌드 확인: `gh api repos/DreamHouseKSH/dreamhouse-briefings/pages/builds/latest --jq .status` → `built` 이면 정상.
- 사이트 구조 상세: [`docs/WORKFLOW.md`](docs/WORKFLOW.md) 6장.

## 알려진 공백 / 다음 에이전트에게

- `news/2026-10-06/엔진.md` 의 링크는 채팅 원본 링크 대신 **공식 릴리스 노트 등 1차 출처**로 채웠습니다. 원본 링크를 확인할 수 있으면 교체해도 됩니다.
- `github/2026-10-06.md` 의 카테고리 구분은 아카이브 작성 시 재구성한 것입니다. 별 수치는 당일 08시대 GitHub Trending 스냅샷(`/workspace/trend/*.html`) 기준.
