# Go 코드 리뷰 가이드

## 목차
1. [에러 처리](#1-에러-처리)
2. [네이밍](#2-네이밍)
3. [타입 안전성](#3-타입-안전성)
4. [동시성](#4-동시성)
5. [리소스 관리](#5-리소스-관리)
6. [인터페이스 설계](#6-인터페이스-설계)

---

## 1. 에러 처리

### 1.1 에러 무시 금지

에러를 무시하면 런타임에 원인 파악이 불가능한 장애로 이어진다. 프로덕션에서 silent failure가 가장 디버깅하기 어려운 유형이기 때문에, 모든 에러는 명시적으로 처리해야 한다.

```go
// Bad
data, _ := json.Marshal(v)

// Good
data, err := json.Marshal(v)
if err != nil {
    return fmt.Errorf("marshaling config: %w", err)
}
```

### 1.2 에러 래핑

에러를 그대로 반환하면 호출 체인에서 어디서 에러가 발생했는지 알 수 없다. `%w`로 래핑하면 `errors.Is()`, `errors.As()`로 에러 체인을 탐색할 수 있어, 상위 호출자가 에러 유형에 따라 분기 처리할 수 있다.

```go
// Bad — 컨텍스트 없이 에러 전달
if err != nil {
    return err
}

// Good — 현재 작업의 컨텍스트를 추가
if err != nil {
    return fmt.Errorf("loading user %d: %w", userID, err)
}
```

### 1.3 에러 타입 설계

sentinel error(`var ErrNotFound = errors.New(...)`)는 패키지 경계에서 사용하고, 내부 로직에서는 `%w` 래핑으로 충분하다. 커스텀 에러 타입은 추가 필드(코드, 메타데이터)가 필요할 때만 만든다.

```go
// Bad — 문자열 비교로 에러 판별
if err.Error() == "not found" { ... }

// Good — sentinel error 또는 타입 단언 사용
if errors.Is(err, ErrNotFound) { ... }
```

---

## 2. 네이밍

### 2.1 패키지명

패키지명은 소문자 단수형이어야 한다. 복수형이나 camelCase는 Go 생태계 전체의 컨벤션과 충돌하며, `import` 시 별칭을 붙여야 하는 불편을 초래한다.

```go
// Bad
package userUtils
package models

// Good
package user
package model
```

### 2.2 Getter에 Get 접두사 금지

Go에서는 Getter에 Get 접두사를 붙이지 않는다. Java/C# 관행이 Go에서는 불필요한 장황함으로 여겨지며, stdlib 전체가 이 패턴을 따른다.

```go
// Bad
func (u *User) GetName() string { return u.name }

// Good
func (u *User) Name() string { return u.name }
```

### 2.3 변수명 길이

변수의 스코프가 짧으면 짧은 이름, 스코프가 길면 서술적 이름을 사용한다. 루프 변수에 descriptiveName을 쓰면 오히려 가독성이 떨어진다.

```go
// 짧은 스코프 — 짧은 이름
for i, v := range items { ... }

// 긴 스코프 — 서술적 이름
var currentRetryCount int
```

---

## 3. 타입 안전성

### 3.1 any (interface{}) 남용 지양

`any`는 컴파일 타임 타입 검사를 포기하는 것이다. 제네릭이 도입된 Go 1.18 이후로는 대부분의 `interface{}` 사용을 제네릭으로 대체할 수 있다. 타입 안전성을 포기하면 런타임 panic 위험이 증가한다.

```go
// Bad
func Process(data any) any { ... }

// Good — 제네릭 사용
func Process[T Processable](data T) (Result, error) { ... }

// Good — 구체적 인터페이스
func Process(data io.Reader) (Result, error) { ... }
```

### 3.2 타입 단언 시 ok 체크

타입 단언 실패 시 panic이 발생한다. 프로덕션 코드에서 panic은 프로세스 전체를 종료시키므로, 반드시 comma-ok 패턴을 사용해야 한다.

```go
// Bad — panic 위험
val := i.(string)

// Good
val, ok := i.(string)
if !ok {
    return fmt.Errorf("expected string, got %T", i)
}
```

---

## 4. 동시성

### 4.1 goroutine 누수

goroutine은 가비지 컬렉션되지 않는다. 종료 조건 없이 생성된 goroutine은 메모리와 CPU를 영구적으로 점유하며, 장기 운영 서비스에서 점진적 성능 저하를 유발한다.

```go
// Bad — 종료 신호 없음
go func() {
    for {
        doWork()
        time.Sleep(time.Second)
    }
}()

// Good — context로 종료 제어
go func(ctx context.Context) {
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()
    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            doWork()
        }
    }
}(ctx)
```

### 4.2 channel 닫기

channel을 닫지 않으면 수신자가 영원히 블로킹된다. 송신 측에서 더 이상 보낼 데이터가 없을 때 반드시 닫아야 하며, 수신 측에서 닫으면 panic이 발생한다.

```go
// Bad — channel이 닫히지 않아 range가 영원히 블로킹
ch := make(chan int)
go func() {
    for i := 0; i < 10; i++ {
        ch <- i
    }
}()
for v := range ch { ... } // 영원히 블로킹

// Good
go func() {
    defer close(ch)
    for i := 0; i < 10; i++ {
        ch <- i
    }
}()
```

### 4.3 sync 패턴

mutex 사용 시 `defer mu.Unlock()`을 습관화한다. early return 경로에서 unlock을 빠뜨리면 deadlock이 발생하며, defer는 이를 구조적으로 방지한다.

```go
// Bad — early return 시 unlock 누락 위험
mu.Lock()
if condition {
    mu.Unlock()
    return
}
// ... 복잡한 로직
mu.Unlock()

// Good
mu.Lock()
defer mu.Unlock()
if condition {
    return
}
```

---

## 5. 리소스 관리

### 5.1 defer close 패턴

파일, DB 연결, HTTP body 등 리소스는 획득 직후 `defer`로 해제를 예약한다. 함수 중간에 에러로 반환될 때 리소스 누수가 발생하는 것을 방지한다.

```go
// Bad — 에러 경로에서 close 누락
f, err := os.Open(path)
if err != nil {
    return err
}
// ... 중간에 return이 있으면 f가 닫히지 않음
f.Close()

// Good
f, err := os.Open(path)
if err != nil {
    return err
}
defer f.Close()
```

### 5.2 HTTP response body

`http.Client.Do()`의 응답 body는 반드시 닫아야 한다. 닫지 않으면 TCP 연결이 재사용되지 않아 connection pool이 고갈되며, 대량 요청 시 "too many open files" 에러가 발생한다.

```go
resp, err := client.Do(req)
if err != nil {
    return err
}
defer resp.Body.Close()
```

---

## 6. 인터페이스 설계

### 6.1 소비자 측에서 정의

Go의 인터페이스는 암시적으로 구현되므로, 인터페이스를 사용하는 쪽(소비자)에서 정의하는 것이 올바르다. 생산자 측에서 인터페이스를 정의하면 불필요하게 큰 인터페이스가 만들어지고, 소비자가 필요하지 않은 메서드까지 의존하게 된다.

```go
// Bad — 구현 측에서 거대 인터페이스 정의
type UserStore interface {
    Get(id int) (*User, error)
    List() ([]*User, error)
    Create(u *User) error
    Update(u *User) error
    Delete(id int) error
}

// Good — 소비자가 필요한 메서드만 정의
type UserGetter interface {
    Get(id int) (*User, error)
}
```

### 6.2 인터페이스 크기

인터페이스는 작을수록 좋다. 1~3개 메서드가 이상적이며, 5개 이상이면 분리를 검토한다. 큰 인터페이스는 mock 작성이 어렵고, 구현 시 불필요한 메서드까지 구현해야 하는 부담을 준다.
