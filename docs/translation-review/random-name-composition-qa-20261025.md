# 생성형 이름 병합 후 C++ 연결 검증 (2026-10-25)

대상: `ko/rand_all.txt`, `ko/randname.txt`, `ko/randbook.txt` (PR #29~31, main 병합).
정적 대조: 124/124 keys, 2664/2664 alternatives, weight order and `@...@` multiset match, 0 mismatches. 이는 **게임 실행 검증이 아님**.

## 실제 소스 코드에서 확인한 결합 오류

1. `source/randbook.cc:730-733` — `make_stringf("%s%s of %s", ...)`: 한국어 책 종류와 제목 사이에 **English `of`**가 직접 삽입된다. 예: `마도서 of 연금술`.
2. `source/randbook.cc:453-455` — Xom의 책 이름을 `book_noun + " of " + Xom_book_title`로 조립한다. 한영 혼합 필연.
3. `source/randbook.cc:740-790` — `book_name + " " + [형용사+학파명 | 학파명 + " and " + 학파명]`. 현재 `book_name`이 한국어 명사(예: `마도서`)라 `마도서 화염`, `마도서 화염 and 냉기`처럼 표시될 수 있음.
4. `source/randbook.cc:480-484` — `@level@`을 영어 `number_in_words(level)`로 치환. 한국어 템플릿 `제@level@권`이 `제Three권`처럼 혼합될 수 있음.
5. `source/randbook.cc:448-449,720-722` — 저자명에 `apostrophise(owner) + " "` 사용. 한국어 음역 저자명에 영어 소유격과 선행 어순이 발생할 수 있음.
6. `source/artefact.cc:1653-1676` — 무기·방어구 기본 이름에 공백을 덧붙여 randname 결과와 결합. 현재 `ko/randname.txt`의 `·` 구분자는 조사는 피하지만 최종 문체/폭은 검증되지 않음.
7. `source/artefact.cc:1684-1694` — DB 경로를 우회하는 고유 이름 분기에는 `" of "`가 C++에서 직접 붙음.
8. `source/artefact.cc:1670-1674` — 이름 길이를 `strwidth(name) > 25`로 제한하고 실패 시 `of Bugginess` 영어로 대체. 긴 한국어 조합의 빈도/성공률 확인 필요.

## 병합된 번역의 한계

원문 개수, 가중치, 참조 무결성은 확보되었지만 **생성 조합의 한국어 품질과 런타임 정합성은 미검증**이다. 특히 `@god_name_possessive@`와 저자명 참조는 언어별 소유격 치환을 따로 설계해야 한다.

## 다음 구현 단계

- `randbook.cc`의 3개 합성 분기(고정 제목, 주제 결합, 학파 결합)를 한국어 데이터에 맞게 분리; 영문 플레이 모드는 유지하도록 언어 분기 조사.
- `@level@`의 한국어 숫자 치환과 저자 소유격을 수정하고 각각 테스트 추가.
- `artefact.cc`의 C++ `of` 직접 연결 경로 2곳을 검사하고 한국어 이름 조합 테스트 추가.
- Windows MSYS2로 실제 `crawl.exe` 재빌드 후 새 책 생성, 좀 책, 저자 있는 책, 이중 학파 책, 무작위 아티팩트 이름 각 20개 이상 표본 검사.
- 사용자가 원할 때에만 Actions `workflow_dispatch` 수동 실행 (기본은 로컬 검증).

상태: 문제 발견 및 소스 경로 검증 완료, C++ 수정·빌드·타일 게임 플레이 검증은 아직 시행하지 않음.
