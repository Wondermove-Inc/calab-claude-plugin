#!/usr/bin/env python3
"""
JIRA 연동 유틸리티 함수

설정 파일, 매핑 파일, Worktree 파일 로드/저장을 담당합니다.
"""

import json
from pathlib import Path


def load_config(config_path: str | Path | None = None) -> dict:
    """
    설정 파일 로드

    Args:
        config_path: 설정 파일 경로 (None이면 기본 경로 사용)

    Returns:
        설정 dict (파일 없으면 빈 dict)
    """
    if config_path is None:
        # 기본 경로: plugins/jira/integrations/ 기준
        project_root = Path(__file__).parent.parent.parent.parent
        config_path = project_root / '.claude' / 'integrations' / 'jira_config.json'

    config_path = Path(config_path)

    if not config_path.exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_mapping(mapping_path: str | Path | None = None) -> dict:
    """
    매핑 파일 로드

    Args:
        mapping_path: 매핑 파일 경로 (None이면 기본 경로 사용)

    Returns:
        매핑 dict
    """
    if mapping_path is None:
        project_root = Path(__file__).parent.parent.parent.parent
        mapping_path = project_root / '.claude-state' / 'jira_mapping.json'

    mapping_path = Path(mapping_path)

    if not mapping_path.exists():
        return {
            'project_key': None,
            'base_url': None,
            'mappings': {},
            'reverse_mappings': {},
            'last_sync': None,
            'sync_history': []
        }

    with open(mapping_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mapping(mapping: dict, mapping_path: str | Path | None = None) -> None:
    """
    매핑 파일 저장

    Args:
        mapping: 저장할 매핑 dict
        mapping_path: 매핑 파일 경로 (None이면 기본 경로 사용)
    """
    if mapping_path is None:
        project_root = Path(__file__).parent.parent.parent.parent
        mapping_path = project_root / '.claude-state' / 'jira_mapping.json'

    mapping_path = Path(mapping_path)
    mapping_path.parent.mkdir(parents=True, exist_ok=True)

    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)


def load_worktree(worktree_path: str | Path | None = None) -> dict:
    """
    Worktree 파일 로드

    Args:
        worktree_path: Worktree 파일 경로 (None이면 기본 경로 사용)

    Returns:
        Worktree dict (파일 없으면 빈 dict)
    """
    if worktree_path is None:
        project_root = Path(__file__).parent.parent.parent.parent
        worktree_path = project_root / '.claude-state' / 'worktree.json'

    worktree_path = Path(worktree_path)

    if not worktree_path.exists():
        return {}

    with open(worktree_path, 'r', encoding='utf-8') as f:
        return json.load(f)
