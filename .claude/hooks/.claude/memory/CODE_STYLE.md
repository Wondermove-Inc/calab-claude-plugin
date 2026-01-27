# 코드 스타일 규칙

> 이 규칙들은 **모든 코드 생성에서 반드시 준수**해야 합니다.
> 위반 시 PostToolUse Hook이 자동으로 경고합니다.

---

## 절대 규칙 (위반 시 경고)

### 1. 파일 줄 수 제한

```
최대 줄 수: 500줄
권장 줄 수: 150-200줄
경고 임계값: 250줄
```

**500줄 초과 시 필수 조치:**
- 파일을 논리적 단위로 분리
- 유틸리티 함수는 별도 파일로 추출
- 클래스가 여러 개면 각각 분리
- 타입 정의는 types 파일로 분리

**분리 기준:**
```
1. 기능별 분리: auth.ts, profile.ts, permission.ts
2. 레이어별 분리: service.ts, repository.ts, controller.ts
3. 타입 분리: types.ts, interfaces.ts
4. 유틸리티 분리: utils.ts, helpers.ts
```

### 2. 주석 필수 요건

#### 함수/메서드 주석 (필수)

**TypeScript/JavaScript:**
```typescript
/**
 * 사용자 ID로 사용자 정보를 조회합니다.
 *
 * @param userId - 조회할 사용자의 고유 ID
 * @returns 사용자 객체 또는 존재하지 않으면 null
 * @throws DatabaseError 데이터베이스 연결 실패 시
 *
 * @example
 * const user = await getUserById('user-123');
 */
async function getUserById(userId: string): Promise<User | null> {
```

**Python:**
```python
async def get_user_by_id(user_id: str) -> Optional[User]:
    """
    사용자 ID로 사용자 정보를 조회합니다.

    Args:
        user_id: 조회할 사용자의 고유 ID

    Returns:
        User 객체 또는 존재하지 않으면 None

    Raises:
        DatabaseError: 데이터베이스 연결 실패 시
    """
```

#### 복잡한 로직 주석 (필수)

다음 경우 반드시 설명 주석 추가:
- 조건문 3개 이상
- 중첩 루프 2단계 이상
- 정규식 사용
- 비즈니스 로직
- 알고리즘 구현

```typescript
// 가격 계산 로직:
// 1. 기본 가격에서 할인율 적용
// 2. 멤버십 등급별 추가 할인
// 3. 쿠폰 적용 (중복 불가)
// 4. 최종 가격은 100원 단위로 반올림
const finalPrice = calculateFinalPrice(basePrice, discountRate, membership, coupon);
```

---

## 권장 규칙

### 3. 함수 길이

```
최대 줄 수: 50줄
권장 줄 수: 20-30줄
```

50줄 초과 시 함수 분리 고려:
- 유효성 검증 → validateXxx()
- 데이터 변환 → transformXxx()
- 에러 처리 → handleXxxError()

### 4. 파일 구조

```typescript
// ===== 1. 임포트 =====
import { ... } from 'external-lib';      // 외부 라이브러리
import { ... } from '@/internal';        // 내부 모듈 (절대 경로)
import { ... } from './local';           // 상대 경로
import type { ... } from './types';      // 타입 임포트

// ===== 2. 타입/인터페이스 정의 =====
interface User { ... }
type UserRole = 'admin' | 'user';

// ===== 3. 상수 정의 =====
const MAX_RETRY = 3;
const DEFAULT_TIMEOUT = 5000;

// ===== 4. 유틸리티 함수 (private) =====
function validateInput(input: string): boolean { ... }

// ===== 5. 메인 로직 (export) =====
export async function mainFunction() { ... }
export class MainClass { ... }
```

### 5. 네이밍 규칙

```
파일명:      kebab-case        (user-service.ts)
클래스:      PascalCase        (UserService)
함수/메서드: camelCase         (getUserById)
상수:        UPPER_SNAKE_CASE  (MAX_RETRY_COUNT)
타입:        PascalCase        (UserResponse)
인터페이스:  PascalCase + I    (IUserRepository) - 선택
```

---

## 체크리스트

코드 작성 완료 후 자체 검증:

- [ ] 파일이 500줄 이하인가?
- [ ] 모든 public 함수에 JSDoc/Docstring이 있는가?
- [ ] 복잡한 로직에 설명 주석이 있는가?
- [ ] 함수가 50줄 이하인가?
- [ ] 매직 넘버 대신 상수를 사용했는가?
- [ ] 파일 구조가 일관성 있는가?

---

## 위반 시 자동 처리

### PostToolUse Hook 동작

1. **500줄 초과**: 즉시 경고 + 분리 권고
2. **250줄 이상**: 경고 + 주의 메시지
3. **주석 누락**: 함수 목록과 함께 경고

### 수동 검사

```
/check-quality
```

프로젝트 전체 소스 파일 스캔하여 위반 사항 보고

---

*이 파일은 code-quality 스킬과 code_quality_validator.py 훅에서 참조됩니다.*
