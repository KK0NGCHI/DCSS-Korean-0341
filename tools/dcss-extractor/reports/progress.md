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
