# /docs --generate - 전체 문서 자동 생성

> **프로젝트 심층 분석 후 전체 문서 구조 생성**

## 실행 절차

### Step 1: 프로젝트 심층 분석

**분석 대상:**
- 기술 스택 (package.json, tsconfig.json)
- 디렉토리 구조
- API 엔드포인트
- 컴포넌트
- 타입 정의
- 설정 파일
- 테스트 구조

### Step 2: 문서 구조 생성

```
.claude/docs-site/
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   ├── configuration.md
│   └── deployment.md
├── architecture/
│   ├── overview.md
│   ├── system-design.md
│   ├── data-flow.md
│   └── decisions.md
├── api-reference/
│   ├── overview.md
│   ├── authentication.md
│   ├── types.md
│   ├── errors.md
│   └── endpoints/
├── components/
├── guides/
├── configuration/
├── faq.md
├── troubleshooting.md
└── index.md
```

### Step 3: 품질 기준 적용

**필수 요소:**
- 기능당 최소 4개 코드 예시 (기본, 실전, 고급, 에러처리)
- 복사-붙여넣기로 즉시 실행 가능한 코드
- Mermaid 다이어그램 (복잡한 구조/흐름)
- 이미지 플레이스홀더: `<!-- 📸 스크린샷 필요: [설명] -->`

### Step 4: 자동 검증
- 필수 섹션 존재 확인
- 코드 예시 문법 확인
- 링크 유효성 확인
- TypeScript 컴파일 검증

### Step 5: 품질 점수 계산
- 완성도 (필수 섹션)
- 코드 예시 품질
- 다이어그램 포함
- 링크 유효성

### 완료 보고
```
============================================
 DOCS GENERATE 완료
============================================
 생성된 문서: 25개
 품질 점수: 85/100
 위치: .claude/docs-site/
============================================
```
