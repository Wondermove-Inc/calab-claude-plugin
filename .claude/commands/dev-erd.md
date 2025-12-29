---
description: ERD (Entity-Relationship Diagram)를 설계합니다. 데이터 모델을 정의하고 테이블 구조를 설계합니다.
allowed-tools: Read, Write, Edit, Glob
argument-hint: [기능명 (선택)]
---

# ERD 설계

## 목적

데이터 모델을 정의하고, 데이터베이스 스키마를 설계합니다.

## 실행 절차

### Step 1: 컨텍스트 로드

```
1. .claude/memory/CURRENT_CONTEXT.md - 현재 작업 상태
2. docs/prd/{feature}/prd.md - PRD 문서
3. docs/architecture/system-architecture.md - 아키텍처 문서
4. .claude/best-practices/database.md - DB 베스트 프랙티스
```

### Step 2: 엔티티 식별

PRD의 기능 요구사항에서 엔티티 추출:

```
예시:
- User (사용자)
- Order (주문)
- Product (상품)
- OrderItem (주문 항목)
```

### Step 3: 관계 정의

엔티티 간의 관계 정의:

```
User ||--o{ Order : "places"
Order ||--|{ OrderItem : "contains"
Product ||--o{ OrderItem : "included in"
```

### Step 4: 베스트 프랙티스 적용

`.claude/best-practices/database.md` 규칙 적용:

- **필수 컬럼**: id (UUID), created_at, updated_at, deleted_at
- **네이밍**: snake_case, 복수형 테이블명
- **인덱스**: FK, 검색 컬럼에 인덱스
- **정규화**: 최소 3NF 적용

### Step 5: ERD 문서 작성

`docs/architecture/erd.md` 작성:

```markdown
# ERD: {기능명}

**작성일**: {날짜}

---

## 1. ERD 다이어그램

\`\`\`mermaid
erDiagram
    users ||--o{ orders : places
    users {
        uuid id PK
        string email UK
        string password_hash
        string name
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }
    orders ||--|{ order_items : contains
    orders {
        uuid id PK
        uuid user_id FK
        string status
        decimal total_amount
        timestamp created_at
        timestamp updated_at
    }
    products ||--o{ order_items : "included in"
    products {
        uuid id PK
        string name
        decimal price
        int stock
        timestamp created_at
        timestamp updated_at
    }
    order_items {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
        timestamp created_at
    }
\`\`\`

---

## 2. 테이블 정의

### 2.1 users

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | UUID | PK | 고유 식별자 |
| email | VARCHAR(255) | UK, NOT NULL | 이메일 |
| password_hash | VARCHAR(255) | NOT NULL | 암호화된 비밀번호 |
| name | VARCHAR(100) | | 사용자 이름 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 생성일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정일시 |
| deleted_at | TIMESTAMP | | 삭제일시 (Soft Delete) |

### 2.2 orders

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | UUID | PK | 고유 식별자 |
| user_id | UUID | FK(users.id), NOT NULL | 주문자 |
| status | VARCHAR(20) | NOT NULL | 주문 상태 |
| total_amount | DECIMAL(10,2) | NOT NULL | 총 금액 |
| created_at | TIMESTAMP | NOT NULL | 주문일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정일시 |

---

## 3. 인덱스 전략

\`\`\`sql
-- 외래 키 인덱스
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- 검색/정렬 인덱스
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX idx_users_email ON users(email);
\`\`\`

---

## 4. Prisma 스키마

\`\`\`prisma
model User {
  id           String   @id @default(uuid())
  email        String   @unique
  passwordHash String   @map("password_hash")
  name         String?
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt @map("updated_at")
  deletedAt    DateTime? @map("deleted_at")

  orders       Order[]

  @@map("users")
}

model Order {
  id          String   @id @default(uuid())
  userId      String   @map("user_id")
  status      String
  totalAmount Decimal  @map("total_amount") @db.Decimal(10, 2)
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  user        User     @relation(fields: [userId], references: [id])
  items       OrderItem[]

  @@index([userId])
  @@map("orders")
}
\`\`\`

---

## 5. 마이그레이션 고려사항

- [ ] 기존 데이터 마이그레이션 필요 여부
- [ ] 롤백 계획
- [ ] 인덱스 생성 순서

---

*다음 단계: /dev-tasks*
```

### Step 6: 상태 업데이트

`.claude/memory/CURRENT_CONTEXT.md` 업데이트

### Step 7: 완료 보고

```
============================================
[ERD] 데이터 모델 설계 완료
============================================

 기능: {feature-name}
 생성된 문서: docs/architecture/erd.md

 데이터 모델 요약:
• 테이블: {n}개
• 관계: {n}개
• 인덱스: {n}개

 테이블 목록:
• users
• orders
• products
• order_items

 다음 단계: /dev-tasks

============================================
```

## 참조 파일

- `.claude/best-practices/database.md` - DB 베스트 프랙티스
- `docs/prd/{feature}/prd.md` - PRD 문서
