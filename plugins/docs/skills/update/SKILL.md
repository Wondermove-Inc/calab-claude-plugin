---
name: docs:update
description: 코드 변경사항을 반영하여 기존 문서 업데이트. /docs update 또는 "문서 업데이트" 키워드 시 자동 활성화.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# /docs update - 기존 문서 업데이트

> 코드 변경 사항을 반영하여 기존 문서를 업데이트합니다.

## 사용법

```bash
/docs update
/docs update [type]
/docs update --since="2024-01-01"
```

## 실행 단계

### 1단계: 변경 사항 감지

다음 방법으로 변경 사항을 감지합니다:

1. **Git diff 분석**: 마지막 문서 생성 이후 변경된 파일
2. **타임스탬프 비교**: 문서보다 최신인 소스 파일
3. **해시 비교**: 파일 내용 해시 비교

### 2단계: 영향 분석

변경된 파일이 영향을 미치는 문서를 파악합니다:

| 변경 파일 | 영향받는 문서 |
|-----------|---------------|
| API 라우터 | api-reference/ |
| 컴포넌트 | components/ |
| 설정 파일 | configuration/ |
| 타입 정의 | api-reference/types.md |

### 3단계: 문서 업데이트

영향받는 문서만 선택적으로 업데이트합니다.

## 실행 예시

### 전체 업데이트

```bash
/docs update
```

**결과:**

```
🔄 문서 업데이트

[1/3] 변경 사항 감지 중...
  ✓ 마지막 업데이트: 2024-01-15 14:30
  ✓ 변경된 파일: 8개

  변경된 파일:
  - src/api/users.ts (수정)
  - src/api/products.ts (수정)
  - src/components/Button.tsx (수정)
  - src/components/Modal.tsx (신규)
  - src/config/settings.ts (수정)

[2/3] 영향 분석 중...
  영향받는 문서:
  - api-reference/endpoints/users.md
  - api-reference/endpoints/products.md
  - components/button.md
  - components/modal.md (신규 생성)
  - configuration/options.md

[3/3] 업데이트 중...
  ✓ api-reference/endpoints/users.md (업데이트)
  ✓ api-reference/endpoints/products.md (업데이트)
  ✓ components/button.md (업데이트)
  ✓ components/modal.md (신규 생성)
  ✓ configuration/options.md (업데이트)

✅ 문서 업데이트 완료

📊 업데이트 요약:
  - 업데이트: 4개
  - 신규 생성: 1개
  - 변경 없음: 58개
```

### 특정 유형만 업데이트

```bash
/docs update api
```

### 특정 기간 이후 변경 사항

```bash
/docs update --since="2024-01-01"
```

## 변경 추적

`.claude/docs-site/.docs-meta.json`에 메타데이터를 저장합니다:

```json
{
  "lastUpdated": "2024-01-20T10:30:00Z",
  "version": "1.2.0",
  "files": {
    "api-reference/endpoints/users.md": {
      "sourceHash": "abc123",
      "generatedAt": "2024-01-20T10:30:00Z",
      "sources": [
        "src/api/users.ts",
        "src/types/user.ts"
      ]
    }
  }
}
```

## 업데이트 전략

### 보수적 업데이트 (기본)

- 변경된 섹션만 업데이트
- 수동 편집 내용 보존
- 충돌 시 사용자 확인 요청

### 전체 재생성

```bash
/docs update --regenerate
```

- 문서 전체 재생성
- 수동 편집 내용 백업

## 충돌 처리

수동으로 편집된 문서가 있을 경우:

```
⚠️ 충돌 감지: components/button.md

해당 문서가 수동으로 편집되었습니다.

선택하세요:
  [1] 자동 업데이트 (수동 편집 보존)
  [2] 전체 재생성 (수동 편집 덮어쓰기)
  [3] 건너뛰기
  [4] 비교 보기
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--since` | 특정 날짜 이후 변경 사항만 |
| `--regenerate` | 전체 재생성 |
| `--dry-run` | 실제 변경 없이 미리보기 |
| `--force` | 충돌 무시하고 업데이트 |
| `--backup` | 업데이트 전 백업 생성 |

## 자동 업데이트 설정

PostToolUse 훅에 연결하여 코드 변경 시 자동 업데이트:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'docs-update-pending' >> .claude/docs-site/.pending"
        }
      ]
    }
  ]
}
```

> 📘 자동 업데이트는 성능을 위해 배치로 처리됩니다.
