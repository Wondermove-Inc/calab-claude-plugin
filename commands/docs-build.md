---
description: 정적 사이트를 빌드합니다.
allowed-tools: Bash, Read, Glob, Task
argument-hint: [--output <dir>]
---

# /docs-build - 정적 사이트 빌드

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

Docusaurus 문서 사이트를 정적 HTML로 빌드합니다.
빌드된 파일은 GitHub Pages, Vercel, Netlify 등에 배포할 수 있습니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--output` | 출력 디렉토리 | docs-site/build |

## 실행 단계

### 1. 빌드 전 검사

에이전트를 사용하여 검사:

```
검사 항목:
- 깨진 링크
- 누락된 이미지
- frontmatter 오류
- 마크다운 문법 오류
```

### 2. 의존성 확인

```bash
cd docs-site && npm install
```

### 3. 빌드 실행

```bash
cd docs-site && npm run build
```

### 4. 빌드 결과 검증

에이전트를 사용하여 검증:

```
검증 항목:
- build 디렉토리 생성 확인
- index.html 존재 확인
- 404.html 존재 확인
- 주요 페이지 존재 확인
```

### 5. 결과 리포트

**성공 시:**

```
============================================
 ✅ 빌드 완료!
============================================

 출력 디렉토리: docs-site/build/

 빌드 통계:
 - 총 HTML 파일: 15개
 - 총 용량: 2.3MB
 - 빌드 시간: 12초

 파일 구조:
 build/
 ├── index.html
 ├── 404.html
 ├── getting-started/
 ├── concepts/
 ├── tutorials/
 ├── guides/
 ├── api/
 └── assets/

 배포 옵션:

 1. GitHub Pages:
    - Settings > Pages > Source: Deploy from branch
    - Branch: gh-pages, /root

 2. Vercel:
    vercel deploy docs-site/build

 3. Netlify:
    netlify deploy --dir=docs-site/build

 4. 정적 서버 테스트:
    npx serve docs-site/build

============================================
```

**실패 시:**

```
============================================
 ❌ 빌드 실패
============================================

 에러:

 [ERROR] Docusaurus build failed

 1. 깨진 링크 발견:
    - /docs/concepts/missing.md (in tutorials/first-project.md)

 2. 이미지 누락:
    - /img/architecture.png (in concepts/architecture.md)

 해결 방법:

 1. 깨진 링크 수정:
    - 존재하는 문서로 링크 변경
    - 또는 해당 문서 생성

 2. 이미지 추가:
    - docs-site/static/img/ 에 이미지 추가

 3. 일시적 무시 (권장하지 않음):
    docusaurus.config.ts에서:
    onBrokenLinks: 'warn',
    onBrokenMarkdownLinks: 'warn',

 수정 후: /docs build 재실행

============================================
```

## 배포 가이드

### GitHub Pages

1. **Repository 설정**
   ```bash
   # gh-pages 브랜치에 배포
   cd docs-site
   npm run deploy
   ```

2. **GitHub Actions (자동 배포)**
   ```yaml
   # .github/workflows/docs.yml
   name: Deploy Docs

   on:
     push:
       branches: [main]
       paths:
         - 'docs-site/**'

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-node@v3
           with:
             node-version: 18
         - run: cd docs-site && npm ci
         - run: cd docs-site && npm run build
         - uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./docs-site/build
   ```

### Vercel

```bash
# Vercel CLI 사용
npm i -g vercel
cd docs-site
vercel --prod
```

### Netlify

```bash
# Netlify CLI 사용
npm i -g netlify-cli
cd docs-site
netlify deploy --prod --dir=build
```

## 빌드 최적화

### 1. 이미지 최적화

```bash
# 이미지 압축
npm install -g imagemin-cli
imagemin docs-site/static/img/* --out-dir=docs-site/static/img/
```

### 2. 번들 분석

```bash
cd docs-site
npm run build -- --bundle-analyzer
```

### 3. 캐시 활용

```javascript
// docusaurus.config.ts
module.exports = {
  // ...
  future: {
    experimental_faster: true,
  },
};
```

## 문제 해결

### 메모리 부족

```bash
# Node.js 메모리 증가
NODE_OPTIONS=--max_old_space_size=4096 npm run build
```

### TypeScript 에러

```bash
# 타입 체크 스킵
npm run build -- --skip-type-check
```

### 깨진 링크 무시 (임시)

```typescript
// docusaurus.config.ts
const config: Config = {
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  // ...
};
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs preview` | 로컬 프리뷰 |
| `/docs status` | 빌드 전 상태 확인 |
