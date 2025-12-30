#!/usr/bin/env python3
"""
UserPromptSubmit Hook - 사용자 입력 전처리

트리거: 사용자가 프롬프트 제출 시
동작: 컨텍스트 자동 주입, 규칙 리마인더 추가
"""

import json
import sys
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
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_current_context() -> str:
    """현재 작업 컨텍스트 요약 반환"""
    context_file = MEMORY_PATH / 'CURRENT_CONTEXT.md'
    if not context_file.exists():
        return ""

    with open(context_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 현재 목표 섹션 추출
    lines = content.split('\n')
    goal_section = []
    in_goal = False

    for line in lines:
        if '## 현재 목표' in line:
            in_goal = True
            continue
        if in_goal:
            if line.startswith('## ') or line.startswith('---'):
                break
            if line.strip():
                goal_section.append(line.strip())

    return ' | '.join(goal_section[:3]) if goal_section else ""


def get_current_task() -> str:
    """현재 진행 중인 태스크 반환"""
    worktree_file = STATE_PATH / 'worktree.json'
    worktree = load_json(worktree_file)

    current_task = worktree.get('current_task', '')
    if not current_task:
        return ""

    # 태스크 이름 찾기
    for epic in worktree.get('epics', []):
        for story in epic.get('stories', []):
            for task in story.get('tasks', []):
                if task.get('id') == current_task:
                    return f"{current_task}: {task.get('name', '')}"

    return current_task


def detect_keywords(prompt: str) -> list:
    """프롬프트에서 특정 키워드 감지"""
    keywords_detected = []

    keyword_rules = {
        'code_change': ['코드', '구현', '작성', '수정', '추가', 'implement', 'write', 'create'],
        'review': ['리뷰', '검토', '확인', 'review', 'check'],
        'architecture': ['아키텍처', '설계', '구조', 'architecture', 'design'],
        'task_complete': ['완료', '끝', '다했', 'done', 'complete', 'finish'],
    }

    prompt_lower = prompt.lower()
    for rule_name, keywords in keyword_rules.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                keywords_detected.append(rule_name)
                break

    return list(set(keywords_detected))


def generate_context_reminder(keywords: list) -> str:
    """감지된 키워드 기반 컨텍스트 리마인더 생성"""
    reminders = []

    if 'code_change' in keywords:
        reminders.append("📋 코드 품질 규칙: 300줄 제한, 함수 주석 필수")

    if 'architecture' in keywords:
        reminders.append("🏗️ 클린 아키텍처: Domain → Application → Adapters → Infrastructure")

    if 'task_complete' in keywords:
        reminders.append("✅ 완료 시 /worktree done 실행 권장")

    return ' | '.join(reminders) if reminders else ""


def main():
    """
    메인 함수 - Hook Entry Point

    UserPromptSubmit 이벤트에서 호출됩니다.
    stdout으로 출력하면 프롬프트에 추가됩니다.
    """
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt:
            return

        # 컨텍스트 정보 수집
        current_context = get_current_context()
        current_task = get_current_task()
        keywords = detect_keywords(prompt)
        reminder = generate_context_reminder(keywords)

        # 컨텍스트 주입 (stdout으로 출력)
        context_parts = []

        if current_task:
            context_parts.append(f"[현재 태스크: {current_task}]")

        if reminder:
            context_parts.append(f"[리마인더: {reminder}]")

        if context_parts:
            # JSON 형식으로 출력 (Claude Code가 파싱)
            output = {
                "result": "continue",
                "context": " ".join(context_parts)
            }
            print(json.dumps(output, ensure_ascii=False))

    except Exception as e:
        # 에러 시 조용히 통과 (프롬프트 처리 방해하지 않음)
        pass


if __name__ == '__main__':
    main()
