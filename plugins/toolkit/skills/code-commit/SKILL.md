---
name: toolkit:code-commit
description: 현재 변경사항을 분석하고 커밋 메시지를 생성합니다
user-invocable: true
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

3. **커밋 메시지 생성**
   - 다음 형식을 따름:
   ```
   [type]: 간단 명료한 제목

   - 주요 변경사항 1
   - 주요 변경사항 2
   - 주요 변경사항 3

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

   - Type 종류:
     - `feature`: 새로운 기능 추가
     - `fix`: 버그 수정
     - `refactor`: 코드 리팩토링
     - `test`: 테스트 코드 추가/수정
     - `docs`: 문서 수정
     - `chore`: 기타 변경사항

4. **사용자 확인 및 커밋**
   - 생성된 커밋 메시지를 사용자에게 보여주고 확인 요청
   - 승인 시 `git add` 및 `git commit` 실행

## 주의사항

- 민감한 정보(.env, credentials 등)가 포함된 파일은 경고
- 바이너리 파일이나 빌드 결과물은 제외 확인
- 테스트가 실패한 상태면 경고
- 커밋 전에 린트 검사 수행 (선택적)

## 사용 예시

### 기본 사용
```
/toolkit:code-commit
```
→ 현재 변경사항 분석 후 커밋 메시지 생성

### 메시지 힌트 제공
```
/toolkit:code-commit "인증 기능 수정"
```
→ 힌트를 바탕으로 커밋 메시지 생성

## 커밋 메시지 예시

```
[refactor]: Predicate 로직 개선 및 빈 Status 처리 추가

- hasStatusData 함수 재도입하여 빈 Status 명시적 처리
- hasStatusChanged에 newStatus 데이터 존재 여부 체크 추가
- Edge case 테스트 7개 추가 (총 13개 테스트 통과)
- 코드 주석 및 문서화 개선

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
[feature]: 사용자 알림 설정 기능 추가

- NotificationSettings 컴포넌트 구현
- 이메일/푸시 알림 토글 기능
- 설정 변경 시 API 연동
- 로딩/에러 상태 처리

Co-Authored-By: Claude <noreply@anthropic.com>
```

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
