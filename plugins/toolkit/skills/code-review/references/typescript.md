# TypeScript 코드 리뷰 가이드

## 목차
1. [타입 안전성](#1-타입-안전성)
2. [null 안전성](#2-null-안전성)
3. [불변성](#3-불변성)
4. [에러 처리](#4-에러-처리)
5. [비동기 처리](#5-비동기-처리)
6. [모듈 설계](#6-모듈-설계)

---

## 1. 타입 안전성

### 1.1 any 지양

`any`는 TypeScript의 타입 시스템을 완전히 우회한다. `any`가 코드베이스에 들어오면 전파되어 주변 코드의 타입 안전성까지 훼손하며, 런타임 에러가 컴파일 타임에 잡히지 않게 된다.

```typescript
// Bad
function parse(data: any): any {
  return data.items.map((item: any) => item.name);
}

// Good — 구체적 타입 정의
interface ApiResponse {
  items: Array<{ name: string }>;
}
function parse(data: ApiResponse): string[] {
  return data.items.map(item => item.name);
}

// Good — 타입을 모를 때는 unknown 사용
function parse(data: unknown): string[] {
  if (!isApiResponse(data)) throw new Error("Invalid response");
  return data.items.map(item => item.name);
}
```

### 1.2 타입 단언 최소화

`as` 연산자는 컴파일러에게 "내가 맞으니 믿어라"라고 말하는 것이다. 컴파일러의 타입 체크를 무시하므로, 잘못된 단언이 있어도 컴파일 에러 없이 런타임에서 실패한다. 타입 단언 대신 타입 가드를 사용하면 런타임 검증과 타입 추론을 동시에 얻는다.

```typescript
// Bad — 런타임 검증 없이 타입 강제
const user = response.data as User;

// Good — 타입 가드로 런타임 검증 + 타입 추론
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}
if (isUser(response.data)) {
  // 여기서 response.data는 User 타입으로 추론됨
}
```

### 1.3 @ts-ignore 금지

`@ts-ignore`는 해당 줄의 모든 타입 에러를 무시한다. 나중에 코드가 변경되어 새로운 타입 에러가 발생해도 경고 없이 지나가므로, 잠재적 버그가 숨겨진다. 불가피한 경우 `@ts-expect-error`를 사용하면, 에러가 해소됐을 때 알림을 받을 수 있다.

```typescript
// Bad — 모든 에러를 무시
// @ts-ignore
const value = obj.unknownProp;

// Better — 에러가 해소되면 알림
// @ts-expect-error: legacy API가 타입 정의를 제공하지 않음
const value = obj.unknownProp;

// Best — 타입을 제대로 정의
interface LegacyObj { unknownProp: string; }
const value = (obj as LegacyObj).unknownProp;
```

---

## 2. null 안전성

### 2.1 Optional chaining

중첩된 null 체크는 가독성을 심각하게 해친다. `?.`는 체인 중간에 null/undefined가 있으면 즉시 undefined를 반환하여, 깊은 중첩 없이 안전한 접근을 보장한다.

```typescript
// Bad
const city = user && user.address && user.address.city;

// Good
const city = user?.address?.city;
```

### 2.2 Nullish coalescing

`||`는 falsy 값(0, "", false)도 기본값으로 대체한다. `??`는 null/undefined만 대체하므로, 0이나 빈 문자열이 유효한 값인 경우 의도치 않은 동작을 방지한다.

```typescript
// Bad — port가 0이면 3000으로 대체됨
const port = config.port || 3000;

// Good — null/undefined일 때만 3000
const port = config.port ?? 3000;
```

### 2.3 non-null assertion 지양

`!` 연산자는 "null이 아니다"라고 컴파일러에게 단언하는 것이다. 실제로 null이면 런타임에서 `TypeError`가 발생한다. 타입 가드나 조건 체크로 대체해야 한다.

```typescript
// Bad
const el = document.getElementById("app")!;

// Good
const el = document.getElementById("app");
if (!el) throw new Error("Element #app not found");
```

---

## 3. 불변성

### 3.1 const 우선

`let`은 재할당 가능성을 의미한다. 코드를 읽는 사람은 "이 변수가 나중에 바뀌는구나"라고 기대하게 된다. 실제로 재할당하지 않는 변수에 `let`을 쓰면 불필요한 인지 부담을 준다.

```typescript
// Bad — 재할당하지 않는데 let 사용
let baseUrl = "https://api.example.com";

// Good
const baseUrl = "https://api.example.com";
```

### 3.2 readonly

객체 프로퍼티의 불변성을 타입 레벨에서 보장한다. `const`는 변수 재할당만 막지, 객체 내부 변경은 막지 못한다. `readonly`를 사용하면 컴파일 타임에 의도치 않은 변경을 차단한다.

```typescript
// Bad — 내부 변경 가능
interface Config {
  apiUrl: string;
  timeout: number;
}

// Good — 내부 변경 시 컴파일 에러
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Good — 유틸리티 타입 사용
type Config = Readonly<{
  apiUrl: string;
  timeout: number;
}>;
```

---

## 4. 에러 처리

### 4.1 구체적 에러 타입

`catch(e)`의 `e`는 `unknown` 타입이다. 타입을 확인하지 않고 사용하면 에러 객체가 아닌 값이 throw된 경우 이차 에러가 발생한다.

```typescript
// Bad — e의 타입을 가정
try {
  await fetchData();
} catch (e) {
  console.error(e.message); // e가 Error가 아닐 수 있음
}

// Good — 타입 확인 후 사용
try {
  await fetchData();
} catch (e) {
  const message = e instanceof Error ? e.message : String(e);
  console.error(message);
}
```

### 4.2 에러 무시 금지

빈 catch 블록은 에러를 삼켜버린다. 최소한 로깅이라도 해야 문제 발생 시 원인을 추적할 수 있다. 의도적으로 무시하는 경우 주석으로 이유를 명시한다.

```typescript
// Bad
try {
  await saveCache();
} catch {}

// Good — 의도적 무시 시 이유 명시
try {
  await saveCache();
} catch {
  // 캐시 저장 실패는 비즈니스 로직에 영향 없음
}
```

---

## 5. 비동기 처리

### 5.1 await 누락

Promise를 await하지 않으면 fire-and-forget이 되어, 에러가 unhandled rejection으로 프로세스를 종료시킬 수 있다. 의도적인 fire-and-forget이라면 `.catch()`를 명시한다.

```typescript
// Bad — 에러가 잡히지 않음
function handleRequest(req: Request) {
  saveAuditLog(req); // Promise 반환하지만 await 안 함
  return respond(req);
}

// Good
async function handleRequest(req: Request) {
  await saveAuditLog(req);
  return respond(req);
}

// Good — 의도적 fire-and-forget
function handleRequest(req: Request) {
  saveAuditLog(req).catch(err => logger.warn("audit log failed", err));
  return respond(req);
}
```

### 5.2 병렬 실행

독립적인 비동기 작업을 순차 실행하면 불필요한 대기 시간이 발생한다. `Promise.all()`로 병렬 실행하면 전체 소요 시간이 가장 느린 작업 하나의 시간으로 줄어든다.

```typescript
// Bad — 순차 실행 (총 시간 = A + B + C)
const users = await fetchUsers();
const orders = await fetchOrders();
const products = await fetchProducts();

// Good — 병렬 실행 (총 시간 = max(A, B, C))
const [users, orders, products] = await Promise.all([
  fetchUsers(),
  fetchOrders(),
  fetchProducts(),
]);
```

---

## 6. 모듈 설계

### 6.1 barrel export 주의

`index.ts`에서 모든 것을 re-export하면, 하나의 심볼만 import해도 전체 모듈이 로드된다. tree-shaking이 완벽하지 않은 환경(특히 CommonJS)에서 번들 크기가 불필요하게 커진다.

```typescript
// Bad — index.ts에서 모든 것을 re-export
export * from "./userService";
export * from "./orderService";
export * from "./productService";

// Good — 필요한 모듈에서 직접 import
import { UserService } from "./user/userService";
```

### 6.2 순환 의존

A → B → A 형태의 순환 참조는 초기화 순서에 따라 undefined import가 발생할 수 있다. 공통 의존성을 별도 모듈로 추출하거나, 의존 방향을 인터페이스로 역전시켜 해결한다.
