---
description: QA 프로세스를 시작합니다. 기능 분석, 계획서 작성, 테스트 준비를 수행합니다.
allowed-tools: Read, Write, Glob, Grep, Bash, mcp__puppeteer__*
---

# /qa - QA 프로세스 시작

## 설명

프론트엔드 기능 QA를 **체계적으로 시작**합니다.
기능 목록을 분석하고, QA 계획서를 작성하며, 테스트 준비를 완료합니다.

**목표**: QA 100% 완료까지 지속 가능한 프로세스 구축

---

## 사용법

```bash
/qa                     # 전체 QA 시작
/qa --from-prd          # PRD 기반 QA
/qa --from-worktree     # Worktree 태스크 기반 QA
/qa --feature 로그인     # 특정 기능만 QA
```

---

## 실행 프로세스

### Step 1: 환경 확인 (30초)

```bash
# 개발 서버 상태 확인
curl -s http://localhost:3000 > /dev/null && echo "서버 실행 중" || echo "서버 미실행"
```

**체크리스트:**
- [ ] 개발 서버 실행 여부
- [ ] MCP Puppeteer 연결 상태
- [ ] 테스트 데이터 준비

### Step 2: 기능 목록 수집 (2분)

**수집 소스:**

| 소스 | 위치 | 추출 정보 |
|------|------|----------|
| PRD | `docs/prd/*.md` | 기능 요구사항 |
| Worktree | `.claude-state/worktree.json` | 구현된 태스크 |
| Routes | `src/app/**/page.tsx` | 페이지 목록 |
| Components | `src/components/**/*.tsx` | UI 컴포넌트 |

**기능 분류:**

```markdown
## 기능 목록

### P0 (Critical) - 핵심 기능
- [ ] 로그인/로그아웃
- [ ] 메인 페이지 로드
- [ ] 결제 프로세스

### P1 (High) - 주요 기능
- [ ] 프로필 수정
- [ ] 검색 기능
- [ ] 필터링

### P2 (Medium) - 보조 기능
- [ ] 설정 변경
- [ ] 알림 확인
```

### Step 3: QA 계획서 작성 (3분)

**자동 생성 파일:**

```
docs/qa/
├── QA_PLAN.md              # QA 계획서
├── TEST_CASES.md           # 테스트 케이스 목록
└── .claude-state/qa/
    ├── qa-plan.json        # 계획 데이터
    └── test-cases.json     # 케이스 데이터
```

**계획서 내용:**

```markdown
# QA 계획서

## 1. 개요
- 프로젝트: {project_name}
- 테스트 범위: {scope}
- 시작일: {date}

## 2. 테스트 전략
- 테스트 유형: E2E (MCP Puppeteer)
- 우선순위: P0 → P1 → P2
- 실행 방식: 자동화 + 수동 검증

## 3. 성공 기준
- 전체 통과율: 100%
- Critical 버그: 0개
- 스크린샷: 모든 케이스 첨부
```

### Step 4: 테스트 케이스 생성 (5분)

**테스트 케이스 형식:**

| ID | 기능 | 시나리오 | 우선순위 | Given | When | Then |
|----|------|----------|----------|-------|------|------|
| TC-001 | 로그인 | 정상 로그인 | P0 | 로그인 페이지 | 올바른 자격 증명 | 대시보드 이동 |
| TC-002 | 로그인 | 잘못된 비밀번호 | P0 | 로그인 페이지 | 틀린 비밀번호 | 에러 메시지 |

**MCP 테스트 스크립트 생성:**

```markdown
## TC-001: 정상 로그인

### 테스트 스크립트

1. 페이지 이동
   ```
   puppeteer_navigate: http://localhost:3000/login
   ```

2. 이메일 입력
   ```
   puppeteer_fill: #email, test@example.com
   ```

3. 비밀번호 입력
   ```
   puppeteer_fill: #password, password123
   ```

4. 로그인 버튼 클릭
   ```
   puppeteer_click: button[type="submit"]
   ```

5. 결과 확인
   ```
   puppeteer_screenshot: tc-001-result
   puppeteer_evaluate: window.location.pathname === '/dashboard'
   ```
```

### Step 5: QA 상태 초기화

**생성되는 상태 파일:**

```json
// .claude-state/qa/qa-status.json
{
  "status": "ready",
  "startDate": "2025-01-01T10:00:00Z",
  "totalCases": 25,
  "completed": 0,
  "passed": 0,
  "failed": 0,
  "blocked": 0,
  "currentCase": null,
  "bugs": []
}
```

---

## 출력 예시

```
🚀 QA 프로세스 시작...

══════════════════════════════════════════════
 Step 1: 환경 확인
══════════════════════════════════════════════
✅ 개발 서버: http://localhost:3000 (실행 중)
✅ MCP Puppeteer: 연결됨
✅ 테스트 환경: 준비 완료

══════════════════════════════════════════════
 Step 2: 기능 목록 수집
══════════════════════════════════════════════
📋 PRD 분석: 15개 기능 발견
📋 Worktree: 8개 완료된 태스크
📋 라우트: 12개 페이지

기능 분류:
 • P0 (Critical): 5개
 • P1 (High): 7개
 • P2 (Medium): 11개

══════════════════════════════════════════════
 Step 3: QA 계획서 작성
══════════════════════════════════════════════
📄 QA_PLAN.md 생성 완료
📄 TEST_CASES.md 생성 완료

══════════════════════════════════════════════
 Step 4: 테스트 케이스 생성
══════════════════════════════════════════════
✅ 총 25개 테스트 케이스 생성
   • 로그인/인증: 5개
   • 메인 페이지: 3개
   • 검색/필터: 4개
   • 결제: 6개
   • 프로필: 4개
   • 기타: 3개

══════════════════════════════════════════════
 Step 5: QA 상태 초기화
══════════════════════════════════════════════
✅ qa-status.json 초기화 완료
✅ 스크린샷 폴더 생성 완료

══════════════════════════════════════════════
🎯 QA 준비 완료!
══════════════════════════════════════════════

📁 생성된 파일:
├── docs/qa/QA_PLAN.md
├── docs/qa/TEST_CASES.md
├── .claude-state/qa/qa-status.json
├── .claude-state/qa/test-cases.json
└── .claude-state/qa/screenshots/

💡 다음 단계:
   /qa-run              → 테스트 실행 시작
   /qa-run TC-001       → 특정 테스트 실행
   /qa-status           → 진행 상태 확인
```

---

## 옵션 설명

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--from-prd` | PRD 문서 기반 기능 추출 | `/qa --from-prd` |
| `--from-worktree` | Worktree 완료 태스크 기반 | `/qa --from-worktree` |
| `--feature [이름]` | 특정 기능만 QA | `/qa --feature 로그인` |
| `--priority [P0/P1/P2]` | 특정 우선순위만 | `/qa --priority P0` |

---

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 테스트 실행 시작 | `/qa-run` |
| 특정 케이스 실행 | `/qa-run TC-001` |
| 진행 상태 확인 | `/qa-status` |
| 계획서 수정 | `/qa-plan --edit` |

---

## 참조

- `/qa-plan` - QA 계획서 상세 생성
- `/qa-run` - 테스트 실행
- `/qa-report` - 보고서 생성
- `/qa-status` - 상태 확인
- `.claude/skills/qa-testing/SKILL.md`
