# TDD 워크플로우 가이드

> 이 문서는 Planner, Tester, Coder 에이전트가 공통으로 참조합니다.

## 핵심 규칙

**모든 코드 로직 변경 작업은 TDD로 실행합니다.** 스킵 허용 케이스는 아래 참조.

| 규칙 | 위반 시 처리 |
|------|------------|
| Coder 호출 전 Tester 호출 필수 | Planner가 Tester 먼저 호출 |
| Tester는 RED 상태를 검증해야 함 | RED 미확인 시 Planner에게 보고 |
| Coder는 GREEN 상태를 검증해야 함 | GREEN 미확인 시 Planner에게 보고 |
| 테스트 없이 구현 코드 작성 금지 | Coder가 즉시 중단, Planner에게 보고 |

## TDD 원칙

**RED → GREEN → REFACTOR** 사이클을 준수합니다.

```
1. RED: 실패하는 테스트 작성 (Tester)
   └─ 테스트 실행 → FAIL 확인

2. GREEN: 테스트 통과하는 코드 작성 (Coder)
   └─ 테스트 실행 → PASS 확인

3. REFACTOR: 코드 개선 (Coder, 선택)
   └─ 테스트 실행 → PASS 유지
```

## 호출 순서

```
Planner
   │
   ├─→ Tester: 테스트 작성
   │      └─→ 테스트 실행 → FAIL (RED) 확인
   │
   ├─→ Coder: 구현 코드 작성
   │      └─→ 테스트 실행 → PASS (GREEN) 확인
   │
   └─→ Coder: 리팩토링 (선택)
          └─→ 테스트 실행 → PASS 유지 확인
```

## 절대 금지

- ❌ Coder를 Tester보다 먼저 호출
- ❌ 테스트 없이 구현 코드 작성
- ❌ 테스트 실패 확인 없이 구현 진행

## TDD 스킵 허용 케이스

> **코드 로직 변경이 없는 경우에만** 스킵이 허용됩니다.
> 코드 로직을 변경하는 작업은 반드시 TDD를 따릅니다.

| 스킵 허용 | 예시 | 판단 기준 |
|-----------|------|----------|
| 설정 파일 수정 | config.yaml, .env | 코드 로직 변경 아님 |
| 문서 수정 | README.md, CHANGELOG.md | 코드 로직 변경 아님 |
| 단순 오타 수정 | 주석 오타, 로그 메시지 오타 | 런타임 동작 영향 없음 |
| 테스트 불가능 코드 | main 함수, CLI 진입점 | 실행 환경 의존 |

| 스킵 불가 (TDD 필수) | 예시 |
|---------------------|------|
| 버그 수정 | 로직 오류, 예외 처리 누락 |
| 새 기능 구현 | 함수/메서드/클래스 추가 |
| 리팩토링 | 함수 분리, 인터페이스 변경 |
| API 변경 | 엔드포인트, 파라미터 변경 |

## 테스트 실패 핸들링

### RED 단계 (Tester 완료 후)
- 테스트 FAIL = 정상 동작
- Coder에게 GREEN 작업 전달

### GREEN 단계 (Coder 완료 후)
- 테스트 PASS = 성공
- 테스트 FAIL = Coder 재호출 (최대 3회)
- 3회 연속 실패 시 사용자에게 보고

### REFACTOR 단계
- 테스트 PASS 유지 필수
- 실패 시 리팩토링 롤백

## 검증 명령어

### Go
```bash
# 테스트 실행
go test ./...

# 특정 테스트
go test -run TestXXX ./...

# RED 상태 확인
go test -run TestXXX ./... 2>&1 | grep -q "FAIL" && echo "RED 확인"
```

### TypeScript
```bash
# 테스트 실행
npm test

# 특정 테스트
npm test -- --testNamePattern="XXX"

# RED 상태 확인
npm test -- --testNamePattern="XXX" 2>&1 | grep -q "FAIL" && echo "RED 확인"
```

### Python
```bash
# 테스트 실행
pytest

# 특정 테스트
pytest -k "test_xxx"

# RED 상태 확인
pytest -k "test_xxx" 2>&1 | grep -q "FAILED" && echo "RED 확인"
```
