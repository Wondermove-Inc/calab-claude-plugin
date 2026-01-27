---
name: workflow:context-show
description: 현재 프로젝트 컨텍스트를 표시합니다. 기술 스택, 패턴, 아키텍처, 도메인 정보를 확인합니다.
allowed-tools: Read, Glob
user-invocable: true
---
# /context-show - 컨텍스트 표시

## 설명
현재 로드된 프로젝트 컨텍스트를 요약하여 표시합니다.

## 사용법
```
/context-show              # 전체 요약
/context-show tech         # 기술 스택만
/context-show patterns     # 코드 패턴만
/context-show architecture # 아키텍처만
/context-show domain       # 도메인 지식만
```

## 출력 형식

### 전체 요약 (`/context-show`)

```
📋 현재 프로젝트 컨텍스트

=== 프로젝트 정보 ===
이름: my-awesome-project
설명: E-commerce platform
분석일: 2024-01-15

=== 기술 스택 ===
Frontend: React 18, Next.js 14, TypeScript
Backend: Node.js, Express
Database: PostgreSQL, Prisma
Testing: Jest, Testing Library

=== 디렉토리 구조 ===
src/
├── app/           # Next.js App Router
├── components/    # React 컴포넌트
├── lib/           # 공통 유틸리티
├── services/      # API 서비스
└── types/         # TypeScript 타입

=== 주요 패턴 ===
- 컴포넌트: Function Components + Hooks
- 상태 관리: React Query + Zustand
- API: RESTful, NextResponse 형식
- 에러 처리: 중앙 집중식

=== 도메인 지식 ===
- 핵심 개념: User, Product, Order, Cart
- 비즈니스 규칙: 최소 주문 10,000원, 무료 배송 50,000원+

=== 현재 작업 ===
태스크: 사용자 프로필 페이지 구현
상태: In Progress
진행률: 60%
```

### 기술 스택만 (`/context-show tech`)

```
📦 기술 스택

| 카테고리 | 기술 | 버전 |
|---------|------|------|
| Language | TypeScript | 5.3.x |
| Frontend | React | 18.x |
| Framework | Next.js | 14.x |
| Styling | Tailwind CSS | 3.x |
| Database | PostgreSQL | 15.x |
| ORM | Prisma | 5.x |
| Testing | Jest | 29.x |
| Testing | Testing Library | 14.x |

참조: .claude/memory/PROJECT_SUMMARY.md
```

### 코드 패턴만 (`/context-show patterns`)

```
🎨 코드 패턴

=== 컴포넌트 패턴 ===
```typescript
'use client';
import { useState } from 'react';

export function ComponentName({ prop }: Props) {
  const [state, setState] = useState(init);
  return <div>...</div>;
}
```

=== API 패턴 ===
```typescript
export async function GET(request: NextRequest) {
  try {
    const data = await service.getData();
    return NextResponse.json({ data });
  } catch (error) {
    return NextResponse.json({ error: '...' }, { status: 500 });
  }
}
```

=== 테스트 패턴 ===
```typescript
describe('Component', () => {
  it('should ...', () => {
    render(<Component />);
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});
```

참조: .claude/memory/CODE_PATTERNS.md
```

## 컨텍스트가 없는 경우

```
⚠️ 프로젝트 컨텍스트가 없습니다.

다음 명령어로 온보딩을 시작하세요:
- /onboard       - 전체 분석
- /onboard-quick - 빠른 분석

온보딩 후 AI가 프로젝트 스타일에 맞게 개발할 수 있습니다.
```

## 참조
- `/onboard` - 초기 온보딩
- `/context-refresh` - 컨텍스트 갱신
