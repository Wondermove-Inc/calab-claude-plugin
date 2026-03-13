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
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# 경로 설정
HOME_DIR = os.environ.get('HOME', '')
PROJECT_DIR = os.environ.get('CLAUDE_PROJECT_DIR', '.')

# 상태는 프로젝트별
STATE_PATH = Path(PROJECT_DIR) / '.claude-state'

# 메모리 경로
PROJECT_MEMORY = Path(PROJECT_DIR) / '.claude' / 'memory'
GLOBAL_MEMORY = Path(HOME_DIR) / '.claude' / 'memory'

# 읽기: 프로젝트 우선, 없으면 글로벌 fallback
MEMORY_PATH = PROJECT_MEMORY if PROJECT_MEMORY.exists() else GLOBAL_MEMORY

# 쓰기: 항상 프로젝트에 (디렉토리 없으면 생성)
MEMORY_PATH_WRITE = PROJECT_MEMORY


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


def detect_slash_command(prompt: str) -> Optional[dict]:
    """슬래시 명령어 감지"""
    prompt_stripped = prompt.strip()

    # 슬래시 명령어 패턴 정의 (존재하는 스킬만 포함)
    # 현재 스킬: dev, solve, onboard (메타), best-practices, code-quality, tdd-workflow,
    #           project-rules, work-tracker, clarification-protocol (패시브)
    command_patterns = {
        # /plan - 작업 계획 (PRD 작성)
        '/plan --design': {'type': 'design', 'category': '계획 + 설계', 'command': '/plan --design'},
        '/plan': {'type': 'design', 'category': '계획', 'command': '/plan'},

        # /brainstorm - 발산적 사고 + 원인 분석
        '/brainstorm --5whys': {'type': 'fix', 'category': '5 Whys 분석', 'command': '/brainstorm --5whys'},
        '/brainstorm --rca': {'type': 'fix', 'category': 'Root Cause Analysis', 'command': '/brainstorm --rca'},
        '/brainstorm --hypothesis': {'type': 'fix', 'category': '가설 검증', 'command': '/brainstorm --hypothesis'},
        '/brainstorm': {'type': 'design', 'category': '브레인스토밍', 'command': '/brainstorm'},

        # /jira-ticket - JIRA 티켓 추천
        '/jira-ticket --subtasks': {'type': 'design', 'category': 'JIRA 티켓 추천 (Sub-task 포함)', 'command': '/jira-ticket --subtasks'},
        '/jira-ticket': {'type': 'design', 'category': 'JIRA 티켓 추천', 'command': '/jira-ticket'},

        # /cleanup - PR 머지 후 브랜치 정리
        '/cleanup --dry-run': {'type': 'refactor', 'category': '브랜치 정리 (미리보기)', 'command': '/cleanup --dry-run'},
        '/cleanup': {'type': 'refactor', 'category': '브랜치 정리', 'command': '/cleanup'},

        # /onboard - 프로젝트 온보딩 (메타 스킬)
        '/onboard --quick': {'type': 'research', 'category': '빠른 온보딩', 'command': '/onboard --quick'},
        '/onboard --phases': {'type': 'research', 'category': '단계별 온보딩', 'command': '/onboard --phases'},
        '/onboard': {'type': 'research', 'category': '프로젝트 온보딩', 'command': '/onboard'},
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


def detect_work_intent(prompt: str) -> Optional[dict]:
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
    """현재 목표 자동 업데이트 - 작업 스택에 누적"""
    # 읽기: 프로젝트 우선, 없으면 글로벌 fallback
    context_file_read = MEMORY_PATH / 'CURRENT_CONTEXT.md'
    # 쓰기: 항상 프로젝트에
    context_file = MEMORY_PATH_WRITE / 'CURRENT_CONTEXT.md'

    # 프로젝트 memory 디렉토리 생성
    MEMORY_PATH_WRITE.mkdir(parents=True, exist_ok=True)

    if not context_file.exists():
        if context_file_read.exists() and context_file_read != context_file:
            # 글로벌 템플릿을 프로젝트로 복사
            import shutil
            shutil.copy(context_file_read, context_file)
        else:
            # 기본 구조 생성
            create_default_context_file(context_file)

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    # 작업 설명 추출
    task_desc = extract_task_description(prompt)
    category = intent.get('category', '작업')
    timestamp = datetime.now().strftime('%H:%M')
    today = datetime.now().strftime('%Y-%m-%d')

    # 중복 방지: 작업 스택 섹션에서만 동일한 작업 설명 검사
    # 전체 task_desc를 비교하되, 타임스탬프 부분 제외
    stack_section_match = re.search(r'## 작업 스택[^\n]*\n\n(.*?)(\n\n---|\n\n##)', content, re.DOTALL)
    if stack_section_match:
        stack_content = stack_section_match.group(1)
        # 작업 스택에서 이미 같은 설명이 있는지 확인 (타임스탬프 제외)
        # 패턴: - [HH:MM] **[카테고리]** 설명
        existing_entries = re.findall(r'\*\*\[[^\]]+\]\*\* (.+)', stack_content)
        if task_desc in existing_entries:
            # 마지막 업데이트 시간만 갱신
            updated_content = re.sub(
                r'> 마지막 업데이트: .*',
                f'> 마지막 업데이트: {today} {timestamp} (자동)',
                content
            )
            try:
                with open(context_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            except Exception:
                pass
            return

    # 새 작업 항목
    new_work_entry = f"- [{timestamp}] **[{category}]** {task_desc}"

    updated_content = content

    # 방법 1: "작업 스택" 섹션에 추가
    stack_pattern = r'(## 작업 스택[^\n]*\n\n)(.*?)(\n\n---|\n\n##)'
    stack_match = re.search(stack_pattern, content, re.DOTALL)

    if stack_match:
        current_stack = stack_match.group(2).strip()
        # 비어있는 상태면 새 항목만 추가
        if '비어있음' in current_stack or current_stack == '':
            new_stack = new_work_entry
        else:
            # 기존 항목 위에 새 항목 추가 (스택이므로 최신이 위)
            new_stack = f"{new_work_entry}\n{current_stack}"

        updated_content = re.sub(
            stack_pattern,
            f"## 작업 스택 (위에서 아래로 진입 순서)\n\n{new_stack}\n\n---",
            updated_content,
            count=1,
            flags=re.DOTALL
        )
    else:
        # 방법 2: "최근 완료된 작업" 섹션 위에 추가
        recent_pattern = r'(## 최근 완료된 작업)'
        if re.search(recent_pattern, content):
            # "진행 중인 작업" 섹션이 있는지 확인
            progress_pattern = r'(## 진행 중인 작업[^\n]*\n\n)(.*?)(\n\n---|\n\n##)'
            progress_match = re.search(progress_pattern, content, re.DOTALL)

            if progress_match:
                # 기존 진행 중 섹션에 추가
                current_progress = progress_match.group(2).strip()
                if '없음' in current_progress or current_progress == '':
                    new_progress = new_work_entry
                else:
                    new_progress = f"{new_work_entry}\n{current_progress}"

                updated_content = re.sub(
                    progress_pattern,
                    f"## 진행 중인 작업\n\n{new_progress}\n\n---",
                    updated_content,
                    count=1
                )
            else:
                # "진행 중인 작업" 섹션 새로 생성
                updated_content = re.sub(
                    recent_pattern,
                    f"## 진행 중인 작업\n\n{new_work_entry}\n\n---\n\n## 최근 완료된 작업",
                    updated_content,
                    count=1
                )

    # 마지막 업데이트 시간 갱신
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


def create_default_context_file(context_file: Path):
    """기본 CURRENT_CONTEXT.md 파일 생성"""
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%H:%M')

    default_content = f"""# 현재 작업 컨텍스트

> 마지막 업데이트: {today} {timestamp} (자동)

---

## 현재 목표

(목표 설정 대기)

---

## 작업 스택 (위에서 아래로 진입 순서)

(작업 대기)

---

## 최근 완료된 작업

(없음)

---

## 주요 파일

(분석 대기)

---

*이 파일은 자동 훅에 의해 업데이트됩니다.*
"""

    try:
        context_file.parent.mkdir(parents=True, exist_ok=True)
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(default_content)
    except Exception:
        pass


def log_user_prompt(prompt: str, intent: Optional[dict]):
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


def update_work_history(prompt: str, intent: dict):
    """
    WORK_HISTORY.md에 작업 기록 추가

    역할 분리:
    - CURRENT_CONTEXT.md: 현재 작업 스택 (실시간 상태)
    - WORK_HISTORY.md: 날짜별 아카이브 (간략 기록)

    중복 최소화: 슬래시 명령어와 주요 작업만 기록
    """
    # 슬래시 명령어가 아닌 일반 작업은 기록하지 않음 (중복 방지)
    if not intent.get('is_command', False):
        return

    # 쓰기: 항상 프로젝트에
    history_file = MEMORY_PATH_WRITE / 'WORK_HISTORY.md'
    # 프로젝트 memory 디렉토리 생성
    MEMORY_PATH_WRITE.mkdir(parents=True, exist_ok=True)

    task_desc = extract_task_description(prompt)
    category = intent.get('category', '작업')
    timestamp = datetime.now().strftime('%H:%M')
    today = datetime.now().strftime('%Y-%m-%d')

    new_entry = f"- [{timestamp}] **[{category}]** {task_desc}"

    if not history_file.exists():
        # 파일이 없으면 기본 구조 생성
        default_content = f"""# 작업 히스토리

> 마지막 업데이트: {today} {timestamp} (자동)

---

## {today}

{new_entry}

---

*이 파일은 자동 훅에 의해 업데이트됩니다.*
"""
        try:
            history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(default_content)
        except Exception:
            pass
        return

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    updated_content = content

    # 오늘 날짜 섹션이 있는지 확인 (다양한 형식 지원)
    # 형식 1: ## 2025-12-30
    # 형식 2: ## 2025-12-30: 제목
    today_section_pattern = rf'(## {today}[^\n]*\n\n)(.*?)(\n\n---|\n\n##|$)'
    today_match = re.search(today_section_pattern, content, re.DOTALL)

    if today_match:
        # 오늘 섹션에 추가 (위에 새 항목 추가)
        section_header = today_match.group(1)
        current_entries = today_match.group(2).strip()
        section_end = today_match.group(3)

        # 기존 형식이 다르면 (예: ### 완료된 작업) 그 위에 추가
        if current_entries.startswith('###'):
            new_section = f"{new_entry}\n\n{current_entries}"
        else:
            new_section = f"{new_entry}\n{current_entries}"

        updated_content = re.sub(
            today_section_pattern,
            f'{section_header}{new_section}{section_end}',
            content,
            count=1,
            flags=re.DOTALL
        )
    else:
        # 오늘 섹션이 없으면 새로 생성
        # 첫 번째 --- 다음에 추가
        first_separator = content.find('---\n\n')
        if first_separator != -1:
            insert_pos = first_separator + 5  # '---\n\n' 다음
            new_section = f"## {today}\n\n{new_entry}\n\n---\n\n"
            updated_content = content[:insert_pos] + new_section + content[insert_pos:]
        else:
            # --- 가 없으면 파일 끝에 추가
            updated_content = content + f"\n\n## {today}\n\n{new_entry}\n\n---\n"

    # 마지막 업데이트 시간 갱신 (있으면)
    if '> 마지막 업데이트:' in updated_content:
        updated_content = re.sub(
            r'> 마지막 업데이트: .*',
            f'> 마지막 업데이트: {today} {timestamp} (자동)',
            updated_content
        )

    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception:
        pass


def get_context_reminder(intent: Optional[dict]) -> str:
    """작업 의도 기반 컨텍스트 리마인더"""
    if not intent:
        return ""

    reminders = {
        'implement': "📋 코드 품질: 500줄 제한, JSDoc 주석 필수",
        'fix': "🔍 문제 분석: /brainstorm 명령으로 원인 분석 가능",
        'refactor': "🏗️ 리팩토링: 기존 테스트 통과 확인 필수",
        'review': "✅ 리뷰: 품질 규칙 준수 여부 확인",
        'design': "📐 설계: /plan --design 명령으로 아키텍처 설계",
        'research': "🔎 리서치: /onboard 명령으로 프로젝트 분석",
        'document': "📝 문서화: 코드 주석과 README 동기화",
        'test': "🧪 테스트: TDD는 모든 빌드에서 기본 적용"
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

        # 3. intent가 있으면 현재 목표 업데이트 (CURRENT_CONTEXT.md + WORK_HISTORY.md)
        if intent:
            update_current_goal(prompt, intent)
            update_work_history(prompt, intent)

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
