# Architecture — Chaos Universe

## Overview
Chaos Universe is a self-learning AI assistant platform inspired by Jarvis from Iron Man, built with Next.js 15, TypeScript, and PostgreSQL.

## High-Level Data Flow
```
User Interface (Next.js App Router)
    |
    v
API Routes / Server Actions
    |
    v
Service Layer (Business Logic)
    |
    v
Drizzle ORM
    |
    v
PostgreSQL
```

## Core Modules
- **UI/Graphics Engine:** Interactive JARVIS-style interface with motion and visual feedback
- **Conversation Engine:** Natural language processing and context-aware responses
- **Self-Learning Module:** Adaptive behavior based on user interactions and feedback
- **Auth & Security:** Authentication middleware with role-based access

## Database Schemas
_(To be defined as features are built)_

## Key Design Decisions
- App Router for server-first rendering and streaming
- Drizzle ORM for type-safe database queries
- Zod for runtime validation at all system boundaries
- No default exports — named exports only for better refactoring support
