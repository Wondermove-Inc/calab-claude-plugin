# /docs --update - 기존 문서 업데이트

> **코드 변경 사항 반영하여 문서 증분 업데이트**

## 사용법
```bash
/docs --update                  # 모든 변경 반영
/docs --update --since 2025-01-01  # 특정 날짜 이후
/docs --update --regenerate     # 전체 재생성
```

## 실행 절차

### Step 1: 변경 사항 감지

**감지 방법:**
- Git diff: `git diff --name-only HEAD~10`
- 타임스탬프 비교: 소스 파일 vs 문서 파일
- 해시 비교: 소스 파일 해시 vs .docs-meta.json

### Step 2: 영향 분석

| 변경된 파일 | 영향받는 문서 |
|------------|-------------|
| src/app/api/users/route.ts | api-reference/endpoints/users.md |
| src/components/Button.tsx | components/button.md |
| package.json | getting-started/installation.md |

### Step 3: 선택적 업데이트

**보수적 업데이트 (기본):**
- 변경된 섹션만 업데이트
- 수동 편집 보존

**충돌 시:**
```
⚠️ 충돌: api-reference/users.md
[1] 자동 업데이트
[2] 전체 재생성
[3] 건너뛰기
[4] 비교 보기
```

### Step 4: 메타데이터 저장

**.claude/docs-site/.docs-meta.json:**
```json
{
  "files": {
    "api-reference/users.md": {
      "sourceHash": "abc123",
      "generatedAt": "2025-01-15T10:00:00Z",
      "sources": ["src/app/api/users/route.ts"]
    }
  }
}
```

### 완료 보고
```
============================================
 DOCS UPDATE 완료
============================================
 업데이트: 5개
 건너뜀: 2개 (수동 편집 보존)
 충돌: 0개
============================================
```
