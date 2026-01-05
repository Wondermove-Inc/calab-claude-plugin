#!/bin/bash
# Calab Claude Plugin - 공식 플러그인 시스템 기반 제거

set -e

PLUGIN_NAME="calab-plugin"
MARKETPLACE_DIR="$HOME/.claude/calab-marketplace"

echo "=================================================="
echo " Calab Claude Plugin - 플러그인 제거"
echo "=================================================="
echo ""

echo "다음 명령어를 실행하세요:"
echo ""
echo "  # 플러그인 언설치"
echo "  claude plugin uninstall $PLUGIN_NAME"
echo ""
echo "  # 마켓플레이스 제거 (선택사항)"
echo "  claude plugin marketplace remove calab-marketplace"
echo ""
echo "  # 마켓플레이스 디렉토리 삭제 (선택사항)"
echo "  rm -rf $MARKETPLACE_DIR"
echo ""
echo "  # 확인"
echo "  claude plugin list"
echo ""

echo "=================================================="
echo " 📋 제거 안내"
echo "=================================================="
echo ""
echo "⚠️  주의사항:"
echo "  - 플러그인만 제거되고 사용자 설정은 보존됩니다"
echo "  - 프로젝트별 .claude/ 폴더는 영향받지 않습니다"
echo "  - SuperClaude 설정도 영향받지 않습니다"
echo ""
echo "🔄 재설치 방법:"
echo "  ./install-plugin.sh"
echo ""
