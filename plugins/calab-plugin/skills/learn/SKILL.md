---
name: learn
description: |
  특정 영역을 심층 학습합니다. 파일이나 폴더를 분석하여 패턴과 구조를 파악합니다.
  USE WHEN: 학습, learn, 코드 패턴, pattern, 구조 분석, 파일 분석, 폴더 분석,
  이해, understand, 파악, 분석해줘, analyze,
  어떻게 동작, how it works, 로직, logic,
  흐름, flow, 데이터 흐름, 호출 관계,
  이 파일, 이 폴더, 이 코드, 설명해줘, explain
argument-hint: "<path>"
allowed-tools: [Read, Glob, Grep]
agent: Explore
---

# /learn - 특정 영역 학습

> **코드 패턴 및 구조 심층 분석**

## 사용법

```bash
/learn <path>
/learn src/components/Button
/learn src/services/
/learn src/app/api/users/route.ts
```

## 🤖 에이전트 호출 (필수)

> **이 스킬은 반드시 Explore 에이전트를 통해 실행해야 합니다.**

스킬이 로드되면 즉시 다음 에이전트를 호출하세요:

```
Task(
  subagent_type="Explore",
  description="코드 패턴 심층 학습: {path}",
  prompt="""
  **역할**: 코드 패턴 분석 전문가

  **목표**: {path} 영역의 코드 패턴 및 구조 심층 분석

  **분석 대상**:
  - 지정된 경로의 모든 소스 파일
  - 테스트 파일 (.test.ts, .spec.ts)
  - 타입 정의 파일 (.types.ts)

  **추출 항목**:
  1. import 패턴 (외부 라이브러리, 내부 모듈)
  2. export 구조 (default, named, barrel)
  3. 함수/컴포넌트 구조
  4. 타입 정의 방식
  5. 주석/문서화 스타일
  6. 에러 처리 패턴

  **출력 형식**:
  === 파일 분석 ===
  분석된 파일: [목록]

  === 발견된 패턴 ===
  1. [패턴명]: [코드 예시]
  2. [패턴명]: [코드 예시]

  === 권장 사항 ===
  - 이 패턴을 다른 코드에 적용할 때 주의점

  **제약 조건**:
  - ❌ 코드 수정 금지 (분석만)
  - ✅ CODE_PATTERNS.md에 새 패턴 기록
  """
)
```

---

## 학습 대상

### 폴더 학습
```
/learn src/components/

분석 내용:
- 모든 컴포넌트 파일 구조
- 공통 패턴 추출
- props 타입 정의 방식
- 스타일링 방식
- 테스트 구조
```

### 파일 학습
```
/learn src/services/userService.ts

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

## 출력 예시

### 컴포넌트 폴더 학습

```
/learn src/components/Button

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

## 고급 사용법

### 다중 경로 학습
```
/learn src/components/Button src/components/Input src/components/Modal
```

### 학습 후 즉시 생성
```
/learn src/components/Button
이제 동일한 패턴으로 Checkbox 컴포넌트를 만들어줘
```

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 학습된 패턴 확인 | `/context` |
| 동일 패턴으로 코드 생성 | "학습한 패턴으로 XXX 만들어줘" |
| 컨텍스트 갱신 | `/context --refresh` |
