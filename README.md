# Calab Claude Plugin Marketplace

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Private](https://img.shields.io/badge/Repo-Private-orange.svg)]()
[![Version](https://img.shields.io/badge/Version-2.2.0-blue.svg)]()

> **어떤 상황에서든 동일한 개발 품질을 보장하는** Claude Code 플러그인 마켓플레이스 (사내 전용)

---

## 문제 해결 매트릭스

| 상황 | 문제점 | 솔루션 | 명령어 |
|------|--------|--------|--------|
| **새 프로젝트 시작** | 어떻게 시작할지 막막함 | 체계적 워크플로우 제공 | `/workflow:dev-plan` |
| **기존 프로젝트 투입** | 코드베이스 파악에 시간 소요 | 5개 컨텍스트 문서 자동 분석 | `/onboarding:onboard` |
| **기술 조사 필요** | 검색 + 요약 반복 작업 | 5-10회 자동 검색 + 핵심 요약 | `/toolkit:research` |
| **버그 발생** | 원인 파악 어려움 | 5 Whys, RCA 방법론 적용 | `/toolkit:solve` |
| **아키텍처 혼란** | 의존성 규칙 위반 | 클린 아키텍처 강제 | `/architecture:clean-init` |
| **QA 누락** | 수동 테스트 반복 | E2E 자동화 | `/workflow:qa` |
| **JIRA 수동 업데이트** | 중복 작업 | 양방향 자동 동기화 | `/workflow:jira-sync` |

---

## 플러그인 목록

| 플러그인 | 설명 | 명령어 수 |
|----------|------|----------|
| **[workflow](plugins/workflow/)** | 개발 워크플로우 + JIRA + QA 통합 | 23개 |
| **[onboarding](plugins/onboarding/)** | 프로젝트 분석 및 온보딩 자동화 | 5개 |
| **[architecture](plugins/architecture/)** | 클린 아키텍처 설계 및 검증 | 4개 |
| **[toolkit](plugins/toolkit/)** | 리서치 및 문제 해결 | 5개 |

---

## 설치

> **Note**: 이 저장소는 Private입니다. GitHub 접근 권한이 필요합니다.

### 플러그인 설치

```bash
# 1. 마켓플레이스 등록 (SSH - 최초 1회)
/plugin marketplace add https://github.com/Wondermove-Inc/calab-claude-plugin.git
# workflow 브랜치 등록
/plugin marketplace add https://github.com/Wondermove-Inc/calab-claude-plugin.git#workflow


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

SSH 설정이 어려운 경우:

```bash
# 1. 저장소 클론
git clone git@github.com:Wondermove-Inc/calab-claude-plugin.git ~/workspace/calab-claude-plugin

# 2. 로컬 경로로 마켓플레이스 등록
/plugin marketplace add ~/workspace/calab-claude-plugin

# 3. 플러그인 설치
/plugin install workflow@calab-marketplace --scope user
```

---

## 명령어 레퍼런스

### Workflow

```bash
# 개발 워크플로우
/workflow:dev-plan [기능]      # 기획 및 PRD 생성
/workflow:dev-design           # 아키텍처 설계
/workflow:dev-tasks            # 태스크 분해
/workflow:dev-build [task-id]  # 태스크 구현
/workflow:dev-status           # 진행 상황 확인

# JIRA 연동
/workflow:jira-init [key]      # JIRA 연동 초기화
/workflow:jira-sync            # 양방향 동기화

# QA 테스트
/workflow:qa                   # QA 프로세스 시작
/workflow:qa-plan              # QA 계획서 생성
/workflow:qa-run [tc-id]       # 테스트 실행
```

### Onboarding

```bash
/onboarding:onboard            # 전체 프로젝트 분석
/onboarding:onboard-quick      # 빠른 분석
/onboarding:learn [path]       # 특정 영역 학습
```

### Architecture

```bash
/architecture:clean-init       # 4-레이어 구조 초기화
/architecture:clean-entity     # 도메인 엔티티 생성
/architecture:clean-usecase    # 유스케이스 생성
/architecture:clean-validate   # 의존성 규칙 검증
```

### Toolkit

```bash
/toolkit:research [주제]       # 기본 리서치 (5회 검색)
/toolkit:research [주제] --deep # 심층 리서치 (10회)
/toolkit:solve [문제]          # 체계적 문제 분석
/toolkit:solve-report [id]     # 해결 보고서 생성
```

---

## 자동 적용 기능 (패시브 스킬)

코드 작성 시 **사용자 요청 없이** 자동으로 적용:

| 스킬 | 활성화 조건 | 제공 플러그인 |
|------|------------|--------------|
| `clean-architecture` | 코드 구현 시 | architecture |
| `best-practices` | 기술 감지 시 | workflow |
| `code-quality` | 코드 생성 시 | workflow |
| `problem-solving` | 에러/버그 언급 시 | toolkit |
| `research-skill` | 조사 요청 시 | toolkit |

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json         # 마켓플레이스 정의
├── plugins/
│   ├── workflow/                # 개발 워크플로우 + JIRA + QA
│   ├── onboarding/              # 프로젝트 온보딩
│   ├── architecture/            # 클린 아키텍처
│   └── toolkit/                 # 리서치 + 문제해결
└── README.md
```

---

## 버전 히스토리

### v2.2.0 (2026-01-19)

**모듈형 마켓플레이스 전환** - 단일 플러그인 → 4개 독립 플러그인

- **Breaking Change**: 설치 방식 변경
  - 기존: `/plugin install calab-plugin@calab-marketplace`
  - 변경: `/plugin install workflow@calab-marketplace` (플러그인별 개별 설치)
- **모듈화**: 4개 독립 플러그인으로 분리 (workflow, onboarding, architecture, toolkit)
- **문서 경로 통일**: 모든 생성 문서를 `.claude/` 하위로 통일
  - `memory/` → `.claude/memory/`
- **플러그인별 상세 README**: 각 플러그인에 상세 사용법, 예시, 다이어그램 추가
- **marketplace.json 스키마 준수**: 공식 Claude Code 스키마로 업데이트

### v2.1.0 (2026-01-10)

- 글로벌/프로젝트 경로 명확화
- 설치 안정성 개선: 심볼릭 링크 → 전체 복사
- 프로젝트별 폴더 완성: `project-context/`, `research/`, `problem-solving/`

### v2.0.0 (2026-01-02)

- 파일 복사 방식 → 공식 플러그인 시스템으로 전환
- 명령어 네임스페이스 자동 적용
- 마켓플레이스 기반 설치

### v1.x (deprecated)

- 파일 복사 방식 설치 (레거시)
- 직접 명령어 사용

---

## 라이선스

MIT License - Wondermove CA Lab
