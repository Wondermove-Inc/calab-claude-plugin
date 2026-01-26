---
name: toolkit:problem-solving
description: 문제 해결 방법론을 적용합니다. 에러, 버그, 문제, 디버깅, 해결 키워드 시 자동 활성화. 5 Whys, RCA, 가설 기반 접근을 사용합니다.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch
---

# Problem Solving Skill

## 자동 활성화 조건

이 스킬은 다음 키워드가 감지되면 자동으로 활성화됩니다:

**문제 관련**:
- "에러", "오류", "버그", "문제"
- "안 돼", "안되", "작동 안함", "동작 안함"
- "실패", "failure", "error", "bug"

**해결 관련**:
- "해결", "디버깅", "디버그", "debug"
- "왜 이런지", "원인", "이유"
- "고치", "fix", "수정"

**분석 관련**:
- "분석", "원인 분석", "RCA"
- "5 whys", "왜왜왜"

---

## 핵심 원칙

### 1. 증상과 원인 구분

```
❌ 나쁜 예: 증상을 해결
   "500 에러가 나니까 try-catch로 감싸자"

✅ 좋은 예: 원인을 해결
   "왜 500 에러가 나는지 확인하자"
   → DB 쿼리 실패
   → 컬럼 없음
   → 마이그레이션 누락
   → 마이그레이션 실행
```

### 2. 체계적 접근

문제 해결 시 반드시 6단계 프로세스 따르기:

```
1. Define   - 문제 정확히 정의
2. Gather   - 관련 정보 수집
3. Analyze  - 원인 분석 (5 Whys, RCA)
4. Hypothesize - 가설 수립 및 검증
5. Solve    - 해결책 적용
6. Document - 문서화 및 학습
```

### 3. 가설 기반 접근

```
❌ 나쁜 예: 무작위 시도
   "이것저것 바꿔보자"

✅ 좋은 예: 가설 검증
   "X가 원인이면 Y 현상이 있을 것이다"
   → 실험으로 검증
   → 가설 채택/기각
```

### 4. 문서화 필수

모든 문제 해결 과정을 기록:
- 문제 정의
- 분석 과정
- 검증한 가설들
- 최종 해결책
- 재발 방지책

---

## 방법론 가이드

### 5 Whys (근본 원인 추적)

**사용 시점**: 원인이 불명확할 때

**프로세스**:
1. 문제 현상 명시
2. "왜?" 질문 반복 (3-7회)
3. 더 이상 "왜?"가 의미없을 때 = 근본 원인

**예시**:
```
문제: 배포 후 서비스 다운
Why 1: 왜? → 메모리 부족
Why 2: 왜? → 메모리 누수
Why 3: 왜? → 이벤트 리스너 미해제
Why 4: 왜? → cleanup 코드 없음
Why 5: 왜? → 코드 리뷰 체크리스트에 없음
→ 근본 원인: 리뷰 체크리스트 미흡
```

**주의사항**:
- 추측 아닌 사실 기반 답변
- 5번이 정답이 아님 (상황에 따라 3~7회)
- 다중 원인 시 분기하여 분석

### Root Cause Analysis (RCA)

**사용 시점**: 복잡한 문제, 다중 원인

**8단계**:
1. 문제 정의
2. 데이터 수집
3. 원인 식별
4. 근본 원인 확정
5. 해결책 개발
6. 해결책 구현
7. 효과 검증
8. 문서화

### 가설 기반 접근 (Scientific Method)

**사용 시점**: 모든 문제에 적용 가능

**프로세스**:
```
1. 관찰: 현상 파악
2. 가설: "X가 원인이다"
3. 예측: "X를 수정하면 Y가 된다"
4. 실험: 수정 적용
5. 분석: 결과 확인
6. 결론: 가설 채택/기각
```

### Binary Search Debugging

**사용 시점**: 코드 내 버그 위치 특정

**프로세스**:
1. 코드 범위 설정
2. 중간 지점에 검증 포인트
3. 정상/비정상 판단
4. 범위 절반으로 축소
5. 반복 (O(log n))

### Fishbone Diagram (Ishikawa)

**사용 시점**: 다중 원인 시각화

**6M 카테고리**:
- Man (사람): 실수, 지식 부족
- Machine (기계): 시스템, 인프라
- Method (방법): 프로세스, 절차
- Material (자재): 데이터, 입력
- Measurement (측정): 모니터링, 로깅
- Milieu (환경): 설정, 외부 의존성

---

## 자동 정보 수집

문제 발생 시 자동으로 수집할 정보:

```bash
# Git 정보
git log --oneline -10          # 최근 커밋
git status                      # 현재 상태
git diff --name-only HEAD~5     # 최근 변경 파일

# 환경 정보
node --version                  # Node 버전
cat package.json | jq '.dependencies' # 의존성

# 에러 정보
# 사용자 제공 에러 메시지, 스택 트레이스
```

---

## 유사 문제 자동 추천

지식 베이스에서 유사 문제 검색:

```
현재 문제 키워드: ["500", "DB", "쿼리"]
    ↓
지식 베이스 검색
    ↓
유사 문제 추천:
• PROB-012: DB 쿼리 실패 (유사도 85%)
• PROB-008: 커넥션 에러 (유사도 60%)
```

---

## 저장 구조

```
.claude/problem-solving/
├── active/                     # 진행 중
│   └── {problem-id}/
│       ├── problem.md          # 문제 정의
│       ├── analysis.md         # 분석 기록
│       ├── hypotheses.md       # 가설 목록
│       └── experiments.md      # 실험 기록
│
├── resolved/                   # 해결 완료
│   └── {problem-id}/
│       └── report.md           # 최종 보고서
│
└── knowledge-base/             # 지식 베이스
    ├── patterns.json           # 문제 패턴
    └── solutions.json          # 해결책 인덱스
```

---

## 출력 형식

### 분석 시작

```
============================================
[SOLVE] 문제 해결 시작
============================================

 🔍 문제: {문제 설명}
 📁 ID: {problem-id}

 현재 단계: Phase 1 - 문제 정의

============================================
```

### 5 Whys 진행

```
[SOLVE] 5 Whys 분석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

문제: {문제}

Why 1: {질문}
→ {답변}

Why 2: {질문}
→ {답변}

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
근본 원인: {근본 원인}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 해결 완료

```
============================================
[SOLVE] 문제 해결 완료
============================================

 ✅ 문제: {문제}
 🎯 원인: {원인}
 💡 해결: {해결책}
 ⏱️ 시간: {소요 시간}

 📁 보고서: .claude/problem-solving/resolved/{id}/

============================================
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/solve [문제]` | 문제 해결 시작 |
| `/solve --5whys` | 5 Whys 분석 |
| `/solve --rca` | RCA 프로세스 |
| `/solve --hypothesis` | 가설 기반 접근 |
| `/solve --binary` | Binary Search 디버깅 |
| `/solve-log` | 진행 상황 확인 |
| `/solve-history` | 과거 이력 조회 |
| `/solve-report` | 보고서 생성 |

---

## 참조 파일

- `skills/problem-solving/methods/five-whys.md`
- `skills/problem-solving/methods/rca.md`
- `skills/problem-solving/methods/hypothesis.md`
- `skills/problem-solving/methods/binary-search.md`
- `skills/problem-solving/methods/fishbone.md`
- `templates/problem-definition.md`
- `templates/solution-report.md`
