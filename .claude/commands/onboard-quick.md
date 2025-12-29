---
description: 빠른 프로젝트 온보딩을 실행합니다. 핵심 정보만 분석하여 최소 컨텍스트를 구축합니다.
allowed-tools: Read, Write, Glob
---

# /onboard-quick - 빠른 온보딩

## 설명
핵심 정보만 빠르게 분석하여 최소한의 컨텍스트를 구축합니다. 시간이 촉박하거나 간단한 작업을 위해 사용합니다.

## 사용법
```
/onboard-quick
```

## 분석 범위 (간소화)

### 분석하는 것
- `package.json` - 기술 스택만 추출
- `src/` 최상위 디렉토리 구조
- 1-2개 대표 파일

### 분석하지 않는 것
- 상세 아키텍처 분석
- 모든 파일 패턴 추출
- 도메인 지식 수집

## 실행 순서

### Step 1: 기술 스택 파악

```
package.json에서 추출:
- dependencies
- devDependencies
- scripts
```

### Step 2: 디렉토리 구조 확인

```
src/
├── app/        ← 라우팅
├── components/ ← UI 컴포넌트
├── lib/        ← 유틸리티
└── ...
```

### Step 3: 대표 파일 분석

- 메인 페이지 또는 앱 진입점
- 1개 컴포넌트 예시

### Step 4: 간단 문서 생성

**PROJECT_SUMMARY.md만 생성** (다른 문서는 필요 시 추가)

```markdown
# 프로젝트 요약

## 기술 스택
- Next.js 14
- React 18
- TypeScript
- Prisma

## 디렉토리 구조
src/
├── app/
├── components/
├── lib/
└── types/

## 개발 명령어
- npm run dev
- npm run build
- npm run test
```

## 출력 예시

```
⚡ 빠른 온보딩 시작...

✓ 기술 스택: Next.js 14, React, TypeScript, Prisma
✓ 디렉토리 구조 파악 완료
✓ PROJECT_SUMMARY.md 생성 완료

⚡ 빠른 온보딩 완료! (15초)

기본 컨텍스트가 설정되었습니다.
상세 분석이 필요하면 /onboard 를 실행하세요.
```

## 언제 사용하나요?

| 상황 | 권장 명령어 |
|------|------------|
| 새 프로젝트 투입, 장기 개발 | `/onboard` |
| 간단한 버그 수정 | `/onboard-quick` |
| 빠른 코드 리뷰 | `/onboard-quick` |
| 깊은 이해 필요 없는 작업 | `/onboard-quick` |

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 더 자세한 분석 필요 | `/onboard` |
| 바로 작업 시작 | 코드 작성 시작 (컨텍스트 자동 참조) |

## 참조

- `/onboard` - 전체 온보딩
- `.claude/skills/project-onboarding/SKILL.md`
