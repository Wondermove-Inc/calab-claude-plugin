---
name: workflow:compound
description: 완료된 워크플로우를 분석하여 성공/개선 패턴을 추출하고 시스템 개선안을 제안합니다.
disable-model-invocation: true
---

# /workflow:compound 커맨드

완료된 워크플로우의 회고 분석을 수행하고, 워크플로우 시스템의 구체적 개선안을 제안합니다.

## 사용법

### 특정 워크플로우 분석
```
/workflow:compound <epic-id>

예시:
/workflow:compound calab-claude-plugin-abc123
```

### 최근 워크플로우 자동 선택
```
/workflow:compound --latest
```

### 전체 트렌드 분석
```
/workflow:compound --trend
```
기존 `.workflow/compound/` 의 모든 분석 결과를 종합하여 트렌드를 보여줍니다.

## 동작 방식

### 1단계: 분석 대상 확인

`Task` 도구로 `workflow:compound` 에이전트를 호출합니다.

#### 특정 Epic 분석
```
Task (subagent_type: workflow:compound, model: opus, run_in_background: true):
"Compound 분석: <epic-id>
프로젝트: {현재 경로}"
```

#### 최근 워크플로우 (--latest)
```bash
# 가장 최근 closed Epic 찾기
bd list --status closed --type epic | head -1
```

찾은 Epic ID로 compound 에이전트를 호출합니다.

#### 트렌드 분석 (--trend)
```
Task (subagent_type: workflow:compound, model: opus, run_in_background: true):
"트렌드 분석 수행.
.workflow/compound/ 디렉토리의 모든 분석 결과를 종합.
프로젝트: {현재 경로}"
```

### 2단계: 에이전트가 수행하는 3-Layer 분석

에이전트는 3개 데이터 소스를 종합 분석합니다:

**L1. 세션 대화 분석** (가장 핵심):
- `~/.claude/projects/<프로젝트경로>/` 의 JSONL 세션 파일 분석
- 사용자-AI 상호작용 패턴, 시행착오, 의사결정 과정 추적
- 사용자 피드백(수정 요청, 거부, 칭찬) 분류

**L2. 이슈 기록 분석**:
- 에이전트 호출 순서, Gate 승인 이력, 재시도 기록

**L3. 산출물 품질 분석**:
- spec.md, design.md, 코드, 테스트 평가

**종합 평가**:
- **5축 점수 평가**: 요구사항 정확도, 설계 품질, 구현 효율, 협업 흐름, 산출물 완성도
- **KIT 패턴 분류**: Keep(유지), Improve(개선), Try(시도)
- **구체적 수정안 생성**: 에이전트 프롬프트, 가이드, 템플릿 변경 제안
- **보고서 저장**: `.workflow/compound/<epic-id>.md`

### 3단계: 결과 확인

에이전트가 반환하는 1줄 요약:
```
완료: <issue-id> (총점 N/25, K:N/I:N/T:N, 수정안 N건) → .workflow/compound/<epic-id>.md
```

상세 내용은 보고서 파일에서 확인:
```bash
cat .workflow/compound/<epic-id>.md
```

### 4단계: 수정안 적용 (선택)

보고서의 수정안을 검토하고, 적용할 항목을 선택합니다.
수정안 적용은 사용자가 직접 결정합니다.

## 산출물

| 파일 | 위치 | 내용 |
|------|------|------|
| Compound 보고서 | `.workflow/compound/<epic-id>.md` | 평가 점수, KIT 패턴, 수정안 |

## 사용 예시

### 예시 1: 기능 개발 후 회고
```
/workflow:compound calab-claude-plugin-abc123
```
결과: 총점 18/25, Keep 3건, Improve 4건, Try 2건, 수정안 5건

### 예시 2: 트렌드 확인
```
/workflow:compound --trend
```
결과: 최근 5개 워크플로우의 점수 트렌드, 개선 추이, 미적용 수정안 목록

### 예시 3: Planner 자동 호출
워크플로우 Gate 3 통과 후 Planner가 사용자에게 compound 분석 실행 여부를 묻습니다:
```
Gate 3 통과 완료. Compound 분석을 실행할까요?
- 예: 워크플로우 회고 및 개선안 도출
- 아니오: 워크플로우 종료
```

## Compound Engineering 루프

```
Plan → Work → Review → Compound → Repeat
                         ↑
                    이 단계를 수행

Plan: 다음 워크플로우에서 이전 compound 결과 참조
Work: 개선된 에이전트/가이드로 더 효율적 작업
Review: 강화된 기준으로 더 정확한 검토
Compound: 새로운 학습 축적
```

매 워크플로우 후 compound를 실행하면, 학습이 누적되어 시스템이 점점 더 정확하고 효율적으로 작동합니다.
