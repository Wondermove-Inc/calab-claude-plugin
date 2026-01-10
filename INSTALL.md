# Calab Plugin 설치/제거 가이드

## 글로벌 vs 프로젝트 구조

```
┌─────────────────────────────────────────────────────────────┐
│  📁 글로벌 (~/.claude/)                                      │
│  → install-plugin.sh가 설치                                  │
│  → 모든 프로젝트에서 공유                                    │
├─────────────────────────────────────────────────────────────┤
│  ├── CLAUDE.md              # 마스터 지침                   │
│  ├── settings.json          # 훅 설정                       │
│  ├── hooks/                 # 자동 실행 훅                   │
│  ├── best-practices/        # 언어별 베스트 프랙티스          │
│  ├── templates/             # 문서 템플릿                    │
│  ├── agents/                # 서브에이전트                   │
│  ├── integrations/          # 외부 연동                     │
│  ├── memory/                # 메모리 템플릿                  │
│  ├── problem-solving/       # 문제 해결 방법론               │
│  └── calab-marketplace/     # 마켓플레이스                   │
│      └── plugins/calab-plugin/  # 전체 복사됨                │
│          ├── commands/          # 35개 슬래시 명령어          │
│          ├── skills/            # 11개 자동 스킬             │
│          └── .claude-plugin/                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📁 프로젝트별 (명령어 실행 시 자동 생성)                       │
│  → 각 프로젝트마다 독립적으로 생성                            │
│  → 글로벌 설치에 포함되지 않음                                │
├─────────────────────────────────────────────────────────────┤
│  프로젝트/                                                  │
│  ├── .claude-state/         # 런타임 상태 (자동)              │
│  │   ├── worktree.json, checkpoint.json, ...               │
│  │                                                         │
│  └── .claude/               # 프로젝트별 문서                 │
│      ├── docs/              # 기능 문서 (/dev-plan)           │
│      │   ├── active/        # 진행 중                       │
│      │   └── complete/      # 완료                          │
│      ├── project-context/   # 온보딩 (/onboard)              │
│      ├── research/          # 리서치 (/research)             │
│      └── problem-solving/   # 문제 해결 (/solve)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 설치

### Step 1: 글로벌 파일 설치 + 마켓플레이스 생성

```bash
./install-plugin.sh
```

**설치되는 항목 (글로벌):**

```
~/.claude/
├── CLAUDE.md              # 마스터 지침 (모든 프로젝트 적용)
├── settings.json          # 훅 설정 (이벤트 트리거)
├── hooks/                 # Python 훅 (자동 실행)
│   ├── session_start.py
│   ├── code_quality_validator.py
│   ├── track_changes.py
│   └── ...
├── best-practices/        # 15개 언어별 베스트 프랙티스
│   ├── python.md
│   ├── react.md
│   ├── go.md
│   └── ...
├── templates/             # 문서 템플릿
├── agents/                # 서브에이전트
├── integrations/          # JIRA 등 외부 연동
├── memory/                # 메모리 템플릿
├── problem-solving/       # 문제 해결 방법론
└── calab-marketplace/     # 마켓플레이스 (명령어/스킬 로드)
    └── plugins/
        └── calab-plugin/  # 전체 복사 (심볼릭 링크 아님)
            ├── commands/  # 35개 슬래시 명령어
            ├── skills/    # 11개 자동 활성화 스킬
            └── .claude-plugin/
```

### Step 2: Claude 플러그인 시스템에 등록 (최초 1회만)

> **중요**: 아래 명령어는 터미널이 아닌 **Claude Code 내부**에서 실행합니다.

```bash
# 마켓플레이스 추가 (Claude Code 내부에서)
/plugin marketplace add ~/.claude/calab-marketplace

# 플러그인 설치 (Claude Code 내부에서)
/plugin install calab-plugin@calab-marketplace --scope user
```

### Step 3: 설치 확인

```bash
# 플러그인 목록 확인 (Claude Code 내부에서)
/plugin list

# 명령어 테스트
/calab-plugin:onboard
```

---

## 제거

### 방법 1: 스크립트 사용

```bash
./uninstall-plugin.sh
```

스크립트가 다음을 수행합니다:
1. Claude 플러그인 시스템에서 제거 안내
2. `~/.claude/`에 설치된 파일 제거
3. 마켓플레이스 디렉토리 제거

### 방법 2: 수동 제거

```bash
# 1. 플러그인 언설치 (Claude Code 내부에서)
/plugin uninstall calab-plugin

# 2. 마켓플레이스 제거 (Claude Code 내부에서)
/plugin marketplace remove calab-marketplace
```

```bash
# 3. 글로벌 파일 제거 (터미널에서)
rm ~/.claude/CLAUDE.md
rm ~/.claude/settings.json
rm -rf ~/.claude/hooks/
rm -rf ~/.claude/best-practices/
rm -rf ~/.claude/templates/
rm -rf ~/.claude/agents/
rm -rf ~/.claude/integrations/
rm -rf ~/.claude/memory/
rm -rf ~/.claude/problem-solving/
rm -rf ~/.claude/calab-marketplace/

# 4. (선택) 프로젝트별 파일 제거
# rm -rf 프로젝트경로/.claude-state/   # 런타임 상태
# rm -rf 프로젝트경로/.claude/docs/    # 기능 문서
```

---

## 프로젝트별 파일 (자동 생성)

설치 후 각 프로젝트에서 작업하면 **자동으로 생성**됩니다:

```
프로젝트/
├── .claude-state/              # 런타임 상태 (.gitignore 권장)
│   ├── worktree.json           # 작업 트리 상태
│   ├── checkpoint.json         # 체크포인트
│   ├── recent_changes.json     # 최근 변경 이력
│   ├── prompt_history.json     # 프롬프트 히스토리
│   └── qa/                     # QA 런타임
│
└── .claude/                    # 프로젝트별 문서 (명령어 실행 시 생성)
    │
    ├── docs/                   # 기능별 문서 (/dev-plan 시 생성)
    │   ├── active/             # 진행 중인 기능
    │   │   └── {feature-name}/
    │   │       ├── 01-brainstorm.md
    │   │       ├── 02-prd.md
    │   │       ├── 03-architecture.md
    │   │       ├── 04-erd.md
    │   │       ├── 05-tasks.md
    │   │       └── qa/
    │   │
    │   └── complete/           # 완료된 기능 (자동 이동)
    │
    ├── project-context/        # 온보딩 문서 (/onboard 시 생성)
    │   ├── PROJECT_SUMMARY.md
    │   ├── ARCHITECTURE.md
    │   ├── CODE_PATTERNS.md
    │   ├── CONVENTIONS.md
    │   └── DOMAIN_KNOWLEDGE.md
    │
    ├── research/               # 리서치 결과 (/research 시 생성)
    │   └── {topic}/
    │       ├── report.md
    │       ├── summary.md
    │       └── sources.md
    │
    └── problem-solving/        # 문제 해결 보고서 (/solve 시 생성)
        ├── active/             # 진행 중인 문제
        │   └── {problem-id}/
        └── resolved/           # 해결된 문제
            └── {problem-id}/
                └── report.md
```

**권장: 프로젝트 `.gitignore`에 추가**

```gitignore
.claude-state/
```

---

## 사용법

```bash
# 프로젝트 분석
/calab-plugin:onboard

# 기획
/calab-plugin:dev-plan 사용자 인증

# 리서치
/calab-plugin:research OAuth 2.0

# 컨텍스트 복원 (세션 시작, Compact 후)
/calab-plugin:restore-context
```

상세: `CLAUDE.md`, `README.md`
