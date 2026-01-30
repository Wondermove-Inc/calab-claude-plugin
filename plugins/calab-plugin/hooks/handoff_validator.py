#!/usr/bin/env python3
"""
Handoff Validator Hook - 단계 간 전제 조건 검증

트리거: UserPromptSubmit 이벤트
동작: /dev 명령어의 각 단계 실행 전 이전 단계 산출물 존재 확인

Structured Handoffs:
- --design: 01-PRD.md 필수
- --tasks: 01-PRD.md + 02-architecture.md 필수
- --build: 03-tasks.md + worktree.json 필수
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import List, Tuple, Optional

# 프로젝트 루트 경로
PROJECT_ROOT = Path(os.getcwd())
DOCS_PATH = PROJECT_ROOT / '.claude' / 'docs' / 'active'
STATE_PATH = PROJECT_ROOT / '.claude-state'


# 단계별 전제 조건 정의 (새 파일 구조에 맞게 업데이트)
HANDOFF_PREREQUISITES = {
    '--plan': {
        'required_files': [],
        'description': '첫 단계 (전제 조건 없음)'
    },
    '--design': {
        'required_files': [
            ('01-brainstorm.md', '브레인스토밍 문서'),
            ('02-PRD.md', 'PRD 문서')
        ],
        'description': '브레인스토밍 + PRD 문서 필요',
        'previous_step': '--plan'
    },
    '--tasks': {
        'required_files': [
            ('03-architecture.md', '아키텍처 설계 문서'),
            ('04-ERD.md', 'ERD 문서')
        ],
        'description': '아키텍처 + ERD 문서 필요',
        'previous_step': '--design'
    },
    '--build': {
        'required_files': [
            ('05-tasks.md', 'Task 분해 문서')
        ],
        'extra_files': [
            (STATE_PATH / 'worktree.json', 'Worktree 상태 파일')
        ],
        'description': 'Task 문서 + Worktree 필요',
        'previous_step': '--tasks'
    }
}


def find_feature_folders() -> List[Path]:
    """
    활성 기능 폴더 목록 반환
    .claude/docs/active/ 하위 폴더들
    """
    if not DOCS_PATH.exists():
        return []

    folders = []
    for item in DOCS_PATH.iterdir():
        if item.is_dir():
            folders.append(item)

    return sorted(folders, key=lambda x: x.stat().st_mtime, reverse=True)


def check_file_exists(feature_folder: Path, filename: str) -> bool:
    """특정 파일이 기능 폴더에 존재하는지 확인"""
    file_path = feature_folder / filename
    return file_path.exists() and file_path.is_file()


def validate_handoff(step: str, feature_name: Optional[str] = None) -> Tuple[bool, str, List[str]]:
    """
    단계별 전제 조건 검증

    Returns:
        (통과여부, 메시지, 누락된_파일목록)
    """
    if step not in HANDOFF_PREREQUISITES:
        return True, '', []

    prereq = HANDOFF_PREREQUISITES[step]
    required_files = prereq.get('required_files', [])
    extra_files = prereq.get('extra_files', [])

    # 전제 조건 없는 단계
    if not required_files and not extra_files:
        return True, '', []

    # 기능 폴더 찾기
    feature_folders = find_feature_folders()

    if not feature_folders:
        if required_files:
            return False, f"⚠️  {step} 실행 불가: 활성 기능 폴더가 없습니다.\n   먼저 /dev --plan [기능명]을 실행하세요.", []
        return True, '', []

    # 특정 기능명이 있으면 해당 폴더만 검사
    if feature_name:
        target_folders = [f for f in feature_folders if f.name == feature_name]
        if not target_folders:
            # 새 기능이면 통과 (--plan 단계)
            if step == '--plan':
                return True, '', []
            return False, f"⚠️  기능 '{feature_name}' 폴더가 없습니다.", []
    else:
        # 가장 최근 폴더 사용
        target_folders = [feature_folders[0]]

    missing = []

    # 필수 파일 확인 (기능 폴더 내)
    for folder in target_folders:
        for filename, desc in required_files:
            if not check_file_exists(folder, filename):
                missing.append(f"{filename} ({desc})")

    # 추가 파일 확인 (절대 경로)
    for file_path, desc in extra_files:
        if isinstance(file_path, Path):
            if not file_path.exists():
                missing.append(f"{file_path.name} ({desc})")

    if missing:
        prev_step = prereq.get('previous_step', '')
        msg = f"⚠️  {step} 실행 불가: 전제 조건 미충족\n"
        msg += f"   누락된 파일:\n"
        for m in missing:
            msg += f"   • {m}\n"
        if prev_step:
            msg += f"\n   먼저 /dev {prev_step}을 실행하세요."
        return False, msg, missing

    return True, '', []


def extract_dev_step(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    사용자 입력에서 /dev 단계와 기능명 추출

    Returns:
        (단계, 기능명) 또는 (None, None)
    """
    # /dev --plan feature_name 패턴
    patterns = [
        r'/dev\s+(--plan|--design|--tasks|--build)(?:\s+(.+))?',
        r'dev\s+(--plan|--design|--tasks|--build)(?:\s+(.+))?',
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            step = match.group(1).lower()
            feature = match.group(2).strip() if match.group(2) else None
            return step, feature

    return None, None


def main():
    """
    메인 함수 - Hook Entry Point

    UserPromptSubmit 이벤트에서 호출.
    /dev 명령어의 각 단계 전제 조건을 검증.
    """
    try:
        # stdin에서 데이터 읽기
        input_data = json.load(sys.stdin)

        hook_event_name = input_data.get('hook_event_name', '')

        # UserPromptSubmit 이벤트만 처리
        if hook_event_name != 'UserPromptSubmit':
            sys.exit(0)

        # 사용자 입력 추출
        user_input = input_data.get('user_input', '')

        # /dev 명령어인지 확인
        step, feature_name = extract_dev_step(user_input)

        if not step:
            sys.exit(0)

        # 전제 조건 검증
        passed, message, missing = validate_handoff(step, feature_name)

        if not passed:
            # 방법 1: JSON decision: block (Exit 0) - 구조화된 응답
            # 방법 2: Exit Code 2 + stderr - 간단한 차단
            #
            # 베스트 프랙티스: JSON 응답이 더 명확하므로 둘 다 지원

            # JSON 응답 (exit 0일 때 파싱됨)
            response = {
                "decision": "block",
                "reason": message,
                "systemMessage": f"전제 조건 미충족: {prereq.get('description', '')}. 이전 단계를 먼저 완료하세요."
            }
            print(json.dumps(response, ensure_ascii=False))

            # stderr로도 출력 (사용자 피드백)
            print(f"\n[HANDOFF VALIDATION FAILED]", file=sys.stderr)
            print(message, file=sys.stderr)
            print(f"\n⚠️  전제 조건 미충족으로 실행 차단", file=sys.stderr)
            print(f"   위 문제를 해결한 후 다시 시도하세요.", file=sys.stderr)

            # Exit Code 0 (JSON 응답이 파싱되도록)
            # decision: block이 차단을 처리함
            sys.exit(0)
        else:
            # 통과 시 조용히 종료
            pass

    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"[HANDOFF] Error: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()
