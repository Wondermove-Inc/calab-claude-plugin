# Workflow Plugin

개발 워크플로우 자동화 (Plan → Design → Tasks → Build)

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/dev-plan` | 기능 기획 및 PRD 생성 |
| `/dev-design` | 아키텍처 설계 |
| `/dev-tasks` | 태스크 분해 |
| `/dev-build` | 태스크 구현 |
| `/dev-status` | 진행 상황 확인 |
| `/worktree` | 작업 트리 관리 |
| `/restore-context` | 컨텍스트 복원 |
| `/save-progress` | 진행 상황 저장 |
| `/show-rules` | 프로젝트 규칙 표시 |
| `/check-quality` | 코드 품질 검사 |
| `/context-refresh` | 컨텍스트 갱신 |
| `/context-show` | 현재 컨텍스트 표시 |

## 스킬

- `dev-workflow`: 개발 워크플로우 가이드
- `work-tracker`: 작업 추적
- `project-rules`: 프로젝트 규칙 관리
- `code-quality`: 코드 품질 검증
- `best-practices`: 언어별 베스트 프랙티스

## 훅

- `code_quality_validator`: 코드 품질 자동 검사
- `track_changes`: 변경 사항 추적
- `session_start/end`: 세션 관리
- `pre_compact`: 컴팩트 전 처리
- `notification_handler`: 알림 처리
- `subagent_tracker`: 서브에이전트 추적

## 포함 리소스

- **best-practices/**: Go, Java, Node.js, Python, React, Rust, Tailwind, TypeScript, Next.js
- **templates/**: PRD, Task
- **memory/**: 프로젝트 규칙, 컨텍스트, 작업 히스토리
- **agents/**: 코드 리뷰어, 프로젝트 가디언
