---
name: browser
description: |
  cmux 브라우저 자동화 - 열기, 탐색, DOM 조작, 스크린샷, 정보 추출.
  웹 페이지 열기, 브라우저 조작, 폼 입력, 버튼 클릭, 스크린샷, 페이지 스냅샷, DOM 탐색 등 브라우저 자동화가 필요할 때 사용합니다.
allowed-tools: Bash
---

# cmux:browser - 브라우저 자동화

Playwright 기반 내장 브라우저를 제어합니다.

## 명령어 카테고리

| 카테고리 | 주요 명령어 | 용도 |
|----------|------------|------|
| 열기/탐색 | `open`, `goto`, `back`, `forward`, `reload`, `url` | 페이지 이동 |
| 클릭/입력 | `click`, `fill`, `type`, `press`, `check`, `select` | DOM 조작 |
| 정보 추출 | `snapshot`, `screenshot`, `get`, `is`, `eval` | 페이지 분석 |
| 대기 | `wait --selector`, `wait --text`, `wait --url-contains` | 요소/상태 대기 |
| 요소 찾기 | `find role`, `find text`, `find label`, `find testid` | 접근성 기반 탐색 |
| 고급 | `frame`, `dialog`, `cookies`, `storage`, `network` | 프레임/쿠키/네트워크 |

명령어 상세 옵션은 플러그인 루트의 `references/browser-api.md`를 참조하세요.

## 워크플로우 패턴

1. `cmux browser snapshot`으로 현재 페이지 상태 파악
2. DOM 조작 시 `--snapshot-after` 플래그 추가 → 조작 결과를 즉시 확인
   - 예: `cmux browser click "#btn" --snapshot-after`
3. 복잡한 조작은 `cmux browser eval`로 JS 직접 실행

## 주의사항

- 브라우저 서피스가 없으면 먼저 `cmux browser open <url>` 실행 필요
- `--surface` 옵션으로 특정 브라우저 서피스 지정 가능
- `--snapshot-after`는 모든 조작 명령에 추가 가능 — 별도 snapshot 호출보다 효율적
- CSS 셀렉터 외에 접근성 기반 `find` 명령으로도 요소 탐색 가능
