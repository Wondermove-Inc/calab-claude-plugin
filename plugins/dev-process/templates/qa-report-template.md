# QA 보고서

> 생성일: {TODAY}
> 프로젝트: {PROJECT_NAME}

---

## 1. 요약 (Executive Summary)

### 1.1 테스트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트 | {PROJECT_NAME} |
| 버전 | {VERSION} |
| 테스트 기간 | {START_DATE} ~ {END_DATE} |
| 총 테스트 시간 | {TOTAL_DURATION} |
| 담당자 | Claude AI |

### 1.2 결과 요약

```
┌─────────────────────────────────────────────┐
│                  테스트 결과                 │
├─────────────────────────────────────────────┤
│                                             │
│  전체 통과율: {PASS_RATE}%                   │
│                                             │
│  ████████████████░░░░ {PASSED}/{TOTAL}      │
│                                             │
│  ✅ 통과: {PASSED}    ❌ 실패: {FAILED}      │
│  ⏸️ 블록: {BLOCKED}   ⏭️ 스킵: {SKIPPED}     │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.3 품질 판정

| 기준 | 목표 | 실제 | 판정 |
|------|------|------|------|
| P0 통과율 | 100% | {P0_RATE}% | {P0_STATUS} |
| P1 통과율 | 95% | {P1_RATE}% | {P1_STATUS} |
| P2 통과율 | 90% | {P2_RATE}% | {P2_STATUS} |
| Critical 버그 | 0개 | {CRITICAL_BUGS}개 | {CRIT_STATUS} |
| Major 버그 | 해결 | {MAJOR_OPEN}개 Open | {MAJOR_STATUS} |

### 1.4 릴리스 권장

```
┌─────────────────────────────────────────────┐
│                                             │
│  릴리스 권장: {RELEASE_RECOMMENDATION}       │
│                                             │
│  {RELEASE_CONDITION}                        │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 2. 상세 결과

### 2.1 테스트 통계

| 상태 | 수량 | 비율 | 그래프 |
|------|------|------|--------|
| ✅ 통과 | {PASSED} | {PASS_RATE}% | ████████░░ |
| ❌ 실패 | {FAILED} | {FAIL_RATE}% | ██░░░░░░░░ |
| ⏸️ 블록됨 | {BLOCKED} | {BLOCK_RATE}% | █░░░░░░░░░ |
| ⏭️ 스킵 | {SKIPPED} | {SKIP_RATE}% | ░░░░░░░░░░ |
| **총계** | **{TOTAL}** | **100%** | |

### 2.2 우선순위별 결과

| 우선순위 | 총계 | 통과 | 실패 | 통과율 | 목표 | 달성 |
|----------|------|------|------|--------|------|------|
| P0 (Critical) | {P0_TOTAL} | {P0_PASSED} | {P0_FAILED} | {P0_RATE}% | 100% | {P0_MET} |
| P1 (High) | {P1_TOTAL} | {P1_PASSED} | {P1_FAILED} | {P1_RATE}% | 95% | {P1_MET} |
| P2 (Medium) | {P2_TOTAL} | {P2_PASSED} | {P2_FAILED} | {P2_RATE}% | 90% | {P2_MET} |

### 2.3 기능별 결과

| 기능 | 총계 | 통과 | 실패 | 통과율 |
|------|------|------|------|--------|
| 인증 | {AUTH_TOTAL} | {AUTH_PASSED} | {AUTH_FAILED} | {AUTH_RATE}% |
| 상품 | {PROD_TOTAL} | {PROD_PASSED} | {PROD_FAILED} | {PROD_RATE}% |
| 검색 | {SEARCH_TOTAL} | {SEARCH_PASSED} | {SEARCH_FAILED} | {SEARCH_RATE}% |
| 결제 | {PAY_TOTAL} | {PAY_PASSED} | {PAY_FAILED} | {PAY_RATE}% |
| 사용자 | {USER_TOTAL} | {USER_PASSED} | {USER_FAILED} | {USER_RATE}% |

---

## 3. 통과한 테스트

| ID | 기능 | 시나리오 | 우선순위 | 실행 시간 | 비고 |
|----|------|----------|----------|----------|------|
| TC-001 | 로그인 | 정상 로그인 | P0 | 5.2s | |
| TC-002 | 로그인 | 비밀번호 오류 | P0 | 3.1s | |
| TC-003 | 회원가입 | 정상 가입 | P0 | 8.5s | |
| ... | ... | ... | ... | ... | ... |

---

## 4. 실패한 테스트

### TC-{FAIL_ID_1}: {FAIL_SCENARIO_1}

| 항목 | 내용 |
|------|------|
| **ID** | TC-{FAIL_ID_1} |
| **기능** | {FAIL_FEATURE_1} |
| **시나리오** | {FAIL_SCENARIO_1} |
| **우선순위** | {FAIL_PRIORITY_1} |
| **관련 버그** | BUG-{BUG_ID_1} |

**기대 결과:**
- {EXPECTED_1}

**실제 결과:**
- {ACTUAL_1}

**스크린샷:**
![TC-{FAIL_ID_1}](../screenshots/TC-{FAIL_ID_1}-result.png)

---

### TC-{FAIL_ID_2}: {FAIL_SCENARIO_2}

| 항목 | 내용 |
|------|------|
| **ID** | TC-{FAIL_ID_2} |
| **기능** | {FAIL_FEATURE_2} |
| **시나리오** | {FAIL_SCENARIO_2} |
| **우선순위** | {FAIL_PRIORITY_2} |
| **관련 버그** | BUG-{BUG_ID_2} |

**기대 결과:**
- {EXPECTED_2}

**실제 결과:**
- {ACTUAL_2}

**스크린샷:**
![TC-{FAIL_ID_2}](../screenshots/TC-{FAIL_ID_2}-result.png)

---

## 5. 블록된 테스트

| ID | 기능 | 시나리오 | 블록 사유 | 해결 방안 |
|----|------|----------|----------|----------|
| TC-{BLOCK_ID} | {BLOCK_FEATURE} | {BLOCK_SCENARIO} | {BLOCK_REASON} | {BLOCK_SOLUTION} |

---

## 6. 버그 보고서

### 6.1 버그 요약

| 심각도 | 발견 | Open | Fixed | Verified |
|--------|------|------|-------|----------|
| 🔴 Critical | {CRIT_FOUND} | {CRIT_OPEN} | {CRIT_FIXED} | {CRIT_VERIFIED} |
| 🟠 Major | {MAJOR_FOUND} | {MAJOR_OPEN} | {MAJOR_FIXED} | {MAJOR_VERIFIED} |
| 🟡 Minor | {MINOR_FOUND} | {MINOR_OPEN} | {MINOR_FIXED} | {MINOR_VERIFIED} |
| ⚪ Trivial | {TRIV_FOUND} | {TRIV_OPEN} | {TRIV_FIXED} | {TRIV_VERIFIED} |
| **Total** | **{BUG_TOTAL}** | **{BUG_OPEN}** | **{BUG_FIXED}** | **{BUG_VERIFIED}** |

### 6.2 버그 상세

---

#### BUG-001: {BUG_TITLE_1}

| 항목 | 내용 |
|------|------|
| **ID** | BUG-001 |
| **심각도** | {BUG_SEVERITY_1} |
| **상태** | {BUG_STATUS_1} |
| **발견 테스트** | TC-{BUG_TC_1} |
| **발견일** | {BUG_DATE_1} |
| **할당** | {BUG_ASSIGNEE_1} |

**재현 단계:**
1. {REPRO_STEP_1}
2. {REPRO_STEP_2}
3. {REPRO_STEP_3}

**기대 결과:**
- {BUG_EXPECTED_1}

**실제 결과:**
- {BUG_ACTUAL_1}

**스크린샷:**
![BUG-001](../screenshots/BUG-001.png)

**권장 수정:**
- {BUG_FIX_SUGGESTION_1}

---

## 7. 스크린샷 증거

### 7.1 주요 화면

| 화면 | 스크린샷 | 상태 |
|------|---------|------|
| 로그인 페이지 | ![login](../screenshots/login-page.png) | ✅ |
| 대시보드 | ![dashboard](../screenshots/dashboard.png) | ✅ |
| 상품 목록 | ![products](../screenshots/products.png) | ✅ |

### 7.2 버그 증거

| 버그 ID | 스크린샷 |
|---------|---------|
| BUG-001 | ![bug-001](../screenshots/BUG-001.png) |
| BUG-002 | ![bug-002](../screenshots/BUG-002.png) |

---

## 8. 권장 사항

### 8.1 필수 조치 (릴리스 전)

| 우선순위 | 항목 | 담당 | 기한 |
|----------|------|------|------|
| 1 | {MUST_ACTION_1} | {MUST_OWNER_1} | {MUST_DUE_1} |
| 2 | {MUST_ACTION_2} | {MUST_OWNER_2} | {MUST_DUE_2} |

### 8.2 권장 조치 (릴리스 후)

| 우선순위 | 항목 | 예상 효과 |
|----------|------|----------|
| 1 | {SHOULD_ACTION_1} | {SHOULD_EFFECT_1} |
| 2 | {SHOULD_ACTION_2} | {SHOULD_EFFECT_2} |

### 8.3 개선 제안

- {IMPROVEMENT_1}
- {IMPROVEMENT_2}

---

## 9. 다음 단계

### 9.1 즉시

- [ ] {NEXT_IMMEDIATE_1}
- [ ] {NEXT_IMMEDIATE_2}

### 9.2 다음 테스트 사이클

- [ ] 버그 수정 후 회귀 테스트
- [ ] 추가 기능 테스트
- [ ] 퍼포먼스 테스트 (선택)

---

## 10. 결론

### 10.1 전체 평가

```
┌─────────────────────────────────────────────┐
│              품질 점수: {QUALITY_SCORE}/100  │
├─────────────────────────────────────────────┤
│                                             │
│  기능 완성도:  {FUNC_SCORE}%  ██████████    │
│  안정성:       {STAB_SCORE}%  ████████░░    │
│  사용성:       {USAB_SCORE}%  ████████░░    │
│                                             │
└─────────────────────────────────────────────┘
```

### 10.2 최종 권장

{FINAL_RECOMMENDATION}

---

## 서명

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| QA 담당 | Claude AI | ✓ | {TODAY} |
| 검토자 | | | |
| 승인자 | | | |

---

## 첨부

1. 전체 테스트 케이스 목록: TEST_CASES.md
2. 상세 테스트 결과: TEST_RESULTS.md
3. 스크린샷 폴더: .claude-state/qa/screenshots/
4. 버그 상세: BUG_REPORT.md

---

**관련 명령어:**
- `/qa-run --failed` - 실패 테스트 재실행
- `/qa-status` - 현재 상태 확인
- `/qa-plan` - 계획서 확인
