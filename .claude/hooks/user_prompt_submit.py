#!/usr/bin/env python3
"""
UserPromptSubmit Hook - 사용자 입력 전처리 (완전 자동화)

트리거: 사용자가 프롬프트 제출 시
동작:
  1. 작업 의도 자동 감지 및 기록
  2. 현재 목표 자동 업데이트
  3. 컨텍스트 리마인더 제공
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
MEMORY_PATH = PROJECT_ROOT / '.claude' / 'memory'
STATE_PATH = PROJECT_ROOT / '.claude-state'


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path: Path, data: dict):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def detect_work_intent(prompt: str) -> dict | None:
    """프롬프트에서 작업 의도 감지"""
    prompt_lower = prompt.lower()

    # 작업 의도 패턴
    intent_patterns = {
        'implement': {
            'keywords': ['구현', '작성', '만들어', '추가', '생성', 'implement', 'create', 'add', 'write', 'build'],
            'category': '구현'
        },
        'fix': {
            'keywords': ['수정', '고쳐', '버그', '에러', '오류', 'fix', 'bug', 'error', 'debug'],
            'category': '수정/버그픽스'
        },
        'refactor': {
            'keywords': ['리팩토링', '개선', '정리', '리팩터', 'refactor', 'improve', 'clean'],
            'category': '리팩토링'
        },
        'review': {
            'keywords': ['리뷰', '검토', '확인', '검사', 'review', 'check', 'verify'],
            'category': '검토'
        },
        'design': {
            'keywords': ['설계', '아키텍처', '구조', '기획', 'design', 'architect', 'plan'],
            'category': '설계'
        },
        'research': {
            'keywords': ['조사', '리서치', '알아봐', '찾아', 'research', 'find', 'search'],
            'category': '리서치'
        },
        'document': {
            'keywords': ['문서', '주석', '설명', 'document', 'comment', 'explain'],
            'category': '문서화'
        },
        'test': {
            'keywords': ['테스트', '검증', 'test', 'verify', 'validate'],
            'category': '테스트'
        }
    }

    detected_intent = None
    for intent_type, data in intent_patterns.items():
        for keyword in data['keywords']:
            if keyword in prompt_lower:
                detected_intent = {
                    'type': intent_type,
                    'category': data['category'],
                    'keyword': keyword
                }
                break
        if detected_intent:
            break

    return detected_intent


def extract_task_description(prompt: str) -> str:
    """프롬프트에서 작업 설명 추출 (첫 문장 또는 핵심 부분)"""
    # 줄바꿈 기준 첫 줄
    first_line = prompt.split('\n')[0].strip()

    # 너무 길면 자르기
    if len(first_line) > 100:
        first_line = first_line[:97] + '...'

    return first_line


def update_current_goal(prompt: str, intent: dict):
    """현재 목표 자동 업데이트"""
    context_file = MEMORY_PATH / 'CURRENT_CONTEXT.md'

    if not context_file.exists():
        return

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    # 작업 설명 추출
    task_desc = extract_task_description(prompt)
    category = intent.get('category', '작업')
    timestamp = datetime.now().strftime('%H:%M')

    # "현재 목표" 섹션 찾기
    goal_pattern = r'(## 현재 목표\n\n)(.*?)(\n\n---|\n\n##)'
    match = re.search(goal_pattern, content, re.DOTALL)

    if not match:
        return

    # 새로운 목표로 업데이트 (기존 목표 유지하면서 현재 작업 추가)
    current_goal = match.group(2).strip()

    # 이미 같은 작업이 있으면 업데이트 안함
    if task_desc[:30] in current_goal:
        return

    # 현재 진행 중인 작업 표시
    new_goal_section = f"## 현재 목표\n\n**[{category}] {task_desc}** ← 진행 중 ({timestamp})"

    # 기존 목표가 있고 "완료"가 아니면 유지
    if current_goal and '✅ 완료' not in current_goal:
        # 기존 목표를 "이전 목표"로 이동하지 않고, 현재 목표만 업데이트
        pass

    updated_content = re.sub(
        goal_pattern,
        f"{new_goal_section}\n\n---",
        content,
        count=1
    )

    # 마지막 업데이트 시간 갱신
    today = datetime.now().strftime('%Y-%m-%d')
    updated_content = re.sub(
        r'> 마지막 업데이트: .*',
        f'> 마지막 업데이트: {today} {timestamp} (자동)',
        updated_content
    )

    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception:
        pass


def log_user_prompt(prompt: str, intent: dict | None):
    """사용자 프롬프트 로깅"""
    log_file = STATE_PATH / 'prompt_history.json'

    history = load_json(log_file)
    if not isinstance(history, dict):
        history = {'prompts': []}

    if 'prompts' not in history:
        history['prompts'] = []

    # 프롬프트 기록 (개인정보 보호를 위해 첫 100자만)
    entry = {
        'timestamp': datetime.now().isoformat(),
        'summary': extract_task_description(prompt),
        'intent': intent.get('category') if intent else 'unknown'
    }

    history['prompts'].append(entry)

    # 최근 50개만 유지
    history['prompts'] = history['prompts'][-50:]

    save_json(log_file, history)


def get_context_reminder(intent: dict | None) -> str:
    """작업 의도 기반 컨텍스트 리마인더"""
    if not intent:
        return ""

    reminders = {
        'implement': "📋 코드 품질: 300줄 제한, JSDoc 주석 필수",
        'fix': "🔍 문제 해결: /solve 명령으로 체계적 분석 가능",
        'refactor': "🏗️ 리팩토링: 기존 테스트 통과 확인 필수",
        'review': "✅ 리뷰: 품질 규칙 준수 여부 확인",
        'design': "📐 설계: 클린 아키텍처 4-레이어 고려",
        'research': "🔎 리서치: /research 명령으로 심층 조사",
        'document': "📝 문서화: 코드 주석과 README 동기화",
        'test': "🧪 테스트: TDD 모드 --tdd 옵션 활용"
    }

    return reminders.get(intent.get('type', ''), '')


def main():
    """
    메인 함수 - Hook Entry Point

    UserPromptSubmit 이벤트에서 호출됩니다.
    완전 자동화: 사용자 입력에서 작업 의도를 감지하고 자동 기록
    """
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt or len(prompt) < 5:
            # 너무 짧은 프롬프트는 무시
            print("Success")
            return

        # 1. 작업 의도 감지
        intent = detect_work_intent(prompt)

        if intent:
            # 2. 현재 목표 자동 업데이트
            update_current_goal(prompt, intent)

            # 3. 프롬프트 히스토리 기록
            log_user_prompt(prompt, intent)

        # 4. 컨텍스트 리마인더 생성 (stdout으로 출력하지 않음 - 조용히 동작)
        # reminder = get_context_reminder(intent)

        # 성공 응답
        print("Success")

    except Exception as e:
        # 에러 로깅
        try:
            error_log = STATE_PATH / 'hook_errors.log'
            with open(error_log, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] user_prompt_submit error: {e}\n")
        except Exception:
            pass

        # 에러가 있어도 프롬프트 처리는 진행
        print("Success")


if __name__ == '__main__':
    main()
