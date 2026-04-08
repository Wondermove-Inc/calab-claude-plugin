---
name: setup:graph
description: code-review-graph 프로젝트 초기화 및 관리. 코드 그래프 빌드, 벡터 임베딩 생성, 그래프 상태 확인을 수행합니다.
allowed-tools: Bash, Read, mcp__plugin_code-review-graph_code-review-graph__build_or_update_graph_tool, mcp__plugin_code-review-graph_code-review-graph__embed_graph_tool, mcp__plugin_code-review-graph_code-review-graph__list_graph_stats_tool
disable-model-invocation: true
---

# /setup:graph - code-review-graph 초기화 및 관리

## 설명
프로젝트의 코드 지식 그래프를 빌드하고 벡터 임베딩을 생성합니다. 그래프가 구축되면 architect, reviewer, code-review 등의 에이전트/스킬이 구조적 영향 분석을 수행할 수 있습니다.

## 사용법
- `/setup:graph` - 그래프 빌드 + 임베딩 (초기화 또는 증분 업데이트)
- `/setup:graph 전체` - 전체 재빌드 + 임베딩
- `/setup:graph 상태` - 그래프 상태 확인
- `/setup:graph 삭제` - 그래프 데이터 삭제

## 실행 방식

### 사용자 요청 분석
사용자 입력에서 키워드를 감지하여 모드를 선택합니다.

| 키워드 | 모드 |
|--------|------|
| "전체", "재빌드", "full", "rebuild" | 전체 재빌드 모드 |
| "상태", "status", "확인" | 상태 확인 모드 |
| "삭제", "제거", "remove", "clean" | 삭제 모드 |
| 키워드 없음 (기본) | 초기화/업데이트 모드 |

---

## 초기화/업데이트 모드 (기본)

### 1단계: 환경 확인
```bash
# code-review-graph 설치 확인
uv tool list 2>/dev/null | grep code-review-graph || echo "NOT_INSTALLED"
```

- **미설치 시**: 아래 안내를 출력하고 종료
  ```
  code-review-graph가 설치되지 않았습니다.
  설치: uv tool install "code-review-graph[embeddings]"
  ```

### 2단계: 기존 그래프 확인
```bash
# 그래프 DB 존재 여부
ls -la .code-review-graph/graph.db 2>/dev/null
```

- **존재**: "기존 그래프를 증분 업데이트합니다." 표시
- **미존재**: "새 그래프를 빌드합니다." 표시

### 3단계: 그래프 빌드
```
build_or_update_graph_tool(full_rebuild: false)
```

빌드 결과를 확인하고 오류 시 사용자에게 보고합니다.

### 4단계: 벡터 임베딩
```
embed_graph_tool()
```

임베딩 결과를 확인하고 오류 시 사용자에게 보고합니다.

### 5단계: 검증
```
list_graph_stats_tool()
```

그래프 통계를 표시합니다:
```
그래프 초기화 완료

| 항목 | 결과 |
|------|------|
| 노드 | N개 |
| 엣지 | N개 |
| 파일 | N개 |
| 언어 | ... |
| 임베딩 | 완료 |
```

---

## 전체 재빌드 모드

3단계만 다릅니다:
```
build_or_update_graph_tool(full_rebuild: true)
```

이후 4~5단계 동일.

---

## 상태 확인 모드

### 1단계: 환경 확인
```bash
uv tool list 2>/dev/null | grep code-review-graph || echo "NOT_INSTALLED"
```

### 2단계: 그래프 상태
```bash
ls -la .code-review-graph/graph.db 2>/dev/null
```

- **미존재**: "그래프가 빌드되지 않았습니다. `/setup:graph`로 초기화하세요." 출력 후 종료

### 3단계: 통계 표시
```
list_graph_stats_tool()
```

---

## 삭제 모드

### 1단계: 그래프 존재 확인
```bash
ls -la .code-review-graph/ 2>/dev/null
```

- **미존재**: "삭제할 그래프가 없습니다." 출력 후 종료

### 2단계: 삭제 실행
```bash
rm -rf .code-review-graph/
```

### 3단계: 확인
```
그래프 데이터가 삭제되었습니다.
재빌드: /setup:graph
```

---

## .gitignore 처리

그래프 빌드 후 `.code-review-graph/`가 `.gitignore`에 포함되어 있는지 확인합니다. 포함되지 않았으면 안내합니다:
```
.code-review-graph/ 디렉토리가 .gitignore에 포함되지 않았습니다.
그래프 DB는 프로젝트별로 빌드되므로 커밋할 필요가 없습니다.
```
