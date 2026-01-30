#!/usr/bin/env python3
"""
Skill Activator Hook - 스킬 강제 활성화 (벡터 검색 보완)

트리거: UserPromptSubmit 이벤트
동작: 키워드 기반 스킬 활성화 힌트를 Claude에게 제공

베스트 프랙티스:
- 벡터 검색 활성화율: 20% → 훅 기반 활성화율: 84%
- Plain text 출력으로 Claude에게 스킬 컨텍스트 주입
"""

import json
import sys
import re
from typing import List, Tuple


# 스킬 활성화 규칙 정의
# 우선순위: 1(최고) ~ 10(최저)
# 키워드 중복 최소화 - 각 스킬에 고유한 키워드만 할당
SKILL_ACTIVATION_RULES = {
    # Active Skills (우선순위 1-3)
    'solve': {
        'priority': 1,  # 최우선: 문제 해결은 즉시 대응 필요
        'keywords': [
            # solve 전용 키워드 (에러/버그 관련)
            '에러', 'error', '버그', 'bug', '오류', '실패', 'fail',
            '안됨', '안돼', '작동안함', '동작안함', 'not working', 'broken',
            '왜 안되지', '이상해', '예외', 'exception', 'crash', '크래시',
            '터짐', '죽음', '멈춤', 'hang', 'timeout', '타임아웃',
            '디버깅', 'debug', '5whys', 'rca', 'root cause'
        ],
        'hint': '[SKILL] /solve 스킬 활성화 - 문제 해결 프로세스',
        'subskills': {
            '5whys': ['5whys', '근본 원인', 'why'],
            'rca': ['RCA', 'root cause', '원인 분석'],
            'hypothesis': ['가설', 'hypothesis']
        }
    },
    'dev': {
        'priority': 2,  # 개발 워크플로우
        'keywords': [
            # dev 전용 키워드 (개발/구현 관련)
            '구현', 'implement', '개발', 'develop', '만들어', 'create',
            '기능', 'feature', '설계', 'design', '아키텍처', 'architecture',
            'PRD', '요구사항', 'requirement', '기획', 'plan',
            '태스크', 'task', '스토리', 'story', '에픽', 'epic',
            '착수', '진행', 'proceed', '코딩', 'coding'
        ],
        'hint': '[SKILL] /dev 스킬 활성화 - 개발 워크플로우 관리',
        'subskills': {
            'plan': ['기획', 'plan', 'PRD', '요구사항', '브레인스토밍'],
            'design': ['설계', 'design', '아키텍처', 'architecture', 'ERD'],
            'tasks': ['태스크', 'task', '분해', 'breakdown', '스토리'],
            'build': ['구현', 'implement', '코딩', 'coding']
        }
    },
    'onboard': {
        'priority': 3,  # 프로젝트 분석
        'keywords': [
            # onboard 전용 키워드 (분석/이해 관련)
            '온보딩', 'onboard', 'onboarding', '프로젝트 분석', '코드베이스',
            '기술 스택', 'tech stack', '스택', 'stack',
            '새 프로젝트', '처음', '어떻게 되어있어', '구조가 뭐야',
            '뭘로 만들어졌어', '코드 이해', '프로젝트 이해'
        ],
        'hint': '[SKILL] /onboard 스킬 활성화 - 프로젝트 온보딩'
    },

    # Passive Skills (우선순위 4-7, 중복 키워드 제거)
    'tdd-workflow': {
        'priority': 4,  # TDD 전용 (명확한 키워드)
        'keywords': [
            # tdd 전용 키워드
            'tdd', '테스트 주도', 'test first', '테스트 먼저',
            'red green', 'red-green-refactor', '단위 테스트', 'unit test'
        ],
        'hint': '[PASSIVE] tdd-workflow 스킬 로드 - Red-Green-Refactor 사이클 적용'
    },
    'best-practices': {
        'priority': 5,  # 기술별 베스트 프랙티스
        'keywords': [
            # 프레임워크/라이브러리 전용 키워드
            'react', 'vue', 'angular', 'svelte', 'node', 'python', 'go', 'rust',
            'java', 'typescript', 'graphql', 'prisma', 'drizzle',
            'fastapi', 'express', 'spring', 'django', 'flask', 'nest',
            'useState', 'useEffect', 'useMemo', 'useCallback'
        ],
        'hint': '[PASSIVE] best-practices 스킬 로드 - 기술별 베스트 프랙티스 적용'
    },
    'project-rules': {
        'priority': 6,  # 규칙/컨벤션 전용
        'keywords': [
            # 규칙 전용 키워드
            '규칙', 'rule', '컨벤션', 'convention', '스타일', 'style',
            '코딩 표준', 'coding standard', '네이밍', 'naming', 'lint', 'eslint'
        ],
        'hint': '[PASSIVE] project-rules 스킬 로드 - 프로젝트 규칙 참조'
    },
    'code-quality': {
        'priority': 7,  # 최후순위 (가장 일반적인 키워드)
        'keywords': [
            # 코드 작성 일반 키워드 (다른 스킬에 없는 것만)
            '함수', 'function', '클래스', 'class', '모듈', 'module',
            '리팩토링', 'refactor', '정리', 'cleanup', '500줄'
        ],
        'hint': '[PASSIVE] code-quality 스킬 로드 - 500줄 제한, 주석 필수 규칙 적용'
    }
}


def detect_skills(prompt: str) -> List[Tuple[str, str, str]]:
    """
    프롬프트에서 활성화할 스킬 감지 (우선순위 기반)

    Returns:
        List of (skill_name, hint, subskill_hint) - 우선순위 순으로 정렬됨
    """
    prompt_lower = prompt.lower()
    detected = []

    # 우선순위 순으로 정렬하여 순회
    sorted_rules = sorted(
        SKILL_ACTIVATION_RULES.items(),
        key=lambda x: x[1].get('priority', 99)
    )

    for skill_name, rule in sorted_rules:
        for keyword in rule['keywords']:
            if keyword.lower() in prompt_lower:
                # 서브스킬 감지
                subskill_hint = ''
                if 'subskills' in rule:
                    for sub_name, sub_keywords in rule['subskills'].items():
                        for sub_kw in sub_keywords:
                            if sub_kw.lower() in prompt_lower:
                                subskill_hint = f'  → 옵션: --{sub_name}'
                                break
                        if subskill_hint:
                            break

                detected.append((skill_name, rule['hint'], subskill_hint))
                break  # 각 스킬은 한 번만 감지

    # Active 스킬은 하나만 (최우선순위), Passive는 모두 반환
    active_skills = [(s, h, sub) for s, h, sub in detected if '[SKILL]' in h]
    passive_skills = [(s, h, sub) for s, h, sub in detected if '[PASSIVE]' in h]

    # Active 스킬은 가장 높은 우선순위 하나만
    result = []
    if active_skills:
        result.append(active_skills[0])  # 최우선순위 Active 스킬만
    result.extend(passive_skills)  # Passive는 모두

    return result


def format_skill_hints(detected_skills: List[Tuple[str, str, str]]) -> str:
    """
    스킬 힌트를 포맷팅

    Returns:
        Plain text 형태의 스킬 힌트 (Claude에게 주입)
    """
    if not detected_skills:
        return ""

    lines = []

    # Active 스킬과 Passive 스킬 분리
    active = [(s, h, sub) for s, h, sub in detected_skills if '[SKILL]' in h]
    passive = [(s, h, sub) for s, h, sub in detected_skills if '[PASSIVE]' in h]

    if active:
        for skill_name, hint, subskill in active:
            lines.append(hint)
            if subskill:
                lines.append(subskill)

    if passive:
        # Passive 스킬은 간략하게
        passive_names = [s for s, _, _ in passive]
        if passive_names:
            lines.append(f"[PASSIVE] 자동 로드됨: {', '.join(passive_names)}")

    return '\n'.join(lines)


def main():
    """
    메인 함수 - Hook Entry Point

    UserPromptSubmit 이벤트에서 호출.
    Exit Code 0 + stdout 출력 → Claude에게 컨텍스트 주입
    """
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt or len(prompt) < 3:
            sys.exit(0)

        # 슬래시 명령어는 이미 스킬이 활성화되므로 스킵
        if prompt.strip().startswith('/'):
            sys.exit(0)

        # 스킬 감지
        detected = detect_skills(prompt)

        if detected:
            hints = format_skill_hints(detected)
            if hints:
                print(hints)  # stdout으로 Claude에게 주입

    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
