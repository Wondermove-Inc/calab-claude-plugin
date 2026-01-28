# Calab Claude Plugin

[![Version](https://img.shields.io/badge/version-2.5.0-blue.svg)](https://github.com/Wondermove-Inc/calab-claude-plugin)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)](https://claude.ai/code)

> **일관된 개발 품질을 보장하는** Claude Code 워크플로우 자동화 플러그인

---

## 왜 Calab Plugin인가?

| 문제 | Calab Plugin 해결책 |
|------|---------------------|
| 매번 다른 코드 품질 | 자동 품질 검사 + 베스트 프랙티스 강제 |
| 컨텍스트 유실 (Compact) | 자동 저장/복원으로 작업 연속성 보장 |
| 반복적인 보일러플레이트 | 클린 아키텍처 자동 생성 |
| 문서화 누락 | 코드 변경 시 자동 문서 동기화 |
| 할루시네이션 | validator/reinforcer 에이전트로 검증 |

---

## 한눈에 보기

```
┌─────────────────────────────────────────────────────────────┐
│  16개 명령어  │  7개 패시브 스킬  │  15개 에이전트  │  20개 훅  │
└─────────────────────────────────────────────────────────────┘
```

---

## 빠른 시작

### 1. 마켓플레이스 추가

```bash
# Claude Code 실행 후
/plugin marketplace add Wondermove-Inc/calab-claude-plugin
```

### 2. 플러그인 설치

```bash
# 브라우징으로 설치 (권장)
/plugin
# → Discover 탭에서 calab-plugin 선택

# 또는 직접 설치
/plugin install calab-plugin@calab-marketplace
```

### 3. 설치 확인

```bash
/plugins
# calab-plugin이 목록에 표시되어야 함
```

### 4. CLAUDE.md 적용 (선택)

글로벌 지침을 적용하려면 CLAUDE.md를 복사합니다:

```bash
# 설치된 플러그인에서 CLAUDE.md 복사
curl -o ~/.claude/CLAUDE.md https://raw.githubusercontent.com/Wondermove-Inc/calab-claude-plugin/main/plugins/calab-plugin/CLAUDE.md
```

### 5. 프로젝트 온보딩

```bash
/onboard
```

### 6. 개발 시작

```bash
/dev --plan 사용자 인증 시스템
```

---

## 명령어

### 메타커맨드 (8개)

하나의 명령어로 여러 서브 기능을 제어합니다.

| 명령어 | 옵션 | 설명 |
|--------|------|------|
| `/dev` | `--plan` `--design` `--tasks` `--build` `--status` | 개발 워크플로우 전체 관리 |
| `/clean` | `--init` `--entity` `--usecase` `--validate` | 클린 아키텍처 4-Layer 생성 |
| `/docs` | `--generate` `--add` `--update` `--validate` | 문서 자동 생성/동기화 |
| `/jira` | `--init` `--pull` `--push` `--link` `--sync` | JIRA 양방향 연동 |
| `/qa` | `--plan` `--run` `--report` `--status` | E2E/통합 테스트 관리 |
| `/solve` | `--5whys` `--rca` `--hypothesis` | 체계적 문제 해결 |
| `/onboard` | `--quick` `--phases` | 프로젝트 분석 및 컨텍스트 생성 |
| `/context` | `--show` `--refresh` | 프로젝트 컨텍스트 관리 |

### 독립 명령어 (8개)

| 명령어 | 설명 | 사용 예시 |
|--------|------|----------|
| `/security` | OWASP Top 10 보안 취약점 검사 | `/security` |
| `/quality` | 코드 품질 전체 검사 (500줄, 주석, 타입) | `/quality` |
| `/restore` | Compact 후 컨텍스트 복원 | `/restore` |
| `/save` | 작업 체크포인트 저장 | `/save "기능 구현 완료"` |
| `/rules` | 프로젝트 규칙 표시 | `/rules` |
| `/worktree` | 작업 트리 및 진행률 확인 | `/worktree status` |
| `/learn` | 특정 코드 영역 심층 학습 | `/learn src/components/` |
| `/research` | 웹 검색 + 핵심 요약 | `/research Next.js 15 변경사항` |

---

## 패시브 스킬 (7개)

코드 작성 시 **자동으로 활성화**되어 품질을 보장합니다.

| 스킬 | 트리거 | 효과 |
|------|--------|------|
| `best-practices` | React, TypeScript 등 기술 감지 | 해당 기술 베스트 프랙티스 자동 적용 |
| `code-quality` | 코드 생성/수정 시 | 500줄 제한, 함수 주석, 타입 강제 |
| `tdd-workflow` | `--tdd` 옵션 또는 테스트 키워드 | Red-Green-Refactor 강제 |
| `work-tracker` | 소스 파일 수정 시 | Worktree 자동 업데이트 |
| `project-rules` | 모든 코드 작성 시 | PROJECT_RULES.md 규칙 적용 |
| `e2e-runner` | E2E/Playwright 키워드 | 자동 테스트 실행 |
| `refactor-cleaner` | 리팩토링 요청 시 | 데드 코드 탐지 및 정리 |

---

## 에이전트 (15개)

특화된 작업을 수행하는 서브에이전트입니다.

### 워크플로우 에이전트

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `dev-workflow` | Plan → Design → Tasks → Build | `/dev` 실행 |
| `docs-generator` | 문서 자동 생성/업데이트 | `/docs` 실행 |
| `jira-connector` | JIRA 이슈 동기화 | `/jira` 실행 |
| `project-onboarder` | 프로젝트 분석 | `/onboard` 실행 |
| `deep-researcher` | 5-10회 검색 심층 리서치 | `/research` 실행 |

### 웹 리서치 에이전트

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `web-researcher` | Tavily MCP 기반 실시간 웹 검색/분석 | 검색, 조사, 최신 정보 요청 시 |

### 품질 에이전트

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `code-reviewer` | 코드 품질/스타일 검토 | 리뷰 요청 시 |
| `security-reviewer` | OWASP Top 10 검사 | 보안 검사 시 |
| `project-guardian` | 프로젝트 규칙 준수 검증 | 규칙 확인 시 |
| `build-error-resolver` | 빌드/타입 오류 해결 | 빌드 실패 시 |

### 검증/보강 에이전트

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `validator` | AC/완전성/엣지케이스 검증 | 구현 완료 후 **필수** |
| `reinforcer` | 검증 실패 항목 자동 수정 | validator 실패 시 |

### 자동화 에이전트

| 에이전트 | 역할 | 호출 조건 |
|----------|------|----------|
| `refactor-cleaner` | 데드 코드/미사용 import 정리 | 리팩토링 시 |
| `e2e-runner` | Playwright/Puppeteer 테스트 | E2E 테스트 시 |
| `doc-updater` | 코드 변경 감지 문서 업데이트 | 문서 동기화 시 |

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json       # 마켓플레이스 정의
│
├── README.md
│
└── plugins/
    └── calab-plugin/          # 플러그인 본체
        ├── .claude-plugin/
        │   └── plugin.json    # 플러그인 메타데이터
        │
        ├── CLAUDE.md          # Claude 지침 (핵심)
        │
        ├── skills/            # 23개 스킬
        │   ├── dev/          # 개발 워크플로우
        │   ├── clean/        # 클린 아키텍처
        │   ├── qa/           # QA 테스트
        │   ├── solve/        # 문제 해결
        │   ├── security/     # 보안 검사
        │   └── ...
        │
        ├── agents/            # 15개 에이전트
        │   ├── web-researcher.md
        │   ├── validator.md
        │   ├── reinforcer.md
        │   └── ...
        │
        └── hooks/             # 20개 훅 스크립트
```

---

## 워크플로우 예시

### 새 기능 개발

```bash
# 1. 기획
/dev --plan 사용자 인증 시스템

# 2. 설계
/dev --design

# 3. 태스크 분해
/dev --tasks

# 4. 구현 (태스크별)
/dev --build TASK-001
/dev --build TASK-002

# 5. QA
/qa --run

# 6. 보안 검사
/security
```

### 버그 수정

```bash
# 에러 메시지와 함께 실행
/solve TypeError: Cannot read property 'id' of undefined

# 또는 특정 방법론 선택
/solve --5whys      # 반복 문제
/solve --rca        # 시스템 문제
/solve --hypothesis # 불명확한 원인
```

### Compact 후 복구

```bash
# 이전 작업 컨텍스트 복원
/restore
```

---

## 설치 옵션

### 옵션 1: 마켓플레이스 설치 (권장)

```bash
# 1. 마켓플레이스 추가 (GitHub에서 자동 다운로드)
/plugin marketplace add Wondermove-Inc/calab-claude-plugin

# 2. 플러그인 설치
/plugin install calab-plugin@calab-marketplace

# 3. 설치 확인
/plugins
```

### 옵션 2: 인터랙티브 설치

```bash
# 플러그인 브라우저 열기
/plugin

# → "Add Marketplace" 선택
# → "Wondermove-Inc/calab-claude-plugin" 입력
# → "Discover" 탭에서 calab-plugin 선택하여 설치
```

### 옵션 3: 로컬 개발용

```bash
# 리포지토리 클론
git clone https://github.com/Wondermove-Inc/calab-claude-plugin.git

# 로컬 마켓플레이스로 추가
/plugin marketplace add /path/to/calab-claude-plugin
```

---

## 설정

### settings.json

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Write", "Edit"],
    "deny": []
  },
  "hooks": {
    "enabled": true
  }
}
```

### 필수 디렉토리

플러그인이 사용하는 디렉토리:

```
.claude/
├── memory/                # 컨텍스트 저장
│   ├── CURRENT_CONTEXT.md
│   └── PROJECT_RULES.md
├── project-context/       # 프로젝트 분석 결과
│   ├── PROJECT_SUMMARY.md
│   ├── CODE_PATTERNS.md
│   └── ARCHITECTURE.md
└── docs/                  # 생성된 문서
    ├── active/           # 진행 중 기능
    └── complete/         # 완료된 기능
```

---

## 요구사항

- **Claude Code CLI** v1.0.0 이상
- **Node.js** 18+ (일부 훅에서 사용)
- **Python** 3.8+ (일부 훅에서 사용)

---

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 라이선스

MIT License - [Wondermove CALab](https://wondermove.net)

---

## 문의

- **Issues**: [GitHub Issues](https://github.com/Wondermove-Inc/calab-claude-plugin/issues)
- **Email**: captain@wondermove.net
