---
name: docs
description: |
  문서 생성. API, 컴포넌트, 가이드 문서를 자동 생성합니다.
argument-hint: "[--api|--component|--guide|--update] [대상]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Task]
skills: [project-rules, code-quality, skill-completion-rules]
agents:
  primary: docs-generator
  orchestration:
    api: [calab-plugin:docs-generator]
    component: [calab-plugin:docs-generator]
    guide: [calab-plugin:docs-generator]
    update: [calab-plugin:doc-updater]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /docs - 문서 생성

> **API, 컴포넌트, 가이드 문서 자동 생성**

---

## 사용법

```bash
/docs [대상]                # 자동 감지하여 문서 생성
/docs --api [경로]          # API 엔드포인트 문서 생성
/docs --component [경로]    # 컴포넌트 문서 생성
/docs --guide [주제]        # 사용 가이드 생성
/docs --update              # 기존 문서 업데이트
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

### 기본 모드

```python
Task(
    subagent_type="calab-plugin:docs-generator",
    description="문서 생성",
    prompt="""
[Role] 문서 생성 전문가
[Goal] {대상}에 대한 문서 생성
[Scope] {경로 또는 주제}
[Output] docs/{type}/{name}.md

## 문서 필수 항목
- Overview: 개요
- Usage: 사용법
- API/Props: 인터페이스
- Examples: 예제 코드
- Related: 관련 문서
"""
)
```

### --update 모드

```python
Task(
    subagent_type="calab-plugin:doc-updater",
    description="문서 업데이트",
    prompt="코드 변경 사항을 반영하여 기존 문서 업데이트"
)
```

---

## 지원 문서 유형

| 유형 | 옵션 | 출력 위치 |
|------|------|----------|
| API 문서 | `--api` | `docs/api/{endpoint}.md` |
| 컴포넌트 | `--component` | `docs/components/{name}.md` |
| 가이드 | `--guide` | `docs/guides/{topic}.md` |
| 아키텍처 | `--architecture` | `docs/architecture/*.md` |

---

## 산출물 (필수)

| 산출물 | 필수 |
|--------|------|
| 해당 문서 파일 | Yes |
| 예제 코드 포함 | Yes |

---

## 다음 단계 선택 (필수)

| 완료 후 | 권장 |
|--------|------|
| API 문서 생성 | `/security --api` 보안 검사 |
| 컴포넌트 문서 | 관련 테스트 확인 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> 문서 생성이 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
