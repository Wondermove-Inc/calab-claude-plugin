---
name: help
description: cli-tools 플러그인 사용법을 안내합니다. 도구별 상세 가이드를 제공합니다.
allowed-tools: Read
---

# /cli-tools:help - 플러그인 도움말

## 사용법
- `/cli-tools:help` - 지원 도구 목록 표시
- `/cli-tools:help {도구명}` - 해당 도구의 상세 가이드

## 실행 방식

### 사용자 요청 분석
사용자 입력에서 도구명을 파악합니다:
- "statusline" 키워드 → statusline 상세 가이드 출력
- 키워드 없음 → 도구 목록 출력

---

## 도구 목록 (기본 출력)

사용자가 `/cli-tools:help`만 입력한 경우 아래 내용을 **그대로** 출력합니다:

---
**[출력 시작]**

# cli-tools 플러그인 (v1.0.0)

Claude Code 터미널 환경을 개선하는 도구 모음입니다.

## 지원 도구

| 도구 | 설명 | 명령어 |
|------|------|--------|
| statusline | 터미널 상태바 설치/관리 | `/cli-tools:statusline` |

## 도구별 상세 가이드

`/cli-tools:help {도구명}`으로 상세 가이드를 확인하세요.

예시:
- `/cli-tools:help statusline`

**[출력 끝]**

---

---

## statusline 상세 가이드

사용자가 `/cli-tools:help statusline`을 입력한 경우 아래 내용을 **그대로** 출력합니다:

---
**[출력 시작]**

# statusline 도구

Claude Code 터미널에 상태 정보를 표시하는 statusline을 설치하고 관리합니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| /cli-tools:statusline | 플러그인 statusline 설치 |
| /cli-tools:statusline 롤백 | 이전 설정으로 복원 |
| /cli-tools:statusline rollback | 이전 설정으로 복원 |

## 표시 예시

[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
[Sonnet 4] ████░░░░░░ 40% | ➜ api-server git:(feature) ✗

## 표시 항목

| 항목 | 설명 |
|------|------|
| [Opus 4.5] | 현재 Claude 모델 |
| ██████░░░░ | 컨텍스트 사용량 게이지 |
| 60% | 컨텍스트 사용 백분율 |
| my-project | 현재 작업 디렉토리 |
| git:(main) | Git 브랜치명 |
| ✗ | 변경사항 있음 (빨간색) |

## 색상 규칙

- 녹색: 50% 미만 (안전)
- 노란색: 50-75% (주의)
- 빨간색: 75% 이상 (위험)

## 설치 동작

1. 기존 설정이 있으면 ~/.claude/backup/statusline_<timestamp>/에 백업
2. 플러그인의 statusline 스크립트 설치
3. settings.json 업데이트
4. Claude Code 재시작 필요

## 롤백 동작

1. 백업 목록에서 복원할 버전 선택
2. 현재 설정을 안전 백업 (pre_restore_<timestamp>)
3. 선택한 백업으로 복원

## 파일 위치

| 파일 | 설명 |
|------|------|
| ~/.claude/statusline-command.sh | Statusline 스크립트 |
| ~/.claude/settings.json | Claude Code 설정 |
| ~/.claude/backup/ | 백업 디렉토리 |

## 요구사항

- jq: JSON 파싱용
  - macOS: brew install jq
  - Ubuntu: sudo apt install jq
- bc: 계산용 (대부분 기본 설치됨)
  - Ubuntu: sudo apt install bc

**[출력 끝]**

---
