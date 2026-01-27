#!/usr/bin/env python3
"""
JIRA Connector CLI 테스트 도구

사용법:
    python cli.py --test
    python cli.py --test --url https://your-domain.atlassian.net --project PROJ
"""

import argparse

from .connector import JiraConnector
from .utils import load_config


def main():
    """CLI 엔트리포인트"""
    parser = argparse.ArgumentParser(description='JIRA Connector CLI')
    parser.add_argument('--test', action='store_true', help='연결 테스트')
    parser.add_argument('--url', help='JIRA Base URL')
    parser.add_argument('--project', help='프로젝트 키')

    args = parser.parse_args()

    if args.test:
        config = load_config()
        if args.url:
            config.setdefault('jira', {})['base_url'] = args.url
        if args.project:
            config.setdefault('jira', {})['project_key'] = args.project

        connector = JiraConnector(config)
        result = connector.test_connection()

        if result['success']:
            print(f"✅ 연결 성공!")
            print(f"   사용자: {result['user']}")
            print(f"   이메일: {result['email']}")
        else:
            print(f"❌ 연결 실패: {result['error']}")


if __name__ == '__main__':
    main()
