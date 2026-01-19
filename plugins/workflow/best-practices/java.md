# Java & Spring Boot 베스트 프랙티스 (2025)

> 이 문서는 Java/Spring Boot 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 프로젝트 구조 (Hexagonal Architecture)

### 1.1 패키지 구조

```
src/main/java/com/example/myapp/
├── MyAppApplication.java           # 진입점
├── domain/                          # 도메인 계층 (핵심)
│   ├── model/
│   │   ├── User.java               # 엔티티
│   │   └── UserId.java             # 값 객체
│   ├── repository/
│   │   └── UserRepository.java     # 포트 (인터페이스)
│   └── service/
│       └── UserDomainService.java  # 도메인 서비스
├── application/                     # 애플리케이션 계층
│   ├── port/
│   │   ├── in/
│   │   │   └── CreateUserUseCase.java
│   │   └── out/
│   │       └── LoadUserPort.java
│   ├── service/
│   │   └── UserApplicationService.java
│   └── dto/
│       ├── CreateUserCommand.java
│       └── UserResponse.java
├── adapter/                         # 어댑터 계층
│   ├── in/
│   │   └── web/
│   │       ├── UserController.java
│   │       └── dto/
│   │           └── CreateUserRequest.java
│   └── out/
│       └── persistence/
│           ├── UserJpaEntity.java
│           ├── UserJpaRepository.java
│           └── UserPersistenceAdapter.java
└── config/                          # 설정
    ├── SecurityConfig.java
    └── JpaConfig.java
```

---

## 2. 엔티티와 값 객체

### 2.1 JPA 엔티티

```java
package com.example.myapp.adapter.out.persistence;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

/**
 * 사용자 JPA 엔티티.
 *
 * <p>데이터베이스 테이블 매핑용 엔티티입니다.
 * 도메인 모델과 분리하여 영속성 관심사만 처리합니다.</p>
 */
@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@Builder
public class UserJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false)
    private String passwordHash;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

### 2.2 도메인 모델

```java
package com.example.myapp.domain.model;

import lombok.Builder;
import lombok.Getter;
import java.time.LocalDateTime;

/**
 * 사용자 도메인 모델.
 *
 * <p>비즈니스 로직을 포함하는 풍부한 도메인 모델입니다.</p>
 */
@Getter
@Builder
public class User {

    private final UserId id;
    private final String email;
    private String name;
    private final String passwordHash;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    /**
     * 이름 변경.
     *
     * @param newName 새로운 이름 (1~100자)
     * @throws IllegalArgumentException 이름이 유효하지 않은 경우
     */
    public void changeName(String newName) {
        validateName(newName);
        this.name = newName;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 이메일 유효성 검사.
     *
     * @return 유효한 이메일 형식이면 true
     */
    public boolean hasValidEmail() {
        return email != null && email.contains("@") && email.length() <= 255;
    }

    private void validateName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("이름은 필수입니다");
        }
        if (name.length() > 100) {
            throw new IllegalArgumentException("이름은 100자를 초과할 수 없습니다");
        }
    }
}
```

### 2.3 값 객체

```java
package com.example.myapp.domain.model;

import java.util.UUID;

/**
 * 사용자 ID 값 객체.
 *
 * @param value UUID 문자열
 */
public record UserId(String value) {

    public UserId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("ID는 필수입니다");
        }
    }

    /**
     * 새로운 UserId 생성.
     *
     * @return 랜덤 UUID 기반 UserId
     */
    public static UserId generate() {
        return new UserId(UUID.randomUUID().toString());
    }

    /**
     * 문자열에서 UserId 생성.
     *
     * @param id ID 문자열
     * @return UserId 인스턴스
     */
    public static UserId of(String id) {
        return new UserId(id);
    }
}
```

---

## 3. 유스케이스와 서비스

### 3.1 유스케이스 인터페이스 (Port In)

```java
package com.example.myapp.application.port.in;

import com.example.myapp.application.dto.CreateUserCommand;
import com.example.myapp.application.dto.UserResponse;

/**
 * 사용자 생성 유스케이스.
 */
public interface CreateUserUseCase {

    /**
     * 새로운 사용자 생성.
     *
     * @param command 생성 명령
     * @return 생성된 사용자 응답
     * @throws com.example.myapp.domain.exception.DuplicateEmailException 이메일 중복 시
     */
    UserResponse execute(CreateUserCommand command);
}
```

### 3.2 애플리케이션 서비스

```java
package com.example.myapp.application.service;

import com.example.myapp.application.dto.CreateUserCommand;
import com.example.myapp.application.dto.UserResponse;
import com.example.myapp.application.port.in.CreateUserUseCase;
import com.example.myapp.application.port.out.LoadUserPort;
import com.example.myapp.application.port.out.SaveUserPort;
import com.example.myapp.domain.exception.DuplicateEmailException;
import com.example.myapp.domain.model.User;
import com.example.myapp.domain.model.UserId;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 사용자 애플리케이션 서비스.
 *
 * <p>유스케이스를 구현하고 트랜잭션을 관리합니다.</p>
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserApplicationService implements CreateUserUseCase {

    private final LoadUserPort loadUserPort;
    private final SaveUserPort saveUserPort;
    private final PasswordEncoder passwordEncoder;

    /**
     * {@inheritDoc}
     */
    @Override
    @Transactional
    public UserResponse execute(CreateUserCommand command) {
        // 이메일 중복 검사
        if (loadUserPort.existsByEmail(command.email())) {
            throw new DuplicateEmailException(command.email());
        }

        // 도메인 모델 생성
        User user = User.builder()
                .id(UserId.generate())
                .email(command.email())
                .name(command.name())
                .passwordHash(passwordEncoder.encode(command.password()))
                .build();

        // 저장
        User savedUser = saveUserPort.save(user);

        return UserResponse.from(savedUser);
    }
}
```

### 3.3 DTO (Command & Response)

```java
package com.example.myapp.application.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * 사용자 생성 커맨드.
 *
 * @param email 이메일 (필수, 이메일 형식)
 * @param password 비밀번호 (8자 이상)
 * @param name 이름 (1~100자)
 */
public record CreateUserCommand(
        @NotBlank(message = "이메일은 필수입니다")
        @Email(message = "올바른 이메일 형식이 아닙니다")
        String email,

        @NotBlank(message = "비밀번호는 필수입니다")
        @Size(min = 8, message = "비밀번호는 8자 이상이어야 합니다")
        String password,

        @NotBlank(message = "이름은 필수입니다")
        @Size(max = 100, message = "이름은 100자를 초과할 수 없습니다")
        String name
) {
    /**
     * Request DTO에서 Command 생성.
     */
    public static CreateUserCommand from(CreateUserRequest request) {
        return new CreateUserCommand(
                request.email(),
                request.password(),
                request.name()
        );
    }
}
```

```java
package com.example.myapp.application.dto;

import com.example.myapp.domain.model.User;
import java.time.LocalDateTime;

/**
 * 사용자 응답 DTO.
 */
public record UserResponse(
        String id,
        String email,
        String name,
        LocalDateTime createdAt
) {
    /**
     * 도메인 모델에서 Response 생성.
     */
    public static UserResponse from(User user) {
        return new UserResponse(
                user.getId().value(),
                user.getEmail(),
                user.getName(),
                user.getCreatedAt()
        );
    }
}
```

---

## 4. 컨트롤러 (REST API)

### 4.1 REST 컨트롤러

```java
package com.example.myapp.adapter.in.web;

import com.example.myapp.application.dto.CreateUserCommand;
import com.example.myapp.application.dto.UserResponse;
import com.example.myapp.application.port.in.CreateUserUseCase;
import com.example.myapp.application.port.in.GetUserUseCase;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 사용자 REST 컨트롤러.
 */
@Tag(name = "Users", description = "사용자 관리 API")
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final CreateUserUseCase createUserUseCase;
    private final GetUserUseCase getUserUseCase;

    /**
     * 사용자 생성.
     *
     * @param request 생성 요청
     * @return 생성된 사용자 (201 Created)
     */
    @Operation(summary = "사용자 생성", description = "새로운 사용자를 생성합니다")
    @PostMapping
    public ResponseEntity<ApiResponse<UserResponse>> createUser(
            @Valid @RequestBody CreateUserRequest request
    ) {
        CreateUserCommand command = CreateUserCommand.from(request);
        UserResponse response = createUserUseCase.execute(command);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(ApiResponse.success(response));
    }

    /**
     * 사용자 조회.
     *
     * @param id 사용자 ID
     * @return 사용자 정보 (200 OK)
     */
    @Operation(summary = "사용자 조회", description = "ID로 사용자를 조회합니다")
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponse>> getUser(
            @PathVariable String id
    ) {
        UserResponse response = getUserUseCase.execute(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
```

### 4.2 API 응답 래퍼

```java
package com.example.myapp.adapter.in.web;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;

/**
 * 통일된 API 응답 래퍼.
 *
 * @param <T> 응답 데이터 타입
 */
@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {

    private final boolean success;
    private final T data;
    private final ErrorInfo error;

    /**
     * 성공 응답 생성.
     */
    public static <T> ApiResponse<T> success(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .build();
    }

    /**
     * 에러 응답 생성.
     */
    public static <T> ApiResponse<T> error(String code, String message) {
        return ApiResponse.<T>builder()
                .success(false)
                .error(new ErrorInfo(code, message))
                .build();
    }

    public record ErrorInfo(String code, String message) {}
}
```

---

## 5. 예외 처리

### 5.1 도메인 예외

```java
package com.example.myapp.domain.exception;

/**
 * 애플리케이션 기본 예외.
 */
public abstract class ApplicationException extends RuntimeException {

    private final String errorCode;

    protected ApplicationException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public String getErrorCode() {
        return errorCode;
    }
}
```

```java
package com.example.myapp.domain.exception;

/**
 * 이메일 중복 예외.
 */
public class DuplicateEmailException extends ApplicationException {

    public DuplicateEmailException(String email) {
        super("DUPLICATE_EMAIL", "이미 사용 중인 이메일입니다: " + email);
    }
}
```

```java
package com.example.myapp.domain.exception;

/**
 * 리소스를 찾을 수 없음 예외.
 */
public class ResourceNotFoundException extends ApplicationException {

    public ResourceNotFoundException(String resource, String id) {
        super("NOT_FOUND", resource + "을(를) 찾을 수 없습니다: " + id);
    }
}
```

### 5.2 글로벌 예외 핸들러

```java
package com.example.myapp.config;

import com.example.myapp.adapter.in.web.ApiResponse;
import com.example.myapp.domain.exception.ApplicationException;
import com.example.myapp.domain.exception.ResourceNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 글로벌 예외 핸들러.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 리소스 없음 예외 처리.
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(ResourceNotFoundException e) {
        log.warn("Resource not found: {}", e.getMessage());
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(e.getErrorCode(), e.getMessage()));
    }

    /**
     * 애플리케이션 예외 처리.
     */
    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ApiResponse<Void>> handleApplicationException(ApplicationException e) {
        log.warn("Application error: {}", e.getMessage());
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(e.getErrorCode(), e.getMessage()));
    }

    /**
     * 유효성 검증 예외 처리.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleValidation(MethodArgumentNotValidException e) {
        String message = e.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .findFirst()
                .orElse("유효성 검증 실패");

        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error("VALIDATION_ERROR", message));
    }

    /**
     * 기타 예외 처리.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleException(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ApiResponse.error("INTERNAL_ERROR", "서버 오류가 발생했습니다"));
    }
}
```

---

## 6. 테스트

### 6.1 단위 테스트

```java
package com.example.myapp.application.service;

import com.example.myapp.application.dto.CreateUserCommand;
import com.example.myapp.application.dto.UserResponse;
import com.example.myapp.application.port.out.LoadUserPort;
import com.example.myapp.application.port.out.SaveUserPort;
import com.example.myapp.domain.exception.DuplicateEmailException;
import com.example.myapp.domain.model.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserApplicationService 테스트")
class UserApplicationServiceTest {

    @Mock
    private LoadUserPort loadUserPort;

    @Mock
    private SaveUserPort saveUserPort;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserApplicationService sut;

    @Nested
    @DisplayName("사용자 생성")
    class CreateUser {

        private CreateUserCommand command;

        @BeforeEach
        void setUp() {
            command = new CreateUserCommand(
                    "test@example.com",
                    "password123",
                    "테스트 사용자"
            );
        }

        @Test
        @DisplayName("유효한 정보로 사용자 생성 성공")
        void success() {
            // given
            given(loadUserPort.existsByEmail(command.email())).willReturn(false);
            given(passwordEncoder.encode(command.password())).willReturn("hashedPassword");
            given(saveUserPort.save(any(User.class))).willAnswer(invocation -> invocation.getArgument(0));

            // when
            UserResponse result = sut.execute(command);

            // then
            assertThat(result).isNotNull();
            assertThat(result.email()).isEqualTo(command.email());
            assertThat(result.name()).isEqualTo(command.name());
        }

        @Test
        @DisplayName("중복 이메일로 생성 시 예외 발생")
        void duplicateEmail_throwsException() {
            // given
            given(loadUserPort.existsByEmail(command.email())).willReturn(true);

            // when & then
            assertThatThrownBy(() -> sut.execute(command))
                    .isInstanceOf(DuplicateEmailException.class)
                    .hasMessageContaining(command.email());
        }
    }
}
```

### 6.2 통합 테스트

```java
package com.example.myapp.adapter.in.web;

import com.example.myapp.application.port.in.CreateUserUseCase;
import com.example.myapp.application.dto.UserResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
@DisplayName("UserController 통합 테스트")
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CreateUserUseCase createUserUseCase;

    @Test
    @DisplayName("POST /api/v1/users - 사용자 생성 성공")
    void createUser_success() throws Exception {
        // given
        var request = new CreateUserRequest("test@example.com", "password123", "테스트");
        var response = new UserResponse("1", "test@example.com", "테스트", LocalDateTime.now());

        given(createUserUseCase.execute(any())).willReturn(response);

        // when & then
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.email").value("test@example.com"));
    }

    @Test
    @DisplayName("POST /api/v1/users - 유효성 검증 실패")
    void createUser_validationFailed() throws Exception {
        // given
        var request = new CreateUserRequest("invalid-email", "short", "");

        // when & then
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.success").value(false));
    }
}
```

---

## 7. 설정

### 7.1 application.yml

```yaml
spring:
  application:
    name: myapp

  datasource:
    url: jdbc:postgresql://localhost:5432/myapp
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
    driver-class-name: org.postgresql.Driver

  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        format_sql: true
        default_batch_fetch_size: 100

  jackson:
    property-naming-strategy: SNAKE_CASE
    serialization:
      write-dates-as-timestamps: false

logging:
  level:
    com.example.myapp: DEBUG
    org.springframework.web: INFO
    org.hibernate.SQL: DEBUG

---
spring:
  config:
    activate:
      on-profile: test

  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver

  jpa:
    hibernate:
      ddl-auto: create-drop
```

---

## 8. 금지 사항

- [ ] `@Autowired` 필드 주입 (생성자 주입 사용)
- [ ] `Optional.get()` 직접 호출 (orElseThrow 사용)
- [ ] 원시 타입 컬렉션 (`List` → `List<User>`)
- [ ] `@Transactional` 없이 쓰기 작업
- [ ] 도메인 모델에 JPA 어노테이션 혼재
- [ ] 컨트롤러에서 비즈니스 로직 처리
- [ ] catch 블록 비우기 (`catch (Exception e) {}`)
- [ ] System.out.println (Logger 사용)

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] 헥사고날 아키텍처 준수
- [ ] Record 타입 DTO 사용
- [ ] Bean Validation 적용
- [ ] 글로벌 예외 핸들러 구현
- [ ] Javadoc 주석 작성
- [ ] 단위 테스트 + 통합 테스트
- [ ] 파일 300줄 이하
