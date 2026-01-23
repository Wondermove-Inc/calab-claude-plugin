---
description: 로컬 프리뷰 서버를 실행합니다.
allowed-tools: Bash, Read
argument-hint: [--port <number>]
---

# /docs-preview - 로컬 프리뷰 서버

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

Docusaurus 개발 서버를 실행하여 문서 사이트를 로컬에서 미리 확인합니다.
Hot reload가 지원되어 문서 수정 시 즉시 반영됩니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--port` | 서버 포트 | 3000 |

## 실행 단계

### 1. 사전 조건 확인

```bash
# .claude/docs-site 디렉토리 존재 확인
ls .claude/docs-site/

# node_modules 존재 확인
ls .claude/docs-site/node_modules/
```

### 2. 의존성 확인

node_modules가 없으면 설치:

```bash
cd .claude/docs-site && npm install
```

### 3. 개발 서버 실행

```bash
cd .claude/docs-site && npm run start -- --port 3000
```

### 4. 완료 메시지

```
============================================
 🚀 프리뷰 서버 시작!
============================================

 URL: http://localhost:3000

 기능:
 - Hot reload 지원 (파일 저장 시 자동 새로고침)
 - 실시간 편집 확인

 종료: Ctrl+C

 팁:
 - 다른 포트 사용: /docs preview --port 3001
 - 빌드 테스트: /docs build

============================================
```

## 문제 해결

### 포트 사용 중

```
Error: Port 3000 is already in use.

해결: /docs preview --port 3001
```

### node_modules 없음

```
Error: Cannot find module 'docusaurus'

해결:
cd .claude/docs-site && npm install
```

### 빌드 에러

```
Error: [문서파일] contains invalid frontmatter

해결: 해당 파일의 frontmatter 문법 확인
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs build` | 정적 사이트 빌드 |
| `/docs status` | 문서 현황 확인 |
