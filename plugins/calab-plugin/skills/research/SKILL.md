---
name: research
description: |
  심층 리서치를 수행합니다. 주제에 대해 5-10회 검색 후 핵심 요약을 제공합니다.
  USE WHEN: 리서치, research, 조사, investigate, 알아봐, 찾아봐, search,
  검색, 정보, information, 최신, latest, 트렌드, trend,
  베스트 프랙티스, best practices, 권장, recommend,
  비교, compare, comparison, 어떤게 좋아, 뭐가 나아,
  방법, how to, 가이드, guide,
  레퍼런스, reference, 참고, 자료
argument-hint: "<주제> [--quick | --deep]"
allowed-tools: [Read, Write, WebSearch, WebFetch, mcp__tavily__tavily-search, mcp__tavily__tavily-extract, mcp__tavily__tavily-crawl, mcp__tavily__tavily-map]
agent: web-researcher
agents:
  primary: web-researcher
  secondary: deep-researcher
  orchestration:
    plan: [Plan]
    search: [web-researcher]
    extract: [web-researcher]
    crawl: [web-researcher]
    analyze: [deep-researcher, code-reviewer]
    report: [deep-researcher, doc-updater]
---

# /research - 심층 리서치 및 핵심 요약

> **체계적 리서치 + 핵심 추출 + 보고서 생성**

## 사용법

```bash
/research <주제>              # 리서치 시작
/research <주제> --quick      # 빠른 리서치 (3회 검색)
/research <주제> --deep       # 심층 리서치 (10회 검색)
```

## 실행 절차

### Phase 1: 리서치 계획 수립

**주제 분석 및 검색 전략 수립:**

```
============================================
 RESEARCH: {주제}
============================================

 리서치 계획:

 1. 핵심 질문 정의
    • {주제}란 무엇인가?
    • 왜 사용하는가? (목적/장점)
    • 어떻게 적용하는가? (방법)
    • 주의사항/단점은?
    • 실제 사례는?

 2. 검색 전략
    • 기본 개념 검색
    • 장단점 비교 검색
    • 실제 적용 사례 검색
    • 베스트 프랙티스 검색
    • 최신 트렌드 검색

============================================
```

### Phase 2: 다중 검색 수행

**5-10회 Tavily 검색 자동 수행:**

| 검색 | 쿼리 | 목적 |
|------|------|------|
| 1 | "{주제} 정의 개념" | 기본 이해 |
| 2 | "{주제} 장점 benefits" | 장점 파악 |
| 3 | "{주제} 단점 problems" | 단점/주의사항 |
| 4 | "{주제} 사용법 how to" | 적용 방법 |
| 5 | "{주제} 예제 example" | 실제 사례 |
| 6 | "{주제} best practices" | 베스트 프랙티스 |
| 7 | "{주제} vs 대안" | 대안 비교 |
| 8 | "{주제} 2024 2025 latest" | 최신 트렌드 |

### Phase 3: 실시간 핵심 추출

**각 검색 결과에서 즉시 핵심 추출:**

```
[검색 1/8] "{주제} 정의 개념"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 핵심 발견:
 • {핵심 포인트 1}
 • {핵심 포인트 2}
 출처: {URL}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 4: 종합 분석

**모든 검색 결과 종합:**

1. 중복 제거
2. 모순점 식별
3. 신뢰도 평가
4. 우선순위 결정

### Phase 5: 리서치 보고서 생성

**`.claude/research/{topic}/report.md` 생성:**

```markdown
# 리서치 보고서: {주제}

## 메타 정보
| 항목 | 내용 |
|------|------|
| 주제 | {주제} |
| 리서치 일시 | {날짜} |
| 검색 횟수 | {n}회 |
| 참조 출처 | {n}개 |

---

## 1. 핵심 요약 (Executive Summary)

> **한 줄 요약**: {주제}는 {핵심 정의}

### 3줄 요약
1. **정의**: {무엇인가}
2. **목적**: {왜 사용하는가}
3. **효과**: {어떤 이점이 있는가}

---

## 2. 주요 발견 사항 (Key Findings)

### 핵심 포인트 (5-7개)

| # | 포인트 | 중요도 | 출처 |
|---|--------|--------|------|
| 1 | {핵심 포인트 1} | ⭐⭐⭐ | [1] |
| 2 | {핵심 포인트 2} | ⭐⭐⭐ | [2] |

---

## 3. 상세 분석

### 3.1 개념 정의
### 3.2 장점
### 3.3 단점/주의사항
### 3.4 적용 방법
### 3.5 실제 사례

---

## 4. 실행 액션 아이템

### 즉시 적용 가능
- [ ] {액션 1}
- [ ] {액션 2}

---

## 5. 출처 및 참조

| # | 출처 | URL | 신뢰도 |
|---|------|-----|--------|
| [1] | {사이트명} | {URL} | ⭐⭐⭐ |
```

### Phase 6: 완료 보고

```
============================================
 RESEARCH 완료: {주제}
============================================

 📊 리서치 통계:
 • 검색 횟수: 8회
 • 분석 출처: 15개
 • 추출 포인트: 23개
 • 핵심 인사이트: 5개

 📁 생성된 문서:
 • .claude/research/{topic}/report.md (전체 보고서)
 • .claude/research/{topic}/summary.md (1페이지 요약)
 • .claude/research/{topic}/sources.md (출처 목록)

 🎯 핵심 요약:
 ┌─────────────────────────────────────────┐
 │ {주제}는 {핵심 정의 한 문장}              │
 │                                          │
 │ 핵심 포인트:                              │
 │ 1. {포인트 1}                             │
 │ 2. {포인트 2}                             │
 │ 3. {포인트 3}                             │
 └─────────────────────────────────────────┘

============================================
```

## 출력 파일 구조

```
.claude/research/
└── {topic}/
    ├── report.md      # 전체 보고서 (상세)
    ├── summary.md     # 1페이지 핵심 요약
    ├── sources.md     # 출처 목록
    └── meta.json      # 리서치 메타데이터
```

## 참조 파일

### 템플릿 (스킬 내부)

| 용도 | 템플릿 |
|------|--------|
| 리서치 보고서 | `templates/research-report-template.md` |

### 베스트 프랙티스 (스킬 내부)

- `references/anthropic-official.md` - 검색/분석 가이드
