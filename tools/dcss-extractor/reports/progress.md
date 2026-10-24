# DCSS 0.34.1 한국어화 현황

**기준일:** 2026-10-24 · **공식 작업 브랜치:** `main` · **대상 버전:** DCSS 0.34.1

> 여기서 '설명 데이터 키 대응 100%'는 게임 전체 번역률, 번역 품질, 실제 출력 검증률이 아닙니다.

## 확인된 결과

| 항목 | 기준 커밋 / 검사 | 관측된 결과 |
|---|---|---|
| 설명 파일 쌍 | [설명 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40072181157) | EN 23개 / KO 23개 |
| 설명 원문 고유 키 | 동일 | 3,778개, 한국어 대응 3,778개, 누락 0개 |
| 원문에 없는 한국어 키 | 동일 | 260개, 삭제하지 않고 검토 |
| 참조/Lua 검사 후보 | 동일 | 참조 5건 / Lua 4건 / 원문 중복 키 3건 (이후 수정 전 측정) |
| 전체 읽기·추출 | [전체 조사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40072181172) | 텍스트 소스 1,341개 / 추출 레코드 61,032개 / 읽기 오류 0 |
| 화면 출력·동적 후보 | 동일 | 3,753개 + 2,286개; 이들은 미번역 확정 수가 아님 |
| Linux 콘솔 C++ 빌드 | [빌드 성공](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40072181195) | 공식 0.34.1 릴리스에 번역 C++ 10개를 덮어써 전체 컴파일·링크 성공 |
| Windows 타일 빌드·한국어 UI 출력 | 미검사 | 실제 실행 및 한글 폰트, 동적 조사, 저장/불러오기 미확인 |

전체 조사 상세 분류: `internal_candidate=8448`, `review_unknown=41242`, `comment_candidate=1501`, `review_dynamic=2286`, `visible_candidate=3753`, `test_marker=21`, `review_translation_present=3781`.

`test_marker=21`은 전 소스의 어휘적 검사 결과이며, `message.cc`, `invent.cc`, `describe.cc`의 과거 강제 표시 코드가 남아 있다는 뜻이 아닙니다. 별도 smoke guard는 이 세 파일의 마커 부재를 검사해 통과했습니다.

## 작업 단계

| 단계 | 상태 | 완료 조건 |
|---|---|---|
| 00 원본 파일 기준 | 완료(외부 근거) | 로컬 26,187개 파일의 manifest 보고, 원본 해시·manifest 미등록 |
| 01 추출 파일럿 | 진행 중 | 샘플 파일의 렉시컬/AST 누락·오탐 검토 |
| 02 C++ 전체 조사 | 진행 중 | 실출력 콜사이트와 중복 번역 단위 확정 |
| 03 Lua·데이터 조사 | 진행 중 | 23개 설명쌍 및 기타 게임 데이터 전체 검증 |
| 04 분류 | 진행 중 | 화면 출력/내부/동적/미확인 분류 정밀 검증 |
| 05 0.24 구번역 대응 | 미착수 | 재현 가능한 매핑·충돌 리포트 |
| 06 검수 가능한 번역 카탈로그 | 진행 중 | 키·문맥·포맷·용어별 검수·검증 상태 |
| 07 통합 및 런타임 | 진행 중 | Linux 콘솔 C++ 빌드 통과, Windows 타일/게임 출력 검증 필요 |

## 2026-10-24 후속 작업

- PR #1의 87개 커밋을 `main`에 병합 (병합 커밋 `c59c4dd`).
- `fix/ko-qa-progress-20261024`에서 `ability.txt`, `features.txt`, `monsters.txt`, `tutorial.txt`의 한국어 설명 항목 8개 교정. [후속 설명 감사 CI](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40073426356) 통과: 참조 차이 5→1, Lua 구분자 차이 4→0, 고유 키 대응 3,778/3,778 유지. 남은 참조 경고는 `HINT_SEEN_BRANCH`.
- `HINT_SEEN_BRANCH`의 원문/번역 태그 개수 차이는 원문 자체의 `<nomouse` 표기 문제를 동반하므로 로더 동작 확인 전까지 임의로 삭제하지 않음.
- 영어 중복 3개 키(`CMD_EXPLORE_NO_REST`, `damage-immune at range monstatus`, `+LOS mutation`)는 게임 로더의 중복 키 처리 순서를 확인하기 전 삭제하지 않음.
- 한국어 추가 키 260개는 기존 버전의 번역 자산일 수 있어 참조 여부 조사 전 일괄 삭제 금지.

## 다음 작업의 우선순위

1. 설명 감사 경고의 재측정과 실오류 확인. 차이가 의도적인 태그·원본 중복·과거 데이터인지 문맥별로 분류.
2. `full_inventory_v1.py`의 후보를 **실제 화면 출력 호출부**로 좁혀 미번역/이미 번역/내부용을 분리하고 파일별 통계를 남김.
3. 전투·상태·메뉴·신앙·소환 등 P0/P1 실출력 미번역을 일괄 교정. 동적 한국어 조사는 공통 처리 방식을 별도로 설계.
4. 공식 Windows 타일 게임에 C++ 및 설명 데이터를 함께 통합해 `language = ko` 실행·UI 렌더링·문자열 조합을 검증.
5. 재현 가능한 릴리스 제작, 설치 가이드, README, 번역 범위 고지.

**기록 규칙:** C++ 후보 개수와 완성 번역 개수를 혼동하지 않는다. 0.24 자산의 재사용 가능성을 분석하되 현재 0.34.1의 사용 가능 키만 검증한다. 문서에 각 수치의 CI 링크 및 대상 커밋을 함께 기록한다.

## 2026-10-24 출력 후보 분류 자동화

- [실행 성공](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40073769987): 가시 출력 3,753 + 동적 2,286 = 6,039개 레코드를 5,450개 고유 리터럴 검토 그룹으로 정리.
- P0 그룹 646개 중 영문/식별자 후보 642개, P1 635개, P2 4,169개. **미번역 확정·번역률 수치가 아님.**
- 결과물: `triage/review_queue.csv`, `triage/p0_english_review.csv`, `triage/triage_summary.json` (GitHub Actions 아티팩트).
- 상세 기준: [TRIAGE-001](../../docs/translation-review/visible-candidate-triage-20261024.md).
- 다음: P0 642개에 대한 콜사이트 검증 및 실제 미번역 확인 후 일괄 번역.

## 2026-10-24 P0 출력 호출부 감사 및 첫 한국어화 묶음

- [최초 P0 호출부 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40074747440) 통과: 11개 C++ 파일, 직접 문자열 호출 959곳, 한글 포함 729, 영어 출력 검토 후보 202, 오류용 후보 3, 서식/기호 25.
- 후속 광선 메시지 21종 번역 전의 최초 수치. 최신 최종 커밋 기준 검사를 별도로 확인한다.
- 실제 소스 변경: 59종 원문 패턴(62개 발생 위치) 한국어화, `newgame.cc` 잔여 `[KO TEST]` 2곳 제거.
- `mon-util.cc`를 Linux 콘솔 빌드 오버레이에 추가. C++ 빌드와 실제 타일 게임 출력은 별도 검증.
- 자세한 내용: [P0 직접 호출부 보고서](../../docs/translation-review/p0-direct-callsites-20261024.md).

## 2026-10-24 P0 번역 후속 + 게임 대사 DB 1차 감사 (병합 완료)

- PR #4 [P0 C++ 직접 메시지 번역 및 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/4) 병합: `522d00b`.
- 최종 [P0 출력 호출부 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076532595): 11개 파일, 문자열이 포함된 직접 호출부 959곳, 한글 포함 885곳, 영문·식별자 검토 후보 46곳(초기 202곳), 개발자 오류 후보 3곳, 포맷·기호 중심 25곳. 후보 수 감소는 전체 한국어화율이 아님.
- 최신 [Linux 콘솔 컴파일](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076532601) 성공, 번역 C++ 오버레이 11개 파일. [스모크 마커 검사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076532612) 통과. Windows 타일 및 한국어 DB 로딩은 아직 미검증.
- PR #5 [신의 칭호 KO 오버레이 + 게임 대사 DB 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/5) 병합: `5d766a3`.
- [게임 대사 DB 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076997160): 최상위 텍스트 23개/원문 고유 키 2,019개, 한국어 오버레이 1개(`godname.txt` 키 23개/23개), 칭호 본문 50개. 기존 원본의 한글 본문 301줄, 라틴 전용 본문 13,245줄. 마커와 고유명칭이 포함되므로 미번역률을 뜻하지 않음.
- DB 상세: [database-audit-20261024.md](../../docs/translation-review/database-audit-20261024.md).

**다음 작업:** 남은 P0 직접 출력 후보 46곳의 문맥 검수, 동적 조사 결합, `monspeak.txt` 730개 키, `monspell.txt` 260개 키, `wpnnoise.txt` 65개 키 등 데이터 대사 한국어화. 기존 원본에 삽입된 한국어는 보존하고 KO 오버레이로 누락분을 병합. Windows Tiles 및 `language = ko` 출력은 별도 실행 검증.

## 2026-10-24 몬스터 주문 대사 대량 번역 — 병합 완료

- [PR #6](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/6): `source/dat/database/ko/monspell.txt` 154개 키 한국어 오버레이와 변형/토큰/가중치 자동 감사 추가.
- [PR #7](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/7): 실제 게임 로더가 `%%%%%`도 구분자로 인정한다는 점을 반영하여 감사 도구의 키 집계 오류 수정, 누락 대사 2개 추가.
- [최종 검증](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40081571286): 원문 키 **262개**, 한국어 **156개**, 잔여 **106개**, 원문과 불일치·중복·빈 본문·필수 마커/가중치 오류 **0건**.
- 별도 게임 대사 DB 전체 조사: 원본 23개 파일에 고유 키 합계 **2,022개**, 한국어 오버레이 2개 파일, 오버레이 대응 키 합계 **179개**. 원본에 이미 한국어인 경우는 별도 집계.
- 위 156/262(약 59.5%)는 **monspell.txt의 키 대응률**일 뿐, 실제 번역 품질·전체 게임 한국어화율·Windows Tiles 출력 검증률이 아님.
- 상세 작업 및 후속 과제: [몬스터 주문 대사 검증 보고서](../../docs/translation-review/monspell-audit-20261024.md).

## 2026-10-24 최신 몬스터 대사 한국어화 (PR #8 · #9 병합)

**이 단락의 최신 CI 집계가 상단의 과거 스냅샷보다 우선합니다.**

- [PR #8](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/8): `monspell.txt`에 추가 89개 대사 키를 번역해 **245/262개** 대응. 나머지 **12개 키 참조 + 5개 `__NONE`**으로, 독립적인 영문 대사 본문이 남은 키는 **0개**. [CI](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40082885965) 통과.
- [PR #9](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/9): `monspeak.txt`에 **65개 키** 한국어 대사 오버레이 작성. 원문 **731개 고유 키(732개 항목, 중복 1건)** 대비 잔여 666개. 동작·전투·혼란·침묵·도주·사제·경비병·임프·플레이어 유령의 대사를 포함. [CI](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40084216618) 통과.
- 게임 대사 DB 23개 원문 파일의 총 고유 키 합계 **2,022개**. 별도 한국어 오버레이 3개 파일, 원문과 대응하는 키 합계 **333개**(신 칭호 23 + 주문 대사 245 + 일반 대사 65). 원본 자체에 포함된 한국어는 별개이며 **전체 번역률은 아님**.
- 전용 몬스터 대사 정적 검사(`audit_monspeak_ko.py`)는 필수 치환 변수·`VISUAL:`/`SOUND:`·`w:` 가중치·랜덤 대사 선택·변형 문장 수를 확인한다. 최신 구조 검사 오류 **0건**.
- 남은 주요 번역 대상: `monspeak.txt` 추가 일반/고유 대사, `wpnnoise.txt` 무기 소음, `godspeak.txt` 영어 잔존, Lua와 동적 조사 등. Windows Tiles 실제 렌더링은 미검증.
- 최신 자세한 기록: [monspell 완료 현황](../../docs/translation-review/monspell-audit-20261024.md).

## 2026-10-24 몬스터 대사 127개 키 대량 번역 완료

- [PR #11](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/11) 병합: `59ee951` — `monspeak.txt`에 한국어 대응 키 **127개**, 새 대사 변형 **379개**를 추가.
- `monspeak.txt` 고유 원문 키 **731개** 중 한국어 대응 **216개** (이전 89개), 미대응 **515개**. 원문의 `_laughs_` 중복 키 **1건**은 그대로 보존하고, 번역 오버레이는 첫 번째 정의 기준 6개 웃음 표현으로 구성.
- `godname.txt` 23개, `monspell.txt` 245개, `monspeak.txt` 216개를 합산한 별도 KO 오버레이 원문 키 대응 합계 **484개**. 이 합계는 전체 게임 번역률로 사용하지 않는다.
- [최종 GitHub Actions 데이터베이스 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40088380643) 성공: 누락 필수 치환 토큰, 무작위 표현 수, 지시 접두부, `w:` 가중치, 번역 키 중복 등 구조 오류 **0건**. 검사기와 회귀 테스트도 통과.
- 세부 보고서: [몬스터 대사 번역 배치](../../docs/translation-review/monspeak-batch-20261024.md). 실제 Tiles 로그 표시, 이름 뒤 조사, Lua 대사 및 시각 표현은 추가 검증 필요.
- 다음 검토 대상: 나머지 `monspeak.txt`의 515개 키(참조 별칭·빈 출력 혼합), `wpnnoise.txt`의 무기 소음, `godspeak.txt` 내 기존 한글·영어 혼합.

## 2026-10-24 몬스터·무기 대사 추가 대량 번역

- [PR #12](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/12) 병합: `23cd0ca`. `monspeak.txt` **44개 키·150개 문장 변형** 추가, `wpnnoise.txt` **신규 한국어 파일 18개 키·192개 문장/효과음 변형** 추가. 총 **62개 키·342개 변형**.
- `monspeak.txt`: 원문 고유 키 731개 중 한국어 대응 260개(35.6%), 미대응 471개. 원문 중복 `_laughs_` 1건은 그대로 유지.
- `wpnnoise.txt`: 원문 고유 키 65개 중 한국어 대응 18개(27.7%), 미대응 47개. 노래하는 검과 특수 유물, 자아가 있는 무기의 소리·대사를 번역.
- 별도 한국어 DB 파일 합계 4개(`godname` 23, `monspell` 245, `monspeak` 260, `wpnnoise` 18): 대응 원문 키 **546개**.
- [Korean gameplay database audit — 성공](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40090108540): 모든 번역 키/가중치/`@...@` 마커/`[선택지|...]`/`VISUAL:`·`SOUND:` 검사 통과. 무기 대사 전용 검사와 회귀 테스트를 추가.
- 상세: [몬스터·무기 음성 배치 검증 문서](../../docs/translation-review/monspeak-wpnnoise-batch-20261024.md).
- 이 수치는 **파일별 키 대응률**이지 전체 게임 한국어화율이 아니다. Windows Tiles 실사용, Lua 동적 문구, 조사 결합, 음성 문장 자연스러움은 별도 테스트가 필요하다.

## 2026-10-24 실제 한국어 데이터 로더 런타임 검증 — 성공

- [PR #13](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/13) 병합. [실행 결과](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40095478475): Linux 콘솔에서 실제 게임 실행 파일 빌드, `language=ko -builddb -reset-cache` 실행 및 캐시 검사가 모두 성공.
- 공식 0.34.1 원본 아카이브의 SHA-256 확인 후 번역 C++ 파일 **11개**와 저장소의 **게임 대사 DB/설명 데이터 전체**를 합쳐 컴파일.
- 게임 실행 파일이 생성한 `descriptions.ko.db`, `speak.ko.db`, `misc.ko.db`에서 한국어 UTF-8 본문 **3종**을 직접 확인. 검사값은 `대상에게 독침을 내뱉는다.`, `바람이 거세게 부는 소리가 들린다.`, `율법을 세우는 진`임.
- **검증 범위의 한계:** 이 테스트는 한국어 데이터베이스를 실제 런타임에서 생성할 수 있음을 입증함. Windows Tiles 빌드, 게임 내 UI·전투 출력, 실제 글꼴 표시, 조사·변수 결합, 세이브 로드 정상성은 **여전히 미검증**.
- 재검사 자동화: `.github/workflows/korean-runtime-smoke.yml`. GitHub Actions에서 수동 실행 또는 해당 소스·데이터 변경 PR로 다시 검사 가능.

## 2026-10-24 고유 몬스터 대사 82개 키 추가 — PR #14

- 번역 파일: `source/dat/database/ko/monspeak.txt`. [PR #14](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/14)에서 **82개 원문 대응 키**(27+31+24)를 추가해 **260/731 → 342/731(46.8%)**, 미대응 **471 → 389개**.
- 이번 배치에는 원문/한국어 변형 및 참조 **418줄**이 대응하며, 그중 **361줄**에 한글 본문이 포함됨. 원문 참조만 하는 별칭 등도 집계하므로 418을 고유 번역 문장 수로 취급하지 않음.
- Edmund, Erica, Erolcha, Eustachio, Frances, Frederick, Fannar, Gastronok, Grinder, Harold, Ignacio, Ilsuiw, Jessica, Natasha, Robin, Nessos, Pargi, Jorgrun, Joseph, Josephina, Josephine, Khufu, Kirke, Lodul, Louise, Maggie, Mara 등 고유 몬스터 대사를 번역.
- [최종 구조 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40097262348) 및 [Linux 한국어 DB 로더 재검증](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40097262320)을 실행. 실행 완료 여부와 성공 판정은 링크에서 확인; Windows Tiles 및 동적 조사 결합은 검사 범위 밖.
- DB 4개 오버레이의 원문 대응 키 합계는 **628개**(godname 23 + monspell 245 + monspeak 342 + wpnnoise 18). **게임 전체 번역률 아님**.
- 상세: [고유 몬스터 대사 번역 배치](../../docs/translation-review/monspeak-unique-batch-20261024.md).

## 2026-10-24 고유 몬스터 대사 추가 번역 — PR #15

- `monspeak.txt` 원문 고유 키 대응 **342/731(46.8%) → 413/731(56.5%)**. 추가 **71개**, 미대응 **318개**.
- 추가된 출력·참조 변형 **350줄** 중 **305줄**이 한국어 포함. 참조만 있는 원문 동일 키 **20개**가 포함되므로 이를 모두 별도 번역 문장으로 셀 수 없음.
- 대상: Pikel, Polyphemus, Prince Ribbit, Parghit, Roxanne, Rupert, Snorg, Sonja, Xtahua, Zenata, Aizul, Agnes, Amaemon, Arachne, Azrael, Bai Suzhen, Dissolution, Murray, Nellie, Nergalle, Nikola, Menkaure, Maurice 등.
- 잔여 318개 1차 분류: 일반·혼합 본문 190, 참조 전용 99, Lua 14, 무출력 15. 분류는 최종 실출력 판정이 아닌 잠정 구조 분류.
- [구조 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40098709326) 성공. [Linux 런타임 DB 재검증](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40098709301)은 별도 확인. 실제 고유 몬스터 출력 및 Windows Tiles와 한글 조사는 여전히 미검증.
- 누적 4개 데이터 오버레이 원문 대응 합계 **699개** = godname 23 + monspell 245 + monspeak 413 + wpnnoise 18. 이는 게임 전체 한국어화율과 무관.
- 상세 기록: [고유 몬스터 대사 71키 추가 보고](../../docs/translation-review/monspeak-named-20261024-batch2.md).

## 2026-10-24 무기 대사 원문 키 100% 대응 · 몬스터 대사 추가 — PR #16

- `wpnnoise.txt` 한국어 원문 키 대응: **18/65 → 65/65(100%)**, **47개 신규 키**. 신규 출력·참조 변형 **541줄**, 그중 **516줄**에 한국어 포함. **5개는 원문 참조 라우팅을 그대로 유지**한 키임.
- `monspeak.txt` 한국어 원문 키 대응: **413/731 → 429/731(58.7%)**, **16개 신규 키**. 신규 출력·참조 변형 **58줄**, 그중 **46줄**에 한국어 포함. 미대응 **302개**.
- 누적 4개 KO DB 오버레이의 원문 고유 키 대응 합계: **762**(godname 23 + monspell 245 + monspeak 429 + wpnnoise 65).
- 주요 번역: 노래하는 검의 일상/전투/비명/노래, 마진보, 종굴드로크 모자·왕관 반응, 균류/장어 손, 다우안·듀베사·조리의 대사.
- [무기·몬스터 대사 구조 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40101207409) 성공. [Linux 한국어 DB 로더 검사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40101207364)의 완료 결과는 링크에서 별도 확인.
- **100%는 `wpnnoise.txt`의 키 대응률**이며 게임 전체 번역률이나 동적 한국어 출력 품질을 보증하지 않음. Lua 변환과 실제 이름·조사 결합, Windows Tiles UI 및 폰트는 게임 내 재검토 필요.
- 상세 보고서: [무기 대사 전수 키 대응 및 남은 검증](../../docs/translation-review/wpnnoise-complete-20261024.md).
