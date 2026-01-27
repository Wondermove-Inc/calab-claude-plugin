# cli-tools 플러그인

> Claude Code CLI 환경 설정 - Statusline 자동 설치

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/cli-tools:statusline` | Statusline 설정 및 설치 |
| `/cli-tools:help` | 플러그인 도움말 |

## 빠른 시작

```bash
# Statusline 설정
/cli-tools:statusline
```

## Statusline 기능

터미널 프롬프트에 유용한 정보를 표시합니다:
- 현재 Claude 모델명 (Opus, Sonnet, Haiku)
- 컨텍스트 윈도우 사용량 (진행바 + 백분율)
- 현재 작업 디렉토리
- Git 브랜치 및 변경 상태

### 표시 예시

```
[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
```

### 색상 안내

컨텍스트 사용량에 따른 색상:
- 50% 미만: 녹색
- 50-75%: 노란색
- 75% 이상: 빨간색

## 요구사항

- `jq`: JSON 파싱
- `bc`: 수학 계산 (macOS 기본 포함)

## 플러그인 구조

```
plugins/cli-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── statusline/SKILL.md
│   └── help/SKILL.md
└── README.md
```
