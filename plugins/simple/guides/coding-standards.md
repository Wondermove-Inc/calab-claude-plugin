# 코딩 표준 가이드

> Simple Worker 에이전트가 코드 구현 및 리팩토링 시 참조합니다.

## SOLID 원칙

| 원칙 | 검증 질문 |
|------|----------|
| **SRP** (단일 책임) | 클래스/모듈이 여러 책임을 갖는가? |
| **OCP** (개방-폐쇄) | 새 기능 추가 시 기존 코드를 수정하는가? |
| **LSP** (리스코프 치환) | 자식이 부모의 계약을 위반하는가? |
| **ISP** (인터페이스 분리) | 클라이언트가 불필요한 메서드에 의존하는가? |
| **DIP** (의존성 역전) | 고수준이 저수준에 직접 의존하는가? |

## 의존성 방향 규칙

```
Infrastructure → Adapters → Application → Domain
```

**절대 불변**: 내부 레이어는 외부 레이어를 참조하지 않습니다.

| 레이어 | 허용된 Import | 금지된 Import |
|--------|---------------|---------------|
| **Domain** | 표준 라이브러리만 | Application, Adapters, Infrastructure |
| **Application** | Domain | Adapters, Infrastructure |
| **Adapters** | Domain, Application | Infrastructure |
| **Infrastructure** | 모두 허용 | - |

## 언어별 핵심 규칙

### Go
- 함수 50줄 이상 → 분리 검토
- 중첩 3단계 이상 → 리팩토링
- `any` (interface{}) 남용 지양
- 에러 무시 금지 (`_ = err` 지양)
- 에러 래핑 (`fmt.Errorf("context: %w", err)`)
- 패키지명 소문자 단수형

### TypeScript
- `any` 타입 지양 (unknown 또는 구체적 타입)
- 타입 단언(as) 최소화
- Optional chaining (`?.`), Nullish coalescing (`??`) 활용
- `const` 우선, `readonly` 적극 사용

### Python
- 함수 시그니처에 타입 힌트 명시
- Bare except 금지 (`except Exception:` 명시)
- Mutable 객체 기본값 금지 (`[]`, `{}`)
