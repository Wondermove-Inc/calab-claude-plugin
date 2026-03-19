# Python 코드 리뷰 가이드

## 목차
1. [타입 힌트](#1-타입-힌트)
2. [예외 처리](#2-예외-처리)
3. [함수 설계](#3-함수-설계)
4. [리소스 관리](#4-리소스-관리)
5. [보안](#5-보안)

---

## 1. 타입 힌트

### 1.1 함수 시그니처에 타입 명시

타입 힌트가 없으면 호출자가 함수의 입출력을 이해하기 위해 구현을 읽어야 한다. mypy 같은 정적 분석 도구가 타입 불일치를 사전에 잡아주므로, 런타임 에러를 줄일 수 있다.

```python
# Bad
def calculate_discount(price, rate):
    return price * (1 - rate)

# Good
def calculate_discount(price: float, rate: float) -> float:
    return price * (1 - rate)
```

### 1.2 복합 타입

컬렉션 타입은 내부 요소의 타입까지 명시한다. `list`만 쓰면 무엇의 리스트인지 알 수 없어, 잘못된 요소를 추가해도 타입 체커가 잡지 못한다.

```python
# Bad
def get_user_ids(users) -> list:
    return [u.id for u in users]

# Good
def get_user_ids(users: list[User]) -> list[int]:
    return [u.id for u in users]
```

### 1.3 Optional 명시

None이 될 수 있는 값은 `Optional` 또는 `X | None`으로 명시한다. 호출자가 None 가능성을 인지하지 못하면 `AttributeError`가 발생한다.

```python
# Bad — None 반환 가능성이 숨겨짐
def find_user(user_id: int) -> User:
    return db.query(User).filter_by(id=user_id).first()  # None 가능

# Good
def find_user(user_id: int) -> User | None:
    return db.query(User).filter_by(id=user_id).first()
```

---

## 2. 예외 처리

### 2.1 Bare except 금지

`except:`는 `KeyboardInterrupt`와 `SystemExit`까지 잡는다. Ctrl+C로 프로세스를 종료할 수 없게 되며, 메모리 부족 같은 시스템 레벨 에러도 삼켜버린다.

```python
# Bad — 모든 예외를 잡음 (KeyboardInterrupt 포함)
try:
    process_data()
except:
    pass

# Bad — 너무 넓은 범위
try:
    process_data()
except Exception:
    pass

# Good — 구체적 예외 지정
try:
    process_data()
except (ValueError, KeyError) as e:
    logger.error("Data processing failed: %s", e)
```

### 2.2 에러 무시 금지

빈 except 블록은 실패를 완전히 숨긴다. 최소한 로깅을 해야 프로덕션에서 문제 발생 시 원인을 추적할 수 있다.

```python
# Bad
try:
    save_to_cache(data)
except CacheError:
    pass

# Good — 의도적 무시 시 로깅 + 이유 명시
try:
    save_to_cache(data)
except CacheError:
    logger.debug("Cache save failed, continuing without cache")
```

### 2.3 예외 체이닝

원본 예외 정보를 보존하지 않으면 디버깅 시 root cause를 찾기 어렵다. `from` 키워드로 원본 예외를 연결하면 전체 traceback이 보존된다.

```python
# Bad — 원본 예외 소실
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    raise ValueError("Invalid config format")

# Good — 원본 예외 보존
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise ValueError("Invalid config format") from e
```

---

## 3. 함수 설계

### 3.1 Mutable 기본 인자 금지

Python의 기본 인자는 함수 정의 시 한 번만 평가된다. Mutable 객체를 기본값으로 사용하면 모든 호출이 같은 객체를 공유하여, 한 호출에서의 변경이 다른 호출에 영향을 미친다.

```python
# Bad — 모든 호출이 같은 리스트를 공유
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"] — 예상: ["b"]

# Good — None을 기본값으로 사용
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 3.2 단일 책임

하나의 함수가 데이터 조회, 변환, 저장을 모두 하면 테스트와 재사용이 어렵다. 각 단계를 분리하면 조합하여 다양한 시나리오에 대응할 수 있다.

```python
# Bad — 조회 + 변환 + 저장이 결합
def process_orders():
    orders = db.query(Order).filter_by(status="pending").all()
    for order in orders:
        order.total = sum(item.price for item in order.items)
        order.status = "processed"
    db.commit()

# Good — 각 단계를 분리
def get_pending_orders() -> list[Order]:
    return db.query(Order).filter_by(status="pending").all()

def calculate_total(order: Order) -> float:
    return sum(item.price for item in order.items)

def process_orders():
    for order in get_pending_orders():
        order.total = calculate_total(order)
        order.status = "processed"
    db.commit()
```

---

## 4. 리소스 관리

### 4.1 Context manager 사용

파일, DB 연결, 네트워크 소켓 등은 `with` 문으로 관리한다. 예외 발생 시에도 자동으로 리소스가 해제되므로, `try/finally`보다 안전하고 간결하다.

```python
# Bad — 예외 시 파일이 닫히지 않음
f = open("data.csv")
data = f.read()
f.close()

# Good
with open("data.csv") as f:
    data = f.read()
```

### 4.2 DB 세션 관리

ORM 세션을 명시적으로 닫지 않으면 connection pool이 고갈된다. context manager 패턴으로 세션 라이프사이클을 보장한다.

```python
# Bad — 예외 시 세션이 닫히지 않음
session = SessionLocal()
users = session.query(User).all()
session.close()

# Good
with SessionLocal() as session:
    users = session.query(User).all()
```

---

## 5. 보안

### 5.1 f-string SQL 금지

사용자 입력을 직접 SQL 문자열에 삽입하면 SQL injection 공격에 노출된다. 파라미터 바인딩을 사용하면 DB 드라이버가 입력값을 안전하게 이스케이프한다.

```python
# Bad — SQL injection 취약
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

# Good — 파라미터 바인딩
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

### 5.2 subprocess 보안

`shell=True`와 사용자 입력을 결합하면 command injection이 가능하다. 리스트 형태로 인자를 전달하면 셸 해석을 우회하여 안전하다.

```python
# Bad — command injection 취약
subprocess.run(f"grep {user_input} /var/log/app.log", shell=True)

# Good — 셸 해석 없이 직접 실행
subprocess.run(["grep", user_input, "/var/log/app.log"])
```

### 5.3 pickle 역직렬화 금지

`pickle.loads()`는 임의 코드 실행이 가능하다. 신뢰할 수 없는 소스의 데이터를 pickle로 역직렬화하면 원격 코드 실행(RCE) 취약점이 된다.

```python
# Bad — 원격 코드 실행 가능
data = pickle.loads(request.body)

# Good — 안전한 직렬화 포맷 사용
data = json.loads(request.body)
```
