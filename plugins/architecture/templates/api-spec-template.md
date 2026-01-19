# API 스펙: {기능명}

## 문서 정보

| 항목 | 내용 |
|------|------|
| 작성자 | {작성자} |
| 작성일 | {날짜} |
| 버전 | v1.0 |
| 상태 | Draft / Review / Approved |
| Base URL | `/api/v1` |
| 인증 방식 | Bearer Token (JWT) |

---

## 목차

1. [개요](#1-개요)
2. [인증 및 권한](#2-인증-및-권한)
3. [공통 규격](#3-공통-규격)
4. [엔드포인트 목록](#4-엔드포인트-목록)
5. [상세 API 스펙](#5-상세-api-스펙)
6. [에러 코드](#6-에러-코드)
7. [TypeScript 타입](#7-typescript-타입)
8. [Rate Limiting](#8-rate-limiting)
9. [버저닝 전략](#9-버저닝-전략)
10. [체크리스트](#10-체크리스트)

---

## 1. 개요

### 1.1 문서 목적

이 문서는 {기능명} 관련 REST API의 상세 스펙을 정의합니다.

### 1.2 API 설계 원칙

| 원칙 | 설명 | 예시 |
|------|------|------|
| **RESTful** | 리소스 중심 설계 | `GET /users/:id` |
| **일관성** | 동일한 패턴 유지 | 모든 리소스 CRUD 동일 구조 |
| **멱등성** | GET, PUT, DELETE 멱등 | 동일 요청 반복해도 결과 동일 |
| **HATEOAS** | 하이퍼미디어 링크 제공 | 선택적 적용 |

### 1.3 HTTP 메서드 의미

| 메서드 | 용도 | 멱등성 | Safe |
|--------|------|--------|------|
| `GET` | 리소스 조회 | Yes | Yes |
| `POST` | 리소스 생성 | No | No |
| `PUT` | 리소스 전체 수정 | Yes | No |
| `PATCH` | 리소스 부분 수정 | No | No |
| `DELETE` | 리소스 삭제 | Yes | No |

### 1.4 URL 명명 규칙

```
# 좋은 예시
GET    /api/v1/users                    # 목록 조회
GET    /api/v1/users/:id                # 단일 조회
POST   /api/v1/users                    # 생성
PUT    /api/v1/users/:id                # 전체 수정
PATCH  /api/v1/users/:id                # 부분 수정
DELETE /api/v1/users/:id                # 삭제
GET    /api/v1/users/:id/orders         # 중첩 리소스

# 나쁜 예시
GET    /api/v1/getUser                  # 동사 사용 X
POST   /api/v1/user/create              # 동사 사용 X
GET    /api/v1/User                     # 대문자 사용 X
GET    /api/v1/user-list                # 단수/복수 혼용 X
```

---

## 2. 인증 및 권한

### 2.1 인증 방식

#### Bearer Token (JWT)

모든 API는 `Authorization` 헤더를 통한 Bearer Token 인증이 필요합니다.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Token 구조 (JWT Payload)

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "role": "user",
  "iat": 1700000000,
  "exp": 1700086400
}
```

### 2.2 인증 플로우

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Server
    participant R as Resource Server

    C->>A: POST /auth/login (email, password)
    A-->>C: { accessToken, refreshToken }
    C->>R: GET /api/v1/users (Authorization: Bearer token)
    R-->>C: { data: [...] }

    Note over C,R: Token 만료 시
    C->>A: POST /auth/refresh (refreshToken)
    A-->>C: { accessToken, refreshToken }
```

### 2.3 권한 레벨

| 역할 | 코드 | 권한 |
|------|------|------|
| **Guest** | - | 공개 API만 접근 가능 |
| **User** | `user` | 자신의 리소스 CRUD |
| **Seller** | `seller` | 상품/주문 관리 |
| **Admin** | `admin` | 모든 리소스 관리 |
| **Super Admin** | `super_admin` | 시스템 설정 포함 전체 |

### 2.4 권한 체크 표시

각 API에 필요한 권한을 다음과 같이 표시:

| 표시 | 의미 |
|------|------|
| `🔓 Public` | 인증 불필요 |
| `🔐 Auth` | 인증 필요 (모든 역할) |
| `👤 Owner` | 리소스 소유자만 |
| `🛡️ Admin` | 관리자만 |

---

## 3. 공통 규격

### 3.1 요청 형식

#### Content-Type

```http
Content-Type: application/json
```

#### 쿼리 파라미터 명명

```
# camelCase 사용
GET /users?sortBy=createdAt&orderBy=desc

# 배열 파라미터
GET /products?categoryIds=1,2,3
GET /products?categoryIds[]=1&categoryIds[]=2
```

### 3.2 응답 형식

#### 성공 응답 (단일)

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "홍길동",
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

#### 성공 응답 (목록)

```json
{
  "data": [
    { "id": "...", "name": "..." },
    { "id": "...", "name": "..." }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

#### 성공 응답 (HATEOAS 적용 시)

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  },
  "_links": {
    "self": { "href": "/api/v1/users/550e8400-e29b-41d4-a716-446655440000" },
    "orders": { "href": "/api/v1/users/550e8400-e29b-41d4-a716-446655440000/orders" }
  }
}
```

#### 에러 응답 (RFC 7807 표준)

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "입력 데이터가 유효하지 않습니다.",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "올바른 이메일 형식이 아닙니다."
    },
    {
      "field": "password",
      "code": "TOO_SHORT",
      "message": "비밀번호는 최소 8자 이상이어야 합니다."
    }
  ],
  "timestamp": "2024-01-15T09:30:00Z",
  "traceId": "abc123def456"
}
```

### 3.3 페이지네이션

#### Offset 기반 (기본)

```http
GET /api/v1/users?page=1&limit=20&sortBy=createdAt&order=desc
```

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| page | number | 1 | 페이지 번호 (1부터 시작) |
| limit | number | 20 | 페이지당 개수 (max: 100) |
| sortBy | string | createdAt | 정렬 필드 |
| order | string | desc | 정렬 방향 (asc/desc) |

#### Cursor 기반 (대용량)

```http
GET /api/v1/users?cursor=eyJpZCI6IjEyMyIsImNyZWF0ZWRBdCI6IjIwMjQtMDEtMTUifQ&limit=20
```

```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "nextCursor": "eyJpZCI6IjE1MCIsImNyZWF0ZWRBdCI6IjIwMjQtMDEtMTAifQ",
    "prevCursor": "eyJpZCI6IjEzMCIsImNyZWF0ZWRBdCI6IjIwMjQtMDEtMTIifQ",
    "hasNext": true,
    "hasPrev": true
  }
}
```

### 3.4 필터링

#### 단순 필터

```http
GET /api/v1/products?category=electronics&isActive=true
```

#### 범위 필터

```http
GET /api/v1/products?minPrice=1000&maxPrice=5000
GET /api/v1/orders?startDate=2024-01-01&endDate=2024-01-31
```

#### 검색

```http
GET /api/v1/products?search=키보드
GET /api/v1/products?q=키보드&searchFields=name,description
```

### 3.5 필드 선택 (Sparse Fieldsets)

```http
GET /api/v1/users?fields=id,name,email
GET /api/v1/users?include=orders,addresses
```

### 3.6 날짜/시간 형식

모든 날짜/시간은 **ISO 8601** 형식을 사용:

```
2024-01-15T09:30:00Z        # UTC
2024-01-15T18:30:00+09:00   # 타임존 포함
2024-01-15                  # 날짜만
```

---

## 4. 엔드포인트 목록

### 4.1 {리소스명} API

| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| `GET` | `/api/v1/{resource}` | 목록 조회 | 🔐 Auth |
| `GET` | `/api/v1/{resource}/:id` | 상세 조회 | 🔐 Auth |
| `POST` | `/api/v1/{resource}` | 생성 | 🔐 Auth |
| `PUT` | `/api/v1/{resource}/:id` | 전체 수정 | 👤 Owner |
| `PATCH` | `/api/v1/{resource}/:id` | 부분 수정 | 👤 Owner |
| `DELETE` | `/api/v1/{resource}/:id` | 삭제 | 👤 Owner |

### 4.2 인증 API

| Method | Endpoint | 설명 | 권한 |
|--------|----------|------|------|
| `POST` | `/api/v1/auth/register` | 회원가입 | 🔓 Public |
| `POST` | `/api/v1/auth/login` | 로그인 | 🔓 Public |
| `POST` | `/api/v1/auth/logout` | 로그아웃 | 🔐 Auth |
| `POST` | `/api/v1/auth/refresh` | 토큰 갱신 | 🔓 Public |
| `POST` | `/api/v1/auth/forgot-password` | 비밀번호 찾기 | 🔓 Public |
| `POST` | `/api/v1/auth/reset-password` | 비밀번호 재설정 | 🔓 Public |

---

## 5. 상세 API 스펙

### 5.1 {Resource} 목록 조회

**`GET /api/v1/{resource}`** `🔐 Auth`

> {리소스} 목록을 페이지네이션하여 조회합니다.

#### Request

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|---------|------|------|--------|------|------|
| page | integer | N | 1 | 페이지 번호 | 1 |
| limit | integer | N | 20 | 페이지당 개수 (1-100) | 20 |
| sortBy | string | N | createdAt | 정렬 필드 | createdAt, name |
| order | string | N | desc | 정렬 방향 | asc, desc |
| status | string | N | - | 상태 필터 | active, inactive |
| search | string | N | - | 검색어 | 키워드 |

**Headers:**

```http
Authorization: Bearer {token}
Accept: application/json
```

#### Response

**200 OK:**

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Example",
      "status": "active",
      "createdAt": "2024-01-15T09:30:00Z",
      "updatedAt": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

**401 Unauthorized:**

```json
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "유효하지 않은 토큰입니다.",
  "instance": "/api/v1/{resource}"
}
```

---

### 5.2 {Resource} 상세 조회

**`GET /api/v1/{resource}/:id`** `🔐 Auth`

> 특정 {리소스}의 상세 정보를 조회합니다.

#### Request

**Path Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| id | uuid | Y | 리소스 ID |

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| include | string | N | 포함할 관계 (orders,addresses) |

#### Response

**200 OK:**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Example",
    "description": "상세 설명",
    "status": "active",
    "metadata": {
      "key": "value"
    },
    "createdAt": "2024-01-15T09:30:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**404 Not Found:**

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "요청한 리소스를 찾을 수 없습니다.",
  "instance": "/api/v1/{resource}/invalid-id"
}
```

---

### 5.3 {Resource} 생성

**`POST /api/v1/{resource}`** `🔐 Auth`

> 새로운 {리소스}를 생성합니다.

#### Request

**Headers:**

```http
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "New Resource",
  "description": "설명 텍스트",
  "categoryId": "123e4567-e89b-12d3-a456-426614174000",
  "metadata": {
    "key": "value"
  }
}
```

| 필드 | 타입 | 필수 | 제약조건 | 설명 |
|------|------|------|---------|------|
| name | string | Y | 2-200자 | 이름 |
| description | string | N | max 2000자 | 설명 |
| categoryId | uuid | N | valid UUID | 카테고리 ID |
| metadata | object | N | - | 추가 메타데이터 |

#### Response

**201 Created:**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "New Resource",
    "description": "설명 텍스트",
    "categoryId": "123e4567-e89b-12d3-a456-426614174000",
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

**Headers:**

```http
Location: /api/v1/{resource}/550e8400-e29b-41d4-a716-446655440000
```

**400 Bad Request:**

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "입력 데이터가 유효하지 않습니다.",
  "instance": "/api/v1/{resource}",
  "errors": [
    {
      "field": "name",
      "code": "REQUIRED",
      "message": "이름은 필수 입력 항목입니다."
    }
  ]
}
```

**409 Conflict:**

```json
{
  "type": "https://api.example.com/errors/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "이미 존재하는 리소스입니다.",
  "instance": "/api/v1/{resource}"
}
```

---

### 5.4 {Resource} 전체 수정

**`PUT /api/v1/{resource}/:id`** `👤 Owner`

> {리소스}의 전체 정보를 수정합니다. (모든 필드 필수)

#### Request

**Request Body:**

```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "categoryId": "123e4567-e89b-12d3-a456-426614174000",
  "status": "active"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name | string | Y | 이름 |
| description | string | Y | 설명 (빈 문자열 허용) |
| categoryId | uuid | Y | 카테고리 (null 허용) |
| status | string | Y | 상태 |

#### Response

**200 OK:**

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

### 5.5 {Resource} 부분 수정

**`PATCH /api/v1/{resource}/:id`** `👤 Owner`

> {리소스}의 일부 정보만 수정합니다. (변경할 필드만 전송)

#### Request

**Request Body:**

```json
{
  "name": "Partially Updated Name"
}
```

#### Response

**200 OK:**

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Partially Updated Name",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

---

### 5.6 {Resource} 삭제

**`DELETE /api/v1/{resource}/:id`** `👤 Owner`

> {리소스}를 삭제합니다. (Soft Delete)

#### Response

**204 No Content:**

(빈 응답)

**409 Conflict:**

```json
{
  "type": "https://api.example.com/errors/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "연관된 데이터가 있어 삭제할 수 없습니다.",
  "instance": "/api/v1/{resource}/550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 5.7 벌크 작업 (Bulk Operations)

#### 벌크 생성

**`POST /api/v1/{resource}/bulk`** `🔐 Auth`

```json
{
  "items": [
    { "name": "Item 1", "description": "..." },
    { "name": "Item 2", "description": "..." }
  ]
}
```

**Response (207 Multi-Status):**

```json
{
  "results": [
    { "index": 0, "status": 201, "data": { "id": "..." } },
    { "index": 1, "status": 400, "error": { "message": "Validation failed" } }
  ],
  "summary": {
    "total": 2,
    "success": 1,
    "failed": 1
  }
}
```

#### 벌크 삭제

**`DELETE /api/v1/{resource}/bulk`** `🛡️ Admin`

```json
{
  "ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ]
}
```

---

## 6. 에러 코드

### 6.1 HTTP 상태 코드

| 코드 | 이름 | 설명 | 사용 시점 |
|------|------|------|----------|
| 200 | OK | 성공 | GET, PUT, PATCH 성공 |
| 201 | Created | 생성 성공 | POST 성공 |
| 204 | No Content | 성공 (응답 없음) | DELETE 성공 |
| 207 | Multi-Status | 벌크 작업 부분 성공 | 벌크 작업 |
| 400 | Bad Request | 잘못된 요청 | 유효성 검사 실패 |
| 401 | Unauthorized | 인증 필요 | 토큰 없음/만료 |
| 403 | Forbidden | 권한 없음 | 접근 권한 없음 |
| 404 | Not Found | 리소스 없음 | 리소스 미존재 |
| 409 | Conflict | 충돌 | 중복, 삭제 불가 |
| 422 | Unprocessable Entity | 처리 불가 | 비즈니스 로직 오류 |
| 429 | Too Many Requests | 요청 과다 | Rate Limit 초과 |
| 500 | Internal Server Error | 서버 오류 | 예상치 못한 오류 |
| 503 | Service Unavailable | 서비스 불가 | 점검 중 |

### 6.2 비즈니스 에러 코드

| 코드 | HTTP | 설명 |
|------|------|------|
| `AUTH_INVALID_CREDENTIALS` | 401 | 이메일 또는 비밀번호 불일치 |
| `AUTH_TOKEN_EXPIRED` | 401 | 토큰 만료 |
| `AUTH_TOKEN_INVALID` | 401 | 유효하지 않은 토큰 |
| `AUTH_EMAIL_NOT_VERIFIED` | 403 | 이메일 미인증 |
| `AUTH_ACCOUNT_SUSPENDED` | 403 | 계정 정지됨 |
| `RESOURCE_NOT_FOUND` | 404 | 리소스 없음 |
| `RESOURCE_ALREADY_EXISTS` | 409 | 리소스 중복 |
| `RESOURCE_CANNOT_DELETE` | 409 | 삭제 불가 (의존성) |
| `VALIDATION_REQUIRED` | 400 | 필수 필드 누락 |
| `VALIDATION_INVALID_FORMAT` | 400 | 형식 오류 |
| `VALIDATION_OUT_OF_RANGE` | 400 | 범위 초과 |
| `BUSINESS_INSUFFICIENT_STOCK` | 422 | 재고 부족 |
| `BUSINESS_INVALID_STATUS_TRANSITION` | 422 | 상태 전이 불가 |
| `RATE_LIMIT_EXCEEDED` | 429 | 요청 제한 초과 |

---

## 7. TypeScript 타입

### 7.1 공통 타입

```typescript
// ===========================================
// Common Types
// ===========================================

export interface ApiResponse<T> {
  data: T;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

export interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

export interface ApiError {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
  errors?: ValidationError[];
  timestamp: string;
  traceId: string;
}

export interface ValidationError {
  field: string;
  code: string;
  message: string;
}

// ===========================================
// Query Parameters
// ===========================================

export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}

export interface SearchParams extends PaginationParams {
  search?: string;
  searchFields?: string[];
}
```

### 7.2 리소스 타입

```typescript
// ===========================================
// {Resource} Types
// ===========================================

// Entity
export interface {Resource} {
  id: string;
  name: string;
  description: string | null;
  status: {Resource}Status;
  createdAt: string;  // ISO 8601
  updatedAt: string;  // ISO 8601
}

export type {Resource}Status = 'active' | 'inactive' | 'deleted';

// DTOs
export interface Create{Resource}Dto {
  name: string;
  description?: string;
  categoryId?: string;
}

export interface Update{Resource}Dto {
  name: string;
  description: string | null;
  categoryId: string | null;
  status: {Resource}Status;
}

export interface Patch{Resource}Dto {
  name?: string;
  description?: string | null;
  categoryId?: string | null;
  status?: {Resource}Status;
}

// Query Parameters
export interface Get{Resource}ListParams extends PaginationParams {
  status?: {Resource}Status;
  categoryId?: string;
  search?: string;
}
```

### 7.3 API 클라이언트 예시

```typescript
// ===========================================
// API Client
// ===========================================

class {Resource}Api {
  private baseUrl = '/api/v1/{resource}';

  async getList(params?: Get{Resource}ListParams): Promise<PaginatedResponse<{Resource}>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) searchParams.set(key, String(value));
      });
    }
    const response = await fetch(`${this.baseUrl}?${searchParams}`);
    return response.json();
  }

  async getById(id: string): Promise<ApiResponse<{Resource}>> {
    const response = await fetch(`${this.baseUrl}/${id}`);
    return response.json();
  }

  async create(data: Create{Resource}Dto): Promise<ApiResponse<{Resource}>> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async update(id: string, data: Update{Resource}Dto): Promise<ApiResponse<{Resource}>> {
    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async patch(id: string, data: Patch{Resource}Dto): Promise<ApiResponse<{Resource}>> {
    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async delete(id: string): Promise<void> {
    await fetch(`${this.baseUrl}/${id}`, { method: 'DELETE' });
  }
}
```

---

## 8. Rate Limiting

### 8.1 제한 정책

| 카테고리 | 제한 | 윈도우 | 적용 대상 |
|----------|------|--------|----------|
| **인증** | 10 req | 1분 | IP |
| **읽기** | 100 req | 1분 | User |
| **쓰기** | 30 req | 1분 | User |
| **검색** | 20 req | 1분 | User |
| **파일 업로드** | 10 req | 1분 | User |
| **전체** | 1000 req | 1시간 | User |

### 8.2 응답 헤더

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700000060
Retry-After: 30
```

### 8.3 Rate Limit 초과 응답

**429 Too Many Requests:**

```json
{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "요청 제한을 초과했습니다. 30초 후 다시 시도해주세요.",
  "instance": "/api/v1/{resource}",
  "retryAfter": 30
}
```

---

## 9. 버저닝 전략

### 9.1 버전 관리 방식

**URL Path 방식 (권장):**

```
/api/v1/users
/api/v2/users
```

**Header 방식 (대안):**

```http
Accept: application/vnd.api+json; version=1
```

### 9.2 버전 업그레이드 정책

| 변경 유형 | 버전 | 예시 |
|----------|------|------|
| **Breaking Change** | Major (v1 → v2) | 필드 삭제, 타입 변경 |
| **New Feature** | Minor | 필드 추가 (optional) |
| **Bug Fix** | - | 동작 수정 |

### 9.3 Deprecation 정책

1. **사전 공지**: 최소 6개월 전 공지
2. **경고 헤더**: `Deprecation: true`, `Sunset: 2024-12-31`
3. **문서 업데이트**: 마이그레이션 가이드 제공
4. **종료**: 공지된 날짜에 제거

**Deprecation 응답 헤더:**

```http
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: </api/v2/users>; rel="successor-version"
```

---

## 10. 체크리스트

### 10.1 API 설계 체크리스트

#### 기본 요소
- [ ] RESTful URL 구조 사용
- [ ] 적절한 HTTP 메서드 사용
- [ ] 일관된 응답 형식 적용
- [ ] RFC 7807 에러 형식 사용
- [ ] 페이지네이션 구현

#### 인증/권한
- [ ] 인증 방식 명시
- [ ] 각 엔드포인트별 권한 표시
- [ ] 토큰 갱신 API 제공

#### 문서화
- [ ] 모든 파라미터 설명
- [ ] 요청/응답 예시 포함
- [ ] 에러 케이스 문서화
- [ ] 타입 정의 포함

#### 보안
- [ ] Rate Limiting 적용
- [ ] 입력 유효성 검사
- [ ] 민감 정보 마스킹

### 10.2 검토 체크리스트

- [ ] 모든 CRUD 엔드포인트 정의됨
- [ ] 성공/실패 응답 모두 명시됨
- [ ] TypeScript 타입 정의 완료
- [ ] 베스트 프랙티스 준수 확인

---

## 금지 사항

### API 설계 시 하지 말아야 할 것

1. **URL 설계**
   - URL에 동사 사용 금지 (`/getUser`, `/createOrder`)
   - 대문자 사용 금지 (`/Users`, `/productList`)
   - 파일 확장자 포함 금지 (`/users.json`)

2. **HTTP 메서드**
   - 모든 작업에 POST 사용 금지
   - GET으로 데이터 변경 금지
   - DELETE 후 200으로 body 반환 금지 (204 사용)

3. **응답 형식**
   - 성공/실패 응답 형식 혼용 금지
   - 에러 시 200 반환 금지
   - 배열을 최상위로 반환 금지 (객체로 감싸기)

4. **보안**
   - 비밀번호 평문 전송 금지
   - 토큰을 URL 쿼리에 포함 금지
   - 민감 정보 로깅 금지

5. **기타**
   - 페이지네이션 없이 전체 목록 반환 금지
   - 버저닝 없이 Breaking Change 금지
   - Rate Limiting 없이 운영 금지

---

## 참조

- `best-practices/api-design.md` - API 베스트 프랙티스
- `templates/erd-template.md` - ERD 템플릿
- [RFC 7807 - Problem Details](https://tools.ietf.org/html/rfc7807)
- [OpenAPI Specification](https://swagger.io/specification/)

---

*다음 단계: /dev-tasks*
