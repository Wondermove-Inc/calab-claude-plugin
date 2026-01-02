# Calab Claude Plugin

> Claude Code 공식 플러그인 시스템 기반 개발 워크플로우 자동화

---

## 특징

- ✅ **체계적 개발**: Plan → Design → Tasks → Build
- ✅ **클린 아키텍처**: 4-레이어 자동 생성
- ✅ **프로젝트 온보딩**: 5개 컨텍스트 문서 자동 분석
- ✅ **리서치**: 5-10회 검색 + 핵심 요약
- ✅ **문제 해결**: 5 Whys, RCA 방법론
- ✅ **QA 테스트**: MCP Puppeteer E2E 테스트
- ✅ **JIRA 연동**: 양방향 동기화

---

## 설치

```bash
./install-plugin.sh
```

출력된 명령어 복사 후 실행:

```bash
claude plugin marketplace add ~/.claude/calab-marketplace
claude plugin install calab-plugin@calab-marketplace --scope user
```

상세: [INSTALL.md](INSTALL.md)

---

## 사용법

플러그인 명령어는 네임스페이스가 자동으로 붙습니다:

```bash
/calab-plugin:명령어
```

### 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `/calab-plugin:onboard` | 프로젝트 전체 분석 |
| `/calab-plugin:onboard-quick` | 빠른 분석 (1분) |
| `/calab-plugin:dev-plan` | 기획 (PRD) |
| `/calab-plugin:dev-design` | 설계 (아키텍처 + ERD) |
| `/calab-plugin:dev-tasks` | 태스크 분해 |
| `/calab-plugin:dev-build` | 구현 |
| `/calab-plugin:research` | 리서치 |
| `/calab-plugin:solve` | 문제 해결 |
| `/calab-plugin:qa` | QA 테스트 |

### 시나리오별 사용

| 상황 | 명령어 |
|------|--------|
| 새 프로젝트 시작 | `/calab-plugin:dev-plan 기능명` |
| 기존 프로젝트 투입 | `/calab-plugin:onboard` |
| 작업 재개 | `/calab-plugin:restore-context` |
| 버그 해결 | `/calab-plugin:solve 문제` |

---

## 워크플로우

```
리서치 → 기획 → 설계 → 태스크 분해 → 구현 → QA
```

### 개발 단계

1. **리서치**: `/calab-plugin:research OAuth 2.0`
2. **기획**: `/calab-plugin:dev-plan 사용자 인증`
3. **설계**: `/calab-plugin:dev-design`
4. **태스크 분해**: `/calab-plugin:dev-tasks`
5. **구현**: `/calab-plugin:dev-build TASK-001`
6. **QA**: `/calab-plugin:qa`

---

## 자동 적용 스킬

코드 작성 시 자동으로 활성화:

- `clean-architecture` - 4-레이어 구조 강제
- `best-practices` - 기술별 베스트 프랙티스
- `code-quality` - 300줄 제한, 주석 필수
- `project-rules` - 프로젝트 규칙 참조

---

## 프로젝트 구조

```
.claude-plugin/
└── plugin.json              # 플러그인 메타데이터

.claude/
├── commands/                # 35개 슬래시 명령어
├── skills/                  # 11개 자동 활성화 스킬
├── hooks/                   # 11개 이벤트 훅
├── best-practices/          # 15개 기술별 가이드
├── templates/               # 11개 문서 템플릿
├── memory/                  # 프로젝트 규칙/컨텍스트
├── integrations/            # JIRA 연동
└── agents/                  # 서브에이전트
```

---

## 제거

```bash
claude plugin uninstall calab-plugin
claude plugin marketplace remove calab-marketplace
rm -rf ~/.claude/calab-marketplace
```

---

## 문서

- [INSTALL.md](INSTALL.md) - 설치/제거 가이드
- [CLAUDE.md](CLAUDE.md) - 핵심 사용법 (상세)

---

## 라이선스

MIT License - Wonder Move Lab
