---
description: 프로젝트 분석 기반으로 전체 문서를 자동 생성합니다.
allowed-tools: Read, Write, Edit, Glob, Bash, Task
argument-hint: [--from-prd] [--from-context] [--sections <list>]
---

# /docs-generate - 전체 문서 자동 생성

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

프로젝트 분석 결과(PRD, 컨텍스트 문서)를 기반으로 문서 사이트의 모든 콘텐츠를 자동 생성합니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--from-prd` | PRD 문서 기반 생성 | false |
| `--from-context` | 컨텍스트 문서 기반 생성 | true |
| `--sections` | 생성할 섹션 지정 (쉼표 구분) | all |

## 사전 조건

1. `/docs init` 실행 완료 (docs-site 디렉토리 존재)
2. 다음 중 하나 이상 존재:
   - `.claude/memory/CURRENT_CONTEXT.md`
   - `.claude/docs/prd.md`
   - `.claude/context/` 디렉토리

## 실행 단계

### 1. 사전 조건 확인

```
에이전트를 사용하여 확인:
1. docs-site/ 디렉토리 존재 여부
2. 컨텍스트 문서 존재 여부
3. PRD 문서 존재 여부
```

### 2. 소스 문서 수집

다음 순서로 소스 수집 (에이전트 사용):

1. **PRD 우선** (`--from-prd` 옵션 시):
   - `.claude/docs/prd.md`
   - `.claude/docs/architecture.md`
   - `.claude/docs/erd.md`

2. **컨텍스트 기반** (기본):
   - `.claude/context/` 내 모든 문서
   - `.claude/memory/CURRENT_CONTEXT.md`
   - `.claude/memory/PROJECT_RULES.md`

3. **코드 분석**:
   - `package.json` 또는 프로젝트 설정 파일
   - README.md (있는 경우)
   - 주요 소스 파일 구조

### 3. 섹션별 문서 생성

각 섹션에 대해 에이전트를 병렬로 실행하여 생성:

#### 3.1 Intro (intro.md)

소스: PRD 개요, 프로젝트 설명
내용:
- 제품 한 줄 소개
- 주요 기능 3-5개
- 대상 사용자
- 빠른 시작 링크

#### 3.2 Getting Started

| 파일 | 소스 | 내용 |
|------|------|------|
| overview.md | PRD, 아키텍처 | 제품 개요, 구성 요소 |
| quickstart.md | 설치 가이드 | 5분 내 첫 실행 |
| installation.md | package.json, 환경설정 | 상세 설치 방법 |

#### 3.3 Concepts (핵심 개념)

| 파일 | 소스 | 내용 |
|------|------|------|
| architecture.md | 아키텍처 문서 | 시스템 구조 설명 |
| key-concepts.md | 도메인 문서 | 핵심 용어/개념 정의 |

#### 3.4 Tutorials

| 파일 | 소스 | 내용 |
|------|------|------|
| first-project.md | PRD 핵심 기능 | 단계별 첫 프로젝트 |

#### 3.5 Guides (How-to)

| 파일 | 소스 | 내용 |
|------|------|------|
| configuration.md | 설정 파일 분석 | 설정 방법 가이드 |

#### 3.6 API Reference

| 파일 | 소스 | 내용 |
|------|------|------|
| reference.md | 코드 분석, OpenAPI | API 레퍼런스 |

#### 3.7 Troubleshooting

| 파일 | 소스 | 내용 |
|------|------|------|
| common-issues.md | FAQ, 이슈 이력 | 자주 발생하는 문제 |

### 4. 문서 품질 검증

에이전트를 사용하여 검증:
- 링크 유효성
- 마크다운 문법
- 이미지 참조 확인
- 중복 내용 제거

### 5. 결과 리포트

```
============================================
 ✅ 문서 자동 생성 완료!
============================================

 생성된 문서:

 ├── intro.md ✅
 ├── getting-started/
 │   ├── overview.md ✅
 │   ├── quickstart.md ✅
 │   └── installation.md ✅
 ├── concepts/
 │   ├── architecture.md ✅
 │   └── key-concepts.md ✅
 ├── tutorials/
 │   └── first-project.md ✅
 ├── guides/
 │   └── configuration.md ✅
 ├── api/
 │   └── reference.md ⚠️ (수동 보완 필요)
 └── troubleshooting/
     └── common-issues.md ✅

 통계:
 - 총 10개 문서 생성
 - 예상 단어 수: ~5,000
 - 자동 생성률: 90%

 수동 보완 필요:
 - api/reference.md: OpenAPI 스펙 없음

 다음 단계:
 1. /docs preview  - 로컬에서 확인
 2. /docs status   - 완성도 체크
 3. 수동 보완 후 /docs build

============================================
```

## 문서 생성 템플릿

### Overview 템플릿

```markdown
---
sidebar_position: 1
---

# 개요

## [프로젝트명]이란?

[한 문단 설명]

## 주요 기능

### 기능 1: [이름]
[설명]

### 기능 2: [이름]
[설명]

## 시스템 구성

```mermaid
graph LR
    A[사용자] --> B[프론트엔드]
    B --> C[백엔드]
    C --> D[데이터베이스]
```

## 다음 단계

- [빠른 시작](/getting-started/quickstart)으로 바로 시작하기
- [핵심 개념](/concepts/key-concepts)으로 더 알아보기
```

### Quickstart 템플릿

```markdown
---
sidebar_position: 2
---

# 빠른 시작

:::info 소요 시간
이 가이드는 약 5분이 소요됩니다.
:::

## 사전 요구사항

- Node.js 18+
- npm 또는 yarn

## 1단계: 설치

```bash
npm install [패키지명]
```

## 2단계: 초기 설정

```bash
[설정 명령어]
```

## 3단계: 첫 실행

```bash
[실행 명령어]
```

## 결과 확인

[스크린샷 또는 예상 출력]

## 다음 단계

축하합니다! 🎉 첫 실행을 완료했습니다.

- [상세 설치 가이드](/getting-started/installation)
- [첫 프로젝트 튜토리얼](/tutorials/first-project)
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/onboard` | 프로젝트 분석 및 컨텍스트 생성 |
| `/dev plan` | PRD 작성 |
| `/docs add` | 개별 문서 추가 |

## 참조

- Diátaxis Framework: https://diataxis.fr/
- 좋은 문서 작성법: https://www.writethedocs.org/
