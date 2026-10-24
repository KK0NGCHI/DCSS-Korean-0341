# DCSS 0.34.1 몬스터 대사 — 원문 실제 본문 키 대응 검토 (2026-10-24)

## 결과

- 작업 브랜치: `translation/monspeak-donald-regions-20261024-h`
- PR: [#19](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/19)
- 대상: `source/dat/database/ko/monspeak.txt` / 원문 `source/dat/database/monspeak.txt`
- 원문 고유 키 **731개**, 한국어 오버레이 대응 **562 → 629개** (**67개 신규**, 대응률 **86.0%**).
- 이번 추가 항목의 소스 대응 변형/코드 줄 **868개**, 그중 한글 포함 줄 **749개**. 여기에는 Lua 코드, 원문 참조만 유지한 행도 포함되므로 868개의 독립 번역 문장이라는 뜻은 아님.
- 미대응 원문 키 **102개**는 **참조·라우팅 전용 87개**, `__NONE` 등 **무출력 15개**. 최초 분류 방식에 따른 미대응 **독립 본문 또는 Lua 포함 항목은 0개**.
- 한국어 4개 DB 오버레이 원문 키 대응 합계 **962개**: `godname` 23 + `monspell` 245 + `monspeak` 629 + `wpnnoise` 65.

## 이번 번역 내용

1. 도널드(Donald)의 미대응 지역별 대사: Orc, Elf, Swamp, Shoals, Spider, Slime, Snake, Vaults, Crypt, Abyss, Zot, Orb 소지. 공통 대사 `_generic_Donald_`는 이전에 번역돼 있음.
2. 도널드의 미대응 신앙별 대사: Zin, the Shining One, Kikubaaqudgha, Yredelemnul, Okawaru, Makhleb, Sif Muna, Trog, Nemelex Xobeh, Elyvilon, Lugonu, Beogh, Ignis, Jiyva, Cheibriados, Xom, Vehumet, Ashenzari, Dithmenos, Gozag, Qazlal, Pakellas, Hepliaklqana, Uskayaw, Wu Jian 등.
3. Crazy Yiuf의 철학적 독백, 혼란 상태, 일반 광기 어린 대사와 **72 + 85개** 무작위 단어 조각.
4. 그룬(Grunn)의 희귀 대사, 나타샤 사망 대사, 자크크리시스의 몬스터 연구 독백, 베오그 신도의 우호적 일반·희귀 대사.
5. Lua 조건문을 이용하는 13개 원문 미대응 키: 외양에 따라 바뀌는 임프 호칭·신체 명칭, 아군 사냥개, 아스테리온·이지브·테런스·성 로카·스프로즈·자크크리시스·네코마타 등의 조건부 발언. **게임 로직인 조건과 비교 연산, 참조 변수 자체는 원문을 유지하고 화면에 출력할 문자열만 번역.** `Sprozz` 자체는 참조 경로만 갖고 있어 원문 구조와 동일.

## 검증

- 원문 대비 신규 67개 키와 그 **868개 행/변형** 검사: 대응 행 수, `w:` 가중치, `@...@` 동적 토큰, 대안 선택 `[a|b]`, `VISUAL:` 지시부 및 Lua 블록 구분자 불일치 **0개**.
- 기존 대응 키를 포함한 미변경 영어 실질 문장 재조사: 기존 원문과 똑같이 남아 있는 항목은 `__NONE`, 참조 전용 조합, Lua 조건식 등으로 확인. **원문 본문 키는 모두 대응하지만 문체·출력의 정확성까지 확인된 것은 아님.**
- 남은 참조 키 중 `_blorkula_colour_`의 `@rainbow_colour@`·`@misc_colour@`은 같은 `monspeak.txt`의 독립 키가 아닌 외부 치환 후보로 확인됨. 실제 엔진 처리와 한국어 조사 결합은 런타임 검토가 필요.
- 자동 구조 감사: [PR #19](https://github.com/KK0NGCHI/DCSS-Korean-0341/pull/19) CI 검사와 병합 후 main 결과를 확인할 것.
- Linux headless 런타임: 실제 `crawl` 빌드 및 한국어 DB 생성 검사에 해당. **629개 키 각각의 전투·대사 표시를 직접 테스트하는 방식은 아님.**
- Windows Tiles와 폰트, UI, 동적 `@...@` 호출 결과 및 자연스러운 한국어 어순/조사, Lua 문자열 조합은 별도 플레이테스트가 필요.

## 대응률 해석 및 다음 우선순위

**`monspeak` 원문 모든 키의 번역 오버레이 대응률: 629/731 = 86.0%.** 그러나 남은 102개는 본문이 아니라 참조 라우팅 및 무출력 키로 분류되므로, 불필요하게 복사해 형식상의 100%를 만들지 않음. 이는 게임 전체 한국어화 완료나 실제 모든 메시지의 정상 재생을 뜻하지 않음.

후속으로 남은 전체 DB 파일의 실제 영어 본문, C++ 동적 메시지, 한국어 이름 뒤 조사와 슬롯·템플릿 출력, Windows Tiles 런타임 검증을 진행할 것.
