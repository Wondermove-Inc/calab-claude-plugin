# cli-tools 플러그인

> Claude Code CLI 환경 설정 도구 모음

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/cli-tools:statusline` | Statusline 설정 및 설치 |
| `/cli-tools:beads` | Beads(bd) 설치 가이드 |
| `/cli-tools:help` | 플러그인 도움말 |

## 도구 목록

### 1. Statusline

터미널 프롬프트에 유용한 정보를 표시합니다.

```bash
# 설치/업데이트
bash scripts/setup-statusline.sh install

# 삭제
bash scripts/setup-statusline.sh uninstall
```

**표시 정보:**
- 현재 Claude 모델명 (Opus, Sonnet, Haiku)
- 컨텍스트 윈도우 사용량 (진행바)
- API 사용량 (5시간 리밋 %, 리셋 시간)
- 현재 작업 디렉토리
- Git 브랜치

**표시 예시:**
```
Opus 4.5 | ▓▓▓▓░░░░░░ | 32% (Rst:2h15m) | my-project |  main
```

### 2. Beads (bd)

Claude Code용 이슈 트래킹 도구입니다. 기본적으로 `--stealth` 모드(로컬 전용)를 사용합니다.

```bash
# 설치
bash scripts/setup-beads.sh install

# 삭제
bash scripts/setup-beads.sh uninstall
```

**요구사항:** macOS + Homebrew

**주요 명령어:**
```bash
bd init --stealth     # 프로젝트 초기화 (stealth 모드)
bd ready              # 작업 가능한 이슈 조회
bd create "제목"      # 이슈 생성
bd update <id> --status in_progress  # 작업 시작
bd close <id>         # 작업 완료
```

## 요구사항

- **Statusline**: `jq`
- **Beads**: macOS, Homebrew

## 플러그인 구조

```
plugins/cli-tools/
├── .claude-plugin/
│   └── plugin.json
├── scripts/
│   ├── setup-statusline.sh
│   ├── statusline-command.sh
│   └── setup-beads.sh
├── skills/
│   ├── statusline/SKILL.md
│   └── help/SKILL.md
└── README.md
```
