---
name: architecture:clean-validate-ts
description: 클린 아키텍처 규칙 준수를 검증합니다. 레이어 의존성, 네이밍 규칙, 구조적 무결성을 검사합니다.
allowed-tools: Read, Glob, Grep
argument-hint: [--fix] [--layer <layer>]
user-invocable: true
---

# /architecture:clean-validate-ts - 클린 아키텍처 검증

## 설명
현재 프로젝트 코드가 클린 아키텍처 원칙을 준수하는지 검증합니다.

## 사용법
```
/architecture:clean-validate-ts
/architecture:clean-validate-ts --fix
/architecture:clean-validate-ts --layer domain
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--fix` | 자동 수정 가능한 위반 사항 수정 |
| `--layer <name>` | 특정 레이어만 검증 |
| `--verbose` | 상세 출력 |

## 검증 항목

### 1. 의존성 규칙 (Dependency Rule)

**검증 내용**:
```
Domain → 외부 import 없음
Application → Domain만 import
Adapters → Domain, Application만 import
Infrastructure → 모든 레이어 import 가능
```

**위반 예시**:
```typescript
// domain/entities/User.ts에서 위반
import { PrismaClient } from '@prisma/client';  // Infrastructure 의존!

// 올바른 방법
// domain은 순수 TypeScript만 사용
```

### 2. 레이어별 파일 위치

**검증 내용**:
```
엔티티는 domain/entities/에 위치
유스케이스는 application/use-cases/에 위치
컨트롤러는 adapters/controllers/에 위치
설정 파일은 infrastructure/에 위치
```

### 3. 인터페이스 분리

**검증 내용**:
```
리포지토리 인터페이스는 domain/interfaces/에 정의
구현체는 adapters/repositories/에 위치
유스케이스는 인터페이스에 의존
```

### 4. DTO 사용

**검증 내용**:
```
엔티티가 직접 API 응답으로 노출되지 않음
입출력 DTO가 application/dtos/에 정의
Controller에서 DTO 변환 수행
```

## 실행 순서

### 1. 디렉토리 구조 확인
```
src/
├── domain/          존재
├── application/     존재
├── adapters/        존재
└── infrastructure/  존재
```

### 2. Import 분석

각 파일의 import 문을 분석하여 의존성 규칙 위반을 탐지합니다.

```typescript
// 분석 대상 파일: src/domain/entities/User.ts
import { Email } from '../value-objects/Email';     // OK (같은 레이어)
import { prisma } from '@infrastructure/database';  // 위반!
```

### 3. 위반 사항 보고

```
클린 아키텍처 검증 결과

=== 의존성 규칙 위반 ===
src/domain/entities/User.ts:3
   Domain 레이어에서 Infrastructure를 import
   - import { prisma } from '@infrastructure/database'
   → Domain은 외부 의존성을 가질 수 없습니다

src/application/use-cases/CreateUser.ts:5
   Application 레이어에서 Adapters를 import
   - import { UserController } from '@adapters/controllers'
   → Application은 Domain만 import할 수 있습니다

=== 파일 위치 위반 ===
src/services/UserService.ts
   레이어 구조에 맞지 않는 위치
   → application/use-cases/ 또는 adapters/로 이동 필요

=== 요약 ===
총 파일: 45개
검증 통과: 42개
위반: 3개

권장 조치:
1. Domain 엔티티에서 prisma import 제거
2. UseCase에서 Controller import 제거
3. UserService를 적절한 레이어로 이동
```

### 4. --fix 옵션 실행 시

자동 수정 가능한 항목:
- 파일 위치 이동 제안
- import 경로 수정 제안
- 인터페이스 추출 제안

```
자동 수정 실행

1. src/domain/entities/User.ts
   - 외부 import 제거됨
   - 인터페이스로 의존성 역전 적용

2. src/services/UserService.ts → src/application/use-cases/UserService.ts
   - 파일 이동됨
   - import 경로 업데이트됨

2개 항목 수정 완료
1개 항목 수동 수정 필요
```

## 출력 형식

### 성공 시
```
클린 아키텍처 검증 통과

검증된 파일: 45개
레이어별 현황:
- Domain: 8개 파일
- Application: 12개 파일
- Adapters: 15개 파일
- Infrastructure: 10개 파일

의존성 그래프: 정상
인터페이스 분리: 정상
DTO 사용: 정상
```

### 실패 시
```
클린 아키텍처 검증 실패

위반 사항: 5개
- 의존성 규칙 위반: 3개
- 파일 위치 위반: 1개
- 인터페이스 누락: 1개

상세 내용은 위 보고서를 확인하세요.
```

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 위반 자동 수정 | `/architecture:clean-validate-ts --fix` |
| 새 엔티티 생성 | `/architecture:clean-entity-ts <name>` |
| 새 유스케이스 생성 | `/architecture:clean-usecase-ts <name>` |
| 구현 진행 | `/workflow:dev-build TASK-XXX` |

## 참조

- `skills/clean-architecture-ts/SKILL.md`
- `best-practices/clean-architecture-ts.md`
