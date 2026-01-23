---
description: Docusaurus 기반 문서 사이트 스켈레톤을 생성합니다.
allowed-tools: Read, Write, Edit, Glob, Bash, Task
argument-hint: [--template saas|library|cli] [--name <project-name>]
---

# /docs-init - 문서 사이트 초기화

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

Docusaurus 기반의 문서 사이트 스켈레톤을 생성합니다.
Diátaxis 프레임워크에 맞춘 표준 구조를 자동으로 구축합니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--template` | 템플릿 타입 (saas, library, cli) | saas |
| `--name` | 프로젝트 이름 | 현재 디렉토리명 |

## 실행 단계

### 1. 사전 조건 확인

```bash
# Node.js 버전 확인 (18+ 필요)
node --version

# npm 또는 yarn 확인
npm --version
```

### 2. 프로젝트 정보 수집

$ARGUMENTS에서 옵션 파싱:
- `--template`: 템플릿 타입
- `--name`: 프로젝트명 (없으면 현재 디렉토리명 사용)

### 3. Docusaurus 프로젝트 생성

```bash
# docs-site 디렉토리에 Docusaurus 설치
npx create-docusaurus@latest docs-site classic --typescript
```

### 4. 디렉토리 구조 생성

생성할 구조 (Diátaxis 프레임워크 기반):

```
docs-site/
├── docs/
│   ├── intro.md                      # 제품 소개
│   ├── getting-started/
│   │   ├── _category_.json
│   │   ├── overview.md               # 개요
│   │   ├── quickstart.md             # 빠른 시작 (5분)
│   │   └── installation.md           # 설치 가이드
│   ├── concepts/                     # 핵심 개념 (Explanation)
│   │   ├── _category_.json
│   │   ├── architecture.md
│   │   └── key-concepts.md
│   ├── tutorials/                    # 학습 (Tutorials)
│   │   ├── _category_.json
│   │   └── first-project.md
│   ├── guides/                       # How-to Guides
│   │   ├── _category_.json
│   │   └── configuration.md
│   ├── api/                          # Reference
│   │   ├── _category_.json
│   │   └── reference.md
│   └── troubleshooting/
│       ├── _category_.json
│       └── common-issues.md
├── blog/                             # Changelog/Release Notes
│   └── releases.md
├── src/
│   └── css/
│       └── custom.css
├── static/
│   └── img/
├── docusaurus.config.ts
├── sidebars.ts
└── package.json
```

### 5. 템플릿 파일 생성

각 문서 파일에 기본 템플릿 적용:

#### intro.md
```markdown
---
sidebar_position: 1
slug: /
---

# [프로젝트명]

> 한 줄 설명

## 주요 기능

- 기능 1
- 기능 2
- 기능 3

## 빠른 시작

[빠른 시작 가이드](/docs/getting-started/quickstart)로 이동하세요.
```

#### getting-started/_category_.json
```json
{
  "label": "시작하기",
  "position": 2,
  "collapsible": true,
  "collapsed": false
}
```

#### concepts/_category_.json
```json
{
  "label": "핵심 개념",
  "position": 3,
  "collapsible": true,
  "collapsed": false
}
```

#### tutorials/_category_.json
```json
{
  "label": "튜토리얼",
  "position": 4,
  "collapsible": true,
  "collapsed": true
}
```

#### guides/_category_.json
```json
{
  "label": "가이드",
  "position": 5,
  "collapsible": true,
  "collapsed": true
}
```

#### api/_category_.json
```json
{
  "label": "API Reference",
  "position": 6,
  "collapsible": true,
  "collapsed": true
}
```

### 6. docusaurus.config.ts 커스터마이징

```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: '[프로젝트명]',
  tagline: '프로젝트 한 줄 설명',
  favicon: 'img/favicon.ico',
  url: 'https://docs.your-domain.com',
  baseUrl: '/',
  organizationName: 'your-org',
  projectName: 'docs',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'ko',
    locales: ['ko', 'en'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: {
          showReadingTime: true,
          blogTitle: 'Release Notes',
          blogDescription: '업데이트 및 릴리즈 노트',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    navbar: {
      title: '[프로젝트명]',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {to: '/blog', label: 'Release Notes', position: 'left'},
        {
          href: 'https://github.com/your-org/your-repo',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: '시작하기', to: '/getting-started/overview'},
            {label: '튜토리얼', to: '/tutorials/first-project'},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'GitHub', href: 'https://github.com/your-org'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Your Company.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    algolia: {
      // Algolia DocSearch 설정 (선택사항)
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'YOUR_INDEX_NAME',
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

### 7. 완료 메시지 출력

```
============================================
 ✅ 문서 사이트 초기화 완료!
============================================

 생성된 디렉토리: docs-site/

 구조:
 └── docs/
     ├── intro.md
     ├── getting-started/
     ├── concepts/
     ├── tutorials/
     ├── guides/
     ├── api/
     └── troubleshooting/

 다음 단계:

 1. 문서 자동 생성:
    /docs generate

 2. 개별 문서 추가:
    /docs add quickstart
    /docs add tutorial "첫 프로젝트"

 3. 로컬 프리뷰:
    /docs preview

 4. 설정 커스터마이징:
    docs-site/docusaurus.config.ts 편집

============================================
```

## 템플릿 타입별 차이

### SaaS (기본)
- 사용자 온보딩 중심
- 기능별 가이드 강조
- 요금제/플랜 문서 포함

### Library
- API Reference 중심
- 코드 예제 강조
- 설치/의존성 관리 상세

### CLI
- 명령어 레퍼런스 중심
- 플래그/옵션 문서화
- 스크립팅 가이드 포함

## 참조

- Docusaurus: https://docusaurus.io/
- Diátaxis Framework: https://diataxis.fr/
