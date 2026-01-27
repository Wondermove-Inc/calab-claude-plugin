# Python 베스트 프랙티스 (2025)

> 이 문서는 Python 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 타입 힌트 (Type Hints)

### 1.1 기본 타입 힌트 (Python 3.9+)

```python
# 기본 타입
def greet(name: str) -> str:
    """사용자에게 인사 메시지 반환."""
    return f"Hello, {name}!"

# 컬렉션 타입 (Python 3.9+ 네이티브)
def process_items(items: list[str]) -> dict[str, int]:
    """아이템 목록을 처리하여 카운트 반환."""
    return {item: len(item) for item in items}

# Optional 타입
def find_user(user_id: str) -> User | None:
    """ID로 사용자 조회. 없으면 None 반환."""
    return users.get(user_id)
```

### 1.2 고급 타입 힌트

```python
from typing import TypeVar, Generic, Callable, TypeAlias

# 제네릭
T = TypeVar('T')

class Repository(Generic[T]):
    """제네릭 저장소 패턴."""

    def find_by_id(self, id: str) -> T | None:
        ...

    def save(self, entity: T) -> T:
        ...

# TypeAlias (Python 3.10+)
UserId: TypeAlias = str
UserDict: TypeAlias = dict[str, "User"]

# Callable
Handler: TypeAlias = Callable[[Request], Response]
```

### 1.3 Pydantic 모델 (데이터 검증)

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    """사용자 생성 요청 모델."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)

class UserResponse(BaseModel):
    """사용자 응답 모델."""

    id: str
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # ORM 모드

# 사용
user_data = UserCreate(
    email="user@example.com",
    password="secure123",
    name="John Doe"
)
```

---

## 2. 코드 스타일 (PEP 8)

### 2.1 네이밍 규칙

```python
# 모듈: snake_case
# user_service.py

# 클래스: PascalCase
class UserService:
    pass

# 함수/메서드: snake_case
def get_user_by_id(user_id: str) -> User:
    pass

# 상수: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 프라이빗: _prefix
class Service:
    def __init__(self):
        self._cache = {}

    def _internal_method(self):
        pass
```

### 2.2 Docstring (Google 스타일)

```python
def calculate_discount(
    price: float,
    discount_rate: float,
    min_price: float = 0.0
) -> float:
    """가격에서 할인율을 적용하여 최종 가격 계산.

    Args:
        price: 원래 가격
        discount_rate: 할인율 (0.0 ~ 1.0)
        min_price: 최소 가격 (기본값: 0.0)

    Returns:
        할인이 적용된 최종 가격

    Raises:
        ValueError: 할인율이 0~1 범위를 벗어난 경우

    Examples:
        >>> calculate_discount(100, 0.2)
        80.0
        >>> calculate_discount(100, 0.2, min_price=90)
        90.0
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("할인율은 0과 1 사이여야 합니다")

    discounted = price * (1 - discount_rate)
    return max(discounted, min_price)
```

---

## 3. 프로젝트 구조

### 3.1 패키지 구조 (src layout)

```
project/
├── pyproject.toml          # 프로젝트 설정 (Poetry/pip)
├── README.md
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py         # 진입점
│       ├── config.py       # 설정
│       ├── domain/         # 도메인 모델
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── exceptions.py
│       ├── services/       # 비즈니스 로직
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── repositories/   # 데이터 접근
│       │   ├── __init__.py
│       │   └── user_repository.py
│       └── api/            # API 레이어
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures
│   ├── unit/
│   └── integration/
└── scripts/
```

### 3.2 pyproject.toml (현대적 설정)

```toml
[project]
name = "myproject"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true
```

---

## 4. 에러 처리

### 4.1 커스텀 예외

```python
class AppError(Exception):
    """애플리케이션 기본 예외."""

    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    """리소스를 찾을 수 없음."""

    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            code="NOT_FOUND"
        )

class ValidationError(AppError):
    """유효성 검증 실패."""

    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation failed for '{field}': {message}",
            code="VALIDATION_ERROR"
        )
```

### 4.2 에러 처리 패턴

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def handle_db_errors() -> Generator[None, None, None]:
    """데이터베이스 에러 컨텍스트 매니저."""
    try:
        yield
    except IntegrityError as e:
        raise ValidationError("data", "Duplicate entry") from e
    except OperationalError as e:
        raise AppError("Database connection failed", "DB_ERROR") from e

# 사용
def create_user(data: UserCreate) -> User:
    """사용자 생성."""
    with handle_db_errors():
        user = User(**data.model_dump())
        db.add(user)
        db.commit()
        return user
```

---

## 5. 비동기 프로그래밍 (Async/Await)

### 5.1 비동기 함수

```python
import asyncio
from typing import Sequence

async def fetch_user(user_id: str) -> User:
    """비동기로 사용자 조회."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            data = await response.json()
            return User(**data)

async def fetch_users(user_ids: list[str]) -> list[User]:
    """여러 사용자 동시 조회."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

### 5.2 FastAPI 비동기 엔드포인트

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """데이터베이스 세션 의존성."""
    async with async_session() as session:
        yield session

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> User:
    """사용자 조회 API."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## 6. 테스트

### 6.1 pytest 기본

```python
import pytest
from myproject.services.user_service import UserService

class TestUserService:
    """UserService 테스트."""

    @pytest.fixture
    def service(self) -> UserService:
        """테스트용 서비스 인스턴스."""
        return UserService()

    def test_create_user_success(self, service: UserService) -> None:
        """유효한 데이터로 사용자 생성 성공."""
        # Arrange
        data = UserCreate(email="test@example.com", password="secure123", name="Test")

        # Act
        user = service.create(data)

        # Assert
        assert user.email == "test@example.com"
        assert user.name == "Test"

    def test_create_user_invalid_email(self, service: UserService) -> None:
        """잘못된 이메일로 ValidationError 발생."""
        with pytest.raises(ValidationError, match="email"):
            service.create(UserCreate(email="invalid", password="secure123", name="Test"))
```

### 6.2 pytest fixture

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    """테스트용 데이터베이스 엔진."""
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="function")
def db_session(engine):
    """각 테스트마다 새로운 DB 세션."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
```

---

## 7. 로깅

### 7.1 구조화된 로깅

```python
import logging
import structlog

# structlog 설정
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# 사용
def process_order(order_id: str) -> None:
    """주문 처리."""
    log = logger.bind(order_id=order_id)
    log.info("processing_order_started")

    try:
        # 처리 로직
        log.info("processing_order_completed", status="success")
    except Exception as e:
        log.error("processing_order_failed", error=str(e))
        raise
```

---

## 8. 금지 사항

- [ ] 타입 힌트 없는 함수
- [ ] bare except 사용 (`except:` → `except Exception:`)
- [ ] mutable 기본 인자 (`def f(items=[])` → `def f(items=None)`)
- [ ] global 변수 사용
- [ ] import * 사용
- [ ] 단일 문자 변수명 (루프 제외)
- [ ] print 대신 logger 사용
- [ ] 하드코딩된 설정값

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] 타입 힌트 100% 적용
- [ ] Google 스타일 Docstring
- [ ] PEP 8 준수 (ruff 검사)
- [ ] 커스텀 예외 사용
- [ ] pytest 테스트 작성
- [ ] 구조화된 로깅
- [ ] 파일 300줄 이하
