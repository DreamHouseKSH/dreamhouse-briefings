# 클라우드 Sohee 발표 생성

새 하루 발표는 공개 아카이브의 기존 대본을 공식 Qwen3-TTS `Sohee` 화자로 합성한다. Linux 클라우드의 CPU(Central Processing Unit, 중앙처리장치)에서 실행하며 Mac·MLX·유료 음성 서비스·새 계정이나 키는 필요 없다. 모델은 실행 호스트에 내려받고 대본을 외부 합성 서비스로 보내지 않는다. 모델·가상환경·임시 파형은 공개 저장소에 넣지 않는다.

**이 문서는 실행 경로와 발행 절차다. 새 예약 실행기나 Actions 스케줄이 설치된 것은 아니다.** 매일 발행하려면 기존 뉴스·GitHub 루틴이 실행 가능한 승인된 클라우드 호스트에서 아래 명령을 호출해야 한다. GitHub Pages는 검증된 콘텐츠와 MP3를 받아 정적 빌드·배포만 수행한다.

## 고정 모델과 환경

- 공식 모델: [`Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice), revision `0c0e3051f131929182e2c023b9537f8b1c68adfe`.
- 공식 실행 코드: [`QwenLM/Qwen3-TTS`](https://github.com/QwenLM/Qwen3-TTS), `qwen-tts==0.1.1`. 모델 카드와 코드 저장소의 라이선스 표시는 Apache-2.0이다.
- 검증 환경: Linux x86_64, Python 3.12.14, PyTorch `2.15.0+cpu`, Transformers `4.57.3`, Accelerate `1.12.0`, torchaudio `2.11.1+cpu`.
- 합성 설정: Korean / Sohee, BF16(bfloat16, Brain Floating Point 16 — 16비트 부동소수점 계산), SDPA(Scaled Dot Product Attention, 내적 기반 주의 계산), CPU 스레드 4개. 감정 지시: `차분하고 따뜻한 목소리로 자연스럽게 말해주세요.`
- 공식 모델·음성 토크나이저 파일은 약 4.52 GB다. 9.7 GiB 메모리 호스트에서 짧은 샘플의 최대 프로세스 메모리는 약 4.76 GiB였다. 실행 전 여유 메모리·디스크를 확인하고 모델·의존성·대본별 파형을 모두 수용할 공간을 확보한다.
- 짧은 3.44초 샘플의 합성은 12.90초였다. CPU에서는 재생 시간보다 오래 걸릴 수 있으므로 미리 생성하는 브리핑용 경로이며 실시간 음성 응답을 보장하지 않는다. 전체 대본의 실제 시간은 해당 실행 로그로 확인한다.

공식 모델은 기존 Mac의 MLX 변환판과 실행 코드·정밀도가 다르다. 같은 `Sohee`라는 이름만으로 파형 일치나 동일한 자연스러움을 보증하지 않는다. 자동 전사는 내용 확인을 보조할 뿐 사람의 청취 평가를 대신하지 않는다.

## 격리 환경 준비

이미 검증된 환경이 있으면 재사용한다. 새 환경은 저장소 **밖**에 만들며 시스템 Python을 변경하지 않는다. `ffmpeg`와 `ffprobe`가 기존 호스트에 있어야 한다. 없으면 차단 상태를 보고하고 임의 시스템 권한 변경이나 유료 서비스를 추가하지 않는다.

```sh
python3.12 -m venv ../briefing-tts-venv
. ../briefing-tts-venv/bin/activate
python -m pip install torch==2.15.0+cpu torchaudio==2.11.1+cpu \
  --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r scripts/requirements-sohee.txt
python -m pip check
command -v ffmpeg
command -v ffprobe
export ORT_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_TELEMETRY=1 DO_NOT_TRACK=1
export HF_HOME="$(pwd)/../briefing-model-cache"
```

`scripts/requirements-sohee.txt`는 실제 검증 환경의 전체 의존성 버전을 고정한다. 위 순서대로 CPU 전용 PyTorch를 먼저 설치한다.

모델 경로를 생략하면 생성기가 공식 저장소의 고정 revision만 내려받는다. 이미 검증한 로컬 모델을 재사용할 때만 `--model-dir /absolute/path/to/pinned-model`을 지정한다. 로컬 경로에서도 가중치·설정·토크나이저의 고정 SHA-256을 검사하며 맞지 않으면 중단한다. 임의 커뮤니티 변환판이나 다른 버전으로 조용히 바꾸지 않는다. 인증을 요구하거나 다운로드가 차단되면 중단·보고한다. 의존성 변경도 기존 환경에서 섞어 설치하지 말고 별도 검증한다.

## 매일 새 날짜 생성

날짜는 한국시간 기준이다. 뉴스·GitHub가 모두 준비된 뒤 같은 가상환경에서 실행한다.

```sh
DATE=YYYY-MM-DD
python scripts/build-daily.py "$DATE" --audio --audio-backend sohee --if-ready \
  --work-dir "../briefing-audio-work/$DATE"
python scripts/build-daily.py "$DATE" --check
python scripts/test-daily.py
python scripts/test-sohee.py
node scripts/test-daily-audio.cjs
```

`--if-ready`는 뉴스·GitHub 중 한쪽이 없을 때만 PENDING으로 끝난다. 잘못된 본문이나 검증 실패를 성공으로 바꾸지 않는다. 기존 완성 판은 검사만 하며 자동으로 다시 합성하거나 덮어쓰지 않는다. Yuna가 명시적으로 필요한 보존 작업만 `--audio-backend yuna`를 사용하고, 이는 macOS 경로다. Linux 실패 시 Yuna나 다른 음성으로 임의 대체하지 않는다.

공개 대본은 그대로 보존하고, `2026-109618` 같은 긴 하이픈 식별번호는 합성 입력에서 정확한 숫자값을 한국어로 읽고 일부 기술 이름은 한국어 발음으로 적는다. 숫자값은 바꾸지 않으며 별도 합성입력 해시를 기록한다.

생성기는 대본의 각 단계(cue)를 따로 합성하고 실제 파형 샘플 수로 경계를 계산한다. 단계 사이 0.20초 여백을 포함해 원시 파형을 먼저 이어 붙인 뒤 MP3를 한 번 인코딩하므로 단계별 MP3 인코딩 지연이 누적되지 않는다. 유한값·음량·길이·토큰 상한을 점검하고 실패 구간은 제한된 재시도 후 중단한다. `--work-dir`의 구간 캐시는 대본·모델·설정에 연결된 키와 오디오 체크섬으로 검사한다. 임시 파일을 공개 저장소에 넣지 않는다.

## 기존 판의 승인된 음성 교체

10/27~29의 기존 Yuna 오디오는 보존한다. 10/30 등 이미 있는 판을 바꾸는 것은 새 날짜 생성과 다르며, 승인된 대상 날짜만 별도 경로에 생성한다. 기존 오디오와 메타데이터는 새 결과 검증이 끝날 때까지 그대로 둔다.

```sh
DATE=2026-10-30
KEY=20261030
STAGE="../briefing-sohee-stage/$DATE"
mkdir -p "$STAGE"
python scripts/build-daily-sohee.py "$DATE" \
  --data "_data/day_${KEY}.json" \
  --audio "$STAGE/narration.mp3" --metadata "$STAGE/audio.json" \
  --work-dir "../briefing-audio-work/$DATE"
```

단독 생성기도 이미 있는 출력 경로는 거절한다. 재실행 전에 실패 원인을 확인하고 검증되지 않은 산출물만 검토하여 처리한다. 완성된 기존 판을 삭제해 재실행하지 않는다. 검증 후에만 `assets/audio/DATE-narration.mp3`와 `_data/day_KEY_audio.json`을 한 게시 변경으로 함께 반영한다. 대본·원문·출처 링크를 음성 교체 과정에서 수정하지 않는다.

## 재사용 가능한 오디오 검증 명령

`check-sohee-audio.py`는 합성이나 파일 교체 없이 검증한다. 기본 실행에는 표준 Python과 기존 `ffmpeg`·`ffprobe`만 필요하다. 새 Sohee 파일뿐 아니라 기존 Yuna 파일도 검사할 수 있다.

```sh
python scripts/check-sohee-audio.py \
  --data "_data/day_${KEY}.json" \
  --audio "$STAGE/narration.mp3" --metadata "$STAGE/audio.json" \
  --report "$STAGE/audio-validation.json"
```

검사 항목은 공개 대본·오디오 SHA-256, 모든 cue 순서·연속성·마지막 경계, 실제 디코딩 표본 수·표본화율, 각 구간의 유한값·0이 아닌 음성·음량·클리핑이다. 게시본은 `--audio assets/audio/DATE-narration.mp3 --metadata _data/day_KEY_audio.json`으로 검사한다. 파형 검사만으로 발음·누락·자연스러움이 검증되는 것은 아니다.

이미 준비된 **로컬** Whisper 모델이 있을 때만 같은 명령에 `--asr-model /absolute/path/to/verified-whisper-model`을 추가한다. ASR(Automatic Speech Recognition, 음성을 글자로 바꾸는 자동 음성 인식)은 Sohee 환경의 PyTorch·Transformers·SciPy 등을 사용하며 모델을 자동 다운로드하거나 음성을 외부 전송하지 않는다. 각 cue의 원문·전사·문장 유사도와 검토 필요 여부를 보고서에 남긴다. 문장 부호·띄어쓰기·영문 대소문자는 비교에서 제외한다.

종료값은 `0` 요청한 검사 통과, `1` 구조·파형·실행 오류, `2` 자동 전사 검토 필요다. 유사도 0.75 미만이나 전사 상한 의심은 검토 대상으로 표시한다. 낮은 점수가 합성 오류의 증거인 것은 아니며 고유명사·숫자·전사기 오류를 사람이 대조해야 한다. 30초를 넘는 cue는 Whisper 입력 잘림을 피하기 위해 자동 전사를 생략하고 검토 대상으로 남긴다. 높은 유사도도 특정 숫자·단어 누락을 배제하지 않으므로 중요 표현은 별도로 확인한다. 자동 전사 결과를 사람의 청취나 자연스러움 평가로 보고하지 않는다.

## 검증과 게시 완료 기준

1. 원문 입력 해시·공개 대본 해시가 변하지 않았는지 확인한다. 모든 장·단계의 cue가 순서대로 한 번씩 있고 0초부터 마지막 샘플까지 연속이며 겹침·누락이 없어야 한다.
2. 완성 MP3를 다시 디코딩하여 실제 샘플 수·길이·표본화율이 cue와 일치하는지 확인한다. 각 구간이 무음·잘림·반복 폭주·클리핑 상태가 아닌지 검사한다.
3. 가능한 범위에서 독립 한국어 자동 전사로 문장·숫자·이름을 대조하고 차이는 검토한다. 전사기 오류와 합성 오류를 구분하며 낮은 일치율을 무조건 통과 처리하지 않는다. 사람이 듣지 않았다면 청취 검증을 했다고 쓰지 않는다.
4. Python·Node 검사와 브라우저의 시작/일시정지/재개·장 이동·마지막 종료·집중 보기·배경 전환을 확인한다. 모의 이벤트, 실제 브라우저 재생, 실제 iPad/iPhone 기기 검증을 구분한다.
5. 커밋 직전 원격 상태를 다시 읽는다. 원격이 작업 시작 이후 바뀌었거나 같은 날짜를 다른 작성자가 수정했으면 게시를 멈추고 재검토한다. 다른 변경을 덮어쓰거나 force-push하지 않는다.
6. 오디오 URL은 메타데이터의 콘텐츠 SHA-256을 쿼리 문자열에 붙여 이전 음성과 새 cue가 캐시에서 섞이지 않게 한다. 해시를 붙인 실제 URL도 검증한다. 기대한 커밋이 원격 `main`에 있는지, **그 커밋**의 Pages 빌드·배포가 성공했는지 확인한다. 실제 날짜 페이지와 오디오 URL의 응답·본문·콘텐츠 유형·크기·체크섬을 확인한 뒤에만 완료로 보고한다. 생성 성공·문서 갱신만으로 게시나 예약 자동화 완료를 주장하지 않는다.

### 의존성 진단 전송 비활성화

생성기는 ML 의존성을 가져오기 전에 `ORT_DISABLE_TELEMETRY=1`을 설정한다. [ONNX Runtime 공식 개인정보 문서](https://github.com/microsoft/onnxruntime/blob/main/docs/Privacy.md)에 따르면 초기화 전 이 설정은 프로세스 전체에서 업로더·이벤트·영구 기기 식별자 생성을 막는다. Hugging Face 진단 전송도 비활성화한다. 이미 모델을 받은 검증 실행에는 `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`을 함께 사용한다. 진단 전송이나 권한 차단이 발생하면 우회하지 말고 정확한 상태를 보고한다.
