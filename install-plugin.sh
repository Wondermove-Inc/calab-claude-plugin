#!/bin/bash
# Calab Claude Plugin - 글로벌 설치 스크립트
# ~/.claude/에 플러그인 파일들을 설치하여 모든 프로젝트에서 사용 가능하게 함
#
# ============================================================
# 글로벌 vs 프로젝트 구조:
# ============================================================
#
# 📁 글로벌 (~/.claude/) - 이 스크립트가 설치
#    ├── CLAUDE.md              # 마스터 지침
#    ├── settings.json          # 훅 설정
#    ├── hooks/                 # 자동 실행 훅
#    ├── best-practices/        # 언어별 베스트 프랙티스
#    ├── templates/             # 문서 템플릿
#    ├── agents/                # 서브에이전트
#    ├── integrations/          # 외부 연동 설정
#    ├── memory/                # 메모리 템플릿
#    ├── problem-solving/       # 문제 해결 방법론
#    └── calab-marketplace/     # 명령어/스킬 마켓플레이스
#        └── plugins/
#            └── calab-plugin/  # 전체 복사 (심볼릭 링크 아님)
#
# 📁 프로젝트별 (자동 생성, 글로벌에 설치 안 함)
#    프로젝트/
#    ├── .claude-state/         # 런타임 상태 (worktree, checkpoint 등)
#    └── .claude/docs/          # 기능별 문서
#        ├── active/            # 진행 중 기능
#        └── complete/          # 완료된 기능
#
# ============================================================

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_NAME="calab-plugin"
CLAUDE_HOME="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_HOME/calab-marketplace"

echo "=================================================="
echo " Calab Claude Plugin - 글로벌 설치"
echo "=================================================="
echo ""
echo "📦 플러그인 소스: $PLUGIN_DIR"
echo "🏠 글로벌 설치 위치: $CLAUDE_HOME"
echo ""
echo "📋 설치 범위:"
echo "   • 글로벌 (~/.claude/): CLAUDE.md, hooks, best-practices 등"
echo "   • 프로젝트별: .claude-state/, .claude/docs/ (사용 시 자동 생성)"
echo ""

# .claude-plugin/plugin.json 확인
if [ ! -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
    echo "❌ plugin.json이 없습니다: $PLUGIN_DIR/.claude-plugin/plugin.json"
    exit 1
fi

echo "✅ plugin.json 확인 완료"
echo ""

# ============================================================
# Step 0: 이전 설치 캐시 정리 (업데이트/재설치 시)
# ============================================================
PLUGIN_CACHE="$CLAUDE_HOME/plugins/cache/calab-marketplace"
if [ -d "$PLUGIN_CACHE" ]; then
    echo "🔄 이전 플러그인 캐시 발견: $PLUGIN_CACHE"
    read -p "   캐시를 삭제하시겠습니까? (재설치/업데이트 시 권장) (Y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        rm -rf "$PLUGIN_CACHE"
        echo "   ✅ 이전 캐시 삭제 완료"
    else
        echo "   ⏭️ 캐시 유지 (플러그인 재설치 시 문제가 발생할 수 있습니다)"
    fi
    echo ""
fi

# ============================================================
# Step 1: ~/.claude/ 디렉토리 생성 및 파일 복사
# ============================================================
echo "🔧 1/3: 글로벌 파일 설치 중..."

mkdir -p "$CLAUDE_HOME"

# CLAUDE.md 복사
if [ -f "$PLUGIN_DIR/CLAUDE.md" ]; then
    cp "$PLUGIN_DIR/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
    echo "   ✅ CLAUDE.md 복사 완료"
fi

# hooks/ 복사
if [ -d "$PLUGIN_DIR/.claude/hooks" ]; then
    mkdir -p "$CLAUDE_HOME/hooks"
    cp -r "$PLUGIN_DIR/.claude/hooks/"* "$CLAUDE_HOME/hooks/"
    echo "   ✅ hooks/ 복사 완료"
fi

# best-practices/ 복사
if [ -d "$PLUGIN_DIR/.claude/best-practices" ]; then
    mkdir -p "$CLAUDE_HOME/best-practices"
    cp -r "$PLUGIN_DIR/.claude/best-practices/"* "$CLAUDE_HOME/best-practices/"
    echo "   ✅ best-practices/ 복사 완료"
fi

# templates/ 복사
if [ -d "$PLUGIN_DIR/.claude/templates" ]; then
    mkdir -p "$CLAUDE_HOME/templates"
    cp -r "$PLUGIN_DIR/.claude/templates/"* "$CLAUDE_HOME/templates/"
    echo "   ✅ templates/ 복사 완료"
fi

# agents/ 복사
if [ -d "$PLUGIN_DIR/.claude/agents" ]; then
    mkdir -p "$CLAUDE_HOME/agents"
    cp -r "$PLUGIN_DIR/.claude/agents/"* "$CLAUDE_HOME/agents/"
    echo "   ✅ agents/ 복사 완료"
fi

# integrations/ 복사
if [ -d "$PLUGIN_DIR/.claude/integrations" ]; then
    mkdir -p "$CLAUDE_HOME/integrations"
    cp -r "$PLUGIN_DIR/.claude/integrations/"* "$CLAUDE_HOME/integrations/"
    echo "   ✅ integrations/ 복사 완료"
fi

# memory/ 복사 (기본 템플릿)
if [ -d "$PLUGIN_DIR/.claude/memory" ]; then
    mkdir -p "$CLAUDE_HOME/memory"
    cp -r "$PLUGIN_DIR/.claude/memory/"* "$CLAUDE_HOME/memory/"
    echo "   ✅ memory/ 복사 완료"
fi

# problem-solving/ 복사
if [ -d "$PLUGIN_DIR/.claude/problem-solving" ]; then
    mkdir -p "$CLAUDE_HOME/problem-solving"
    cp -r "$PLUGIN_DIR/.claude/problem-solving/"* "$CLAUDE_HOME/problem-solving/"
    echo "   ✅ problem-solving/ 복사 완료"
fi

echo ""

# ============================================================
# Step 2: settings.json 설치 (훅 경로를 ~/.claude/hooks/로 수정)
# ============================================================
echo "🔧 2/3: settings.json 설치 중..."

# settings.json에서 ${CLAUDE_PROJECT_DIR}/.claude/hooks/ → ~/.claude/hooks/로 변경
if [ -f "$PLUGIN_DIR/.claude/settings.json" ]; then
    # 경로 치환하여 복사
    sed 's|\${CLAUDE_PROJECT_DIR}/\.claude/hooks/|'"$CLAUDE_HOME"'/hooks/|g' \
        "$PLUGIN_DIR/.claude/settings.json" > "$CLAUDE_HOME/settings.json"
    echo "   ✅ settings.json 설치 완료 (훅 경로 수정됨)"
else
    echo "   ⚠️ settings.json이 없습니다"
fi

echo ""

# ============================================================
# Step 3: 마켓플레이스 생성 (commands/, skills/ 로드용)
# ============================================================
echo "🔧 3/3: 로컬 마켓플레이스 생성 중..."

mkdir -p "$MARKETPLACE_DIR/.claude-plugin"
mkdir -p "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME"

# 플러그인 전체 복사 (심볼릭 링크 대신 실제 복사)
# commands/, skills/, .claude-plugin/ 복사
if [ -d "$PLUGIN_DIR/commands" ]; then
    cp -r "$PLUGIN_DIR/commands" "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/"
    echo "   ✅ commands/ 복사 완료"
fi

if [ -d "$PLUGIN_DIR/skills" ]; then
    cp -r "$PLUGIN_DIR/skills" "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/"
    echo "   ✅ skills/ 복사 완료"
fi

if [ -d "$PLUGIN_DIR/.claude-plugin" ]; then
    cp -r "$PLUGIN_DIR/.claude-plugin" "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME/"
    echo "   ✅ .claude-plugin/ 복사 완료"
fi

# marketplace.json 생성 (.claude-plugin/ 내부에 위치해야 함)
cat > "$MARKETPLACE_DIR/.claude-plugin/marketplace.json" <<MARKETPLACE
{
  "\$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "calab-marketplace",
  "description": "Calab Plugin Marketplace - 개발 워크플로우 자동화",
  "owner": {
    "name": "Wondermove CALAB",
    "email": "captain@wondermove.net"
  },
  "plugins": [
    {
      "name": "$PLUGIN_NAME",
      "description": "개발 워크플로우 자동화 플러그인 - Plan → Design → Tasks → Build",
      "version": "2.1.0",
      "author": {
        "name": "Wondermove CALAB",
        "email": "captain@wondermove.net"
      },
      "source": "./plugins/$PLUGIN_NAME",
      "category": "development",
      "strict": false
    }
  ]
}
MARKETPLACE

echo "   ✅ 마켓플레이스 생성 완료: $MARKETPLACE_DIR"
echo ""

# ============================================================
# 완료
# ============================================================
echo "=================================================="
echo " ✅ 글로벌 설치 완료!"
echo "=================================================="
echo ""
echo "📁 글로벌 설치 파일 (~/.claude/):"
echo "   ├── CLAUDE.md              # 마스터 지침"
echo "   ├── settings.json          # 훅 설정"
echo "   ├── hooks/                 # 자동 실행 훅"
echo "   ├── best-practices/        # 언어별 베스트 프랙티스"
echo "   ├── templates/             # 문서 템플릿"
echo "   ├── agents/                # 서브에이전트"
echo "   ├── integrations/          # 외부 연동"
echo "   ├── memory/                # 메모리 템플릿"
echo "   ├── problem-solving/       # 문제 해결 방법론"
echo "   └── calab-marketplace/     # 마켓플레이스"
echo "       └── plugins/calab-plugin/"
echo "           ├── commands/      # 35개 슬래시 명령어"
echo "           ├── skills/        # 11개 자동 활성화 스킬"
echo "           └── .claude-plugin/"
echo ""
echo "📁 프로젝트별 (사용 시 자동 생성):"
echo "   프로젝트/"
echo "   ├── .claude-state/         # 런타임 상태"
echo "   └── .claude/docs/          # 기능별 문서"
echo "       ├── active/            # 진행 중 기능"
echo "       └── complete/          # 완료된 기능"
echo ""
echo "📋 Claude Code 내부에서 다음 명령어를 실행하세요 (최초 1회만):"
echo ""
echo "   # 마켓플레이스 추가 (Claude Code 내부에서)"
echo "   /plugin marketplace add $MARKETPLACE_DIR"
echo ""
echo "   # 플러그인 설치 (Claude Code 내부에서)"
echo "   /plugin install $PLUGIN_NAME@calab-marketplace --scope user"
echo ""
echo "   ※ 터미널이 아닌 Claude Code를 실행한 후 내부에서 입력하세요"
echo ""
echo "🔄 재설치/업데이트 시:"
echo "   # Claude Code 내부에서 먼저 제거"
echo "   /plugin uninstall $PLUGIN_NAME"
echo "   /plugin marketplace remove calab-marketplace"
echo ""
echo "   # 터미널에서 다시 설치"
echo "   ./install-plugin.sh  # 캐시 삭제 권장"
echo ""
echo "   # Claude Code 내부에서 다시 등록"
echo "   /plugin marketplace add $MARKETPLACE_DIR"
echo "   /plugin install $PLUGIN_NAME@calab-marketplace --scope user"
echo ""
echo "✨ 설치 후 사용법:"
echo "   /calab-plugin:onboard        - 프로젝트 분석"
echo "   /calab-plugin:dev-plan       - 기획"
echo "   /calab-plugin:research       - 리서치"
echo ""
