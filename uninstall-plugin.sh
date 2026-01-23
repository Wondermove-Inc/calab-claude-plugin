#!/bin/bash
# Calab Claude Plugin - 글로벌 제거 스크립트
# ~/.claude/에 설치된 플러그인 파일들을 제거
#
# ============================================================
# 제거 범위:
# ============================================================
#
# 📁 글로벌 (~/.claude/) - 이 스크립트가 제거
#    ├── CLAUDE.md, settings.json, statusline-command.sh
#    ├── hooks/, best-practices/, templates/
#    ├── agents/, integrations/, memory/, problem-solving/
#    ├── project-context/
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
# Step 1: 플러그인 캐시 및 설정 파일 완전 삭제 (버그 대응)
# ============================================================
echo "📋 1/4: 플러그인 캐시 및 설정 완전 삭제"
echo ""
echo "   ⚠️ 알려진 버그: /plugin uninstall, /plugin marketplace remove 명령어로는"
echo "      완전 제거가 안 됩니다. 수동 파일 삭제가 필요합니다."
echo ""
echo "   삭제할 파일:"
echo "   - ~/.claude/plugins/cache/"
echo "   - ~/.claude/plugins/installed_plugins.json"
echo "   - ~/.claude/plugins/known_marketplaces.json"
echo ""

read -p "   플러그인 캐시와 설정 파일을 삭제하시겠습니까? (Y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    # 캐시 삭제
    if [ -d "$CLAUDE_HOME/plugins/cache" ]; then
        rm -rf "$CLAUDE_HOME/plugins/cache"
        echo "   ✅ plugins/cache/ 삭제 완료"
    else
        echo "   ⏭️ plugins/cache/ 없음"
    fi

    # installed_plugins.json 삭제
    if [ -f "$CLAUDE_HOME/plugins/installed_plugins.json" ]; then
        rm -f "$CLAUDE_HOME/plugins/installed_plugins.json"
        echo "   ✅ installed_plugins.json 삭제 완료"
    else
        echo "   ⏭️ installed_plugins.json 없음"
    fi

    # known_marketplaces.json 삭제
    if [ -f "$CLAUDE_HOME/plugins/known_marketplaces.json" ]; then
        rm -f "$CLAUDE_HOME/plugins/known_marketplaces.json"
        echo "   ✅ known_marketplaces.json 삭제 완료"
    else
        echo "   ⏭️ known_marketplaces.json 없음"
    fi
else
    echo "   ⏭️ 캐시/설정 파일 유지"
fi

echo ""

# ============================================================
# Step 2: ~/.claude/에 설치된 파일 제거
# ============================================================
echo "🔧 2/4: 글로벌 파일 제거 중..."
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

# project-context/ 제거
if [ -d "$CLAUDE_HOME/project-context" ]; then
    rm -rf "$CLAUDE_HOME/project-context"
    echo "   ✅ project-context/ 제거 완료"
fi

# statusline-command.sh 제거
if [ -f "$CLAUDE_HOME/statusline-command.sh" ]; then
    rm "$CLAUDE_HOME/statusline-command.sh"
    echo "   ✅ statusline-command.sh 제거 완료"
fi

echo ""

# ============================================================
# Step 3: 마켓플레이스 디렉토리 제거
# ============================================================
echo "🔧 3/4: 마켓플레이스 제거 중..."

if [ -d "$MARKETPLACE_DIR" ]; then
    rm -rf "$MARKETPLACE_DIR"
    echo "   ✅ 마켓플레이스 제거 완료: $MARKETPLACE_DIR"
else
    echo "   ⏭️ 마켓플레이스 디렉토리 없음"
fi

echo ""

# ============================================================
# Step 4: 완료 확인
# ============================================================
echo "🔧 4/4: 제거 완료 확인 중..."

# 잔여 파일 확인
REMAINING_FILES=false

if [ -d "$CLAUDE_HOME/plugins/cache" ]; then
    echo "   ⚠️ plugins/cache/ 아직 존재 (수동 삭제 필요)"
    REMAINING_FILES=true
fi

if [ -f "$CLAUDE_HOME/plugins/installed_plugins.json" ]; then
    echo "   ⚠️ installed_plugins.json 아직 존재 (수동 삭제 필요)"
    REMAINING_FILES=true
fi

if [ -f "$CLAUDE_HOME/plugins/known_marketplaces.json" ]; then
    echo "   ⚠️ known_marketplaces.json 아직 존재 (수동 삭제 필요)"
    REMAINING_FILES=true
fi

if [ "$REMAINING_FILES" = false ]; then
    echo "   ✅ 모든 플러그인 관련 파일 제거 완료"
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
echo "   ~/.claude/plugins/cache/               # 플러그인 캐시"
echo "   ~/.claude/plugins/installed_plugins.json"
echo "   ~/.claude/plugins/known_marketplaces.json"
echo "   ~/.claude/CLAUDE.md"
echo "   ~/.claude/settings.json (선택)"
echo "   ~/.claude/statusline-command.sh"
echo "   ~/.claude/hooks/"
echo "   ~/.claude/best-practices/"
echo "   ~/.claude/templates/"
echo "   ~/.claude/agents/"
echo "   ~/.claude/integrations/"
echo "   ~/.claude/memory/ (선택)"
echo "   ~/.claude/problem-solving/"
echo "   ~/.claude/project-context/"
echo "   ~/.claude/calab-marketplace/"
echo ""
echo "⚠️ 프로젝트별 파일은 수동 제거 필요:"
echo "   rm -rf 프로젝트경로/.claude-state/   # 런타임 상태"
echo "   rm -rf 프로젝트경로/.claude/docs/    # 기능 문서"
echo ""
echo "🔄 재설치 방법:"
echo "   ./install-plugin.sh"
echo ""
