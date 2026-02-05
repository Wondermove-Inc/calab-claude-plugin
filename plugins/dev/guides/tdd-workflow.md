# TDD 워크플로우 가이드

> 이 문서는 Planner, Tester, Coder 에이전트가 공통으로 참조합니다.

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

| 케이스 | 예시 |
|--------|------|
| 설정 파일 수정 | config.yaml, .env |
| 문서 수정 | README.md, CHANGELOG.md |
| 단순 오타 수정 | 변수명 오타, 주석 수정 |
| 테스트 불가능 코드 | main 함수, 초기화 코드 |

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
