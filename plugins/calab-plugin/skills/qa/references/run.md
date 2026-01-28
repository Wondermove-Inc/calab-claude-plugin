# /qa --run - 테스트 실행

> **MCP Puppeteer로 E2E 테스트 순차 실행**

## 전제 조건
- [ ] 개발 서버 실행 중
- [ ] MCP Puppeteer 연결됨
- [ ] 테스트 케이스 준비됨

## 실행 절차

### Step 1: 환경 확인
```javascript
// 개발 서버 확인
mcp__puppeteer__puppeteer_navigate({ url: "http://localhost:3000" })
```

### Step 2: 테스트 케이스 로드
```
.claude-state/qa/test-cases.json 로드
```

### Step 3: 순차 실행
```javascript
// 각 테스트 케이스마다:
1. mcp__puppeteer__puppeteer_navigate({ url: targetUrl })
2. mcp__puppeteer__puppeteer_screenshot({ name: "step-1" })
3. mcp__puppeteer__puppeteer_fill({ selector, value })
4. mcp__puppeteer__puppeteer_click({ selector })
5. mcp__puppeteer__puppeteer_evaluate({ script: "검증 스크립트" })
```

### Step 4: 결과 기록
- 상태: passed / failed / blocked
- 스크린샷 저장
- 실패 시 버그 자동 생성

### Step 5: 100% 완료까지 반복

### 출력 파일
- `.claude-state/qa/test-results.json`
- `.claude-state/qa/bugs.json`
- `.claude-state/qa/screenshots/`
