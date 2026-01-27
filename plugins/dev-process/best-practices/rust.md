# Rust 베스트 프랙티스 (2025)

> 이 문서는 Rust 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 소유권과 빌림 (Ownership & Borrowing)

### 1.1 소유권 기본

```rust
// 소유권 이동 (Move)
fn process_string(s: String) {
    println!("{}", s);
} // s가 drop됨

fn main() {
    let s = String::from("hello");
    process_string(s);
    // println!("{}", s); // ❌ 컴파일 에러: s가 이동됨
}

// 빌림 (Borrow) - 불변 참조
fn print_string(s: &String) {
    println!("{}", s);
}

fn main() {
    let s = String::from("hello");
    print_string(&s);
    println!("{}", s); // ✅ OK: s는 여전히 유효
}

// 가변 빌림 (Mutable Borrow)
fn append_world(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s = String::from("hello");
    append_world(&mut s);
    println!("{}", s); // "hello world"
}
```

### 1.2 빌림 규칙

```rust
// 규칙 1: 여러 불변 참조 OR 하나의 가변 참조
fn main() {
    let mut s = String::from("hello");

    // ✅ 여러 불변 참조 OK
    let r1 = &s;
    let r2 = &s;
    println!("{} {}", r1, r2);

    // ✅ 이후 가변 참조 OK (r1, r2는 더 이상 사용 안 함)
    let r3 = &mut s;
    r3.push_str(" world");
}
```

---

## 2. 에러 처리 (Result & Option)

### 2.1 Result 타입

```rust
use std::fs::File;
use std::io::{self, Read};

/// 파일에서 사용자 이름을 읽습니다.
fn read_username_from_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?; // ? 연산자로 에러 전파
    let mut username = String::new();
    file.read_to_string(&mut username)?;
    Ok(username)
}

// 체이닝 스타일
fn read_username_chained(path: &str) -> Result<String, io::Error> {
    let mut username = String::new();
    File::open(path)?.read_to_string(&mut username)?;
    Ok(username)
}

// 더 간결하게
fn read_username_fs(path: &str) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}
```

### 2.2 커스텀 에러 타입

```rust
use thiserror::Error;

/// 애플리케이션 에러 타입
#[derive(Error, Debug)]
pub enum AppError {
    #[error("User not found: {0}")]
    NotFound(String),

    #[error("Validation failed: {0}")]
    Validation(String),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

// Result 타입 별칭
pub type Result<T> = std::result::Result<T, AppError>;

// 사용
fn find_user(id: &str) -> Result<User> {
    let user = db.find_by_id(id)?;  // sqlx::Error → AppError::Database
    user.ok_or_else(|| AppError::NotFound(id.to_string()))
}
```

### 2.3 Option 타입

```rust
/// Option 처리 패턴
fn find_item(items: &[Item], id: u32) -> Option<&Item> {
    items.iter().find(|item| item.id == id)
}

fn main() {
    let items = vec![Item { id: 1, name: "A" }, Item { id: 2, name: "B" }];

    // match 패턴
    match find_item(&items, 1) {
        Some(item) => println!("Found: {}", item.name),
        None => println!("Not found"),
    }

    // if let 패턴
    if let Some(item) = find_item(&items, 1) {
        println!("Found: {}", item.name);
    }

    // unwrap_or_default
    let item = find_item(&items, 999).unwrap_or(&Item::default());

    // map 체이닝
    let name = find_item(&items, 1).map(|i| i.name.to_uppercase());
}
```

---

## 3. 구조체와 Trait

### 3.1 구조체 정의

```rust
use serde::{Deserialize, Serialize};

/// 사용자 엔티티
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: String,
    pub email: String,
    pub name: String,
    #[serde(skip_serializing)]
    pub password_hash: String,
}

impl User {
    /// 새 사용자 생성
    pub fn new(email: String, name: String, password_hash: String) -> Self {
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            email,
            name,
            password_hash,
        }
    }

    /// 이메일 유효성 검사
    pub fn validate_email(&self) -> bool {
        self.email.contains('@')
    }
}

/// 빌더 패턴
#[derive(Default)]
pub struct UserBuilder {
    email: Option<String>,
    name: Option<String>,
    password_hash: Option<String>,
}

impl UserBuilder {
    pub fn email(mut self, email: impl Into<String>) -> Self {
        self.email = Some(email.into());
        self
    }

    pub fn name(mut self, name: impl Into<String>) -> Self {
        self.name = Some(name.into());
        self
    }

    pub fn password_hash(mut self, hash: impl Into<String>) -> Self {
        self.password_hash = Some(hash.into());
        self
    }

    pub fn build(self) -> Result<User, AppError> {
        Ok(User::new(
            self.email.ok_or(AppError::Validation("email required".into()))?,
            self.name.ok_or(AppError::Validation("name required".into()))?,
            self.password_hash.ok_or(AppError::Validation("password required".into()))?,
        ))
    }
}
```

### 3.2 Trait 정의

```rust
use async_trait::async_trait;

/// Repository trait (비동기)
#[async_trait]
pub trait Repository<T> {
    async fn find_by_id(&self, id: &str) -> Result<Option<T>>;
    async fn save(&self, entity: &T) -> Result<()>;
    async fn delete(&self, id: &str) -> Result<()>;
}

/// UserRepository 구현
pub struct PostgresUserRepository {
    pool: sqlx::PgPool,
}

#[async_trait]
impl Repository<User> for PostgresUserRepository {
    async fn find_by_id(&self, id: &str) -> Result<Option<User>> {
        sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
            .fetch_optional(&self.pool)
            .await
            .map_err(AppError::from)
    }

    async fn save(&self, user: &User) -> Result<()> {
        sqlx::query!(
            "INSERT INTO users (id, email, name) VALUES ($1, $2, $3)",
            user.id,
            user.email,
            user.name
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }

    async fn delete(&self, id: &str) -> Result<()> {
        sqlx::query!("DELETE FROM users WHERE id = $1", id)
            .execute(&self.pool)
            .await?;
        Ok(())
    }
}
```

---

## 4. 비동기 프로그래밍 (Async/Await)

### 4.1 tokio 런타임

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<()> {
    // 비동기 함수 호출
    let result = fetch_data().await?;
    println!("{:?}", result);
    Ok(())
}

/// HTTP 요청 (reqwest)
async fn fetch_data() -> Result<String> {
    let response = reqwest::get("https://api.example.com/data")
        .await
        .map_err(|e| AppError::Io(std::io::Error::new(std::io::ErrorKind::Other, e)))?;

    let text = response.text().await
        .map_err(|e| AppError::Io(std::io::Error::new(std::io::ErrorKind::Other, e)))?;

    Ok(text)
}

/// 동시 실행
async fn fetch_multiple() -> Result<Vec<String>> {
    let urls = vec!["url1", "url2", "url3"];

    let futures: Vec<_> = urls.iter().map(|url| fetch_url(url)).collect();
    let results = futures::future::join_all(futures).await;

    results.into_iter().collect()
}
```

### 4.2 Axum 웹 프레임워크

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use std::sync::Arc;

/// 애플리케이션 상태
pub struct AppState {
    pub user_service: UserService,
}

/// 라우터 설정
pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).delete(delete_user))
        .with_state(state)
}

/// GET /users/:id
async fn get_user(
    State(state): State<Arc<AppState>>,
    Path(id): Path<String>,
) -> impl IntoResponse {
    match state.user_service.find_by_id(&id).await {
        Ok(Some(user)) => (StatusCode::OK, Json(user)).into_response(),
        Ok(None) => (StatusCode::NOT_FOUND, "User not found").into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

/// POST /users
async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(input): Json<CreateUserInput>,
) -> impl IntoResponse {
    match state.user_service.create(input).await {
        Ok(user) => (StatusCode::CREATED, Json(user)).into_response(),
        Err(e) => (StatusCode::BAD_REQUEST, e.to_string()).into_response(),
    }
}
```

---

## 5. 테스트

### 5.1 단위 테스트

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_email_validation() {
        let user = User::new(
            "test@example.com".to_string(),
            "Test".to_string(),
            "hash".to_string(),
        );
        assert!(user.validate_email());
    }

    #[test]
    fn test_invalid_email() {
        let user = User::new(
            "invalid".to_string(),
            "Test".to_string(),
            "hash".to_string(),
        );
        assert!(!user.validate_email());
    }

    #[test]
    #[should_panic(expected = "email required")]
    fn test_builder_missing_email() {
        UserBuilder::default()
            .name("Test")
            .password_hash("hash")
            .build()
            .unwrap();
    }
}
```

### 5.2 비동기 테스트

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio;

    #[tokio::test]
    async fn test_fetch_user() {
        let repo = MockUserRepository::new();
        let service = UserService::new(Arc::new(repo));

        let result = service.find_by_id("1").await;
        assert!(result.is_ok());
    }
}
```

---

## 6. 금지 사항

- [ ] unwrap() 프로덕션 코드에서 사용 (expect() 또는 ? 사용)
- [ ] unsafe 블록 남용 (필요시 문서화 필수)
- [ ] clone() 남용 (참조로 해결 가능한지 확인)
- [ ] panic! 복구 가능한 에러에 사용
- [ ] 불필요한 Box<dyn Trait> (제네릭으로 해결 가능시)
- [ ] mut 과다 사용 (불변성 우선)
- [ ] 글로벌 상태 (lazy_static 등)

---

## 7. 체크리스트

코드 생성 시 확인:

- [ ] 소유권/빌림 규칙 준수
- [ ] Result/Option 적절히 사용
- [ ] thiserror로 커스텀 에러
- [ ] derive 매크로 활용
- [ ] clippy 경고 없음
- [ ] rustfmt 적용
- [ ] 문서 주석 (///) 작성
- [ ] 파일 300줄 이하
