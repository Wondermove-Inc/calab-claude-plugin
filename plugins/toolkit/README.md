# Toolkit Plugin

> **코드 리뷰/커밋, 이슈 관리, Jira 동기화 도구**

---

## 명령어

### Git 도구

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/toolkit:code-review` | "코드 리뷰해줘" | 최근 변경사항 리뷰 (보안/아키텍처/정확성) |
| `/toolkit:code-review [범위]` | "최근 3개 커밋 리뷰해줘" | 특정 범위 리뷰 |
| `/toolkit:code-commit` | "커밋해줘" | 변경사항 분석 후 커밋 메시지 생성 |
| `/toolkit:code-commit [힌트]` | "인증 수정 커밋해줘" | 힌트 기반 커밋 메시지 생성 |

### 이슈 관리

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/toolkit:create-issue` | "이슈 만들어줘" | beads 이슈 생성 |
| `/toolkit:sync-jira` | "Jira 동기화해줘" | Jira 이슈와 동기화 |

---

## 코드 리뷰 상세

code-review-graph와 Serena를 활용한 구조적 코드 리뷰를 수행합니다.

**리뷰 흐름:**
1. 구조적 영향 분석 (code-review-graph: blast radius, 리스크 점수)
2. 변경사항 파악 (git diff + 변경 컨텍스트)
3. 리뷰 기준 적용 (보안/아키텍처/정확성/언어별 권장사항)
4. Auto-fix 실행 + Needs Decision 분류
5. 리뷰 요약 리포트 생성

**리뷰 기준:**
- **Critical** — 보안 (OWASP, 인젝션, 인증/인가, Secrets)
- **Warning** — 아키텍처 적합성, 정확성 (에러 핸들링, 동시성, 경계값)
- **Suggestion** — 언어별 권장사항 (Go, TypeScript, React, Python)
- **Warning** — AI 생성 코드 검증 (환각 탐지, 의도 일치)

---

## 포함 리소스

```
plugins/toolkit/
├── skills/
│   ├── code-review/       # 코드 리뷰 (references/ 포함)
│   ├── code-commit/       # 커밋 메시지 생성
│   ├── create-issue/      # beads 이슈 생성
│   ├── sync-jira/         # Jira 동기화
│   └── help/              # 도움말
├── guides/                # 공통 가이드
└── knowledge-base/        # 지식 베이스
```
