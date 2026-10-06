# DreamHouse 브리핑 아카이브

평일 아침 브리핑을 **요약형**으로 날짜·분야별로 쌓는 비공개 저장소입니다.
기사 전문 복제·통번역은 하지 않습니다. 각 항목은 넉넉한 요약 + 기술용어 괄호 설명 + 원문 링크입니다.

- 🤖 **에이전트라면 먼저:** [`AGENTS.md`](AGENTS.md) (핸드오프) → [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (상세 규칙)
- 📑 **목차(날짜별):** [`docs/index.md`](docs/index.md)

## 열람 방법

GitHub Pages는 사용하지 않습니다 — 개인 계정 private 저장소에서는 "로그인한 사람만 보는" 비공개 Pages가 불가능하고(Enterprise Cloud 조직 전용), 켜면 사이트가 인터넷에 공개되기 때문입니다. 대신:

| 방법 | 주소 |
|---|---|
| 목차 (GitHub 렌더링) | https://github.com/DreamHouseKSH/dreamhouse-briefings/blob/main/docs/index.md |
| 저장소 브라우즈 | https://github.com/DreamHouseKSH/dreamhouse-briefings |
| github.dev (웹 에디터, 검색 편리) | https://github.dev/DreamHouseKSH/dreamhouse-briefings — 저장소 페이지에서 `.` 키 |
| 모바일 | GitHub 앱 로그인 후 저장소 열람 |

모두 DreamHouseKSH 계정(또는 콜라보레이터) 로그인 필요.

## 구조

```
AGENTS.md            # 에이전트 핸드오프
docs/
  WORKFLOW.md        # 루틴·스타일·저작권 규칙
  index.md           # 날짜별 목차
news/YYYY-MM-DD/
  IT.md
  AI.md
  모델.md
  엔진.md            # 소식이 없으면 생략
github/YYYY-MM-DD.md
templates/news-item.md
```

## 항목 형식

각 파일은 항목마다:

- 제목
- 원문 링크
- 넉넉한 한국어 요약 (과도한 축약 X)
- 기술 용어는 괄호로 풀어 씀 예: MoE(Mixture of Experts, 전문가 혼합)

## 자동화 (KST, 평일)

- 08:01 뉴스 아카이브 → `news/`
- 08:06 GitHub 트렌드 아카이브 → `github/`
