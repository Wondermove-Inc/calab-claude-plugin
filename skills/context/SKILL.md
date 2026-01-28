---
name: context
description: |
  현재 프로젝트 컨텍스트를 표시하거나 갱신합니다. 기술 스택, 패턴, 아키텍처, 도메인 정보를 확인합니다.
  USE WHEN: 컨텍스트, context, 확인, 갱신, refresh, 프로젝트 정보,
  기술 스택, tech stack, 스택, 패턴, 아키텍처, 도메인,
  현재 상황, 현황, status, 정보, info,
  뭘로 만들어졌어, 기술이 뭐야, 어떤 프레임워크
argument-hint: "[--show|--refresh] [tech|patterns|architecture|domain]"
allowed-tools: [Read, Write, Edit, Glob, Grep]
agent: Explore
---

# /context - 컨텍스트 관리

> **프로젝트 컨텍스트 표시 및 갱신**

## 사용법

```bash
/context                   # 컨텍스트 표시 (기본)
/context --show            # 컨텍스트 표시
/context --show tech       # 기술 스택만
/context --show patterns   # 코드 패턴만
/context --show architecture  # 아키텍처만
/context --show domain     # 도메인 지식만
/context --refresh         # 컨텍스트 갱신
/context --refresh patterns  # 패턴만 갱신
/context --help            # 도움말
```

## 인자 파싱

입력: $ARGUMENTS

### 옵션별 라우팅

1. **`--help` 또는 `-h`** → 도움말 출력

2. **`--show` 또는 옵션 없음** → `references/show.md` 실행
   - 현재 컨텍스트 표시
   - 필터 옵션: `tech`, `patterns`, `architecture`, `domain`

3. **`--refresh`** → `references/refresh.md` 실행
   - 코드 변경 감지
   - 컨텍스트 문서 증분 업데이트
   - 필터 옵션: `patterns`, `architecture`, `conventions`, `summary`

## 컨텍스트 출력

```
============================================
 PROJECT CONTEXT: {프로젝트명}
============================================

 📋 프로젝트 정보
 • 이름: {name}
 • 설명: {description}
 • 분석일: {date}

 🔧 기술 스택
 ┌────────────────────────────────────────┐
 │ Frontend │ Next.js 14, React 18       │
 │ Backend  │ Node.js, Express           │
 │ Database │ PostgreSQL, Prisma         │
 │ Testing  │ Jest, Testing Library      │
 └────────────────────────────────────────┘

 📁 디렉토리 구조
 src/
 ├── app/          # Next.js App Router
 ├── components/   # UI 컴포넌트
 ├── features/     # 기능별 모듈
 ├── lib/          # 유틸리티
 └── types/        # 타입 정의

 📝 주요 패턴
 • 컴포넌트: FC + Props 인터페이스
 • API: Route Handler + Zod 검증
 • 상태: TanStack Query + Zustand

 🏗️ 아키텍처
 • 타입: Feature-based
 • 레이어: Presentation → Application → Domain

 📖 도메인
 • 핵심 엔티티: User, Order, Product
 • 비즈니스 규칙: {규칙}

============================================
 마지막 갱신: {timestamp}
 명령어: /context --refresh (갱신)
============================================
```

## 필터 옵션

| 필터 | 표시 내용 |
|------|----------|
| `tech` | 기술 스택만 |
| `patterns` | 코드 패턴만 |
| `architecture` | 아키텍처만 |
| `domain` | 도메인 지식만 |

## Refresh 동작

### 변경 감지
- 현재 상태 vs 기존 컨텍스트 비교
- 새로 추가/삭제된 파일/폴더 감지
- 기술 스택 변경 식별
- 패턴 변화 감지

### 증분 업데이트
- 전체 재분석이 아닌 변경분만 업데이트
- 새 패턴 추가
- 삭제된 패턴 제거
- 분석 날짜 업데이트

## 파일 참조

```
.claude/project-context/
├── PROJECT_SUMMARY.md      # /context --show tech
├── CODE_PATTERNS.md        # /context --show patterns
├── ARCHITECTURE.md         # /context --show architecture
├── CONVENTIONS.md          # (--refresh 대상)
└── DOMAIN_KNOWLEDGE.md     # /context --show domain
```

## 컨텍스트 없을 때

```
⚠️ 프로젝트 컨텍스트가 없습니다.

다음 명령어로 온보딩을 실행하세요:
• /onboard --quick  (빠른 분석, ~1분)
• /onboard          (전체 분석, ~10분)
```

## 레거시 명령어 호환

| 이전 명령어 | 신규 명령어 |
|------------|------------|
| `/context-show` | `/context` 또는 `/context --show` |
| `/context-refresh` | `/context --refresh` |

## Refresh 트리거 상황

- 여러 새 기능 추가 후
- 프로젝트 구조 변경 후
- 새 라이브러리 도입 후
- 다른 개발자의 대규모 변경 후

## 다음 단계

| 상황 | 권장 명령어 |
|------|------------|
| 컨텍스트 확인 | `/context` |
| 특정 정보만 | `/context --show [필터]` |
| 코드 변경 후 | `/context --refresh` |
| 컨텍스트 없음 | `/onboard` |
| 개발 시작 | `/dev --plan [기능]` |
