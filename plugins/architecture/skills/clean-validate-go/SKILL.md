---
name: architecture:clean-validate-go
description: Go 클린 아키텍처 규칙 준수를 검증합니다. 레이어 의존성, 네이밍 규칙, 구조적 무결성을 검사합니다.
allowed-tools: Read, Glob, Grep, Bash
argument-hint: [--fix] [--layer <layer>]
user-invocable: true
---

# /architecture:clean-validate-go - Go 클린 아키텍처 검증

## 설명
현재 Go 프로젝트 코드가 클린 아키텍처 원칙을 준수하는지 검증합니다.

## 사용법
```
/architecture:clean-validate-go
/architecture:clean-validate-go --fix
/architecture:clean-validate-go --layer domain
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
Domain → 외부 import 없음 (표준 라이브러리만)
Application → Domain만 import
Adapters → Domain, Application만 import
Infrastructure → 모든 레이어 import 가능
```

**위반 예시**:
```go
// internal/domain/entity/user.go에서 위반
import (
    "github.com/myorg/myproject/internal/infrastructure/database"  // Infrastructure 의존!
)

// 올바른 방법
// domain은 표준 라이브러리만 사용
import (
    "time"
    "regexp"
)
```

### 2. 레이어별 파일 위치

**검증 내용**:
```
엔티티는 internal/domain/entity/에 위치
값 객체는 internal/domain/valueobject/에 위치
리포지토리 인터페이스는 internal/domain/repository/에 위치
유스케이스는 internal/application/usecase/에 위치
DTO는 internal/application/dto/에 위치
핸들러는 internal/adapters/handler/에 위치
리포지토리 구현체는 internal/adapters/repository/에 위치
설정 파일은 internal/infrastructure/에 위치
```

### 3. Go 패키지 구조

**검증 내용**:
```
cmd/ 디렉토리에 진입점 존재
internal/ 디렉토리로 비공개 패키지 분리
순환 import 없음
패키지 이름이 디렉토리와 일치
```

### 4. 인터페이스 분리

**검증 내용**:
```
리포지토리 인터페이스는 domain/repository/에 정의
구현체는 adapters/repository/에 위치
유스케이스는 인터페이스에 의존
인터페이스는 사용하는 곳에서 정의 (소비자 정의)
```

### 5. Context 사용

**검증 내용**:
```
모든 유스케이스 메서드의 첫 번째 파라미터가 context.Context
리포지토리 메서드의 첫 번째 파라미터가 context.Context
context가 올바르게 전파됨
```

## 실행 순서

### 1. 디렉토리 구조 확인
```
project/
├── cmd/                 존재
├── internal/
│   ├── domain/          존재
│   ├── application/     존재
│   ├── adapters/        존재
│   └── infrastructure/  존재
└── go.mod               존재
```

### 2. Import 분석

각 파일의 import 문을 분석하여 의존성 규칙 위반을 탐지합니다.

```go
// 분석 대상 파일: internal/domain/entity/user.go
import (
    "time"                                                    // OK (표준 라이브러리)
    "github.com/myorg/myproject/internal/domain/valueobject"  // OK (같은 레이어)
    "github.com/myorg/myproject/internal/infrastructure/db"   // 위반!
)
```

### 3. 위반 사항 보고

```
Go 클린 아키텍처 검증 결과

=== 의존성 규칙 위반 ===
internal/domain/entity/user.go:5
   Domain 레이어에서 Infrastructure를 import
   - import "github.com/myorg/myproject/internal/infrastructure/db"
   → Domain은 외부 의존성을 가질 수 없습니다

internal/application/usecase/user/create_user.go:8
   Application 레이어에서 Adapters를 import
   - import "github.com/myorg/myproject/internal/adapters/handler"
   → Application은 Domain만 import할 수 있습니다

=== 파일 위치 위반 ===
internal/services/user_service.go
   레이어 구조에 맞지 않는 위치
   → internal/application/usecase/ 또는 internal/adapters/로 이동 필요

=== Context 사용 위반 ===
internal/application/usecase/user/get_user.go:15
   func GetUser(id string) 에 context.Context 파라미터 없음
   → func GetUser(ctx context.Context, id string) 로 수정 필요

=== 요약 ===
총 파일: 45개
검증 통과: 41개
위반: 4개

권장 조치:
1. Domain 엔티티에서 infrastructure import 제거
2. UseCase에서 handler import 제거
3. user_service.go를 적절한 레이어로 이동
4. GetUser 함수에 context.Context 파라미터 추가
```

### 4. --fix 옵션 실행 시

자동 수정 가능한 항목:
- 파일 위치 이동 제안
- import 경로 수정 제안
- 인터페이스 추출 제안

```
자동 수정 실행

1. internal/domain/entity/user.go
   - 외부 import 제거됨
   - 인터페이스로 의존성 역전 적용

2. internal/services/user_service.go → internal/application/usecase/user/user_service.go
   - 파일 이동됨
   - import 경로 업데이트됨

2개 항목 수정 완료
2개 항목 수동 수정 필요
```

## 검증 스크립트 (참고용)

### 의존성 검사 스크립트
```bash
# Domain 레이어에서 외부 의존성 검사
grep -r "import" internal/domain/ | grep -v "internal/domain" | grep "myorg/myproject/internal"

# Application에서 Adapters/Infrastructure 의존성 검사
grep -r "import" internal/application/ | grep -E "(adapters|infrastructure)"

# 순환 import 검사
go mod graph | grep -E "cycle"
```

## 출력 형식

### 성공 시
```
Go 클린 아키텍처 검증 통과

검증된 파일: 45개
레이어별 현황:
- Domain: 8개 파일
- Application: 12개 파일
- Adapters: 15개 파일
- Infrastructure: 10개 파일

의존성 그래프: 정상
인터페이스 분리: 정상
Context 사용: 정상
```

### 실패 시
```
Go 클린 아키텍처 검증 실패

위반 사항: 5개
- 의존성 규칙 위반: 3개
- 파일 위치 위반: 1개
- Context 사용 위반: 1개

상세 내용은 위 보고서를 확인하세요.
```

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 위반 자동 수정 | `/architecture:clean-validate-go --fix` |
| 새 엔티티 생성 | `/architecture:clean-entity-go <name>` |
| 새 유스케이스 생성 | `/architecture:clean-usecase-go <name>` |
| 구현 진행 | `/workflow:dev-build TASK-XXX` |

## 참조

- `skills/clean-architecture-go/SKILL.md`
- `best-practices/clean-architecture-go.md`
