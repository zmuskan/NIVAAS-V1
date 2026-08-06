# NIVAAS — Frontend Foundation

Bangalore Rental Intelligence Platform. This package is the **frontend
foundation only** — application shell, design system, and infrastructure.
No feature pages (search, analytics, recommendations, property detail)
are implemented yet; each gets its own session against this foundation.

## Stack

React 19 · Vite · TypeScript (strict) · Tailwind CSS · shadcn/ui ·
React Router · TanStack Query · Axios · Leaflet · Framer Motion · Lucide

## Getting started

```bash
npm install
cp .env.example .env.local   # fill in VITE_API_BASE_URL, etc.
npm run dev
```

## Folder structure

```
src/
├── components/
│   ├── ui/            # Design-system primitives: Button, Card, Section, Typography
│   └── layout/         # App chrome: Navbar, Sidebar, Footer, LogoMark
├── layouts/            # Route-level layout shells (RootLayout)
├── router/             # React Router configuration
├── routes/             # Route-bound components not tied to a specific feature (404, placeholder)
├── providers/           # App-wide context providers (Theme, Query)
├── lib/                # Cross-cutting infrastructure: axios instance, api client, query client, cn()
├── config/             # Typed environment configuration
├── features/            # Feature modules (empty — see below)
├── hooks/               # Shared, cross-feature hooks (empty — see below)
├── types/               # Shared, cross-feature types (empty — see below)
├── styles/              # Reserved for additional stylesheets beyond index.css
├── index.css            # Tailwind entry + design tokens (shadcn CSS-variable bridge)
├── App.tsx
└── main.tsx
```

### Feature-based organization

Each product capability lives under `src/features/<feature-name>/` once
built, and is self-contained:

```
src/features/property-search/
├── api.ts            # feature-scoped calls through lib/api-client.ts
├── hooks.ts           # useQuery/useMutation hooks for this feature
├── components/         # feature-only UI, not shared elsewhere
├── types.ts            # DTOs matching the real FastAPI schema
└── index.ts             # public exports consumed by routes/router
```

Nothing is scaffolded inside `features/`, `hooks/`, or `types/` yet —
they exist so the convention is established before the first feature
lands, not to hold placeholder code.

## Design system

See `tailwind.config.ts` for the full token system (color, type scale,
spacing, shadows, motion) and its rationale, and
`src/components/ui/` for the primitives built on top of it:
`Button`, `Card` (+ subcomponents), `Section`, and the `Typography` set
(`DisplayXL/LG/SM`, `Text`, `TextLead`, `TextSmall`, `Caption`, `DataText`).

## Backend contract

This foundation makes **no assumptions about specific endpoints**. All
HTTP traffic funnels through `src/lib/axios-instance.ts` (interceptors,
error normalization) and `src/lib/api-client.ts` (typed get/post/put/
patch/delete). Feature modules define their own request functions
against the real FastAPI routes when each feature is built.
