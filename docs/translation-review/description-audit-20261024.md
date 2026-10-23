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
