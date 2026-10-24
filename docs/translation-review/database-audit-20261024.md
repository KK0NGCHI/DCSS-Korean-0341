# DCSS 0.34.1 게임 대사 DB 감사 — 2026-10-24

기준: `main`, `source/dat/database`, `DB-AUDIT-001`. 자동 검증: [Korean gameplay database audit](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40076997160) (성공).

## 확인된 현황

- 최상위 원본 `*.txt` **23개**, 원본 고유 키 합계 **2,019개**.
- 한국어 `dat/database/ko` 오버레이는 `godname.txt` **1개**. 원문 23개 키 모두 대응, 누락/중복/빈 항목 0개.
- `godname.txt`의 신별칭과 좀(Xom)의 무작위 칭호 **본문 50개**를 번역했으며 원본 키 및 `w:` 가중치를 보존했다.
- 최상위 원본 파일 본문에 이미 한글을 포함한 줄 **301개**. 한글이 없고 라틴 문자를 포함한 줄 **13,245개**. 라틴 문자는 이름·기능 키·동적 마커에도 있으므로 **미번역 확정 개수로 해석 금지**.
- 언어 데이터베이스 로더는 현재 언어의 오버레이를 우선 조회하고 없으면 원문 DB를 참조한다. `ko` 폴더가 비어 있었어도 최상위 원본 파일에 한글이 포함된 부분은 기존부터 한국어로 표시될 수 있었다.

| DB 원본 | 고유 키 | 기존 원본 한글 본문 줄 | 원본 내 라틴 전용 본문 줄 | 별도 KO 키 대응 |
|---|---:|---:|---:|---:|
| `monspeak.txt` | 730 | 0 | 3,540 | 0 |
| `monspell.txt` | 260 | 0 | 357 | 0 |
| `wpnnoise.txt` | 65 | 0 | 733 | 0 |
| `godspeak.txt` | 193 | 123 | 430 | 0 |
| `shout.txt` | 93 | 87 | 32 | 0 |
| `godname.txt` | 23 | 0 | 50 | 23 |

`monflee.txt`와 `shout.txt` 등은 최상위 원본에 한국어가 이미 삽입되어 있으므로 전면 재번역 전에 실물 검수가 필요하다. 위 수치는 검사기의 보수적 정적 분류이며 **실제 화면 출력이나 전체 번역률이 아니다**.

## 후속 처리 순서

1. 몬스터 특수대사(`monspeak.txt`), 몬스터 주문 대사(`monspell.txt`), 무기 소음(`wpnnoise.txt`)의 실제 호출·참조 분류. 중복 키 및 참조 토큰 `@...@`, `VISUAL:`, `SOUND:`, `w:` 보존.
2. 기존 한국어가 섞인 `godspeak.txt`, `shout.txt`는 한국어 대사 및 참조에 영향 주지 않는 항목부터 검토.
3. 대량 번역은 `dat/database/ko/<name>.txt` 오버레이 방식으로 관리하여 원문·기존 번역을 보존하고 미번역은 원문으로 폴백. 모든 키를 채우기 전에 실행 검증을 별도 수행.
4. 번역 항목별 `draft / reviewed / runtime_checked` 상태를 기록하고 실제 화면 출력의 자연스러움 및 변수를 검사.
5. 원본 텍스트 라이브러리의 키와 데이터에 대한 자동 회귀 검사 및 Windows Tiles 통합 검증.

도구: `tools/dcss-extractor/scripts/audit_database_translations.py`, CI `.github/workflows/database-translation-audit.yml`. 실행 예:

```powershell
python tools/dcss-extractor/scripts/audit_database_translations.py --source source --output tools/dcss-extractor/output/DB-AUDIT-001
```
