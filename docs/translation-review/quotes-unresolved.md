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
