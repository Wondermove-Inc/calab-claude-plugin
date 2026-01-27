---
title: useReducer for Complex State
impact: MEDIUM
impactDescription: Centralizes state logic, prevents inconsistent state updates
tags: state, useReducer, complex-state
---

## useReducer for Complex State

**Impact: MEDIUM - Centralizes state logic, prevents inconsistent state updates**

useReducer ensures related state changes happen together and makes state transitions explicit.

**Incorrect (related state scattered across multiple useState calls):**

```tsx
function UserForm() {
  const [values, setValues] = useState({})
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Easy to update one but forget another
  const setField = (field: string, value: string) => {
    setValues({ ...values, [field]: value })
    // Forgot to clear error!
  }
}
```

**Correct (all state transitions in one place):**

```tsx
type FormAction =
  | { type: 'SET_FIELD'; field: string; value: string }
  | { type: 'SET_ERROR'; field: string; error: string }
  | { type: 'START_SUBMIT' }
  | { type: 'SUBMIT_SUCCESS' }

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value },
        errors: { ...state.errors, [action.field]: '' } // Always clears error
      }
    // ... other cases
  }
}

function UserForm() {
  const [state, dispatch] = useReducer(formReducer, initialState)
}
```

**Why**: useReducer ensures related state changes happen together and makes state transitions explicit.

Reference: [useReducer](https://react.dev/reference/react/useReducer)
