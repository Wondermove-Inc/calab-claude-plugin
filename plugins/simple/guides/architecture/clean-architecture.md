# Clean Architecture 가이드

> 레이어드 구조 변경 시 참조합니다.

## 4-레이어 구조

```
┌─────────────────────────────────────────────────┐
│              Infrastructure Layer                 │
│        (HTTP Server, DB, Config, DI)             │
├─────────────────────────────────────────────────┤
│                Adapters Layer                     │
│       (Handler/Controller, Repository Impl)      │
├─────────────────────────────────────────────────┤
│              Application Layer                    │
│             (UseCase, DTO, Port)                  │
├─────────────────────────────────────────────────┤
│                Domain Layer                       │
│      (Entity, Value Object, Repository IF)       │
└─────────────────────────────────────────────────┘
            ↑ 의존성 방향 (안쪽으로만)
```

## 레이어별 역할

| 레이어 | 역할 | 포함 요소 |
|--------|------|----------|
| **Domain** | 핵심 비즈니스 규칙 | Entity, Value Object, Repository Interface |
| **Application** | 유스케이스 구현 | UseCase, DTO, Port |
| **Adapters** | 포트 구현, 데이터 변환 | Handler, Repository Impl, Gateway |
| **Infrastructure** | 프레임워크 설정 | HTTP Server, DB, Config, DI |

## 핵심 패턴

- **Entity**: private 필드 + Getter, Factory Method로 유효성 검사
- **UseCase**: Repository 인터페이스 주입, 비즈니스 흐름 조율
- **Repository**: Domain에 인터페이스, Adapters에 구현체
- **DTO**: 레이어 경계에서 데이터 변환

## 금지 사항

| 위반 | 설명 |
|------|------|
| Domain에서 외부 라이브러리 import | 표준 라이브러리만 허용 |
| Application에서 Adapters import | 인터페이스만 의존 |
| Handler에서 직접 DB 접근 | UseCase를 통해서만 |
| 엔티티 직접 노출 | DTO로 변환하여 반환 |
| 순환 import | 의존성 방향 위반 |
