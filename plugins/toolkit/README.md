# Toolkit Plugin

> 리서치 및 문제 해결 도구

## 명령어

### Research (리서치)

```bash
/toolkit:research [주제]             # 기본 (5회 검색)
/toolkit:research [주제] --quick     # 빠른 (3회)
/toolkit:research [주제] --deep      # 심층 (10회)
```

### Solver (문제 해결)

```bash
/toolkit:solve [문제]           # 체계적 분석
/toolkit:solve-log              # 분석 진행 상황
/toolkit:solve-history          # 과거 사례 검색
/toolkit:solve-report [id]      # 해결 보고서
```

## 스킬

- **research-skill**: 웹 검색 기반 정보 수집 및 분석
- **problem-solving**: 체계적 문제 해결 방법론 (5 Whys, Fishbone, RCA 등)

## 문제 해결 방법론

| 방법 | 설명 | 적합한 상황 |
|------|------|------------|
| 5 Whys | 근본 원인 추적 | 단일 원인 문제 |
| Fishbone | 다중 원인 분류 | 복잡한 문제 |
| Binary Search | 이분 탐색 | 회귀 버그 |
| Hypothesis | 가설 검증 | 불확실한 상황 |
| RCA | 근본 원인 분석 | 시스템 장애 |
