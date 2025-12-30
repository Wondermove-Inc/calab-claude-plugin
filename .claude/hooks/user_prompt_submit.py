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


def detect_slash_command(prompt: str) -> dict | None:
    """슬래시 명령어 감지"""
    prompt_stripped = prompt.strip()

    # 슬래시 명령어 패턴 정의
    command_patterns = {
        # 개발 워크플로우
        '/dev plan': {'type': 'design', 'category': '기획', 'command': '/dev plan'},
        '/dev design': {'type': 'design', 'category': '설계', 'command': '/dev design'},
        '/dev tasks': {'type': 'implement', 'category': '태스크 분해', 'command': '/dev tasks'},
        '/dev build': {'type': 'implement', 'category': '구현', 'command': '/dev build'},
        '/dev status': {'type': 'review', 'category': '진행 확인', 'command': '/dev status'},
        '/dev-plan': {'type': 'design', 'category': '기획', 'command': '/dev-plan'},
        '/dev-design': {'type': 'design', 'category': '설계', 'command': '/dev-design'},
        '/dev-tasks': {'type': 'implement', 'category': '태스크 분해', 'command': '/dev-tasks'},
        '/dev-build': {'type': 'implement', 'category': '구현', 'command': '/dev-build'},
        '/dev-status': {'type': 'review', 'category': '진행 확인', 'command': '/dev-status'},

        # 클린 아키텍처
        '/clean-init': {'type': 'design', 'category': '클린 아키텍처 초기화', 'command': '/clean-init'},
        '/clean-entity': {'type': 'implement', 'category': '엔티티 생성', 'command': '/clean-entity'},
        '/clean-usecase': {'type': 'implement', 'category': '유스케이스 생성', 'command': '/clean-usecase'},
        '/clean-validate': {'type': 'review', 'category': '아키텍처 검증', 'command': '/clean-validate'},

        # 온보딩
        '/onboard': {'type': 'research', 'category': '프로젝트 온보딩', 'command': '/onboard'},
        '/onboard-quick': {'type': 'research', 'category': '빠른 온보딩', 'command': '/onboard-quick'},
        '/learn': {'type': 'research', 'category': '영역 학습', 'command': '/learn'},
        '/context-refresh': {'type': 'document', 'category': '컨텍스트 갱신', 'command': '/context-refresh'},
        '/context-show': {'type': 'review', 'category': '컨텍스트 확인', 'command': '/context-show'},

        # 리서치
        '/research': {'type': 'research', 'category': '리서치', 'command': '/research'},

        # Worktree
        '/worktree': {'type': 'review', 'category': '작업 트리 확인', 'command': '/worktree'},
        '/worktree status': {'type': 'review', 'category': '작업 상태 확인', 'command': '/worktree status'},
        '/worktree start': {'type': 'implement', 'category': '태스크 시작', 'command': '/worktree start'},
        '/worktree done': {'type': 'implement', 'category': '태스크 완료', 'command': '/worktree done'},
        '/worktree block': {'type': 'implement', 'category': '블로커 등록', 'command': '/worktree block'},
        '/worktree reset': {'type': 'implement', 'category': '작업 트리 초기화', 'command': '/worktree reset'},

        # 컨텍스트 관리
        '/restore-context': {'type': 'review', 'category': '컨텍스트 복원', 'command': '/restore-context'},
        '/save-progress': {'type': 'document', 'category': '진행 저장', 'command': '/save-progress'},
        '/show-rules': {'type': 'review', 'category': '규칙 확인', 'command': '/show-rules'},

        # 코드 품질
        '/check-quality': {'type': 'review', 'category': '품질 검사', 'command': '/check-quality'},

        # 문제 해결
        '/solve': {'type': 'fix', 'category': '문제 해결', 'command': '/solve'},
        '/solve-log': {'type': 'review', 'category': '분석 로그 확인', 'command': '/solve-log'},
        '/solve-history': {'type': 'research', 'category': '해결 이력 검색', 'command': '/solve-history'},
        '/solve-report': {'type': 'document', 'category': '보고서 생성', 'command': '/solve-report'},

        # JIRA 연동
        '/jira-init': {'type': 'implement', 'category': 'JIRA 연동 초기화', 'command': '/jira-init'},
        '/jira-push': {'type': 'implement', 'category': 'JIRA 푸시', 'command': '/jira-push'},
        '/jira-pull': {'type': 'implement', 'category': 'JIRA 풀', 'command': '/jira-pull'},
        '/jira-sync': {'type': 'implement', 'category': 'JIRA 동기화', 'command': '/jira-sync'},
        '/jira-link': {'type': 'implement', 'category': 'JIRA 연결', 'command': '/jira-link'},
        '/jira-status': {'type': 'review', 'category': 'JIRA 상태 확인', 'command': '/jira-status'},
    }

    # 정확한 명령어 매칭 (긴 명령어부터 체크)
    for cmd, info in sorted(command_patterns.items(), key=lambda x: -len(x[0])):
        if prompt_stripped.startswith(cmd):
            return {
                'type': info['type'],
                'category': info['category'],
                'command': info['command'],
                'is_command': True
            }

    return None


def detect_work_intent(prompt: str) -> dict | None:
    """프롬프트에서 작업 의도 감지 (슬래시 명령어 + 자연어 키워드)"""

    # 1. 슬래시 명령어 우선 감지
    command_intent = detect_slash_command(prompt)
    if command_intent:
        return command_intent

    # 2. 자연어 키워드 기반 감지
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
                    'keyword': keyword,
                    'is_command': False
                }
                break
        if detected_intent:
            break

    return detected_intent


def extract_task_description(prompt: str) -> str:
    """프롬프트에서 작업 설명 추출 (슬래시 명령어 또는 첫 문장)"""
    prompt_stripped = prompt.strip()

    # 슬래시 명령어인 경우 전체 명령어 반환
    if prompt_stripped.startswith('/'):
        # 명령어와 인자를 포함한 전체 첫 줄 반환
        first_line = prompt_stripped.split('\n')[0].strip()
        if len(first_line) > 100:
            first_line = first_line[:97] + '...'
        return first_line

    # 자연어인 경우 첫 줄
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
    """사용자 프롬프트 로깅 (슬래시 명령어 + 자연어 모두 기록)"""
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
        'intent': intent.get('category') if intent else 'general',
        'is_command': intent.get('is_command', False) if intent else False
    }

    # 슬래시 명령어인 경우 command 필드 추가
    if intent and intent.get('is_command'):
        entry['command'] = intent.get('command', '')

    history['prompts'].append(entry)

    # 최근 100개만 유지 (50개에서 증가)
    history['prompts'] = history['prompts'][-100:]

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

        if not prompt or len(prompt) < 3:
            # 너무 짧은 프롬프트는 무시
            print("Success")
            return

        # 1. 작업 의도 감지 (슬래시 명령어 + 자연어)
        intent = detect_work_intent(prompt)

        # 2. 프롬프트 히스토리 기록 (모든 프롬프트 기록)
        log_user_prompt(prompt, intent)

        # 3. intent가 있으면 현재 목표 업데이트
        if intent:
            update_current_goal(prompt, intent)

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
