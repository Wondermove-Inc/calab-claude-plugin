---
name: best-practices
description: 기술별 베스트 프랙티스를 적용합니다. 코드 작성, 구현, 개발, React, Node.js, TypeScript, 데이터베이스, API 요청 시 자동 활성화. 검증된 패턴과 방법론을 사용합니다.
allowed-tools: Read, Glob
---

# Best Practices Skill

## 목적

각 기술에 대해 검증된 베스트 프랙티스와 디자인 패턴을 적용하여
일관되고 유지보수 가능한 코드를 생성합니다.

## 활성화 조건

- 코드 작성/구현 요청 시
- React, Node.js, TypeScript 등 기술 언급 시
- "패턴", "베스트 프랙티스", "모범 사례" 언급 시
- 아키텍처, 설계 결정 시

## 베스트 프랙티스 적용 프로토콜

### 1. 기술 스택 확인

```
.claude/memory/TECH_STACK.md 읽기
→ 사용 중인 기술 식별
→ 해당 베스트 프랙티스 파일 로드
```

### 2. 베스트 프랙티스 로드

```
.claude/best-practices/{technology}.md 읽기
→ 패턴, 규칙, 예시 코드 확인
→ 현재 작업에 적용할 항목 선택
```

### 3. 코드 생성 시 적용

- **파일 구조**: 해당 기술의 권장 구조 사용
- **네이밍**: 기술별 컨벤션 적용
- **패턴**: 검증된 디자인 패턴 사용
- **에러 처리**: 표준 에러 처리 패턴 적용
- **테스트**: 기술별 테스트 패턴 적용

## 지원 기술

| 기술 | 파일 | 주요 내용 |
|------|------|----------|
| React | `react.md` | 컴포넌트 패턴, 훅, 상태 관리 |
| Next.js | `nextjs.md` | App Router, 서버 컴포넌트, 데이터 페칭 |
| Node.js | `nodejs.md` | 레이어 아키텍처, 에러 처리, 로깅 |
| TypeScript | `typescript.md` | 타입 패턴, 제네릭, 유틸리티 타입 |
| Database | `database.md` | 스키마 설계, 쿼리 최적화, 마이그레이션 |
| API Design | `api-design.md` | REST/GraphQL, 버저닝, 에러 응답 |
| Testing | `testing.md` | 단위/통합/E2E 테스트 패턴 |

## 출력 형식

### 코드 생성 전 확인

```
============================================
[BEST PRACTICES] 적용 패턴 확인
============================================

 기술 스택: React + TypeScript + Node.js

 적용할 패턴:
• React: Function Components + Custom Hooks
• TypeScript: Strict Mode + Utility Types
• Node.js: Layered Architecture (Controller → Service → Repository)

 참조 문서:
• .claude/best-practices/react.md
• .claude/best-practices/typescript.md
• .claude/best-practices/nodejs.md

============================================
위 패턴을 적용하여 코드를 생성합니다.
```

## 코드 생성 체크리스트

코드 생성 시 다음을 확인:

- [ ] 해당 기술의 권장 디렉토리 구조 사용
- [ ] 파일당 300줄 이하
- [ ] 모든 함수에 주석 (JSDoc/Docstring)
- [ ] 해당 기술의 네이밍 컨벤션 적용
- [ ] 에러 처리 패턴 적용
- [ ] 타입 정의 완전성

## 참조 파일

- `.claude/memory/TECH_STACK.md` - 기술 스택 설정
- `.claude/best-practices/` - 기술별 베스트 프랙티스
- `.claude/memory/CODE_STYLE.md` - 코드 스타일 규칙
