#!/bin/bash
# Calab Claude Plugin - 글로벌 제거 스크립트
# ~/.claude/에 설치된 플러그인 파일들을 제거
#
# ============================================================
# 제거 범위 (v2.3.0):
# ============================================================
#
# 📁 글로벌 (~/.claude/) - 이 스크립트가 제거
#    ├── CLAUDE.md, settings.json, statusline-command.sh
#    ├── hooks/, best-practices/, templates/
#    ├── agents/ (7개), integrations/, memory/, problem-solving/
#    ├── project-context/, rules/, scripts/
#    └── calab-marketplace/
#        └── plugins/calab-plugin/
#            ├── commands/  # 42개 슬래시 명령어
#            └── skills/    # 16개 자동 활성화 스킬
#
# 📁 프로젝트별 (수동 제거 필요)
#    프로젝트/.claude-state/    # 런타임 상태 (worktree, checkpoint 등)
#    프로젝트/.claude/docs/     # 기능 문서 (active/, complete/)
#    프로젝트/.claude/skills/   # 심볼릭 링크 (에이전트용)
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
# Step 1: calab-plugin 캐시만 삭제 (다른 플러그인 보호)
# ============================================================
echo "📋 1/4: calab-plugin 캐시 삭제"
echo ""
echo "   ⚠️ 알려진 버그: /plugin uninstall, /plugin marketplace remove 명령어로는"
echo "      완전 제거가 안 됩니다. 수동 파일 삭제가 필요합니다."
echo ""
echo "   삭제할 파일:"
echo "   - ~/.claude/plugins/cache/calab-marketplace/ (calab-plugin만)"
echo ""

read -p "   calab-plugin 캐시를 삭제하시겠습니까? (Y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    # calab-marketplace 캐시만 삭제 (다른 플러그인 보호)
    if [ -d "$CLAUDE_HOME/plugins/cache/calab-marketplace" ]; then
        rm -rf "$CLAUDE_HOME/plugins/cache/calab-marketplace"
        echo "   ✅ plugins/cache/calab-marketplace/ 삭제 완료"
    else
        echo "   ⏭️ plugins/cache/calab-marketplace/ 없음"
    fi

    # installed_plugins.json에서 calab-plugin 항목만 제거
    if [ -f "$CLAUDE_HOME/plugins/installed_plugins.json" ]; then
        # jq가 있으면 calab-plugin만 제거, 없으면 경고
        if command -v jq &> /dev/null; then
            jq 'del(.["calab-marketplace"])' "$CLAUDE_HOME/plugins/installed_plugins.json" > "$CLAUDE_HOME/plugins/installed_plugins.json.tmp" && \
            mv "$CLAUDE_HOME/plugins/installed_plugins.json.tmp" "$CLAUDE_HOME/plugins/installed_plugins.json"
            echo "   ✅ installed_plugins.json에서 calab-plugin 제거 완료"
        else
            echo "   ⚠️ jq 없음 - installed_plugins.json 수동 편집 필요"
            echo "      (calab-marketplace 항목 삭제)"
        fi
    else
        echo "   ⏭️ installed_plugins.json 없음"
    fi

    # known_marketplaces.json에서 calab-marketplace 항목만 제거
    if [ -f "$CLAUDE_HOME/plugins/known_marketplaces.json" ]; then
        if command -v jq &> /dev/null; then
            jq 'del(.["calab-marketplace"])' "$CLAUDE_HOME/plugins/known_marketplaces.json" > "$CLAUDE_HOME/plugins/known_marketplaces.json.tmp" && \
            mv "$CLAUDE_HOME/plugins/known_marketplaces.json.tmp" "$CLAUDE_HOME/plugins/known_marketplaces.json"
            echo "   ✅ known_marketplaces.json에서 calab-marketplace 제거 완료"
        else
            echo "   ⚠️ jq 없음 - known_marketplaces.json 수동 편집 필요"
            echo "      (calab-marketplace 항목 삭제)"
        fi
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

# rules/ 제거
if [ -d "$CLAUDE_HOME/rules" ]; then
    rm -rf "$CLAUDE_HOME/rules"
    echo "   ✅ rules/ 제거 완료"
fi

# scripts/ 제거
if [ -d "$CLAUDE_HOME/scripts" ]; then
    rm -rf "$CLAUDE_HOME/scripts"
    echo "   ✅ scripts/ 제거 완료"
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

# 잔여 파일 확인 (calab-plugin 관련만)
REMAINING_FILES=false

if [ -d "$CLAUDE_HOME/plugins/cache/calab-marketplace" ]; then
    echo "   ⚠️ plugins/cache/calab-marketplace/ 아직 존재"
    REMAINING_FILES=true
fi

if [ -d "$MARKETPLACE_DIR" ]; then
    echo "   ⚠️ calab-marketplace/ 아직 존재"
    REMAINING_FILES=true
fi

if [ "$REMAINING_FILES" = false ]; then
    echo "   ✅ calab-plugin 관련 파일 제거 완료"
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
echo "   ~/.claude/plugins/cache/calab-marketplace/  # calab-plugin 캐시만"
echo "   ~/.claude/CLAUDE.md"
echo "   ~/.claude/settings.json (선택)"
echo "   ~/.claude/statusline-command.sh"
echo "   ~/.claude/hooks/"
echo "   ~/.claude/best-practices/"
echo "   ~/.claude/templates/"
echo "   ~/.claude/agents/                      # 7개 서브에이전트"
echo "   ~/.claude/integrations/"
echo "   ~/.claude/memory/ (선택)"
echo "   ~/.claude/problem-solving/"
echo "   ~/.claude/project-context/"
echo "   ~/.claude/rules/"
echo "   ~/.claude/scripts/"
echo "   ~/.claude/calab-marketplace/"
echo "       └── plugins/calab-plugin/"
echo "           ├── commands/                  # 42개 슬래시 명령어"
echo "           └── skills/                    # 16개 자동 활성화 스킬"
echo ""
echo "⚠️ 프로젝트별 파일은 수동 제거 필요:"
echo "   rm -rf 프로젝트경로/.claude-state/   # 런타임 상태 (worktree, checkpoint)"
echo "   rm -rf 프로젝트경로/.claude/docs/    # 기능 문서 (active/, complete/)"
echo "   rm -rf 프로젝트경로/.claude/skills/  # 심볼릭 링크 (에이전트용)"
echo ""
echo "🔄 재설치 방법:"
echo "   ./install-plugin.sh"
echo ""
