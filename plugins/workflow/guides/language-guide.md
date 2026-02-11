# 코딩 가이드

> 이 문서는 Worker, Reviewer 에이전트가 참조합니다.

---

## 공통 원칙

### SOLID 원칙

| 원칙 | 설명 |
|------|------|
| **S (단일 책임)** | 클래스/함수는 하나의 책임만, 변경 이유는 하나만 |
| **O (개방-폐쇄)** | 확장에 열림, 수정에 닫힘. 인터페이스로 확장 설계 |
| **L (리스코프 치환)** | 자식은 부모를 대체 가능해야 함 |
| **I (인터페이스 분리)** | 작은 인터페이스 여러 개 > 큰 인터페이스 하나 |
| **D (의존성 역전)** | 추상화에 의존, 구체 구현에 의존 금지. DI 활용 |

### DRY / KISS 원칙

- **DRY**: 동일 로직 3회 반복 시 추상화. 단, 맥락이 다르면 별도 유지
- **KISS**: 가장 간단한 솔루션 선택. "영리한" 코드보다 "명확한" 코드

### 보안 원칙

- 모든 외부 입력 검증 (화이트리스트 선호)
- SQL Injection, XSS, Command Injection 방지
- 민감 정보 하드코딩 금지 → 환경 변수/시크릿 매니저 사용
- 로그에 민감 정보 노출 금지
- 최소 권한 원칙 적용

### 에러 처리 원칙

- 에러 무시 금지, 적절한 수준에서 처리
- 에러 컨텍스트 보존 (래핑)
- 복구 가능: 재시도/대안 제시 | 복구 불가: fail fast

### 네이밍 원칙

- 의도를 드러내는 이름, 축약어 지양
- 스코프 넓을수록 설명적으로, 로컬 변수는 짧게
- 프로젝트/언어 컨벤션 준수

### 공통 코드 냄새

| 항목 | 기준 |
|------|------|
| 긴 함수 | 30줄+ (언어별 상이) |
| 매개변수 과다 | 4개+ |
| 깊은 중첩 | 3단계+ |
| 거대 클래스 | 단일 책임 위반 |
| 매직 넘버/문자열 | 상수 미정의 |
| 죽은 코드 | 미사용 코드 |

### 리팩토링 시점

- 새 기능 추가 전, 버그 수정 전, 코드 리뷰 후
- 테스트 커버리지 확보 후, 작은 단위로 점진적 변경

### 주석 규칙

- 한글 주석 사용
- 언어별 문서화 형식 준수 (godoc, TSDoc, Google Docstring, JSDoc)
- 특수 주석: `TODO:`, `FIXME:`, `NOTE:`

---

## Go

### 설계 원칙
- Accept interfaces, return structs
- 작은 인터페이스 (1-3개 메서드) 선호
- 컴포지션 우선 (임베딩 활용)
- 명시적 에러 처리 (error 반환값)
- 전역 변수 지양, DI로 테스트 용이성 확보
- context 전파 필수

### 에러 처리
- 센티널 에러: `var ErrXxx = errors.New(...)`
- 에러 래핑: `fmt.Errorf("context: %w", err)`
- 에러 검사: `errors.Is()`, `errors.As()` 사용
- 에러는 로깅하거나 반환, 둘 다 하지 않음

### 동시성
- 채널 크기: 0(동기) 또는 1 권장
- 고루틴 종료: `context.Context` 또는 done 채널로 명시적 종료
- 리소스 정리에 `defer` 활용

### 네이밍
- MixedCaps (언더스코어 대신 대소문자 혼합)
- Getter: `GetXxx()` 대신 `Xxx()` / Setter: `SetXxx()`
- 약어: URL, HTTP, ID 등 일관된 대문자
- 패키지명: 소문자, 단수형, 간결하게

### 코드 냄새

| 항목 | 기준 |
|------|------|
| 함수 길이 | 50줄 이상 |
| 중첩 깊이 | 3단계 이상 |
| any 타입 | 남용 시 |
| 에러 래핑 | 누락 시 |

### 테스트
```go
func TestXXX(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"valid", "input", "expected", false},
        {"error", "", "", true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Function(tt.input)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.want, got)
            }
        })
    }
}
```

### 커버리지
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

---

## TypeScript

### 설계 원칙
- `strict` 모드 필수
- `any` 금지 → `unknown` 사용, 타입 좁히기
- 함수 반환 타입 명시, 단순한 경우 추론 활용
- `readonly`, `as const`로 불변성 확보

### 타입 vs 인터페이스
- Interface: 객체 형태 정의, 확장 가능
- Type: 유니온, 인터섹션, 조건부 타입

### 유틸리티 타입
- `Partial<T>`, `Required<T>`, `Readonly<T>`
- `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`

### 네이밍
- 타입/인터페이스: PascalCase
- I 접두사 지양 (`IUser` → `User`)
- Props 접미사 (`ButtonProps`)

### 코드 냄새

| 항목 | 기준 |
|------|------|
| any 타입 | 사용 시 |
| 타입 단언 | as 남용 |
| ts-ignore | 사용 시 |
| strict 위반 | 설정 무시 |

### 테스트 (Jest/Vitest)
```typescript
describe('Function', () => {
  it('should return expected value', () => {
    const result = myFunction('input');
    expect(result).toBe('expected');
  });

  it('should throw error for invalid input', () => {
    expect(() => myFunction('')).toThrow();
  });
});
```

### 커버리지
```bash
npm test -- --coverage
npx vitest --coverage
```

---

## React

### 설계 원칙
- 단일 책임: 컴포넌트는 하나의 역할만
- 컴포지션 우선, Props 최소화
- 불변성 유지, 선언적 UI
- Hook 규칙 준수

### 상태 관리
- 로컬 상태 우선, 공유 필요시만 끌어올리기
- Context: 전역 테마, 인증 등 광범위 데이터
- 복잡한 상태: Zustand/Jotai 고려

### 성능
- React Compiler 활용 시 수동 useMemo/useCallback 최소화
- 대용량 리스트 가상화, 코드 스플리팅

### 에러 처리
- Error Boundaries: 컴포넌트 트리 에러 격리
- Suspense Boundaries: 비동기 로딩 상태 처리

### 네이밍
- 컴포넌트: PascalCase
- Hooks: use 접두사 (`useToggle`)
- 이벤트 핸들러: handle 접두사
- Boolean props: is/has/should 접두사

### 코드 냄새

| 항목 | 기준 |
|------|------|
| 컴포넌트 크기 | 100줄 이상 |
| Prop drilling | 3단계 이상 |
| Hook 규칙 | 조건부 호출 |
| 리렌더링 | 불필요한 리렌더 |

### 테스트 (React Testing Library)
```typescript
import { render, screen, fireEvent } from '@testing-library/react';

describe('Component', () => {
  it('should render correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('should handle click', () => {
    const onClick = vi.fn();
    render(<MyComponent onClick={onClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

---

## Python

### 설계 원칙
- 타입 힌트 100% 적용 필수
- 불변성 선호, EAFP 스타일 (try/except 우선)
- 컴포지션 우선, 표준 라이브러리 우선 사용
- dataclass/Pydantic 활용

### 타입 힌트
- 컬렉션: `list[str]`, `dict[str, int]`
- Optional: `User | None`

### 네이밍 (PEP 8)
- 모듈/함수: snake_case
- 클래스: PascalCase
- 상수: UPPER_SNAKE_CASE
- 프라이빗: _prefix

### 에러 처리
- 커스텀 예외 계층 정의
- 컨텍스트 매니저로 리소스 관리
- `from e` 체이닝으로 원인 보존

### 금지 사항
- 타입 힌트 없는 공개 함수
- bare except (`except:`)
- mutable 기본 인자 (`def f(items=[])`)
- global 변수, `import *`

### 코드 냄새

| 항목 | 기준 |
|------|------|
| 타입 힌트 | 누락 시 |
| bare except | `except:` 사용 |
| mutable 기본 인자 | `def f(x=[])` |
| global 변수 | 사용 시 |

### 테스트 (pytest)
```python
import pytest

class TestFunction:
    def test_valid_input(self):
        result = my_function("input")
        assert result == "expected"

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            my_function("")

    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_parametrized(self, input, expected):
        assert my_function(input) == expected
```

### 커버리지
```bash
pytest --cov
pytest --cov=mypackage --cov-report=term-missing
```
