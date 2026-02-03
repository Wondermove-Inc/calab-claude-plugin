---
name: toolkit:code-review
description: 최근 변경사항을 리뷰하고 개선점을 제안합니다
user-invocable: true
---

# Code Review Command

최근 변경된 코드를 분석하여 코드 품질, 설계 패턴, 잠재적 이슈를 검토하고 개선점을 제안합니다.

## 작업 순서

1. **변경사항 파악**
   - `git diff HEAD~1` 또는 사용자가 지정한 범위의 변경사항 확인
   - 수정/추가/삭제된 파일 목록 확인

2. **코딩 가이드 참조**
   변경된 파일의 확장자를 확인하고 `guides/language-guide.md`의 해당 언어 섹션 참조:

   | 파일 확장자 | 참조 섹션 |
   |-------------|-----------|
   | `.go`, `go.mod` | Go 섹션 |
   | `.ts`, `.tsx` | TypeScript 섹션 |
   | `.tsx`, `.jsx` (React 컴포넌트) | React 섹션 |
   | `.py`, `pyproject.toml` | Python 섹션 |

   - 각 언어의 설계 원칙, 코드 냄새 감지 기준, 네이밍 규칙을 리뷰에 적용
   - 여러 언어가 섞인 경우 각각의 섹션을 모두 참조

3. **코드 리뷰 수행**
   다음 항목들을 체크:

   ### 3.1 코드 품질
   - [ ] SOLID 원칙 준수 여부
   - [ ] DRY 원칙 (코드 중복 최소화)
   - [ ] 함수/메서드 길이 적절성
   - [ ] 네이밍 명확성 (변수, 함수, 타입명)
   - [ ] 복잡도 (중첩 깊이, Cyclomatic Complexity)

   ### 3.2 에러 처리
   - [ ] 모든 에러 케이스 처리 여부
   - [ ] 에러 메시지의 명확성
   - [ ] 에러 로깅 적절성
   - [ ] 예외/에러 전파 적절성

   ### 3.3 주석 및 문서화
   - [ ] 복잡한 로직에 주석 작성
   - [ ] 함수/메서드 문서화 (언어별 표준 형식)
   - [ ] TODO/FIXME 주석 적절성
   - [ ] 한글 주석 사용 (프로젝트 규칙)

   ### 3.4 성능 및 최적화
   - [ ] 불필요한 메모리 할당
   - [ ] N+1 쿼리 문제
   - [ ] 비효율적인 반복문
   - [ ] 적절한 데이터 구조 사용

   ### 3.5 보안
   - [ ] 민감 정보 하드코딩 여부
   - [ ] 입력 검증
   - [ ] SQL Injection 등 취약점
   - [ ] 적절한 권한 검사

4. **개선점 제안**
   - 발견된 이슈를 우선순위별로 분류:
     - Critical: 반드시 수정 필요
     - Warning: 개선 권장
     - Suggestion: 선택적 개선

   - 각 이슈에 대해:
     - 문제점 설명
     - 개선 방법 제시
     - 코드 예시 제공 (Before/After)

5. **리뷰 요약 리포트 생성**
   ```
   ## Code Review Summary

   ### Overall Assessment
   - Quality Score: X/10
   - Issues Found: X

   ### Good Points
   - 잘 작성된 부분들 나열

   ### Critical Issues
   - 반드시 수정이 필요한 이슈들

   ### Warnings
   - 개선이 권장되는 부분들

   ### Suggestions
   - 선택적 개선 제안들

   ### Recommendations
   - 전반적인 개선 방향 제시
   ```

## 사용 예시

### 기본 사용
```
/toolkit:code-review
```
→ 최근 커밋과 현재 변경사항 리뷰

### 특정 커밋 범위 지정
```
/toolkit:code-review HEAD~3..HEAD
```
→ 최근 3개 커밋 리뷰

### 특정 파일만 리뷰
```
/toolkit:code-review src/service.ts src/utils.ts
```
→ 지정된 파일만 리뷰

## 주의사항

- 코드 스타일은 프로젝트의 기존 컨벤션을 따름
- 언어별 Best Practice 적용
- 과도한 추상화보다는 단순명료함 우선
- 성능 최적화는 실제 병목이 확인된 경우에만 제안
