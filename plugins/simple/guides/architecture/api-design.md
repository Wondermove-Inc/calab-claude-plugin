# API 설계 가이드

> API 엔드포인트 변경 시 참조합니다.

## RESTful 원칙

```
GET    /users           → 목록 조회
GET    /users/{id}      → 단건 조회
POST   /users           → 생성
PUT    /users/{id}      → 전체 수정
PATCH  /users/{id}      → 부분 수정
DELETE /users/{id}      → 삭제
```

- URL은 리소스 기반, 복수형 (`/users`, `/orders`)
- 동사 기반 URL 금지 (`/getUsers`, `/createUser`)

## HTTP 메서드 & 상태 코드

| 메서드 | 성공 코드 | 멱등성 |
|--------|----------|--------|
| GET | 200 | Yes |
| POST | 201 | No |
| PUT/PATCH | 200 | Yes/No |
| DELETE | 204 | Yes |

| 에러 코드 | 용도 |
|----------|------|
| 400 | 유효성 검증 실패 |
| 401 | 인증 필요 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 409 | 충돌 (중복) |
| 422 | 비즈니스 규칙 위반 |

## 응답 형식

```json
// 성공
{ "data": { ... } }

// 컬렉션
{ "data": [...], "pagination": { "page": 1, "limit": 20, "total": 100 } }

// 에러
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
```

## 금지 사항

- 동사 기반 URL
- 일관되지 않은 응답 형식
- 에러 시 200 응답
- 민감 정보 노출
- 버저닝 없이 Breaking Change
