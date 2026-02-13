---
name: toolkit:code-commit
description: 현재 변경사항을 분석하고 커밋 메시지를 생성합니다
allowed-tools: Bash, Read, AskUserQuestion
disable-model-invocation: true
---

# Commit Changes Command

현재 작업 디렉토리의 변경사항을 분석하고, 적절한 커밋 메시지를 생성하여 커밋을 수행합니다.

## 작업 순서

1. **Git 상태 확인**
   - `git status`로 변경된 파일 목록 확인
   - `git diff --cached` 또는 `git diff`로 변경 내용 확인

2. **변경사항 분석**
   - 수정된 파일들의 변경 내용 파악
   - 변경의 주요 목적과 범위 파악
   - 테스트 코드 포함 여부 확인

3. **Jira ticket key 확인**
   - 인자로 전달되지 않은 경우 `AskUserQuestion` 툴을 사용하여 Jira ticket key 입력받음
   - 질문 형식:
     - question: "이 커밋과 연관된 Jira 티켓 키를 입력해주세요"
     - header: "Jira 티켓"
     - 옵션 제공 불필요 (사용자가 직접 입력)

4. **커밋 메시지 생성**
   - 메시지 형식:
   ```
   [type]: 작업 내용, JIRA-KEY

   - 주요 변경사항 1
   - 주요 변경사항 2

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

   - fix 타입인 경우 Jira 티켓 링크를 본문에 추가

   - Type 종류:
     - `feature`: 새로운 기능 추가
     - `fix`: 버그 수정
     - `docs`: 문서 수정
     - `style`: 코드 포맷팅, 세미콜론 누락 등
     - `refactor`: 코드 리팩토링
     - `test`: 테스트 코드 추가/수정
     - `chore`: 기타 변경사항

5. **사용자 확인 및 커밋**
   - 생성된 커밋 메시지를 사용자에게 보여주고 `AskUserQuestion` 툴로 확인 요청
   - 질문 형식:
     - question: "이 커밋 메시지로 커밋하시겠습니까?"
     - header: "커밋 확인"
     - options: [{"label": "예", "description": "커밋 진행"}, {"label": "아니오", "description": "취소"}]
   - "예" 선택 시 `git add` 및 `git commit` 실행

## 사용 예시

```
/toolkit:code-commit                          # 변경사항 분석 후 Jira key 질문
/toolkit:code-commit "인증 기능 수정"          # 힌트 제공, Jira key 질문
/toolkit:code-commit PROJ-123                 # Jira key 직접 전달
```

## 커밋 메시지 예시

```
[feature]: Add login functionality, PROJ-123

- OAuth2 기반 로그인 플로우 구현
- 세션 관리 미들웨어 추가
- 로그인/로그아웃 API 엔드포인트 추가

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
[fix]: Correct typo in readme file, PROJ-456

- README.md 설치 가이드 오탈자 수정

Jira: https://jira.example.com/browse/PROJ-456

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
[refactor]: Predicate 로직 개선 및 빈 Status 처리 추가, PROJ-789

- hasStatusData 함수 재도입하여 빈 Status 명시적 처리
- hasStatusChanged에 newStatus 데이터 존재 여부 체크 추가

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 주의사항

- 민감한 정보(.env, credentials 등)가 포함된 파일은 경고
- 바이너리 파일이나 빌드 결과물은 제외 확인
- 테스트가 실패한 상태면 경고

## 민감 파일 경고 목록

다음 파일이 포함된 경우 경고:
- `.env`, `.env.*`
- `credentials.json`, `secrets.json`
- `*.pem`, `*.key`
- `config/local.json`
- `*_secret*`, `*_token*`

## 제외 권장 파일

다음 파일은 커밋에서 제외 권장:
- `node_modules/`
- `dist/`, `build/`
- `*.log`
- `.DS_Store`
- `__pycache__/`
- `*.pyc`
- 바이너리 파일 (실행 파일, 이미지 등)
