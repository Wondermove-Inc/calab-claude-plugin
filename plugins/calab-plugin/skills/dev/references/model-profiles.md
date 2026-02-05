# Model Profile Management

> **에이전트별 모델을 프로필로 관리하여 품질/비용/속도를 최적화한다**

---

## 프로필 종류

| 프로필 | 설명 | 사용 시점 |
|--------|------|----------|
| **quality** | 모든 단계 opus 사용 | 핵심 기능, 높은 정확도 필요 |
| **balanced** | 계획 opus + 실행 sonnet (권장) | 일반 개발 |
| **budget** | 모든 단계 haiku/sonnet | 반복 작업, 비용 절감 |

---

## 프로필별 모델 매핑

### quality 프로필

| 에이전트 | 모델 | 근거 |
|----------|------|------|
| planner-phase | opus | 전략적 기획 - 높은 추론 필요 |
| planner-task | opus | Task 분해 정확도 |
| design | opus | 아키텍처 결정 품질 |
| dev-executor | opus | 구현 정확도 |
| validator | opus | 검증 정밀도 |
| reinforcer | opus | 수정 정확도 |
| code-reviewer | opus | 리뷰 품질 |
| security-reviewer | opus | 보안 분석 정밀도 |
| task-validator | opus | 검증 품질 |

### balanced 프로필 (권장)

| 에이전트 | 모델 | 근거 |
|----------|------|------|
| planner-phase | opus | 전략적 기획 - 높은 추론 필요 |
| planner-task | sonnet | Task 분해는 sonnet으로 충분 |
| design | opus | 아키텍처 결정은 높은 추론 필요 |
| dev-executor | sonnet | 구현은 sonnet으로 충분 |
| validator | sonnet | 체크리스트 기반 검증 |
| reinforcer | sonnet | 패턴 기반 수정 |
| code-reviewer | sonnet | 코드 분석 |
| security-reviewer | opus | 보안은 높은 추론 필요 |
| task-validator | sonnet | 체크리스트 기반 검증 |

### budget 프로필

| 에이전트 | 모델 | 근거 |
|----------|------|------|
| planner-phase | sonnet | 비용 절감 |
| planner-task | haiku | 단순 분해 작업 |
| design | sonnet | 기본 설계 |
| dev-executor | sonnet | 구현 |
| validator | haiku | 빠른 체크 |
| reinforcer | sonnet | 수정 |
| code-reviewer | haiku | 빠른 리뷰 |
| security-reviewer | sonnet | 보안 검사 |
| task-validator | haiku | 빠른 검증 |

---

## 설정 파일

### 경로: `.claude/settings/model-profile.json`

```json
{
  "profile": "balanced",
  "overrides": {},
  "description": "에이전트별 모델 프로필 설정"
}
```

### Override 예시

```json
{
  "profile": "balanced",
  "overrides": {
    "dev-executor": "opus",
    "validator": "opus"
  }
}
```

> override가 설정되면 프로필 기본값 대신 override 모델 사용

---

## 적용 방법

### 에이전트 호출 시 모델 지정

```python
# 프로필에서 모델 결정
profile = Read(".claude/settings/model-profile.json")
model = get_model_for_agent("dev-executor", profile)

Task(
    subagent_type="calab-plugin:dev-executor",
    description="TDD 구현",
    prompt="...",
    model=model  # 프로필 기반 모델
)
```

### 프로필 변경

```python
def set_profile(profile_name):
    """프로필 변경"""
    config = Read(".claude/settings/model-profile.json")
    config["profile"] = profile_name
    Write(".claude/settings/model-profile.json", json.dumps(config))
```

### 단일 에이전트 오버라이드

```python
def set_model_override(agent_name, model):
    """특정 에이전트 모델 오버라이드"""
    config = Read(".claude/settings/model-profile.json")
    config["overrides"][agent_name] = model
    Write(".claude/settings/model-profile.json", json.dumps(config))
```

---

## 모델 선택 가이드

| 작업 특성 | 권장 모델 | 근거 |
|----------|----------|------|
| 전략적 결정 (기획, 설계) | opus | 높은 추론 능력 필요 |
| 코드 생성 (구현) | sonnet | 충분한 품질 + 빠른 속도 |
| 패턴 매칭 (검증, 리뷰) | sonnet/haiku | 체크리스트 기반 작업 |
| 보안 분석 | opus | 취약점 탐지에 높은 추론 필요 |
| 탐색/검색 | haiku | 빠른 응답 우선 |

---

## 비용 비교 (추정)

| 프로필 | 상대 비용 | 품질 |
|--------|----------|------|
| quality | 100% (기준) | ★★★★★ |
| balanced | ~60% | ★★★★☆ |
| budget | ~30% | ★★★☆☆ |
