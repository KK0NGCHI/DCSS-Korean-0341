# 몬스터 주문 시전 대사 한국어화 — 2026-10-24 최종 현황

원문: `source/dat/database/monspell.txt` · 한국어: `source/dat/database/ko/monspell.txt` · 대상: DCSS 0.34.1.

## 검증된 현황

| 검사항목 | 결과 |
|---|---:|
| 원문 고유 키 | **262개** |
| 실제 대사 본문을 한국어로 제공하는 키 | **245개** |
| 번역 오버레이에 없는 키 | **17개** |
| 그중 다른 대사 키 참조(`@...@`) | 12개 |
| 그중 의도적으로 출력하지 않음(`__NONE`) | 5개 |
| 실제 영어 대사 본문이 남은 독립 키 | **0개** |
| 원문에 없는 한국어 키·중복 키·빈 본문 | **0개** |
| 변형 수·필수 치환 변수·가중치·대사 선택 문법 오류 | **0건** |

**주의:** 245/262는 이 파일의 한국어 키 대응률이다. **실제 출력 대사 본문이 있는 원문 키는 모두 대응**하지만, 게임 내 한국어 조사 결합·이름 치환·타일 화면의 정상 출력까지 검증된 것은 아니다. 소스의 별도 메시지·Lua·다른 DB에 남은 영어에도 영향을 주지 않는다.

## 반영한 변경

- [PR #6](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/6): 154개 키 한국어화 및 자동 감사 추가.
- [PR #7](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/7): 게임 DB 로더의 `%%%%%` 구분자 허용 규칙 반영, 빠진 2개 대사 추가.
- [PR #8](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/8): 특수 주문·고유 몬스터·일반 몬스터 대사 89개 키 추가 및 참조 전용/무출력 키 분류.
- [최종 구조 감사](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/40082885965) 통과.

한국어 문장에서는 영어식 전치사·소유격 치환값 일부를 제거하고 문장을 재구성했으며, `@The_monster@`, `@target@`, `@beam@`, 신의 이름·대사 참조 등 중요한 토큰은 보존했다. 원문의 `[표현1|표현2]` 무작위 선택, `w:` 가중치, `VISUAL:` 및 `SOUND:` 지시문도 그대로 다룬다.

## 다음 작업

`monspeak.txt` 일반 몬스터 대사와 `wpnnoise.txt` 무기 소음, 기존 원문에 한국어가 섞인 `godspeak.txt` 및 `shout.txt`를 우선 검토한다. 동적 이름과 한국어 조사, Windows Tiles의 데이터 로딩/화면 출력은 별도 런타임 검증이 필요하다.

재검사 명령:

```powershell
python tools/dcss-extractor/scripts/audit_monspell_ko.py --original source/dat/database/monspell.txt --localized source/dat/database/ko/monspell.txt
```
