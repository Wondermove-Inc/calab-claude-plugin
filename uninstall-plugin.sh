#!/bin/bash
# Calab Claude Plugin - 글로벌 제거 스크립트
# ~/.claude/에 설치된 플러그인 파일들을 제거
#
# ============================================================
# 제거 범위:
# ============================================================
#
# 📁 글로벌 (~/.claude/) - 이 스크립트가 제거
#    ├── CLAUDE.md, settings.json
#    ├── hooks/, best-practices/, templates/
#    ├── agents/, integrations/, memory/, problem-solving/
#    └── calab-marketplace/
#
# 📁 프로젝트별 (수동 제거 필요)
#    프로젝트/.claude-state/    # 런타임 상태
#    프로젝트/.claude/docs/     # 기능 문서
#
# ============================================================

set -e

PLUGIN_NAME="calab-plugin"
CLAUDE_HOME="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_HOME/calab-marketplace"

echo "=================================================="
echo " Calab Claude Plugin - 글로벌 제거"
echo "=================================================="
echo ""
echo "📋 제거 범위:"
echo "   • 글로벌 (~/.claude/): 설치된 모든 파일"
echo "   • 프로젝트별 (.claude-state/, .claude/docs/): 수동 제거 필요"
echo ""

# ============================================================
# Step 1: Claude 플러그인 시스템에서 제거 안내
# ============================================================
echo "📋 1/3: 플러그인 시스템에서 제거하기"
echo ""
echo "   Claude Code 내부에서 다음 명령어를 먼저 실행하세요:"
echo ""
echo "   /plugin uninstall $PLUGIN_NAME"
echo "   /plugin marketplace remove calab-marketplace"
echo ""
echo "   (터미널이 아닌 Claude Code 내부에서 슬래시 명령어로 입력)"
echo ""
read -p "   위 명령어를 실행했나요? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "   ⚠️ 먼저 위 명령어를 실행한 후 다시 시도하세요."
    exit 1
fi

echo ""

# ============================================================
# Step 2: ~/.claude/에 설치된 파일 제거
# ============================================================
echo "🔧 2/3: 글로벌 파일 제거 중..."
echo ""

# CLAUDE.md 제거
if [ -f "$CLAUDE_HOME/CLAUDE.md" ]; then
    rm "$CLAUDE_HOME/CLAUDE.md"
    echo "   ✅ CLAUDE.md 제거 완료"
fi

# settings.json 제거 (주의: 다른 설정이 있을 수 있음)
if [ -f "$CLAUDE_HOME/settings.json" ]; then
    echo "   ⚠️ settings.json 발견"
    read -p "   settings.json을 제거하시겠습니까? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$CLAUDE_HOME/settings.json"
        echo "   ✅ settings.json 제거 완료"
    else
        echo "   ⏭️ settings.json 유지"
    fi
fi

# hooks/ 제거
if [ -d "$CLAUDE_HOME/hooks" ]; then
    rm -rf "$CLAUDE_HOME/hooks"
    echo "   ✅ hooks/ 제거 완료"
fi

# best-practices/ 제거
if [ -d "$CLAUDE_HOME/best-practices" ]; then
    rm -rf "$CLAUDE_HOME/best-practices"
    echo "   ✅ best-practices/ 제거 완료"
fi

# templates/ 제거
if [ -d "$CLAUDE_HOME/templates" ]; then
    rm -rf "$CLAUDE_HOME/templates"
    echo "   ✅ templates/ 제거 완료"
fi

# agents/ 제거
if [ -d "$CLAUDE_HOME/agents" ]; then
    rm -rf "$CLAUDE_HOME/agents"
    echo "   ✅ agents/ 제거 완료"
fi

# integrations/ 제거
if [ -d "$CLAUDE_HOME/integrations" ]; then
    rm -rf "$CLAUDE_HOME/integrations"
    echo "   ✅ integrations/ 제거 완료"
fi

# memory/ 제거 (주의: 사용자 데이터가 있을 수 있음)
if [ -d "$CLAUDE_HOME/memory" ]; then
    echo "   ⚠️ memory/ 폴더 발견 (사용자 작업 기록 포함 가능)"
    read -p "   memory/ 폴더를 제거하시겠습니까? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$CLAUDE_HOME/memory"
        echo "   ✅ memory/ 제거 완료"
    else
        echo "   ⏭️ memory/ 유지"
    fi
fi

# problem-solving/ 제거
if [ -d "$CLAUDE_HOME/problem-solving" ]; then
    rm -rf "$CLAUDE_HOME/problem-solving"
    echo "   ✅ problem-solving/ 제거 완료"
fi

echo ""

# ============================================================
# Step 3: 마켓플레이스 디렉토리 제거
# ============================================================
echo "🔧 3/3: 마켓플레이스 제거 중..."

if [ -d "$MARKETPLACE_DIR" ]; then
    rm -rf "$MARKETPLACE_DIR"
    echo "   ✅ 마켓플레이스 제거 완료: $MARKETPLACE_DIR"
else
    echo "   ⏭️ 마켓플레이스 디렉토리 없음"
fi

echo ""

# ============================================================
# 완료
# ============================================================
echo "=================================================="
echo " ✅ 제거 완료!"
echo "=================================================="
echo ""
echo "📁 제거된 항목:"
echo "   ~/.claude/CLAUDE.md"
echo "   ~/.claude/settings.json (선택)"
echo "   ~/.claude/hooks/"
echo "   ~/.claude/best-practices/"
echo "   ~/.claude/templates/"
echo "   ~/.claude/agents/"
echo "   ~/.claude/integrations/"
echo "   ~/.claude/memory/ (선택)"
echo "   ~/.claude/problem-solving/"
echo "   ~/.claude/calab-marketplace/"
echo ""
echo "⚠️ 프로젝트별 파일은 수동 제거 필요:"
echo "   rm -rf 프로젝트경로/.claude-state/   # 런타임 상태"
echo "   rm -rf 프로젝트경로/.claude/docs/    # 기능 문서"
echo ""
echo "🔄 재설치 방법:"
echo "   ./install-plugin.sh"
echo ""
