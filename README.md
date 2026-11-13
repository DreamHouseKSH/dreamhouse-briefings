# DreamHouse 브리핑 아카이브

매일 아침 뉴스와 주요 테크 리더들의 X(트위터) 포스트, 평일 GitHub 트렌드를 **요약 및 심층 해석형**으로 날짜·분야별로 쌓는 아카이브입니다.

> 🌐 **공개 사이트 (GitHub Pages, 인터넷 전체 공개):** **https://daily.dahangis.co.kr/**  
> 저장소와 사이트 모두 **public**이며 Pages는 정기 운영 중입니다. **누구나 열람할 수 있으니** 비공개 업무 정보나 개인정보는 커밋하지 않습니다.

기사 전문 복제나 단순 기계 번역은 하지 않습니다. 각 항목은 넉넉한 사실 요약과 전문 기술용어 괄호 풀이, 원문 링크, 그리고 교차 검증(다른 시각/반론)을 함께 제공합니다.

- 🤖 **에이전트 핸드오프:** [`AGENTS.md`](AGENTS.md) → 상세 규칙 [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
- 👥 **X 모니터링 인물 명단:** [`PEOPLE.md`](PEOPLE.md) (AI · IT/인프라 · 경제/투자 19인 추적 풀)
- 📑 **전체 목차:** 사이트 [전체 아카이브](https://daily.dahangis.co.kr/archive/) · 문서 허브 [`docs/index.md`](docs/index.md)

---

## 열람 방법

| 방법 | 주소 | 공개 범위 |
|---|---|---|
| **GitHub Pages 사이트 (권장)** | https://daily.dahangis.co.kr/ | 🌐 **공개** (로그인 불필요) |
| **분야별 모아보기** | `/category/it/` · `/category/ai/` · `/category/model/` · `/category/engine/` · `/category/x/` · `/category/github/` | 🌐 공개 |
| **전체 아카이브** | https://daily.dahangis.co.kr/archive/ | 🌐 공개 |
| **저장소 브라우즈** | https://github.com/DreamHouseKSH/dreamhouse-briefings | 🌐 공개 |
| **github.dev (웹 에디터)** | https://github.dev/DreamHouseKSH/dreamhouse-briefings — 저장소 페이지에서 `.` 키 | 🔒 편집은 로그인 필요 |

- **Pages 환경:** `main` 브랜치 루트(`/`), GitHub 기본 Jekyll 빌드. push 후 1~2분 내 서비스 반영.
- **한국어 가독성 최적화:** Pretendard 폰트, 어절 단위 줄바꿈, 라이트/다크 모드 지원.
- **자동 색인:** 홈과 아카이브의 날짜·분야 목록은 `news/`, `github/` 폴더에서 자동 생성되며, 상단 한 줄 하이라이트는 `_data/highlights.yml`을 참조합니다.

---

## 디렉터리 구조

```text
AGENTS.md            # 에이전트 역할 및 작업 인계 규약
PEOPLE.md            # X 브리핑 모니터링 핵심 인물 명단 (19인)
docs/
  WORKFLOW.md        # 수집·검증·작성·스타일 상세 규칙
  ARTICLE-INDEX.md   # 기사 중복 방지 및 사건 색인 운영 가이드
  index.md           # 문서 허브 (사이트 /docs/)
news/YYYY-MM-DD/
  IT.md              # IT 산업·반도체·클라우드·보안·국내 기업
  AI.md              # AI 기업 동향·투자·인프라·M&A
  모델.md            # 신규 파운데이션 모델 발표 (공식 발표 수치 명시)
  엔진.md            # 추론 엔진·경량화 런타임 릴리스 (소식 없으면 생략)
  X.md               # 주요 테크·경제 리더 19인 핵심 포스트 및 심층 해석
github/YYYY-MM-DD.md # 평일 GitHub 일일 트렌드 (스타 급상승 및 카테고리별 정리)
templates/
  news-item.md       # 일반 뉴스 항목 템플릿
_data/
  x-watchlist.yml    # X 브리핑 추적 인물 데이터 (PEOPLE.md 연계)
  highlights.yml     # 날짜별 주요 소식 하이라이트
  glossary.yml       # 전문 기술 용어 사전
_config.yml, _layouts/, _includes/, assets/   # Jekyll 사이트 빌드 리소스
index.html, archive.html, category/           # 웹 페이지 인터페이스
```

---

## 항목 작성 규격

### 1. 일반 뉴스 (`IT.md`, `AI.md`, `모델.md`, `엔진.md`)
- 제목 및 원문 출처 링크
- 사실에 입각한 충실한 요약 (과도한 축약 지양)
- 첫 등장 기술 약어는 괄호 풀이 명시 (예: MoE, JEPA, ABI)
- 기사 논조 점검 및 타 매체의 다른 시각(반론/후속 보도) 링크 1~3개 교차 검증

### 2. X 브리핑 (`X.md`)
- 대상: [`PEOPLE.md`](PEOPLE.md) 19인 인물 풀 기준 최근 24시간 핵심 글 3~5건
- 항목 구성:
  - `## N. {인물명} — {핵심 요약 제목}`
  - `- **게시글:** {x.com 원문 링크}`
  - `- **날짜:** {작성일시}`
  - `### 인용`: 영어 원문 발췌 + 한국어 번역 요약
  - `### 해석`: 배경, 행간의 의미(생략된 맥락), 업계 및 시장 파급력
  - `### 논조·다른 시각`: 작성자 논조 분석 및 커뮤니티/업계 반응 링크

---

## 자동화 파이프라인 (KST 기준)

- **매일 07:00** — **X 브리핑 작성 및 배포** (`news/YYYY-MM-DD/X.md`)  
  글로벌 리더 19인의 최근 24시간 포스트 수집, 사실 검증, 해석 및 교차 검증 후 main 브랜치 커밋·푸시.
- **매일 08:01** — **일일 뉴스 브리핑 아카이브** (`news/YYYY-MM-DD/`)  
  IT · AI · 모델 · 엔진 4개 분야의 신규 뉴스 수집, 중복 게이트 통과 후 발행.
- **평일 08:06** — **GitHub 트렌드 아카이브** (`github/YYYY-MM-DD.md`)  
  당일 오픈소스 스타 급상승 저장소 선별 및 요약.
- **상시 (15분 주기)** — **리서치 이슈 모니터링** (`research/`)  
  저장소 Issue에 등록된 심층 조사 요청 감지 및 리서치 문서 생성.

---

## 기사 색인 및 중복 검증

뉴스 중복 발행을 방지하기 위해 `article-index/editions/`의 날짜별 JSON 메타데이터를 운영합니다. 신규 발행 전 `scripts/article-index.py`를 통해 사건 식별자와 URL 중복 여부를 전수 검사(`gate`)한 후 발행합니다. 상세 내용은 [기사 색인 운영](docs/ARTICLE-INDEX.md)을 참고합니다.
