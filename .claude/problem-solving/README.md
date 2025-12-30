# Problem Solving 저장소

## 디렉토리 구조

```
.claude/problem-solving/
├── active/                     # 진행 중인 문제 해결
│   └── {problem-id}/
│       ├── problem.md          # 문제 정의
│       ├── analysis.md         # 원인 분석
│       ├── hypotheses.md       # 가설 목록
│       ├── experiments.md      # 실험 기록
│       └── solution.md         # 해결책
│
├── resolved/                   # 해결 완료된 문제
│   └── {problem-id}/
│       └── report.md           # 최종 보고서
│
├── knowledge-base/             # 지식 베이스
│   ├── patterns.json           # 문제 패턴 DB
│   └── solutions.json          # 해결책 인덱스
│
└── README.md                   # 이 파일
```

## 사용 방법

### 문제 ID 형식

```
PROB-{YYYYMMDD}-{HHMMSS}
예: PROB-20251230-103045
```

### 상태 관리

1. **진행 중**: `active/{problem-id}/`에 파일 생성
2. **해결 완료**: `resolved/{problem-id}/`로 이동 + 보고서 생성
3. **지식 베이스**: 해결 시 자동으로 `knowledge-base/` 업데이트

### 지식 베이스 구조

**patterns.json**: 문제 패턴 데이터베이스
- 유사 문제 자동 감지
- 해결책 추천

**solutions.json**: 해결 기록
- 과거 해결 사례 검색
- 통계 및 분석

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/solve` | 새 문제 해결 시작 |
| `/solve-log` | 진행 상황 확인 |
| `/solve-history` | 과거 이력 조회 |
| `/solve-report` | 보고서 생성 |

## 자동 정리

- 30일 이상 된 active 문제는 정리 대상
- resolved 문제는 영구 보존
- knowledge-base는 지속적으로 업데이트

---

*생성일: 2025-12-30*
