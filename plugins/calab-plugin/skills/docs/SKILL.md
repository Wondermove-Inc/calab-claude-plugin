---
name: docs
description: |
  문서 콘텐츠를 자동 생성하고 관리합니다. 전체 생성, 유형별 추가, 업데이트, 검증, 상태 확인을 수행합니다.
  USE WHEN: 문서, document, docs, 업데이트, update, 동기화, sync,
  API 문서, 컴포넌트 문서, 문서화, documentation,
  README, 가이드, guide, 튜토리얼, tutorial,
  주석, comment, JSDoc, docstring,
  설명, explain, 정리, organize,
  작성해줘, 써줘, write, generate
argument-hint: "[--generate|--add|--update|--validate|--status] [유형]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
agent: doc-updater
agents:
  primary: doc-updater
  orchestration:
    analyze: [Explore, code-reviewer]
    generate: [doc-updater]
    update: [doc-updater, Explore]
    validate: [validator, code-reviewer, doc-updater]
    reinforce: [reinforcer]
---

# /docs - 문서 관리

> **프로젝트 문서 자동 생성 및 관리**

## 사용법

```bash
/docs                      # 상태 확인 (기본)
/docs --generate           # 전체 문서 자동 생성
/docs --add api            # 특정 유형 문서 추가
/docs --update             # 코드 변경 반영 업데이트
/docs --validate           # 문서 품질 검증
/docs --status             # 문서화 현황 확인
/docs --help               # 도움말
```

## 🤖 에이전트 호출 (필수)

> **이 스킬은 반드시 doc-updater 에이전트를 통해 실행해야 합니다.**

### --generate / --add / --update 단계

```
Task(
  subagent_type="calab-plugin:doc-updater",
  description="프로젝트 문서 생성/업데이트",
  prompt="""
  **역할**: 문서화 전문가

  **목표**: {--generate: 전체 문서 생성 | --add: 특정 유형 추가 | --update: 변경 반영}

  **산출물**:
  - .claude/docs-site/ 디렉토리 구조
  - getting-started/, architecture/, api-reference/
  - 각 문서의 품질 점수

  **품질 기준**:
  - 모든 코드: 복사-붙여넣기 즉시 실행 가능
  - 기능당 최소 4개 예시 (기본, 실전, 고급, 에러처리)
  - 복잡한 구조: Mermaid 다이어그램 필수

  **제약 조건**:
  - ❌ 추측으로 API 문서 작성 금지
  - ✅ 실제 코드 분석 후 문서화
  """
)
```

### --validate 단계

```
Task(
  subagent_type="calab-plugin:validator",
  description="문서 품질 검증",
  prompt="""
  **역할**: 문서 품질 검증 전문가

  **목표**: 생성된 문서의 완전성과 정확성 검증

  **검증 항목**:
  1. 구조 검증: 필수 섹션 존재 여부
  2. 링크 검증: 깨진 링크 탐지
  3. 코드 검증: 예제 코드 실행 가능성
  4. 일관성 검증: 용어/스타일 통일
  5. 완성도 검증: 누락된 문서 식별

  **출력 형식**:
  | 항목 | 상태 | 문제점 | 권장 수정 |
  |------|------|--------|----------|
  """
)
```

---

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **`--generate`** → `references/generate.md` 실행
   - 프로젝트 심층 분석
   - 전체 문서 구조 자동 생성
   - 품질 점수 계산

3. **`--add [유형]`** → `references/add.md` 실행
   - 특정 유형 문서 개별 추가
   - 유형: `api`, `component`, `architecture`, `getting-started`, `guide`, `config`, `faq`, `troubleshooting`

4. **`--update`** → `references/update.md` 실행
   - 코드 변경 사항 감지
   - 영향받는 문서만 선택적 업데이트
   - `--since {날짜}` 옵션 지원
   - `--regenerate` 전체 재생성

5. **`--validate`** → `references/validate.md` 실행
   - 구조, 링크, 코드, 일관성, 완성도 검증
   - `--strict` 옵션 지원
   - `--fix` 자동 수정

6. **`--status`** → `references/status.md` 실행
   - 문서 커버리지 확인
   - 품질 점수 확인
   - 최신성 확인

7. **옵션 없음** → `--status` 실행 (기본)

## 문서 구조

```
.claude/docs-site/
├── getting-started/          # 시작 가이드
│   ├── installation.md
│   ├── quick-start.md
│   ├── configuration.md
│   └── deployment.md
│
├── architecture/             # 아키텍처
│   ├── overview.md
│   ├── system-design.md
│   ├── data-flow.md
│   └── decisions.md
│
├── api-reference/            # API 레퍼런스
│   ├── overview.md
│   ├── authentication.md
│   ├── types.md
│   ├── errors.md
│   └── endpoints/
│       └── {endpoint}.md
│
├── components/               # 컴포넌트
│   └── {component}.md
│
├── guides/                   # 가이드
│   └── {feature}.md
│
├── configuration/            # 설정
│   ├── environment.md
│   └── options.md
│
├── faq.md                    # FAQ
├── troubleshooting.md        # 트러블슈팅
└── index.md                  # 인덱스

.claude/docs-site/.docs-meta.json  # 메타데이터
.claude/docs-site/.docsrc.json     # 설정
```

## 문서 유형별 필수 항목

| 유형 | 필수 항목 수 | Mermaid | 스크린샷 |
|------|-------------|--------|---------|
| `getting-started` | 15개 | - | 필수 |
| `architecture` | 12개 | 4개+ | 선택 |
| `api` | 20개/엔드포인트 | 필수 | - |
| `component` | 18개/컴포넌트 | 선택 | 필수 |
| `guide` | 10개 | 필수 | 단계별 |
| `config` | 8개/옵션 | - | 선택 |
| `faq` | 5개/질문 | - | - |
| `troubleshooting` | 6개/이슈 | - | 필수 |

## 품질 기준

- **모든 코드**: 복사-붙여넣기로 즉시 실행 가능
- **기능당 최소 4개 예시**: 기본, 실전, 고급, 에러처리
- **복잡한 구조**: Mermaid 다이어그램 필수
- **스크린샷 위치**: `<!-- 📸 스크린샷 필요: [설명] -->` 주석

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/docs-generate` | `/docs --generate` |
| `/docs-add` | `/docs --add` |
| `/docs-update` | `/docs --update` |
| `/docs-validate` | `/docs --validate` |
| `/docs-status` | `/docs --status` |

## 워크플로우

```
/docs --generate        # 최초 전체 생성
      ↓
/docs --add {유형}      # 필요한 문서 추가
      ↓
(코드 변경)
      ↓
/docs --update          # 변경사항 반영
      ↓
/docs --validate        # 품질 검증
      ↓
/docs --status          # 현황 확인
```

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| 문서 없음 | `/docs --generate` |
| 특정 문서 필요 | `/docs --add {유형}` |
| 코드 변경 후 | `/docs --update` |
| 품질 확인 | `/docs --validate` |
| 현황 파악 | `/docs --status` |

## 참조 파일

### 템플릿 (스킬 내부)

| 문서 유형 | 템플릿 |
|----------|--------|
| API 문서 | `templates/api-spec-template.md` |
| 아키텍처 | `templates/architecture-template.md` |
| PRD | `templates/prd-template.md` |

### 베스트 프랙티스 (스킬 내부)

- `references/api-design.md` - API 문서화
- `references/clean-architecture.md` - 아키텍처 문서화
