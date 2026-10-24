# P0 화면 출력 함수 직접 조사 및 한국어화 — 2026-10-24

## 조사 원칙

이번 단계는 기존 `FULL-INVENTORY-001`의 **어휘적 후보 642개**를 실제 출력 함수의 호출부로 좁혀 검토하기 위한 후속 분석이다. 두 수치는 측정 기준이 달라 단순 뺄셈으로 진행률을 계산하면 안 된다.

- 대상 파일: `ability.cc`, `beam.cc`, `describe.cc`, `god-abil.cc`, `invent.cc`, `message.cc`, `mon-util.cc`, `newgame.cc`, `player.cc`, `player-equip.cc`, `spl-summoning.cc` (11개).
- 조사 도구: `tools/dcss-extractor/scripts/audit_p0_callsites.py`.
- `mpr`, `mprf`, `simple_god_message`, `simple_monster_message`, `yesno`, `yesnoquit`, `cprintf`의 호출과 직접 문자열을 정적 추출한다.
- 소스에서 주석과 인용 리터럴을 가려 가짜 함수 호출을 제거하며, 원본 줄 번호·호출 함수·문구·포맷 지정자를 CSV에 기록한다.
- 스캐너가 다루지 않는 사용자 정의 래퍼, 간접 호출, 매크로, Lua, C++ raw literal 및 실행 조건은 따로 조사한다.

## 최초 성공한 자동검사

[GitHub Actions: P0 callsite audit](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40074747440)

| 분류 | 개수 |
|---|---:|
| 출력 호출부 내 직접 리터럴 | 959 |
| 한글 포함 | 729 |
| 영문 문자열 검토 후보 | 202 |
| 개발용 오류 가능성 | 3 |
| 포맷/기호 중심 | 25 |

이 숫자는 **첫 번째 수정 묶음 반영 시점**에 측정했다. 이후 `beam.cc`에서 추가 21개 리터럴을 교정했으므로 최신 결과는 마지막 CI에서 재산정한다.

**영문 문자열 검토 후보 202곳은 미번역 확정 202곳이 아니다.** `message.cc`처럼 간접 메시지 내용이 전달되는 곳은 문자열 리터럴만으로 출력 내용을 알 수 없다. 반대로 `printf`의 단독 `%s`는 영어 문장 자체가 아닐 수 있다.

## 이번 실제 소스 번역 작업

- `player-equip.cc`: 무기 장착·해제에 따른 효과 문구 23종(26개 발생 위치).
- `ability.cc`: 능력 실패·확인·지속 효과 안내 7종.
- `player.cc`: HP/MP 부족 경고, 수직 통로, 신앙 보호 문구 4종.
- `invent.cc`: 목록 메뉴·취소 안내 1종.
- `mon-util.cc`: 공격 회피·성역 보호 문구 3종.
- `beam.cc`: 광선·상태 이상·몬스터 반응 문구 21종.
- 합계 **59종의 원문 리터럴 패턴, 62개 발생 위치**에서 한국어 번역을 적용했다.
- `newgame.cc`의 사용자 화면에 나타나던 임시 `[KO TEST]` 표시 **2곳** 제거. `korean-smoke-guard.yml` 검사 대상에 새 게임 UI 추가.
- 기존 Linux 빌드 검증 대상에 `mon-util.cc`를 포함하여 직접 수정한 C++ 파일을 검증하도록 조정.

C++ 출력은 `%s` 등을 보존하여 컴파일 가능성을 유지했으나 이름과 결합된 조사 `이(가)`, `은(는)` 등은 임시 표현이므로, 실제 한국어 음운/조사 선택은 런타임 조합기로 별도 설계한다.

## 후속 번역 큐

1. CI `P0 Korean output callsite audit`에서 `p0-output-callsites` 아티팩트를 내려받아 `english_callsites.csv`를 확인한다.
2. 화면 출력을 확정할 수 있는 고정 문구와 복잡한 동적 조합을 구분한다. `god-abil.cc`, `spl-summoning.cc`, `beam.cc`의 `%s` + 영문 동사 패턴은 C++ 코드 경로에 맞게 별도 분기한다.
3. `source/dat/database/*`, Lua 및 그 밖의 게임 UI 출력 경로도 확인한다. P0 11개 파일만으로 프로젝트 전체 번역률을 주장하지 않는다.
4. Windows 타일 모드에서 게임 생성, 인벤토리, 전투 및 상태 변경을 실제 실행해 화면 출력·UTF-8 글꼴·줄바꿈을 검사한다.

## 최종 병합 결과

- [PR #4](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/4) 병합: `522d00b`.
- 초기 59개 원문 리터럴 패턴 묶음에 이어 신앙·소환·광선·몬스터·플레이어 메시지를 추가 교정. 일부 C++ 출력의 영문 동사 활용·소유격 인자를 제거했으므로 초기 59개만을 전체 신규 번역 수로 사용하면 안 됨.
- [최종 P0 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076532595): 959개 직접 문자열 호출부, 한글 포함 885, 영어/식별자 검토 46, 개발·오류 3, 서식·기호 중심 25.
- [최종 Linux C++ 컴파일](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076532601) 성공. 대상 11개 번역 C++ 파일. 실제 Windows 타일 렌더링, Lua/DB 동적 출력, 한국어 조사 처리 및 대량 플레이 테스트는 미검증.
- `source/dat/database` 계열의 별도 [게임 대사 DB 감사](database-audit-20261024.md)에도 후속 번역이 필요하며, `ko/` 디렉터리가 없어도 원본에 한국어가 일부 포함될 수 있음.
