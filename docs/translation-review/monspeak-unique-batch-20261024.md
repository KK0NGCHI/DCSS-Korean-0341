# DCSS 0.34.1 — 고유 몬스터 대사 추가 번역 (2026-10-24)

## 범위와 실측

- 파일: `source/dat/database/ko/monspeak.txt`.
- 번역 전 원문 대응 고유 키: **260/731**, 미대응 **471**.
- 이번 배치: **82개** 고유 키 추가 (27 + 31 + 24).
- 번역 후 원문 대응 고유 키: **342/731 (46.8%)**, 미대응 **389**.
- 수치는 **해당 대사 파일의 고유 키 대응률**로, 실제 대사 본문만의 완료율이나 게임 전체 번역률이 아님.
- 원문 중복 키 `_laughs_` 1건을 유지하고 원문 데이터는 수정하지 않음.

## 번역한 고유 몬스터·세부 대사

- 1차 27개 키: Edmund, Erica, Erolcha, Eustachio, Frances, Frederick, Fannar, Gastronok; 공통/희귀 대사, Frederick의 신앙별 문구, 전투 승리 대사.
- 2차 31개 키: Grinder, Harold, Ignacio, Ilsuiw, Jessica, Natasha, Robin, Nessos, Pargi; 현상금 사냥꾼 Harold의 은퇴 계획을 구성하는 조합 단어 포함.
- 3차 24개 키: Jorgrun, Joseph, Josephina, Josephine, Khufu, Kirke, Lodul, Louise, Maggie, Mara; 일반/희귀 대사, 비고유 조합 토큰·무작위 대사 선택 포함.

원문의 **가중치(`w:`)**, **대사 참조(`@...@`)**, **VISUAL/SOUND 접두부**, **무작위 대안(`[A|B]`)**을 대응되게 유지했다. 이름·대상 등 게임에서 삽입되는 필수 변수는 보존하되 한국어 문장에 불필요한 영어식 전치사·소유격 변수는 문장에 흡수했다.

## 검증 및 제한

- 구조 감사: [Korean gameplay database audit](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40097133502).
- Linux 한국어 DB 로더: [Korean localized database runtime smoke](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40097133504).
- 구조 감사는 변형 수, 토큰, 가중치 및 지시부 규칙을 확인하며, 한국어 번역의 문학적 품질이나 실제 호출 시 자연스러운 조사 결합을 보증하지 않는다.
- 기존 Linux 런타임 스모크는 DB에 한국어 본문이 담기는지 대표값 3개를 검증하는 방식이므로, 이번 82개 키 **각각의 실제 대사 출력**까지 테스트한 것은 아니다.
- Windows Tiles에서 한국어 폰트·줄바꿈·동적 이름 결합 미검증.

## 후속 작업

1. 미대응 389개 키를 **실제 출력 본문 / 참조·무출력 / Lua·변수 결합**으로 분리하고 고유 몬스터 대사를 계속 번역한다.
2. 일반 몬스터 대사를 더 번역하면서 이름 뒤 한국어 조사 결합을 개선한다.
3. `wpnnoise.txt` 미대응 47개 키, `godspeak.txt`의 영어 잔여 본문을 처리한다.
4. 대표 고유 몬스터의 실제 게임 호출에서 텍스트 자연스러움을 확인한다.
