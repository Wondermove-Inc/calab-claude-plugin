# Calab Claude Plugin Marketplace

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Private](https://img.shields.io/badge/Repo-Private-orange.svg)]()

> **어떤 상황에서든 동일한 개발 품질을 보장하는** Claude Code 플러그인 마켓플레이스 (사내 전용)

---

## Breaking Changes (v4.0)

**v4.0에서 플러그인 통합이 이루어졌습니다:**

| 항목 | v3.x (Old) | v4.0 (Current) |
|------|-----------|----------------|
| 플러그인 수 | 7개 | 4개 |
| jira, test | 별도 플러그인 | workflow에 통합 |
| research, solver | 별도 플러그인 | toolkit에 통합 |
| 네임스페이스 | `/jira:*`, `/test:*`, `/research:*`, `/solver:*` | `/workflow:*`, `/toolkit:*` |

---

## 플러그인 목록

| 플러그인 | 네임스페이스 | 설명 | 명령어 수 |
|----------|-------------|------|----------|
| **[workflow](plugins/workflow/)** | `/workflow:*` | 개발 워크플로우 + JIRA + QA 통합 | 23개 |
| **[onboarding](plugins/onboarding/)** | `/onboarding:*` | 프로젝트 분석 및 온보딩 자동화 | 5개 |
| **[architecture](plugins/architecture/)** | `/architecture:*` | 클린 아키텍처 설계 및 검증 | 4개 |
| **[toolkit](plugins/toolkit/)** | `/toolkit:*` | 리서치 및 문제 해결 | 5개 |

---

## 설치

> **Note**: 이 저장소는 Private입니다. 설치 전 GitHub 접근 권한이 필요합니다.

### 사전 준비

```bash
# SSH 키가 GitHub에 등록되어 있어야 합니다
ssh -T git@github.com
# "Hi username!" 메시지가 나오면 준비 완료
```

### 플러그인 설치

```bash
# 1. 마켓플레이스 등록 (SSH - 최초 1회)
/plugin marketplace add git@github.com:Wondermove-Inc/calab-claude-plugin.git

# 2. 원하는 플러그인 설치
/plugin install workflow@calab-marketplace --scope user      # 개발 워크플로우 + JIRA + QA
/plugin install onboarding@calab-marketplace --scope user    # 프로젝트 온보딩
/plugin install architecture@calab-marketplace --scope user  # 클린 아키텍처
/plugin install toolkit@calab-marketplace --scope user       # 리서치 + 문제해결
```

### 권장 설치 조합

| 용도 | 설치할 플러그인 |
|------|----------------|
| **Full** (모든 기능) | workflow, onboarding, architecture, toolkit |
| **Core** (핵심 개발) | workflow, architecture |
| **Minimal** (최소 구성) | workflow |

### 로컬 설치 (대안)

SSH 설정이 어려운 경우 로컬 클론 후 설치:

```bash
# 1. 저장소 클론
git clone git@github.com:Wondermove-Inc/calab-claude-plugin.git ~/workspace/calab-claude-plugin

# 2. 로컬 경로로 마켓플레이스 등록 (클론한 경로 사용)
/plugin marketplace add ~/workspace/calab-claude-plugin

# 3. 플러그인 설치
/plugin install workflow@calab-marketplace --scope user
```

### 훅 설정

v4.0에서 훅은 workflow 플러그인에 통합되었습니다:

| 플러그인 | 훅 파일 | 기능 |
|----------|---------|------|
| workflow | `plugins/workflow/settings.json` | 세션 관리, 코드 품질, 변경 추적, JIRA 동기화 |

**설치 방법** (프로젝트별):

```bash
# 방법 1: 플러그인 개발 프로젝트에서 직접 사용 (이미 적용됨)
# settings.json이 프로젝트 루트에 있으면 자동 적용

# 방법 2: 다른 프로젝트에서 사용 (클론한 경로로 대체)
cp ~/workspace/calab-claude-plugin/plugins/workflow/settings.json ~/.claude/
```

> **Note**: `${PLUGIN_DIR}` 변수는 플러그인 설치 경로로 자동 치환됩니다.

---

## 빠른 시작

### 상황별 명령어

| 상황 | 자연어 | 명령어 |
|------|--------|--------|
| **새 프로젝트 시작** | "사용자 인증 시스템 기획해줘" | `/workflow:dev-plan 사용자 인증` |
| **기존 프로젝트 투입** | "이 프로젝트 분석해줘" | `/onboarding:onboard` |
| **아키텍처 설계** | "클린 아키텍처 만들어줘" | `/architecture:clean-init` |
| **QA 테스트** | "QA 테스트 시작해줘" | `/workflow:qa` |
| **버그 해결** | "로그인 에러 해결해줘" | `/toolkit:solve 로그인 에러` |
| **기술 조사** | "OAuth 조사해줘" | `/toolkit:research OAuth` |
| **JIRA 동기화** | "JIRA 동기화해줘" | `/workflow:jira-sync` |

---

## 플러그인별 명령어

### Workflow (개발 워크플로우 + JIRA + QA)

```bash
# 개발 워크플로우
/workflow:dev-plan [기능]      # 기획 및 PRD 생성
/workflow:dev-design           # 아키텍처 설계
/workflow:dev-tasks            # 태스크 분해
/workflow:dev-build [task-id]  # 태스크 구현
/workflow:dev-status           # 진행 상황 확인
/workflow:worktree             # 작업 트리 관리
/workflow:restore-context      # 컨텍스트 복원
/workflow:save-progress        # 진행 상황 저장
/workflow:show-rules           # 프로젝트 규칙 표시
/workflow:check-quality        # 코드 품질 검사
/workflow:context-refresh      # 컨텍스트 갱신
/workflow:context-show         # 현재 컨텍스트 표시

# JIRA 연동
/workflow:jira-init [key]      # JIRA 연동 초기화
/workflow:jira-push            # Worktree → JIRA
/workflow:jira-pull            # JIRA → Worktree
/workflow:jira-sync            # 양방향 동기화
/workflow:jira-link [id] [key] # 수동 매핑
/workflow:jira-status          # 상태 확인

# QA 테스트
/workflow:qa                   # QA 프로세스 시작
/workflow:qa-plan              # QA 계획서 생성
/workflow:qa-run [tc-id]       # 테스트 실행
/workflow:qa-report            # 테스트 결과 보고서
/workflow:qa-status            # 진행률 확인
```

### Onboarding (프로젝트 온보딩)

```bash
/onboarding:onboard            # 전체 프로젝트 분석
/onboarding:onboard-quick      # 빠른 분석
/onboarding:learn [path]       # 특정 영역 학습
/onboarding:context-refresh    # 컨텍스트 갱신
/onboarding:context-show       # 컨텍스트 표시
```

### Architecture (클린 아키텍처)

```bash
/architecture:clean-init       # 4-레이어 구조 초기화
/architecture:clean-entity     # 도메인 엔티티 생성
/architecture:clean-usecase    # 유스케이스 생성
/architecture:clean-validate   # 의존성 규칙 검증
```

### Toolkit (리서치 및 문제 해결)

```bash
# 리서치
/toolkit:research [주제]             # 기본 리서치 (5회 검색)
/toolkit:research [주제] --quick     # 빠른 리서치 (3회)
/toolkit:research [주제] --deep      # 심층 리서치 (10회)

# 문제 해결
/toolkit:solve [문제]          # 체계적 문제 분석
/toolkit:solve-log             # 분석 진행 상황
/toolkit:solve-history         # 과거 사례 검색
/toolkit:solve-report [id]     # 해결 보고서 생성
```

---

## 자동 적용 기능 (패시브 스킬)

코드 작성 시 **사용자 요청 없이** 자동으로 적용되는 기능:

| 스킬 | 활성화 조건 | 제공 플러그인 |
|------|------------|--------------|
| `clean-architecture` | 코드 구현 시 | architecture |
| `best-practices` | 기술 감지 시 | workflow |
| `code-quality` | 코드 생성 시 | workflow |
| `work-tracker` | 소스 코드 수정 시 | workflow |
| `jira-integration` | JIRA 언급 시 | workflow |
| `qa-testing` | QA/테스트 언급 시 | workflow |
| `problem-solving` | 에러/버그 언급 시 | toolkit |
| `research-skill` | 조사 요청 시 | toolkit |

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   ├── plugin.json              # 레거시 단일 플러그인
│   └── marketplace.json         # 마켓플레이스 정의
│
├── plugins/                     # 4개 플러그인
│   ├── workflow/                # 23개 명령어 (jira, qa 통합)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/            # 23개 명령어
│   │   ├── skills/              # 7개 스킬
│   │   ├── hooks/               # 9개 훅
│   │   ├── best-practices/      # 11개 언어별 가이드
│   │   ├── templates/           # PRD, Task, QA
│   │   ├── memory/              # 컨텍스트, 규칙
│   │   ├── agents/              # 서브에이전트
│   │   └── integrations/        # JIRA 연동
│   │
│   ├── onboarding/              # 5개 명령어
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/
│   │   ├── skills/
│   │   └── best-practices/
│   │
│   ├── architecture/            # 4개 명령어
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/
│   │   ├── skills/
│   │   ├── best-practices/
│   │   └── templates/
│   │
│   └── toolkit/                 # 5개 명령어 (research, solver 통합)
│       ├── .claude-plugin/plugin.json
│       ├── commands/
│       ├── skills/
│       ├── knowledge-base/
│       └── templates/
│
├── README.md                    # 이 문서
└── settings.json                # 훅 설정
```

---

## 버전 히스토리

### v4.0 (2026-01-19)
- **플러그인 통합**: 7개 → 4개로 단순화
- **workflow 강화**: jira, test 플러그인 통합 (23개 명령어)
- **toolkit 신설**: research, solver 플러그인 통합 (5개 명령어)
- **훅 통합**: 모든 훅을 workflow에서 관리

### v3.0 (2026-01-15)
- **마켓플레이스 구조 전환**: 7개 개별 플러그인으로 분리
- **선택적 설치**: 필요한 플러그인만 설치 가능
- **번들 지원**: Full, Core, Minimal 번들 제공
- **네임스페이스 분리**: `/workflow:`, `/test:` 등 플러그인별 네임스페이스

### v2.2 (2026-01-14)
- **설치 간소화**: Claude Code 내부에서 2줄로 설치
- **구조 단순화**: `.claude/` 하위 폴더들을 루트로 이동
- **hooks 경로 변경**: `$HOME/.claude/hooks/`

### v2.0 (2026-01-02)
- 공식 플러그인 시스템 전환
- 마켓플레이스 기반 설치
- 명령어 네임스페이스 도입

---

## 마켓플레이스 등록 방법

이 플러그인을 Claude Code 공식 마켓플레이스 생태계에 등록하는 방법입니다.

### 1. 마켓플레이스 구조

마켓플레이스는 `.claude-plugin/marketplace.json` 파일이 있는 Git 저장소입니다:

```
your-marketplace/
├── .claude-plugin/
│   └── marketplace.json    # 마켓플레이스 정의 (필수)
└── plugins/
    └── your-plugin/
        └── .claude-plugin/
            └── plugin.json # 플러그인 정의
```

### 2. marketplace.json 스키마

```json
{
  "name": "your-marketplace",           // 마켓플레이스 식별자 (kebab-case)
  "owner": {
    "name": "Your Name",                // 필수
    "email": "your@email.com"           // 선택
  },
  "metadata": {
    "description": "마켓플레이스 설명",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",            // 필수: 플러그인 이름
      "source": "./plugins/plugin-name", // 필수: 플러그인 경로
      "description": "플러그인 설명",
      "version": "1.0.0",
      "category": "development",
      "tags": ["workflow", "automation"]
    }
  ]
}
```

### 3. GitHub에 배포

```bash
# GitHub 저장소 생성 및 푸시 (예시)
git init
git add .
git commit -m "Initial marketplace"
git remote add origin https://github.com/<your-org>/<your-marketplace>.git
git push -u origin main
```

### 4. 사용자 설치 방법

```bash
# 마켓플레이스 추가 (GitHub)
/plugin marketplace add your-org/your-marketplace

# 플러그인 설치
/plugin install plugin-name@your-marketplace
```

**이 마켓플레이스 설치 예시:**

```bash
# Calab 마켓플레이스 추가 (Private - SSH 필요)
/plugin marketplace add git@github.com:Wondermove-Inc/calab-claude-plugin.git

# 플러그인 설치
/plugin install workflow@calab-marketplace --scope user
```

### 5. Public vs Private 저장소

| 항목 | Public | Private |
|------|--------|---------|
| 마켓플레이스 등록 | `owner/repo` 형식 | SSH URL 필요 |
| claudemarketplaces.com 자동 검색 | ✓ 자동 등록 | ✗ 불가능 |
| 팀 외부 공유 | ✓ 가능 | ✗ 불가능 |
| 접근 권한 | 불필요 | GitHub 권한 필요 |

**Public 저장소인 경우** [claudemarketplaces.com](https://claudemarketplaces.com)에서 자동 검색됩니다:
- 별도 제출 불필요 - 24시간 내 자동 발견
- 매일 업데이트 - 스타 수, 메타데이터 자동 갱신

### 6. 플러그인 소스 유형

| 소스 유형 | 예시 | 설명 |
|----------|------|------|
| 상대 경로 | `./plugins/my-plugin` | 같은 저장소 내 플러그인 |
| GitHub | `owner/repo` | GitHub 저장소 |
| GitHub 하위 경로 | `owner/repo:path/to/plugin` | 저장소 내 특정 경로 |
| Git URL | `https://github.com/owner/repo.git` | 일반 Git URL |

### 7. 로컬 테스트

```bash
# 로컬 마켓플레이스 테스트
/plugin marketplace add /path/to/local/marketplace

# 플러그인 설치 테스트
/plugin install plugin-name@your-marketplace

# 설치 확인
/plugin list
```

### 참고 문서

- [공식 문서: 플러그인 마켓플레이스 생성](https://code.claude.com/docs/en/plugin-marketplaces)
- [공식 문서: 플러그인 발견 및 설치](https://code.claude.com/docs/en/discover-plugins)
- [Claude Code 마켓플레이스 디렉토리](https://claudemarketplaces.com)

---

## 라이선스

MIT License - wondermove CA Lab
