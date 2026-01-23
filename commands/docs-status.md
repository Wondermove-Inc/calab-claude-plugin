---
description: 문서 현황 및 완성도를 확인합니다.
allowed-tools: Read, Glob, Task
argument-hint: [--verbose]
---

# /docs-status - 문서 현황 확인

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

문서 사이트의 현재 상태와 완성도를 분석하여 리포트합니다.
누락된 문서, 미완성 섹션, 품질 이슈를 파악합니다.

## 옵션

| 옵션 | 설명 |
|------|------|
| `--verbose` | 상세 분석 결과 출력 |

## 실행 단계

### 1. 문서 구조 스캔

에이전트를 사용하여 `docs-site/docs/` 디렉토리 구조 분석:

```
스캔 항목:
- 디렉토리별 파일 목록
- 각 파일 크기 및 수정일
- _category_.json 존재 여부
```

### 2. 문서 완성도 분석

각 문서 파일에 대해:

| 체크 항목 | 기준 |
|-----------|------|
| 최소 길이 | 500자 이상 |
| 제목 존재 | H1 헤더 필수 |
| 코드 예제 | 기술 문서는 코드 블록 필요 |
| 링크 유효성 | 내부 링크 확인 |
| 이미지 | 참조된 이미지 존재 여부 |
| 메타데이터 | frontmatter 완성도 |

### 3. 섹션별 상태 집계

```
섹션 상태:
- ✅ 완성: 모든 체크 항목 통과
- ⚠️ 미완성: 일부 체크 항목 미통과
- ❌ 누락: 필수 문서 없음
- 📝 초안: 템플릿만 존재
```

### 4. 결과 리포트 출력

```
============================================
 📊 문서 사이트 현황
============================================

 📁 구조 분석

 docs/
 ├── intro.md ✅ (1,234자)
 ├── getting-started/
 │   ├── overview.md ✅ (2,100자)
 │   ├── quickstart.md ⚠️ (코드 예제 부족)
 │   └── installation.md ✅ (1,800자)
 ├── concepts/
 │   ├── architecture.md ✅ (3,200자)
 │   └── key-concepts.md 📝 (템플릿만)
 ├── tutorials/
 │   └── first-project.md ⚠️ (500자 미만)
 ├── guides/
 │   └── configuration.md ✅ (1,500자)
 ├── api/
 │   └── reference.md ❌ (파일 없음)
 └── troubleshooting/
     └── common-issues.md 📝 (템플릿만)

 📈 완성도 통계

 ┌─────────────────┬────────┬─────────┐
 │ 섹션            │ 상태   │ 완성도  │
 ├─────────────────┼────────┼─────────┤
 │ Getting Started │ ⚠️     │ 75%     │
 │ Concepts        │ ⚠️     │ 50%     │
 │ Tutorials       │ ⚠️     │ 40%     │
 │ Guides          │ ✅     │ 100%    │
 │ API Reference   │ ❌     │ 0%      │
 │ Troubleshooting │ 📝     │ 10%     │
 └─────────────────┴────────┴─────────┘

 전체 완성도: 58% ████████░░░░░░░░

 🔧 권장 작업

 1. [높음] api/reference.md 생성 필요
    /docs add api

 2. [높음] tutorials/first-project.md 보강
    최소 500자 이상 작성

 3. [중간] quickstart.md 코드 예제 추가
    설치/실행 코드 블록 필요

 4. [낮음] key-concepts.md 내용 작성
    템플릿 채우기

============================================
```

## --verbose 옵션 추가 출력

```
============================================
 📋 상세 분석 결과
============================================

 🔗 링크 검사

 유효한 내부 링크: 15개
 깨진 링크: 2개
   - /docs/concepts/missing.md (tutorials/first-project.md:25)
   - /docs/api/endpoints.md (guides/configuration.md:42)

 🖼️ 이미지 검사

 총 이미지 참조: 5개
 존재하는 이미지: 3개
 누락된 이미지: 2개
   - /img/architecture.png
   - /img/flow-diagram.svg

 📝 Frontmatter 검사

 완전한 frontmatter: 7개
 불완전한 frontmatter: 3개
   - tutorials/first-project.md (sidebar_position 누락)
   - concepts/key-concepts.md (description 누락)

 📊 단어 수 분포

 ┌────────────────────────┬───────────┐
 │ 파일                   │ 단어 수   │
 ├────────────────────────┼───────────┤
 │ architecture.md        │ 850       │
 │ overview.md            │ 560       │
 │ installation.md        │ 480       │
 │ configuration.md       │ 400       │
 │ intro.md               │ 320       │
 │ quickstart.md          │ 280       │
 │ first-project.md       │ 120       │ ⚠️
 │ key-concepts.md        │ 50        │ 📝
 │ common-issues.md       │ 30        │ 📝
 └────────────────────────┴───────────┘

============================================
```

## 완성도 계산 기준

| 항목 | 배점 | 기준 |
|------|------|------|
| 파일 존재 | 30% | 필수 파일 존재 여부 |
| 최소 분량 | 25% | 500자 이상 |
| 코드 예제 | 20% | 기술 문서 코드 블록 |
| 메타데이터 | 15% | frontmatter 완성 |
| 링크 유효성 | 10% | 깨진 링크 없음 |

## 필수 파일 체크리스트

```
docs/
├── intro.md                    [필수]
├── getting-started/
│   ├── overview.md             [필수]
│   ├── quickstart.md           [필수]
│   └── installation.md         [권장]
├── concepts/
│   └── *.md (1개 이상)         [필수]
├── tutorials/
│   └── *.md (1개 이상)         [권장]
├── guides/
│   └── *.md (1개 이상)         [권장]
├── api/
│   └── reference.md            [권장]
└── troubleshooting/
    └── common-issues.md        [권장]
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs generate` | 누락된 문서 자동 생성 |
| `/docs add` | 개별 문서 추가 |
| `/docs preview` | 로컬에서 확인 |
