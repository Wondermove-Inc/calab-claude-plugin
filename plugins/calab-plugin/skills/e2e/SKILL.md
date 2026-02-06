---
name: e2e
description: |
  E2E 테스트. Playwright/Puppeteer 기반 통합 테스트를 실행합니다.
argument-hint: "[--run|--debug|--record|--headed] [테스트파일]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task, mcp__puppeteer__puppeteer_navigate, mcp__puppeteer__puppeteer_screenshot, mcp__puppeteer__puppeteer_click, mcp__puppeteer__puppeteer_fill, mcp__puppeteer__puppeteer_evaluate]
skills: [project-rules, code-quality, clarification-protocol, skill-completion-rules]
agents:
  primary: e2e-runner
  orchestration:
    run: [calab-plugin:e2e-runner]
    debug: [calab-plugin:e2e-runner]
    record: [calab-plugin:e2e-runner]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /e2e - E2E 테스트

> **Playwright/Puppeteer 기반 통합 테스트 실행**

---

## 사용법

```bash
/e2e                        # 전체 E2E 테스트 실행
/e2e [테스트파일]           # 특정 테스트 실행
/e2e --debug [테스트]       # 디버그 모드
/e2e --record [테스트]      # 실행 녹화
/e2e --headed               # 브라우저 표시 모드
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

```python
Task(
    subagent_type="calab-plugin:e2e-runner",
    description="E2E 테스트 실행",
    prompt="""
[Role] E2E 테스트 전문가
[Goal] {테스트파일 또는 전체} 테스트 실행
[Scope] {--run|--debug|--record}

## 테스트 프레임워크
- Playwright (우선)
- Puppeteer (대안)
- Cypress (대안)

## 실행 단계
1. 테스트 환경 확인
2. 테스트 실행
3. 결과 수집
4. 실패 시 스크린샷 캡처

[Output]
- 테스트 결과 요약
- 실패 시 스크린샷
- 디버그 정보
"""
)
```

---

## 실행 모드

| 옵션 | 설명 |
|------|------|
| `--run` | 기본 실행 (headless) |
| `--debug` | 디버그 모드 (느리게, 로그 상세) |
| `--record` | 실행 영상 녹화 |
| `--headed` | 브라우저 화면 표시 |

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 테스트 결과 | `.claude/docs/active/{feature}/e2e-report.md` |
| 스크린샷 | `.claude/screenshots/` |

### 보고서 형식

```markdown
# E2E Test Report

## Summary
- Total: N tests
- Passed: N
- Failed: N
- Skipped: N

## Results
### Passed
- [x] login.spec.ts

### Failed
- [ ] checkout.spec.ts
  - Error: Element not found
  - Screenshot: screenshots/checkout-error.png

## Performance
- Average duration: Ns
```

---

## 다음 단계 선택 (필수)

| 결과 | 권장 |
|------|------|
| 전체 통과 | 배포 준비 |
| 실패 발생 | `/solve` 로 디버깅 |

> **⚠️ 작업 완료 후 반드시 AskUserQuestion 호출**
>
> E2E 테스트가 완료되면 현재 상황을 분석하여 AskUserQuestion으로 다음 단계 선택지를 제시하세요.
