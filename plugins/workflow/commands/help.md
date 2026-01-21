---
description: Workflow 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
---

# /help - Workflow 플러그인 도움말

## 설명
Workflow 플러그인의 모든 명령어와 사용 예시를 안내합니다.

## 출력 형식

```
╔════════════════════════════════════════════════════════╗
║           🔄 Workflow Plugin v2.3.0                    ║
║  Dev Workflow + JIRA Integration + QA Automation       ║
╚════════════════════════════════════════════════════════╝

📋 플러그인 개요
───────────────────────────────────────────────────────────────
  Plan → Design → Tasks → Build의 체계적인 개발 프로세스를
  제공합니다. JIRA 연동과 QA 테스트 자동화를 지원합니다.

📌 개발 워크플로우
───────────────────────────────────────────────────────────────
  /workflow:dev-plan [기능]
      브레인스토밍 + PRD 문서 생성
      옵션: --brainstorm, --prd
      예시: /workflow:dev-plan 사용자 인증 시스템

  /workflow:dev-design
      아키텍처 + ERD 설계
      옵션: --arch, --erd
      예시: /workflow:dev-design --arch

  /workflow:dev-tasks
      태스크 목록 자동 생성
      예시: /workflow:dev-tasks

  /workflow:dev-build [task-id]
      태스크 구현
      옵션: --tdd (테스트 주도 개발)
      예시: /workflow:dev-build TASK-001 --tdd

  /workflow:dev-status
      진행 상황 확인
      예시: /workflow:dev-status

📌 Worktree (작업 추적)
───────────────────────────────────────────────────────────────
  /workflow:worktree
      작업 트리 시각화
      예시: /workflow:worktree

  /workflow:worktree status
      진행률 요약
      예시: /workflow:worktree status

  /workflow:worktree start [id]
      태스크 시작
      예시: /workflow:worktree start TASK-001

  /workflow:worktree done [id]
      태스크 완료
      예시: /workflow:worktree done TASK-001

  /workflow:worktree block [id] [사유]
      블로커 등록
      예시: /workflow:worktree block TASK-002 "API 미완성"

📌 컨텍스트 관리
───────────────────────────────────────────────────────────────
  /workflow:restore-context
      규칙 + 작업 상태 복원 (Compact 후 사용)
      예시: /workflow:restore-context

  /workflow:save-progress [메시지]
      체크포인트 저장
      예시: /workflow:save-progress "로그인 기능 완료"

  /workflow:show-rules
      전체 규칙 표시
      예시: /workflow:show-rules

  /workflow:context-show
      현재 컨텍스트 확인
      예시: /workflow:context-show

  /workflow:context-refresh
      컨텍스트 문서 갱신
      예시: /workflow:context-refresh

📌 코드 품질
───────────────────────────────────────────────────────────────
  /workflow:check-quality
      전체 프로젝트 품질 검사 (300줄 제한, 주석 검사)
      예시: /workflow:check-quality

📌 JIRA 연동
───────────────────────────────────────────────────────────────
  /workflow:jira-init [project-key]
      JIRA 연동 초기화
      예시: /workflow:jira-init MYPROJ

  /workflow:jira-push
      Worktree → JIRA 동기화
      예시: /workflow:jira-push

  /workflow:jira-pull
      JIRA → Worktree 동기화
      예시: /workflow:jira-pull

  /workflow:jira-sync
      양방향 동기화
      예시: /workflow:jira-sync

  /workflow:jira-link [task-id] [jira-key]
      수동 매핑
      예시: /workflow:jira-link TASK-001 MYPROJ-123

  /workflow:jira-status
      JIRA 연동 상태 확인
      예시: /workflow:jira-status

📌 QA 테스트
───────────────────────────────────────────────────────────────
  /workflow:qa
      QA 프로세스 시작
      옵션: --from-prd, --from-worktree
      예시: /workflow:qa --from-prd

  /workflow:qa-plan
      QA 계획서 생성
      옵션: --edit
      예시: /workflow:qa-plan

  /workflow:qa-run [tc-id]
      테스트 실행
      옵션: --all, --failed, --continue
      예시: /workflow:qa-run --all

  /workflow:qa-report
      테스트 결과 보고서
      옵션: --summary, --full
      예시: /workflow:qa-report --full

  /workflow:qa-status
      QA 진행률 확인
      예시: /workflow:qa-status

🔄 자연어 사용 예시
───────────────────────────────────────────────────────────────
  "기획해줘"           → /workflow:dev-plan
  "설계해줘"           → /workflow:dev-design
  "태스크 분해해줘"    → /workflow:dev-tasks
  "구현해줘"           → /workflow:dev-build
  "진행 상황 보여줘"   → /workflow:dev-status
  "컨텍스트 복원해줘"  → /workflow:restore-context
  "QA 시작해줘"        → /workflow:qa

🔗 관련 문서
───────────────────────────────────────────────────────────────
  • best-practices/ - 언어별 베스트 프랙티스 가이드
  • templates/ - PRD, Task 템플릿
  • README.md - 플러그인 상세 문서

📊 권장 워크플로우 순서
───────────────────────────────────────────────────────────────
  dev-plan ──→ dev-design ──→ dev-tasks ──→ dev-build
      │             │              │              │
      ▼             ▼              ▼              ▼
    PRD        Architecture      Tasks          Code

💡 팁
───────────────────────────────────────────────────────────────
  • 위 순서대로 진행하면 체계적인 개발이 가능합니다
  • Compact 후에는 /workflow:restore-context로 컨텍스트 복원
  • JIRA 연동 시 환경변수 설정 필요 (JIRA_EMAIL, JIRA_API_TOKEN)
  • 코드 작성 시 best-practices가 자동 적용됩니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 현재 작업 상태에 따라 다음 추천 명령어 안내
