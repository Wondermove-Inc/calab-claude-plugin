---
name: doc-updater
description: 코드 변경 사항을 감지하여 문서를 자동으로 업데이트합니다. 문서 업데이트, 동기화, API 문서, 컴포넌트 문서 키워드 시 자동 활성화.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Doc Updater

코드 변경 사항을 감지하여 관련 문서를 자동으로 업데이트하는 스킬.

## 문서 유형

### 1. API 문서
- OpenAPI/Swagger 스펙
- REST 엔드포인트 문서
- GraphQL 스키마 문서

### 2. 컴포넌트 문서
- React/Vue 컴포넌트 Props
- Storybook 스토리
- 사용 예시

### 3. 프로젝트 문서
- README.md
- CHANGELOG.md
- CONTRIBUTING.md

## 업데이트 워크플로우

### Phase 1: 변경 감지
```bash
# Git diff로 변경 파일 확인
git diff --name-only HEAD~1

# 변경 유형 분류
- 소스 코드 변경 → API/컴포넌트 문서 업데이트
- 설정 변경 → README 업데이트
- 기능 추가/수정 → CHANGELOG 업데이트
```

### Phase 2: 문서 분석
```bash
# 관련 문서 찾기
Grep: 변경된 함수/클래스명 in docs/

# 문서-코드 매핑
src/api/users.ts → docs/api/users.md
src/components/Button.tsx → docs/components/Button.md
```

### Phase 3: 자동 업데이트
```markdown
## 업데이트 대상

### API 문서
- 엔드포인트 시그니처 변경 반영
- 요청/응답 타입 업데이트
- 예시 코드 갱신

### 컴포넌트 문서
- Props 타입 변경 반영
- 사용 예시 업데이트
- 스토리 갱신

### README
- 설치 방법 변경 반영
- 사용법 업데이트
- 의존성 목록 갱신
```

## 자동 추출 패턴

### TypeScript 함수 문서화
```typescript
/**
 * 사용자를 생성합니다.
 * @param name - 사용자 이름
 * @param email - 이메일 주소
 * @returns 생성된 사용자 객체
 */
export async function createUser(name: string, email: string): Promise<User> {
  // ...
}
```

→ 자동 생성:
```markdown
### createUser

사용자를 생성합니다.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| name | string | 사용자 이름 |
| email | string | 이메일 주소 |

**Returns:** `Promise<User>` - 생성된 사용자 객체
```

### React 컴포넌트 문서화
```typescript
interface ButtonProps {
  /** 버튼 텍스트 */
  label: string;
  /** 클릭 핸들러 */
  onClick: () => void;
  /** 비활성화 여부 */
  disabled?: boolean;
}
```

→ 자동 생성:
```markdown
### Button Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| label | string | ✅ | 버튼 텍스트 |
| onClick | () => void | ✅ | 클릭 핸들러 |
| disabled | boolean | ❌ | 비활성화 여부 |
```

## CHANGELOG 자동 생성

### Conventional Commits 기반
```bash
# Git 로그 분석
git log --oneline --since="2024-01-01"

# 커밋 유형 분류
feat: → Added
fix: → Fixed
docs: → Documentation
refactor: → Changed
```

### 출력 형식
```markdown
## [1.2.0] - 2024-01-15

### Added
- 사용자 프로필 편집 기능 (#123)
- 다크 모드 지원 (#125)

### Fixed
- 로그인 세션 만료 버그 (#120)
- 모바일 레이아웃 깨짐 (#122)

### Changed
- API 응답 형식 개선 (#124)
```

## 문서 동기화 검증

### 불일치 탐지
```markdown
## 문서-코드 불일치 리포트

### ⚠️ 경고
| 파일 | 문제 | 권장 조치 |
|------|------|----------|
| docs/api/users.md | createUser 파라미터 변경됨 | role 파라미터 추가 필요 |
| docs/components/Modal.md | size prop 타입 변경됨 | 'sm'|'md'|'lg' → 'small'|'medium'|'large' |

### ❌ 누락
| 코드 | 문서 필요 |
|------|----------|
| src/api/orders.ts | docs/api/orders.md 생성 필요 |
| src/hooks/useAuth.ts | docs/hooks/useAuth.md 생성 필요 |
```

## 통합 명령어

### 전체 문서 동기화
```bash
# 모든 문서 검증 및 업데이트
/docs validate
/docs update --all

# 특정 영역만
/docs update --api
/docs update --components
```

### 변경 사항 기반
```bash
# 최근 커밋 기준
/docs update --since HEAD~5

# 특정 브랜치 기준
/docs update --since main
```

## 출력 형식

```markdown
## 문서 업데이트 결과

### 업데이트됨 (5개)
| 문서 | 변경 내용 |
|------|----------|
| docs/api/users.md | createUser 파라미터 업데이트 |
| docs/components/Button.md | variant prop 추가 |
| README.md | 설치 명령어 업데이트 |
| CHANGELOG.md | v1.2.0 릴리즈 노트 추가 |

### 생성됨 (2개)
| 문서 | 대상 코드 |
|------|----------|
| docs/api/orders.md | src/api/orders.ts |
| docs/hooks/useAuth.md | src/hooks/useAuth.ts |

### 검증 필요 (1개)
| 문서 | 이유 |
|------|------|
| docs/api/payments.md | 복잡한 변경, 수동 검토 권장 |
```

## 관련 스킬
- `dev-workflow`: 개발 워크플로우
- `code-quality`: 코드 품질 (문서화 포함)

## 참조
- `.claude/best-practices/api-design.md`
- `.claude/memory/TECH_STACK.md`
