---
name: learn
description: 특정 영역을 심층 학습합니다. 파일이나 폴더를 분석하여 패턴과 구조를 파악합니다.
allowed-tools: Read, Glob, Grep
argument-hint: <path>
disable-model-invocation: true
---

# /onboarding:learn - 특정 영역 학습

## 설명
프로젝트의 특정 파일이나 폴더를 심층 분석하여 해당 영역의 패턴과 구조를 학습합니다.

## 사용법
```
/onboarding:learn <path>
/onboarding:learn src/components/Button
/onboarding:learn src/services/
/onboarding:learn src/app/api/users/route.ts
```

## 학습 대상

### 폴더 학습
```
/onboarding:learn src/components/

분석 내용:
- 모든 컴포넌트 파일 구조
- 공통 패턴 추출
- props 타입 정의 방식
- 스타일링 방식
- 테스트 구조
```

### 파일 학습
```
/onboarding:learn src/services/userService.ts

분석 내용:
- 함수 구조
- 에러 처리 방식
- API 호출 패턴
- 타입 정의
```

## 실행 순서

### 1. 대상 파일 수집

```
지정된 경로의 모든 파일 목록화:
- .ts, .tsx, .js, .jsx 파일
- 테스트 파일 (.test.ts, .spec.ts)
- 타입 정의 파일 (.types.ts)
```

### 2. 패턴 분석

```
각 파일에서 추출:
- import 패턴
- export 구조
- 함수/컴포넌트 구조
- 타입 정의 방식
- 주석/문서화 스타일
```

### 3. 패턴 통합

```
공통 패턴 식별:
- 일관된 구조
- 네이밍 규칙
- 의존성 패턴
```

### 4. 컨텍스트 업데이트

```
학습 결과를 다음에 반영:
- CODE_PATTERNS.md에 새 패턴 추가
- 해당 영역 전용 섹션 생성
```

## 사용 예시

### 컴포넌트 폴더 학습

```
/onboarding:learn src/components/Button

📚 학습 시작: src/components/Button

=== 파일 분석 ===
분석된 파일:
- Button.tsx (메인 컴포넌트)
- Button.types.ts (타입 정의)
- Button.module.css (스타일)
- Button.test.tsx (테스트)
- index.ts (배럴 export)

=== 발견된 패턴 ===

1. 컴포넌트 구조:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  return (
    <button
      className={cn(styles.button, styles[variant], styles[size])}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

2. 타입 분리:
   - 별도의 .types.ts 파일
   - 인터페이스로 props 정의

3. 스타일링:
   - CSS Modules 사용
   - cn() 유틸로 클래스 조합

4. 테스트:
   - Testing Library 사용
   - describe/it 구조
   - 각 variant별 테스트

=== 컨텍스트 업데이트 ===
✓ CODE_PATTERNS.md에 Button 컴포넌트 패턴 추가

📚 학습 완료!

이제 이 패턴을 기반으로 유사한 컴포넌트를 생성할 수 있습니다.
```

### API 서비스 학습

```
/onboarding:learn src/services/

📚 학습 시작: src/services/

=== 파일 분석 ===
- userService.ts
- productService.ts
- orderService.ts
- api.ts (공통 유틸)

=== 발견된 패턴 ===

1. API 클라이언트 구조:
```typescript
// api.ts - 공통 유틸
const api = {
  async get<T>(url: string): Promise<T> {
    const res = await fetch(url);
    if (!res.ok) throw new ApiError(res);
    return res.json();
  },
  // post, put, delete...
};
```

2. 서비스 구조:
```typescript
// userService.ts
export const userService = {
  getUser: (id: string) => api.get<User>(`/api/users/${id}`),
  createUser: (data: CreateUserDto) => api.post<User>('/api/users', data),
  // ...
};
```

3. 에러 처리:
   - ApiError 클래스 사용
   - 상태 코드별 분기 처리

=== 컨텍스트 업데이트 ===
✓ CODE_PATTERNS.md에 서비스 패턴 추가

📚 학습 완료!
```

## 고급 사용법

### 다중 경로 학습
```
/onboarding:learn src/components/Button src/components/Input src/components/Modal
```

### 학습 후 즉시 생성
```
/onboarding:learn src/components/Button
이제 동일한 패턴으로 Checkbox 컴포넌트를 만들어줘
```

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 학습된 패턴 확인 | `/onboarding:show patterns` |
| 동일 패턴으로 코드 생성 | "학습한 패턴으로 XXX 만들어줘" |
| 컨텍스트 갱신 | `/onboarding:refresh` |

## 참조

- `/onboarding:start` - 전체 프로젝트 온보딩
- `/onboarding:show patterns` - 학습된 패턴 확인
