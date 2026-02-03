# API 설계 베스트 프랙티스 (2025)

> 이 문서는 REST API 설계 시 **반드시** 참조해야 합니다.

---

## 1. RESTful 원칙

### 리소스 기반 URL

```
Good:
GET    /users           → 사용자 목록
GET    /users/{id}      → 특정 사용자
POST   /users           → 사용자 생성
PUT    /users/{id}      → 사용자 전체 수정
PATCH  /users/{id}      → 사용자 부분 수정
DELETE /users/{id}      → 사용자 삭제

Bad:
GET    /getUsers
POST   /createUser
POST   /deleteUser/{id}
```

### 중첩 리소스

```
GET    /users/{userId}/orders         → 사용자의 주문 목록
POST   /users/{userId}/orders         → 주문 생성
GET    /users/{userId}/orders/{id}    → 특정 주문
```

### 컬렉션 vs 단일 리소스

```
/users      → 복수형 (컬렉션)
/users/{id} → 단수 리소스
/me         → 현재 사용자 (특수 케이스)
```

---

## 2. HTTP 메서드

| 메서드 | 용도 | 멱등성 | 안전성 |
|--------|------|--------|--------|
| GET | 조회 | Yes | Yes |
| POST | 생성 | No | No |
| PUT | 전체 수정 | Yes | No |
| PATCH | 부분 수정 | No | No |
| DELETE | 삭제 | Yes | No |

---

## 3. 상태 코드

### 성공 (2xx)

```
200 OK           → GET, PUT, PATCH 성공
201 Created      → POST 성공 (리소스 생성)
204 No Content   → DELETE 성공 (응답 바디 없음)
```

### 클라이언트 에러 (4xx)

```
400 Bad Request      → 잘못된 요청 (유효성 검증 실패)
401 Unauthorized     → 인증 필요
403 Forbidden        → 권한 없음
404 Not Found        → 리소스 없음
409 Conflict         → 충돌 (중복 등)
422 Unprocessable    → 처리 불가 (비즈니스 규칙 위반)
429 Too Many Requests → 요청 제한 초과
```

### 서버 에러 (5xx)

```
500 Internal Server Error → 서버 에러
502 Bad Gateway          → 업스트림 에러
503 Service Unavailable  → 서비스 일시 중단
504 Gateway Timeout      → 타임아웃
```

---

## 4. 요청/응답 형식

### 성공 응답

```json
// 단일 리소스
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2024-01-15T09:30:00Z"
  }
}

// 컬렉션
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 에러 응답

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}
```

### TypeScript 타입

```typescript
/**
 * API 성공 응답
 */
interface ApiResponse<T> {
  data: T;
}

/**
 * 페이지네이션 응답
 */
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

/**
 * API 에러 응답
 */
interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Array<{
      field: string;
      message: string;
    }>;
  };
}
```

---

## 5. 쿼리 파라미터

### 페이지네이션

```
GET /users?page=1&limit=20

// Offset 기반
GET /users?offset=0&limit=20

// Cursor 기반 (대용량)
GET /users?cursor=abc123&limit=20
```

### 필터링

```
GET /users?status=active
GET /users?role=admin&status=active
GET /orders?createdAt[gte]=2024-01-01&createdAt[lt]=2024-02-01
```

### 정렬

```
GET /users?sort=createdAt:desc
GET /users?sort=name:asc,createdAt:desc
```

### 필드 선택

```
GET /users?fields=id,name,email
GET /users?include=orders,profile
```

---

## 6. 버저닝

### URL 버저닝 (권장)

```
/api/v1/users
/api/v2/users
```

### 헤더 버저닝

```
Accept: application/vnd.api+json;version=1
```

---

## 7. 인증

### Bearer Token

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 구현 예시

```typescript
// middleware/auth.ts
export const authMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Authentication required',
      },
    });
  }

  try {
    const payload = await verifyToken(token);
    req.user = payload;
    next();
  } catch {
    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid or expired token',
      },
    });
  }
};
```

---

## 8. Rate Limiting

### 헤더

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

### 429 응답

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
```

---

## 9. API 문서화

### OpenAPI 스키마

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
```

---

## 10. 금지 사항

- [ ] 동사 기반 URL (/getUsers)
- [ ] 일관되지 않은 응답 형식
- [ ] 에러 시 200 응답
- [ ] 민감 정보 노출 (비밀번호, 토큰)
- [ ] 버저닝 없이 Breaking Change
- [ ] 문서화 없는 API

---

## 11. 체크리스트

API 설계 시 확인:

- [ ] RESTful URL 구조
- [ ] 적절한 HTTP 메서드
- [ ] 적절한 상태 코드
- [ ] 일관된 응답 형식
- [ ] 페이지네이션 구현
- [ ] 에러 처리 표준화
- [ ] API 문서화 (OpenAPI)
