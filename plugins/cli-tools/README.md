# cli-tools

Claude Code CLI 환경 설정 플러그인

## 개요

터미널에서 Claude Code 사용 경험을 개선하는 CLI 도구 모음입니다.

## 기능

### Statusline
터미널 프롬프트에 유용한 정보를 표시합니다:
- 현재 Claude 모델명 (Opus, Sonnet, Haiku)
- 컨텍스트 윈도우 사용량 (진행바 + 백분율)
- 현재 작업 디렉토리
- Git 브랜치 및 변경 상태

## 설치

```bash
# 마켓플레이스에서 설치
claude plugin install cli-tools
```

## 스킬

| 스킬 | 설명 |
|------|------|
| `/cli-tools:setup` | Statusline 자동 설치 |
| `/cli-tools:restore` | 백업에서 설정 복원 |

## 빠른 시작

```bash
# 자동 설치
bash ~/.claude/plugins/cli-tools/scripts/setup-statusline.sh
```

## Statusline 예시

```
[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
```

컨텍스트 사용량에 따른 색상:
- 50% 미만: 녹색
- 50-75%: 노란색
- 75% 이상: 빨간색

## 요구사항

- `jq`: JSON 파싱
- `bc`: 수학 계산 (macOS 기본 포함)

## 라이선스

MIT
