# 번역 작업: Actions 자동 실행 없이 로컬 검증하기

번역 작업 중에는 PR 생성, 커밋, main 병합만으로 GitHub Actions를 실행하지 않는다. 주요 검사 7개 워크플로는 `workflow_dispatch`(수동 실행) 전용이다.

## Windows 11 / PowerShell

저장소 루트에서 실행:

```powershell
cd C:\DCSS-dev\stone_soup-0.34.1-ko
python -m unittest discover -s tools/dcss-extractor/scripts -p 'test_audit_database_translations.py' -v
python tools/dcss-extractor/scripts/audit_database_translations.py --source source --output tools/dcss-extractor/output/DB-AUDIT-LOCAL
python -m unittest discover -s tools/dcss-extractor/scripts -p 'test_audit_monspell_ko.py' -v
python -m unittest discover -s tools/dcss-extractor/scripts -p 'test_audit_monspeak_ko.py' -v
```

소스, 폰트, 게임 바이너리 등은 별도로 빌드·검증해야 한다. **이 검사는 GitHub Actions 시간을 쓰지 않는다.** 원본 파일 누락 또는 환경 문제로 검사가 실패하면 결과를 성공으로 간주하지 않는다.

## 운영 원칙

- 번역문은 충분한 단위(예: DB 1~3개 파일)로 모아 커밋한다.
- 원문 키, 변형 개수, `w:N` 가중치, `@...@` 참조, Lua 문법을 정적 비교한다.
- CI 자동 실행은 비활성화한다. 사용량과 필요성을 확인한 후 검증 시점에만 GitHub Actions 화면에서 **Run workflow**를 직접 누른다.
- 신규 워크플로 추가 시에도 자동 PR/push 트리거 대신 수동 실행을 기본값으로 한다.
- 정적 검사 통과는 실제 Windows Tiles 표시 품질 또는 완전한 컴파일 성공을 의미하지 않는다.

기존 사용자의 실제 클론 경로가 다르면 첫 줄의 `cd`만 본인 경로로 변경한다.
