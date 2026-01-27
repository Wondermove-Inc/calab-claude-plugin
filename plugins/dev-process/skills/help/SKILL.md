---
name: workflow:help
description: Workflow 플러그인 도움말을 표시합니다. 모든 명령어와 사용 예시를 확인할 수 있습니다.
allowed-tools: Read
user-invocable: true
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

📌 개발 프로세스
───────────────────────────────────────────────────────────────
  /dev-process:process [기능]
      전체 프로세스 실행 (Plan → Design → Tasks → Build)
      옵션: --from=plan|design|tasks|build
      예시: /dev-process:process 사용자 인증 시스템

  /dev-process:process-plan [기능]
      브레인스토밍 + PRD 문서 생성
      옵션: --brainstorm, --prd
      예시: /dev-process:process-plan 사용자 인증 시스템

  /dev-process:process-design
      아키텍처 + ERD 설계
      옵션: --arch, --erd
      예시: /dev-process:process-design --arch

  /dev-process:process-tasks
      태스크 목록 자동 생성
      예시: /dev-process:process-tasks

  /dev-process:process-build [task-id]
      태스크 구현
      옵션: --tdd (테스트 주도 개발)
      예시: /dev-process:process-build TASK-001 --tdd

  /dev-process:process-status
      진행 상황 확인
      예시: /dev-process:process-status

📌 Worktree (작업 추적)
───────────────────────────────────────────────────────────────
  /dev-process:worktree
      작업 트리 시각화
      예시: /dev-process:worktree

  /dev-process:worktree status
      진행률 요약
      예시: /dev-process:worktree status

  /dev-process:worktree start [id]
      태스크 시작
      예시: /dev-process:worktree start TASK-001

  /dev-process:worktree done [id]
      태스크 완료
      예시: /dev-process:worktree done TASK-001

  /dev-process:worktree block [id] [사유]
      블로커 등록
      예시: /dev-process:worktree block TASK-002 "API 미완성"

📌 컨텍스트 관리
───────────────────────────────────────────────────────────────
  /dev-process:restore-context
      규칙 + 작업 상태 복원 (Compact 후 사용)
      예시: /dev-process:restore-context

  /dev-process:save-progress [메시지]
      체크포인트 저장
      예시: /dev-process:save-progress "로그인 기능 완료"

  /dev-process:show-rules
      전체 규칙 표시
      예시: /dev-process:show-rules

  /dev-process:context-show
      현재 컨텍스트 확인
      예시: /dev-process:context-show

  /dev-process:context-refresh
      컨텍스트 문서 갱신
      예시: /dev-process:context-refresh

📌 코드 품질
───────────────────────────────────────────────────────────────
  /dev-process:check-quality
      전체 프로젝트 품질 검사 (300줄 제한, 주석 검사)
      예시: /dev-process:check-quality

📌 JIRA 연동
───────────────────────────────────────────────────────────────
  /dev-process:jira-init [project-key]
      JIRA 연동 초기화
      예시: /dev-process:jira-init MYPROJ

  /dev-process:jira-push
      Worktree → JIRA 동기화
      예시: /dev-process:jira-push

  /dev-process:jira-pull
      JIRA → Worktree 동기화
      예시: /dev-process:jira-pull

  /dev-process:jira-sync
      양방향 동기화
      예시: /dev-process:jira-sync

  /dev-process:jira-link [task-id] [jira-key]
      수동 매핑
      예시: /dev-process:jira-link TASK-001 MYPROJ-123

  /dev-process:jira-status
      JIRA 연동 상태 확인
      예시: /dev-process:jira-status

📌 QA 테스트
───────────────────────────────────────────────────────────────
  /dev-process:qa
      QA 프로세스 시작
      옵션: --from-prd, --from-worktree
      예시: /dev-process:qa --from-prd

  /dev-process:qa-plan
      QA 계획서 생성
      옵션: --edit
      예시: /dev-process:qa-plan

  /dev-process:qa-run [tc-id]
      테스트 실행
      옵션: --all, --failed, --continue
      예시: /dev-process:qa-run --all

  /dev-process:qa-report
      테스트 결과 보고서
      옵션: --summary, --full
      예시: /dev-process:qa-report --full

  /dev-process:qa-status
      QA 진행률 확인
      예시: /dev-process:qa-status

🔄 자연어 사용 예시
───────────────────────────────────────────────────────────────
  "개발 시작해줘"      → /dev-process:process
  "기획해줘"           → /dev-process:process-plan
  "설계해줘"           → /dev-process:process-design
  "태스크 분해해줘"    → /dev-process:process-tasks
  "구현해줘"           → /dev-process:process-build
  "진행 상황 보여줘"   → /dev-process:process-status
  "컨텍스트 복원해줘"  → /dev-process:restore-context
  "QA 시작해줘"        → /dev-process:qa

🔗 관련 문서
───────────────────────────────────────────────────────────────
  • best-practices/ - 언어별 베스트 프랙티스 가이드
  • templates/ - PRD, Task 템플릿
  • README.md - 플러그인 상세 문서

📊 권장 워크플로우 순서
───────────────────────────────────────────────────────────────
  process-plan ──→ process-design ──→ process-tasks ──→ process-build
       │                │                  │                 │
       ▼                ▼                  ▼                 ▼
      PRD          Architecture          Tasks             Code

  또는 /dev-process:process 로 전체 프로세스 한번에 실행

💡 팁
───────────────────────────────────────────────────────────────
  • 위 순서대로 진행하면 체계적인 개발이 가능합니다
  • Compact 후에는 /dev-process:restore-context로 컨텍스트 복원
  • JIRA 연동 시 환경변수 설정 필요 (JIRA_EMAIL, JIRA_API_TOKEN)
  • 코드 작성 시 best-practices가 자동 적용됩니다
```

## 실행 방식

1. 위 형식의 도움말을 콘솔에 출력
2. 현재 작업 상태에 따라 다음 추천 명령어 안내
