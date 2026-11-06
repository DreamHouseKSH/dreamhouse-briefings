# 기사 색인·게시 전 중복 검사

이 색인은 공개된 우리 브리핑의 제목·출처·자체 요약을 다시 찾고 중복을 검토하는 장치입니다. 기사 전문을 내려받거나 저장하지 않으며, 과거 Markdown·발표 JSON·음성·source hash를 바꾸지 않습니다. 원출처의 사실·발표 시각을 확인하는 조사와 배포 확인은 별도입니다.

## 저장 구조와 식별 기준

- **지속 원본:** `article-index/config.json`, `article-index/editions/YYYY-MM-DD.json`. Git에서 이력을 관리하고 공개 사이트에서도 같은 JSON에 접근할 수 있습니다. 요약은 기존 공개 브리핑의 첫 요약 문단이며, 제3자 기사 전문이 아닙니다.
- **로컬 캐시:** `.cache/article-index.sqlite3`. Python 표준 SQLite로 언제든 재생성합니다. Git에 넣지 않고 클라우드 서비스·키·계정·유료 도구도 필요 없습니다. 후보 판정과 검사는 항상 JSON을 직접 읽으므로 오래된 캐시로 게시를 허용하지 않습니다.
- **`entry_id`:** 날짜/분야/기사 번호로 브리핑 내 게재 위치를 가리킵니다. 발행 후 번호는 유지하고 추가 항목은 뒤에 붙입니다. 번호 변경은 새 위치이므로 재검토가 필요합니다.
- **`article_id`:** 대표 URL을 보수적으로 정규화한 해시입니다. 호스트 대소문자·기본 포트·추적 인자·fragment를 정리합니다. `www`, HTTP/HTTPS, 경로 대소문자·끝 슬래시, 의미 있는 query 및 반복 query 순서는 유지합니다. 리다이렉트/다른 URL이 같은 기사를 가리키는지는 자동 확정하지 않습니다.
- **`revision_id`:** 우리 제목+자체 요약의 편집 버전 해시입니다. 언론사의 원문 수정 시각이나 실질적 새 사건을 뜻하지 않습니다. 단순 문장 수정은 후속 뉴스가 아닙니다.
- **`event`:** 편집자가 확인한 사건의 key·entities(주체)·date(알려진 사건일 또는 null)·action(행위)·core_facts(핵심 사실). 같은 발표의 다른 매체 보도는 동일한 사건 key를 씁니다. 제품명만 같은 새 버전/새 발표는 다른 사건일 수 있습니다.
- **시간:** `briefing_date`는 KST 브리핑 날짜일 뿐입니다. `publication_note`, `publisher_update_note`, `event_date_note`는 본문에 실제 적힌 설명을 옮깁니다. 날짜만 있거나 미확인이면 시각·시간대를 만들어 넣지 않습니다.
- **추적·검증:** 파일 해시와 기사 구간 해시로 원본 변경/누락을 검사합니다. `review.basis_sha256`는 현재 기사·사건 메타·모든 중복 후보에 묶인 승인입니다. 하나라도 바뀌면 다시 검토해야 합니다.

2026-11-06까지의 23일·236항목은 `origin: legacy`, `decision: legacy-unreviewed`입니다. 이는 별도 색인이지, 오래된 기사 사실·시각·중복을 새로 검증하거나 과거 판을 정정했다는 뜻이 아닙니다. 10/6의 묶음 기사 4-1/4-2도 별도 항목으로 포함했습니다. 과거 원문은 보존합니다.

## 매일 뉴스 게시 순서 (주말 포함)

1. 작업 시작 때 `git pull --rebase`로 최신 원격을 받습니다. 남의 미커밋 변경이 있으면 별도 worktree를 사용합니다. 같은 날짜가 이미 있으면 임의 덮어쓰지 않습니다.
2. 조사 전에 `python3 scripts/article-index.py search "회사 또는 제품"`로 지난 게재를 찾아 원문과 비교합니다. `docs/news-reviews/YYYY-MM-DD.md`에는 채택하지 않은 후보·이유·검색 공백도 남깁니다. 이 스크립트는 외부 뉴스를 수집하지 않습니다.
3. 새 뉴스 Markdown을 작성한 다음 색인을 만듭니다.

   ```sh
   python3 scripts/article-index.py prepare YYYY-MM-DD
   ```

4. 해당 JSON에서 **event 필드만** 검증한 사실로 채웁니다. key는 같은 사건에 재사용할 사람이 읽을 수 있는 이름(예: `example-product-v2-release-2026-11-07`)을 사용합니다. entities/action/core_facts는 필수이며 date는 불명확하면 null입니다. 자동 추출 필드(title/summary/URL/hash 등)는 직접 수정하지 말고 원본 수정 후 `prepare YYYY-MM-DD --refresh`로 갱신합니다. 새 요약에 전문 복제·비공개 메모·개인정보·비밀 URL을 넣지 않습니다.
5. 후보를 읽고 URL뿐 아니라 주체·제품·발표·핵심 사실을 원출처와 비교합니다. 같은 날 다른 분야의 앞선 항목도 대조합니다.

   ```sh
   python3 scripts/article-index.py candidates YYYY-MM-DD
   ```

6. 항목마다 검토 판정을 기록합니다. 후보가 없으면 `new`, 후보와 사실상 다른 사건이면 `distinct`, 검증된 실질적 후속 변화가 있으면 `update`입니다. 후보가 있는 경우 **각 candidate entry_id를 `--match`로 모두 명시**합니다. 중복이면 본문에서 채택을 취소하고 검토 기록에 제외 사유를 남깁니다. 형식 예시이며 내용은 실제 근거로 바꿉니다.

   ```sh
   python3 scripts/article-index.py review YYYY-MM-DD YYYY-MM-DD/IT/1 \
     --decision new --reason "확인한 출처와 과거 게재를 비교한 구체적 판정 근거"

   python3 scripts/article-index.py review YYYY-MM-DD YYYY-MM-DD/IT/2 \
     --decision update --match 이전날짜/IT/1 \
     --reason "이전 발표와 오늘 보도의 차이를 원문에서 확인" \
     --material-change "새로 제공되는 지역·기능·출시 상태 등 실제 달라진 사실"
   ```

   같은 URL은 `distinct`로 우회하지 못하며, 이전과 같은 자체 요약은 설명만 붙인 `update`로도 통과하지 못합니다. 제목/표현의 변화만으로 새 사실이 증명되지는 않습니다. 판정 명령은 편집자의 결정을 기록할 뿐 사실을 자동 검증하지 않습니다.
7. **뉴스 자체의 게시 직전에** 다음을 실행하고 성공한 날짜별 JSON을 뉴스와 같은 커밋에 넣습니다. 발표·GitHub가 없거나 아직 준비되지 않았어도 생략하지 않습니다.

   ```sh
   python3 scripts/article-index.py check
   python3 scripts/article-index.py gate YYYY-MM-DD
   python3 scripts/test-article-index.py
   ```

8. 커밋 전 최신 원격을 다시 확인합니다. 작업 변경을 보존한 상태에서 원격 변경을 안전하게 반영하고 `check`와 `gate`를 재실행한 뒤 일반 push를 합니다. 충돌이면 중단·보고하며 force push하지 않습니다. 실제 해당 커밋의 Pages 성공·게시된 본문을 확인한 뒤 완료를 알립니다.

이 도구가 git push 자체를 가로채지는 않습니다. 위 독립 gate가 뉴스 작성 자동화의 필수 게시 단계입니다. 추가 방어로 `build-daily.py`도 **새 발표의 생성 직전과 오디오 생성 후** gate 및 색인 해시를 확인합니다. 기존 `--check`, 이미 발행된 발표 검사, `--plan` 미리보기는 기존 방식으로 유지합니다. 정규 뉴스 수집 마감, 매일 08:01 KST 뉴스 일정, 주간·GitHub 일정도 바꾸지 않습니다.

## 갱신·검색·복구

```sh
# 뉴스 본문을 정당하게 변경한 뒤 명시적으로 색인 갱신
python3 scripts/article-index.py prepare YYYY-MM-DD --refresh
# 변경되지 않은 항목의 판정은 보존, 바뀐 새 항목은 pending으로 돌아감
python3 scripts/article-index.py check

# JSON 원본 직접 검색
python3 scripts/article-index.py search "삼성"
# 선택 사항: 로컬 SQLite 캐시 재생성
python3 scripts/article-index.py sqlite
```

`prepare`는 기존 JSON을 기본적으로 덮어쓰지 않습니다. 쓰기 명령은 날짜별 로컬 잠금과 원본 재확인, 완성된 임시 파일의 원자적 교체를 사용합니다. 직접 JSON을 편집하는 동안 같은 날짜의 명령을 동시에 실행하지 않습니다. 원문 수정과 색인 갱신은 그 작업의 권한 범위 안에서만 합니다. 리서치 링크 추가처럼 과거 본문이 정당하게 바뀌었으면 해당 날짜를 `--refresh`하고 검사합니다. 이 도구가 기존 발표 source hash를 고쳐 주지는 않습니다. 기존 발표가 변경을 감지하면 원래의 중단·검토 절차를 따릅니다.

최초 과거 색인은 `bootstrap --through 2026-11-06`으로 만들었으며 재실행은 거부합니다. config의 `legacy_through`를 늘려 새 기사를 검토 예외로 만들지 않습니다. JSON이 삭제/손상되면 Git에서 정상본을 확인해 복구하고 검사합니다. 뉴스 날짜 누락·빈 색인·잘못된 schema·중복 ID·번호 없는 기사·원본 불일치는 오류로 중단합니다.

## 검사 범위와 한계

- 정확 URL/같은 자체 요약은 강한 중복 신호입니다. 동일 사건 key, 명시된 핵심 사실/주체·행위·사건일, 유사 제목은 **검토 후보**만 만듭니다. 다른 언어·다른 표현·다른 URL의 같은 사건을 모두 찾아내지 못합니다. 첫 과거 색인에는 사건 메타를 추정해 넣지 않았으므로 검색과 편집자의 비교가 필수입니다.
- `check`는 색인·원본 일치 검사이며 새 뉴스의 검토 승인은 아닙니다. `gate DATE` 성공도 외부 원문 사실·시각·저작권 또는 Pages 배포 완료를 증명하지 않습니다.
- 이 색인은 뉴스만 다룹니다. 반복 등장 자체가 의미 있는 GitHub 트렌드, 주간 종합, 심층 리서치를 새 뉴스 중복으로 자동 제거하지 않습니다.
- 새 예약 실행기·Actions 스케줄·서버·계정·키·영구 접근 권한을 만들지 않습니다. 표준 Python만으로 실행됩니다.
