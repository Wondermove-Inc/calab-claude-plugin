---
name: toolkit:code-review
description: 코드 품질(보안/아키텍처/정확성/언어별 권장사항)을 검증하고 개선점을 제안합니다. simplify가 다루지 않는 보안 취약점, 아키텍처 적합성, 설계 패턴, 동시성, AI 코드 검증 등 구조적 리뷰를 수행합니다. 보안 분석, OWASP 취약점 점검, 아키텍처 검증, SOLID 원칙 위반 탐지가 필요할 때 사용합니다.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Code Review Command

변경된 코드의 **보안, 아키텍처, 정확성, 언어별 권장사항**을 검토합니다.
코드 재사용, 중복 제거, hacky 패턴, 효율성은 `/simplify`가 담당하므로 여기서 다루지 않습니다.

## 작업 순서

0. **구조적 영향 분석 (code-review-graph)**
   - `get_minimal_context(task: "code review")` → 리스크 점수, 영향 커뮤니티 조감 (~100토큰)
   - `detect_changes` → 리스크 기반 우선순위로 리뷰 대상 자동 정렬
   - `get_impact_radius` → 변경 파일의 blast radius 확인 (의존 그래프 2홉)
   - 이 결과를 이후 리뷰 범위 판단과 심각도 분류에 활용

1. **변경사항 파악**
   - `git diff HEAD~1` 또는 사용자가 지정한 범위의 변경사항 확인
   - 변경된 파일 목록과 변경 컨텍스트 (관련 이슈, 커밋 메시지) 파악

2. **코드 리뷰 수행**
   - 아래 리뷰 기준에 따라 **변경된 코드만** 분석
   - 프로젝트의 CLAUDE.md, 린트 설정 등 기존 컨벤션 확인 후 적용
   - 각 피드백을 **Auto-fix** vs **Needs Decision**으로 분류

3. **자동 수정 실행**
   - Auto-fix 대상: 보안 취약점, 에러 핸들링 누락, 리소스 해제 누락, 언어별 관용 패턴 위반
   - Needs Decision 대상: 아키텍처/설계 변경, API 변경, 의존성 변경, 동시성 모델 변경

4. **리뷰 요약 리포트 생성**

```
## Code Review Summary

### Overall Assessment
- Quality Score: X/10
- Issues Found: X (Critical: X, Warning: X, Suggestion: X)
- Auto-fixed: X items

### Auto-fixed (자동 수정 완료)
| # | 파일 | 내용 | 수정 내용 |
|---|------|------|----------|
| 1 | path/to/file:line | [이슈] | [수정한 내용] |

### Needs Decision (사용자 판단 필요)
| # | 파일 | 내용 | 판단 사유 | 수정 방안 |
|---|------|------|----------|----------|
| 1 | path/to/file:line | [이슈] | [사용자 판단이 필요한 이유] | [선택지] |

### Good Points
- [잘 작성된 부분들]
```

## 사용 예시

```
/toolkit:code-review                          # 최근 커밋과 현재 변경사항 리뷰
/toolkit:code-review HEAD~3..HEAD             # 최근 3개 커밋 리뷰
/toolkit:code-review src/service.ts           # 특정 파일만 리뷰
```

---

## 리뷰 원칙

- **변경 코드 집중**: 새로 도입된 이슈만 보고
- **높은 확신도**: 추측성 지적보다 명확한 이슈에 집중
- **프로젝트 컨벤션 우선**: 일반 규칙보다 기존 패턴을 우선
- **심각도 분류**: Critical(보안) → Warning(아키텍처/정확성) → Suggestion(언어별 패턴)
- **NOTICED BUT NOT TOUCHING**: 변경 범위 밖에서 발견한 기존 이슈는 수정하지 않고, 리포트 하단에 별도 기록

리포트에 범위 외 발견사항이 있으면 다음 섹션을 추가합니다:

```
### Noticed But Not Touching (범위 외 발견)
| # | 파일 | 내용 | 사유 |
|---|------|------|------|
| 1 | path/to/file:line | [기존 이슈] | 이번 변경과 무관 |
```

---

## 신뢰 수준 체계

Untrusted → Trusted 경계를 넘는 데이터 흐름에서 검증이 누락되면 Critical로 분류합니다. 수준 정의는 글로벌 CLAUDE.md의 MCP 도구 활용 정책을 참조.

## 리뷰 기준

### 1. 보안 (Security) — Critical

- **입력 검증**: 모든 외부 입력에 검증이 적용되는가 (화이트리스트 선호)
- **인젝션 방지**: SQL, XSS, Command Injection 취약점
- **인증/인가**: 적절한 권한 검사, 인증 우회 불가 여부
- **Secrets 관리**: API 키, 비밀번호 하드코딩 여부
- **민감 정보 노출**: 로그, 에러 메시지, 응답에 민감 정보 포함 여부
- **의존성 보안**: 알려진 취약점이 있는 의존성 사용 여부

#### 자동화 스캔 (변경된 언어/파일이 있을 때만 실행)

```bash
# Secrets — 변경된 파일만 스캔
command -v gitleaks &>/dev/null && git diff --name-only HEAD~1 | xargs gitleaks detect --source

# 의존성 — 의존성 파일이 변경된 경우에만
git diff --name-only HEAD~1 | grep -q "go\.\(mod\|sum\)" && command -v nancy &>/dev/null && go list -json -m all | nancy sleuth
git diff --name-only HEAD~1 | grep -q "package" && [ -f package.json ] && npm audit 2>/dev/null
git diff --name-only HEAD~1 | grep -q "requirements" && command -v pip-audit &>/dev/null && pip-audit

# 정적 분석 — 해당 언어 파일이 변경된 경우에만
git diff --name-only HEAD~1 | grep -q "\.go$" && command -v gosec &>/dev/null && gosec ./...
git diff --name-only HEAD~1 | grep -q "\.py$" && command -v bandit &>/dev/null && bandit -r .
```

### 2. 아키텍처 적합성 (Architecture) — Warning

- **계층 분리**: 프레젠테이션/비즈니스/데이터 계층 간 경계 유지 여부
- **의존성 방향**: 의존성이 안쪽(도메인)을 향하는가, 역방향 의존 여부
- **모듈 경계**: 패키지/모듈 간 순환 의존 여부
- **책임 분리**: 하나의 모듈이 여러 책임을 담당하지 않는가 (SRP)
- **인터페이스 설계**: 외부 API가 내부 구현에 결합되지 않았는가
- **설정 관리**: 환경별 설정이 코드와 분리되어 있는가

### 3. 정확성 (Correctness) — Warning

- **에러 핸들링**: 에러 무시 여부, 컨텍스트 보존 여부
- **리소스 관리**: 파일, 연결, 메모리 등 리소스 해제 여부
- **동시성**: race condition, deadlock, goroutine 누수, channel 미닫힘
- **경계값 처리**: nil/null/empty 체크, 오버플로우, off-by-one 에러

### 4. 언어별 권장사항 — Suggestion

변경된 파일의 언어에 해당하는 참조 가이드를 읽고, 해당 기준으로 리뷰한다.
각 가이드에는 항목별 Bad/Good 예시와 근거가 포함되어 있다.

| 언어 | 참조 파일 | 주요 항목 |
|------|----------|----------|
| Go | `references/go.md` | 에러 처리, 네이밍, 타입 안전성, 동시성, 리소스 관리, 인터페이스 설계 |
| TypeScript | `references/typescript.md` | 타입 안전성, null 안전성, 불변성, 에러 처리, 비동기 처리, 모듈 설계 |
| React | `references/react.md` | Hook 규칙, 컴포넌트 설계, 상태 관리, 렌더링 최적화 |
| Python | `references/python.md` | 타입 힌트, 예외 처리, 함수 설계, 리소스 관리, 보안 |

### 5. AI 생성 코드 검증 — Warning

- **환각 탐지**: 존재하지 않는 함수, 라이브러리, API 사용 여부
- **의도 일치**: 요청된 변경과 실제 코드 일치 여부
- **코드베이스 정합성**: 기존 코드 스타일/패턴과 일치 여부
