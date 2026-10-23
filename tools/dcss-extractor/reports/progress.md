# DCSS Korean extraction progress

Current phase: **01 — pilot (pending)**

## Phase 00 — baseline completed (2026-10-21)
- Roadmap, extraction rules and tracking schema committed to GitHub.
- Source: `C:\DCSS-Dev\stone_soup-0.34.1\source` (English original).
- Local manifest: `C:\DCSS-Dev\dcss-extractor\source-manifest.json`.
- Files hashed: **26,187**.
- Manifest size: **4,884,428 bytes**.
- Missing pilot files: **0**.
- Read errors: **0**.
- Validation evidence: user-provided console output; manifest contents not independently reviewed.
- Full manifest not yet committed to GitHub.
- Extracted strings / translation coverage: not yet measured.

## Next batch
CPP-PILOT-001: `message.cc`, `invent.cc`, `describe.cc`, `newgame.cc`.

## Batch log
- BASELINE-001: local source manifest generated; zero missing pilot files and read errors.

## FULL-INVENTORY-001 (2026-10-23)
- 전체 소스를 읽기 전용으로 훑는 `scripts/full_inventory_v1.py` 추가. C++/Lua/DES 리터럴과 23종 설명 데이터의 영문↔한국어 키·본문 누락을 CSV로 기록하도록 설계.
- **스크립트 추가 완료 / 실제 전체 실행 및 건수 검증은 미완료**: 현재 연결된 GitHub 환경에서 로컬 Windows의 원본 소스 및 이전 `CPP-PILOT-005/strings.csv`에 접근할 수 없음.
- 실행: `python tools/dcss-extractor/scripts/full_inventory_v1.py --source source --output tools/dcss-extractor/output/FULL-INVENTORY-001`
- 산출물: `strings.csv`, `summary.json`. 이 결과를 기존 AST 기반 `cpp_pilot_v4.py` 분류와 합쳐 정밀 누락 검사를 거쳐야 진정한 전체 인벤토리로 확정 가능.
- 참고: 단순 정규표현식 추출에는 주석 내부 문자열의 오탐 및 C++ raw literal 누락 가능성이 있음. `visible_candidate`는 화면 노출 확정 판정이 아님.
