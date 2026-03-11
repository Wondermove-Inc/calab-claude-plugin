# Hexagonal Architecture 가이드

> Port/Adapter 구조 변경 시 참조합니다.

## 핵심 구조

```
┌──────────────────────────────────────────┐
│         Driving Adapters (Input)          │
│    (REST Handler, CLI, gRPC, Consumer)   │
├──────────────────────────────────────────┤
│          Driving Ports (Input)            │
│         (UseCase Interfaces)             │
├──────────────────────────────────────────┤
│           Application Core                │
│  (Domain Entities + Application Services) │
├──────────────────────────────────────────┤
│          Driven Ports (Output)            │
│  (Repository, Gateway, Notifier IF)      │
├──────────────────────────────────────────┤
│         Driven Adapters (Output)          │
│   (PostgreSQL, Redis, HTTP Client, SMTP) │
└──────────────────────────────────────────┘
```

## Port/Adapter 역할

| 구분 | Port (인터페이스) | Adapter (구현) |
|------|-------------------|----------------|
| **Driving (Input)** | UseCase 인터페이스 | HTTP Handler, CLI, gRPC |
| **Driven (Output)** | Repository, Gateway IF | PostgreSQL, Redis, SMTP |

## 핵심 원칙

- Port는 Core 내부에 정의, 도메인 언어 사용
- Adapter는 Core 외부에서 Port 구현
- Core는 Adapter를 절대 import하지 않음
- Application Service는 Driving Port 구현 + Driven Port 사용
- DI 조립 순서: Driven Adapters → Services → Driving Adapters

## 금지 사항

- Core에서 Adapter import
- Entity에서 외부 라이브러리 의존
- Port 없이 직접 Adapter 호출
- Adapter 간 직접 통신
- Driving Adapter에서 비즈니스 로직 구현
