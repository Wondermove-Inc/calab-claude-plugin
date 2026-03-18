# cmux Browser API Reference

cmux 내장 브라우저 자동화 명령어 레퍼런스입니다. Playwright 기반으로 동작합니다.

## 기본 사용법

```bash
cmux browser [--surface <id|ref|index>] <subcommand> [options]
```

`--surface` 옵션으로 특정 브라우저 서피스를 지정합니다. 생략 시 현재 포커스된 브라우저 서피스가 대상입니다.

---

## 브라우저 열기/탐색

```bash
cmux browser open [url]                                # 새 브라우저 패널 열기
cmux browser open [url] --workspace <id|ref>           # 특정 워크스페이스에 열기
cmux browser open-split [url]                          # 분할로 열기
cmux browser new [url]                                 # open과 동일
cmux browser goto <url> [--snapshot-after]             # URL 이동
cmux browser navigate <url>                            # goto와 동일
cmux browser back [--snapshot-after]                   # 뒤로
cmux browser forward [--snapshot-after]                # 앞으로
cmux browser reload [--snapshot-after]                 # 새로고침
cmux browser url                                       # 현재 URL
cmux browser get-url                                   # url과 동일
```

## 페이지 스냅샷

```bash
cmux browser snapshot                                  # 전체 접근성 트리
cmux browser snapshot --interactive                    # 상호작용 가능 요소만 (-i)
cmux browser snapshot --compact                        # 간결한 출력
cmux browser snapshot --cursor                         # 커서 포함
cmux browser snapshot --max-depth <n>                  # 깊이 제한
cmux browser snapshot --selector <css>                 # 특정 영역만
```

## 스크린샷

```bash
cmux browser screenshot                                # 화면 캡처 (stdout 또는 기본 경로)
cmux browser screenshot --out /tmp/page.png            # 파일로 저장
cmux browser screenshot --json                         # JSON (base64)
```

## 클릭/상호작용

모든 조작 명령에 `--snapshot-after` 추가 시 조작 후 자동 스냅샷 반환.

```bash
cmux browser click [--selector <css> | <css>]          # 클릭
cmux browser dblclick [--selector <css> | <css>]       # 더블클릭
cmux browser hover [--selector <css> | <css>]          # 호버
cmux browser focus [--selector <css> | <css>]          # 포커스
cmux browser check [--selector <css> | <css>]          # 체크
cmux browser uncheck [--selector <css> | <css>]        # 체크 해제
cmux browser scroll-into-view [--selector <css> | <css>]  # 화면에 스크롤
```

## 텍스트 입력

```bash
cmux browser fill [--selector <css>] [--text <text>]   # 값 교체 (clear + type)
cmux browser type [--selector <css>] [--text <text>]   # 키 하나씩 입력
cmux browser press [--key <key> | <key>]               # 단일 키
cmux browser key [--key <key> | <key>]                 # press와 동일
cmux browser keydown [--key <key> | <key>]             # 키 다운
cmux browser keyup [--key <key> | <key>]               # 키 업
```

## 셀렉트/스크롤

```bash
cmux browser select [--selector <css>] [--value <value>]  # 드롭다운 선택
cmux browser scroll [--selector <css>] [--dx <n>] [--dy <n>]  # 스크롤
```

## 정보 추출

```bash
cmux browser get url                                   # 현재 URL
cmux browser get title                                 # 페이지 제목
cmux browser get text [--selector <css>]               # 텍스트
cmux browser get html [--selector <css>]               # HTML
cmux browser get value [--selector <css>]              # input value
cmux browser get attr --selector <css> --name <attr>   # 속성 값
cmux browser get count --selector <css>                # 요소 개수
cmux browser get box [--selector <css>]                # 바운딩 박스
cmux browser get styles [--selector <css>]             # 스타일
```

## 요소 상태 확인

```bash
cmux browser is visible [--selector <css>]             # 표시 여부
cmux browser is enabled [--selector <css>]             # 활성화 여부
cmux browser is checked [--selector <css>]             # 체크 여부
```

## 요소 찾기 (접근성 기반)

```bash
cmux browser find role <role>                          # ARIA role
cmux browser find text <text>                          # 텍스트 내용
cmux browser find label <label>                        # ARIA label
cmux browser find placeholder <text>                   # placeholder
cmux browser find alt <text>                           # alt 텍스트
cmux browser find title <text>                         # title 속성
cmux browser find testid <id>                          # data-testid
cmux browser find first                                # 첫 번째 요소
cmux browser find last                                 # 마지막 요소
cmux browser find nth <n>                              # n번째 요소
```

## 대기

```bash
cmux browser wait --selector <css>                     # 셀렉터 대기
cmux browser wait --text <text>                        # 텍스트 대기
cmux browser wait --url-contains <text>                # URL 포함 대기
cmux browser wait --url <text>                         # URL 일치 대기
cmux browser wait --load-state <interactive|complete>  # 페이지 로드 대기
cmux browser wait --function <js>                      # JS 함수 결과 대기
cmux browser wait --timeout-ms <ms>                    # 타임아웃 (밀리초)
cmux browser wait --timeout <seconds>                  # 타임아웃 (초)
```

## JavaScript 실행

```bash
cmux browser eval <js>                                 # JS 실행
cmux browser eval --script <js>                        # 동일
```

## 프레임

```bash
cmux browser frame main                                # 메인 프레임으로 전환
cmux browser frame selector --selector <css>           # iframe 내부로 전환
```

## 다이얼로그

```bash
cmux browser dialog accept [text]                      # 수락
cmux browser dialog dismiss [text]                     # 거부
```

## 다운로드

```bash
cmux browser download wait [--path <path>] [--timeout <seconds>]
```

## 쿠키

```bash
cmux browser cookies get [--name <name>] [--all]       # 쿠키 조회
cmux browser cookies set --name <name> --value <value> [--domain <domain>] [--path <path>] [--expires <unix>] [--secure]
cmux browser cookies clear                             # 쿠키 삭제
```

## 스토리지

```bash
cmux browser storage local get [--key <key>]           # localStorage 조회
cmux browser storage local set --key <key> --value <value>
cmux browser storage local clear
cmux browser storage session get [--key <key>]         # sessionStorage 조회
cmux browser storage session set --key <key> --value <value>
cmux browser storage session clear
```

## 탭 관리

```bash
cmux browser tab new [url]                             # 새 탭
cmux browser tab list                                  # 탭 목록
cmux browser tab switch <index>                        # 탭 전환
cmux browser tab close [index]                         # 탭 닫기
```

## 콘솔/에러

```bash
cmux browser console list                              # 콘솔 로그
cmux browser console clear                             # 콘솔 정리
cmux browser errors list                               # 에러 목록
cmux browser errors clear                              # 에러 정리
```

## 네트워크

```bash
cmux browser network requests                          # 요청 목록
cmux browser network route <pattern> [--response <json>]  # 라우트 인터셉트
cmux browser network unroute <pattern>                 # 라우트 해제
```

## 시각 도구

```bash
cmux browser highlight [--selector <css>]              # 요소 강조
cmux browser viewport <width> <height>                 # 뷰포트 설정
cmux browser geolocation <lat> <lng>                   # 위치 설정
cmux browser offline <true|false>                      # 오프라인 모드
```

## 녹화/추적

```bash
cmux browser trace start [path]                        # 추적 시작
cmux browser trace stop [path]                         # 추적 중지
cmux browser screencast start                          # 녹화 시작
cmux browser screencast stop                           # 녹화 중지
```

## 상태 저장/복원

```bash
cmux browser state save <path>                         # 상태 저장
cmux browser state load <path>                         # 상태 복원
```

## 스크립트/스타일 주입

```bash
cmux browser addinitscript <js>                        # 초기화 스크립트
cmux browser addscript <js>                            # 스크립트 추가
cmux browser addstyle <css>                            # 스타일 추가
```

## 입력 시뮬레이션

```bash
cmux browser input mouse [args...]                     # 마우스 입력
cmux browser input keyboard [args...]                  # 키보드 입력
cmux browser input touch [args...]                     # 터치 입력
```

## 포커스 관리

```bash
cmux browser focus-webview                             # 웹뷰 포커스
cmux browser is-webview-focused                        # 포커스 상태 확인
```
