# /context --refresh - 컨텍스트 갱신

> **코드 변경 반영하여 컨텍스트 증분 업데이트**

## 실행 절차

### Phase 1: 변경 감지

**Step 1**: 현재 상태 스캔

```bash
# 파일 구조 스캔
ls -la src/

# package.json 변경 확인
diff 기존 vs 현재

# 새 파일/폴더 감지
find src/ -newer .claude/project-context/PROJECT_SUMMARY.md
```

**Step 2**: 변경 분류

| 변경 유형 | 감지 방법 | 영향 문서 |
|----------|----------|----------|
| 새 파일/폴더 | find -newer | PROJECT_SUMMARY |
| 삭제된 파일 | 존재 확인 | PROJECT_SUMMARY |
| 기술 스택 변경 | package.json diff | PROJECT_SUMMARY |
| 패턴 변화 | 코드 분석 | CODE_PATTERNS |
| 구조 변경 | 디렉토리 diff | ARCHITECTURE |
| 컨벤션 변화 | 설정 파일 diff | CONVENTIONS |

### Phase 2: 증분 업데이트

**Step 1**: 영향받는 문서 식별

```
필터 없음: 모든 변경 적용
필터 있음: 해당 영역만 업데이트
- patterns → CODE_PATTERNS.md
- architecture → ARCHITECTURE.md
- conventions → CONVENTIONS.md
- summary → PROJECT_SUMMARY.md
```

**Step 2**: 문서별 업데이트

**PROJECT_SUMMARY.md:**
```markdown
## 변경 사항
- 디렉토리 구조 업데이트
- 기술 스택 버전 업데이트
- 새 의존성 추가

## 분석 날짜
마지막 분석: {현재 날짜}
```

**CODE_PATTERNS.md:**
```markdown
## 새로 발견된 패턴
- {패턴 설명}
- {패턴 설명}

## 제거된 패턴
- {더 이상 사용되지 않는 패턴}
```

**ARCHITECTURE.md:**
```markdown
## 구조 변경
- 새 레이어/모듈 추가
- 의존성 변경
```

**CONVENTIONS.md:**
```markdown
## 컨벤션 업데이트
- 네이밍 규칙 변경
- 새 린트 규칙
```

### Phase 3: 검증 및 저장

**Step 1**: 변경 사항 요약

```
============================================
 CONTEXT REFRESH 완료
============================================

 📝 업데이트된 문서:
 • PROJECT_SUMMARY.md ✓
 • CODE_PATTERNS.md ✓

 📊 변경 요약:
 • 새 파일: 5개
 • 삭제 파일: 2개
 • 패턴 추가: 3개
 • 패턴 제거: 1개

 ⏰ 갱신 시간: {timestamp}

============================================
```

**Step 2**: 문서 저장

각 영향받은 문서의 "마지막 분석" 날짜 업데이트

## 필터 옵션

| 필터 | 대상 | 설명 |
|------|------|------|
| `patterns` | CODE_PATTERNS.md | 코드 패턴만 갱신 |
| `architecture` | ARCHITECTURE.md | 아키텍처만 갱신 |
| `conventions` | CONVENTIONS.md | 컨벤션만 갱신 |
| `summary` | PROJECT_SUMMARY.md | 프로젝트 요약만 갱신 |

## 주의사항

- **증분 업데이트**: 전체 재분석이 아님
- 허용 도구: `Read`, `Write`, `Glob`, `Grep`
- 에이전트로 문서/코드 검증 필수

## 갱신 권장 시점

- 여러 새 기능 추가 후
- 프로젝트 구조 변경 후
- 새 라이브러리 도입 후
- 다른 개발자의 대규모 변경 후
