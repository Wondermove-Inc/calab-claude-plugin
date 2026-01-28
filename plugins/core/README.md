# Core Plugin

개발 전반에 범용적으로 사용할 수 있는 기본 가이드라인 플러그인입니다.

> **Note**: `architecture` 플러그인이 클린 아키텍처/DDD 특화라면, `core`는 언어별 범용 개발 원칙과 코드 품질 가이드를 제공합니다.

## 스킬 구성

| 스킬 | 호출 방법 | 설명 |
|------|-----------|------|
| coding-principles | (자동 참조) | SOLID, DRY, KISS + 언어별 규칙 (Go, TS, React, Python) |
| code-review | `/core:code-review` | 코드 리뷰 체크리스트 기반 리뷰 |
| code-commit | `/core:code-commit` | 커밋 메시지 생성 및 커밋 워크플로우 |
| help | `/core:help` | 상세 사용법 안내 |

## 설치

```bash
# settings.json에 추가
{
  "plugins": ["path/to/plugins/core"]
}
```

## 빠른 시작

```bash
# 코드 리뷰
/core:code-review

# 커밋 생성
/core:code-commit

# 상세 도움말
/core:help
```
