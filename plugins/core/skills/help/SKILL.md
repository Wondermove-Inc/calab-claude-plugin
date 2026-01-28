---
name: core:help
description: Core 플러그인 사용 도움말
user-invocable: true
---

# Core Plugin Help

Core 플러그인의 기능과 사용법을 안내합니다.

## 플러그인 개요

Core 플러그인은 개발 전반에 범용적으로 사용할 수 있는 기본 가이드라인을 제공합니다.

## 스킬 목록

### Passive Skills (자동 참조)

코드 작성/리뷰 시 자동으로 참조됩니다.

| 스킬 | 설명 |
|------|------|
| `core:coding-principles` | SOLID, DRY, KISS 원칙 + 언어별 개발 규칙 (Go, TypeScript, React, Python) |

### Active Skills (명시적 호출)

슬래시 커맨드로 호출합니다.

| 커맨드 | 설명 |
|--------|------|
| `/core:code-review` | 코드 리뷰 수행 - 변경사항 분석 및 개선점 제안 |
| `/core:code-commit` | 커밋 메시지 생성 - 변경사항 분석 후 커밋 수행 |
| `/core:help` | 이 도움말 표시 |

## 사용 예시

### 코드 리뷰

```
# 기본 리뷰 (최근 변경사항)
/core:code-review

# 특정 범위 리뷰
/core:code-review HEAD~3..HEAD

# 특정 파일 리뷰
/core:code-review src/service.ts
```

### 커밋 생성

```
# 기본 커밋
/core:code-commit

# 힌트 제공
/core:code-commit "인증 기능 수정"
```

## 언어별 주요 원칙

### Go
- Accept interfaces, return structs
- 작은 인터페이스 (1-3 메서드)
- 명시적 에러 처리

### TypeScript
- strict 모드 필수
- any 금지 (unknown 사용)
- 타입 가드 활용

### React
- 단일 책임 컴포넌트
- Props drilling 지양
- Custom Hooks로 로직 추출

### Python
- 타입 힌트 100% 적용
- Pydantic 데이터 검증
- async/await 비동기 패턴

## 코드 품질 체크리스트

모든 코드 작성 시 적용:

- [ ] SOLID 원칙 준수
- [ ] DRY 원칙 (중복 최소화)
- [ ] KISS 원칙 (단순함 우선)
- [ ] 명확한 네이밍
- [ ] 적절한 에러 처리
- [ ] 보안 고려 (민감 정보 하드코딩 금지)
- [ ] 테스트 작성

## 커밋 메시지 형식

```
[type]: 간단 명료한 제목

- 주요 변경사항 1
- 주요 변경사항 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Type 종류
- `feature`: 새로운 기능 추가
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `docs`: 문서 수정
- `chore`: 기타 변경사항

## 관련 링크

- [Core Plugin README](../../../README.md)
- [Plugin Repository](https://github.com/Wondermove-Inc/calab-claude-plugin)
