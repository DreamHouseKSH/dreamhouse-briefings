# WORKFLOW — 브리핑 아카이브 운영 규칙

> 대상: 이 저장소에 쓰는 모든 DreamHouse / Grok Bot 에이전트. 요약 핸드오프는 루트의 [`AGENTS.md`](../AGENTS.md).

## 1. 전체 흐름

```
[평일 아침 루틴 (KST)]
  08:00 전후  IT·AI 뉴스 브리핑 → 사용자에게 채팅으로 전달
  08:01       뉴스 아카이브 루틴 → news/YYYY-MM-DD/{IT,AI,모델,엔진}.md 작성 → push
  08:06       GitHub 트렌드 루틴 → github/YYYY-MM-DD.md 작성 → push
  정오 무렵    엔진 다이제스트 전달 → news/YYYY-MM-DD/엔진.md 추가/갱신 → push
```

- **소스는 "사용자에게 실제로 전달된 브리핑"** 입니다. 아카이브에 새 뉴스를 추가 발굴하지 않습니다. 요약을 넉넉하게 만들기 위해 브리핑에 달린 **원문 링크를 읽는 것은 허용**되지만, 그 기사에 대한 사실 범위를 넘지 않습니다.
- 커밋 계정: gh 로그인 계정 **DreamHouseKSH** (박스 `/home/box/.config/gh`에 설정됨). 토큰 파일을 직접 읽거나 출력하지 마세요. `gh` / `git` 명령만 사용.
- 브랜치: `main` 직접 push. 충돌 시 `git pull --rebase` 후 재시도. force-push 금지(사용자 승인 필요).
- 커밋 메시지 예: `briefings: 2026-10-06 news (IT/AI/모델/엔진) + github trends`

## 2. 파일 레이아웃

| 경로 | 내용 | 비고 |
|---|---|---|
| `news/YYYY-MM-DD/IT.md` | IT 산업·반도체·보안·국내 기업 | |
| `news/YYYY-MM-DD/AI.md` | AI 기업·투자·제품·M&A | |
| `news/YYYY-MM-DD/모델.md` | 신규 모델 발표 | 성능 수치는 "회사 발표" 명시 |
| `news/YYYY-MM-DD/엔진.md` | 추론 엔진·런타임 릴리스, 관련 CVE | 소식 없으면 **파일 생략** |
| `github/YYYY-MM-DD.md` | GitHub 트렌드 | 카테고리별 표 + 별 증가량 |
| `templates/news-item.md` | 뉴스 항목 템플릿 | |
| `docs/index.md` | 날짜별 목차 | **새 날짜마다 맨 위에 행 추가** |

- 날짜는 **KST 기준 브리핑 전달일**. 파일명·폴더명은 `YYYY-MM-DD`.
- 파일 인코딩 UTF-8, 한글 파일명(`모델.md`, `엔진.md`) 그대로 사용.

## 3. 요약 스타일 규칙

각 뉴스 파일 구조:

```markdown
# {분야} 브리핑 — YYYY-MM-DD (요일, KST 아침)
> 한두 줄 안내(요약 아카이브이며 전문이 아님)

## N. {제목}
- **원문:** {url}
- **분야:** {IT|AI|모델|엔진} · {세부}
- **날짜:** {원문 날짜 또는 브리핑 날짜}

### 요약
{3~4문단 넉넉한 요약}

**시사점:** {한두 문장}
```

규칙:

1. **넉넉하게.** 한 줄 요약 금지. 무엇이/누가/왜/숫자/다음 체크포인트까지 3~4문단.
2. **기술 용어 괄호 풀이.** 처음 등장할 때 `용어(영문, 쉬운 설명)` 형태. 예: `KV 캐시(이전 토큰 계산 결과 저장소)`, `CVE(공개 취약점 식별 번호)`.
3. **수치·날짜·인명은 원문 그대로.** 반올림·추정 금지. 자체 발표·미검증 수치는 "회사 발표 기준"이라 표시.
4. **추측 금지.** 브리핑·원문에 없는 전망은 쓰지 않음. "시사점"은 원문 맥락에서 자연스럽게 도출되는 수준으로만.
5. **시간 표기는 KST.** 원문이 UTC/PT면 변환하거나 원문 기준임을 명시.
6. GitHub 파일: 카테고리별 표(저장소 링크 | 언어 | 누적 ⭐ | 일간/주간 증가) + 저장소별 1~2문장 설명(용어 괄호 풀이). 증가량 기준(일간=stars today, 주간=this week)을 상단에 명시.

## 4. 저작권 (중요)

- **기사 전문 스크랩·복제·전체 번역 금지.** 문단 단위 번역도 금지. 자기 말로 다시 쓴 요약만.
- 직접 인용은 꼭 필요할 때 한 문장 이내, 따옴표와 출처 표시.
- 원문 링크는 항상 포함 — 아카이브는 원문으로 가는 **안내판** 역할.
- 페이월 우회·로그인 필요 콘텐츠 긁어오기 금지.
- 이미지·차트 복제 금지(링크만).

## 5. 실행 시각 (cron, KST, 평일 월~금)

| 루틴 | cron (Asia/Seoul) | 산출물 |
|---|---|---|
| 뉴스 아카이브 | `1 8 * * 1-5` (08:01) | `news/YYYY-MM-DD/` |
| GitHub 트렌드 아카이브 | `6 8 * * 1-5` (08:06) | `github/YYYY-MM-DD.md` |

- 공휴일에도 루틴이 돌면 그대로 기록(브리핑이 없으면 파일을 만들지 않음).
- GitHub 트렌드 원천 스냅샷은 박스의 `/workspace/trend/{daily,weekly,go,rust}.html` 에 저장되어 있을 수 있음(아침 수집분). 별 수치 검증에 사용.

## 6. 열람 방법

### GitHub Pages를 쓰지 않는 이유

- 이 저장소는 **개인(User) 계정 DreamHouseKSH 소유의 private 저장소**입니다.
- GitHub Pages의 **비공개 게시(access control, 저장소 읽기 권한자만 열람)** 는 **GitHub Enterprise Cloud 조직 소유 저장소에서만** 가능합니다([공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)).
- 개인 계정(Pro 이상)에서 private 저장소로 Pages를 켜면 **사이트 자체는 인터넷 전체에 공개**됩니다 → 비공개 아카이브 + 저작권 방침과 충돌하므로 **켜지 않습니다**. 켜려면 사용자 명시 승인 필요.

### 권장 열람 방법

1. **목차(GitHub 마크다운 렌더링):** https://github.com/DreamHouseKSH/dreamhouse-briefings/blob/main/docs/index.md
2. **저장소 브라우즈:** https://github.com/DreamHouseKSH/dreamhouse-briefings → `news/`, `github/` 폴더
3. **github.dev 웹 에디터(검색·파일트리 편리):** https://github.dev/DreamHouseKSH/dreamhouse-briefings (저장소 페이지에서 `.` 키)
4. **모바일:** GitHub 앱에서 로그인 후 저장소 열람
5. **로컬:** `gh repo clone DreamHouseKSH/dreamhouse-briefings` 후 아무 마크다운 뷰어

모두 DreamHouseKSH 계정(또는 콜라보레이터)으로 로그인해야 보입니다.

## 7. 새 날짜 추가 절차 (복붙용)

```bash
cd /workspace/dreamhouse-briefings
git pull --ff-only
D=$(date +%F)            # 박스 시계는 KST
mkdir -p news/$D
# ... news/$D/{IT,AI,모델,엔진}.md, github/$D.md 작성 ...
# docs/index.md 표 맨 위에 $D 행 추가
git add -A
git commit -m "briefings: $D news + github trends"
git push origin main
```
