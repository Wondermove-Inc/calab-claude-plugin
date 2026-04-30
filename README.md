# CALab Claude Code Plugin Marketplace

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Private](https://img.shields.io/badge/Repo-Private-orange.svg)]()

> Claude Code 플러그인 모음 - 반복 작업 자동화, 코드 품질 표준화 (사내 전용)

---

## 플러그인 목록

| 플러그인 | 설명 | 스킬 수 |
|----------|------|----------|
| **[workflow](plugins/workflow/)** | 멀티 에이전트 워크플로우 (Discovery → Build) | 4개 + 6 에이전트 |
| **[toolkit](plugins/toolkit/)** | 코드 리뷰/커밋, 이슈 관리, Jira 동기화 | 5개 |
| **[setup](plugins/setup/)** | CLI 환경 설정 (statusline, beads) | 3개 |
| **[cmux](plugins/cmux/)** | tmux 터미널 제어, 브라우저 자동화 | 3개 |

---

## 설치

> **Note**: 이 저장소는 Private입니다. GitHub 접근 권한이 필요합니다.

### 마켓플레이스 등록 (최초 1회)

```bash
/plugin marketplace add https://github.com/Wondermove-Inc/calab-claude-plugin.git#prometheus
```

### 플러그인 설치

```bash
/plugin install workflow@calab-marketplace --scope user  # 멀티 에이전트 워크플로우
/plugin install toolkit@calab-marketplace --scope user   # 코드 리뷰/커밋
/plugin install setup@calab-marketplace --scope user     # CLI 설정
/plugin install cmux@calab-marketplace --scope user      # 터미널 제어
```

### 권장 설치 조합

| 용도 | 설치할 플러그인 |
|------|----------------|
| **Full** | workflow, toolkit, setup, cmux |
| **Core** | workflow, toolkit |
| **Minimal** | workflow |

---

## 빠른 시작

| 상황 | 명령어 |
|------|--------|
| 버그 수정, 단일 모듈 | `/workflow:build [요청]` |
| 새 기능, 다중 모듈 (설계 필요) | `/workflow:discovery [요청]` → `/workflow:build bd-<epic>` |
| 코드 리뷰 | `/toolkit:code-review` |
| 커밋 생성 | `/toolkit:code-commit` |
| 이슈 생성 | `/toolkit:create-issue` |
| 환경 설정 | `/setup:help` |

각 플러그인의 상세 사용법은 해당 플러그인의 README를 참조하세요.

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json      # 마켓플레이스 정의
├── plugins/
│   ├── workflow/              # 멀티 에이전트 워크플로우
│   ├── toolkit/               # 코드 리뷰/커밋, 이슈 관리
│   ├── setup/                 # CLI 환경 설정
│   └── cmux/                  # 터미널 제어
├── CLAUDE.md
├── AGENTS.md
└── README.md
```

---

## 라이선스

MIT License - Wondermove CA Lab
