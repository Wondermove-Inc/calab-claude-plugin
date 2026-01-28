# Phase 4: Context Generation

> **4개 컨텍스트 문서 자동 생성**

## 생성 문서

### 1. PROJECT_SUMMARY.md

```markdown
# 프로젝트 요약

## 개요
- 이름: {name}
- 설명: {description}
- 주요 기능: {features}

## 기술 스택
| 영역 | 기술 | 버전 |
|------|------|------|
| Frontend | Next.js | 14.x |
| ...

## 디렉토리 구조
{구조 설명}

## 개발 명령어
```bash
npm run dev
npm run build
npm run test
```
```

### 2. ARCHITECTURE.md

```markdown
# 아키텍처

## C4 다이어그램
### Level 1: System Context
### Level 2: Container
### Level 3: Component

## 레이어 구조
## 데이터 플로우
## 상태 관리
## 인증/인가
## ADR (Architecture Decision Records)
```

### 3. CODE_PATTERNS.md

```markdown
# 코드 패턴

## 컴포넌트 패턴
- 표준 구조
- 페이지 컴포넌트
- Suspense 사용

## API 패턴
- 요청 스키마 (Zod)
- 인증 검증
- 에러 처리
- 표준 응답 형식

## Hook 패턴
- 쿼리 키
- useQuery
- useMutation

## 에러 처리
- 커스텀 에러 클래스

## 테스트 패턴
```

### 4. CONVENTIONS.md

```markdown
# 컨벤션

## 파일/폴더 네이밍
- 컴포넌트: PascalCase
- 유틸: camelCase

## 코드 네이밍
## 임포트 순서
## 주석 규칙
## Git 커밋 메시지
## 브랜치 전략
```

## 저장 위치
```
.claude/project-context/
├── PROJECT_SUMMARY.md
├── ARCHITECTURE.md
├── CODE_PATTERNS.md
└── CONVENTIONS.md
```
