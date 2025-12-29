---
name: project-onboarding
description: 프로젝트를 분석하고 컨텍스트 문서를 생성합니다. 프로젝트 분석, 코드베이스 학습, 온보딩 키워드 시 자동 활성화.
allowed-tools: Read, Write, Glob, Grep
---

# Project Onboarding Skill

## 자동 활성화 조건

이 스킬은 다음 상황에서 자동으로 활성화됩니다:

### 키워드 감지
- "프로젝트 분석", "코드 분석", "온보딩"
- "기존 프로젝트", "이어서 개발", "개발 이어서"
- "코드베이스 학습", "프로젝트 이해"

### 세션 시작 시
새 세션이 시작되면 자동으로:
1. `.claude/project-context/PROJECT_SUMMARY.md` 확인
2. 존재하면 컨텍스트 자동 로드
3. 없으면 `/onboard` 안내 제공

## 핵심 기능

### 1. 프로젝트 컨텍스트 관리

```
.claude/project-context/
├── PROJECT_SUMMARY.md      # 프로젝트 요약
├── ARCHITECTURE.md         # 아키텍처 분석
├── CODE_PATTERNS.md        # 코드 패턴
├── DOMAIN_KNOWLEDGE.md     # 도메인 지식
└── CONVENTIONS.md          # 코딩 컨벤션
```

### 2. 세션 간 컨텍스트 영속성

```
세션 종료 시 → CURRENT_TASK.md 저장
세션 시작 시 → CURRENT_TASK.md 로드
```

### 3. 일관된 코드 작성

코드 작성 전:
1. CODE_PATTERNS.md 참조
2. CONVENTIONS.md 규칙 확인
3. 기존 코드 스타일 일치

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `/onboard` | 프로젝트 전체 분석 및 온보딩 |
| `/onboard-quick` | 빠른 온보딩 (핵심 정보만) |
| `/context-refresh` | 컨텍스트 갱신 |
| `/context-show` | 현재 컨텍스트 표시 |
| `/learn <path>` | 특정 파일/폴더 심층 학습 |

## 온보딩 프로세스

### Phase 1: 프로젝트 스캔
- package.json, tsconfig.json 분석
- 디렉토리 구조 파악
- 주요 파일 식별

### Phase 2: 코드 패턴 분석
- 컴포넌트 구조 추출
- API 패턴 추출
- 에러 처리 패턴 추출

### Phase 3: 아키텍처 분석
- 레이어 구조 파악
- 모듈 의존성 분석

### Phase 4: 문서 생성
- 5개 컨텍스트 문서 자동 생성

### Phase 5: 사용자 확인
- 분석 결과 검증
- 도메인 지식 보완

## 컨텍스트 활용 가이드

### 새 기능 개발 시
1. ARCHITECTURE.md에서 적절한 위치 확인
2. CODE_PATTERNS.md에서 패턴 참조
3. CONVENTIONS.md 규칙 준수
4. 기존 유틸리티 재사용

### 버그 수정 시
1. 관련 모듈 의존성 파악
2. 에러 처리 패턴 확인
3. 테스트 패턴 참조

### 리팩토링 시
1. 현재 아키텍처 이해
2. 영향 범위 분석
3. 패턴 일관성 유지

## 참조 문서

- `.claude/best-practices/project-onboarding.md` - 상세 가이드
- `.claude/commands/onboard.md` - 온보딩 명령어
