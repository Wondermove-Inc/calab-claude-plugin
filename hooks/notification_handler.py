#!/usr/bin/env python3
"""
Notification Hook - 알림 커스터마이징

트리거: Claude Code가 알림 전송 시
동작: 데스크톱 알림, 로깅, 외부 서비스 연동
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOG_PATH = PROJECT_ROOT / '.claude-state' / 'notifications.log'


def log_notification(notification_type: str, message: str):
    """알림 로깅"""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{notification_type}] {message}\n"

    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def send_desktop_notification(title: str, message: str):
    """데스크톱 알림 전송 (Linux)"""
    try:
        # Linux notify-send 사용
        os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except Exception:
        pass


def format_notification(notification_data: dict) -> tuple:
    """알림 데이터 포맷팅"""
    notification_type = notification_data.get('type', 'info')
    message = notification_data.get('message', '')

    # 알림 타입별 제목 설정
    titles = {
        'input_needed': '🔔 Claude Code - 입력 필요',
        'task_complete': '✅ Claude Code - 작업 완료',
        'error': '❌ Claude Code - 오류 발생',
        'warning': '⚠️ Claude Code - 경고',
        'info': 'ℹ️ Claude Code'
    }

    title = titles.get(notification_type, titles['info'])

    return title, message


def main():
    """
    메인 함수 - Hook Entry Point

    Notification 이벤트에서 호출됩니다.
    """
    try:
        input_data = json.load(sys.stdin)

        notification_type = input_data.get('notification_type', 'info')
        message = input_data.get('message', 'Claude Code 알림')

        # 알림 로깅
        log_notification(notification_type, message)

        # 데스크톱 알림 전송
        title, formatted_message = format_notification({
            'type': notification_type,
            'message': message
        })

        send_desktop_notification(title, formatted_message)

        # Slack/Discord 웹훅 연동 (환경변수 설정 시)
        # webhook_url = os.environ.get('CLAUDE_NOTIFICATION_WEBHOOK')
        # if webhook_url:
        #     send_webhook(webhook_url, title, formatted_message)

    except Exception as e:
        # 에러 로깅
        log_notification('error', f'알림 처리 실패: {str(e)}')


if __name__ == '__main__':
    main()
