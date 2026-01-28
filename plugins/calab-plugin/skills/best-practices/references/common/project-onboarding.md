# Project Onboarding Best Practices

## 효과적인 프로젝트 온보딩 가이드

### 1. 온보딩 시작 전 준비

#### 필요한 정보 확인
```
□ 프로젝트의 목적과 비전
□ 주요 사용자 및 유스케이스
□ 현재 개발 상태 (신규/유지보수/리팩토링)
□ 우선순위가 높은 기능/버그
```

#### 최소 요구 파일
```
project/
├── package.json          # 필수
├── tsconfig.json         # TypeScript 프로젝트인 경우
├── src/                  # 소스 코드
└── README.md             # 프로젝트 설명 (있으면 좋음)
```

---

### 2. 온보딩 단계별 가이드

#### Phase 1: 빠른 스캔 (2분)

```markdown
## 확인 사항
1. package.json의 dependencies 훑어보기
   - React? Vue? Angular?
   - Next.js? Remix? Vite?
   - 상태 관리? (Redux, Zustand, Jotai)
   - 스타일링? (Tailwind, Styled-components, CSS Modules)

2. 디렉토리 구조 파악
   - src/ 하위 폴더들의 역할
   - 특이한 폴더 구조가 있는지

3. 설정 파일 확인
   - tsconfig.json paths 설정
   - .env.example 환경 변수
```

#### Phase 2: 코드 패턴 분석 (5분)

```markdown
## 분석 대상 선정
1. 가장 최근에 수정된 컴포넌트 2-3개
2. 가장 복잡해 보이는 컴포넌트 1개
3. API 엔드포인트 1-2개
4. 유틸리티/헬퍼 함수들

## 추출할 패턴
- 컴포넌트 구조 (props 정의, 훅 사용, 렌더링)
- 상태 관리 방식
- API 호출 방식
- 에러 처리 방식
- 테스트 작성 방식
```

#### Phase 3: 아키텍처 이해 (3분)

```markdown
## 레이어 식별
- Presentation: 화면을 그리는 코드
- Application: 비즈니스 로직
- Domain: 핵심 모델
- Infrastructure: 외부 연동

## 데이터 흐름 파악
사용자 입력 → 컴포넌트 → 훅/서비스 → API → DB
              ↑                              ↓
              └──────── 응답 ────────────────┘
```

---

### 3. 컨텍스트 문서 작성 가이드

#### PROJECT_SUMMARY.md 작성

```markdown
# 필수 포함 사항

## 한 줄 요약
이 프로젝트가 무엇인지 한 문장으로

## 기술 스택 (표 형식)
| 카테고리 | 기술 |
|---------|------|
| Frontend | React 18, Next.js 14 |
| ...      | ...  |

## 디렉토리 맵
각 폴더가 무엇을 담당하는지

## 개발 명령어
npm run dev, build, test 등

## 주요 진입점
어디서부터 코드를 읽어야 하는지
```

#### CODE_PATTERNS.md 작성

```markdown
# 패턴 문서화 원칙

1. 실제 코드 예시 포함
   - 추상적 설명보다 구체적 코드

2. "왜" 설명 포함
   - 이 패턴을 사용하는 이유

3. 변형 케이스 포함
   - 기본 패턴과 예외 상황

## 예시
### 컴포넌트 패턴
```typescript
// 기본 패턴
export function Component({ prop }: Props) { ... }

// 변형: forwardRef 사용 시
export const Component = forwardRef<Ref, Props>(...)
```
```

#### DOMAIN_KNOWLEDGE.md 작성

```markdown
# 도메인 지식 수집 질문

1. 핵심 비즈니스 개념
   - 사용자 유형 (일반/관리자/판매자 등)
   - 주요 엔티티 (상품, 주문, 결제 등)
   - 상태 흐름 (주문 상태 변화 등)

2. 비즈니스 규칙
   - 제약 조건 (최소 주문 금액 등)
   - 계산 로직 (할인, 포인트 등)
   - 권한 규칙 (누가 무엇을 할 수 있는지)

3. 용어 정의
   - 도메인 특화 용어
   - 약어와 전체 명칭
```

---

### 4. 컨텍스트 유지 전략

#### 세션 간 연속성

```markdown
## CURRENT_TASK.md 활용

세션 종료 전:
1. 현재 작업 상태 기록
2. 다음 단계 명시
3. 관련 파일 목록
4. 해결해야 할 이슈

세션 시작 시:
1. CURRENT_TASK.md 확인
2. 이전 작업 이해
3. 자연스럽게 이어서 진행
```

#### 컨텍스트 갱신 타이밍

```markdown
## 갱신이 필요한 시점

1. 새로운 패턴 도입
   - 새 라이브러리 추가
   - 새 컴포넌트 패턴

2. 구조 변경
   - 폴더 구조 리팩토링
   - 레이어 추가/변경

3. 대규모 기능 완료
   - 새 도메인 개념 추가
   - 비즈니스 규칙 변경
```

---

### 5. 일관된 코드 작성

#### 코드 작성 전 체크리스트

```markdown
## 새 파일 생성 전
□ 적절한 폴더 위치 확인 (ARCHITECTURE.md)
□ 파일명 규칙 확인 (CONVENTIONS.md)
□ 유사한 기존 파일 참조 (CODE_PATTERNS.md)

## 코드 작성 중
□ 기존 패턴 따르기
□ 기존 유틸리티 재사용
□ 네이밍 규칙 준수
□ import 순서 준수

## 코드 작성 후
□ 기존 코드와 일관성 확인
□ 테스트 작성 (기존 패턴 따라)
□ 타입 정의 완료
```

#### 기존 코드와 일치시키기

```typescript
// ❌ 기존 패턴 무시
const getUserData = async (userId) => {
  const response = await axios.get(`/users/${userId}`);
  return response.data;
};

// ✅ 기존 패턴 따르기 (프로젝트가 fetch + 서비스 패턴 사용 시)
export const userService = {
  getUser: (id: string) => api.get<User>(`/api/users/${id}`),
};
```

---

### 6. 문제 해결

#### 컨텍스트 누락 시

```markdown
증상: "이 프로젝트에서 어떻게 하는지 모르겠어요"

해결:
1. /learn <관련 폴더> 실행
2. 유사한 기존 코드 찾아서 분석
3. 발견한 패턴을 CODE_PATTERNS.md에 추가
```

#### 패턴 충돌 시

```markdown
증상: "기존 코드에 여러 패턴이 혼재"

해결:
1. 가장 최근 코드의 패턴 우선
2. 주요 기능의 패턴 우선
3. 사용자에게 선호 패턴 질문
```

#### 도메인 지식 부족 시

```markdown
증상: "비즈니스 로직이 이해가 안 됨"

해결:
1. 사용자에게 질문
2. 코드 주석 확인
3. 테스트 코드에서 힌트 찾기
4. DOMAIN_KNOWLEDGE.md에 기록
```

---

### 7. 온보딩 체크리스트

```markdown
## 필수 완료 항목

### 기본 이해
- [ ] 프로젝트 목적 파악
- [ ] 기술 스택 확인
- [ ] 디렉토리 구조 이해

### 패턴 파악
- [ ] 컴포넌트 패턴 확인
- [ ] API 패턴 확인
- [ ] 상태 관리 방식 확인

### 도메인 이해
- [ ] 핵심 개념 파악
- [ ] 비즈니스 규칙 이해
- [ ] 용어 정의

### 문서화
- [ ] PROJECT_SUMMARY.md 생성
- [ ] CODE_PATTERNS.md 생성
- [ ] CONVENTIONS.md 생성

### 검증
- [ ] 간단한 기능 수정으로 패턴 적용 테스트
- [ ] 기존 코드와 일관성 확인
```

---

## 금지 사항

### 온보딩 시 절대 하지 말아야 할 것

```typescript
// ❌ 금지: 코드를 읽지 않고 추측하기
"이 프로젝트는 아마 React를 사용할 것 같습니다..."

// ✅ 올바름: 실제 파일을 확인하고 파악
package.json, tsconfig.json 등 실제 파일을 읽고 기술 스택 파악
```

```typescript
// ❌ 금지: 기존 패턴 무시하고 새 패턴 도입
// 프로젝트가 fetch + 서비스 패턴 사용하는데
const getUserData = async (userId) => {
  const response = await axios.get(`/users/${userId}`);
  return response.data;
};

// ✅ 올바름: 기존 패턴 따르기
export const userService = {
  getUser: (id: string) => api.get<User>(`/api/users/${id}`),
};
```

```typescript
// ❌ 금지: 불완전한 컨텍스트 문서 작성
PROJECT_SUMMARY.md:
"React 프로젝트입니다."  // 너무 간단

// ✅ 올바름: 상세하고 유용한 문서 작성
PROJECT_SUMMARY.md:
- 기술 스택 표
- 디렉토리 맵
- 개발 명령어
- 주요 진입점
```

### 온보딩 문서 작성 금지 사항

- 프로젝트 코드를 직접 확인하지 않고 문서 작성 금지
- 다른 프로젝트의 패턴을 그대로 복사 금지
- 컨텍스트 문서 갱신 없이 구조 변경 금지
- 사용자 확인 없이 대규모 리팩토링 제안 금지
- 기존 코드 스타일 무시하고 개인 선호 스타일 적용 금지

### 피해야 할 실수

1. **성급한 결론**
   - 몇 개 파일만 보고 전체 아키텍처 판단 금지
   - 최소 3-5개 주요 파일 확인 후 패턴 파악

2. **컨텍스트 누락**
   - 온보딩 완료 후 컨텍스트 문서 미생성 금지
   - 세션 종료 전 CURRENT_CONTEXT.md 업데이트 필수

3. **일관성 무시**
   - 기존 네이밍 규칙 무시 금지
   - 기존 폴더 구조 무시하고 새 구조 제안 금지

4. **과도한 리팩토링**
   - 온보딩 단계에서 대규모 코드 변경 금지
   - 먼저 이해하고, 이해 후 개선 제안

---

## 참조

- `skills/project-onboarding/SKILL.md`
- `commands/onboard.md`
- `commands/onboard-quick.md`
