# /jira --init - JIRA 초기 설정

> **JIRA 프로젝트 연결 초기화**

## 전제 조건
- JIRA_EMAIL 환경 변수
- JIRA_API_TOKEN 환경 변수
- API 토큰: https://id.atlassian.com/manage-profile/security/api-tokens

## 실행 절차

### Step 1: 환경 변수 확인
```bash
echo $JIRA_EMAIL
echo $JIRA_API_TOKEN
```

### Step 2: 설정 파일 생성
**.claude/integrations/jira_config.json:**
```json
{
  "jira": {
    "enabled": true,
    "base_url": "https://company.atlassian.net",
    "project_key": "AUTH",
    "auto_sync": {
      "on_task_start": true,
      "on_task_done": true,
      "on_blocker": true
    }
  }
}
```

### Step 3: 연결 테스트
```bash
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  "https://company.atlassian.net/rest/api/3/myself"
```

### Step 4: 프로젝트 검증
- 프로젝트 존재 확인
- 이슈 타입 확인

### Step 5: 매핑 파일 초기화
**.claude-state/jira_mapping.json:**
```json
{
  "project_key": "AUTH",
  "base_url": "https://company.atlassian.net",
  "mappings": {},
  "reverse_mappings": {},
  "last_sync": null
}
```

### 완료 보고
```
============================================
 JIRA INIT 완료
============================================
 연결: ✅ 성공
 프로젝트: AUTH
 다음 단계: /jira --push
============================================
```
