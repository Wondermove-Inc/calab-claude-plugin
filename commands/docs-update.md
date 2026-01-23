---
description: 기존 문서를 업데이트합니다.
allowed-tools: Read, Write, Edit, Glob, Task
argument-hint: [--all] [--section <name>] [--sync-code]
---

# /docs-update - 기존 문서 업데이트

> **🚨 중요**: 문서, 코드, 기타 확인 및 검증이 필요한 부분은 **전부 에이전트 사용 필수**.

## 목적

기존 문서를 최신 상태로 업데이트합니다.
코드 변경사항 반영, 버전 업데이트, 구조 개선 등을 수행합니다.

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--all` | 모든 문서 업데이트 | false |
| `--section` | 특정 섹션만 업데이트 | - |
| `--sync-code` | 코드 변경사항 동기화 | false |
| `--version` | 버전 정보 업데이트 | - |

## 사용법

```bash
/docs update                          # 변경 감지 후 업데이트
/docs update --all                    # 모든 문서 업데이트
/docs update --section getting-started # 특정 섹션만
/docs update --sync-code              # 코드 변경 반영
/docs update --version 2.0.0          # 버전 업데이트
```

## 실행 단계

### 1. 변경 사항 감지

에이전트를 사용하여 분석:

```
분석 항목:
1. 소스 코드 변경 (git diff)
2. API 변경사항
3. 설정 파일 변경
4. 문서와 코드 불일치
```

### 2. 업데이트 대상 식별

```
업데이트 유형:
- 코드 예제 동기화
- API 파라미터 변경
- 버전 번호 업데이트
- 링크 업데이트
- 스크린샷 갱신 필요
```

### 3. 업데이트 계획 제시

```
============================================
 📝 업데이트 계획
============================================

 감지된 변경사항: 8개

 자동 업데이트 가능: 5개
 ─────────────────────────────────────────
 1. api/reference.md
    - POST /users 파라미터 변경
    - 응답 형식 변경

 2. getting-started/quickstart.md
    - 설치 명령어 변경 (v1.x → v2.x)

 3. guides/configuration.md
    - 새 설정 옵션 추가 (3개)

 4. intro.md
    - 버전 번호 업데이트

 5. concepts/architecture.md
    - 컴포넌트 이름 변경

 수동 확인 필요: 3개
 ─────────────────────────────────────────
 1. tutorials/first-project.md
    - 전체 플로우 변경 가능성
    - → 수동 검토 권장

 2. troubleshooting/common-issues.md
    - 해결된 이슈 제거 필요
    - → 수동 검토 권장

 3. 스크린샷 5개
    - UI 변경으로 갱신 필요
    - → 새 스크린샷 촬영 필요

 계속 진행하시겠습니까? (Y/N)
============================================
```

### 4. 업데이트 실행

사용자 확인 후 업데이트 진행:

#### 코드 예제 동기화

```markdown
// 이전
npm install my-package@1.x

// 이후
npm install my-package@2.x
```

#### API 문서 업데이트

```markdown
// 이전
| name | string | 사용자 이름 |

// 이후
| name | string | 사용자 이름 (필수) |
| email | string | 이메일 (선택) |  // 새로 추가
```

#### 버전 정보 업데이트

```markdown
// 이전
현재 버전: 1.5.0

// 이후
현재 버전: 2.0.0
```

### 5. 결과 리포트

```
============================================
 ✅ 문서 업데이트 완료
============================================

 업데이트된 파일: 5개

 📄 api/reference.md
    ├── POST /users 파라미터 업데이트
    ├── 응답 예제 변경
    └── 에러 코드 추가

 📄 getting-started/quickstart.md
    ├── 설치 명령어 v2.x로 변경
    └── 새 초기화 단계 추가

 📄 guides/configuration.md
    ├── newOption1 설명 추가
    ├── newOption2 설명 추가
    └── newOption3 설명 추가

 📄 intro.md
    └── 버전: 1.5.0 → 2.0.0

 📄 concepts/architecture.md
    └── ComponentA → NewComponentA

 ─────────────────────────────────────────

 ⚠️ 수동 작업 필요

 1. tutorials/first-project.md
    전체 튜토리얼 검토 필요
    (API 플로우 변경됨)

 2. 스크린샷 갱신 필요:
    - /img/dashboard.png
    - /img/settings.png
    - /img/user-flow.png

 3. troubleshooting/common-issues.md
    해결된 이슈 제거:
    - "v1.x 호환성 문제" (v2.x에서 해결)

 ─────────────────────────────────────────

 다음 단계:
 1. 수동 작업 완료
 2. /docs validate 로 검증
 3. /docs preview 로 확인
 4. /docs deploy 로 배포

============================================
```

## --sync-code 상세

코드베이스와 문서를 동기화합니다:

### 감지 항목

| 항목 | 소스 | 대상 문서 |
|------|------|-----------|
| 패키지 버전 | package.json | 설치 가이드 |
| API 엔드포인트 | 라우터 파일 | API Reference |
| 설정 옵션 | config 스키마 | 설정 가이드 |
| CLI 명령어 | help 출력 | CLI Reference |
| 타입 정의 | TypeScript | API 타입 문서 |

### 예시: API 동기화

```typescript
// 소스: src/routes/users.ts
router.post('/users', {
  body: {
    name: z.string(),
    email: z.string().email(),  // 새로 추가됨
  }
});
```

자동으로 문서 업데이트:

```markdown
### POST /users

**요청 본문**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name | string | Yes | 사용자 이름 |
| email | string | Yes | 이메일 주소 |  <!-- 자동 추가 -->
```

## Changelog 자동 생성

`--version` 옵션 사용 시:

```bash
/docs update --version 2.0.0
```

`.claude/docs-site/blog/` 에 릴리즈 노트 자동 생성:

```markdown
---
slug: release-2.0.0
title: v2.0.0 Release
date: 2024-01-15
---

# v2.0.0 Release Notes

## 새로운 기능

- 기능 1 설명
- 기능 2 설명

## 변경 사항

- 변경 1 설명

## 버그 수정

- 수정 1 설명

## Breaking Changes

- API 변경 사항

---

전체 변경 로그: [GitHub Releases](https://github.com/org/repo/releases)
```

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/docs generate` | 새 문서 생성 |
| `/docs validate` | 업데이트 후 검증 |
| `/docs status` | 현황 확인 |
