---
name: toolkit:code-review
description: 코드 품질(보안/성능/언어별 권장사항)을 검증하고 개선점을 제안합니다
disable-model-invocation: true
---

# Code Review Command

변경된 코드를 분석하여 **보안, 성능, 코드 품질, 언어별 권장사항**을 검토하고 개선점을 제안합니다.

## 작업 순서

1. **변경사항 파악**
   - `git diff HEAD~1` 또는 사용자가 지정한 범위의 변경사항 확인
   - 변경된 파일 목록과 변경 컨텍스트 (관련 이슈, 커밋 메시지) 파악
   - `git blame`으로 변경 히스토리 확인하여 의도 이해

2. **코드 리뷰 수행**
   - 아래 리뷰 기준에 따라 변경된 코드 분석
   - **변경된 코드에 집중** (기존 코드의 문제가 아닌 새로 도입된 이슈만)
   - 프로젝트의 CLAUDE.md, 린트 설정 등 기존 컨벤션 확인 후 적용

3. **리뷰 요약 리포트 생성**
   다음 형식에 따라 리포트를 작성:

```
## Code Review Summary

### Overall Assessment
- Quality Score: X/10
- Issues Found: X (Critical: X, Warning: X, Suggestion: X)

### Critical Issues (보안 취약점)
| # | 파일 | 내용 | 수정 방안 |
|---|------|------|----------|
| 1 | path/to/file:line | [취약점 유형] | [구체적 수정 방안] |

### Warnings (성능/에러 처리)
| # | 파일 | 내용 | 수정 방안 |
|---|------|------|----------|
| 1 | path/to/file:line | [문제] | [구체적 수정 방안] |

### Suggestions (코드 품질)
| # | 파일 | 내용 | 수정 방안 |
|---|------|------|----------|
| 1 | path/to/file:line | [개선점] | [제안] |

### Language-Specific Issues
- **Go**: [발견 사항]
- **TypeScript**: [발견 사항]
- **React**: [발견 사항]
- **Python**: [발견 사항]

### Good Points
- [잘 작성된 부분들]

### Recommendations
- 전반적인 개선 방향
```

## 사용 예시

```
/toolkit:code-review                          # 최근 커밋과 현재 변경사항 리뷰
/toolkit:code-review HEAD~3..HEAD             # 최근 3개 커밋 리뷰
/toolkit:code-review src/service.ts           # 특정 파일만 리뷰
```

---

## 참조 가이드

- **언어별 가이드**: `guides/language-guide.md` - 코드 품질, 보안, 성능 기준

## 리뷰 원칙

- **변경 코드 집중**: 기존 코드가 아닌 새로 도입된 이슈만 보고
- **코드 품질 중심**: 보안, 성능, 언어별 권장사항에 집중
- **높은 확신도만 보고**: 추측성 지적보다 명확한 이슈에 집중
- **프로젝트 컨벤션 우선**: 일반 규칙보다 프로젝트의 기존 패턴을 우선
- **심각도 분류 엄격 적용**: Critical은 보안 취약점에만, 성능은 Warning, 스타일은 Suggestion

---

## 리뷰 기준

> 상세 기준은 `guides/language-guide.md` 참조

### 1. 보안 (Security) — Critical 우선

#### 필수 검증 항목
- **입력 검증**: 모든 외부 입력에 검증이 적용되는가 (화이트리스트 선호)
- **인젝션 방지**: SQL, XSS, Command Injection 등 인젝션 취약점이 없는가
- **인증/인가**: 적절한 권한 검사가 있는가, 인증 우회가 불가능한가
- **Secrets 관리**: API 키, 비밀번호 등이 하드코딩되어 있지 않은가
- **민감 정보 노출**: 로그, 에러 메시지, 응답에 민감 정보가 노출되지 않는가
- **의존성 보안**: 알려진 취약점이 있는 의존성을 사용하지 않는가

#### 자동화 스캔 명령어

**Secrets 스캔**:
```bash
# gitleaks (권장)
gitleaks detect --source . --verbose

# truffleHog
trufflehog filesystem . --json
```

**의존성 취약점**:
```bash
# Go
go list -json -m all | nancy sleuth

# Node.js
npm audit
yarn audit

# Python
pip-audit
safety check
```

**정적 분석**:
```bash
# Go
gosec ./...

# TypeScript/JavaScript
npm run lint
eslint --ext .ts,.tsx src/

# Python
bandit -r .
```

### 2. 정확성 (Correctness) — Warning 우선

- **에러 핸들링**: 에러가 무시되지 않고 적절히 처리되는가, 컨텍스트가 보존되는가
- **타입 안전성**: 타입 단언/캐스팅 남용, 타입 검증 누락이 없는가
- **리소스 관리**: 파일, 연결, 메모리 등 리소스가 적절히 해제되는가
- **동시성 구현**: race condition, deadlock 가능성

### 3. 성능 (Performance) — Warning 우선

> 실제 병목이 확인되거나 명백한 경우에만 제안

- **쿼리 효율**: N+1 쿼리, 불필요한 전체 조회가 없는가
- **알고리즘 복잡도**: 비효율적인 알고리즘 (불필요한 O(n²) 등)이 없는가
- **불필요한 연산**: 반복문 내 중복 호출, 불필요한 메모리 할당이 없는가
- **캐싱 기회**: 반복 호출되는 비용이 큰 연산에 캐싱이 고려되었는가
- **I/O 최적화**: 불필요한 네트워크/디스크 호출이 없는가

### 4. 코드 품질 (Code Quality) — Suggestion 우선

- **네이밍 명확성**: 변수/함수/타입명이 의도를 명확히 드러내는가
- **함수 크기**: 함수가 적절한 길이인가 (너무 길지 않은가)
- **중첩 깊이**: 3단계 이하로 유지되는가
- **코드 중복**: 동일 로직의 불필요한 반복이 없는가 (DRY)
- **불필요한 코드**: Dead code, unused imports, 미사용 변수 제거
- **주석 품질**:
  - 불필요한 주석 제거 (코드가 설명하는 것을 반복)
  - 오래된 주석 업데이트 또는 제거
  - 복잡한 로직에만 "왜"를 설명
- **과잉 엔지니어링**: 불필요한 추상화 제거 (KISS)

### 5. 언어별 권장사항

#### Go
- **함수 길이**: 50줄 이상 함수 분리 검토
- **중첩 깊이**: 3단계 이상 시 리팩토링
- **타입**: `any` (interface{}) 남용 지양
- **에러 처리**:
  - 에러 무시 금지 (`_ = err` 지양)
  - 에러 래핑 (`fmt.Errorf("context: %w", err)`)
- **네이밍**:
  - 패키지명 소문자 단수형
  - Getter에 Get 접두사 사용 안 함

#### TypeScript
- **타입 안전성**:
  - `any` 타입 지양 (unknown 또는 구체적 타입 사용)
  - 타입 단언 최소화 (as 연산자)
  - `@ts-ignore` 남용 금지
- **null 안전성**: Optional chaining (`?.`), Nullish coalescing (`??`)
- **불변성**: `const` 우선, `readonly` 적극 사용

#### React
- **컴포넌트 크기**: 100줄 이상 시 분리 검토
- **Props**: 3단계 이상 prop drilling 시 Context/상태 관리 고려
- **Hook 규칙**:
  - 최상위에서만 호출
  - 조건문/반복문 내 Hook 금지
  - 의존성 배열 정확히 명시
- **리렌더링**: useMemo, useCallback 적절히 사용

#### Python
- **타입 힌트**: 함수 시그니처에 타입 명시
- **예외 처리**: Bare except 금지 (`except Exception:` 명시)
- **기본 인자**: Mutable 객체 (`[]`, `{}`) 기본값 금지
- **Comprehension**: 복잡한 로직은 일반 반복문 사용

### 6. AI 생성 코드 검증

- **환각 탐지**: 존재하지 않는 함수, 라이브러리, API를 사용하지 않는가
- **의도 일치**: 요청된 변경과 실제 코드가 일치하는가
- **코드베이스 정합성**: 기존 코드 스타일/패턴과 일치하는가
- **불필요한 의존성**: 필요 없는 패키지가 추가되지 않았는가
