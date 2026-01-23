# Anthropic 공식 가이드라인

> **출처**: docs.anthropic.com, console.anthropic.com, anthropic.com/engineering
> **업데이트**: 2025년 1월 (Tavily 검색 기반)

---

## 1. 할루시네이션 방지 (Let Claude Say "I Don't Know")

> 출처: docs.anthropic.com/claude/docs/let-claude-say-i-dont-know

### 기본 전략

```
**핵심 원칙**:
- Claude가 "I don't know"라고 말할 수 있게 허용
- 불확실한 추측보다 정직한 모름이 나음
- 제공된 문서/코드 범위 내에서만 답변
```

### 긴 문서 처리 (20K+ 토큰)

```markdown
**2단계 접근법**:
1. 먼저 관련 인용문 추출
2. 인용문 기반으로 답변 생성

예시 프롬프트:
"다음 문서에서 [질문]과 관련된 직접 인용문을 먼저 찾아주세요.
인용문을 찾을 수 없다면 '관련 정보를 찾을 수 없습니다'라고 말해주세요."
```

### 고급 검증 기법

| 기법 | 설명 | 적용 상황 |
|------|------|----------|
| **Chain-of-thought** | 단계별 추론으로 자기 검증 | 복잡한 논리적 질문 |
| **Best-of-N** | 여러 답변 생성 후 일관성 확인 | 중요한 결정 |
| **직접 인용** | 원본에서 관련 부분 추출 | 긴 문서 분석 |
| **외부 지식 제한** | 제공된 자료만 사용하도록 명시 | 정확성 필수 |

---

## 2. 에이전트 코딩 베스트 프랙티스

> 출처: console.anthropic.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices

### 코드 탐색 필수 규칙

```
ALWAYS read and understand relevant files before proposing code edits.
Do not speculate about code you have not inspected.
If the user references a specific file/path, you MUST open and inspect it
before explaining or proposing fixes.
Be rigorous and persistent in searching code for key facts.
Thoroughly review the style, conventions, and abstractions of the codebase
before implementing new features or abstractions.
```

### 할루시네이션 최소화 규칙

```
Never speculate about code you have not opened.
If the user references a specific file, you MUST read the file before answering.
Make sure to investigate and read relevant files BEFORE answering questions
about the codebase.
Never make any claims about code before investigating unless you are certain
of the correct answer - give grounded and hallucination-free answers.
```

### 체크리스트

- [ ] 파일 열기 전에 코드 내용 추측하지 않음
- [ ] 사용자가 언급한 파일은 반드시 먼저 읽기
- [ ] 코드베이스 스타일/컨벤션 파악 후 구현
- [ ] 확실하지 않으면 "확인 필요"라고 말하기
- [ ] 근거 없는 주장 절대 금지

---

## 3. 효과적인 에이전트 구축

> 출처: anthropic.com/research/building-effective-agents

### 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **단순성 유지** | 복잡한 프레임워크 대신 간단한 구성 선호 |
| **투명성** | 계획 단계를 명시적으로 표시 |
| **ACI 설계** | Agent-Computer Interface를 신중하게 설계 |
| **도구 품질** | 도구 문서화 및 철저한 테스트 |

### 에이전트 패턴

```
1. 프롬프트 체이닝: 여러 Claude 호출을 연결
2. 라우팅: 입력에 따라 적절한 처리 경로 선택
3. 병렬화: 독립적 작업 동시 실행
4. 오케스트레이터-워커: 복잡한 작업 분해
5. 평가자-최적화자: 피드백 루프로 품질 개선
```

---

## 4. 컨텍스트 엔지니어링

> 출처: anthropic.com/engineering/claude-code-best-practices

### Just-in-Time 데이터 로딩

```
**핵심 전략**:
- 경량 식별자만 유지
- 런타임에 필요한 데이터 동적 로드
- 전체 데이터를 미리 로드하지 않음
```

### 진행 상황 추적

```markdown
**권장 패턴**:
- 진행 상황 추적 파일 유지 (예: claude-progress.txt)
- 세션 간 컨텍스트 연속성 보장
- compact 발생 시 체크포인트에서 복구
```

### 컨텍스트 창 관리

```
1. 중요한 정보 우선 배치
2. 불필요한 반복 제거
3. 요약으로 긴 대화 압축
4. 관련성 높은 정보 선별
```

---

## 5. 효과적인 도구 작성

> 출처: anthropic.com/engineering

### 도구 이름 규칙

```
**좋은 예**:
- get_user_profile
- create_payment_intent
- search_documents

**나쁜 예**:
- func_12345
- do_thing
- process
```

### 네임스페이싱

```
도구가 많을 때:
- 카테고리별 그룹화
- 의미 있는 접두사 사용
- 예: user_*, payment_*, search_*
```

### Chain-of-thought 활성화

```
도구 설명에 사고 과정 유도:
"이 도구를 사용하기 전에 왜 이 도구가 필요한지,
어떤 매개변수가 적절한지 먼저 설명하세요."
```

---

## 6. Claude Code 내부 사용 사례 (Anthropic)

> 출처: anthropic.com/engineering/claude-code-best-practices

### Anthropic 내부 워크플로우

```
1. 온보딩에 Claude Code 활용
   - 새 팀원이 코드베이스 이해 가속화

2. Git 작업의 90%+ Claude로 처리
   - 커밋 메시지 생성
   - PR 설명 작성
   - 코드 리뷰 지원

3. 병렬 작업을 위한 git worktree 활용
   - 여러 기능을 동시에 개발
   - 컨텍스트 전환 최소화

4. Jupyter 노트북 작업
   - 데이터 분석
   - 실험적 코드 작성
```

---

## 적용 체크리스트

### 코드 작업 시

- [ ] 파일 읽기 전 추측 금지
- [ ] 스타일/컨벤션 파악 후 구현
- [ ] 확실하지 않으면 인정
- [ ] 근거 있는 답변만 제공

### 에이전트 설계 시

- [ ] 단순성 우선
- [ ] 계획 단계 명시적 표시
- [ ] 도구 품질 테스트
- [ ] 피드백 루프 구현

### 컨텍스트 관리 시

- [ ] Just-in-time 로딩 적용
- [ ] 진행 상황 파일 유지
- [ ] 불필요한 정보 제거
- [ ] 중요 정보 우선 배치

---

## 금지 사항

1. **절대 금지**: 열어보지 않은 파일에 대한 추측
2. **절대 금지**: 확인 없이 코드 구조 주장
3. **절대 금지**: 불확실한 정보를 확실한 것처럼 전달
4. **절대 금지**: 컨텍스트 부족한 상태에서 수정 제안
5. **절대 금지**: 에러 메시지 없이 "안 됩니다" 답변

---

## 참조 링크

- [Let Claude Say I Don't Know](https://docs.anthropic.com/claude/docs/let-claude-say-i-dont-know)
- [Claude 4 Best Practices](https://console.anthropic.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Building Effective Agents](https://anthropic.com/research/building-effective-agents)
- [Claude Code Best Practices](https://anthropic.com/engineering/claude-code-best-practices)
