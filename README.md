# CALab Claude Code Plugin Marketplace

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Private](https://img.shields.io/badge/Repo-Private-orange.svg)]()
[![Version](https://img.shields.io/badge/Version-2.5.0-blue.svg)]()

> Claude Code 플러그인 모음 - 반복 작업 자동화, 코드 품질 표준화 (사내 전용)

---

## 플러그인 목록

| 플러그인 | 설명 | 스킬 수 |
|----------|------|----------|
| **[dev-process](plugins/dev-process/)** | 개발 프로세스 + JIRA + QA 통합 | 33개 |
| **[onboarding](plugins/onboarding/)** | 프로젝트 분석 및 온보딩 자동화 | 7개 |
| **[architecture](plugins/architecture/)** | 클린 아키텍처 설계 및 검증 | 11개 |
| **[toolkit](plugins/toolkit/)** | 리서치 및 문제 해결 | 6개 |
| **[cli-tools](plugins/cli-tools/)** | CLI 환경 설정 (statusline) | 2개 |
| **[docs](plugins/docs/)** | 문서 콘텐츠 자동 생성 (Docusaurus) | 6개 |

---

## 설치

> **Note**: 이 저장소는 Private입니다. GitHub 접근 권한이 필요합니다.

### 마켓플레이스 등록 (최초 1회)

```bash
/plugin marketplace add https://github.com/Wondermove-Inc/calab-claude-plugin.git#marketplace
```

### 플러그인 설치

```bash
/plugin install dev-process@calab-marketplace --scope user   # 개발 프로세스
/plugin install onboarding@calab-marketplace --scope user    # 온보딩
/plugin install architecture@calab-marketplace --scope user  # 클린 아키텍처
/plugin install toolkit@calab-marketplace --scope user       # 리서치/문제해결
/plugin install cli-tools@calab-marketplace --scope user     # CLI 설정
/plugin install docs@calab-marketplace --scope user          # 문서 생성
```

### 권장 설치 조합

| 용도 | 설치할 플러그인 |
|------|----------------|
| **Full** | dev-process, onboarding, architecture, toolkit, cli-tools, docs |
| **Core** | dev-process, architecture, onboarding |
| **Minimal** | dev-process |

### 로컬 설치 (대안)

```bash
git clone git@github.com:Wondermove-Inc/calab-claude-plugin.git ~/workspace/calab-claude-plugin
cd ~/workspace/calab-claude-plugin && git checkout marketplace
/plugin marketplace add ~/workspace/calab-claude-plugin
/plugin install dev-process@calab-marketplace --scope user
```

---

## 빠른 시작

| 상황 | 명령어 |
|------|--------|
| 새 프로젝트 시작 | `/dev-process:process-plan [기능]` |
| 기존 프로젝트 투입 | `/onboarding:start` |
| 기술 조사 | `/toolkit:research [주제]` |
| 버그 원인 분석 | `/toolkit:solve [문제]` |
| 아키텍처 초기화 | `/architecture:clean-init` |
| QA 시작 | `/dev-process:qa` |

각 플러그인의 상세 사용법은 해당 플러그인의 README를 참조하세요.

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json      # 마켓플레이스 정의
├── plugins/
│   ├── dev-process/          # 개발 프로세스 + JIRA + QA
│   ├── onboarding/           # 프로젝트 온보딩
│   ├── architecture/         # 클린 아키텍처
│   ├── toolkit/              # 리서치 + 문제해결
│   ├── cli-tools/            # CLI 환경 설정
│   └── docs/                 # 문서 자동 생성
└── README.md
```

---

## 라이선스

MIT License - Wondermove CA Lab
