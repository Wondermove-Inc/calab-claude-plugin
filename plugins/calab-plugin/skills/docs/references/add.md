# /docs --add - 특정 유형 문서 추가

> **특정 유형의 문서를 개별적으로 추가**

## 사용법
```bash
/docs --add api
/docs --add component
/docs --add architecture
/docs --add getting-started
/docs --add guide
/docs --add config
/docs --add faq
/docs --add troubleshooting
```

## 문서 유형별 필수 항목

| 유형 | 필수 항목 수 | Mermaid | 스크린샷 |
|------|-------------|--------|---------|
| `getting-started` | 15개 | - | 필수 |
| `architecture` | 12개 | 4개+ | 선택 |
| `api` | 20개/엔드포인트 | 필수 | - |
| `component` | 18개/컴포넌트 | 선택 | 필수 |
| `guide` | 10개 | 필수 | 단계별 |
| `config` | 8개/옵션 | - | 선택 |
| `faq` | 5개/질문 | - | - |
| `troubleshooting` | 6개/이슈 | - | 필수 |

## 실행 절차

### Step 1: 문서 유형 파악
$ARGUMENTS에서 유형 추출

### Step 2: 프로젝트 코드 분석
- API: 라우트 파일 스캔
- Component: 컴포넌트 파일 스캔
- 등등

### Step 3: 필수 항목별 문서 작성

**API 예시 (20개 항목/엔드포인트):**
- 엔드포인트 URL
- HTTP 메서드
- 설명
- Request Headers
- Request Body (스키마)
- Path Parameters
- Query Parameters
- Response (200, 201, 400, 401, 403, 404, 500)
- 각 에러의 원인과 해결법
- 코드 예시 4개
- cURL 예시

### Step 4: 플레이스홀더 삽입
```markdown
<!-- 📸 스크린샷 필요: API 응답 예시 -->
```

### 출력 위치
```
.claude/docs-site/{유형}/
```
