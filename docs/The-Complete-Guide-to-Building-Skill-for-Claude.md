# Claude를 위한 스킬 구축 완벽 가이드

**Claude**

---

## 목차

1. 서론 (3페이지)
2. 기본 원리 (4페이지)
3. 기획 및 설계 (7페이지)
4. 테스트 및 반복 개선 (14페이지)
5. 배포 및 공유 (18페이지)
6. 패턴 및 문제 해결 (21페이지)
7. 리소스 및 참고 자료 (28페이지)

---

## 1. 서론

스킬(Skill)은 Claude에게 특정 작업이나 워크플로우를 처리하는 방법을 가르치는 단순한 폴더 형태의 지침 세트입니다. 스킬은 특정 요구 사항에 맞춰 Claude를 커스터마이징하는 가장 강력한 방법 중 하나입니다. 매 대화마다 사용자의 선호도, 프로세스, 전문 지식을 다시 설명하는 대신, 스킬을 통해 Claude에게 한 번만 가르치면 매번 그 혜택을 누릴 수 있습니다.

스킬은 다음과 같은 반복 가능한 워크플로우가 있을 때 강력한 힘을 발휘합니다: 사양에 따른 프론트엔드 디자인 생성, 일관된 방법론을 통한 리서치 수행, 팀의 스타일 가이드를 따르는 문서 작성, 또는 다단계 프로세스 조정 등입니다. 스킬은 코드 실행 및 문서 생성과 같은 Claude의 기본 기능과 잘 작동합니다. MCP(Model Context Protocol) 통합을 구축하는 사람들에게 스킬은 단순한 도구 접근을 안정적이고 최적화된 워크플로우로 전환해 주는 또 다른 강력한 계층을 추가해 줍니다.

이 가이드는 기획 및 구조부터 테스트 및 배포에 이르기까지 효과적인 스킬을 구축하기 위해 알아야 할 모든 내용을 다룹니다. 자신을 위해서든, 팀을 위해서든, 커뮤니티를 위해서든, 가이드 전반에서 실용적인 패턴과 실제 사례를 발견할 수 있을 것입니다.

### 배울 내용

* 스킬 구조에 대한 기술적 요구 사항과 모범 사례
* 독립형 스킬 및 MCP 강화 워크플로우를 위한 패턴
* 다양한 유스케이스에서 효과적으로 작동하는 패턴
* 스킬을 테스트, 반복 개선 및 배포하는 방법

### 대상 독자

* Claude가 특정 워크플로우를 일관되게 따르도록 하려는 개발자
* Claude가 특정 워크플로우를 따르도록 하려는 파워 유저
* 조직 전체에서 Claude가 작동하는 방식을 표준화하려는 팀

### 이 가이드를 통한 두 가지 경로

**독립형 스킬을 구축하는 경우?** 기본 원리, 기획 및 설계, 카테고리 1-2에 집중하세요. **MCP 통합을 강화하는 경우?** "스킬 + MCP" 섹션과 카테고리 3이 적합합니다. 두 경로 모두 동일한 기술적 요구 사항을 공유하지만, 유스케이스에 관련된 내용을 선택할 수 있습니다.

### 이 가이드에서 얻을 수 있는 것

이 가이드를 마치면 단일 세션에서 기능적인 스킬을 구축할 수 있습니다. skill-creator를 사용하여 첫 번째 작동하는 스킬을 구축하고 테스트하는 데 약 15-30분이 소요됩니다.

시작해 봅시다.

---

## 2. 기본 원리

### 스킬이란 무엇인가?

스킬은 다음을 포함하는 폴더입니다:

* **SKILL.md (필수)**: YAML 프론트매터가 포함된 마크다운 형식의 지침
* **scripts/ (선택)**: 실행 가능한 코드 (Python, Bash 등)
* **references/ (선택)**: 필요할 때 로드되는 문서
* **assets/ (선택)**: 출력에 사용되는 템플릿, 폰트, 아이콘

### 핵심 설계 원칙

#### 점진적 공개 (Progressive Disclosure)

스킬은 3단계 시스템을 사용합니다:

* **1단계 (YAML 프론트매터)**: 항상 Claude의 시스템 프롬프트에 로드됩니다. 전체 내용을 컨텍스트에 로드하지 않고도 Claude가 각 스킬을 언제 사용해야 하는지 알 수 있도록 충분한 정보를 제공합니다.
* **2단계 (SKILL.md 본문)**: Claude가 스킬이 현재 작업과 관련이 있다고 판단할 때 로드됩니다. 전체 지침과 가이드가 포함됩니다.
* **3단계 (연결된 파일)**: Claude가 필요할 때만 탐색하고 발견하도록 선택할 수 있는 스킬 디렉토리 내에 번들된 추가 파일입니다.

이러한 점진적 공개는 전문 지식을 유지하면서 토큰 사용을 최소화합니다.

#### 조합성 (Composability)

Claude는 여러 스킬을 동시에 로드할 수 있습니다. 스킬은 다른 스킬과 함께 잘 작동해야 하며, 유일하게 사용 가능한 기능이라고 가정해서는 안 됩니다.

#### 이식성 (Portability)

스킬은 Claude.ai, Claude Code 및 API에서 동일하게 작동합니다. 한 번 스킬을 만들면 스킬이 필요로 하는 종속성을 환경이 지원하는 한 수정 없이 모든 환경에서 작동합니다.

### MCP 빌더를 위한: 스킬 + 커넥터

> 💡 MCP 없이 독립형 스킬을 구축하는 경우? 기획 및 설계로 건너뛰세요 - 나중에 언제든지 여기로 돌아올 수 있습니다.

이미 작동하는 MCP 서버가 있다면, 어려운 부분은 완료된 것입니다. 스킬은 그 위에 있는 지식 계층으로 - 이미 알고 있는 워크플로우와 모범 사례를 캡처하여 Claude가 일관되게 적용할 수 있도록 합니다.

#### 주방 비유

**MCP는 전문 주방을 제공합니다**: 도구, 재료, 장비에 대한 접근.

**스킬은 레시피를 제공합니다**: 가치 있는 것을 만드는 방법에 대한 단계별 지침.

함께, 사용자가 모든 단계를 직접 파악하지 않고도 복잡한 작업을 수행할 수 있게 합니다.

#### 함께 작동하는 방식

| MCP (연결성) | 스킬 (지식) |
|-------------|-----------|
| Claude를 서비스에 연결 (Notion, Asana, Linear 등) | Claude에게 서비스를 효과적으로 사용하는 방법을 가르침 |
| 실시간 데이터 접근 및 도구 호출 제공 | 워크플로우와 모범 사례 캡처 |
| Claude가 할 수 있는 것 | Claude가 해야 하는 방법 |

#### MCP 사용자에게 중요한 이유

**스킬 없이:**
* 사용자가 MCP를 연결하지만 다음에 무엇을 해야 할지 모름
* "통합으로 X를 어떻게 하나요"라는 지원 티켓
* 매 대화가 처음부터 시작
* 사용자마다 다르게 프롬프트하기 때문에 일관성 없는 결과
* 실제 문제가 워크플로우 가이드인데 사용자가 커넥터를 비난

**스킬과 함께:**
* 필요할 때 자동으로 활성화되는 사전 구축된 워크플로우
* 일관되고 안정적인 도구 사용
* 모든 상호작용에 내장된 모범 사례
* 통합에 대한 낮은 학습 곡선

---

## 3. 기획 및 설계

### 유스케이스로 시작하기

코드를 작성하기 전에, 스킬이 가능하게 해야 하는 2-3개의 구체적인 유스케이스를 식별하세요.

**좋은 유스케이스 정의:**

```
Use Case: 프로젝트 스프린트 계획
Trigger: 사용자가 "이 스프린트 계획 도와줘" 또는 "스프린트 작업 생성해줘"라고 말함
Steps:
1. Linear에서 현재 프로젝트 상태 가져오기 (MCP를 통해)
2. 팀 속도와 용량 분석
3. 작업 우선순위 제안
4. 적절한 레이블과 추정치로 Linear에 작업 생성
Result: 작업이 생성된 완전히 계획된 스프린트
```

**스스로에게 물어보세요:**
* 사용자가 무엇을 달성하고 싶어하는가?
* 이를 위해 어떤 다단계 워크플로우가 필요한가?
* 어떤 도구가 필요한가 (내장 또는 MCP)?
* 어떤 도메인 지식이나 모범 사례를 내장해야 하는가?

### 일반적인 스킬 유스케이스 카테고리

Anthropic에서는 세 가지 일반적인 유스케이스를 관찰했습니다:

#### 카테고리 1: 문서 및 자산 생성

**용도**: 문서, 프레젠테이션, 앱, 디자인, 코드 등을 포함한 일관되고 고품질의 출력물 생성.

*실제 예시: frontend-design 스킬 (docx, pptx, xlsx, ppt용 스킬도 참조)*

"높은 디자인 품질로 독특하고 프로덕션급 프론트엔드 인터페이스를 생성합니다. 웹 컴포넌트, 페이지, 아티팩트, 포스터 또는 애플리케이션을 구축할 때 사용하세요."

**핵심 기술:**
* 내장된 스타일 가이드 및 브랜드 표준
* 일관된 출력을 위한 템플릿 구조
* 최종화 전 품질 체크리스트
* 외부 도구 불필요 - Claude의 내장 기능 사용

#### 카테고리 2: 워크플로우 자동화

**용도**: 여러 MCP 서버 간 조정을 포함하여 일관된 방법론의 이점을 얻는 다단계 프로세스.

*실제 예시: skill-creator 스킬*

"새로운 스킬 생성을 위한 대화형 가이드. 유스케이스 정의, 프론트매터 생성, 지침 작성 및 검증을 통해 사용자를 안내합니다."

**핵심 기술:**
* 검증 게이트가 있는 단계별 워크플로우
* 일반적인 구조를 위한 템플릿
* 내장된 검토 및 개선 제안
* 반복적 개선 루프

#### 카테고리 3: MCP 강화

**용도**: MCP 서버가 제공하는 도구 접근을 강화하는 워크플로우 가이드.

*실제 예시: sentry-code-review 스킬 (Sentry 제공)*

"Sentry의 MCP 서버를 통해 Sentry의 오류 모니터링 데이터를 사용하여 GitHub Pull Request에서 감지된 버그를 자동으로 분석하고 수정합니다."

**핵심 기술:**
* 여러 MCP 호출을 순서대로 조정
* 도메인 전문 지식 내장
* 사용자가 달리 지정해야 할 컨텍스트 제공
* 일반적인 MCP 문제에 대한 오류 처리

### 성공 기준 정의

**스킬이 작동하는지 어떻게 알 수 있을까요?**

이것들은 목표 기준입니다 - 정확한 임계값이 아닌 대략적인 벤치마크입니다. 엄격함을 목표로 하되 느낌 기반 평가 요소가 있다는 것을 받아들이세요. 우리는 더 강력한 측정 가이드와 도구를 적극적으로 개발하고 있습니다.

**정량적 지표:**

* 스킬이 관련 쿼리의 90%에서 트리거됨
  - *측정 방법*: 스킬을 트리거해야 하는 10-20개의 테스트 쿼리를 실행합니다. 명시적 호출이 필요한 경우와 자동으로 로드되는 횟수를 추적합니다.
* X번의 도구 호출로 워크플로우 완료
  - *측정 방법*: 스킬을 활성화한 경우와 하지 않은 경우 동일한 작업을 비교합니다. 도구 호출과 소비된 총 토큰을 계산합니다.
* 워크플로우당 0개의 실패한 API 호출
  - *측정 방법*: 테스트 실행 중 MCP 서버 로그를 모니터링합니다. 재시도율과 오류 코드를 추적합니다.

**정성적 지표:**

* 사용자가 다음 단계에 대해 Claude에게 프롬프트할 필요가 없음
  - *평가 방법*: 테스트 중 리디렉션하거나 명확히 해야 하는 빈도를 기록합니다. 베타 사용자에게 피드백을 요청합니다.
* 사용자 수정 없이 워크플로우 완료
  - *평가 방법*: 동일한 요청을 3-5회 실행합니다. 구조적 일관성과 품질에 대해 출력을 비교합니다.
* 세션 간 일관된 결과
  - *평가 방법*: 새 사용자가 최소한의 안내로 첫 시도에서 작업을 수행할 수 있는가?

### 기술적 요구 사항

#### 파일 구조

```
your-skill-name/
├── SKILL.md              # 필수 - 메인 스킬 파일
├── scripts/              # 선택 - 실행 가능한 코드
│   ├── process_data.py   # 예시
│   └── validate.sh       # 예시
├── references/           # 선택 - 문서
│   ├── api-guide.md      # 예시
│   └── examples/         # 예시
└── assets/               # 선택 - 템플릿 등
    └── report-template.md # 예시
```

#### 중요한 규칙

**SKILL.md 이름 지정:**
* 정확히 SKILL.md여야 함 (대소문자 구분)
* 다른 변형은 허용되지 않음 (SKILL.MD, skill.md 등)

**스킬 폴더 이름 지정:**
* 케밥 케이스 사용: `notion-project-setup` ✅
* 공백 없음: `Notion Project Setup` ❌
* 언더스코어 없음: `notion_project_setup` ❌
* 대문자 없음: `NotionProjectSetup` ❌

**README.md 없음:**
* 스킬 폴더 내에 README.md를 포함하지 마세요
* 모든 문서는 SKILL.md 또는 references/에 넣으세요
* 참고: GitHub을 통해 배포할 때는 인간 사용자를 위해 저장소 수준의 README가 여전히 필요합니다 — 배포 및 공유를 참조하세요.

### YAML 프론트매터: 가장 중요한 부분

YAML 프론트매터는 Claude가 스킬을 로드할지 결정하는 방법입니다. 이것을 제대로 작성하세요.

**최소 필수 형식**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

이것이 시작하는 데 필요한 전부입니다.

#### 필드 요구 사항

**name (필수):**
* 케밥 케이스만
* 공백이나 대문자 없음
* 폴더 이름과 일치해야 함

**description (필수):**
* 반드시 둘 다 포함해야 함:
  - 스킬이 하는 것
  - 언제 사용하는지 (트리거 조건)
* 1024자 미만
* XML 태그 없음 (< 또는 >)
* 사용자가 말할 수 있는 특정 작업 포함
* 관련이 있다면 파일 유형 언급

**license (선택):**
* 스킬을 오픈 소스로 만드는 경우 사용
* 일반적: MIT, Apache-2.0

**compatibility (선택):**
* 1-500자
* 환경 요구 사항 표시: 예: 의도된 제품, 필요한 시스템 패키지, 네트워크 접근 필요성 등.

**metadata (선택):**
* 모든 사용자 정의 키-값 쌍
* 권장: author, version, mcp-server
* 예시:
```yaml
metadata:
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
```

#### 보안 제한

**프론트매터에서 금지:**
* XML 꺾쇠 괄호 (< >)
* 이름에 "claude" 또는 "anthropic"이 있는 스킬 (예약됨)

**이유**: 프론트매터가 Claude의 시스템 프롬프트에 나타납니다. 악성 콘텐츠가 지침을 주입할 수 있습니다.

### 효과적인 스킬 작성

#### description 필드

Anthropic의 엔지니어링 블로그에 따르면: "이 메타데이터는...전체 내용을 컨텍스트에 로드하지 않고도 Claude가 각 스킬을 언제 사용해야 하는지 알 수 있도록 충분한 정보를 제공합니다." 이것이 점진적 공개의 첫 번째 수준입니다.

**구조:**

```
[무엇을 하는지] + [언제 사용하는지] + [핵심 기능]
```

**좋은 description 예시:**

```yaml
# 좋음 - 구체적이고 실행 가능
description: Figma 디자인 파일을 분석하고 개발자 핸드오프 문서를 생성합니다.
사용자가 .fig 파일을 업로드하거나 "디자인 스펙", "컴포넌트 문서", "디자인-코드 핸드오프"를
요청할 때 사용하세요.

# 좋음 - 트리거 문구 포함
description: 스프린트 계획, 작업 생성, 상태 추적을 포함한 Linear 프로젝트 워크플로우를
관리합니다. 사용자가 "스프린트", "Linear 작업", "프로젝트 계획"을 언급하거나
"티켓 생성"을 요청할 때 사용하세요.

# 좋음 - 명확한 가치 제안
description: PayFlow를 위한 엔드-투-엔드 고객 온보딩 워크플로우. 계정 생성,
결제 설정, 구독 관리를 처리합니다. 사용자가 "새 고객 온보딩", "구독 설정",
"PayFlow 계정 생성"이라고 말할 때 사용하세요.
```

**나쁜 description 예시:**

```yaml
# 너무 모호함
description: 프로젝트를 도와줍니다.

# 트리거 없음
description: 정교한 다중 페이지 문서 시스템을 생성합니다.

# 너무 기술적, 사용자 트리거 없음
description: 계층적 관계를 가진 Project 엔티티 모델을 구현합니다.
```

#### 메인 지침 작성

프론트매터 이후, 마크다운으로 실제 지침을 작성합니다.

**권장 구조:**

*이 템플릿을 스킬에 맞게 조정하세요. 괄호 안의 섹션을 특정 내용으로 교체하세요.*

```markdown
---
name: your-skill
description: [...]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```
Expected output: [describe what success looks like]

(Add more steps as needed)

## Examples

### Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link

(Add more examples as needed)

## Troubleshooting

### Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]

(Add more error cases as needed)
```

#### 지침 작성 모범 사례

**구체적이고 실행 가능하게**

✅ **좋음:**
```
`python scripts/validate.py --input {filename}`을 실행하여 데이터 형식을 확인합니다.
검증이 실패하면 일반적인 문제는 다음과 같습니다:
- 필수 필드 누락 (CSV에 추가)
- 잘못된 날짜 형식 (YYYY-MM-DD 사용)
```

❌ **나쁨:**
```
진행하기 전에 데이터를 검증합니다.
```

**오류 처리 포함**

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**번들된 리소스 명확히 참조**

```
쿼리를 작성하기 전에 `references/api-patterns.md`를 참조하세요:
- 속도 제한 가이드
- 페이지네이션 패턴
- 오류 코드 및 처리
```

**점진적 공개 사용**

SKILL.md를 핵심 지침에 집중하세요. 상세 문서는 `references/`로 이동하고 링크하세요. (3단계 시스템이 어떻게 작동하는지는 핵심 설계 원칙을 참조하세요.)

---

## 4. 테스트 및 반복 개선

스킬은 필요에 따라 다양한 수준의 엄격함으로 테스트할 수 있습니다:

* **Claude.ai에서 수동 테스트** - 직접 쿼리를 실행하고 동작을 관찰합니다. 빠른 반복, 설정 불필요.
* **Claude Code에서 스크립트 테스트** - 변경 사항에 대해 반복 가능한 검증을 위해 테스트 케이스를 자동화합니다.
* **skills API를 통한 프로그래매틱 테스트** - 정의된 테스트 세트에 대해 체계적으로 실행되는 평가 스위트를 구축합니다.

스킬의 품질 요구 사항과 가시성에 맞는 접근 방식을 선택하세요. 소규모 팀에서 내부적으로 사용하는 스킬은 수천 명의 엔터프라이즈 사용자에게 배포되는 것과 다른 테스트 요구 사항이 있습니다.

> **Pro Tip: 확장하기 전에 단일 작업에서 반복하기**

가장 효과적인 스킬 제작자는 Claude가 성공할 때까지 단일 도전적인 작업에서 반복한 다음, 성공한 접근 방식을 스킬로 추출한다는 것을 발견했습니다. 이는 Claude의 컨텍스트 내 학습을 활용하고 광범위한 테스트보다 더 빠른 신호를 제공합니다. 작동하는 기반이 있으면 커버리지를 위해 여러 테스트 케이스로 확장하세요.

### 권장 테스트 접근 방식

초기 경험을 바탕으로 효과적인 스킬 테스트는 일반적으로 세 가지 영역을 다룹니다:

#### 1. 트리거 테스트

**목표**: 스킬이 올바른 시점에 로드되는지 확인합니다.

**테스트 케이스:**
* ✅ 명확한 작업에서 트리거됨
* ✅ 바꿔 말한 요청에서 트리거됨
* ❌ 관련 없는 주제에서 트리거되지 않음

**예시 테스트 스위트:**

```
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
- "Create a spreadsheet" (unless ProjectHub skill handles sheets)
```

#### 2. 기능 테스트

**목표**: 스킬이 올바른 출력을 생성하는지 확인합니다.

**테스트 케이스:**
* 유효한 출력 생성
* API 호출 성공
* 오류 처리 작동
* 에지 케이스 커버

**예시:**

```
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
  - Project created in ProjectHub
  - 5 tasks created with correct properties
  - All tasks linked to project
  - No API errors
```

#### 3. 성능 비교

**목표**: 스킬이 기준선 대비 결과를 개선하는지 증명합니다.

성공 기준 정의의 지표를 사용하세요. 비교는 다음과 같을 수 있습니다.

**기준선 비교:**

```
Without skill:
- User provides instructions each time
- 15 back-and-forth messages
- 3 failed API calls requiring retry
- 12,000 tokens consumed

With skill:
- Automatic workflow execution
- 2 clarifying questions only
- 0 failed API calls
- 6,000 tokens consumed
```

### skill-creator 스킬 사용

skill-creator 스킬 - Claude.ai에서 플러그인 디렉토리를 통해 사용 가능하거나 Claude Code용 다운로드 - 은 스킬을 구축하고 반복하는 데 도움이 될 수 있습니다. MCP 서버가 있고 상위 2-3개의 워크플로우를 알고 있다면, 단일 세션에서 기능적인 스킬을 구축하고 테스트할 수 있습니다 - 종종 15-30분 내에.

**스킬 생성:**
* 자연어 설명에서 스킬 생성
* 프론트매터가 있는 적절한 형식의 SKILL.md 생성
* 트리거 문구 및 구조 제안

**스킬 검토:**
* 일반적인 문제 (모호한 설명, 누락된 트리거, 구조적 문제) 플래그
* 잠재적인 과잉/과소 트리거 위험 식별
* 스킬의 명시된 목적에 따라 테스트 케이스 제안

**반복적 개선:**
* 스킬을 사용하고 에지 케이스나 실패를 만난 후, 해당 예시를 skill-creator로 가져오세요
* 예시: "이 채팅에서 식별된 문제와 해결책을 사용하여 스킬이 [특정 에지 케이스]를 처리하는 방법을 개선하세요"

**사용하려면:**

```
"Use the skill-creator skill to help me build a skill for [your use case]"
```

*참고: skill-creator는 스킬을 설계하고 개선하는 데 도움이 되지만 자동화된 테스트 스위트를 실행하거나 정량적 평가 결과를 생성하지는 않습니다.*

### 피드백 기반 반복

스킬은 살아있는 문서입니다. 다음을 기반으로 반복할 계획을 세우세요:

**과소 트리거 신호:**
* 스킬이 로드되어야 할 때 로드되지 않음
* 사용자가 수동으로 활성화
* 언제 사용해야 하는지에 대한 지원 질문

> **해결책**: description에 더 많은 세부 사항과 뉘앙스를 추가하세요 - 특히 기술 용어에 대한 키워드를 포함할 수 있습니다

**과잉 트리거 신호:**
* 관련 없는 쿼리에 스킬이 로드됨
* 사용자가 비활성화
* 목적에 대한 혼란

> **해결책**: 부정적 트리거를 추가하고, 더 구체적으로 작성

**실행 문제:**
* 일관성 없는 결과
* API 호출 실패
* 사용자 수정 필요

> **해결책**: 지침 개선, 오류 처리 추가

---

## 5. 배포 및 공유

스킬은 MCP 통합을 더 완벽하게 만듭니다. 사용자가 커넥터를 비교할 때, 스킬이 있는 것이 가치에 더 빠른 경로를 제공하여 MCP 전용 대안보다 우위를 제공합니다.

### 현재 배포 모델 (2026년 1월)

**개별 사용자가 스킬을 얻는 방법:**
1. 스킬 폴더 다운로드
2. 폴더를 zip으로 압축 (필요한 경우)
3. Settings > Capabilities > Skills를 통해 Claude.ai에 업로드
4. 또는 Claude Code skills 디렉토리에 배치

**조직 수준 스킬:**
* 관리자가 워크스페이스 전체에 스킬 배포 가능 (2025년 12월 18일 출시)
* 자동 업데이트
* 중앙 집중식 관리

### 오픈 표준

우리는 Agent Skills를 오픈 표준으로 게시했습니다. MCP와 마찬가지로, 스킬은 도구와 플랫폼 간에 이식 가능해야 한다고 믿습니다 - Claude를 사용하든 다른 AI 플랫폼을 사용하든 동일한 스킬이 작동해야 합니다. 그러나 일부 스킬은 특정 플랫폼의 기능을 최대한 활용하도록 설계되었습니다; 저자는 스킬의 compatibility 필드에 이를 기록할 수 있습니다. 우리는 표준에 대해 생태계 구성원들과 협력해 왔으며, 초기 채택에 흥분하고 있습니다.

### API를 통한 스킬 사용

프로그래매틱 유스케이스 - 스킬을 활용하는 애플리케이션, 에이전트 또는 자동화된 워크플로우 구축 - 의 경우, API는 스킬 관리 및 실행에 대한 직접 제어를 제공합니다.

**핵심 기능:**
* 스킬 나열 및 관리를 위한 `/v1/skills` 엔드포인트
* `container.skills` 파라미터를 통해 Messages API 요청에 스킬 추가
* Claude Console을 통한 버전 관리 및 관리
* 맞춤형 에이전트 구축을 위한 Claude Agent SDK와 함께 작동

**API vs Claude.ai에서 스킬을 사용할 때:**

| 유스케이스 | 최적 환경 |
|----------|---------|
| 스킬과 직접 상호작용하는 최종 사용자 | Claude.ai / Claude Code |
| 개발 중 수동 테스트 및 반복 | Claude.ai / Claude Code |
| 개별적, 임시 워크플로우 | Claude.ai / Claude Code |
| 프로그래매틱으로 스킬을 사용하는 애플리케이션 | API |
| 대규모 프로덕션 배포 | API |
| 자동화된 파이프라인 및 에이전트 시스템 | API |

*참고: API의 스킬은 스킬이 실행하는 데 필요한 안전한 환경을 제공하는 Code Execution Tool 베타가 필요합니다.*

구현 세부 사항은 다음을 참조하세요:
* Skills API Quickstart
* Create Custom skills
* Skills in the Agent SDK

### 오늘 권장되는 접근 방식

공개 저장소, 명확한 README (인간 방문자용 — 이것은 README.md를 포함하지 않아야 하는 스킬 폴더와 별개입니다), 스크린샷이 있는 예시 사용법으로 GitHub에 스킬을 호스팅하는 것으로 시작하세요. 그런 다음 스킬에 대한 링크, 둘을 함께 사용하는 것이 왜 가치 있는지 설명, 빠른 시작 가이드를 MCP 문서에 섹션으로 추가하세요.

**1. GitHub에 호스팅**
- 오픈 소스 스킬을 위한 공개 저장소
- 설치 지침이 있는 명확한 README
- 예시 사용법 및 스크린샷

**2. MCP 저장소에 문서화**
- MCP 문서에서 스킬에 대한 링크
- 둘을 함께 사용하는 가치 설명
- 빠른 시작 가이드 제공

**3. 설치 가이드 생성**

```markdown
## Installing the [Your Service] skill

1. Download the skill:
   - Clone repo: `git clone https://github.com/yourcompany/skills`
   - Or download ZIP from Releases

2. Install in Claude:
   - Open Claude.ai > Settings > skills
   - Click "Upload skill"
   - Select the skill folder (zipped)

3. Enable the skill:
   - Toggle on the [Your Service] skill
   - Ensure your MCP server is connected

4. Test:
   - Ask Claude: "Set up a new project in [Your Service]"
```

### 스킬 포지셔닝

스킬을 어떻게 설명하느냐에 따라 사용자가 그 가치를 이해하고 실제로 시도할지가 결정됩니다. README, 문서 또는 마케팅에서 스킬에 대해 작성할 때 이러한 원칙을 명심하세요.

**기능이 아닌 결과에 집중:**

✅ **좋음:**
```
"ProjectHub 스킬을 사용하면 팀이 수동 설정에 30분을 소비하는 대신
페이지, 데이터베이스, 템플릿을 포함한 완전한 프로젝트 워크스페이스를
몇 초 만에 설정할 수 있습니다."
```

❌ **나쁨:**
```
"ProjectHub 스킬은 MCP 서버 도구를 호출하는 YAML 프론트매터와
마크다운 지침을 포함하는 폴더입니다."
```

**MCP + 스킬 스토리 강조:**

```
"우리의 MCP 서버는 Claude에게 Linear 프로젝트에 대한 접근을 제공합니다.
우리의 스킬은 Claude에게 팀의 스프린트 계획 워크플로우를 가르칩니다.
함께, AI 기반 프로젝트 관리를 가능하게 합니다."
```

---

## 6. 패턴 및 문제 해결

이러한 패턴은 초기 채택자와 내부 팀이 만든 스킬에서 나타났습니다. 이들은 처방적 템플릿이 아닌 효과적으로 작동하는 것으로 본 일반적인 접근 방식을 나타냅니다.

### 접근 방식 선택: 문제 우선 vs. 도구 우선

Home Depot처럼 생각하세요. "주방 캐비닛을 고쳐야 해요"라는 문제를 가지고 들어가면 직원이 올바른 도구를 알려줄 수 있습니다. 또는 새 드릴을 선택하고 특정 작업에 어떻게 사용하는지 물어볼 수 있습니다.

스킬도 마찬가지입니다:

* **문제 우선**: "프로젝트 워크스페이스를 설정해야 해요" → 스킬이 올바른 순서로 올바른 MCP 호출을 조정합니다. 사용자가 결과를 설명하면; 스킬이 도구를 처리합니다.
* **도구 우선**: "Notion MCP가 연결되어 있어요" → 스킬이 Claude에게 최적의 워크플로우와 모범 사례를 가르칩니다. 사용자는 접근 권한이 있고; 스킬이 전문 지식을 제공합니다.

대부분의 스킬은 한 방향으로 기울어집니다. 유스케이스에 맞는 프레이밍을 아는 것이 아래의 올바른 패턴을 선택하는 데 도움이 됩니다.

### 패턴 1: 순차적 워크플로우 오케스트레이션

**사용 시점**: 사용자가 특정 순서로 다단계 프로세스가 필요할 때.

**예시 구조:**

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**핵심 기술:**
* 명시적 단계 순서
* 단계 간 종속성
* 각 단계에서 검증
* 실패 시 롤백 지침

### 패턴 2: 다중 MCP 조정

**사용 시점**: 워크플로우가 여러 서비스에 걸쳐 있을 때.

**예시: 디자인-개발 핸드오프**

```markdown
### Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest

### Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets
3. Generate shareable links

### Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to tasks
3. Assign to engineering team

### Phase 4: Notification (Slack MCP)
1. Post handoff summary to #engineering
2. Include asset links and task references
```

**핵심 기술:**
* 명확한 단계 분리
* MCP 간 데이터 전달
* 다음 단계로 이동하기 전 검증
* 중앙 집중식 오류 처리

### 패턴 3: 반복적 개선

**사용 시점**: 출력 품질이 반복을 통해 개선될 때.

**예시: 보고서 생성**

```markdown
## Iterative Report Creation

### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors

### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

### Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**핵심 기술:**
* 명시적 품질 기준
* 반복적 개선
* 검증 스크립트
* 언제 반복을 멈출지 알기

### 패턴 4: 컨텍스트 인식 도구 선택

**사용 시점**: 컨텍스트에 따라 동일한 결과, 다른 도구.

**예시: 파일 저장**

```markdown
## Smart File Storage

### Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

### Execute Storage
Based on decision:
- Call appropriate MCP tool
- Apply service-specific metadata
- Generate access link

### Provide Context to User
Explain why that storage was chosen
```

**핵심 기술:**
* 명확한 결정 기준
* 대체 옵션
* 선택에 대한 투명성

### 패턴 5: 도메인 특화 인텔리전스

**사용 시점**: 스킬이 도구 접근을 넘어 전문 지식을 추가할 때.

**예시: 금융 컴플라이언스**

```markdown
## Payment Processing with Compliance

### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

### Processing
IF compliance passed:
   - Call payment processing MCP tool
   - Apply appropriate fraud checks
   - Process transaction
ELSE:
   - Flag for review
   - Create compliance case

### Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**핵심 기술:**
* 로직에 내장된 도메인 전문 지식
* 행동 전 컴플라이언스
* 포괄적 문서화
* 명확한 거버넌스

### 문제 해결

#### 스킬이 업로드되지 않음

**오류: "Could not find SKILL.md in uploaded folder"**

원인: 파일 이름이 정확히 SKILL.md가 아님

해결책:
* SKILL.md로 이름 변경 (대소문자 구분)
* `ls -la`로 확인하면 SKILL.md가 표시되어야 함

**오류: "Invalid frontmatter"**

원인: YAML 형식 문제

일반적인 실수:
```yaml
# 잘못됨 - 구분자 누락
name: my-skill
description: Does things

# 잘못됨 - 닫히지 않은 따옴표
name: my-skill
description: "Does things

# 올바름
---
name: my-skill
description: Does things
---
```

**오류: "Invalid skill name"**

원인: 이름에 공백이나 대문자가 있음

```yaml
# 잘못됨
name: My Cool Skill

# 올바름
name: my-cool-skill
```

#### 스킬이 트리거되지 않음

**증상**: 스킬이 자동으로 로드되지 않음

**해결:**

description 필드를 수정하세요. 좋은/나쁜 예시는 description 필드를 참조하세요.

빠른 체크리스트:
* 너무 일반적인가? ("프로젝트를 도와줍니다"는 작동하지 않음)
* 사용자가 실제로 말할 트리거 문구를 포함하는가?
* 해당되는 경우 관련 파일 유형을 언급하는가?

**디버깅 접근 방식:**

Claude에게 물어보세요: "언제 [스킬 이름] 스킬을 사용하겠어?" Claude가 description을 다시 인용할 것입니다. 누락된 내용에 따라 조정하세요.

#### 스킬이 너무 자주 트리거됨

**증상**: 관련 없는 쿼리에 스킬이 로드됨

**해결책:**

1. **부정적 트리거 추가**
```yaml
description: CSV 파일에 대한 고급 데이터 분석. 통계 모델링, 회귀,
클러스터링에 사용하세요. 간단한 데이터 탐색에는 사용하지 마세요
(대신 data-viz 스킬 사용).
```

2. **더 구체적으로**
```yaml
# 너무 넓음
description: Processes documents

# 더 구체적
description: Processes PDF legal documents for contract review
```

3. **범위 명확화**
```yaml
description: PayFlow payment processing for e-commerce. Use
specifically for online payment workflows, not for general
financial queries.
```

#### MCP 연결 문제

**증상**: 스킬은 로드되지만 MCP 호출이 실패함

**체크리스트:**

1. **MCP 서버 연결 확인**
   - Claude.ai: Settings > Extensions > [Your Service]
   - "Connected" 상태가 표시되어야 함

2. **인증 확인**
   - API 키가 유효하고 만료되지 않음
   - 적절한 권한/범위 부여
   - OAuth 토큰 갱신

3. **MCP 독립적으로 테스트**
   - Claude에게 MCP를 직접 호출하도록 요청 (스킬 없이)
   - "Use [Service] MCP to fetch my projects"
   - 이것이 실패하면 문제는 스킬이 아닌 MCP

4. **도구 이름 확인**
   - 스킬이 올바른 MCP 도구 이름을 참조
   - MCP 서버 문서 확인
   - 도구 이름은 대소문자 구분

#### 지침이 따라지지 않음

**증상**: 스킬은 로드되지만 Claude가 지침을 따르지 않음

**일반적인 원인:**

1. **지침이 너무 장황함**
   - 지침을 간결하게 유지
   - 글머리 기호와 번호 목록 사용
   - 상세 참조는 별도 파일로 이동

2. **지침이 묻힘**
   - 중요한 지침을 맨 위에 배치
   - ## Important 또는 ## Critical 헤더 사용
   - 필요하면 핵심 포인트 반복

3. **모호한 언어**
```markdown
# 나쁨
Make sure to validate things properly

# 좋음
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

> **고급 기술**: 중요한 검증의 경우, 언어 지침에 의존하는 대신 프로그래매틱으로 검사를 수행하는 스크립트를 번들링하는 것을 고려하세요. 코드는 결정적입니다; 언어 해석은 그렇지 않습니다. 이 패턴의 예시는 Office 스킬을 참조하세요.

4. **모델 "게으름"** 명시적 격려 추가:
```markdown
## Performance Notes
- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
```

*참고: SKILL.md보다 사용자 프롬프트에 이것을 추가하는 것이 더 효과적입니다*

#### 대용량 컨텍스트 문제

**증상**: 스킬이 느려 보이거나 응답 품질 저하

**원인:**
* 스킬 내용이 너무 큼
* 동시에 활성화된 스킬이 너무 많음
* 점진적 공개 대신 모든 내용이 로드됨

**해결책:**

1. **SKILL.md 크기 최적화**
   - 상세 문서를 references/로 이동
   - 인라인 대신 참조로 링크
   - SKILL.md를 5,000 단어 미만으로 유지

2. **활성화된 스킬 줄이기**
   - 동시에 20-50개 이상의 스킬이 활성화되어 있는지 평가
   - 선택적 활성화 권장
   - 관련 기능을 위한 스킬 "팩" 고려

---

## 7. 리소스 및 참고 자료

첫 번째 스킬을 구축하는 경우, 모범 사례 가이드로 시작한 다음 필요에 따라 API 문서를 참조하세요.

### 공식 문서

**Anthropic 리소스:**
* Best Practices Guide
* Skills Documentation
* API Reference
* MCP Documentation

**블로그 포스트:**
* Introducing Agent Skills
* Engineering Blog: Equipping Agents for the Real World
* Skills Explained
* How to Create Skills for Claude
* Building Skills for Claude Code
* Improving Frontend Design through Skills

### 예시 스킬

**공개 스킬 저장소:**
* GitHub: anthropics/skills
* 커스터마이징할 수 있는 Anthropic이 만든 스킬 포함

### 도구 및 유틸리티

**skill-creator 스킬:**
* Claude.ai에 내장되어 있고 Claude Code에서 사용 가능
* 설명에서 스킬 생성 가능
* 검토 및 권장 사항 제공
* 사용: "Help me build a skill using skill-creator"

**검증:**
* skill-creator가 스킬을 평가할 수 있음
* 요청: "Review this skill and suggest improvements"

### 지원 받기

**기술적 질문:**
* 일반 질문: Claude Developers Discord 커뮤니티 포럼

**버그 보고:**
* GitHub Issues: anthropics/skills/issues
* 포함: 스킬 이름, 오류 메시지, 재현 단계

---

## 참조 A: 빠른 체크리스트

스킬을 업로드 전후에 검증하기 위해 이 체크리스트를 사용하세요. 더 빠르게 시작하려면 skill-creator 스킬을 사용하여 첫 번째 초안을 생성한 다음 이 목록을 통해 누락된 것이 없는지 확인하세요.

### 시작하기 전

- [ ] 2-3개의 구체적인 유스케이스 식별
- [ ] 도구 식별 (내장 또는 MCP)
- [ ] 이 가이드 및 예시 스킬 검토
- [ ] 폴더 구조 계획

### 개발 중

- [ ] 폴더 이름이 케밥 케이스
- [ ] SKILL.md 파일 존재 (정확한 철자)
- [ ] YAML 프론트매터에 --- 구분자 있음
- [ ] name 필드: 케밥 케이스, 공백 없음, 대문자 없음
- [ ] description에 WHAT과 WHEN 포함
- [ ] 어디에도 XML 태그 (< >) 없음
- [ ] 지침이 명확하고 실행 가능함
- [ ] 오류 처리 포함
- [ ] 예시 제공
- [ ] 참조가 명확히 링크됨

### 업로드 전

- [ ] 명확한 작업에서 트리거 테스트
- [ ] 바꿔 말한 요청에서 트리거 테스트
- [ ] 관련 없는 주제에서 트리거되지 않는지 확인
- [ ] 기능 테스트 통과
- [ ] 도구 통합 작동 (해당되는 경우)
- [ ] .zip 파일로 압축

### 업로드 후

- [ ] 실제 대화에서 테스트
- [ ] 과소/과잉 트리거 모니터링
- [ ] 사용자 피드백 수집
- [ ] description 및 지침 반복 개선
- [ ] 메타데이터에서 버전 업데이트

---

## 참조 B: YAML 프론트매터

### 필수 필드

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### 모든 선택 필드

```yaml
name: skill-name
description: [required description]
license: MIT # 선택: 오픈 소스용 라이선스
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch" # 선택: 도구 접근 제한
metadata: # 선택: 사용자 정의 필드
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
```

### 보안 참고 사항

**허용:**
* 모든 표준 YAML 유형 (문자열, 숫자, 불리언, 리스트, 객체)
* 사용자 정의 메타데이터 필드
* 긴 설명 (최대 1024자)

**금지:**
* XML 꺾쇠 괄호 (< >) - 보안 제한
* YAML에서 코드 실행 (안전한 YAML 파싱 사용)
* "claude" 또는 "anthropic" 접두사가 있는 스킬 이름 (예약됨)

---

## 참조 C: 전체 스킬 예시

이 가이드의 패턴을 보여주는 완전한 프로덕션 준비 스킬:

* **Document Skills** - PDF, DOCX, PPTX, XLSX 생성
* **Example Skills** - 다양한 워크플로우 패턴
* **Partner Skills Directory** - Asana, Atlassian, Canva, Figma, Sentry, Zapier 등 다양한 파트너의 스킬 보기

이 저장소는 최신 상태를 유지하며 여기에서 다루는 것 이상의 추가 예시를 포함합니다. 복제하고, 유스케이스에 맞게 수정하고, 템플릿으로 사용하세요.

---

**Claude**
claude.ai
