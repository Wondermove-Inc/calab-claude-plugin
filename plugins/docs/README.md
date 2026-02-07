# docs 플러그인

> 프로젝트 분석 후 전문적인 기술 문서 콘텐츠를 자동 생성합니다 (Docusaurus 기반)

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/docs:help` | 도움말, 문서 작성 가이드라인 |
| `/docs:generate` | 프로젝트 분석 후 전체 문서 자동 생성 |
| `/docs:add [type]` | 특정 유형의 문서 추가 |
| `/docs:update` | 코드 변경 시 기존 문서 업데이트 |
| `/docs:status` | 문서 커버리지 및 품질 현황 |
| `/docs:validate` | 문서 품질 검증 (링크, 일관성, 완성도) |

## 빠른 시작

```bash
# 전체 문서 생성
/docs:generate

# API 문서 추가
/docs:add api

# 가이드 문서 추가
/docs:add guide "인증 설정하기"

# 문서 현황 확인
/docs:status

# 품질 검증
/docs:validate
```

## 문서 유형

| 유형 | 설명 |
|------|------|
| Getting Started | 설치, 빠른 시작, 기본 사용법 |
| Architecture | 시스템 구조, 컴포넌트, 데이터 흐름 |
| API Reference | 엔드포인트, 파라미터, 응답 스키마 |
| Components | UI 컴포넌트 Props, 이벤트, 사용 예시 |
| Guides | 단계별 가이드, 튜토리얼 |
| Configuration | 설정 옵션, 환경 변수 |
| FAQ | 자주 묻는 질문 |
| Troubleshooting | 에러 해결 가이드 |

## 출력 구조

```
.claude/docs-site/
├── getting-started/
│   ├── introduction.md
│   ├── installation.md
│   └── quick-start.md
├── architecture/
│   ├── overview.md
│   └── data-flow.md
├── api-reference/
│   ├── overview.md
│   └── endpoints/
├── components/
├── guides/
├── configuration/
├── faq.md
└── troubleshooting.md
```

## 문서 품질 기준

- 모든 코드 예시는 복사-붙여넣기로 즉시 실행 가능
- 기능당 최소 4개 예시 (기본, 실전, 고급, 에러 처리)
- Mermaid 다이어그램으로 구조/흐름 시각화
- 스크린샷 플레이스홀더로 UI 위치 명시

## 플러그인 구조

```
plugins/docs/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── docs/SKILL.md       # 메인 스킬
│   ├── add/SKILL.md
│   ├── generate/SKILL.md
│   ├── status/SKILL.md
│   ├── update/SKILL.md
│   └── validate/SKILL.md
└── README.md
```
