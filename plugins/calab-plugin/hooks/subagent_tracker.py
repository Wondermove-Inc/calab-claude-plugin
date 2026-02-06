#!/usr/bin/env python3
"""
Subagent Tracker Hook - 서브에이전트 사용 추적 + 산출물 경로 자동 주입

트리거: SubagentStart, SubagentStop 이벤트
동작:
1. 서브에이전트 사용 로깅, 통계 수집
2. SubagentStart 시 필수 산출물 경로를 Claude 컨텍스트에 주입 (핵심)

공식 Claude Code Hook Input 필드 (v2.0.42+ / v2.0.43+):

SubagentStart (v2.0.43+):
  - session_id: 세션 고유 ID
  - transcript_path: 트랜스크립트 파일 경로
  - hook_event_name: "SubagentStart"
  - agent_id: 에이전트 고유 ID (v2.0.43+)
  - subagent_type: 에이전트 타입 (예: "Explore", "Plan") (v2.0.43+)

SubagentStop (v2.0.42+):
  - session_id: 세션 고유 ID
  - transcript_path: 트랜스크립트 파일 경로
  - hook_event_name: "SubagentStop"
  - agent_id: 에이전트 고유 ID (v2.0.42+)
  - agent_transcript_path: 에이전트 트랜스크립트 경로 (v2.0.42+)
  - stop_hook_active: 스톱 훅 활성 여부
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 경로 (현재 작업 디렉토리 사용)
PROJECT_ROOT = Path(os.getcwd())
STATE_PATH = PROJECT_ROOT / '.claude-state'

# 홈 디렉토리의 .claude-state도 체크
HOME_STATE_PATH = Path.home() / '.claude' / 'state'

# 플러그인 루트 경로
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT', '')
if not PLUGIN_ROOT:
    PLUGIN_ROOT = str(Path(__file__).parent.parent)


# 에이전트별 레퍼런스/템플릿 파일 (SubagentStart 시 컨텍스트 주입)
# 사용자 옵션 로드(skill_activator)와 별개로, 에이전트에 특화된 상세 레퍼런스 제공
AGENT_REFERENCES = {
    'calab-plugin:planner-phase': {
        'references': 'skills/dev/references',
        'files': ['plan-phase.md'],
        'templates': 'skills/dev/templates',
        'template_files': ['prd-template.md']
    },
    'calab-plugin:design': {
        'references': 'skills/dev/references',
        'files': ['design-phase.md', 'architecture-init.md', 'architecture-entity.md',
                  'architecture-usecase.md', 'architecture-validate.md'],
        'templates': 'skills/dev/templates',
        'template_files': ['architecture-template.md', 'erd-template.md']
    },
    'calab-plugin:planner-task': {
        'references': 'skills/dev/references',
        'files': ['tasks-phase.md'],
        'templates': 'skills/dev/templates',
        'template_files': ['task-template.md']
    },
    'calab-plugin:dev-executor': {
        'references': 'skills/dev/references',
        'files': ['build-phase.md']
    },
    'calab-plugin:root-cause-finder': {
        'references': 'skills/solve/references',
        'files': ['rca.md'],
        'templates': 'skills/solve/templates',
        'template_files': ['analysis-report.md']
    },
    'calab-plugin:bug-fixer': {
        'references': 'skills/solve/references',
        'files': ['fix.md'],
        'templates': 'skills/solve/templates',
        'template_files': ['solution-report.md']
    },
    'calab-plugin:project-onboarder': {
        'references': 'skills/onboard/references',
        'files': ['project-onboarding.md'],
        'templates': 'skills/onboard/templates',
        'template_files': ['analysis-report.md']
    }
}


# 에이전트별 필수 산출물 경로 (SubagentStart 시 주입)
# {feature}는 현재 작업 중인 기능명으로 대체됨
AGENT_REQUIRED_ARTIFACTS = {
    'calab-plugin:planner-phase': {
        'name': 'PRD 및 브레인스토밍',
        'paths': [
            '.claude/docs/active/{feature}/01-brainstorm.md',
            '.claude/docs/active/{feature}/02-PRD.md'
        ],
        'description': '기능 기획 문서를 생성합니다.'
    },
    'calab-plugin:design': {
        'name': '아키텍처 및 ERD',
        'paths': [
            '.claude/docs/active/{feature}/03-architecture.md',
            '.claude/docs/active/{feature}/04-ERD.md'
        ],
        'description': '설계 문서를 생성합니다.'
    },
    'calab-plugin:planner-task': {
        'name': 'Task 분해 및 Worktree',
        'paths': [
            '.claude/docs/active/{feature}/05-tasks.md',
            '.claude-state/worktree.json'
        ],
        'description': 'Task 분해 문서와 작업 트리를 생성합니다.'
    },
    'calab-plugin:dev-executor': {
        'name': '소스코드 및 테스트',
        'paths': [
            '소스 파일 (기능에 따라 다름)',
            '테스트 파일 (기능에 따라 다름)'
        ],
        'description': 'TDD 방식으로 코드를 구현합니다.',
        'update_worktree': True
    },
    'calab-plugin:validator': {
        'name': '검증 보고서',
        'paths': [
            '.claude/docs/active/{feature}/validation-report.md'
        ],
        'description': '검증 결과를 문서화합니다.'
    },
    'calab-plugin:reinforcer': {
        'name': '보강 보고서',
        'paths': [
            '.claude/docs/active/{feature}/reinforcer-report.md'
        ],
        'description': '보강 작업 결과를 문서화합니다.'
    },
    'calab-plugin:root-cause-finder': {
        'name': '원인 분석',
        'paths': [
            '.claude/problem-solving/active/{problem_id}/analysis.md'
        ],
        'description': '근본 원인 분석 결과를 문서화합니다.'
    },
    'calab-plugin:bug-fixer': {
        'name': '버그 수정 보고서',
        'paths': [
            '.claude/problem-solving/resolved/{problem_id}/fix-report.md'
        ],
        'description': '버그 수정 내용을 문서화합니다.'
    },
    'calab-plugin:project-onboarder': {
        'name': '프로젝트 컨텍스트',
        'paths': [
            '.claude/project-context/PROJECT_SUMMARY.md',
            '.claude/project-context/ARCHITECTURE.md',
            '.claude/project-context/CODE_PATTERNS.md',
            '.claude/project-context/CONVENTIONS.md',
            '.claude/memory/PROJECT_RULES.md'
        ],
        'description': '프로젝트 분석 결과를 문서화합니다.'
    },
    'calab-plugin:build-error-resolver': {
        'name': '빌드 오류 해결 보고서',
        'paths': [
            '.claude/docs/active/{feature}/build-error-report.md'
        ],
        'description': '빌드 오류 해결 과정을 문서화합니다.'
    },
    'calab-plugin:qa': {
        'name': 'QA 보고서',
        'paths': [
            '.claude/docs/active/{feature}/qa-report.md'
        ],
        'description': 'QA 검증 결과를 문서화합니다.'
    }
}


def get_state_path() -> Path:
    """상태 저장 경로 결정"""
    if STATE_PATH.exists() or (PROJECT_ROOT / '.claude').exists():
        return STATE_PATH
    return HOME_STATE_PATH


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json(path: Path, data: dict):
    """JSON 파일 저장"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_current_feature() -> str:
    """현재 작업 중인 기능명 추출"""
    state_path = get_state_path()

    # worktree.json에서 현재 기능명 추출
    worktree_file = state_path / 'worktree.json'
    if worktree_file.exists():
        worktree = load_json(worktree_file)
        if 'feature' in worktree:
            return worktree['feature']

    # CURRENT_CONTEXT.md에서 추출 시도
    context_file = PROJECT_ROOT / '.claude' / 'memory' / 'CURRENT_CONTEXT.md'
    if context_file.exists():
        try:
            content = context_file.read_text(encoding='utf-8')
            # "Feature: xxx" 또는 "기능: xxx" 패턴 찾기
            import re
            match = re.search(r'(?:Feature|기능):\s*(.+)', content)
            if match:
                return match.group(1).strip()
        except:
            pass

    return 'current-feature'


def inject_reference_files(subagent_type: str) -> str:
    """
    에이전트 타입에 맞는 레퍼런스/템플릿 파일을 컨텍스트에 주입

    Returns:
        stdout으로 출력할 레퍼런스 컨텐츠
    """
    if subagent_type not in AGENT_REFERENCES:
        return ''

    ref_spec = AGENT_REFERENCES[subagent_type]
    contents = []

    # 레퍼런스 파일 로드
    ref_base = Path(PLUGIN_ROOT) / ref_spec['references']
    for filename in ref_spec.get('files', []):
        file_path = ref_base / filename
        if file_path.exists():
            try:
                content = file_path.read_text(encoding='utf-8')
                contents.append(f"\n<reference file=\"{filename}\">\n{content}\n</reference>\n")
            except Exception:
                pass

    # 템플릿 파일 로드
    tmpl_base_path = ref_spec.get('templates')
    if tmpl_base_path:
        tmpl_base = Path(PLUGIN_ROOT) / tmpl_base_path
        for filename in ref_spec.get('template_files', []):
            file_path = tmpl_base / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    contents.append(f"\n<template file=\"{filename}\">\n{content}\n</template>\n")
                except Exception:
                    pass

    if contents:
        return f"[AUTO-LOADED] Agent references for {subagent_type}:" + ''.join(contents)
    return ''


def inject_artifact_requirements(subagent_type: str) -> str:
    """
    에이전트 타입에 맞는 필수 산출물 경로를 주입 메시지로 생성

    Returns:
        stdout으로 출력할 산출물 요구사항 메시지
    """
    if subagent_type not in AGENT_REQUIRED_ARTIFACTS:
        return ''

    artifact_spec = AGENT_REQUIRED_ARTIFACTS[subagent_type]
    feature = get_current_feature()

    # 경로에서 {feature} 치환
    paths = [p.replace('{feature}', feature) for p in artifact_spec['paths']]

    lines = [
        f"\n<artifact-requirements agent=\"{subagent_type}\">",
        f"## 필수 산출물 (CRITICAL)",
        f"",
        f"**{artifact_spec['name']}** - {artifact_spec['description']}",
        f"",
        f"### 반드시 생성해야 할 파일:",
    ]

    for path in paths:
        lines.append(f"- `{path}`")

    lines.extend([
        f"",
        f"⚠️ **산출물 미생성 시 작업 실패로 간주됩니다.**",
        f"⚠️ **작업 완료 전 반드시 위 파일들을 Write 도구로 생성하세요.**",
        f"</artifact-requirements>\n"
    ])

    return '\n'.join(lines)


def track_subagent_start(session_id: str, agent_id: str, subagent_type: str, transcript_path: str):
    """서브에이전트 시작 추적 + 산출물 경로 주입 (v2.0.43+ 필드 사용)"""
    state_path = get_state_path()
    stats_file = state_path / 'subagent_stats.json'
    stats = load_json(stats_file)

    # 에이전트 타입별 통계
    if 'agents' not in stats:
        stats['agents'] = {}

    if subagent_type not in stats['agents']:
        stats['agents'][subagent_type] = {
            'total_invocations': 0,
            'last_invoked': None
        }

    stats['agents'][subagent_type]['total_invocations'] += 1
    stats['agents'][subagent_type]['last_invoked'] = datetime.now().isoformat()

    # 현재 실행 중인 에이전트 기록
    if 'running' not in stats:
        stats['running'] = {}

    stats['running'][agent_id] = {
        'type': subagent_type,
        'session_id': session_id,
        'transcript_path': transcript_path,
        'started_at': datetime.now().isoformat()
    }

    # 병렬 배치 크기 추적 (verify-agents 패시브 트리거용)
    running_count = len(stats.get('running', {}))
    current_batch = stats.get('_parallel_batch_size', 0)
    if running_count > current_batch:
        stats['_parallel_batch_size'] = running_count

    # 전체 통계
    if 'total_starts' not in stats:
        stats['total_starts'] = 0
    stats['total_starts'] += 1
    stats['last_start'] = datetime.now().isoformat()

    save_json(stats_file, stats)

    # 레퍼런스/템플릿 주입 (SubagentStart 시 자동 로드)
    ref_msg = inject_reference_files(subagent_type)
    if ref_msg:
        print(ref_msg)

    # 산출물 경로 주입 (stdout → Claude 컨텍스트에 자동 추가)
    artifact_msg = inject_artifact_requirements(subagent_type)
    if artifact_msg:
        print(artifact_msg)

    # 로그 출력 (stderr로)
    print(f"[SUBAGENT] Started: {subagent_type} (id: {agent_id[:8]}...)", file=sys.stderr)


def track_subagent_stop(session_id: str, agent_id: str, agent_transcript_path: str, stop_hook_active: bool):
    """서브에이전트 종료 추적 (v2.0.42+ 필드 사용)"""
    state_path = get_state_path()
    stats_file = state_path / 'subagent_stats.json'
    stats = load_json(stats_file)

    running = stats.get('running', {})
    agent_info = running.pop(agent_id, None)

    if agent_info:
        subagent_type = agent_info.get('type', 'unknown')
        started_at = agent_info.get('started_at')

        # 실행 시간 계산
        duration = 0
        if started_at:
            try:
                start_time = datetime.fromisoformat(started_at)
                duration = (datetime.now() - start_time).total_seconds()

                # 평균 실행 시간 업데이트
                if subagent_type in stats.get('agents', {}):
                    agent_stats = stats['agents'][subagent_type]
                    prev_avg = agent_stats.get('avg_duration', 0)
                    count = agent_stats.get('total_invocations', 1)
                    new_avg = ((prev_avg * (count - 1)) + duration) / count
                    agent_stats['avg_duration'] = round(new_avg, 2)
            except (ValueError, TypeError):
                pass

        stats['running'] = running

        # 전체 통계 (항상 업데이트)
        if 'total_stops' not in stats:
            stats['total_stops'] = 0
        stats['total_stops'] += 1
        stats['last_stop'] = datetime.now().isoformat()

        # 병렬 에이전트 완료 감지: running이 비었고, 이전에 2개+ 에이전트가 실행 중이었으면
        prev_batch = stats.get('_parallel_batch_size', 0)
        if len(running) == 0 and prev_batch >= 2:
            # agent-verifier 자체는 트리거 대상에서 제외
            if subagent_type != 'calab-plugin:agent-verifier':
                stats['_parallel_batch_size'] = 0
                save_json(stats_file, stats)
                # stdout → Claude 컨텍스트에 자동 주입 (논블로킹)
                print(f"\n<verify-agents-trigger>")
                print(f"[AUTO-TRIGGER] 병렬 에이전트 {prev_batch}개 완료 감지")
                print(f"최근 완료: {subagent_type}")
                print(f"")
                print(f"## 자동 검증 (백그라운드, 논블로킹)")
                print(f"병렬 에이전트가 모두 완료되었습니다.")
                print(f"아래 호출을 **반드시 run_in_background=True**로 실행하세요.")
                print(f"사용자 작업을 차단하지 마세요.")
                print(f"")
                print(f"```python")
                print(f"Task(")
                print(f"    subagent_type=\"calab-plugin:agent-verifier\",")
                print(f"    description=\"병렬 에이전트 출력 자동 감사\",")
                print(f"    run_in_background=True,")
                print(f"    model=\"haiku\",")
                print(f"    prompt=\"최근 완료된 병렬 에이전트({prev_batch}개)의 산출물을 검증하세요. "
                       f".claude-state/subagent_stats.json과 subagent.log를 읽고, "
                       f"각 에이전트의 기대 산출물 존재 여부와 내용 충분성을 확인하세요. "
                       f"결과를 stdout으로 체크리스트 형태로 출력하세요.\"")
                print(f")")
                print(f"```")
                print(f"</verify-agents-trigger>\n")
            else:
                stats['_parallel_batch_size'] = 0
                save_json(stats_file, stats)
        else:
            save_json(stats_file, stats)

        # 로그 출력 (stderr로)
        print(f"[SUBAGENT] Stopped: {subagent_type} (duration: {duration:.1f}s)", file=sys.stderr)
    else:
        # running에서 찾지 못한 경우에도 기록
        if 'total_stops' not in stats:
            stats['total_stops'] = 0
        stats['total_stops'] += 1
        stats['last_stop'] = datetime.now().isoformat()
        save_json(stats_file, stats)

        print(f"[SUBAGENT] Stopped: unknown (id: {agent_id[:8] if agent_id else 'N/A'}...)", file=sys.stderr)


def extract_type_from_description(description: str) -> str:
    """
    description 필드에서 에이전트 타입 추출

    Task 도구 호출 시 description에 에이전트 정보가 포함될 수 있음
    """
    if not description:
        return ''

    # 알려진 에이전트 타입 패턴
    known_types = [
        'calab-plugin:planner-phase',
        'calab-plugin:design',
        'calab-plugin:planner-task',
        'calab-plugin:dev-executor',
        'calab-plugin:validator',
        'calab-plugin:reinforcer',
        'calab-plugin:code-reviewer',
        'calab-plugin:security-reviewer',
        'calab-plugin:root-cause-finder',
        'calab-plugin:bug-fixer',
        'calab-plugin:qa',
        'calab-plugin:web-researcher',
        'calab-plugin:deep-researcher',
        'calab-plugin:project-onboarder',
        'calab-plugin:doc-updater',
        'calab-plugin:docs-generator',
        'calab-plugin:build-error-resolver',
        'calab-plugin:e2e-runner',
        'calab-plugin:jira-connector',
        'calab-plugin:project-guardian',
        'calab-plugin:refactor-cleaner',
        'calab-plugin:task-validator',
        'calab-plugin:dev-workflow',
        'calab-plugin:agent-verifier',
        'Explore',
        'Plan',
        'general-purpose',
    ]

    description_lower = description.lower()
    for agent_type in known_types:
        if agent_type.lower() in description_lower:
            return agent_type

    return ''


def log_event(event_type: str, data: dict):
    """이벤트 로깅"""
    state_path = get_state_path()
    log_file = state_path / 'subagent.log'

    state_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{event_type}] {json.dumps(data, ensure_ascii=False)}\n"

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except IOError:
        pass


def main():
    """
    메인 함수 - Hook Entry Point

    사용법: python3 subagent_tracker.py [start|stop]

    Claude Code가 stdin으로 JSON 데이터를 전달합니다.
    v2.0.42+에서 agent_id, agent_transcript_path 필드 추가
    v2.0.43+에서 SubagentStart 훅과 subagent_type 필드 추가
    """
    # 커맨드라인 인자로 이벤트 타입 결정
    event_type = sys.argv[1] if len(sys.argv) > 1 else 'unknown'

    try:
        # stdin에서 Claude Code가 전달하는 공식 데이터 읽기
        input_data = json.load(sys.stdin)

        # 공통 필드
        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        hook_event_name = input_data.get('hook_event_name', event_type)

        # v2.0.42+ 필드
        agent_id = input_data.get('agent_id', 'unknown')

        # 이벤트 로깅
        log_event(hook_event_name, input_data)

        if event_type == 'start' or hook_event_name == 'SubagentStart':
            # v2.0.43+ SubagentStart 필드 - 여러 경로에서 타입 추출 시도
            subagent_type = (
                input_data.get('subagent_type') or
                input_data.get('tool_input', {}).get('subagent_type') or
                input_data.get('agent_type') or
                input_data.get('type') or
                extract_type_from_description(input_data.get('description', '')) or
                'unknown'
            )
            track_subagent_start(session_id, agent_id, subagent_type, transcript_path)

        elif event_type == 'stop' or hook_event_name == 'SubagentStop':
            # v2.0.42+ SubagentStop 필드
            agent_transcript_path = input_data.get('agent_transcript_path', '')
            stop_hook_active = input_data.get('stop_hook_active', False)
            track_subagent_stop(session_id, agent_id, agent_transcript_path, stop_hook_active)

    except json.JSONDecodeError:
        # JSON 파싱 실패 시 조용히 통과
        pass
    except Exception as e:
        # 다른 에러도 조용히 통과 (훅이 실패해도 Claude Code에 영향 주지 않음)
        print(f"[SUBAGENT] Error: {e}", file=sys.stderr)

    # 항상 성공 (exit code 0)
    sys.exit(0)


if __name__ == '__main__':
    main()
