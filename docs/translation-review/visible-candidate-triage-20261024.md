# 출력 문자열 후보 1차 분류 — TRIAGE-001

기준: 2026-10-24, `FULL-INVENTORY-001`을 `triage_visible_v1.py`로 후처리.

## 검증 결과

- GitHub Actions: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40073769987 (전체 조사, 단위 테스트, triage, 산출물 업로드 성공).
- 전체 소스 조사에서 `visible_candidate` **3,753**개와 `review_dynamic` **2,286**개, 합계 **6,039**개 레코드 입력.
- 중복 문자열 리터럴을 묶은 결과 **5,450**개 검토 그룹.
- 구분: `review_english_or_identifier` **5,446**개, `contains_hangul` **4**개.
- 파일별 그룹 우선순위: P0 **646**개, P1 **635**개, P2 **4,169**개.
- **P0 중 영문/식별자 검토 대상은 642개**. 미번역 확정 642개라는 뜻이 아님.

## 내려받을 산출물

위 Actions 실행의 `full-inventory-001` 아티팩트에 다음이 포함됨:

- `triage/review_queue.csv`: 전체 그룹·발생 횟수·원본 문자열·샘플 파일과 위치
- `triage/p0_english_review.csv`: 전투·상태·메시지·메뉴 중심 P0 영문/식별자 후보만 별도 정렬
- `triage/triage_summary.json`: 후보 분류·중복 정리의 실행 수치
- 기존 `strings.csv`, `summary.json`, `priority_files.csv`·`priority_files.json`도 유지됨

## 반드시 구분할 것

1. **미번역 확정이 아님.** `visible_candidate`는 출력 함수 주변에 있다는 근거만 포함하며, 주석/개발용 오류/이미 처리된 문자열이 섞일 수 있음.
2. **문맥이 다르면 별도 번역 단위가 됨.** 동일 문자열끼리 묶었지만 코드 위치는 보존했으며, 실제 동일 번역이 가능한지는 추후 검증.
3. **61,032건의 전체 문자열 재고와 5,450개 그룹은 분모가 다름.** 나머지 `review_unknown` 41,242건은 아직 이 우선 작업 목록 밖에 있고, 중요한 표시 문자열이 포함될 가능성이 있음.
4. **텍스트 조각과 변수 서식은 실행 결과로 확인.** 공백·조사·영문 이름이 결합된 문장은 원본 영어 리터럴을 번역해도 매끄럽지 않을 수 있음.

## 다음 실행 순서

1. `p0_english_review.csv`의 각 후보에 실제 출력 함수·분기·변수 조합 근거를 추가하고 `player-visible / internal / false-positive / already-KO`로 재분류.
2. `player.cc`, `beam.cc`, `ability.cc`, `message.cc`, `invent.cc`, `newgame.cc`, `god-abil.cc`, `spl-summoning.cc` 등에서 실제 미번역인 항목만 모아 배치 작업.
3. 출력 문자열 패턴에서 포맷 문자열·대상 이름 뒤의 한국어 조사 처리를 별도로 검증.
4. CI에서 그룹별 `reviewed`/ `translated`/ `runtime_checked` 상태를 기록하여 **측정 가능한 번역률**을 만들어 나갈 것.
