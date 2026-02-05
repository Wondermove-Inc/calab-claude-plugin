#!/usr/bin/env python3
"""
Skill Activator Hook - 슬래시 명령어 기반 References 자동 로드 + 스킬 상태 저장

트리거: UserPromptSubmit 이벤트
동작:
1. /dev, /solve, /onboard 등 슬래시 명령어 감지 시 references 파일 자동 로드
2. 현재 스킬 상태 저장 (skill_next_step.py에서 사용)

변경 이력:
- v1: 키워드 기반 스킬 활성화 + References 로드
- v2: 자연어 패턴 확장
- v3: 슬래시 명령어 전용 (키워드 매칭 제거) - 깔끔하고 예측 가능한 동작
- v4: 스킬 상태 저장 추가 (다음 단계 선택 기능 지원)
"""

import json
import sys
import os
from pathlib import Path
from typing import Optional

# 프로젝트 루트
PROJECT_ROOT = Path(os.getcwd())
STATE_PATH = PROJECT_ROOT / '.claude-state'


# 플러그인 루트 경로 (환경 변수에서 가져오기)
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT', '')
if not PLUGIN_ROOT:
    # 훅 파일 기준으로 상위 디렉토리 추정
    PLUGIN_ROOT = str(Path(__file__).parent.parent)


# 스킬별 References 파일 매핑
# 옵션별로 로드할 파일 지정
SKILL_REFERENCES = {
    'dev': {
        'base_path': 'skills/dev/references',
        'options': {
            'plan': ['plan-phase.md', 'plan.md'],
            'discuss': ['plan.md'],
            'design': ['design-phase.md', 'design.md'],
            'tasks': ['tasks-phase.md', 'tasks.md'],
            'build': ['build-phase.md', 'build.md'],
            'roadmap': ['roadmap-phase.md'],
            'status': ['status.md'],
            'default': ['plan-phase.md']  # 옵션 없을 때
        },
        'templates': {
            'architecture': 'templates/architecture-template.md',
            'erd': 'templates/erd-template.md',
            'prd': 'templates/prd-template.md',
            'task': 'templates/task-template.md'
        },
        # 에이전트별 레퍼런스 (SubagentStart에서 사용)
        'agents': {
            'planner-task': ['tasks-phase.md'],
            'planner-phase': ['plan-phase.md'],
            'design': ['design-phase.md'],
            'dev-executor': ['build-phase.md']
        }
    },
    'solve': {
        'base_path': 'skills/solve/references',
        'options': {
            '5whys': ['5whys.md'],
            'rca': ['rca.md'],
            'hypothesis': ['hypothesis.md'],
            'binary': ['explore.md'],
            'log': ['log.md'],
            'report': ['report.md'],
            'explore': ['explore.md'],
            'fix': ['fix.md'],
            'default': ['testing.md']  # 기본 디버깅 참조
        },
        'templates': {
            'problem': 'templates/problem-definition.md',
            'analysis': 'templates/analysis-report.md',
            'solution': 'templates/solution-report.md'
        }
    },
    'onboard': {
        'base_path': 'skills/onboard/references',
        'options': {
            'quick': ['quick.md'],
            'full': ['project-onboarding.md', 'clean-architecture.md'],
            'phase': ['phases/01-discovery.md', 'phases/02-architecture.md',
                      'phases/03-context-gen.md', 'phases/04-domain.md'],
            'default': ['quick.md']
        },
        'templates': {
            'analysis': 'templates/analysis-report.md',
            'architecture': 'templates/architecture-template.md'
        }
    }
}

# calab- 접두사 매핑 (심볼릭 링크된 스킬용)
CALAB_SKILL_ALIASES = {
    'calab-dev': 'dev',
    'calab-solve': 'solve',
    'calab-onboard': 'onboard',
    'calab-docs': 'docs',
    'calab-security': 'security',
    'calab-research': 'research',
    'calab-jira': 'jira',
    'calab-refactor': 'refactor',
    'calab-e2e': 'e2e',
    'calab-guard': 'guard',
}

# 모든 스킬 목록 (references가 없어도 상태 저장 대상)
ALL_SKILLS = [
    'dev', 'solve', 'onboard', 'guard', 'security',
    'docs', 'refactor', 'e2e', 'jira', 'research'
]


def save_current_skill(skill: str, option: str = 'default'):
    """
    현재 활성화된 스킬 상태 저장

    skill_next_step.py에서 스킬 완료 후 다음 단계 제시에 사용
    """
    STATE_PATH.mkdir(parents=True, exist_ok=True)
    skill_file = STATE_PATH / 'current_skill.json'

    data = {
        'skill': skill,
        'option': option,
        'started_at': __import__('datetime').datetime.now().isoformat()
    }

    try:
        with open(skill_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def detect_option(prompt: str, skill_name: str) -> str:
    """
    프롬프트에서 스킬 옵션 감지

    Returns:
        옵션 이름 (예: 'plan', 'design') 또는 'default'
    """
    prompt_lower = prompt.lower()

    if skill_name == 'dev':
        if '--plan' in prompt_lower:
            return 'plan'
        elif '--discuss' in prompt_lower:
            return 'discuss'
        elif '--design' in prompt_lower:
            return 'design'
        elif '--tasks' in prompt_lower:
            return 'tasks'
        elif '--build' in prompt_lower:
            return 'build'
        elif '--roadmap' in prompt_lower:
            return 'roadmap'
        elif '--status' in prompt_lower:
            return 'status'
    elif skill_name == 'solve':
        if '--5whys' in prompt_lower:
            return '5whys'
        elif '--rca' in prompt_lower:
            return 'rca'
        elif '--hypothesis' in prompt_lower:
            return 'hypothesis'
        elif '--binary' in prompt_lower:
            return 'binary'
        elif '--log' in prompt_lower:
            return 'log'
        elif '--report' in prompt_lower:
            return 'report'
    elif skill_name == 'onboard':
        if '--quick' in prompt_lower:
            return 'quick'
        elif '--full' in prompt_lower:
            return 'full'
        elif '--phase' in prompt_lower:
            return 'phase'
        elif '--skip-domain' in prompt_lower:
            return 'skip-domain'

    return 'default'


def load_reference_files(skill_name: str, option: str) -> str:
    """
    스킬의 references 파일을 로드

    Args:
        skill_name: 스킬 이름 (dev, solve, onboard)
        option: 옵션 (plan, design, 5whys 등)

    Returns:
        파일 내용 (Claude 컨텍스트에 주입됨)
    """
    if skill_name not in SKILL_REFERENCES:
        return ""

    skill_ref = SKILL_REFERENCES[skill_name]
    base_path = Path(PLUGIN_ROOT) / skill_ref['base_path']

    # 옵션에 해당하는 파일 목록
    files_to_load = skill_ref['options'].get(option, skill_ref['options'].get('default', []))

    contents = []
    for filename in files_to_load:
        file_path = base_path / filename
        if file_path.exists():
            try:
                content = file_path.read_text(encoding='utf-8')
                # 파일 내용을 구분자로 감싸기
                contents.append(f"\n<reference file=\"{filename}\">\n{content}\n</reference>\n")
            except Exception:
                pass

    return ''.join(contents)


def parse_slash_command(prompt: str) -> Optional[str]:
    """
    슬래시 명령어에서 스킬 이름 추출

    Args:
        prompt: 사용자 프롬프트

    Returns:
        스킬 이름 또는 None
    """
    prompt_stripped = prompt.strip()
    if not prompt_stripped.startswith('/'):
        return None

    # 첫 번째 단어 추출 (/dev --plan → dev)
    first_word = prompt_stripped.split()[0].lower()
    skill_name = first_word.lstrip('/')

    # calab- 접두사 처리
    if skill_name in CALAB_SKILL_ALIASES:
        skill_name = CALAB_SKILL_ALIASES[skill_name]

    return skill_name


def main():
    """
    메인 함수 - Hook Entry Point

    UserPromptSubmit 이벤트에서 호출.
    슬래시 명령어 감지 시 references 파일 자동 로드.
    Exit Code 0 + stdout 출력 → Claude에게 컨텍스트 주입
    """
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt or len(prompt) < 2:
            sys.exit(0)

        # 슬래시 명령어만 처리
        skill_name = parse_slash_command(prompt)

        if skill_name and skill_name in ALL_SKILLS:
            option = detect_option(prompt, skill_name)

            # 현재 스킬 상태 저장 (다음 단계 선택 기능용)
            save_current_skill(skill_name, option)

            # References 로드 (있는 경우)
            if skill_name in SKILL_REFERENCES:
                ref_content = load_reference_files(skill_name, option)
                if ref_content:
                    print(f"[AUTO-LOADED] /{skill_name} references ({option}):")
                    print(ref_content)

    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
