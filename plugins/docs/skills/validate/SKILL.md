---
name: docs:validate
description: 문서의 품질, 일관성, 완성도 검증. /docs validate 또는 "문서 검증" 키워드 시 자동 활성화.
allowed-tools: Read, Glob, Grep
user-invocable: true
---

# /docs validate - 문서 품질 검증

> 문서의 품질, 일관성, 완성도를 검증합니다.

## 사용법

```bash
/docs validate
/docs validate [path]
/docs validate --fix
```

## 검증 항목

### 1. 구조 검증

| 항목 | 검사 내용 |
|------|----------|
| 필수 섹션 | 제목, 개요, 본문 등 필수 섹션 포함 |
| 제목 형식 | 일관된 제목 스타일 |
| 섹션 순서 | 표준 섹션 순서 준수 |

### 2. 링크 검증

| 항목 | 검사 내용 |
|------|----------|
| 내부 링크 | 다른 문서로의 링크 유효성 |
| 외부 링크 | 외부 URL 접근 가능 여부 |
| 앵커 링크 | 문서 내 앵커 링크 유효성 |

### 3. 코드 검증

| 항목 | 검사 내용 |
|------|----------|
| 문법 | 코드 블록 문법 오류 |
| import문 | import 경로 유효성 |
| 타입 | TypeScript 타입 일치 |

### 4. 일관성 검증

| 항목 | 검사 내용 |
|------|----------|
| 용어 | 일관된 용어 사용 |
| 스타일 | 마크다운 스타일 일관성 |
| 포맷 | 날짜, 숫자 포맷 일관성 |

### 5. 완성도 검증

| 항목 | 검사 내용 |
|------|----------|
| TODO | 미완성 TODO 항목 |
| 빈 섹션 | 내용 없는 섹션 |
| 플레이스홀더 | 임시 텍스트 |

## 실행 결과

```
🔍 문서 검증 시작

═══════════════════════════════════════════════════════════
📋 검증 결과
═══════════════════════════════════════════════════════════

검사 문서: 62개
검사 항목: 5개 카테고리

✅ 구조 검증     통과: 60/62  실패: 2
✅ 링크 검증     통과: 62/62  실패: 0
⚠️ 코드 검증    통과: 58/62  실패: 4
✅ 일관성 검증   통과: 61/62  실패: 1
⚠️ 완성도 검증  통과: 59/62  실패: 3

═══════════════════════════════════════════════════════════
❌ 오류 (반드시 수정)
═══════════════════════════════════════════════════════════

[구조] api-reference/endpoints/orders.md:1
  └─ 필수 섹션 누락: "개요" 섹션이 없습니다.
     + 해결: 문서 시작 부분에 "## 개요" 섹션을 추가하세요.

[구조] components/modal.md:1
  └─ 필수 섹션 누락: "Props" 섹션이 없습니다.
     + 해결: Props 테이블을 추가하세요.

[코드] api-reference/endpoints/users.md:45
  └─ import 경로 오류: '@/types/user'를 찾을 수 없습니다.
     + 해결: import { User } from '@/types/User' (대소문자 확인)

[코드] components/button.md:23
  └─ 타입 불일치: 'variant' prop이 'primary' | 'secondary'이지만
     예시에서 'default' 사용
     + 해결: 예시 코드를 유효한 값으로 수정하세요.

═══════════════════════════════════════════════════════════
⚠️ 경고 (권장 수정)
═══════════════════════════════════════════════════════════

[코드] guides/authentication.md:78
  └─ 하드코딩된 값: API 키가 하드코딩되어 있습니다.
     + 권장: 환경 변수 사용 예시로 변경

[코드] api-reference/overview.md:34
  └─ 오래된 URL: 'localhost:3000' 사용
     + 권장: 실제 API URL 또는 변수 사용

[일관성] getting-started/installation.md:12
  └─ 용어 불일치: 'npm install'과 'npm i' 혼용
     + 권장: 일관된 명령어 사용

[완성도] architecture/data-flow.md:45
  └─ TODO 발견: "TODO: 다이어그램 추가"
     + 권장: TODO 항목 완료 또는 제거

[완성도] components/drawer.md:1
  └─ 빈 섹션: "예시" 섹션이 비어있습니다.
     + 권장: 코드 예시 추가

[완성도] faq.md:89
  └─ 플레이스홀더: "[답변 작성 필요]" 발견
     + 권장: 실제 내용으로 대체

═══════════════════════════════════════════════════════════
📊 검증 요약
═══════════════════════════════════════════════════════════

총 문서:    62개
오류:       4개 (반드시 수정)
경고:       6개 (권장 수정)
통과:       52개

품질 점수:  84/100

💡 다음 단계:
  /docs validate --fix  # 자동 수정 가능한 항목 수정
```

## 자동 수정

```bash
/docs validate --fix
```

자동으로 수정 가능한 항목:

| 항목 | 자동 수정 |
|------|----------|
| 빈 섹션 | 기본 템플릿 삽입 |
| 링크 대소문자 | 올바른 경로로 수정 |
| 포맷 불일치 | 표준 포맷으로 통일 |
| 마크다운 문법 | 문법 오류 수정 |

```
🔧 자동 수정 실행

수정된 항목:
  ✓ api-reference/endpoints/users.md - import 경로 수정
  ✓ getting-started/installation.md - 명령어 통일

수동 수정 필요:
  ✗ api-reference/endpoints/orders.md - "개요" 섹션 추가 필요
  ✗ components/button.md - 예시 코드 수정 필요

자동 수정: 2개
수동 수정 필요: 2개
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--fix` | 자동 수정 가능한 항목 수정 |
| `--strict` | 경고도 오류로 처리 |
| `--json` | JSON 형식 출력 |
| `--quiet` | 오류만 출력 |
| `--ignore=[rule]` | 특정 규칙 무시 |

## 검증 규칙 설정

`.claude/docs-site/.docsrc.json`에서 규칙을 커스터마이징할 수 있습니다:

```json
{
  "rules": {
    "require-overview": true,
    "require-examples": true,
    "check-external-links": false,
    "max-heading-depth": 4,
    "terminology": {
      "preferred": {
        "npm i": "npm install",
        "utilize": "use"
      }
    }
  },
  "ignore": [
    "**/drafts/**",
    "**/archive/**"
  ]
}
```

## CI/CD 통합

GitHub Actions 예시:

```yaml
- name: Validate Documentation
  run: |
    claude /docs validate --strict --json > docs-report.json
    if [ $(jq '.errors | length' docs-report.json) -gt 0 ]; then
      echo "Documentation validation failed"
      exit 1
    fi
```
