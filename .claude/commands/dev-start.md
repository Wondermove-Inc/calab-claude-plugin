---
description: 전체 개발 워크플로우를 시작합니다. 새 기능 개발, 프로젝트 시작 시 사용하세요. 브레인스토밍부터 태스크 목록까지 자동 생성합니다.
allowed-tools: Read, Write, Edit, Glob
argument-hint: [아이디어 또는 기능 설명]
---

# 개발 워크플로우 시작

## 워크플로우 개요

이 명령어는 다음 단계를 순차적으로 진행합니다:

1. **Phase 1: Brainstorming** - 아이디어 확장 및 문제 정의
2. **Phase 2: PRD** - 요구사항 문서 작성
3. **Phase 3: Architecture** - 시스템 설계 및 ERD
4. **Phase 4: Tasks** - 태스크 분해 및 우선순위

## 실행 절차

### Step 1: 기능명 결정

$ARGUMENTS에서 기능명을 추출하거나 사용자에게 확인:

```
기능명: {feature-name} (kebab-case)
예: user-authentication, payment-system, dashboard
```

### Step 2: 디렉토리 생성

```bash
docs/prd/{feature-name}/
docs/tasks/{feature-name}/
```

### Step 3: Phase 1 - Brainstorming

사용자와 대화형으로 브레인스토밍 진행:

1. **핵심 문제 정의**
   - 어떤 문제를 해결하려고 하나요?
   - 현재 어떻게 해결하고 있나요?

2. **타겟 사용자**
   - 누가 이 기능을 사용하나요?
   - 사용자의 주요 니즈는?

3. **핵심 가치**
   - 이 기능의 핵심 가치는 무엇인가요?
   - 경쟁 제품과의 차별점은?

4. **범위 정의**
   - 반드시 포함할 기능 (Must-have)
   - 있으면 좋은 기능 (Nice-to-have)
   - 제외할 기능 (Out of scope)

**산출물 저장**: `docs/prd/{feature-name}/brainstorm.md`

### Step 4: Phase 2 - PRD 작성

`.claude/templates/prd-template.md` 템플릿을 사용하여 PRD 작성:

- 배경 및 목적
- 목표 (Goals) 및 비목표 (Non-Goals)
- 사용자 스토리
- 기능 요구사항
- 비기능 요구사항
- 성공 지표 (KPIs)

**산출물 저장**: `docs/prd/{feature-name}/prd.md`

### Step 5: Phase 3 - Architecture

1. **기술 스택 확인**
   - `.claude/memory/TECH_STACK.md` 읽기
   - 해당 베스트 프랙티스 로드

2. **시스템 아키텍처 설계**
   - 컴포넌트 다이어그램
   - 데이터 흐름
   - 외부 연동

3. **ERD 설계**
   - 엔티티 정의
   - 관계 정의
   - 인덱스 전략

4. **API 설계**
   - 엔드포인트 목록
   - 요청/응답 스키마
   - 에러 코드

**산출물 저장**:
- `docs/architecture/system-architecture.md`
- `docs/architecture/erd.md`
- `docs/architecture/api-spec.md`

### Step 6: Phase 4 - Task Planning

PRD와 아키텍처 기반으로 태스크 분해:

1. **에픽 (Epic) 정의**
2. **스토리 분해**
3. **태스크 분해**
4. **의존성 분석**
5. **우선순위 결정**

**산출물 저장**: `docs/tasks/{feature-name}/tasks.md`

### Step 7: 상태 업데이트

`.claude/memory/CURRENT_CONTEXT.md` 업데이트:

```markdown
## 워크플로우 상태

- **현재 기능**: {feature-name}
- **현재 단계**: Phase 4 완료, 구현 대기
- **완료된 단계**: Phase 1, 2, 3, 4

## 생성된 문서

- [x] brainstorm.md
- [x] prd.md
- [x] architecture.md
- [x] erd.md
- [x] tasks.md
```

### Step 8: 완료 보고

```
============================================
 개발 워크플로우 완료
============================================

 기능: {feature-name}

 생성된 문서:
• docs/prd/{feature-name}/brainstorm.md
• docs/prd/{feature-name}/prd.md
• docs/architecture/system-architecture.md
• docs/architecture/erd.md
• docs/architecture/api-spec.md
• docs/tasks/{feature-name}/tasks.md

 다음 단계:
1. 태스크 목록 검토: docs/tasks/{feature-name}/tasks.md
2. 구현 시작: /dev-implement [task-id]

============================================
```

## 중요 사항

- 각 단계에서 사용자 확인 후 다음 단계 진행
- 베스트 프랙티스 적용하여 설계
- 모든 산출물은 표준 템플릿 사용
- 진행 상황은 CURRENT_CONTEXT.md에 기록
