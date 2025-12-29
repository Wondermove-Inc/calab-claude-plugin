---
description: PRD (Product Requirements Document)를 작성합니다. 브레인스토밍 결과를 바탕으로 상세 요구사항 문서를 생성합니다.
allowed-tools: Read, Write, Edit, Glob
argument-hint: [기능명 (선택)]
---

# PRD 작성

## 목적

브레인스토밍 결과를 바탕으로 체계적인 요구사항 문서를 작성합니다.

## 실행 절차

### Step 1: 컨텍스트 로드

```
1. .claude/memory/CURRENT_CONTEXT.md - 현재 작업 상태
2. docs/prd/{feature}/brainstorm.md - 브레인스토밍 결과
3. .claude/templates/prd-template.md - PRD 템플릿
4. .claude/research/{관련주제}/ - 관련 리서치 결과 (있는 경우)
```

### Step 1.5: 리서치 결과 자동 통합

**관련 리서치 검색 및 반영:**

1. `.claude/research/` 디렉토리에서 관련 리서치 검색
2. 관련 리서치가 있으면 핵심 인사이트 추출
3. PRD 작성 시 다음 섹션에 자동 반영:
   - 배경 및 목적: 리서치 기반 문제 정의
   - 기능 요구사항: 리서치에서 발견된 베스트 프랙티스
   - 비기능 요구사항: 리서치에서 확인된 주의사항
   - 참조: 리서치 출처 목록

```
리서치 통합 예시:

기능: "사용자 인증"
관련 리서치: .claude/research/jwt-authentication/

→ report.md에서 추출:
  • JWT vs Session: JWT 선택 근거
  • 보안 고려사항: refresh token rotation 필수
  • Best Practice: access token 15분, refresh token 7일

→ PRD 반영:
  FR-005: Refresh Token Rotation 구현 (P0)
  NFR-002: Access Token TTL 15분 이하
```

**리서치 참조 표기:**

```markdown
## 참조 리서치

이 PRD는 다음 리서치 결과를 참조했습니다:

| 리서치 | 주요 반영 내용 | 문서 |
|--------|---------------|------|
| JWT 인증 | 토큰 정책, 보안 고려사항 | .claude/research/jwt-authentication/report.md |
| OAuth 2.0 | 소셜 로그인 플로우 | .claude/research/oauth2/report.md |
```

### Step 2: PRD 작성

`.claude/templates/prd-template.md` 템플릿을 사용하여 다음 섹션 작성:

#### 2.1 배경 및 목적

- 이 기능이 필요한 이유
- 해결하려는 문제
- 기대 효과

#### 2.2 목표 및 비목표

**목표 (Goals)**
- 이 PRD로 달성하려는 것
- 측정 가능한 목표

**비목표 (Non-Goals)**
- 이 PRD에서 다루지 않는 것
- 향후 확장으로 미룰 것

#### 2.3 사용자 스토리

```
As a [사용자 유형],
I want to [원하는 기능],
So that [얻고자 하는 가치].

Acceptance Criteria:
- [ ] 조건 1
- [ ] 조건 2
```

#### 2.4 기능 요구사항

| ID | 기능 | 우선순위 | 설명 |
|----|------|---------|------|
| FR-001 | 기능명 | P0/P1/P2 | 상세 설명 |

#### 2.5 비기능 요구사항

- **성능**: 응답 시간, 처리량
- **보안**: 인증, 권한, 데이터 보호
- **확장성**: 향후 확장 고려사항

#### 2.6 성공 지표 (KPIs)

| 지표 | 현재 | 목표 | 측정 방법 |
|------|------|------|----------|
| 지표명 | 현재값 | 목표값 | 측정 방법 |

### Step 3: PRD 저장

`docs/prd/{feature-name}/prd.md` 저장

### Step 4: 상태 업데이트

`.claude/memory/CURRENT_CONTEXT.md` 업데이트:

```markdown
## 워크플로우 상태

- **현재 기능**: {feature-name}
- **현재 단계**: Phase 2 완료 (PRD)
- **다음 단계**: Phase 3 (Architecture)

## 생성된 문서

- [x] brainstorm.md
- [x] prd.md
- [ ] architecture.md
```

### Step 5: 완료 보고

```
============================================
[PRD] 요구사항 문서 작성 완료
============================================

 기능: {feature-name}
 생성된 문서: docs/prd/{feature-name}/prd.md

 요약:
• 목표: {n}개
• 기능 요구사항: {n}개 (P0: {n}, P1: {n}, P2: {n})
• 사용자 스토리: {n}개

 다음 단계: /dev-architecture

============================================
```

## 참조 파일

- `.claude/templates/prd-template.md` - PRD 템플릿
- `docs/prd/{feature}/brainstorm.md` - 브레인스토밍 결과
