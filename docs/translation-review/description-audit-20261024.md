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

## 2026-10-24 후속 검수 — #10 성공
- 검사기에서 `<key>`뿐 아니라 `[[key]]` 참조 별칭을 인식하도록 보정.
- 순수 참조문을 영어 잔존 오탐으로 잡던 69건이 **0건**으로 감소. 이는 한글 미포함 후보의 규칙상 감소이지 전체 문장 품질 보증이 아님.
- `hints.txt / HINT_CONVERT`: 원문과 달리 파문·징벌을 단정하고, 부정확한 안내 및 불필요한 `()`가 존재해 원문 의미에 맞춰 다시 번역. 게임 화면 출력은 별도 확인 필요.
- `unrand.txt / skin of Zhor`: 원문에 있는 `you.can_smell()` 조건부 분기를 복원하고 후각 관련 설명 및 원문 의미를 보정.
- 검사 결과: 원문 고유 키 **3,778/3,778 (100%)**, `review_no_hangul` **0**, Lua 구분자 차이 **6→4**, `review_printf_count` 29, `review_reference_count` 20, 원문 중복 키 3, 추가 한국어 키 260.
- GitHub Actions: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39984680062
- 잔여 Lua 경고 4개는 한국어 번역에서 조건문을 추가한 경우로, 삭제보다 원문 충실도·게임 로더 지원 여부를 검토해야 함.

## 2026-10-24 중복 원문 및 서식 검사 보정
- 중복 영어 키 3개 실물 확인: `commands.txt/CMD_EXPLORE_NO_REST`, `monstatus.txt/damage-immune at range monstatus`, `mutations.txt/+LOS mutation`. 각각 짧은/상세 설명이 중복됨. 자동 파서의 최종 항목 선택은 실제 게임 로더 의미와 별도로 검증 필요.
- 한국어 `damage-immune at range monstatus`가 더 짧은 설명에만 대응하므로 상세 원문의 비피해 부가효과·피해 발생원 정의를 반영하여 보정.
- `printf` 검사에서 `80% of`, `20% chance` 같은 일반 영문 백분율 뒤의 문자 `o/c`를 잘못 서식 지정자로 판정한 사례 확인. 정규식의 공백 플래그 허용을 제거한 뒤 전체 재검사.
- 재검사: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39986332516 (성공). `review_printf_count` **29→0건**, `review_reference_count` 20건, `review_lua_delimiter` 4건, 중복 키 3건, 추가 한국어 키 260건.
- 29건 감소는 서식 지정자 오탐 수정 결과이며, 실제 게임 출력 검증은 아직 하지 않음. 남은 20건의 참조 태그 차이는 원문과 한국어의 정확한 토큰 위치/유형 및 게임 내 해석을 조사해야 함.

## 2026-10-24 튜토리얼 원문 충실도 교정
- `tutorial2 resting`: 오래된 100턴·비밀문 탐색 설명을 제거하고, 체력 회복까지 휴식·중요 이벤트 중단 및 타일 휴식 버튼을 반영.
- `tutorial4 spell_success`: 원문은 반지의 착용 전후 주문 실패율 비교인데 기존 번역은 지팡이로 잘못 안내하여 수정.
- `tutorial4 memorise2`: 원문은 기존 주문을 잊고 새 주문을 배운 후 악마 아군 소환인데 기존 번역은 해골 군단을 안내하여 수정.
- `tutorial5 exit`: 오래된 `CMD_PRAY`를 원문의 `CMD_GO_DOWNSTAIRS`로 바꾸고 전체 요약을 0.34.1 기준으로 갱신.
- CI: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39987043048 — 성공.
- 참조 태그 개수 차이 20→17건. 잔여는 단순 개수 불일치와 실제 의미/태그 파손을 분리하여 검토할 것.
- 모든 수정은 정적 원문 대조이며 게임 내 튜토리얼 흐름 실행 검증은 별도.

## 2026-10-24 튜토리얼 번역 교정 추가
- 원문과 대조하여 `tutorial2 throwing`(다트→부메랑), `tutorial3 ego_weapon`(무기 휘둘러 식별→바닥에 올라가면 식별), `tutorial4 resting_reminder`(해골→독 저항 임프), `tutorial4 undead`(불필요한 정보 교정), `tutorial1 autoexplore`(타일 버튼 안내), `tutorial2 wait`(타일 대기 조작), `tutorial3 go_shopping`(영어 잔존·검색 절차)의 7개 항목을 수정했다.
- Actions: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39988155421 성공. 참조 구문 개수 차이 **17→11건**. 설명 고유 키 대응 3,778/3,778 유지.
- 본문 내용은 정적 원문 대조만 완료했으며 튜토리얼 런타임 실행 여부는 아직 검증하지 않았다.

## 2026-10-24 안내·튜토리얼 4건 보정
- `hints.txt/welcome`: 최신 원문의 3개 참고 문서(quickstart, crawl_manual, options_guide) 링크 표기를 복구하고 명령 안내를 정돈.
- `tutorial.txt/tutorial intro`: 타일 모드에서 클릭으로 다음 메시지 진행 안내 복구.
- `tutorial.txt/tutorial2 downstairs`: 타일 모드 캐릭터 클릭 동작 복구.
- `tutorial.txt/tutorial4 meph_reminder`: 현재 주문 암기 탭에 맞춰 구버전 마법서/소지품 창 조작법 제거.
- 검사 실행 https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39988582819 성공. 참조 구문 경고 11→7건. 고유 영어 키 대응 3,778/3,778 유지. 미해결: 참조 경고 7, Lua 차이 4, 중복 원문 키 3, 추가 한국어 키 260.
- 검사는 키·표시 태그의 정적 검사이며 실제 게임 실행 확인이 아님.

## 2026-10-24 일괄 처리: 설명 감사에서 전체 문자열 조사로 확대
- 힌트 3개 항목 직접 수정: `HINT_SEEN_FIRST_OBJECT` (중첩 태그 오류·구버전 줍기 조작 안내), `HINT_SEEN_BRANCH` (마우스/키보드별 설명 정리), `finished random 3` (구버전 커뮤니티 주소 목록 제거).
- 설명 감사 CI 성공: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39989209855. 키 대응 3,778/3,778(100%), 참조 경고 7→5, Lua 차이 4, 원문 중복 3, 한국어 추가 키 260.
- 기존 `full_inventory_v1.py`를 재사용하는 전체 인벤토리 CI를 추가. 첫 실행에서 설명 파일 하위 폴더를 정상 원문과 혼합하여 140개 누락이라는 오탐이 발생해, 실제 23개 원문 가족만 설명 키로 취급하도록 수정.
- 교정한 전체 조사 CI 성공: https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/39989209866.
- 전체 조사 결과: 읽은 파일 **1,341**, 추출 레코드 **55,619**, 파일 읽기 오류 **0**. 분류: C++/Lua/DES 등 `visible_candidate` 3,033, `review_dynamic` 1,591, `review_unknown` 35,439, `internal_candidate` 8,126, `comment_candidate` 3,626, `test_marker` 23, 설명 원문 레코드 `review_translation_present` 3,781. `translation_missing_key` 0.
- 모든 분류는 **문자열의 어휘적 후보**이며 실제 화면 출력, 정확한 번역 단위 수, 누락 번역 0건을 입증하는 검사는 아님. 특히 `review_unknown`은 미번역 확정이 아니다.
- 다음 우선순위: `visible_candidate`와 `review_dynamic`의 실제 C++/Lua 출력 근거 확인, `[KO TEST]` 스모크 잔재 조사, 원문과 한국어 런타임 연결 확인.
