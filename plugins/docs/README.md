# docs 플러그인

> 특정 앱의 코드베이스를 분석하여 사람과 AI 모두를 위한 기술 문서를 자동 생성합니다

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/docs help` | 도움말 및 사용법 안내 |
| `/docs generate` | 앱의 전체 기술 문서 최초 생성 |
| `/docs update` | 기존 문서의 추가, 수정, 삭제, 검증 |

## 빠른 시작

```bash
# 전체 문서 최초 생성
/docs generate

# 문서 유지보수 (추가/수정/삭제/검증)
/docs update
```

## 문서의 목적

1. **사람** — 앱의 전체 구조, 비즈니스 로직, API 스펙을 빠르게 파악
2. **AI** — 코드 변경/수정 시 기존 로직, 의존 관계, 사이드 이펙트를 정확히 이해하고 안전하게 작업

## 생성 문서 구조

```
docs/{앱이름}/
├── overview.md              # 앱 개요 및 빠른 이해 가이드
├── architecture.md          # 아키텍처, 패턴, 의존성 규칙
├── api-specification.md     # API 명세서
├── event-specification.md   # 이벤트 명세서
├── database.md              # DB 스키마, 인덱스, 데이터 흐름
├── business-logic.md        # 비즈니스 로직 및 도메인 규칙
└── tech-stack.md            # 기술 스택 설명
```

## 핵심 원칙

- **예시 코드 금지** — 핵심 로직과 규칙만 서술
- **Mermaid 시각화 필수** — 복잡한 개념은 다이어그램으로 표현 (layout: elk)
- **변경 영향도 명시** — 주요 컴포넌트/로직마다 수정 시 영향 범위 기술
- **구현 의도 기록** — "무엇을 하는가"가 아닌 "왜 이렇게 했는가"를 기록

## 플러그인 구조

```
plugins/docs/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── help/SKILL.md         # 도움말
│   ├── generate/SKILL.md     # 최초 문서 생성
│   └── update/SKILL.md       # 추가/수정/삭제/검증
└── README.md
```
