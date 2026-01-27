---
name: refactor-cleaner
description: 데드 코드, 미사용 import, 중복 코드를 자동으로 정리합니다. 리팩토링, 정리, 클린업, 미사용 코드 키워드 시 자동 활성화.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Refactor Cleaner

데드 코드, 미사용 import, 중복 코드를 자동으로 탐지하고 정리하는 스킬.

## 탐지 대상

### 1. 미사용 Import
```typescript
// ❌ 미사용 - 제거 대상
import { unusedFunction } from './utils';
import type { UnusedType } from './types';

// ✅ 사용 중 - 유지
import { usedFunction } from './utils';
```

### 2. 데드 코드
```typescript
// ❌ 도달 불가능한 코드
function example() {
  return true;
  console.log('이 코드는 실행되지 않음'); // 데드 코드
}

// ❌ 미사용 함수
function neverCalled() {  // 어디서도 호출되지 않음
  // ...
}
```

### 3. 중복 코드
```typescript
// ❌ 동일 로직 반복
function processA(data) {
  const result = data.map(x => x * 2);
  return result.filter(x => x > 10);
}

function processB(items) {
  const result = items.map(x => x * 2);  // 중복
  return result.filter(x => x > 10);     // 중복
}
```

## 탐지 워크플로우

### Phase 1: 스캔
```
1. Glob으로 대상 파일 수집
2. Grep으로 import/export 패턴 추출
3. 함수/변수 사용처 분석
```

### Phase 2: 분석
```
1. 미사용 심볼 목록 생성
2. 데드 코드 경로 탐지
3. 중복 패턴 식별
```

### Phase 3: 정리
```
1. 미사용 import 제거
2. 데드 코드 삭제
3. 중복 코드 함수 추출
```

## 탐지 패턴

### TypeScript/JavaScript
```
미사용 import 패턴:
  import\s+\{[^}]+\}\s+from\s+['"][^'"]+['"]

미사용 변수 패턴:
  (const|let|var)\s+(\w+)\s*=

미사용 함수 패턴:
  (function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)
```

### Python
```
미사용 import 패턴:
  ^(import\s+\w+|from\s+\w+\s+import)

미사용 변수 패턴:
  ^\s*(\w+)\s*=

미사용 함수 패턴:
  ^def\s+(\w+)\s*\(
```

## 안전 장치

### 제외 대상
- `__init__.py` 의 re-export
- `index.ts` 의 barrel export
- `@public` 또는 `@api` 주석이 있는 심볼
- 테스트 파일의 mock/fixture
- 설정 파일 (`*.config.*`)

### 확인 필요
- 동적 import (`import()`)
- 리플렉션/메타프로그래밍
- 외부 라이브러리 인터페이스

## 출력 형식

```markdown
## 정리 결과

### 미사용 Import 제거 (12개)
| 파일 | import | 라인 |
|------|--------|------|
| src/utils.ts | unusedHelper | 3 |
| src/api.ts | deprecatedFn | 15 |

### 데드 코드 제거 (5개)
| 파일 | 함수/변수 | 라인 범위 |
|------|----------|----------|
| src/old.ts | legacyHandler | 45-67 |

### 중복 코드 통합 (2개)
| 원본 | 중복 | 공통 함수 |
|------|------|----------|
| processA | processB | processCommon |
```

## 관련 스킬
- `code-quality`: 코드 스멜 탐지
- `best-practices`: 리팩토링 패턴 참조

## 참조
- `.claude/best-practices/typescript.md`
- `.claude/best-practices/python.md`
