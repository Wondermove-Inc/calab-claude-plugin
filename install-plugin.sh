#!/bin/bash
# Calab Claude Plugin - 공식 플러그인 시스템 기반 설치
# 사용자 설정을 침범하지 않고 마켓플레이스를 통해 설치

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_NAME="calab-plugin"
MARKETPLACE_DIR="$HOME/.claude/calab-marketplace"

echo "=================================================="
echo " Calab Claude Plugin - 플러그인 설치"
echo "=================================================="
echo ""
echo "📦 플러그인 위치: $PLUGIN_DIR"
echo "🏪 마켓플레이스: $MARKETPLACE_DIR"
echo ""

# .claude-plugin/plugin.json 확인
if [ ! -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
    echo "❌ plugin.json이 없습니다: $PLUGIN_DIR/.claude-plugin/plugin.json"
    exit 1
fi

echo "✅ plugin.json 확인 완료"
echo ""

# 마켓플레이스 디렉토리 생성
echo "🔧 1/3: 로컬 마켓플레이스 생성 중..."
mkdir -p "$MARKETPLACE_DIR/.claude-plugin"
mkdir -p "$MARKETPLACE_DIR/plugins"

# 플러그인 심볼릭 링크 생성
ln -sf "$PLUGIN_DIR" "$MARKETPLACE_DIR/plugins/$PLUGIN_NAME"

# marketplace.json 생성 (공식 스키마 준수)
cat > "$MARKETPLACE_DIR/.claude-plugin/marketplace.json" <<MARKETPLACE
{
  "\$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "calab-marketplace",
  "description": "Calab Plugin Marketplace - 개발 워크플로우 자동화",
  "owner": {
    "name": "Wonder Move Lab",
    "email": "support@wondermovelab.com"
  },
  "plugins": [
    {
      "name": "$PLUGIN_NAME",
      "description": "개발 워크플로우 자동화 플러그인 - Plan → Design → Tasks → Build",
      "version": "1.0.0",
      "author": {
        "name": "Wonder Move Lab",
        "email": "support@wondermovelab.com"
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

# Claude CLI로 마켓플레이스 추가 및 플러그인 설치
echo "🔧 2/3: Claude CLI를 통한 설치..."
echo ""
echo "다음 명령어를 실행하세요:"
echo ""
echo "  # 마켓플레이스 추가"
echo "  claude plugin marketplace add $MARKETPLACE_DIR"
echo ""
echo "  # 플러그인 설치 (사용자 스코프 - 모든 프로젝트에서 사용)"
echo "  claude plugin install $PLUGIN_NAME@calab-marketplace --scope user"
echo ""
echo "  # 또는 프로젝트 스코프 (현재 프로젝트만)"
echo "  claude plugin install $PLUGIN_NAME@calab-marketplace --scope project"
echo ""
echo ""

echo "=================================================="
echo " 📋 설치 안내"
echo "=================================================="
echo ""
echo "🎯 권장 설치 방법:"
echo ""
echo "  1. 모든 프로젝트에서 사용 (개인 도구)"
echo "     → claude plugin install $PLUGIN_NAME@calab-marketplace --scope user"
echo ""
echo "  2. 현재 프로젝트만 (팀 공유)"
echo "     → claude plugin install $PLUGIN_NAME@calab-marketplace --scope project"
echo ""
echo "  3. 테스트용 (세션 격리)"
echo "     → claude plugin install $PLUGIN_NAME@calab-marketplace --scope local"
echo ""
echo "✨ 설치 후 사용법:"
echo "  /calab-plugin:onboard        - 프로젝트 분석"
echo "  /calab-plugin:dev-plan       - 기획"
echo "  /calab-plugin:dev-design     - 설계"
echo "  /calab-plugin:research       - 리서치"
echo ""
echo "📚 자세한 사용법: CLAUDE.md 참조"
echo ""
