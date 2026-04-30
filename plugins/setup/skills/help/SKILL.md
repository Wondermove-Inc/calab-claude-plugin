---
name: setup:help
description: setup 플러그인 사용법을 안내합니다. 도구별 상세 가이드를 제공합니다.
allowed-tools: Read
disable-model-invocation: true
---

# /setup:help - 플러그인 도움말

## 사용법
- `/setup:help` - 지원 도구 목록 표시
- `/setup:help {도구명}` - 해당 도구의 상세 가이드

## 실행 방식

### 사용자 요청 분석
사용자 입력에서 도구명을 파악합니다:
- "statusline" 키워드 → statusline 상세 가이드 출력
- "beads" 또는 "bd" 키워드 → beads 상세 가이드 출력
- 키워드 없음 → 도구 목록 출력

---

## 도구 목록 (기본 출력)

사용자가 `/setup:help`만 입력한 경우 아래 내용을 **그대로** 출력합니다:

---
**[출력 시작]**

# setup 플러그인 (v1.1.0)

Claude Code 환경 설정 도구 모음입니다.

## 지원 도구

| 도구 | 설명 | 명령어 |
|------|------|--------|
| statusline | 터미널 상태바 설치/관리 | `/setup:statusline` |
| beads | 이슈 트래킹 도구 설치 (macOS) | `/setup:beads` |

## 도구별 상세 가이드

`/setup:help {도구명}`으로 상세 가이드를 확인하세요.

예시:
- `/setup:help statusline`
- `/setup:help beads`

**[출력 끝]**

---

---

## statusline 상세 가이드

사용자가 `/setup:help statusline`을 입력한 경우 아래 내용을 **그대로** 출력합니다:

---
**[출력 시작]**

# statusline 도구

Claude Code 터미널에 상태 정보를 표시하는 statusline을 설치하고 관리합니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| /setup:statusline | 플러그인 statusline 설치 |
| /setup:statusline 롤백 | 이전 설정으로 복원 |
| /setup:statusline rollback | 이전 설정으로 복원 |

## 사용 예시

[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
[Sonnet 4] ████░░░░░░ 40% | ➜ api-server git:(feature) ✗

## 표시 항목

| 항목 | 설명 |
|------|------|
| [Opus 4.5] | 현재 Claude 모델 |
| ██████░░░░ | 컨텍스트 사용량 게이지 |
| 60% | 컨텍스트 사용 백분율 |
| my-project | 현재 작업 디렉토리 |
| git:(main) | Git 브랜치명 |
| ✗ | 변경사항 있음 (빨간색) |

## 색상 규칙

- 녹색: 50% 미만 (안전)
- 노란색: 50-75% (주의)
- 빨간색: 75% 이상 (위험)

## 설치 동작

1. 기존 설정이 있으면 ~/.claude/backup/statusline_<timestamp>/에 백업
2. 플러그인의 statusline 스크립트 설치
3. settings.json 업데이트
4. Claude Code 재시작 필요

## 롤백 동작

1. 백업 목록에서 복원할 버전 선택
2. 현재 설정을 안전 백업 (pre_restore_<timestamp>)
3. 선택한 백업으로 복원

## 파일 위치

| 파일 | 설명 |
|------|------|
| ~/.claude/statusline-command.sh | Statusline 스크립트 |
| ~/.claude/settings.json | Claude Code 설정 |
| ~/.claude/backup/ | 백업 디렉토리 |

## 요구사항

- jq: JSON 파싱용
  - macOS: brew install jq
  - Ubuntu: sudo apt install jq
- bc: 계산용 (대부분 기본 설치됨)
  - Ubuntu: sudo apt install bc

**[출력 끝]**

---

---

## beads 상세 가이드

사용자가 `/setup:help beads`를 입력한 경우 아래 내용을 **그대로** 출력합니다:

---
**[출력 시작]**

# beads (bd) 도구

Claude Code용 경량 이슈 트래킹 도구입니다. 로컬 `.beads/` 디렉토리에 이슈를 저장합니다.

**기본 모드**: `--stealth` (로컬 전용, Git 동기화 없음)

## 명령어

| 명령어 | 설명 |
|--------|------|
| /setup:beads | Beads(bd) 설치 |
| /setup:beads 삭제 | Beads(bd) 삭제 |

## 주요 CLI 명령어

### 작업 찾기
| 명령어 | 설명 |
|--------|------|
| bd ready | 작업 가능한 이슈 (블로커 없음) |
| bd list --status=open | 열린 이슈 전체 |
| bd show <id> | 이슈 상세 보기 |

### 이슈 생성/수정
| 명령어 | 설명 |
|--------|------|
| bd create --title="제목" --type=task --priority=2 | 이슈 생성 |
| bd update <id> --status=in_progress | 작업 시작 |
| bd close <id> | 완료 |

### 의존성 및 상태
| 명령어 | 설명 |
|--------|------|
| bd init --stealth | stealth 모드로 초기화 (기본 권장) |
| bd dep add <issue> <depends-on> | 의존성 추가 |
| bd blocked | 차단된 이슈 보기 |
| bd stats | 프로젝트 통계 |
| bd sync | Git 동기화 (일반 모드만 해당) |

## 이슈 타입
- task: 일반 작업
- bug: 버그 수정
- feature: 새 기능

## 우선순위
- 0 (P0): Critical
- 1 (P1): High
- 2 (P2): Medium (기본값)
- 3 (P3): Low
- 4 (P4): Backlog

## 요구사항

- macOS 필수
- Homebrew 필수
  - 미설치 시: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

**[출력 끝]**

---
