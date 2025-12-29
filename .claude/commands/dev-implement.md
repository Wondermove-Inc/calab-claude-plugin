---
description: 태스크를 구현합니다. 베스트 프랙티스를 적용하여 코드를 생성합니다. 태스크 ID 또는 설명을 인자로 받습니다.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [task-id 또는 태스크 설명]
---

# 태스크 구현

## 목적

태스크를 베스트 프랙티스에 따라 구현합니다.

## 실행 절차

### Step 1: 컨텍스트 로드

```
1. .claude/memory/CURRENT_CONTEXT.md - 현재 작업 상태
2. .claude/memory/TECH_STACK.md - 기술 스택
3. docs/tasks/{feature}/tasks.md - 태스크 목록
4. docs/prd/{feature}/prd.md - 요구사항
5. docs/architecture/ - 설계 문서
```

### Step 2: 태스크 식별

$ARGUMENTS에서 태스크 ID 파악:

```
TASK-001: User 테이블 마이그레이션
```

### Step 3: 베스트 프랙티스 로드

기술 스택에 따라 베스트 프랙티스 로드:

```
.claude/best-practices/react.md
.claude/best-practices/nodejs.md
.claude/best-practices/typescript.md
.claude/best-practices/database.md
```

### Step 4: 구현 계획 수립

```
============================================
[IMPLEMENT] 구현 계획
============================================

 태스크: {task-id} - {task-description}

 적용할 베스트 프랙티스:
• React: Function Component + Custom Hook
• TypeScript: Strict Types
• Node.js: Layered Architecture

 생성할 파일:
1. src/features/{feature}/types/{name}.types.ts
2. src/features/{feature}/services/{name}Service.ts
3. src/features/{feature}/hooks/use{Name}.ts
4. src/features/{feature}/components/{Name}.tsx

 구현 순서:
1. 타입 정의
2. 서비스 레이어
3. 커스텀 훅
4. 컴포넌트
5. 테스트

============================================
이 계획으로 진행할까요?
```

### Step 5: 코드 생성

베스트 프랙티스 적용하여 코드 생성:

#### 5.1 타입 정의

```typescript
// src/features/{feature}/types/{name}.types.ts

/**
 * {설명}
 */
export interface {Name} {
  id: string;
  // ...
}
```

#### 5.2 서비스 레이어

```typescript
// src/features/{feature}/services/{name}Service.ts

/**
 * {Name} 관련 API 서비스
 */
export class {Name}Service {
  /**
   * {Name} 조회
   * @param id - {Name} ID
   * @returns {Name} 데이터
   */
  async findById(id: string): Promise<{Name}> {
    // 구현
  }
}
```

#### 5.3 커스텀 훅

```typescript
// src/features/{feature}/hooks/use{Name}.ts

/**
 * {Name} 관련 커스텀 훅
 */
export const use{Name} = (id: string) => {
  // React Query 또는 useState 사용
};
```

#### 5.4 컴포넌트

```tsx
// src/features/{feature}/components/{Name}.tsx

interface {Name}Props {
  // props 정의
}

/**
 * {Name} 컴포넌트
 * @description {설명}
 */
export const {Name}: React.FC<{Name}Props> = (props) => {
  // 구현
};
```

### Step 6: 코드 품질 검증

자동 검증 (code_quality_validator.py):

- [ ] 파일 300줄 이하
- [ ] 모든 함수에 JSDoc 주석
- [ ] 타입 정의 완전성
- [ ] 네이밍 규칙 준수

### Step 7: 진행 상황 업데이트

`docs/tasks/{feature}/progress.md` 업데이트:

```markdown
## 구현 진행 상황

### 완료된 태스크
- [x] TASK-001: User 타입 정의

### 진행 중
- [ ] TASK-002: UserService 구현 (70%)

### 대기 중
- [ ] TASK-003: 로그인 컴포넌트
```

### Step 8: 완료 보고

```
============================================
[IMPLEMENT] 구현 완료
============================================

 태스크: {task-id} - {task-description}

 생성된 파일:
• src/features/{feature}/types/{name}.types.ts
• src/features/{feature}/services/{name}Service.ts

 적용된 패턴:
• Layered Architecture
• TypeScript Strict Mode
• JSDoc Comments

 품질 검증:
• 줄 수: OK (120줄)
• 함수 주석: OK (5/5)

 다음 태스크: TASK-002

============================================
```

## 코드 품질 규칙

구현 시 반드시 준수:

1. **300줄 제한**: 파일당 300줄 이하
2. **주석 필수**: 모든 함수에 JSDoc 주석
3. **타입 안전성**: any 사용 금지
4. **에러 처리**: 적절한 에러 처리 포함
5. **네이밍**: 해당 기술의 컨벤션 준수

## 참조 파일

- `.claude/best-practices/` - 기술별 베스트 프랙티스
- `.claude/memory/CODE_STYLE.md` - 코드 스타일 규칙
- `.claude/memory/TECH_STACK.md` - 기술 스택
