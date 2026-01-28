# Phase 1-2: Discovery + Pattern Analysis

> **프로젝트 스캔 및 코드 패턴 분석**

## Phase 1: Project Scan

### Step 1: 설정 파일 분석
- package.json
- tsconfig.json
- .env.example
- prisma/schema.prisma

### Step 2: 기술 스택 식별

| 레이어 | 감지 항목 |
|--------|----------|
| Frontend | Framework, UI Library, State |
| Backend | Runtime, Framework, ORM |
| Database | DBMS, Cache |
| Infra | CI/CD, Deploy |

### Step 3: 디렉토리 구조 매핑

**구조 유형:**
- Feature-based: `src/features/{feature}/`
- Layer-based: `src/{layer}/`
- Domain-based: `src/domain/`
- Hybrid: 혼합

## Phase 2: Pattern Extraction

### Step 1: 대표 파일 선택
- 컴포넌트 3-5개 (가장 큰 파일)
- API 2-3개
- 서비스 2-3개

### Step 2: 패턴 추출

**컴포넌트 패턴:**
- Props 정의 방식
- 상태 관리 방식
- 스타일링 방식
- 에러 바운더리

**API 패턴:**
- 미들웨어 체인
- 검증 방식
- 응답 형식
- 페이지네이션

**에러 처리 패턴:**
- 커스텀 에러 클래스
- 로깅 레벨

### Step 3: 임포트 순서 분석
```
표준 순서:
1. 외부 라이브러리
2. 내부 절대 경로
3. 상대 경로
4. 타입
5. 스타일
```

## 출력
- 다음 Phase로 전달할 분석 데이터
