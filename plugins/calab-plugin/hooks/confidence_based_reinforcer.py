#!/usr/bin/env python3
"""
Confidence-Based Reinforcer Hook - validator 결과에 따른 reinforcer 자동 호출 안내

트리거: SubagentStop 이벤트
동작:
1. validator 에이전트 완료 감지
2. 신뢰도 점수 파싱 (Confidence Score)
3. 70-89% 구간 → reinforcer 호출 권장 메시지 출력

신뢰도 기반 에스컬레이션:
- 90%+:   다음 Task 진행 가능
- 70-89%: reinforcer 자동 호출 권장
- 50-69%: 사용자 확인 필요
- 0-49%:  /solve 에스컬레이션 제안
"""

import json
import sys
import re
from pathlib import Path


def parse_confidence_score(output: str) -> float:
    """
    validator 출력에서 신뢰도 점수 추출

    Args:
        output: 에이전트 출력 텍스트

    Returns:
        신뢰도 점수 (0.0 ~ 100.0) 또는 -1 (파싱 실패)
    """
    # 패턴 1: "Confidence Score: 87.5%"
    pattern1 = r'[Cc]onfidence\s*[Ss]core[:\s]+(\d+\.?\d*)%?'
    # 패턴 2: "신뢰도 점수: 87.5%"
    pattern2 = r'신뢰도\s*점수[:\s]+(\d+\.?\d*)%?'
    # 패턴 3: "신뢰도: 87.5%"
    pattern3 = r'신뢰도[:\s]+(\d+\.?\d*)%?'

    for pattern in [pattern1, pattern2, pattern3]:
        match = re.search(pattern, output)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue

    return -1.0


def main():
    """
    메인 함수 - Hook Entry Point

    SubagentStop 이벤트에서 호출.
    validator 완료 시 신뢰도 기반 reinforcer 호출 안내.
    """
    try:
        input_data = json.load(sys.stdin)

        # 에이전트 정보 추출 (agent_type: Claude Code v2.0.42+ 공식 필드)
        agent_type = (
            input_data.get('agent_type', '') or
            input_data.get('subagent_type', '') or
            input_data.get('agent_name', '')
        )
        output = input_data.get('output', '')

        # validator 에이전트인지 확인
        is_validator = 'validator' in agent_type.lower() if agent_type else False

        if not is_validator:
            sys.exit(0)

        # 신뢰도 점수 파싱
        confidence = parse_confidence_score(output)

        if confidence < 0:
            # 파싱 실패 - 무시
            sys.exit(0)

        # 신뢰도 기반 안내 메시지
        if 70 <= confidence < 90:
            print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[AUTO] reinforcer 호출 권장
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

validator 신뢰도: {confidence:.1f}% (70-89% 구간)

이 구간은 자동 수정이 가능한 RETRIABLE 이슈가 있음을 나타냅니다.
reinforcer 에이전트를 호출하여 누락/미흡 항목을 자동 수정하세요.

권장 액션:
Task(subagent_type="calab-plugin:reinforcer", ...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        elif 50 <= confidence < 70:
            print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[WARN] 사용자 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

validator 신뢰도: {confidence:.1f}% (50-69% 구간)

이 구간은 수동 검토가 필요한 이슈가 있음을 나타냅니다.
AskUserQuestion으로 사용자에게 진행 방향을 확인하세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        elif confidence < 50:
            print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CRITICAL] /solve 에스컬레이션 권장
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

validator 신뢰도: {confidence:.1f}% (50% 미만)

심각한 이슈가 발견되었습니다.
/solve 스킬로 에스컬레이션하여 근본 원인 분석을 권장합니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        # 90%+ 는 메시지 없음 (정상)

    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
