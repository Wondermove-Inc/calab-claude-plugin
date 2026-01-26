---
name: cli-tools:restore
description: Statusline 설정을 백업에서 복원합니다. 이전 설정으로 롤백할 때 사용합니다.
allowed-tools: Bash, Read, AskUserQuestion
---

# /cli-tools:restore - Statusline 설정 복원

## 설명
백업된 statusline 설정을 복원합니다. `/cli-tools:setup` 실행 전 상태로 롤백할 수 있습니다.

## 실행 방식

### 1단계: 백업 목록 확인
```bash
# 백업 디렉토리 목록 조회
ls -la ~/.claude/backup/ 2>/dev/null | grep statusline || echo "백업 없음"
```

### 2단계: 백업 내용 확인
각 백업 디렉토리의 내용을 확인합니다:
```bash
# 최신 백업 확인
LATEST_BACKUP=$(ls -td ~/.claude/backup/statusline_* 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    echo "최신 백업: $LATEST_BACKUP"
    ls -la "$LATEST_BACKUP"
fi
```

### 3단계: 복원할 백업 선택
백업이 여러 개인 경우 사용자에게 선택을 요청합니다.

### 4단계: 복원 실행
사용자 확인 후 복원을 진행합니다.

**복원 전 현재 설정 백업** (안전을 위해):
```bash
# 현재 설정을 임시 백업
RESTORE_BACKUP=~/.claude/backup/pre_restore_$(date +%Y%m%d_%H%M%S)
mkdir -p "$RESTORE_BACKUP"
cp ~/.claude/settings.json "$RESTORE_BACKUP/" 2>/dev/null || true
cp ~/.claude/statusline-command.sh "$RESTORE_BACKUP/" 2>/dev/null || true
echo "복원 전 현재 설정 백업: $RESTORE_BACKUP"
```

**복원 실행**:
```bash
# settings.json 복원
cp "$BACKUP_DIR/settings.json" ~/.claude/settings.json

# statusline-command.sh 복원 (있는 경우)
if [ -f "$BACKUP_DIR/statusline-command.sh" ]; then
    cp "$BACKUP_DIR/statusline-command.sh" ~/.claude/statusline-command.sh
fi
```

### 5단계: 완료 안내
복원 완료 후 Claude Code 재시작을 안내합니다.

## 백업 구조
```
~/.claude/backup/
├── statusline_20260126_143052/
│   ├── settings.json
│   └── statusline-command.sh
└── statusline_20260125_091530/
    └── settings.json
```

## 주의사항
- 복원 시 현재 설정이 덮어씌워집니다
- 복원 전 현재 설정의 백업 여부를 확인합니다
