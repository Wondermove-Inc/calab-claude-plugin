# Phase 5: 도메인 지식 수집 (대화형)

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**. 에이전트를 적극 활용하고, 파일이 크면 분할해서 읽어라.

---

## 질문 목록

```markdown
## 도메인 지식 인터뷰

프로젝트의 비즈니스 도메인에 대해 알려주세요:

### 1. 프로젝트 목적
이 프로젝트는 어떤 문제를 해결하나요?
대상 사용자는 누구인가요?

### 2. 핵심 개념
가장 중요한 비즈니스 엔티티는 무엇인가요?
(예: 사용자, 주문, 상품, 예약 등)

### 3. 비즈니스 규칙
꼭 지켜야 하는 중요한 규칙이 있나요?
(예: "주문은 결제 완료 후에만 배송 시작 가능")

### 4. 용어
프로젝트에서 사용하는 특수 용어나 약어가 있나요?
(예: "SKU", "MRR", "DAU" 등)

### 5. 워크플로우
핵심 사용자 시나리오를 설명해주세요.
(예: "사용자가 상품을 검색하고 장바구니에 담아 결제")
```

---

## 출력 예시

```
🔍 프로젝트 온보딩 시작...

══════════════════════════════════════════════════════════════
 Phase 1: 프로젝트 스캔
══════════════════════════════════════════════════════════════
✅ package.json 분석 완료
   - Framework: Next.js 14.1.0
   - Language: TypeScript 5.3.3
   - Database: PostgreSQL (Prisma 5.8.0)

✅ tsconfig.json 분석 완료
   - Path alias: @/* → src/*
   - Strict mode: enabled

✅ 디렉토리 구조 파악
   - 구조 유형: Feature-based (App Router)
   - 주요 폴더: app/, components/, lib/

══════════════════════════════════════════════════════════════
 Phase 2: 코드 패턴 분석
══════════════════════════════════════════════════════════════
✅ 컴포넌트 패턴 (5개 파일 분석)
   - Props: interface 사용
   - 스타일: Tailwind CSS + cn() 유틸
   - 상태: React Query + Zustand

✅ API 패턴 (3개 파일 분석)
   - 라우터: Next.js App Router API Routes
   - 검증: Zod
   - 응답: 표준화된 JSON 형식

✅ 에러 처리 패턴
   - 커스텀 에러 클래스: AppError 기반
   - 전역 핸들러: middleware.ts

══════════════════════════════════════════════════════════════
 Phase 3: 아키텍처 분석 (C4 Model)
══════════════════════════════════════════════════════════════
✅ System Context 파악
   - 사용자: 일반 사용자, 관리자
   - 외부 시스템: Stripe (결제), SendGrid (이메일)

✅ Container 구조
   - Web App: Next.js (Vercel)
   - Database: PostgreSQL (Supabase)
   - Cache: Redis (Upstash)

✅ 레이어 구조
   - Presentation: app/, components/
   - Application: lib/services/
   - Domain: prisma/schema.prisma
   - Infrastructure: lib/api/

══════════════════════════════════════════════════════════════
 Phase 4: 컨텍스트 문서 생성
══════════════════════════════════════════════════════════════
📄 PROJECT_SUMMARY.md 생성 완료 (2.3KB)
📄 ARCHITECTURE.md 생성 완료 (4.1KB)
📄 CODE_PATTERNS.md 생성 완료 (5.8KB)
📄 CONVENTIONS.md 생성 완료 (3.2KB)

══════════════════════════════════════════════════════════════
 Phase 5: 도메인 지식 수집
══════════════════════════════════════════════════════════════
프로젝트의 비즈니스 도메인에 대해 알려주세요:
(위 질문 목록 표시)

══════════════════════════════════════════════════════════════
✅ 온보딩 완료!
══════════════════════════════════════════════════════════════

📁 생성된 컨텍스트 문서:
├── .claude/project-context/PROJECT_SUMMARY.md
├── .claude/project-context/ARCHITECTURE.md
├── .claude/project-context/CODE_PATTERNS.md
├── .claude/project-context/CONVENTIONS.md
└── .claude/project-context/DOMAIN_KNOWLEDGE.md

💡 다음 단계:
   /dev plan [아이디어]  → 새 기능 개발 시작
   /learn <path>        → 특정 영역 심층 학습
   /context-show        → 컨텍스트 확인
```

---

## 품질 체크리스트

**문서 생성 후 검증:**

- [ ] 기술 스택이 정확히 파악되었는가?
- [ ] 디렉토리 구조가 명확히 문서화되었는가?
- [ ] 주요 패턴이 코드 예시와 함께 추출되었는가?
- [ ] C4 다이어그램이 현재 상태를 반영하는가?
- [ ] 컨벤션이 실제 코드와 일치하는가?
- [ ] 개발 명령어가 동작하는가?

---

## 참조

- `skills/project-onboarding/SKILL.md`
- `.claude/best-practices/project-onboarding.md`
- [C4 Model](https://c4model.com/) - 아키텍처 문서화 표준
