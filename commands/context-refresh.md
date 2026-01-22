---
description: 프로젝트 컨텍스트 문서를 갱신합니다. 코드 변경 후 컨텍스트 동기화가 필요할 때 사용합니다.
allowed-tools: Read, Write, Glob, Grep
argument-hint: [patterns | architecture | domain]
---

# /context-refresh - 컨텍스트 갱신

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**. 에이전트를 적극 활용하고, 파일이 크면 분할해서 읽어라.

## 설명
프로젝트에 변경사항이 생겼을 때 컨텍스트 문서를 업데이트합니다.

## 사용법
```
/context-refresh              # 전체 갱신
/context-refresh patterns     # 코드 패턴만 갱신
/context-refresh architecture # 아키텍처만 갱신
```

## 갱신 대상

| 옵션 | 갱신 대상 |
|------|----------|
| (없음) | 모든 컨텍스트 문서 |
| `patterns` | CODE_PATTERNS.md |
| `architecture` | ARCHITECTURE.md |
| `conventions` | CONVENTIONS.md |
| `summary` | PROJECT_SUMMARY.md |

## 실행 순서

### 1. 변경 감지

```
현재 프로젝트 상태와 기존 컨텍스트 비교:
- 새 파일/폴더 추가 여부
- 기술 스택 변경 여부
- 패턴 변화 여부
```

### 2. 증분 업데이트

```
전체 재분석이 아닌 변경된 부분만 업데이트:
- 새로 추가된 패턴 추가
- 삭제된 패턴 제거
- 변경된 구조 반영
```

### 3. 문서 업데이트

```
각 문서의 '최종 분석일' 갱신
변경 내용 반영
```

## 출력 예시

### 전체 갱신

```
🔄 컨텍스트 갱신 중...

변경 감지:
- 새 파일: src/components/Modal/Modal.tsx
- 새 패턴: useModal 훅 발견
- 구조 변경: services/ 폴더 추가

업데이트:
✓ PROJECT_SUMMARY.md - 디렉토리 구조 업데이트
✓ CODE_PATTERNS.md - Modal 패턴 추가
✓ ARCHITECTURE.md - services 레이어 추가

✅ 컨텍스트 갱신 완료!
```

### 특정 대상 갱신

```
/context-refresh patterns

🔄 코드 패턴 갱신 중...

분석된 새 패턴:
- useModal 훅
- ConfirmDialog 컴포넌트
- API 에러 핸들링 개선

✓ CODE_PATTERNS.md 업데이트 완료
```

## 언제 사용하나요?

- 새로운 기능을 여러 개 추가한 후
- 프로젝트 구조가 변경된 후
- 새로운 라이브러리를 도입한 후
- 다른 개발자가 코드를 많이 변경한 후

## 참조
- `/onboard` - 초기 온보딩
- `/context-show` - 현재 컨텍스트 확인
