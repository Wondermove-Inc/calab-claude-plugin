---
title: Next.js API Route Typing
impact: HIGH
impactDescription: Type-safe request/response handling
tags: typescript, nextjs, api, route, typing
---

## Next.js API Route Typing

**Impact: HIGH - Type-safe request/response handling**

Use proper TypeScript types for Next.js App Router API routes to ensure type safety for request parameters, body, and responses.

**Incorrect:**

```typescript
// app/api/users/[id]/route.ts

// Missing type definitions
export async function GET(request: Request, context: any) {
  const id = context.params.id; // any type
  const user = await getUser(id);
  return Response.json(user);
}

// No validation, no type safety
export async function PUT(request: Request, context: any) {
  const body = await request.json(); // any type
  const user = await updateUser(context.params.id, body);
  return Response.json(user);
}
```

**Correct:**

```typescript
// ============================================
// app/api/users/[id]/route.ts (Dynamic Route)
// ============================================
import { NextRequest } from 'next/server';
import { z } from 'zod';

// Type-safe params (synchronous object in App Router)
type RouteContext = {
  params: { id: string };
};

// Response type helper
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string; details?: unknown };

function jsonResponse<T>(data: ApiResponse<T>, status = 200) {
  return Response.json(data, { status });
}

// Schema for request validation
const updateUserSchema = z.object({
  name: z.string().min(1).optional(),
  email: z.string().email().optional()
});

type UpdateUserInput = z.infer<typeof updateUserSchema>;

// GET with typed params
export async function GET(
  request: NextRequest,
  context: RouteContext
): Promise<Response> {
  const { id } = context.params;

  const user = await getUser(id);
  if (!user) {
    return jsonResponse({ success: false, error: 'User not found' }, 404);
  }

  return jsonResponse({ success: true, data: user });
}

// PUT with validated body
export async function PUT(
  request: NextRequest,
  context: RouteContext
): Promise<Response> {
  const { id } = context.params;

  // Parse and validate body
  const body = await request.json();
  const result = updateUserSchema.safeParse(body);

  if (!result.success) {
    return jsonResponse({
      success: false,
      error: 'Validation failed',
      details: result.error.flatten().fieldErrors
    }, 400);
  }

  const user = await updateUser(id, result.data);
  return jsonResponse({ success: true, data: user });
}
```

```typescript
// ============================================
// app/api/users/route.ts (Collection Route - separate file)
// ============================================
import { NextRequest } from 'next/server';

// GET with search params (no dynamic segment)
export async function GET(request: NextRequest): Promise<Response> {
  const searchParams = request.nextUrl.searchParams;

  // Type-safe search param extraction
  const page = parseInt(searchParams.get('page') ?? '1', 10);
  const limit = Math.min(parseInt(searchParams.get('limit') ?? '20', 10), 100);
  const sort = (searchParams.get('sort') ?? 'desc') as 'asc' | 'desc';

  const users = await getUsers({ page, limit, sort });
  return Response.json({ success: true, data: users });
}
```

**Why**: Proper typing in API routes catches parameter mismatches and invalid body shapes at compile time. Note that dynamic route params (`[id]`) and collection routes must be in separate files. Combined with Zod validation, this ensures runtime safety for external inputs while maintaining full type inference throughout the request handler.

Reference: [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
