# DreamHouse 브리핑 아카이브

평일 아침 브리핑을 **요약형**으로 날짜·분야별로 쌓는 아카이브입니다.

> 🌐 **공개 사이트 (GitHub Pages, 인터넷 전체 공개):** **https://dreamhouseksh.github.io/dreamhouse-briefings/**
> 저장소와 사이트 모두 **public**이며 Pages는 운영 중입니다. **누구나 볼 수 있으니** 공개되면 안 되는 내용은 커밋하지 마세요.

기사 전문 복제·통번역은 하지 않습니다. 각 항목은 넉넉한 요약 + 기술용어 괄호 설명 + 원문 링크이며, 대표 이미지는 저장소에 복제하지 않고 원문 이미지 URL을 핫링크해 보여 줍니다.

- 🤖 **에이전트라면 먼저:** [`AGENTS.md`](AGENTS.md) (핸드오프) → [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (상세 규칙)
- 📑 **목차(날짜별):** 사이트의 [전체 아카이브](https://dreamhouseksh.github.io/dreamhouse-briefings/archive/) (자동 생성) · 문서 허브 [`docs/index.md`](docs/index.md)

## 열람 방법

| 방법 | 주소 | 공개 범위 |
|---|---|---|
| **GitHub Pages 사이트 (권장)** | https://dreamhouseksh.github.io/dreamhouse-briefings/ | 🌐 **공개** (로그인 불필요) |
| 분야별 모아보기 | `/category/it/` · `/category/ai/` · `/category/model/` · `/category/engine/` · `/category/github/` | 🌐 공개 |
| 전체 아카이브 | https://dreamhouseksh.github.io/dreamhouse-briefings/archive/ | 🌐 공개 |
| 저장소 브라우즈 | https://github.com/DreamHouseKSH/dreamhouse-briefings | 🌐 공개 |
| github.dev (웹 에디터) | https://github.dev/DreamHouseKSH/dreamhouse-briefings — 저장소 페이지에서 `.` 키 | 🔒 편집은 로그인 필요 |

- Pages 설정: 브랜치 `main`, 폴더 `/`(루트), GitHub 기본 Jekyll 빌드. `main`에 push하면 1~2분 내 사이트에 반영됩니다.
- 사이트는 커스텀 레이아웃(`_layouts/default.html`, `assets/css/style.css`)으로 한국어 가독성(Pretendard 글꼴, 어절 단위 줄바꿈, 읽기 좋은 줄 길이, 라이트/다크 모드)에 맞췄습니다.
- 홈의 날짜·분야 목록은 `news/`, `github/` 폴더에서 **자동 생성**되고, 날짜별 하이라이트 한 줄은 `_data/highlights.yml`에서 읽습니다.

## 구조

```
AGENTS.md            # 에이전트 핸드오프
docs/
  WORKFLOW.md        # 루틴·스타일·저작권 규칙
  index.md           # 문서 허브 (사이트 /docs/)
news/YYYY-MM-DD/
  IT.md
  AI.md
  모델.md
  엔진.md            # 소식이 없으면 생략
github/YYYY-MM-DD.md
templates/news-item.md
_data/highlights.yml # 날짜별 하이라이트 (홈·아카이브 표시)
_config.yml, _layouts/, _includes/, assets/   # Pages 사이트 (Jekyll)
index.html, archive.html, category/           # 홈·아카이브·분야별 페이지
```

## 항목 형식

각 파일은 항목마다:

- 제목
- 원문 링크
- 넉넉한 한국어 요약 (과도한 축약 X)
- 기술 용어는 괄호로 풀어 씀 예: MoE(Mixture of Experts, 전문가 혼합)

## 자동화 (KST)

- 평일 08:01 뉴스 아카이브 → `news/`
- 평일 08:06 GitHub 트렌드 아카이브 → `github/`
- 매일 24시간, 15분마다(매시 05·20·35·50분) 리서치 요청 이슈 확인 → `research/` (요청 있을 때만, 최대 3건)

방문 통계는 GoatCounter(`dh-news`, IP·쿠키 저장 없음)로 헤더에 '오늘 N명'을 표시합니다. 작업 방식 변경 이력은 [`docs/WORKFLOW.md`](docs/WORKFLOW.md) 맨 위에 있습니다.
