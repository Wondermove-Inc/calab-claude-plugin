# CALab Claude Code Plugin Marketplace

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Private](https://img.shields.io/badge/Repo-Private-orange.svg)]()
[![Version](https://img.shields.io/badge/Version-3.0.0-blue.svg)]()

> Claude Code 플러그인 모음 - 반복 작업 자동화, 코드 품질 표준화 (사내 전용)

---

## 플러그인 목록

| 플러그인 | 설명 | 스킬 수 |
|----------|------|----------|
| **[workflow](plugins/workflow/)** | 멀티 에이전트 워크플로우 + 코딩 원칙 + 코드 리뷰/커밋 | 2개 + 8 에이전트 |
| **[toolkit](plugins/toolkit/)** | 리서치 및 문제 해결 | 6개 |
| **[setup](plugins/setup/)** | CLI 환경 설정 (statusline, beads) | 3개 |
| **[docs](plugins/docs/)** | 문서 콘텐츠 자동 생성 (Docusaurus) | 6개 |

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
/plugin install toolkit@calab-marketplace --scope user        # 리서치/문제해결
/plugin install setup@calab-marketplace --scope user          # CLI 설정
/plugin install docs@calab-marketplace --scope user           # 문서 생성
```

### 권장 설치 조합

| 용도 | 설치할 플러그인 |
|------|----------------|
| **Full** | workflow, toolkit, setup, docs |
| **Core** | workflow, toolkit |
| **Minimal** | workflow |

### 로컬 설치 (대안)

```bash
git clone git@github.com:Wondermove-Inc/calab-claude-plugin.git ~/workspace/calab-claude-plugin
cd ~/workspace/calab-claude-plugin && git checkout marketplace
/plugin marketplace add ~/workspace/calab-claude-plugin
/plugin install workflow@calab-marketplace --scope user
```

---

## 빠른 시작

| 상황 | 명령어 |
|------|--------|
| 새 기능 개발 | `/workflow:start [기능]` |
| 코드 리뷰 | `/toolkit:code-review` |
| 커밋 생성 | `/toolkit:code-commit` |
| 기술 조사 | `/toolkit:research [주제]` |
| 버그 원인 분석 | `/toolkit:solve [문제]` |

각 플러그인의 상세 사용법은 해당 플러그인의 README를 참조하세요.

---

## 프로젝트 구조

```
calab-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json      # 마켓플레이스 정의
├── plugins/
│   ├── workflow/              # 멀티 에이전트 + 코딩 원칙
│   ├── toolkit/              # 리서치 + 문제해결 + 리뷰/커밋
│   ├── setup/                # CLI 환경 설정
│   └── docs/                 # 문서 자동 생성
└── README.md
```

---

## 라이선스

MIT License - Wondermove CA Lab
