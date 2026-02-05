#!/usr/bin/env python3
"""
dev 플러그인 워크플로우 강제 Hook

사용자 입력에서 개발 관련 키워드를 감지하면
/dev:workflow 스킬 호출을 강제하는 메시지를 출력합니다.
"""
import sys
import re

def main():
    prompt = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    original_prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # 예외 패턴 (이미 슬래시 커맨드 사용 중이거나 제외 대상)
    exceptions = [
        r'^/', r'/workflow', r'/dev:', r'/toolkit:', r'/commit',
        r'^git\s', r'^bd\s', r'^npm\s', r'^make\s', r'^go\s',
        r'설명해', r'알려줘', r'뭐야', r'무엇', r'\?$',
        r'readme', r'changelog', r'문서.*수정', r'문서.*작성'
    ]
    
    for exc in exceptions:
        if re.search(exc, prompt):
            sys.exit(0)
    
    # 워크플로우 필수 키워드
    keywords = {
        # 리팩토링
        '리팩토링': 'refactoring',
        '리펙토링': 'refactoring', 
        'refactor': 'refactoring',
        # 기능 개발
        '기능 개발': 'feature',
        '기능 추가': 'feature',
        '기능을 추가': 'feature',
        '새로운 기능': 'feature',
        'feature': 'feature',
        # 버그 수정
        '버그 수정': 'bugfix',
        '버그를 수정': 'bugfix',
        '버그를 고쳐': 'bugfix',
        '오류 수정': 'bugfix',
        'fix': 'bugfix',
        'bug': 'bugfix',
        # 성능 최적화
        '성능 최적화': 'optimization',
        '최적화': 'optimization',
        '성능 개선': 'optimization',
        'optimize': 'optimization',
        'performance': 'optimization',
        # 테스트
        '테스트 작성': 'testing',
        '테스트를 작성': 'testing',
        '테스트 추가': 'testing',
        '테스트 코드': 'testing',
        # 설계/아키텍처
        '설계': 'architecture',
        '아키텍처': 'architecture',
        'design': 'architecture',
        'architecture': 'architecture',
        # 구현
        '구현해': 'implementation',
        '개발해': 'implementation',
        '만들어': 'implementation',
        '추가해': 'implementation',
        '수정해': 'implementation',
        '변경해': 'implementation',
    }
    
    # 키워드 감지
    detected = None
    for kw, category in keywords.items():
        if kw in prompt:
            detected = (kw, category)
            break
    
    if detected:
        kw, category = detected
        print(f"""
<user-prompt-submit-hook>
🚨 **워크플로우 필수 요청 감지** (키워드: "{kw}")

이 요청은 **반드시** `/dev:workflow` 스킬을 통해 처리해야 합니다.

## 필수 행동
1. **즉시** Skill 도구를 호출하세요: `Skill(skill: "dev:workflow", args: "{original_prompt}")`
2. 직접 코드를 읽거나 분석하지 마세요
3. Task 에이전트를 직접 호출하지 마세요
4. Read, Grep, Glob 도구로 코드를 탐색하지 마세요

## 이유
dev 플러그인의 워크플로우는 체계적인 Quality Gates와 이슈 관리를 제공합니다.
직접 처리하면 작업 추적과 품질 검증이 누락됩니다.

**지금 즉시 Skill 도구로 dev:workflow를 호출하세요.**
</user-prompt-submit-hook>
""")

if __name__ == "__main__":
    main()
