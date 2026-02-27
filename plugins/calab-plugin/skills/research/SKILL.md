---
name: research
description: |
  웹 리서치. 기술 문서, 베스트 프랙티스, 최신 트렌드를 조사합니다.
argument-hint: "[--deep|--compare] [주제]"
allowed-tools: [Read, Write, Glob, Grep, WebSearch, WebFetch, Task, mcp__tavily__tavily-search, mcp__tavily__tavily-extract]
skills: [project-rules, clarification-protocol, skill-completion-rules]
agents:
  primary: web-researcher
  orchestration:
    search: [calab-plugin:web-researcher]
    analyze: [calab-plugin:deep-researcher]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /research - 웹 리서치

> **기술 문서, 베스트 프랙티스, 최신 트렌드 조사**

---

## 사용법

```bash
/research [주제]            # 기본 리서치
/research --deep [주제]     # 심층 분석 포함
/research --compare [A vs B] # 기술 비교
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

### 기본 리서치

```python
Task(
    subagent_type="calab-plugin:web-researcher",
    description="웹 리서치",
    prompt="""
[Role] 기술 리서치 전문가
[Goal] {주제}에 대한 정보 수집 및 정리
[Scope] 공식 문서, 베스트 프랙티스, 최신 동향

## 조사 항목
1. 공식 문서 확인
2. GitHub 예제 검색
3. Stack Overflow 사례
4. 최신 블로그/아티클

[Output] .claude/research/{topic}.md
"""
)
```

### --deep 심층 분석

```python
# 1단계: 정보 수집
Task(
    subagent_type="calab-plugin:web-researcher",
    description="정보 수집",
    prompt="..."
)

# 2단계: 분석 및 종합
Task(
    subagent_type="calab-plugin:deep-researcher",
    description="심층 분석",
    prompt="""
[Role] 기술 분석가
[Goal] 수집된 정보 종합 분석
[Input] web-researcher 결과
[Output] 구조화된 분석 보고서
"""
)
```

---

## 리서치 유형

| 옵션 | 설명 |
|------|------|
| 기본 | 빠른 정보 수집 |
| `--deep` | 심층 분석 + 보고서 |
| `--compare` | 기술 비교 분석 |

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 리서치 결과 | `.claude/research/{topic}.md` |

### 보고서 형식

```markdown
# Research: {주제}

## Summary
[핵심 요약]

## Key Findings
1. [발견 1]
2. [발견 2]

## Sources
- [출처 1](url)
- [출처 2](url)

## Recommendations
[권장 사항]
```

---

## 다음 단계 선택 (필수)

| 완료 후 | 권장 |
|--------|------|
| 기술 조사 완료 | `/plan` 적용 |
| 비교 완료 | 선택 후 구현 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> 리서치가 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
