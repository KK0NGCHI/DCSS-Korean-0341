# DCSS 0.34.1 — quotes.txt 번역 보류 및 검토 목록

- 기준: `source/dat/descript/quotes.txt`의 영어 원문.
- 작업 원칙: 뜻이 불확실하거나 번역 방식에 이견이 예상되는 인용은 함부로 의역하지 않고 사용자와 검토한 뒤 반영한다.
- 상태: **검토 필요**. 아래 목록은 전체 미번역 목록이 아니라 쟁점이 식별된 사례다.
- 주의: `<key>` 형태의 항목은 다른 인용문 참조이며, 한국어 파일에 키가 있다고 해서 참조 대상 본문까지 번역된 것은 아니다.
- 원문에 포함된 작가명, 연도, 출처는 사실 확인이 필요한 표기일 수 있다. 원문을 보존한 채 별도로 교정한다.

## 결정이 필요한 항목

| 원문 키 | 보류 이유 | 제안 |
| --- | --- | --- |
| `A shimmering altar of Xom` | 인터넷 밈(@dril, 2014)의 노골적인 욕설과 의도적인 비문이 풍자의 핵심 | 욕설 수위를 유지할지, 자연스러운 한국어로 낮출지 결정 |
| `calcifying dust cloud` | T. S. 엘리엇 《황무지》 인용; 국내 번역 관행, 행갈이와 저작권을 점검할 필요 | 작품에 맞는 새 번역을 작성하고 기존 번역의 표현과 대조 |
| `Abyss` | Jonathan Wojcik, *Awful Hospital* (2021)의 장문 초현실 산문; 신조어와 묘사어 다수 | 신조어 용어집을 만든 뒤 단락 단위로 번역 |
| `The open sea` | 장문 인용, 출처·문화적 배경 대조 필요 | 출처 확인 후 전체 문맥 기준 번역 |
| `A one-way gate to the infinite horrors of the Abyss` | 긴 인용의 문학적 맥락 확인 필요 | 원문·작품 출처 교차 검증 |
| `cloak of the Thief` | @dril의 오탈자와 갑작스러운 반전이 개그의 핵심 | 인터넷 밈 특유의 문체 재현 범위 결정 |
| `ring of the Octopus King` | 해학시(limerick)의 운율, 성적 농담 및 반지의 수를 활용한 말장난 | 의미 우선/압운 우선 중 방식 선택 |
| `Bat Form ability` | 바우하우스 노랫말 직접 인용 | 짧은 번역 인용 처리 및 출처 표시 검토 |
| `Bend Time ability`, `Slouch ability`, `Step From Time ability`, `Temporal Distortion ability` | 동일 곡 *Time Warp* 가사의 여러 부분 | 동일 노래의 한국어 표현을 통일하여 번역 |
| `Cause Fear spell`, `Frozen Ramparts spell`, `Irradiate spell`, `Orcish Mines` | 현대 대중음악 가사를 사용함 | 원문 인용 범위와 한국어 번역 방식을 정한 뒤 처리 |
| `ring of stealth`, `ring of fire`, `tower shield of Ignorance` | 가사 원문과 유머를 유지할지 의역할지 판단 필요 | 출처별 문체 규칙 수립 |
| `A faded altar of an unknown god`, `Temple`, `Mass Confusion spell` | 킹제임스 성경의 고풍스러운 어법 | 임시 한국어 번역은 반영함. 국내 성경 번역과 직접 대조한 인용이 아니므로 인용문 표기·어투 검토 |
| `An opulent altar of Gozag` | Francisco de Quevedo, *Poderoso caballero es don Dinero*: 돈을 ‘돈 나리’로 의인화한 풍자 | 임시 한국어 번역 반영. 돈 나리/돈 경/돈 선생 등 명칭 선택 검토 |
| `dark maul` | Janusz Christa의 폴란드 만화 관련 인물·작품 표기의 한국어 정착형 불명확 | 임시 번역 반영했으나 인명·작품명 확인 전까지 재검토 |

## 확인 자료

- 케베도의 원작 시: https://www.wvw.poesi.as/fq03015.htm
- 세르반테스 연구소의 *Poderoso caballero es don Dinero* 관용구 풀이: https://cvc.cervantes.es/lengua/biblioteca_fraseologica/r7_alvarez/senores_08.htm
- 원본 데이터: https://github.com/KK0NGCHI/DCSS-Korean-0341/blob/main/source/dat/descript/quotes.txt

## 향후 처리 기준

1. 키/원문/출처/의미/번역안/결정 상태를 1행으로 관리한다.
2. 영어 원문 키, `%%%%` 구분자, `<key>` 참조, Lua 등은 번역 과정에서 변경하지 않는다.
3. 번역이 어렵다는 이유로 원문의 의미를 바꾸거나 임의의 다른 인용으로 대체하지 않는다.
4. 같은 작품을 여러 번 인용하면 이름과 문체를 통일한다.
5. 게임 내 실제 표시는 별도 빌드·플레이 테스트가 필요하다.

## 2026-10-23 작업 상태 갱신

- 이번 세션의 28·29차 작업에서 일부 검토 대상에도 **임시 번역안**을 추가했다. 파일에 존재한다는 이유로 사용자 검토가 끝난 확정 번역으로 간주하지 않는다.
- 잠정 반영: `A shimmering altar of Xom`, `calcifying dust cloud`, `cloak of the Thief`, `ring of the Octopus King`, `Bat Form ability`, `Bend Time ability`, `Slouch ability`, `Step From Time ability`, `Temporal Distortion ability`, `Cause Fear spell`, `Frozen Ramparts spell`, `Irradiate spell`, `Orcish Mines`, `ring of stealth`.
- 남은 협의 사항: 인터넷 밈의 욕설·오탈자 재현, 시와 노랫말의 운율 및 어투, 고유명사의 정착 표기. 이들 항목은 별도의 품질 승인 전까지 **잠정 번역** 상태다.
- 특히 `A shimmering altar of Xom`: 현재 번역은 노골적 욕설을 일부 완화했으며, 원문의 거친 어감과 정확히 같지 않다. 사용자 결정에 따라 수정한다.
- `ring of the Octopus King`: 의미를 우선한 번역으로 원문의 각운을 보존하지 못했다.
- 이번 단계는 설명 키 대응 작업이며 빌드·게임 출력은 미검증이다.

## 2026-10-23 후속 검수 메모 (44차 이후)

- `Abyss`: 초현실적 신조어와 인물 이름의 표기는 잠정안이며, 원작 *Awful Hospital* 문맥 검수가 필요하다.
- `Swiftness spell`, `Orb Guardian`, `Summon Illusion spell`: 인터넷 밈 또는 가사 특유의 구어체·욕설·반복을 잠정 번역했다. 최종 문체를 일괄 검수한다.
- `ring of poison resistance`, `tyrant leech`: 원문 파일에서 키와 본문 사이 빈 줄이 빠진 듯한 항목. 단순 빈 줄 파서는 대사·출처까지 키로 인식한다. 원본 게임 로더의 실제 구분 규칙을 점검한 다음 원문 키가 무엇인지 확인해야 하며, 잘못된 거대 키를 추가해서 대응률을 올리지 않는다.
- 이 단계의 키 대응은 번역문의 존재만을 뜻하고, 원문 충실도·출처·게임 화면 표시는 아직 전수 검증되지 않았다.

## 2026-10-23 — 원문 키 대응 완료 및 후속 검수 현황

- `source/dat/descript/quotes.txt`: 유효 원문 키 **465개**.
- `source/dat/descript/ko/quotes.txt`: 한국어 항목 **475개**, 그중 원문 대응 **465개(100%)**, 원문에 없는 이전 항목 **10개**, 중복 키 **0개**, 원문 대응 항목 중 빈 본문 **0개**.
- 원문 형식 보정: `ring of poison resistance` 및 `tyrant leech`에서 키 다음 빈 줄이 없어 대사가 키로 잘못 읽히는 문제를 영어 원문에 빈 줄을 추가하여 수정했다. 기존 `ring of poison resistance` 한국어 번역은 유지하고 `tyrant leech`만 추가 번역했다.
- 원문에 없는 한국어 항목 10개(`Terence`, `apple`, `big fish`, `bow`, `giant frog`, `ooze`, `phoenix`, `strawberry`, `sultana`, `wizard`)는 이전 버전 자산일 수 있으므로 제거하지 않는다.
- 이전의 '번역 보류' 표에 기재된 일부 항목과 장문 인용문은 **초벌 번역 반영 / 사용자 일괄 검수 대기**로 해석한다. 키 100%는 번역 품질이 확정되었거나 게임 내 출력이 검증되었다는 뜻이 아니다.
- 다음 단계: 참조 구문·특수기호 검증, 23개 설명 파일의 실제 로더 연결 확인, C++ 및 Lua의 동적 출력 한글화와 타일 빌드 테스트.


## 2026-10-23 — 잔여 번역 범위 1차 재조사 및 AI 제안안

> **이 문서는 인용문만이 아니라 잔여 한글화 과제의 검토 진입점으로도 사용한다.** 모든 아래 번역은 **AI 제안/초벌안**이며 사용자 승인 전에는 확정하지 않는다. 실제 파일 본문을 확인한 것과 실행 검증을 구분한다.

### A. 추가로 번역해야 할 영역 (저장소 실물 대조)

| 우선순위 | 경로·대상 | 확인한 근거 | 상태 및 다음 처리 |
| --- | --- | --- | --- |
| P0 | `source/newgame.cc` | `newgame_char_description`에 `Recommended character`, `Random character`, `Random `, `Recommended `; `_welcome`에 `Welcome` 등 영어 출력 조합이 남아 있음 | **미완료/실제 출력 검증 전**. 새 게임/종족·직업 선택·이름 붙이기와 동적 조사·어순을 우선 처리 |
| P0 | `source/message.cc` | `_mpr`와 메시지 출력 코드가 영어식 구두점·합치기·반복 횟수 표기(` x%d`) 등을 다룸 | **미완료**. 개별 메시지 발생 지점과 한국어 출력·조합 규칙을 별도로 조사. C++ 문자열 모두가 플레이어 표시 문구는 아님 |
| P0 | `source/invent.cc` | `%d/%d gear slots`와 일부 `[KO TEST]` 삽입 문자열 확인 | **부분 시험 상태**. 실제 인벤토리 제목, 슬롯, 장비 표시를 인게임 검증하고 미번역 문구를 처리 |
| P0/P1 | `source/describe.cc` | `Description|Quote`, `describe-generic` 등 설명창 UI 문자열과 `[KO TEST]` 시험 문자열 확인 | **부분 시험 상태**. 설명 텍스트 파일과 별개로 화면의 탭·버튼·동적 설명을 번역 |
| P1 | `source/dat/descript/ko/*.txt` 전체 | 인용문을 제외한 설명 파일도 존재함. 예: `ko/monsters.txt`의 Lua 조건부 설명 | **재검증 필요**. 영문↔한국어 키 대조만으로 문장 내부 영어·참조·스크립트·버전 차이는 파악되지 않음 |
| P1 | `source/dat/dlua/*.lua`, `source/dat/clua/*.lua`, `source/dat/des/**/*.des` | `source/dat/dlua/tutorial.lua`에서 `crawl.mpr(data.text, data.channel)`, `crawl.tutorial_msg(...)` 같은 동적 메시지 경로 확인 | **인벤토리 미완료**. `tutorial.lua` 자체의 채널 이름은 그대로 두고, 실제 문구가 전달되는 호출부·데이터 파일을 추적 |
| P1/P2 | 도움말·키바인딩·게임 옵션·튜토리얼·신앙/상점/종족·직업·스킬 이름 | 추출 로드맵의 P0~P2 범주이나 일괄 번역·실행 검증 완료 근거 없음 | **미완료로 취급**. 독립적인 원문 문자열 목록 및 다국어 키/포맷 대조 필요 |
| 공통 | `tools/dcss-extractor/` 추출 결과 | `ROADMAP.md`는 01~07단계를 아직 완료로 표시하지 않으며, `reports/progress.md`는 01 pilot을 pending으로 기재. 이전 대화에서 더 나아간 로컬 실행 결과가 있었지만 저장소 보고서는 갱신되지 않음 | **상태 기록 불일치**. 로컬 `CPP-PILOT-005`, `strings.csv`, 분류 보고서의 최신 결과를 다시 수집·커밋한 뒤 미번역 분모 산정 |

**중요:** `quotes.txt` 465/465는 **인용문 키**의 완성도일 뿐, DCSS 게임 전체 번역률을 뜻하지 않는다. 전체 미번역 개수는 소스 전체 추출·화면 노출 여부 분류·기존 번역 재대조가 끝나기 전까지 확정하지 않는다.

### B. 표현별 권장 번역안 (원문 / 제안 / 근거)

| 대상 | 원문·쟁점 | **AI 권장안** | 근거 / 유의점 |
| --- | --- | --- | --- |
| 새 게임 시작 | `Recommended character` | **추천 캐릭터** | 간결한 메뉴 라벨. `Recommended ` 접두사를 무조건 치환하는 대신 종족·직업을 포함한 결과 문장을 완성형으로 조합하는 편이 안전 |
| 새 게임 시작 | `Random character` | **무작위 캐릭터** | `무작위` 용어 통일 제안. 한국어에서 종족/직업 앞뒤 어순 별도 처리 |
| 새 게임 환영 | `Welcome` + 종족/직업/이름 | **환영합니다, {이름}님.** 등 완성된 문장 단위 | 지금의 영어식 `the`, `unnamed`, 쉼표 연결을 단순 단어 치환하면 조사·어순이 깨질 수 있음. 인게임 실제 완성 문장 확인 후 설계 |
| 인벤토리 | `%d/%d gear slots` | **장비 슬롯 %d/%d** | 형식 지정자 개수·순서 유지. 실제 의미가 사용/전체인지 화면에서 확인 |
| 설명창 탭 | `Description|Quote` | **설명 / 인용문** | 좌우 탭 UI 표시 폭과 `[<w>!</w>]` 같은 강조 태그 보존 필요 |
| 인용·문체 | `A shimmering altar of Xom`의 @dril 욕설 | **거친 원문의 의도를 살리되 가독성을 해치지 않는 한국어 구어체** | 지나친 순화는 원문 유머를 훼손하므로 현재 초벌안을 기준으로 강도만 보정하는 방향 추천 |
| 인용·말장난 | `ring of the Octopus King` | **뜻을 우선하고 필요하면 운율을 덧붙이는 의역** | 반지 수와 농담의 의미를 보존하고 억지 압운으로 정보가 빠지지 않도록 |
| 인용·고유명 | `An opulent altar of Gozag`의 `don Dinero` | **돈 나리** | 의인화·풍자·호칭의 우스꽝스러움을 전달. 기존 번역과 대조 필요 |
| 인용·신조어 | `Abyss`, *Awful Hospital* | **뜻이 통하는 한국어 문장을 우선, 설정 고유어는 음역/병기** | 본문에 초벌안 반영 완료. `branchinated`, `endomoon` 등은 원작 용례 확인 후 조정 |
| 인용·가사 | `Swiftness spell`, `Orb Guardian` 등 | **반복·명령조·비문을 재현하되 고유명과 출처 보존** | 원문의 과장과 리듬이 핵심. 가사별로 직역만 고집하지 않음 |
| 로그 | 전투·탐색·시스템 메시지 | **짧은 반말 로그** | 프로젝트의 기존 잠정 문체. 주어·목적어·조사 결합 방식은 별도 규칙화 필요 |

### C. 번역 검수 진행 방식에 대한 제안

1. **P0 추출 목록 먼저 확정:** `newgame.cc`, `invent.cc`, `message.cc`, `describe.cc`의 문자열을 화면 출력/내부 식별자/동적 조합/불확실 항목으로 구분한다. 문자열 리터럴 개수를 바로 번역 대상 개수로 간주하지 않는다.
2. **번역안까지 같이 기록:** 검토 대기 행에는 `파일:줄 / 원문 / 문맥 / AI 권장 번역 / 대안 / 보류 이유 / 상태`를 채운다. 제안 없는 '결정 필요'만 쌓지 않는다.
3. **대량 초벌 번역 후 일괄 검수:** 사용자는 제안안에 대해 추후 모아서 의견을 주면 된다. 그 전에는 검수 요청을 작업 정지 조건으로 두지 않는다.
4. **게임 검증은 별개:** 슬롯/색상 태그, `printf` 자리표시자, Lua 삽입식과 조건문, 참조 키, UTF-8/줄폭을 검사하고 타일 빌드에서 확인한다.
