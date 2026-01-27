---
title: Type Guards with is Predicate
impact: HIGH
impactDescription: Runtime type narrowing with compile-time safety
tags: typescript, types, type-guards, narrowing, predicate
---

## Type Guards with is Predicate

**Impact: HIGH - Runtime type narrowing with compile-time safety**

Use type predicates (`is` keyword) to create custom type guards that narrow types at runtime while providing compile-time type information.

**Incorrect:**

```typescript
interface User {
  type: 'user';
  name: string;
  email: string;
}

interface Admin {
  type: 'admin';
  name: string;
  permissions: string[];
}

type Person = User | Admin;

// Returns boolean - TypeScript doesn't narrow the type
function checkAdmin(person: Person): boolean {
  return person.type === 'admin';
}

function handlePerson(person: Person) {
  if (checkAdmin(person)) {
    // Error: Property 'permissions' does not exist on type 'Person'
    console.log(person.permissions);
  }
}
```

**Correct:**

```typescript
interface User {
  type: 'user';
  name: string;
  email: string;
}

interface Admin {
  type: 'admin';
  name: string;
  permissions: string[];
}

type Person = User | Admin;

// Type predicate narrows the type
function isAdmin(person: Person): person is Admin {
  return person.type === 'admin';
}

function isUser(person: Person): person is User {
  return person.type === 'user';
}

function handlePerson(person: Person) {
  if (isAdmin(person)) {
    // TypeScript knows person is Admin here
    console.log(person.permissions); // OK!
  } else {
    // TypeScript knows person is User here
    console.log(person.email); // OK!
  }
}

// Works with arrays too
const people: Person[] = getPeople();
const admins = people.filter(isAdmin); // Type: Admin[]

// Guard for unknown data (API responses, etc.)
function isValidUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'type' in data &&
    (data as User).type === 'user' &&
    'name' in data &&
    typeof (data as User).name === 'string'
  );
}
```

**Why**: Type predicates (`is` keyword) tell TypeScript to narrow the type after the guard returns true. This enables type-safe runtime validation while maintaining full IntelliSense and compile-time checking. Essential for handling union types and unknown data.

Reference: [TypeScript Handbook - Type Guards](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)
