---
name: security
description: |
  보안 검사. OWASP Top 10, 시크릿 탐지, 의존성 취약점을 검사합니다.
  USE WHEN: 보안, security, OWASP, 취약점, vulnerability, 시크릿, secret, 보안 검사
argument-hint: "[--owasp|--secrets|--deps|--full] [경로]"
allowed-tools: [Read, Grep, Glob, Bash, Task]
skills: [project-rules]
agents:
  primary: security-reviewer
  orchestration:
    owasp: [calab-plugin:security-reviewer]
    secrets: [calab-plugin:security-reviewer]
    deps: [calab-plugin:security-reviewer]
    full: [calab-plugin:security-reviewer]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /security - 보안 검사

> **OWASP Top 10, 시크릿 탐지, 의존성 취약점 검사**

---

## 사용법

```bash
/security [경로]            # 전체 보안 검사
/security --owasp [경로]    # OWASP Top 10 검사
/security --secrets [경로]  # 시크릿/키 탐지
/security --deps            # 의존성 취약점 검사
/security --full            # 모든 검사 수행
```

---

## 에이전트 호출 (필수)

> **이 스킬이 로드되면 아래 지침을 따라 Task 도구를 호출하세요.**

```python
Task(
    subagent_type="calab-plugin:security-reviewer",
    description="보안 취약점 검사",
    prompt="""
[Role] 보안 전문가
[Goal] {경로}의 보안 취약점 분석
[Scope] {--owasp|--secrets|--deps|--full}

## 검사 항목
### OWASP Top 10
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection (SQL, XSS, Command)
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Auth Failures
- A08: Data Integrity Failures
- A09: Logging Failures
- A10: SSRF

### 시크릿 탐지
- API 키, 토큰
- 비밀번호, 인증서
- 환경 변수 노출

### 의존성
- npm audit / pip audit
- CVE 취약점

[Output] .claude/docs/security-report.md
"""
)
```

---

## 검사 유형

| 옵션 | 검사 내용 |
|------|----------|
| `--owasp` | OWASP Top 10 취약점 |
| `--secrets` | 하드코딩된 시크릿 |
| `--deps` | 의존성 취약점 |
| `--full` | 위 전체 + 코드 패턴 |

---

## 산출물 (필수)

| 산출물 | 경로 |
|--------|------|
| 보안 리포트 | `.claude/docs/security-report.md` |

### 리포트 형식

```markdown
# Security Report

## Summary
- Critical: N개
- High: N개
- Medium: N개
- Low: N개

## Findings
### [CRITICAL] {취약점명}
- 위치: {파일:라인}
- 설명: {상세}
- 권장 조치: {해결 방법}
```

---

## 다음 단계

| 결과 | 권장 |
|------|------|
| Critical 발견 | 즉시 `/solve` 로 수정 |
| High 발견 | 우선순위 높여 수정 |
| 의존성 취약점 | `npm audit fix` |
