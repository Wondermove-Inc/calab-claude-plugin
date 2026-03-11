# Database 설계 가이드

> DB 스키마 변경 시 참조합니다.

## 테이블 설계 원칙

### 필수 컬럼

모든 테이블: `id` (UUID), `created_at`, `updated_at`, `deleted_at` (Soft Delete)

### 네이밍 규칙

```
테이블명: snake_case, 복수형 (users, order_items)
컬럼명:   snake_case (user_id, created_at)
PK:       id (UUID)
FK:       {테이블_단수}_id (user_id)
인덱스:    idx_{table}_{columns}
```

## 정규화

최소 3NF 적용:
- 1NF: 원자값, 중복 그룹 제거
- 2NF: 부분 함수 종속 제거
- 3NF: 이행 함수 종속 제거

역정규화는 읽기 성능이 중요하고 변경이 드문 경우에만 허용

## 인덱스 전략

| 생성 기준 | 예시 |
|----------|------|
| 외래 키 (필수) | `idx_orders_user_id` |
| WHERE 절 빈번 사용 | `idx_users_email` |
| 정렬 컬럼 | `idx_posts_created_at` |

인덱스 피하기: 자주 변경되는 컬럼, 카디널리티 낮은 컬럼, 작은 테이블

## ERD 표기법 (Mermaid)

```
||--|| : 1:1 (필수)
||--o| : 1:1 (선택)
||--o{ : 1:N
}o--o{ : N:M
```

## 금지 사항

- Auto-increment ID (분산 환경 불가)
- 물리적 삭제 (Soft Delete 사용)
- created_at, updated_at 누락
- 외래 키 인덱스 누락
- 한 컬럼에 여러 값 저장 (CSV)
