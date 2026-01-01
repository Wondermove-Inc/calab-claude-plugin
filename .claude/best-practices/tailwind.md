# Tailwind CSS 베스트 프랙티스 (2025)

> 이 문서는 Tailwind CSS 스타일링 시 **반드시** 참조해야 합니다.

---

## 1. 유틸리티 클래스 기본

### 1.1 레이아웃 (Flexbox & Grid)

```tsx
// Flexbox 레이아웃
<div className="flex items-center justify-between gap-4">
  <span>Left</span>
  <span>Right</span>
</div>

// Flex 컨테이너 패턴
<div className="flex flex-col md:flex-row items-start md:items-center gap-4">
  {/* 모바일: 세로, 태블릿+: 가로 */}
</div>

// Grid 레이아웃
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <Card />
  <Card />
  <Card />
</div>

// 12 컬럼 Grid
<div className="grid grid-cols-12 gap-4">
  <aside className="col-span-12 md:col-span-3">Sidebar</aside>
  <main className="col-span-12 md:col-span-9">Content</main>
</div>
```

### 1.2 간격 (Spacing)

```tsx
// 일관된 간격 스케일 사용
// 4px 단위: 1=4px, 2=8px, 4=16px, 6=24px, 8=32px

// Padding
<div className="p-4">         {/* 16px 전체 */}
<div className="px-6 py-4">   {/* 좌우 24px, 상하 16px */}
<div className="pt-8 pb-4">   {/* 상 32px, 하 16px */}

// Margin
<div className="mt-6 mb-4">   {/* 상 24px, 하 16px */}
<div className="mx-auto">     {/* 좌우 중앙 정렬 */}

// Gap (Flex/Grid)
<div className="flex gap-4">  {/* 자식 간 16px 간격 */}
<div className="gap-x-4 gap-y-2"> {/* 가로 16px, 세로 8px */}

// 섹션 간격 표준
<section className="py-12 md:py-16 lg:py-24">
  {/* 반응형 세로 패딩 */}
</section>
```

### 1.3 타이포그래피

```tsx
// 텍스트 크기 스케일
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">
  Heading 1
</h1>
<h2 className="text-2xl md:text-3xl font-semibold">
  Heading 2
</h2>
<p className="text-base text-gray-600 leading-relaxed">
  Body text with relaxed line height
</p>
<small className="text-sm text-gray-500">
  Small text
</small>

// 텍스트 유틸리티
<p className="font-medium tracking-tight">     {/* 세미볼드, 좁은 자간 */}
<p className="text-center md:text-left">       {/* 반응형 정렬 */}
<p className="truncate">                       {/* 말줄임 */}
<p className="line-clamp-3">                   {/* 3줄 제한 */}
```

---

## 2. 반응형 디자인

### 2.1 브레이크포인트

```tsx
// Tailwind 기본 브레이크포인트
// sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px

// 모바일 퍼스트 접근
<div className="
  w-full          /* 모바일: 전체 너비 */
  sm:w-1/2        /* 640px+: 50% */
  md:w-1/3        /* 768px+: 33% */
  lg:w-1/4        /* 1024px+: 25% */
">

// 컨테이너 패턴
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  {/* 반응형 좌우 패딩 */}
</div>

// 반응형 숨기기/보이기
<div className="hidden md:block">      {/* 태블릿 이상에서만 */}
<div className="block md:hidden">      {/* 모바일에서만 */}
<div className="invisible lg:visible"> {/* 레이아웃 유지하며 숨김 */}
```

### 2.2 반응형 컴포넌트 예시

```tsx
/**
 * 반응형 카드 그리드.
 */
function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="
      grid
      grid-cols-1
      sm:grid-cols-2
      lg:grid-cols-3
      xl:grid-cols-4
      gap-4
      md:gap-6
    ">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

/**
 * 반응형 네비게이션.
 */
function Navigation() {
  return (
    <nav className="flex items-center justify-between px-4 py-3 md:px-6 lg:px-8">
      <Logo className="h-8 md:h-10" />

      {/* 데스크톱 메뉴 */}
      <ul className="hidden md:flex items-center gap-6">
        <NavItem href="/products">제품</NavItem>
        <NavItem href="/about">소개</NavItem>
        <NavItem href="/contact">연락처</NavItem>
      </ul>

      {/* 모바일 햄버거 */}
      <button className="md:hidden p-2">
        <MenuIcon className="w-6 h-6" />
      </button>
    </nav>
  );
}
```

---

## 3. 색상 시스템

### 3.1 시맨틱 색상 정의 (tailwind.config.js)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // 시맨틱 컬러 (CSS 변수 참조)
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
    },
  },
};
```

### 3.2 색상 사용 패턴

```tsx
// 시맨틱 색상 사용 (권장)
<button className="bg-primary text-primary-foreground hover:bg-primary/90">
  Primary Button
</button>

<button className="bg-destructive text-destructive-foreground">
  Delete
</button>

<p className="text-muted-foreground">
  Secondary text
</p>

// 상태별 색상
<span className="text-green-600 dark:text-green-400">Success</span>
<span className="text-yellow-600 dark:text-yellow-400">Warning</span>
<span className="text-red-600 dark:text-red-400">Error</span>

// 다크모드 지원
<div className="bg-white dark:bg-gray-900">
  <p className="text-gray-900 dark:text-gray-100">
    자동 다크모드 전환
  </p>
</div>
```

---

## 4. 컴포넌트 패턴

### 4.1 버튼 variants (CVA 사용)

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

/**
 * 버튼 스타일 variants.
 */
const buttonVariants = cva(
  // 기본 클래스
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

/**
 * 버튼 컴포넌트.
 */
function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

// 사용
<Button variant="default">Default</Button>
<Button variant="destructive" size="lg">Delete</Button>
<Button variant="outline" size="sm">Cancel</Button>
```

### 4.2 카드 컴포넌트

```tsx
/**
 * 카드 컴포넌트.
 */
function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        'rounded-lg border bg-card text-card-foreground shadow-sm',
        className
      )}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('flex flex-col space-y-1.5 p-6', className)}
      {...props}
    />
  );
}

function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  );
}

function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('p-6 pt-0', className)} {...props} />
  );
}

// 사용
<Card>
  <CardHeader>
    <CardTitle>제목</CardTitle>
  </CardHeader>
  <CardContent>
    <p>내용</p>
  </CardContent>
</Card>
```

### 4.3 폼 입력

```tsx
/**
 * 입력 필드 컴포넌트.
 */
function Input({ className, type, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      type={type}
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2',
        'text-sm ring-offset-background',
        'file:border-0 file:bg-transparent file:text-sm file:font-medium',
        'placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  );
}

/**
 * 라벨 컴포넌트.
 */
function Label({ className, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label
      className={cn(
        'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
        className
      )}
      {...props}
    />
  );
}

// 사용
<div className="space-y-2">
  <Label htmlFor="email">이메일</Label>
  <Input id="email" type="email" placeholder="email@example.com" />
</div>
```

---

## 5. 애니메이션

### 5.1 트랜지션

```tsx
// 기본 트랜지션
<button className="transition-colors duration-200 hover:bg-gray-100">
  Hover me
</button>

// 스케일 효과
<div className="transition-transform duration-200 hover:scale-105">
  Scale on hover
</div>

// 다중 속성
<div className="transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1">
  Lift effect
</div>

// 그룹 호버
<div className="group relative">
  <img src="..." className="transition-opacity group-hover:opacity-75" />
  <div className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity group-hover:opacity-100">
    <button>View</button>
  </div>
</div>
```

### 5.2 커스텀 애니메이션 (tailwind.config.js)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in-right': {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-out',
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        shimmer: 'shimmer 2s linear infinite',
      },
    },
  },
};

// 사용
<div className="animate-fade-in">Fade in</div>
<div className="animate-slide-in-right">Slide in</div>

// 스켈레톤 로딩
<div className="animate-shimmer bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%]">
  Loading...
</div>
```

---

## 6. 유틸리티 함수

### 6.1 cn 함수 (clsx + tailwind-merge)

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Tailwind 클래스 병합 유틸리티.
 *
 * @param inputs - 클래스 값들
 * @returns 병합된 클래스 문자열
 *
 * @example
 * cn('px-2 py-1', 'px-4')  // 'py-1 px-4' (충돌 해결)
 * cn('text-red-500', condition && 'text-blue-500')
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 사용 예시
function Component({ className, isActive }: Props) {
  return (
    <div
      className={cn(
        'base-class',
        isActive && 'active-class',
        className  // 외부에서 전달된 클래스가 우선
      )}
    />
  );
}
```

---

## 7. 성능 최적화

### 7.1 PurgeCSS 설정

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  // ... 프로덕션 빌드 시 사용하지 않는 클래스 제거
};
```

### 7.2 JIT 모드 활용

```tsx
// 임의 값 사용 (JIT 모드)
<div className="w-[347px]">      {/* 정확한 너비 */}
<div className="h-[calc(100vh-64px)]">  {/* 계산된 높이 */}
<div className="bg-[#1a1a1a]">  {/* 커스텀 색상 */}
<div className="grid-cols-[1fr_2fr_1fr]">  {/* 커스텀 그리드 */}

// 그룹/피어 수정자
<div className="group">
  <span className="group-hover:text-blue-500">Hover parent</span>
</div>

<input className="peer" />
<span className="peer-invalid:text-red-500">Error message</span>
```

---

## 8. 금지 사항

- [ ] 인라인 style 속성 (`style={{}}`)
- [ ] !important 강제 (`!text-red-500`)
- [ ] 임의 값 남용 (`w-[123px]` 대신 스케일 사용)
- [ ] @apply 과도한 사용 (유틸리티 클래스 직접 사용)
- [ ] 클래스 문자열 동적 생성 (`text-${color}-500` ❌)
- [ ] 중복 클래스 (`px-4 px-6` → 하나만)
- [ ] 하드코딩 색상 (`text-[#ff0000]` → 시맨틱 컬러)

---

## 9. 체크리스트

코드 생성 시 확인:

- [ ] 모바일 퍼스트 반응형 적용
- [ ] 시맨틱 컬러 사용
- [ ] cn() 함수로 클래스 병합
- [ ] 다크모드 지원 (dark: 접두사)
- [ ] 접근성 고려 (focus-visible 등)
- [ ] CVA로 variant 관리
- [ ] 일관된 간격 스케일 사용
