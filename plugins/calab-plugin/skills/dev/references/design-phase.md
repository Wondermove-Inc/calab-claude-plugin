# Design Phase - 에이전트 호출 프롬프트

> **design 에이전트 호출 시 사용되는 프롬프트 템플릿**

---

## 에이전트 호출

```python
Task(
    subagent_type="calab-plugin:design",
    description="아키텍처 설계",
    prompt="""
## Role
시스템 아키텍처 설계 전문가

## Goal
'{feature_name}' 기능의 아키텍처 설계 문서 작성

## Input (필수)
- PRD 문서: .claude/docs/active/{feature_name}/02-PRD.md
- 프로젝트 규칙: .claude/memory/PROJECT_RULES.md (있는 경우)

## Output (필수)
**반드시 생성해야 할 파일:**
.claude/docs/active/{feature_name}/03-architecture.md

## Workflow
1. 02-PRD.md 읽기
2. 요구사항 분석 (P0/P1 추출)
3. 아키텍처 문서 작성 (03-architecture.md)
   - 시스템 컨텍스트 (C4 Level 1)
   - 기술 스택
   - 디렉토리 구조
   - API 설계
   - 컴포넌트 구조
   - 상태 관리
   - ERD (데이터베이스 사용 시)
4. 완료 보고

## Constraints
- 03-architecture.md 파일명 필수 (다른 이름 금지)
- 02-PRD.md 먼저 읽어야 함
- 기술 스택 선택 이유 명시
- Mermaid 다이어그램 포함 권장

## Template
references/design.md 참조
"""
)
```

---

## Data Flow

### Input (이전 단계에서)
| 소스 | 데이터 |
|------|--------|
| /dev --plan | .claude/docs/active/{feature}/02-PRD.md |

### Output (다음 단계로)
| 산출물 | 다음 단계 |
|--------|----------|
| .claude/docs/active/{feature}/03-architecture.md | /dev --tasks |

---

## 검증

산출물 검증은 `post_skill_artifact_check.py`에서 수행:
- 패턴: `{docs}/*/03-architecture.md`
- 필수: Yes
- 미생성 시: Exit Code 2 (차단)
