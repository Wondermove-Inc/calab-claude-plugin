---
name: review
description: |
  Codex 구현물 검증. 원본 명세서와 대조하여 AC 충족 여부를 검증합니다.
argument-hint: "[--spec|--diff|--files] [path]"
allowed-tools: [Read, Glob, Grep, Bash, Task, AskUserQuestion]
skills: [project-rules, code-quality, clarification-protocol, skill-completion-rules]
agents:
  primary: validator
  orchestration:
    verify: [Explore, calab-plugin:validator]
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/post_skill_artifact_check.py\""
          once: true
---

# /review - Codex 구현물 검증 (Opus Review)

> **Codex가 구현한 결과물을 원본 명세서와 대조하여 검증**

## 사용법

```bash
/review                                    # 최근 handoff 기준으로 자동 검증
/review --spec plans/handoff-xxx.md        # 특정 명세서 기준 검증
/review --diff                             # git diff 기반 검증
/review --files src/auth/ src/utils/       # 특정 파일/폴더 검증
```

## 트리거 키워드

`review`, `리뷰`, `검증`, `확인해줘`, `코덱스 결과`, `구현 확인`, `검토`

## 목적

Codex 구현물이 원본 handoff 명세서의 요구사항을 **100% 충족**하는지 검증.
Opus의 강점(아키텍처 이해, 엣지케이스 발견, 설계 일관성)을 활용.

---

## 실행 절차

### Step 1: 원본 명세서 로드

```
1. plans/ 폴더에서 최신 handoff-*.md 탐색
2. 또는 --spec 옵션으로 지정된 파일 로드
3. AC, Constraints, Scope 섹션 추출
```

### Step 2: 구현물 수집

```
1. git diff (명세서 생성 이후 변경분)
2. 또는 --files로 지정된 파일들
3. 변경된 파일 목록 및 내용 수집
```

### Step 3: AC 대조 검증

각 Acceptance Criteria를 하나씩 검증:

```
[AC 검증] handoff-20260225-db-refactor.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ AC1: WHEN --mode ssh THEN 접속 성공
   → lib/connection.sh:12 connect_ssh() 구현 확인

✅ AC2: WHEN --dry-run THEN 실제 실행 없이 검증
   → install.sh:45 DRY_RUN 플래그 처리 확인

❌ AC3: WHEN 잘못된 모드 입력 THEN usage 출력
   → 누락: 입력 검증 로직 없음
   → 수정 필요: lib/validation.sh에 mode 검증 추가

⚠️ AC4: 기존 테스트 통과
   → 미확인: 테스트 실행 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
결과: ❌ 1개 미충족, ⚠️ 1개 미확인
```

### Step 4: Constraints 준수 검증

```
[Constraints 검증]
━━━━━━━━━━━━━━━━━━

✅ "기존 CLI 인터페이스 하위 호환"
   → 기존 인자 모두 동작 확인

✅ "배포 명령어 실행 금지"
   → 배포 관련 코드 없음

❌ "activity.log 기록"
   → 로깅 호출 누락 (3곳)
```

### Step 5: 추가 품질 검사

명세서에 없더라도 Opus가 발견하는 문제:
- 하드코딩된 값
- 에러 처리 누락
- 일관성 없는 네이밍
- 기존 코드 패턴과 불일치

### Step 6: 결과 보고

```
============================================
 REVIEW 완료: handoff-20260225-db-refactor.md
============================================

 📊 AC 검증:
 ✅ 충족: 5/7
 ❌ 미충족: 1/7 (AC3: 입력 검증 누락)
 ⚠️ 미확인: 1/7 (AC4: 테스트 미실행)

 🔒 Constraints:
 ✅ 준수: 2/3
 ❌ 위반: 1/3 (로깅 누락)

 🔍 추가 발견:
 • line 23: 하드코딩된 포트 번호 (4317)
 • line 45: 에러 시 exit 코드 미설정

 📋 다음 조치:
 1. AC3 구현 (입력 검증)
 2. 로깅 추가 (3곳)
 3. 하드코딩 제거

 🔄 재검증: /review --spec plans/handoff-20260225-db-refactor.md
============================================
```

---

## 검증 심각도 분류

| 심각도 | 기준 | 조치 |
|--------|------|------|
| **BLOCK** | AC 미충족, Constraint 위반 | Codex에 수정 재위임 or 직접 수정 |
| **WARN** | 미확인 항목, 품질 이슈 | 수동 확인 후 판단 |
| **INFO** | 개선 제안, 스타일 이슈 | 선택적 반영 |

---

## 수정 후 재검증 플로우

```
/review (1차)
    ↓ 미충족 발견
수정 (Opus 직접 or Codex 재위임)
    ↓
/review (2차) - 미충족 항목만 재검증
    ↓ 전체 통과
✅ 완료
```

Codex에 수정을 재위임할 경우:
```bash
# review 결과를 Codex에 전달
codex "다음 수정사항을 반영해줘:
1. lib/validation.sh에 mode 검증 추가 (ssh|bastion|local만 허용)
2. install.sh 3곳에 log_info 호출 추가
3. lib/connection.sh:23 포트 번호를 변수로 추출"
```

---

## 다음 단계

| 상황 | 명령어 |
|------|--------|
| 전체 AC 통과 | 커밋 & 다음 작업 |
| 미충족 있음 - 직접 수정 | 수정 후 `/review` 재실행 |
| 미충족 있음 - Codex 재위임 | 수정 사항 정리 후 Codex 실행 |
| 새 태스크 위임 | `/handoff [다음 태스크]` |
