# DESC-AUDIT-001 — 설명 데이터 전수 감사 (준비)

기준: `main`에서 2026-10-24 확인한 파일 구성.

## 확인 완료
- `source/dat/descript/*.txt`: 영어 파일 **23개**
- `source/dat/descript/ko/*.txt`: 한국어 파일 **23개**
- 같은 파일명 쌍 **23개**, 대응 파일명 누락 **0개**
- 2026-10-23 기록: `quotes.txt` 유효 원문 키 465/465 대응, 본문 품질 및 런타임은 미검증

## 이번 변경
- `scripts/audit_descriptions.py`: 23개 파일 쌍을 대상으로 영어·한국어 키 누락, 추가 키, 중복 키, 빈 본문, 한글 없는 본문 후보, 참조 수·printf 지정자 수·Lua 구분자 차이를 CSV와 JSON에 기록.
- 결과는 번역 완료 증명이 아니며, 구조 점검에서 의심 항목을 **검토 후보**로만 표시.
- 외부 의존성이 없는 Python 표준 라이브러리 사용. **GitHub 환경에서 실행 결과는 아직 생산하지 않음**.

## 실행
저장소 루트에서:

```powershell
python tools/dcss-extractor/scripts/audit_descriptions.py --source source --output tools/dcss-extractor/output/DESC-AUDIT-001
```

생성 결과:
- `issues.csv`: 실제 키와 문제 분류
- `summary.json`: 파일별 키·문제 개수와 총합

## 판단 기준
- `missing_korean_key`: 우선 번역
- `empty_korean_body`: 우선 복구
- `duplicate_*_key`: 파일 구조 문제 검토
- `review_no_hangul`: 영어 미번역일 수도 있으나 참조/고유명/코드일 수 있음
- `review_reference_count`, `review_printf_count`, `review_lua_delimiter`: 문법 파손 가능성만 표시; 원문과 동일해야 한다는 보장은 없음
- `extra_korean_key`: 버전 간 잔재일 수 있으므로 임의 삭제 금지

## 후속 순서
1. 스크립트 실제 실행 및 출력 검증; 발견된 파서 오탐은 보정.
2. 원문에서 누락된 한국어 키 중 화면에 쓰이는 것 우선 번역.
3. 참조·서식·Lua 항목 수동 검토.
4. 기존 `quotes.txt` 기록과 자동 결과 교차 검증.
5. 확인된 수치를 `reports/progress.json`에 통합; 추출 coverage와 실제 번역/출력 coverage를 분리.

## GitHub Actions 실측 결과 (2026-10-24)

- Workflow run: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39977428592 — 성공.
- 영어 파일 23개 / 한국어 파일 23개.
- 영어 원문 항목 3,781개, 영어 중복 키 3건 ⇒ **고유 영어 키 3,778개**.
- 한국어 대응 고유 키 3,778개 ⇒ **원문 고유 키 대응 100%(3,778/3,778), 누락 0개**.
- 한국어 항목 4,038개; 원문에 없는 한국어 키 260개. 기존 번역 자산 가능성이 있어 삭제하지 않음.
- 검토 후보: 한글 미포함 69개, 서식 지정자 개수 차이 29개, 참조 구문 개수 차이 20개, Lua 구분자 차이 6개. 이들 숫자는 문제의 확정 건수가 아니라 규칙 기반 후보 수임.
- 설명 키 대응률과 번역 품질·실제 게임 출력 검증률은 다름.
- 후속: 보고서 `issues.csv`의 항목별 근거를 읽고 원문 중복 키와 서식 경고를 검증. 이후 C++·Lua 문자열 감사로 전환.

## 2026-10-24 경고 오탐 표본 검증
- 영어/한국어 `egos.txt` 직접 비교: 각각 고유 키 80개, 누락 키 0개, 추가 키 0개, 영어 잔존 후보 0개.
- `quotes.txt` 직접 비교: 원문 고유 키 465개, 한국어 475개, 누락 0개, 추가 10개. 추가 키는 `Terence`, `apple`, `big fish`, `bow`, `giant frog`, `ooze`, `phoenix`, `strawberry`, `sultana`, `wizard`.
- `quotes.txt`의 `Agony spell`, `chain mail`, `large abomination`, `dreamdust necklace`은 한글 없는 문장이 아니라 각각 `<Curse of Agony spell>`, `<leather armour>`, `<small abomination>`, `<dreamshard necklace>` 참조 별칭. 원문 대응 참조이므로 미번역으로 오분류하지 않아야 함.
- 감사 스크립트에 순수 참조문 예외 및 고유 키 대응 통계 추가. 수정 이후 전체 경고 수는 재실행 후 산정하며 이전 69개 한글 미포함 후보를 그대로 확정 수치로 사용하지 않음.
- 별칭의 실제 대상 키 존재·순환 여부와 번역 품질은 추가 검증 과제.
