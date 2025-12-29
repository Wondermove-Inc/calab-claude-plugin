---
name: dev-workflow
description: 구조화된 개발 워크플로우를 관리합니다. 새 기능 개발, 프로젝트 시작, 설계, 아키텍처, PRD, 요구사항, 기획 요청 시 자동 활성화. 브레인스토밍부터 구현까지 전체 프로세스를 안내합니다.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Development Workflow Skill

## 목적

구조화된 개발 워크플로우를 통해 체계적인 소프트웨어 개발을 지원합니다.

## 활성화 조건

- "새 기능", "프로젝트 시작", "개발 시작" 요청 시
- "설계해줘", "아키텍처", "PRD", "요구사항" 언급 시
- "기획", "브레인스토밍", "아이디어" 언급 시
- `/dev-*` 명령어 사용 시

## 워크플로우 단계

### Phase 1: Brainstorming (브레인스토밍)

1. 아이디어 확장
2. 문제 정의
3. 타겟 사용자 식별
4. 핵심 가치 제안
5. 범위 정의 (In/Out of Scope)

**산출물**: `docs/prd/{feature}/brainstorm.md`

### Phase 2: PRD (Product Requirements Document)

1. 배경 및 목적
2. 목표 및 비목표
3. 사용자 스토리
4. 기능 요구사항
5. 비기능 요구사항
6. 성공 지표

**산출물**: `docs/prd/{feature}/prd.md`

### Phase 3: Architecture (아키텍처 설계)

1. 시스템 아키텍처
2. 데이터 모델 (ERD)
3. API 설계
4. 기술 스택 결정
5. 보안 고려사항

**산출물**:
- `docs/architecture/system-architecture.md`
- `docs/architecture/erd.md`
- `docs/architecture/api-spec.md`

### Phase 4: Task Planning (태스크 계획)

1. 태스크 분해
2. 의존성 분석
3. 우선순위 결정

**산출물**: `docs/tasks/{feature}/tasks.md`

### Phase 5: Implementation (구현)

1. 베스트 프랙티스 로드
2. 코드 생성
3. 테스트 작성

## 활성화 시 프로토콜

### 1. 현재 상태 확인

```
.claude/memory/CURRENT_CONTEXT.md 읽기
→ 진행 중인 워크플로우가 있는지 확인
```

### 2. 워크플로우 안내

```
============================================
[DEV WORKFLOW] 개발 워크플로우
============================================

 현재 상태: {상태}
 진행 단계: Phase {n}

 사용 가능한 명령어:
• /dev-start [아이디어]   - 새 워크플로우 시작
• /dev-brainstorm        - 브레인스토밍
• /dev-prd              - PRD 작성
• /dev-architecture      - 아키텍처 설계
• /dev-erd              - ERD 설계
• /dev-tasks            - 태스크 분해
• /dev-implement [task]  - 구현 시작
• /dev-status           - 진행 상황 확인

============================================
```

### 3. 상태 저장

`.claude/memory/CURRENT_CONTEXT.md`에 워크플로우 상태 기록

## 참조 파일

- `.claude/memory/TECH_STACK.md` - 기술 스택 및 베스트 프랙티스
- `.claude/templates/` - 문서 템플릿
- `.claude/best-practices/` - 기술별 베스트 프랙티스
