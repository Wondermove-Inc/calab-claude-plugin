#!/usr/bin/env python3
"""
Skill Next Step Hook - 스킬 완료 후 다음 단계 선택 제시

트리거: Stop 이벤트
동작: 스킬 완료 시 다음 단계 옵션을 제시하여 사용자가 선택할 수 있게 함

Output: Claude에게 AskUserQuestion 호출 지시 주입
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional


# 스킬별 다음 단계 정의
SKILL_NEXT_STEPS: Dict[str, Dict] = {
    'brainstorm': {
        'default': {
            'description': '브레인스토밍 완료',
            'options': [
                {'label': '/plan', 'description': 'PRD 작성으로 진행 (권장)'},
                {'label': '/plan', 'description': '수정 계획 작성'},
                {'label': '/research', 'description': '추가 조사'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'plan': {
        'default': {
            'description': 'PRD 작성 완료',
            'options': [
                {'label': '/handoff', 'description': 'Codex에 구현 위임 (권장)'},
                {'label': '수정 요청', 'description': 'PRD 내용 수정/보완'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        },
        'design': {
            'description': 'PRD + 아키텍처 설계 완료',
            'options': [
                {'label': '/handoff', 'description': 'Codex에 구현 위임 (권장)'},
                {'label': '수정 요청', 'description': '설계 내용 수정/보완'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'onboard': {
        'quick': {
            'description': '빠른 온보딩 완료',
            'options': [
                {'label': '/onboard --full', 'description': '전체 온보딩으로 확장'},
                {'label': '/plan', 'description': '개발 시작'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        },
        'full': {
            'description': '전체 온보딩 완료',
            'options': [
                {'label': '/plan', 'description': '새 기능 개발 시작'},
                {'label': '/brainstorm', 'description': '문제 분석 시작'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        },
        'default': {
            'description': '온보딩 완료',
            'options': [
                {'label': '/plan', 'description': '개발 시작'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'guard': {
        'default': {
            'description': '규칙 검증 완료',
            'options': [
                {'label': '수정 진행', 'description': '발견된 이슈 수정'},
                {'label': '/plan', 'description': '다음 Task 구현'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'security': {
        'default': {
            'description': '보안 검사 완료',
            'options': [
                {'label': '취약점 수정', 'description': '발견된 취약점 수정'},
                {'label': '/guard', 'description': '전체 검증'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'docs': {
        'default': {
            'description': '문서 생성 완료',
            'options': [
                {'label': '다른 문서 생성', 'description': '추가 문서 생성'},
                {'label': '/plan', 'description': '개발 계속'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'refactor': {
        'default': {
            'description': '리팩토링 완료',
            'options': [
                {'label': '/guard', 'description': '변경 검증'},
                {'label': '추가 리팩토링', 'description': '다른 영역 정리'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'research': {
        'default': {
            'description': '리서치 완료',
            'options': [
                {'label': '/plan', 'description': '조사 결과로 개발 시작'},
                {'label': '추가 조사', 'description': '다른 주제 조사'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'e2e': {
        'default': {
            'description': 'E2E 테스트 완료',
            'options': [
                {'label': '실패 수정', 'description': '실패한 테스트 수정'},
                {'label': '테스트 추가', 'description': '새 테스트 케이스 추가'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
    'jira': {
        'default': {
            'description': 'JIRA 동기화 완료',
            'options': [
                {'label': '/plan', 'description': '이슈 구현 시작'},
                {'label': '다른 이슈', 'description': '다른 이슈 처리'},
                {'label': '종료', 'description': '나중에 계속'},
            ]
        }
    },
}


def get_current_skill() -> Optional[str]:
    """현재 활성화된 스킬 확인"""
    state_path = Path(os.getcwd()) / '.claude-state' / 'current_skill.json'
    if state_path.exists():
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('skill'), data.get('option', 'default')
        except (json.JSONDecodeError, IOError):
            pass
    return None, None


def save_current_skill(skill: str, option: str = 'default'):
    """현재 스킬 저장"""
    state_path = Path(os.getcwd()) / '.claude-state'
    state_path.mkdir(parents=True, exist_ok=True)

    skill_file = state_path / 'current_skill.json'
    with open(skill_file, 'w', encoding='utf-8') as f:
        json.dump({'skill': skill, 'option': option}, f, ensure_ascii=False)


def clear_current_skill():
    """현재 스킬 상태 클리어"""
    state_path = Path(os.getcwd()) / '.claude-state' / 'current_skill.json'
    if state_path.exists():
        state_path.unlink()


def format_next_step_prompt(skill: str, option: str) -> str:
    """다음 단계 선택 프롬프트 생성"""
    if skill not in SKILL_NEXT_STEPS:
        return ""

    skill_steps = SKILL_NEXT_STEPS[skill]
    step_info = skill_steps.get(option, skill_steps.get('default', {}))

    if not step_info:
        return ""

    description = step_info.get('description', '작업 완료')
    options = step_info.get('options', [])

    if not options:
        return ""

    # Claude에게 AskUserQuestion 호출 지시
    options_json = json.dumps(options, ensure_ascii=False)

    return f"""
<next-step-required>
## 스킬 완료: {description}

**다음 단계를 선택해주세요.**

AskUserQuestion 도구를 사용하여 다음 옵션을 제시하세요:

```json
{{
  "questions": [{{
    "question": "{description}. 다음으로 무엇을 하시겠습니까?",
    "header": "다음 단계",
    "options": {options_json},
    "multiSelect": false
  }}]
}}
```

**중요**: 반드시 AskUserQuestion을 호출하여 사용자가 다음 단계를 선택할 수 있게 하세요.
</next-step-required>
"""


def main():
    """
    메인 함수 - Hook Entry Point

    Stop 이벤트에서 호출됨.
    스킬 완료 시 다음 단계 옵션 제시.
    """
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')

        # Stop 이벤트만 처리
        if hook_event != 'Stop':
            sys.exit(0)

        # 현재 스킬 확인
        skill, option = get_current_skill()

        if not skill:
            sys.exit(0)

        # 다음 단계 프롬프트 생성
        prompt = format_next_step_prompt(skill, option or 'default')

        if prompt:
            print(prompt)

        # 스킬 상태 클리어
        clear_current_skill()

    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
