# Plan Phase - 에이전트 호출 프롬프트

> **planner-phase 에이전트 호출 시 사용되는 프롬프트 템플릿**

---

## 에이전트 호출

```python
Task(
    subagent_type="calab-plugin:planner-phase",
    description="기능 기획 및 PRD 작성",
    prompt="""
## Role
기능 기획 및 PRD 작성 전문가

## Goal
'{feature_name}' 기능에 대한 PRD(Product Requirements Document) 작성

## Input
- 기능명: {feature_name}
- 사용자 요청: {user_request}
- 프로젝트 컨텍스트: .claude/project-context/ (있는 경우)

## Output (필수)
**반드시 생성해야 할 파일:**
.claude/docs/active/{feature_name}/01-brainstorm.md
.claude/docs/active/{feature_name}/02-PRD.md

## Workflow
1. 기능 폴더 생성: .claude/docs/active/{feature_name}/
2. 브레인스토밍 문서 작성 (01-brainstorm.md)
3. PRD 문서 작성 (02-PRD.md)
   - 문제 정의
   - 목표 사용자
   - 기능 요구사항 (P0/P1/P2)
   - 비기능 요구사항
   - 성공 지표 (KPI)
3. 완료 보고

## Constraints
- 01-brainstorm.md, 02-PRD.md 파일명 필수 (다른 이름 금지)
- P0 요구사항 최소 1개 이상
- 검증 가능한 수용 기준 포함

## Template
references/plan.md 참조
"""
)
```

---

## Data Flow

### Input (이전 단계에서)
| 소스 | 데이터 |
|------|--------|
| 사용자 | 기능 요청 |
| /onboard | .claude/project-context/*.md (선택) |

### Output (다음 단계로)
| 산출물 | 다음 단계 |
|--------|----------|
| .claude/docs/active/{feature}/01-brainstorm.md | /dev --design |
| .claude/docs/active/{feature}/02-PRD.md | /dev --design |

---

## 검증

산출물 검증은 `post_skill_artifact_check.py`에서 수행:
- 패턴: `{docs}/*/01-brainstorm.md`, `{docs}/*/02-PRD.md`
- 필수: Yes
- 미생성 시: Exit Code 2 (차단)
