---
description: 문서 사이트를 배포합니다 (GitHub Pages, Vercel, Netlify).
allowed-tools: Bash, Read, Write, Edit, Task
argument-hint: [--target github-pages|vercel|netlify] [--prod]
---

# /docs-deploy - 문서 사이트 배포

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

빌드된 문서 사이트를 다양한 플랫폼에 배포합니다.
GitHub Pages, Vercel, Netlify를 지원합니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--target` | 배포 대상 (github-pages, vercel, netlify) | github-pages |
| `--prod` | 프로덕션 배포 | false |

## 사용법

```bash
/docs deploy                          # GitHub Pages 배포 (기본)
/docs deploy --target vercel          # Vercel 배포
/docs deploy --target netlify --prod  # Netlify 프로덕션 배포
```

## 실행 단계

### 1. 사전 조건 확인

에이전트를 사용하여 확인:

```
확인 항목:
- docs-site/build 디렉토리 존재 (없으면 /docs build 먼저 실행)
- Git 저장소 설정 (GitHub Pages의 경우)
- 배포 도구 설치 여부
```

빌드 디렉토리가 없으면:
```
⚠️ 빌드 디렉토리가 없습니다.
먼저 /docs build를 실행하세요.
```

### 2. 배포 대상별 실행

#### GitHub Pages

```bash
# Docusaurus GitHub Pages 배포
cd docs-site

# docusaurus.config.ts 설정 확인
# organizationName, projectName, deploymentBranch 필요

# 배포 실행
GIT_USER=<GITHUB_USERNAME> npm run deploy
```

**필요한 설정** (docusaurus.config.ts):
```typescript
const config: Config = {
  organizationName: 'your-org',
  projectName: 'your-repo',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,
};
```

**GitHub Actions 자동 배포 설정**:
```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Docs

on:
  push:
    branches: [main]
    paths:
      - 'docs-site/**'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: docs-site/package-lock.json

      - name: Install dependencies
        run: cd docs-site && npm ci

      - name: Build
        run: cd docs-site && npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs-site/build

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

#### Vercel

```bash
# Vercel CLI 설치 확인
which vercel || npm install -g vercel

# 배포
cd docs-site

# 프리뷰 배포
vercel

# 프로덕션 배포 (--prod 옵션)
vercel --prod
```

**vercel.json 설정** (선택사항):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "docusaurus-2"
}
```

#### Netlify

```bash
# Netlify CLI 설치 확인
which netlify || npm install -g netlify-cli

# 배포
cd docs-site

# 프리뷰 배포
netlify deploy --dir=build

# 프로덕션 배포 (--prod 옵션)
netlify deploy --dir=build --prod
```

**netlify.toml 설정** (선택사항):
```toml
[build]
  base = "docs-site"
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 3. 배포 결과 확인

에이전트를 사용하여 배포 URL 접속 테스트:
- 메인 페이지 로드 확인
- 주요 페이지 링크 확인
- 404 페이지 처리 확인

### 4. 결과 리포트

**성공 시:**

```
============================================
 ✅ 배포 완료!
============================================

 대상: GitHub Pages
 URL: https://your-org.github.io/your-repo/

 배포 정보:
 - 브랜치: gh-pages
 - 커밋: abc1234
 - 시간: 2024-01-01 12:00:00

 확인 사항:
 ✅ 메인 페이지 로드
 ✅ 검색 기능
 ✅ 다크 모드

 다음 단계:
 - 커스텀 도메인 설정 (선택)
 - Algolia 검색 연동 (선택)
 - Google Analytics 설정 (선택)

============================================
```

**실패 시:**

```
============================================
 ❌ 배포 실패
============================================

 에러:
 [에러 메시지]

 원인:
 - 가능한 원인 1
 - 가능한 원인 2

 해결 방법:
 1. [해결 단계]
 2. [해결 단계]

 재시도: /docs deploy --target [target]

============================================
```

## 커스텀 도메인 설정

### GitHub Pages

1. Repository Settings > Pages > Custom domain
2. DNS 설정:
   ```
   # CNAME 레코드
   docs.yourdomain.com -> your-org.github.io

   # 또는 A 레코드 (apex domain)
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```
3. `docs-site/static/CNAME` 파일 생성:
   ```
   docs.yourdomain.com
   ```

### Vercel

```bash
vercel domains add docs.yourdomain.com
```

### Netlify

```bash
netlify domains:add docs.yourdomain.com
```

## 문제 해결

### GitHub Pages 404 에러

```bash
# baseUrl 설정 확인
# docusaurus.config.ts
baseUrl: '/your-repo/',  # 저장소 이름과 일치해야 함
```

### Vercel 빌드 실패

```bash
# Node.js 버전 지정
# package.json
{
  "engines": {
    "node": ">=18"
  }
}
```

### Netlify 리다이렉트 문제

```toml
# netlify.toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs build` | 배포 전 빌드 |
| `/docs preview` | 배포 전 로컬 확인 |
| `/docs validate` | 배포 전 검증 |
