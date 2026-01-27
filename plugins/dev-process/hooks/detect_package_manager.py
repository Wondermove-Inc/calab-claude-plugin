#!/usr/bin/env python3
"""
패키지 매니저 자동 감지 훅 (Package Manager Detection)

프로젝트의 lockfile을 기반으로 패키지 매니저를 자동 감지합니다.
SessionStart 훅으로 실행되어 세션 시작 시 올바른 패키지 매니저를 설정합니다.

지원 패키지 매니저:
    - npm (package-lock.json)
    - pnpm (pnpm-lock.yaml)
    - yarn (yarn.lock)
    - bun (bun.lockb)

참고:
    - everything-claude-code의 package-manager.js 기능 참조
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# 경로 설정
CWD = Path(os.getcwd())
STATE_DIR = CWD / ".claude-state"
PM_STATE_FILE = STATE_DIR / "package_manager.json"

# 패키지 매니저 감지 우선순위
LOCKFILE_MAP = {
    "bun.lockb": {
        "name": "bun",
        "install": "bun install",
        "add": "bun add",
        "add_dev": "bun add -D",
        "remove": "bun remove",
        "run": "bun run",
        "exec": "bunx"
    },
    "pnpm-lock.yaml": {
        "name": "pnpm",
        "install": "pnpm install",
        "add": "pnpm add",
        "add_dev": "pnpm add -D",
        "remove": "pnpm remove",
        "run": "pnpm run",
        "exec": "pnpm exec"
    },
    "yarn.lock": {
        "name": "yarn",
        "install": "yarn install",
        "add": "yarn add",
        "add_dev": "yarn add -D",
        "remove": "yarn remove",
        "run": "yarn",
        "exec": "yarn"
    },
    "package-lock.json": {
        "name": "npm",
        "install": "npm install",
        "add": "npm install",
        "add_dev": "npm install -D",
        "remove": "npm uninstall",
        "run": "npm run",
        "exec": "npx"
    }
}


def detect_package_manager() -> Optional[Dict]:
    """lockfile 기반 패키지 매니저 감지"""
    # 우선순위에 따라 감지
    for lockfile, pm_info in LOCKFILE_MAP.items():
        if (CWD / lockfile).exists():
            return pm_info

    # package.json만 있는 경우 npm 기본값
    if (CWD / "package.json").exists():
        return LOCKFILE_MAP["package-lock.json"]

    return None


def check_package_json() -> Optional[Dict]:
    """package.json에서 추가 정보 추출"""
    package_json = CWD / "package.json"
    if not package_json.exists():
        return None

    try:
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                "name": data.get("name"),
                "scripts": list(data.get("scripts", {}).keys()),
                "packageManager": data.get("packageManager")  # Corepack 설정
            }
    except (json.JSONDecodeError, IOError):
        return None


def save_pm_state(pm_info: Dict, pkg_info: Optional[Dict]) -> None:
    """패키지 매니저 상태 저장"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "package_manager": pm_info,
        "package_info": pkg_info,
        "detected_at": CWD.as_posix()
    }

    with open(PM_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def format_detection_message(pm_info: Dict, pkg_info: Optional[Dict]) -> str:
    """감지 결과 메시지 포맷"""
    lines = []
    lines.append(f"📦 패키지 매니저 감지: {pm_info['name']}")

    if pkg_info:
        if pkg_info.get("name"):
            lines.append(f"   프로젝트: {pkg_info['name']}")
        if pkg_info.get("scripts"):
            scripts = pkg_info["scripts"][:5]  # 최대 5개
            lines.append(f"   스크립트: {', '.join(scripts)}")

    lines.append("")
    lines.append("💡 사용 가능한 명령어:")
    lines.append(f"   • 설치: {pm_info['install']}")
    lines.append(f"   • 추가: {pm_info['add']} <package>")
    lines.append(f"   • 실행: {pm_info['run']} <script>")

    return "\n".join(lines)


def main() -> None:
    """메인 실행 함수"""
    # 패키지 매니저 감지
    pm_info = detect_package_manager()

    if not pm_info:
        print(json.dumps({
            "result": "pass",
            "message": "Node.js 프로젝트가 아닙니다."
        }))
        return

    # package.json 정보 추출
    pkg_info = check_package_json()

    # Corepack 설정 확인 (packageManager 필드)
    if pkg_info and pkg_info.get("packageManager"):
        pm_name = pkg_info["packageManager"].split("@")[0]
        for lockfile, info in LOCKFILE_MAP.items():
            if info["name"] == pm_name:
                pm_info = info
                break

    # 상태 저장
    save_pm_state(pm_info, pkg_info)

    # 결과 메시지
    message = format_detection_message(pm_info, pkg_info)

    print(json.dumps({
        "result": "pass",
        "message": message
    }))


if __name__ == "__main__":
    main()
