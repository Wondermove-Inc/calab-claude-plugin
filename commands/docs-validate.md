---
description: 문서를 검증합니다 (링크, 형식, 품질).
allowed-tools: Read, Glob, Bash, Task
argument-hint: [--fix] [--strict]
---

# /docs-validate - 문서 검증

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

문서 사이트의 품질을 검증합니다.
링크 유효성, 마크다운 형식, 이미지 참조, 메타데이터 등을 검사합니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--fix` | 자동 수정 가능한 문제 수정 | false |
| `--strict` | 엄격 모드 (경고도 에러로 처리) | false |

## 사용법

```bash
/docs validate              # 기본 검증
/docs validate --fix        # 자동 수정 포함
/docs validate --strict     # 엄격 모드
```

## 검증 항목

### 1. 링크 검증 (Links)

| 검사 | 설명 | 심각도 |
|------|------|--------|
| 내부 링크 | docs 내 링크 유효성 | Error |
| 외부 링크 | HTTP 응답 확인 | Warning |
| 앵커 링크 | #heading 유효성 | Warning |
| 이미지 링크 | 이미지 파일 존재 | Error |

### 2. 마크다운 형식 (Format)

| 검사 | 설명 | 심각도 |
|------|------|--------|
| Frontmatter | 필수 필드 존재 | Error |
| 제목 구조 | H1 → H2 → H3 순서 | Warning |
| 코드 블록 | 언어 지정 여부 | Warning |
| 리스트 형식 | 일관된 마커 사용 | Info |

### 3. 콘텐츠 품질 (Quality)

| 검사 | 설명 | 심각도 |
|------|------|--------|
| 최소 길이 | 500자 이상 | Warning |
| 제목 길이 | 10-70자 권장 | Info |
| 코드 예제 | 기술 문서 코드 포함 | Warning |
| alt 텍스트 | 이미지 alt 속재 | Warning |

### 4. 메타데이터 (Metadata)

| 검사 | 설명 | 심각도 |
|------|------|--------|
| sidebar_position | 순서 지정 | Warning |
| description | SEO 설명 | Info |
| keywords | 검색 키워드 | Info |
| slug | URL 경로 | Info |

## 실행 단계

### 1. 파일 수집

에이전트를 사용하여 `.claude/docs-site/docs/` 내 모든 마크다운 파일 수집.

### 2. 검증 실행

각 검증 항목에 대해 병렬로 검사 실행.

### 3. 자동 수정 (--fix 옵션)

수정 가능한 항목:
- 코드 블록 언어 추가 (추론 가능한 경우)
- Frontmatter 필수 필드 추가
- 상대 경로 정규화
- trailing whitespace 제거

### 4. 결과 리포트

```
============================================
 🔍 문서 검증 결과
============================================

 검사한 파일: 15개

 ❌ Errors: 3
 ⚠️ Warnings: 7
 ℹ️ Info: 12

 ─────────────────────────────────────────

 ❌ ERRORS (수정 필요)

 1. [LINK] tutorials/first-project.md:25
    깨진 내부 링크: /docs/concepts/missing.md
    → 해결: 존재하는 경로로 수정 또는 문서 생성

 2. [LINK] guides/configuration.md:42
    이미지 누락: /img/config-screenshot.png
    → 해결: 이미지 파일 추가

 3. [META] api/reference.md:1
    Frontmatter 누락: sidebar_position
    → --fix 옵션으로 자동 수정 가능

 ─────────────────────────────────────────

 ⚠️ WARNINGS (권장 수정)

 1. [QUALITY] tutorials/first-project.md
    콘텐츠 길이 부족: 320자 (최소 500자 권장)

 2. [FORMAT] concepts/key-concepts.md:15
    코드 블록 언어 미지정
    → --fix 옵션으로 자동 수정 가능

 3. [LINK] getting-started/overview.md:50
    외부 링크 응답 없음: https://old-docs.example.com
    (HTTP 404)

 4. [FORMAT] guides/deployment.md
    제목 구조 스킵: H1 → H3 (H2 누락)

 ─────────────────────────────────────────

 ℹ️ INFO (선택 개선)

 1. [META] 5개 파일에 description 누락
 2. [QUALITY] 3개 파일에 alt 텍스트 누락

 ─────────────────────────────────────────

 📊 요약

 ┌────────────────┬───────┬─────────┬──────┐
 │ 카테고리       │ Pass  │ Fail    │ 비율 │
 ├────────────────┼───────┼─────────┼──────┤
 │ 내부 링크      │ 45    │ 2       │ 96%  │
 │ 외부 링크      │ 12    │ 1       │ 92%  │
 │ 이미지         │ 8     │ 1       │ 89%  │
 │ Frontmatter    │ 14    │ 1       │ 93%  │
 │ 콘텐츠 품질    │ 12    │ 3       │ 80%  │
 └────────────────┴───────┴─────────┴──────┘

 전체 점수: 85/100 ⭐⭐⭐⭐☆

 ─────────────────────────────────────────

 💡 권장 작업

 1. /docs validate --fix 로 자동 수정 (2개 항목)
 2. tutorials/first-project.md 콘텐츠 보강
 3. 누락된 이미지 추가: /img/config-screenshot.png

============================================
```

## --fix 옵션 결과

```
============================================
 🔧 자동 수정 완료
============================================

 수정된 항목: 5개

 ✅ api/reference.md
    - sidebar_position: 1 추가

 ✅ concepts/key-concepts.md
    - 코드 블록 언어 추가: javascript

 ✅ guides/deployment.md
    - trailing whitespace 제거

 ✅ tutorials/first-project.md
    - 상대 경로 정규화: ../concepts → /concepts

 ✅ getting-started/quickstart.md
    - description 필드 추가

 수정 불가 항목: 3개 (수동 수정 필요)

 ❌ 깨진 링크 2개 - 수동으로 경로 수정 필요
 ❌ 누락된 이미지 1개 - 파일 추가 필요

============================================
```

## CI/CD 연동

### GitHub Actions

```yaml
# .github/workflows/docs-validate.yml
name: Validate Docs

on:
  pull_request:
    paths:
      - '.claude/docs-site/docs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: cd .claude/docs-site && npm ci

      - name: Build (link check)
        run: cd .claude/docs-site && npm run build
        env:
          NODE_OPTIONS: --max_old_space_size=4096
```

## 검증 규칙 커스터마이징

`.claude/docs-site/.docsvalidate.json`:

```json
{
  "rules": {
    "min-content-length": 500,
    "require-code-language": true,
    "require-alt-text": true,
    "check-external-links": false,
    "heading-structure": "strict"
  },
  "ignore": [
    "drafts/**",
    "**/CHANGELOG.md"
  ]
}
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs status` | 문서 현황 확인 |
| `/docs build` | 빌드 시 링크 체크 |
| `/docs deploy` | 배포 전 검증 권장 |
