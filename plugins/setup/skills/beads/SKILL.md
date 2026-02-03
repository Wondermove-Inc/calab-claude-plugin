---
name: setup:beads
description: Beads(bd) 이슈 트래킹 도구 설치 및 관리. macOS 전용 (Homebrew 사용)
allowed-tools: Bash, Read, AskUserQuestion
---

# /setup:beads - Beads 설치 및 관리

## 설명
Beads(bd)는 Claude Code용 경량 이슈 트래킹 도구입니다. 로컬 `.beads/` 디렉토리에 이슈를 저장합니다.

**기본 모드**: `--stealth` (로컬 전용, Git 동기화 없음)

## 사용법
- `/setup:beads` - Beads(bd) 설치
- `/setup:beads 삭제` - Beads(bd) 삭제
- `/setup:beads uninstall` - Beads(bd) 삭제

## 실행 방식

### 사용자 요청 분석
사용자 입력에서 삭제 키워드가 있으면 **삭제 모드**, 그 외에는 **설치 모드**로 실행합니다.

#### 삭제 키워드
다음 키워드 중 하나가 포함되면 삭제 모드:
- 한글: "삭제", "제거", "언인스톨"
- 영문: "uninstall", "remove"

---

## 설치 모드 (기본)

### 1단계: 환경 확인
```bash
# macOS 확인
uname -s

# Homebrew 확인
which brew

# 기존 설치 확인
which bd
```

### 2단계: 설치 확인
사용자에게 설치 진행 여부를 확인합니다:
- macOS + Homebrew 필요
- steveyegge/beads tap에서 설치

### 3단계: 설치 실행
```bash
bash {PLUGIN_PATH}/scripts/setup-beads.sh install
```

### 4단계: 검증 및 완료
```bash
bd --version
```
설치 완료 후 기본 사용법을 안내합니다.

---

## 삭제 모드

### 1단계: 설치 확인
```bash
which bd
brew list bd 2>/dev/null
```

### 2단계: 삭제 확인
사용자에게 삭제 진행 여부를 확인합니다.

### 3단계: 삭제 실행
```bash
bash {PLUGIN_PATH}/scripts/setup-beads.sh uninstall
```

---

## 주요 명령어

### 작업 찾기
```bash
bd ready                          # 작업 가능한 이슈 (블로커 없음)
bd list --status=open             # 열린 이슈 전체
bd list --status=in_progress      # 진행 중인 작업
bd show <id>                      # 이슈 상세 보기
```

### 이슈 생성/수정
```bash
bd create --title="제목" --type=task --priority=2
# type: task, bug, feature
# priority: 0(critical) ~ 4(backlog)

bd update <id> --status=in_progress   # 작업 시작
bd close <id>                         # 완료
bd close <id1> <id2> <id3>            # 여러 개 한번에 완료
```

### 의존성 관리
```bash
bd dep add <issue> <depends-on>   # 의존성 추가
bd blocked                        # 차단된 이슈 보기
```

### 프로젝트 초기화
```bash
bd init --stealth                 # stealth 모드로 초기화 (기본 권장)
bd init                           # 일반 모드 (Git 동기화 사용)
```

### 상태 확인
```bash
bd stats                          # 프로젝트 통계
bd doctor                         # 문제 진단
```

### Git 동기화 (일반 모드만 해당)
```bash
bd sync                           # Git 원격과 동기화 (stealth 모드에서는 불필요)
```

---

## 요구사항

| 항목 | 필수 |
|------|------|
| macOS | 필수 |
| Homebrew | 필수 |

### Homebrew 미설치 시
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## 문제 해결

### "command not found: bd"
설치 후 터미널을 재시작하거나:
```bash
source ~/.zshrc  # 또는 ~/.bashrc
```

### Homebrew tap 오류
```bash
brew untap steveyegge/beads
brew tap steveyegge/beads
brew install bd
```
