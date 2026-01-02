---
description: 태스크를 구현합니다. 베스트 프랙티스를 적용하여 코드를 생성합니다. --tdd 옵션으로 TDD 모드 실행.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [task-id] [--tdd]
---

# 구현 (Build)

## 목적

태스크를 베스트 프랙티스에 따라 구현합니다.

## 옵션

| 옵션 | 설명 |
|------|------|
| `--tdd` | TDD 모드로 구현 (테스트 먼저 작성) |

## 실행 절차

### Step 1: 컨텍스트 로드

```
1. .claude/memory/CURRENT_CONTEXT.md - 현재 작업 상태
2. .claude/memory/TECH_STACK.md - 기술 스택
3. .claude-state/worktree.json - 태스크 상태
4. docs/prd/{feature}/prd.md - 요구사항
5. docs/architecture/ - 설계 문서
```

### Step 2: 태스크 식별

$ARGUMENTS에서 태스크 ID 파악:

```
TASK-001: User 테이블 마이그레이션
```

### Step 3: 🚨 Worktree 상태 업데이트 (필수)

> **MUST**: 이 단계는 **반드시 즉시 실행**해야 합니다. 건너뛰지 마세요!

**태스크 시작 시 Edit 도구로 `.claude-state/worktree.json` 직접 수정:**

1. worktree.json 파일 읽기
2. 해당 태스크의 `status`를 `"in_progress"`로 변경
3. `started_at`에 현재 시간 추가
4. `current_task` 필드 업데이트
5. 파일 저장

```json
{
  "current_task": "TASK-001",
  "epics": [
    {
      "stories": [
        {
          "tasks": [
            {
              "id": "TASK-001",
              "status": "in_progress",
              "started_at": "2024-01-15T09:00:00Z"
            }
          ]
        }
      ]
    }
  ],
  "progress": {
    "in_progress": 1
  }
}
```

**검증**: Edit 완료 후 worktree.json의 status가 변경되었는지 확인

### Step 4: 베스트 프랙티스 로드

기술 스택에 따라 베스트 프랙티스 로드:

```
.claude/best-practices/react.md
.claude/best-practices/nodejs.md
.claude/best-practices/typescript.md
.claude/best-practices/testing.md
```

**자동 활성화 스킬 (모두 필수 로드):**
| 스킬 | 역할 |
|------|------|
| `clean-architecture` | **4-레이어 구조 강제** |
| `best-practices` | 기술별 패턴 적용 |
| `code-quality` | 300줄 제한, 주석 필수 |
| `work-tracker` | 태스크 상태 자동 추적 |

### 🚨 클린 아키텍처 필수 체크 (구현 전)

> **CRITICAL**: 코드 생성 전 반드시 확인!

```
skills/clean-architecture/SKILL.md 로드
→ 파일 위치가 올바른 레이어인지 확인
→ import 경로가 의존성 규칙 준수하는지 확인
```

**레이어별 파일 위치:**
| 레이어 | 경로 | 허용 import |
|--------|------|-------------|
| Domain | `src/domain/` | 없음 (순수) |
| Application | `src/application/` | Domain만 |
| Adapters | `src/adapters/` | Domain, Application |
| Infrastructure | `src/infrastructure/` | 모두 가능 |

### Step 5: 구현 계획 수립

```
============================================
[BUILD] 구현 계획
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

 구현 순서 (일반 모드):
1. 타입 정의
2. 서비스 레이어
3. 커스텀 훅
4. 컴포넌트
5. 테스트

 구현 순서 (TDD 모드 --tdd):
1. 테스트 작성 (RED)
2. 최소 구현 (GREEN)
3. 리팩토링 (REFACTOR)
4. 반복

============================================
이 계획으로 진행할까요?
```

---

## TDD 모드 (--tdd 옵션)

### TDD 사이클 1: RED (실패하는 테스트)

```typescript
// {name}.service.test.ts
describe('{Name}Service', () => {
  describe('{method}', () => {
    it('should {expected behavior}', () => {
      // Arrange
      const service = new {Name}Service();

      // Act
      const result = service.{method}(input);

      // Assert - 아직 구현 없음, 테스트 실패
      expect(result).toBe(expected);
    });
  });
});
```

```
============================================
[BUILD:TDD] RED - 테스트 작성 완료
============================================

 테스트 파일: src/features/{feature}/__tests__/{name}.service.test.ts
 테스트 케이스: 3개 작성
 상태: ❌ FAILING (예상대로)

 다음 단계: GREEN (최소 구현)

============================================
```

### TDD 사이클 2: GREEN (최소 구현)

```
============================================
[BUILD:TDD] GREEN - 테스트 통과
============================================

 테스트 결과: ✅ 3/3 통과
 구현 파일: src/features/{feature}/services/{name}.service.ts

 다음 단계: REFACTOR (코드 개선)

============================================
```

### TDD 사이클 3: REFACTOR (리팩토링)

```
============================================
[BUILD:TDD] REFACTOR - 코드 개선
============================================

 개선 사항:
• 중복 코드 제거
• 명확한 변수명
• 에러 처리 추가
• JSDoc 주석 추가

 테스트 결과: ✅ 여전히 3/3 통과

 다음: 새로운 기능 추가 시 RED부터 반복

============================================
```

---

## 일반 모드 코드 생성

### 타입 정의

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

### 서비스 레이어

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

---

## 코드 품질 검증

자동 검증:

- [ ] 파일 300줄 이하
- [ ] 모든 함수에 JSDoc 주석
- [ ] 타입 정의 완전성
- [ ] 네이밍 규칙 준수

---

## 🚨 완료 검증 (필수 - 이 단계를 건너뛰지 마세요!)

> **CRITICAL**: 구현 후 **반드시 완료 검증을 수행**해야 합니다. 검증 없이 완료 처리하지 마세요!

### Step 6: Acceptance Criteria 검증 (필수)

**worktree.json에서 해당 Task의 acceptance_criteria를 읽고 하나씩 검증:**

```
============================================
[TASK 완료 검증] {task-id}
============================================

📋 Acceptance Criteria 검증:
□ AC1: {첫 번째 조건}
  → 검증: {어떻게 확인했는지}
  → 결과: ✅ 충족 / ❌ 미충족

□ AC2: {두 번째 조건}
  → 검증: {어떻게 확인했는지}
  → 결과: ✅ 충족 / ❌ 미충족

...

🔍 기능 동작 검증:
□ 코드 컴파일/빌드 성공 여부
□ 기본 시나리오 동작 여부
□ 에러 처리 구현 여부

🛡️ 엣지 케이스 검증:
□ 빈 값/null/undefined 처리
□ 잘못된 입력 처리
□ 경계값 처리

📊 코드 품질 검증:
□ 파일 300줄 이하
□ 모든 함수에 JSDoc 주석
□ 타입 정의 완전성

============================================
최종 결과: ✅ 모두 충족 / ❌ 미충족 항목 있음
============================================
```

### Step 7: 미충족 시 추가 구현 (반복)

**❌ 미충족 항목이 있으면:**
1. 해당 항목 추가 구현
2. Step 6 재실행
3. 모든 항목 ✅ 될 때까지 반복

**⚠️ 절대로 미충족 상태에서 다음 Task로 넘어가지 마세요!**

### Step 8: 완료 처리 (검증 통과 후에만)

> **MUST**: **Step 6 검증이 모두 통과한 후에만** 완료 처리!

**태스크 완료 시 Edit 도구로 `.claude-state/worktree.json` 직접 수정:**

1. worktree.json 파일 읽기
2. 해당 태스크의 `status`를 `"done"`으로 변경
3. `completed_at`에 현재 시간 추가
4. `progress` 필드의 `done` 카운트 증가, `in_progress` 감소
5. `percentage` 재계산
6. 파일 저장

```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "status": "done",
      "started_at": "2024-01-15T09:00:00Z",
      "completed_at": "2024-01-15T10:30:00Z"
    }
  ],
  "progress": {
    "done": 1,
    "in_progress": 0,
    "percentage": 10
  }
}
```

---

## 완료 보고

```
============================================
[BUILD] 구현 완료
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

 ✅ Worktree 업데이트 완료:
• status: in_progress → done
• completed_at: {timestamp}
• progress.done: +1

 다음 태스크: /dev build TASK-002

============================================
```

## 코드 품질 규칙

1. **300줄 제한**: 파일당 300줄 이하
2. **주석 필수**: 모든 함수에 JSDoc 주석
3. **타입 안전성**: any 사용 금지
4. **에러 처리**: 적절한 에러 처리 포함
5. **네이밍**: 해당 기술의 컨벤션 준수

## 참조 파일

- `.claude/best-practices/` - 기술별 베스트 프랙티스
- `.claude/best-practices/testing.md` - TDD 가이드
- `.claude/memory/TECH_STACK.md` - 기술 스택
- `.claude-state/worktree.json` - 작업 상태
