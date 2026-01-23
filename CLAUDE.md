# 원더 무브 연구소 Claude Plug-in

> **어떤 상황에서든 동일한 개발 품질을 보장하는** 업무 자동화 플러그인

---

## CRITICAL RULES (절대 무시 금지)

이 섹션의 규칙들은 **모든 응답에서 반드시 준수**해야 합니다.

### 핵심 규칙 요약

1. **컨텍스트 유지**: 작업 시작 전 `.claude/memory/CURRENT_CONTEXT.md` 확인 필수
2. **규칙 준수**: 코드 작성 전 `.claude/memory/PROJECT_RULES.md` 참조 필수
3. **🚨 작업 내용 상세 기록**: 의미 있는 작업 완료 시 Memory에 직접 기록
4. **작업 스택 유지**: 하위 작업 진입 시 상위 작업 목표 기억
5. **Worktree 추적**: 소스 코드 수정 시 자동 시작 (완료는 수동)
6. **UI/UX 필수**: ShadCN/UI 컴포넌트 우선 사용
7. **🚨 Task 완료 검증 필수**: 아래 조건 충족 전까지 다음 Task 금지
8. **🚨 패시브 스킬 조건부 적용**: 요청 타입에 따라 필요한 것만 로드
9. **🚨 할루시네이션 방지 (Anthropic 공식)**: 아래 규칙 절대 준수

### 🚨 할루시네이션 방지 (Anthropic 공식 가이드라인)

> **출처**: docs.anthropic.com, console.anthropic.com/docs - Claude Best Practices

**절대 규칙:**
- **읽지 않은 코드에 대해 추측 금지** - 파일을 열어보지 않은 코드에 대해 절대 추측하지 마세요
- **파일 참조 시 반드시 먼저 읽기** - 사용자가 특정 파일을 언급하면 반드시 먼저 열어서 확인
- **확실하지 않으면 "모르겠다" 인정** - 불확실한 답변보다 "확인이 필요합니다" 선호
- **근거 없는 주장 금지** - 코드를 조사하기 전에 어떤 주장도 하지 마세요

**코드 탐색 전 필수 행동:**
```
1. 관련 파일 먼저 읽고 이해
2. 코드베이스의 스타일, 컨벤션, 추상화 파악
3. 충분한 컨텍스트 확보 후 답변/수정 제안
```

**검증 기법 (복잡한 답변 시):**
- **직접 인용**: 긴 문서(>20K 토큰)에서는 관련 인용문 먼저 추출
- **Chain-of-thought**: 단계별 추론으로 검증
- **외부 지식 제한**: 제공된 문서/코드만 사용하도록 명시

### 🚨 조건부 패시브 로드 (최적화됨)

> 요청 타입에 따라 **필요한 파일만** 로드합니다.

| 요청 타입 | 로드 파일 | 토큰 |
|----------|----------|------|
| **새 기능 구현** (`/dev build`, 엔티티) | clean-architecture + best-practices + code-quality + PROJECT_RULES | ~1,800 |
| **기존 파일 수정** (함수 수정, 변수 변경) | code-quality + {기술}.md | ~1,000 |
| **포맷/주석만** (주석 추가, 정렬) | code-quality만 | ~500 |
| **버그 해결** (에러 수정) | problem-solving | ~1,200 |
| **리서치** (조사, 알아봐) | research-skill | ~800 |

**자동 로드 표시 (Silent Mode):**
```
// Applied: code-quality, typescript.md
```

### 🚨 Task 완료 조건 (Definition of Done)

필수 체크리스트:
- [ ] **AC 100% 충족** - 각 항목 명시적 검증
- [ ] **기능 동작 확인** - 빌드/실행 가능
- [ ] **엣지 케이스 처리** - null, 빈값, 경계값
- [ ] **코드 품질** - 300줄↓, 주석, 타입
- [ ] **사용자 확인** - 중요 기능인 경우

**AC 검증 출력:**
```
[TASK 완료 검증] TASK-001
✅ AC1: 충족 | ✅ AC2: 충족 | ❌ AC3: 미충족 → 추가 구현
결과: ❌ 완료 불가
```

**미충족 시 절대로 다음 Task로 넘어가지 마세요.**

### 🚨 Memory 기록 규칙

**기록 위치:** CURRENT_CONTEXT.md (상세) + WORK_HISTORY.md (요약)

**기록 형식:**
```markdown
- [HH:MM] **[카테고리]** 작업 제목 ✅
  - 목적 | 수행 | 변경 파일 | 결과 | 다음
```

**카테고리:** `구현`, `수정`, `버그픽스`, `리팩토링`, `설계`, `문서화`, `테스트`, `문제해결`

### UI/UX 규칙

- **ShadCN/UI** 표준 컴포넌트 우선 사용
- 커스터마이징 시 **변경 사항 문서화 필수**

---

## 빠른 참조

### 자주 쓰는 명령어

| 명령어 | 자연어 | 설명 |
|--------|--------|------|
| `/dev plan [기능]` | "기획해줘" | 브레인스토밍 + PRD |
| `/dev build [task]` | "구현해줘" | 태스크 구현 |
| `/onboard` | "프로젝트 분석해줘" | 컨텍스트 문서 생성 |
| `/restore-context` | "복원해줘" | 규칙 + 작업 상태 복원 |
| `/solve [문제]` | "해결해줘" | 체계적 문제 해결 |
| `/research [주제]` | "조사해줘" | 검색 + 핵심 요약 |
| `/worktree` | "작업 트리" | 진행률 확인 |
| `/qa` | "QA 시작" | E2E 테스트 |
| `/check-quality` | "품질 검사" | 코드 품질 검사 |
| `/save-progress` | "저장해줘" | 체크포인트 저장 |

**전체 명령어 (35개):** [COMMANDS_REFERENCE.md](docs/COMMANDS_REFERENCE.md) 참조

---

## 자동 동작 요약

| 트리거 | 자동 동작 |
|--------|----------|
| 코드 작성 | 품질 검사 + 베스트 프랙티스 적용 |
| 파일 수정 | 변경 이력 기록 + worktree 업데이트 |
| 세션 시작 | 이전 컨텍스트 안내 |
| Compact | 체크포인트 자동 저장 |
| 민감 파일 | `.env`, `credentials` 자동 차단 |

---

## 자동 활성화 스킬 (11개)

- **코드 작성**: clean-architecture, best-practices, code-quality
- **에러/버그**: problem-solving
- **JIRA/이슈**: jira-integration
- **QA/테스트**: qa-testing
- **작업 관리**: work-tracker, dev-workflow
- **프로젝트 분석**: project-onboarding, research-skill
- **규칙 준수**: project-rules

---

## Compact 발생 시

1. `/restore-context` 실행
2. 복원된 규칙과 작업 상태 확인
3. 작업 재개

---

## 상세 문서

- **전체 명령어**: [COMMANDS_REFERENCE.md](docs/COMMANDS_REFERENCE.md)
- **기능 상세**: [FEATURES_GUIDE.md](docs/FEATURES_GUIDE.md)
- **아키텍처**: [ARCHITECTURE_GUIDE.md](docs/ARCHITECTURE_GUIDE.md)
- **README**: [README.md](README.md)
