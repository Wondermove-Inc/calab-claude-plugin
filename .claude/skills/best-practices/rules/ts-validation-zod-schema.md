---
title: Schema Validation with Zod
impact: HIGH
impactDescription: Runtime validation with inferred TypeScript types
tags: typescript, validation, zod, schema, api
---

## Schema Validation with Zod

**Impact: HIGH - Runtime validation with inferred TypeScript types**

Use Zod for runtime validation that automatically generates TypeScript types, eliminating type duplication between validation and application code.

**Incorrect:**

```typescript
// Manual type definition
interface CreateUserInput {
  name: string;
  email: string;
  age?: number;
}

// Manual validation - no connection to types
function validateCreateUser(data: unknown): CreateUserInput {
  if (typeof data !== 'object' || data === null) {
    throw new Error('Invalid input');
  }
  const obj = data as Record<string, unknown>;
  if (typeof obj.name !== 'string') {
    throw new Error('name must be a string');
  }
  if (typeof obj.email !== 'string') {
    throw new Error('email must be a string');
  }
  // Types and validation can drift apart!
  return data as CreateUserInput;
}
```

**Correct:**

```typescript
import { z } from 'zod';

// Define schema - single source of truth
const createUserSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  age: z.number().int().positive().optional()
});

// Infer TypeScript type from schema
type CreateUserInput = z.infer<typeof createUserSchema>;

// Validation automatically matches the type
function validateCreateUser(data: unknown): CreateUserInput {
  return createUserSchema.parse(data); // Throws ZodError on failure
}

// Safe parse for non-throwing validation
function safeValidateUser(data: unknown) {
  const result = createUserSchema.safeParse(data);
  if (!result.success) {
    return { ok: false, errors: result.error.flatten() } as const;
  }
  return { ok: true, data: result.data } as const;
}

// Next.js API route example
export async function POST(request: Request) {
  const body = await request.json();
  const result = createUserSchema.safeParse(body);

  if (!result.success) {
    return Response.json(
      { errors: result.error.flatten().fieldErrors },
      { status: 400 }
    );
  }

  // result.data is fully typed as CreateUserInput
  const user = await createUser(result.data);
  return Response.json(user);
}

// Composing schemas
const updateUserSchema = createUserSchema.partial(); // All fields optional
const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
});
```

**Why**: Zod provides runtime validation with automatic TypeScript type inference. This eliminates duplicate type definitions, ensures validation and types stay in sync, and provides detailed error messages. Essential for API boundaries where external data enters the application.

Reference: [Zod Documentation](https://zod.dev/)
