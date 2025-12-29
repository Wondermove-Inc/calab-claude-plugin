# API 스펙: {기능명}

## 문서 정보

| 항목 | 내용 |
|------|------|
| 작성일 | {날짜} |
| Base URL | /api/v1 |
| 인증 | Bearer Token |

---

## 엔드포인트 목록

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /{resource} | 목록 조회 |
| GET | /{resource}/{id} | 상세 조회 |
| POST | /{resource} | 생성 |
| PUT | /{resource}/{id} | 전체 수정 |
| PATCH | /{resource}/{id} | 부분 수정 |
| DELETE | /{resource}/{id} | 삭제 |

---

## 공통 사항

### 인증

모든 API는 Bearer Token 인증이 필요합니다.

```
Authorization: Bearer {token}
```

### 응답 형식

**성공 응답**:
```json
{
  "data": { ... }
}
```

**에러 응답**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": [ ... ]
  }
}
```

### 페이지네이션

```
GET /{resource}?page=1&limit=20
```

```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

---

## 상세 API 스펙

### 1. {Resource} 목록 조회

**Endpoint**: `GET /{resource}`

**Query Parameters**:

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| page | number | N | 페이지 번호 (기본: 1) |
| limit | number | N | 페이지당 개수 (기본: 20) |
| sort | string | N | 정렬 (예: createdAt:desc) |
| status | string | N | 상태 필터 |

**Response (200 OK)**:

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Example",
      "createdAt": "2024-01-15T09:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

---

### 2. {Resource} 상세 조회

**Endpoint**: `GET /{resource}/{id}`

**Path Parameters**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| id | uuid | 리소스 ID |

**Response (200 OK)**:

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Example",
    "description": "Description text",
    "createdAt": "2024-01-15T09:30:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

| 상태 코드 | 코드 | 설명 |
|----------|------|------|
| 404 | NOT_FOUND | 리소스를 찾을 수 없음 |

---

### 3. {Resource} 생성

**Endpoint**: `POST /{resource}`

**Request Body**:

```json
{
  "name": "New Resource",
  "description": "Description text"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name | string | Y | 이름 (max 200) |
| description | string | N | 설명 |

**Response (201 Created)**:

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "New Resource",
    "description": "Description text",
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

**Error Responses**:

| 상태 코드 | 코드 | 설명 |
|----------|------|------|
| 400 | VALIDATION_ERROR | 유효성 검사 실패 |
| 409 | CONFLICT | 중복된 리소스 |

---

### 4. {Resource} 수정

**Endpoint**: `PUT /{resource}/{id}`

**Request Body**:

```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Response (200 OK)**:

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Name",
    "description": "Updated description",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

---

### 5. {Resource} 삭제

**Endpoint**: `DELETE /{resource}/{id}`

**Response (204 No Content)**:

빈 응답

**Error Responses**:

| 상태 코드 | 코드 | 설명 |
|----------|------|------|
| 404 | NOT_FOUND | 리소스를 찾을 수 없음 |
| 409 | CONFLICT | 삭제할 수 없음 (연관 데이터) |

---

## 에러 코드

| 코드 | HTTP 상태 | 설명 |
|------|----------|------|
| VALIDATION_ERROR | 400 | 입력 데이터 유효성 오류 |
| UNAUTHORIZED | 401 | 인증 필요 |
| FORBIDDEN | 403 | 권한 없음 |
| NOT_FOUND | 404 | 리소스 없음 |
| CONFLICT | 409 | 충돌 (중복 등) |
| INTERNAL_ERROR | 500 | 서버 내부 오류 |

---

## TypeScript 타입

```typescript
// Request Types
interface Create{Resource}Dto {
  name: string;
  description?: string;
}

interface Update{Resource}Dto {
  name?: string;
  description?: string;
}

// Response Types
interface {Resource} {
  id: string;
  name: string;
  description: string | null;
  createdAt: Date;
  updatedAt: Date;
}

interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

---

## Rate Limiting

| 엔드포인트 | 제한 |
|-----------|------|
| 인증 API | 10 req/min |
| 읽기 API | 100 req/min |
| 쓰기 API | 30 req/min |

---

*참조: `.claude/best-practices/api-design.md`*
