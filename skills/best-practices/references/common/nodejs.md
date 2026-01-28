# Node.js/Express 베스트 프랙티스 (2025)

> 이 문서는 Node.js 백엔드 코드 생성 시 **반드시** 참조해야 합니다.

---

## 1. 레이어드 아키텍처

### 필수 레이어 구조

```
Controller (HTTP 처리)
    ↓
Service (비즈니스 로직)
    ↓
Repository (데이터 접근)
    ↓
Database
```

### 각 레이어 책임

```typescript
// Controller - HTTP 요청/응답만 처리
/**
 * 사용자 관련 HTTP 엔드포인트
 */
export class UserController {
  constructor(private userService: UserService) {}

  /**
   * 사용자 조회 API
   * @param req - Express Request
   * @param res - Express Response
   */
  async getUser(req: Request, res: Response): Promise<void> {
    const user = await this.userService.findById(req.params.id);
    res.json(UserMapper.toResponse(user));
  }
}

// Service - 비즈니스 로직
/**
 * 사용자 비즈니스 로직 서비스
 */
export class UserService {
  constructor(private userRepository: UserRepository) {}

  /**
   * ID로 사용자 조회
   * @param id - 사용자 ID
   * @returns 사용자 정보
   * @throws NotFoundException - 사용자가 없을 경우
   */
  async findById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundException('User not found');
    }
    return user;
  }
}

// Repository - 데이터 접근만
/**
 * 사용자 데이터 저장소
 */
export class UserRepository {
  /**
   * ID로 사용자 조회
   * @param id - 사용자 ID
   * @returns 사용자 또는 null
   */
  async findById(id: string): Promise<User | null> {
    return prisma.user.findUnique({ where: { id } });
  }
}
```

---

## 2. 디렉토리 구조

### Domain-Driven Structure (권장)

```
src/
├── features/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.types.ts
│   │   ├── dto/
│   │   │   ├── login.dto.ts
│   │   │   └── register.dto.ts
│   │   └── index.ts
│   └── users/
│       └── ...
├── shared/
│   ├── middleware/
│   ├── utils/
│   ├── types/
│   └── exceptions/
├── config/
│   └── index.ts
└── app.ts
```

---

## 3. 에러 처리

### 커스텀 에러 클래스

```typescript
// shared/exceptions/http.exception.ts

/**
 * HTTP 예외 기본 클래스
 */
export class HttpException extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

/**
 * 404 Not Found 예외
 */
export class NotFoundException extends HttpException {
  constructor(message = 'Not Found') {
    super(404, message, 'NOT_FOUND');
  }
}

/**
 * 400 Bad Request 예외
 */
export class BadRequestException extends HttpException {
  constructor(message = 'Bad Request') {
    super(400, message, 'BAD_REQUEST');
  }
}

/**
 * 401 Unauthorized 예외
 */
export class UnauthorizedException extends HttpException {
  constructor(message = 'Unauthorized') {
    super(401, message, 'UNAUTHORIZED');
  }
}

/**
 * 403 Forbidden 예외
 */
export class ForbiddenException extends HttpException {
  constructor(message = 'Forbidden') {
    super(403, message, 'FORBIDDEN');
  }
}
```

### 글로벌 에러 핸들러

```typescript
// shared/middleware/error.middleware.ts
import { ErrorRequestHandler } from 'express';
import { logger } from '../utils/logger';

/**
 * 글로벌 에러 핸들러 미들웨어
 */
export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  logger.error({
    statusCode,
    message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  res.status(statusCode).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message,
    },
  });
};
```

---

## 4. DTO 패턴

### Request DTO

```typescript
// dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator';

/**
 * 사용자 생성 요청 DTO
 */
export class CreateUserDto {
  /** 이메일 주소 */
  @IsEmail()
  email: string;

  /** 비밀번호 (최소 8자) */
  @IsString()
  @MinLength(8)
  password: string;

  /** 이름 (선택) */
  @IsString()
  @IsOptional()
  name?: string;
}
```

### Response DTO

```typescript
// dto/user-response.dto.ts

/**
 * 사용자 응답 DTO
 * 비밀번호는 절대 노출하지 않음
 */
export class UserResponseDto {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

/**
 * Entity를 Response DTO로 변환
 */
export class UserMapper {
  static toResponse(user: User): UserResponseDto {
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      createdAt: user.createdAt,
    };
  }
}
```

---

## 5. 환경 설정

### Config Module

```typescript
// config/index.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('7d'),
});

export type Config = z.infer<typeof envSchema>;

/**
 * 환경 변수 검증 및 파싱
 */
export const config = envSchema.parse(process.env);
```

---

## 6. 로깅

### 구조화된 로깅

```typescript
// shared/utils/logger.ts
import pino from 'pino';

/**
 * 구조화된 로거
 */
export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
});

/**
 * 요청 로깅 미들웨어
 */
export const requestLogger = pinoHttp({ logger });
```

---

## 7. 보안

### 보안 미들웨어

```typescript
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import cors from 'cors';

// 보안 헤더
app.use(helmet());

// CORS 설정
app.use(cors({
  origin: config.ALLOWED_ORIGINS.split(','),
  credentials: true,
}));

// Rate Limiting
app.use(rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // IP당 100 요청
}));
```

### 비밀번호 해싱

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

/**
 * 비밀번호 해싱
 */
export const hashPassword = (password: string): Promise<string> => {
  return bcrypt.hash(password, SALT_ROUNDS);
};

/**
 * 비밀번호 검증
 */
export const verifyPassword = (password: string, hash: string): Promise<boolean> => {
  return bcrypt.compare(password, hash);
};
```

---

## 8. 금지 사항

- [ ] Controller에서 직접 DB 접근
- [ ] 비즈니스 로직을 Controller에 작성
- [ ] try-catch 없는 async 함수 (또는 wrapper 미사용)
- [ ] 하드코딩된 설정값
- [ ] console.log (logger 사용)
- [ ] any 타입 사용
- [ ] 비밀번호 평문 저장
- [ ] 민감 정보 로그 출력

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] Layered Architecture 적용
- [ ] DTO 패턴 사용
- [ ] 커스텀 에러 클래스 사용
- [ ] 구조화된 로깅
- [ ] 환경 변수 검증 (zod)
- [ ] JSDoc 주석 작성
- [ ] 파일 500줄 이하
