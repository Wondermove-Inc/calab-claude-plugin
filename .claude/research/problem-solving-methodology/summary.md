# 문제 해결 플러그인 - 1페이지 요약

## 핵심 개념

**문제 해결 플러그인**은 소프트웨어 개발 중 발생하는 문제(버그, 에러, 장애)를 **체계적으로 분석하고 해결**하는 자동화 도구입니다.

---

## 학습된 방법론 (7개)

| 방법론 | 핵심 | 적용 시점 |
|--------|------|----------|
| **5 Whys** | 반복적 "왜?" 질문 | 원인 불명확 시 |
| **RCA** | 체계적 근본 원인 분석 | 복잡한 문제 |
| **가설 기반** | 관찰→가설→실험→결론 | 모든 문제 |
| **Decision Tree** | 단계별 진단 플로우 | 반복적 문제 |
| **Binary Search** | 이분 탐색으로 범위 축소 | 코드 디버깅 |
| **Fishbone** | 원인-결과 시각화 | 다중 원인 |
| **ITIL** | Incident vs Problem 구분 | 운영 환경 |

---

## 제안 플러그인 구조

### 명령어
```
/solve [문제]          # 문제 해결 시작
/solve --5whys         # 5 Whys 분석
/solve --rca           # RCA 분석
/solve-history         # 과거 사례 검색
/solve-report          # 보고서 생성
```

### 6단계 프로세스
```
Define → Gather → Analyze → Hypothesize → Solve → Document
정의      수집      분석        가설         해결     문서화
```

---

## 핵심 기능

1. **구조화된 문제 정의**: 증상, 재현 조건, 영향 범위 체계적 정리
2. **자동 정보 수집**: Git 로그, 에러 로그, 환경 정보 자동 수집
3. **가이드된 원인 분석**: 5 Whys, Binary Search 등 방법론 적용
4. **가설 검증 도구**: 과학적 방법론으로 원인 검증
5. **자동 문서화**: 해결 보고서 자동 생성
6. **지식 베이스**: 해결 사례 축적 및 유사 문제 추천

---

## 구현 우선순위

| Phase | 항목 | 우선순위 |
|-------|------|----------|
| **MVP** | /solve 명령어, 5 Whys, 보고서 | P0 |
| **확장** | 가설 검증, Binary Search, 지식 베이스 | P1 |
| **고급** | Fishbone, AI 패턴 인식 | P2-P3 |

---

## 예상 효과

- **디버깅 시간 40% 단축** (AI 지원 통계 기반)
- **재발률 감소**: 근본 원인 해결로 동일 문제 재발 방지
- **지식 축적**: 팀 전체의 문제 해결 역량 향상

---

## 생성된 문서

| 문서 | 경로 |
|------|------|
| 전체 보고서 | `.claude/research/problem-solving-methodology/report.md` |
| 설계 계획 | `.claude/research/problem-solving-methodology/plugin-design-plan.md` |
| 1페이지 요약 | `.claude/research/problem-solving-methodology/summary.md` |

---

*완료: 2025-12-30*
