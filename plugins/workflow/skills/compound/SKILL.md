---
name: workflow:compound
description: 최근 1주일간 완료된 워크플로우를 전체 분석하여 성공/개선 패턴을 추출하고 시스템 개선안을 제안합니다.
allowed-tools: Agent, Bash, Read
disable-model-invocation: true
---

# /workflow:compound 커맨드

최근 1주일간 완료된 워크플로우를 전체 분석하여 시스템 개선안을 도출합니다.

> **수동 호출 전용**: 워크플로우 자동 흐름에 포함되지 않습니다. 사용자가 직접 호출합니다.

## 사용법

```
/workflow:compound

예시:
/workflow:compound
```

## 동작 방식

### 1단계: 분석 대상 수집

최근 1주일간 closed된 Epic 목록을 수집합니다.

```bash
# 최근 1주일 closed Epic 목록 조회
bd list --status closed --type epic
```

### 2단계: Compound 에이전트 호출

`Agent` 도구를 **포그라운드**(`run_in_background: false`)로 호출합니다. 분석이 완료되면 에이전트의 최종 출력(1줄 요약)이 직접 반환됩니다.

```
Agent(
  subagent_type: "workflow:compound",
  model: "opus",
  run_in_background: false,
  description: "Compound 회고 분석",
  prompt: "최근 1주일간 완료된 워크플로우 전체 분석.
대상 Epic: <수집된 epic-id 목록>
프로젝트: {현재 경로}"
)
```

### 3단계: 에이전트가 수행하는 3-Layer 분석

**L1. 세션 대화 분석** (가장 핵심):
- `~/.claude/projects/<프로젝트경로>/`의 JSONL 세션 파일 분석
- 사용자-AI 상호작용 패턴, 시행착오, 의사결정 과정 추적

**L2. 이슈 기록 분석**:
- 에이전트 호출 순서, Gate 승인 이력, Worker ↔ Reviewer 순환 횟수

**L3. 산출물 분석**:
- Planner/Worker/Reviewer 이슈 품질 + Worker 이슈의 변경 파일 경로에서 실제 코드 읽어 품질 평가

**종합 평가**:
- **5축 점수 평가**: 요구사항 정확도, 설계 품질, 구현 효율, 협업 흐름, 산출물 완성도
- **KIT 패턴 분류**: Keep(유지), Improve(개선), Try(시도)
- **구체적 수정안 생성**: 에이전트 프롬프트, 가이드 변경 제안
- **보고서 저장**: `.workflow/compound/<날짜>.md`

### 4단계: 결과 확인

에이전트가 반환하는 1줄 요약:
```
완료: (Epic N건, 총점 N/25, K:N/I:N/T:N, 수정안 N건) → .workflow/compound/<날짜>.md
```

상세 내용은 보고서 파일에서 확인:
```bash
cat .workflow/compound/<날짜>.md
```

### 5단계: 수정안 적용 (선택)

보고서의 수정안을 검토하고, 적용할 항목을 선택합니다.
수정안 적용은 사용자가 직접 결정합니다.

## 산출물

| 파일 | 위치 | 내용 |
|------|------|------|
| Compound 보고서 | `.workflow/compound/<날짜>.md` | 대상 Epic 목록, 평가 점수, KIT 패턴, 수정안, 트렌드 |

## 사용 예시

```
/workflow:compound
```
결과: Epic 3건 분석, 총점 18/25, Keep 3건, Improve 4건, Try 2건, 수정안 5건
이전 분석 대비 트렌드 포함
