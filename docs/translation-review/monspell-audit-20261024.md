# 몬스터 주문 시전 대사 한국어화 — 2026-10-24

대상 버전: DCSS 0.34.1. 원문 `source/dat/database/monspell.txt`, 번역 `source/dat/database/ko/monspell.txt`.

## 검증 결과

| 항목 | 결과 |
|---|---:|
| 원문 고유 키 | **262개** |
| 한국어 오버레이 키 | **156개** |
| 정확히 대응하는 원문 키 | 156개 |
| 추가 번역이 필요한 원문 키 | **106개** |
| 원문과 대응하지 않는 한국어 키 | 0개 |
| 중복 한국어 키 | 0개 |
| 한국어 빈 본문 | 0개 |
| 치환 변수·선택지·가중치 구조 오류 | **0건** |

- PR #6: https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/6 — 초기 154개 키 한국어화, 몬스터 주문 구조 감사·회귀 테스트 추가.
- PR #7: https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/7 — 엔진의 `%%%%%` 구분자 호환성과 누락된 2개 주문 대사 번역.
- 최종 CI: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40081571286 — 데이터베이스 감사 및 추가 테스트 모두 성공.
- 엔진 구문: `source/database.cc`의 `_parse_text_db`는 줄 시작의 `%%%%` 4글자를 확인하므로 `%%%%%`도 유효한 구분자이다. 기존 감사 도구가 이 차이를 무시해 `Electrical Bolt cast`, `Spit Lava cast` 2개 키를 누락 집계했으나 현재 교정했다.

**156/262 (약 59.5%)는 해당 파일의 키 대응률이다.** 실제 게임 전체 한국어화율, 개별 대사 문장 수의 번역률, 품질·런타임 검증률을 뜻하지 않는다. 원문에 이미 존재하는 한국어 항목이나 다른 DB 파일은 별도 집계한다.

## 범위 및 주의사항

- 일반 사제·마법사·비인간형 마법사·보이지 않는 시전자 등의 범용 문구, 원소·자연 계열 공격, 고유 몬스터와 일부 일반 몬스터의 주문 대사 번역 포함.
- `@The_monster@`, `@target@`, `@beam@`, 신명·대사 참조 키 등 핵심 동적 변수를 보존한다. 영어 어순에만 필요한 `@at@`, `@possessive@`, `@reflexive@`, `@arms@`, `@subjective@`는 한국어 문장으로 재구성하면서 생략한 경우가 있다.
- `VISUAL:` 및 `SOUND:` 구분, `[표현1|표현2]` 가변 문장, `w:` 가중치 구조를 검사한다.
- 원문 파일을 수정하지 않고 언어별 오버레이를 사용해 남은 106개 키는 게임 데이터베이스 폴백으로 처리한다.
- `@...@`로 치환되는 몬스터 고유명사 및 조사의 자연스러운 연결, 폭·줄바꿈·타일 UI·실제 전투 로그는 Windows Tiles 실행으로 확인해야 한다.

## 다음 번역 단계

1. `monspell.txt`의 잔여 106개 키를 **실제 번역이 필요한 문장, 참조용 별칭, `__NONE`(출력 없음)**으로 분리한다. 무의미한 별칭의 복제 번역은 피하고 실대사부터 교정한다.
2. `monspeak.txt` 원문 고유 키 약 730개와 `wpnnoise.txt` 약 65개의 실제 출력 문구를 우선순위별로 분리해 한국어 오버레이로 추가한다.
3. `godspeak.txt`, `shout.txt`는 최상위 원본에 이미 한글이 일부 있으므로 이를 보존하고 누락만 검토한다.
4. 공통 한국어 조사·명사 결합 전략을 검토하고, 빌드와 게임 실행으로 검증한다.

## 재검사

```powershell
python tools/dcss-extractor/scripts/audit_monspell_ko.py --original source/dat/database/monspell.txt --localized source/dat/database/ko/monspell.txt
python tools/dcss-extractor/scripts/audit_database_translations.py --source source --output tools/dcss-extractor/output/DB-AUDIT-001
```
