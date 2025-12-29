# /onboard - 프로젝트 온보딩

## 설명
기존 프로젝트를 분석하여 AI가 효과적으로 개발을 이어나갈 수 있도록 컨텍스트 문서를 생성합니다.

## 사용법
```
/onboard
/onboard --skip-domain  # 도메인 지식 단계 건너뛰기
```

## 실행 순서

### Phase 1: 프로젝트 스캔 (자동)

**분석 대상 파일**:
- `package.json` - 기술 스택, 스크립트
- `tsconfig.json` - TypeScript 설정
- `.env.example` - 환경 변수
- `prisma/schema.prisma` - DB 스키마 (있는 경우)

**수행 작업**:
```bash
# 디렉토리 구조 확인
ls -la src/

# 주요 설정 파일 읽기
cat package.json
cat tsconfig.json
```

### Phase 2: 코드 패턴 분석 (자동)

**분석 대상**:
- 3-5개 대표 컴포넌트 파일
- API 엔드포인트 파일
- 유틸리티/헬퍼 파일

**추출 패턴**:
1. 컴포넌트 구조 (props, state, hooks 사용 방식)
2. API 응답 형식
3. 에러 처리 방식
4. import 순서 및 스타일

### Phase 3: 아키텍처 분석 (자동)

**분석 내용**:
- 레이어 구조 (presentation, application, domain, infrastructure)
- 폴더별 역할
- 모듈 간 의존성

### Phase 4: 컨텍스트 문서 생성 (자동)

다음 파일들을 `.claude/project-context/`에 생성:

1. **PROJECT_SUMMARY.md**
   - 프로젝트 기본 정보
   - 기술 스택
   - 디렉토리 구조
   - 개발 명령어

2. **ARCHITECTURE.md**
   - 레이어 구조 다이어그램
   - 모듈 의존성
   - 데이터 흐름
   - 상태 관리 방식

3. **CODE_PATTERNS.md**
   - 컴포넌트 템플릿
   - API 패턴
   - 테스트 패턴
   - 에러 처리 패턴

4. **CONVENTIONS.md**
   - 파일/폴더 구조 규칙
   - 네이밍 규칙
   - Import 순서
   - 주석 규칙
   - Git 커밋 메시지 규칙

### Phase 5: 도메인 지식 수집 (대화형)

사용자에게 질문:
```
프로젝트의 비즈니스 도메인에 대해 알려주세요:

1. 이 프로젝트는 어떤 문제를 해결하나요?
2. 핵심 비즈니스 개념(엔티티)은 무엇인가요?
3. 중요한 비즈니스 규칙이 있나요?
4. 특수 용어나 약어가 있나요?
```

수집된 정보로 **DOMAIN_KNOWLEDGE.md** 생성.

## 출력 예시

```
🔍 프로젝트 온보딩 시작...

=== Phase 1: 프로젝트 스캔 ===
✓ package.json 분석 완료
✓ tsconfig.json 분석 완료
✓ 디렉토리 구조 파악 완료

=== Phase 2: 코드 패턴 분석 ===
✓ 5개 컴포넌트 분석 완료
✓ API 패턴 추출 완료
✓ 에러 처리 패턴 추출 완료

=== Phase 3: 아키텍처 분석 ===
✓ 레이어 구조 파악 완료
✓ 모듈 의존성 분석 완료

=== Phase 4: 문서 생성 ===
✓ PROJECT_SUMMARY.md 생성 완료
✓ ARCHITECTURE.md 생성 완료
✓ CODE_PATTERNS.md 생성 완료
✓ CONVENTIONS.md 생성 완료

=== Phase 5: 도메인 지식 ===
프로젝트의 비즈니스 도메인에 대해 알려주세요...

✅ 온보딩 완료!

생성된 컨텍스트 문서:
├── .claude/project-context/PROJECT_SUMMARY.md
├── .claude/project-context/ARCHITECTURE.md
├── .claude/project-context/CODE_PATTERNS.md
├── .claude/project-context/CONVENTIONS.md
└── .claude/project-context/DOMAIN_KNOWLEDGE.md

이제 이 프로젝트의 스타일에 맞춰 개발할 준비가 되었습니다!
```

## 참조
- `.claude/skills/project-onboarding/SKILL.md`
- `requirement/PRD-project-onboarding.md`
