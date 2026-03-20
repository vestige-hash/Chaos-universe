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
    ├──> AI Provider (swappable)
    |      ├── Dev:  Ollama (local, $0)
    |      └── Prod: Claude API (direct)
    |
    ├──> Memory Layer
    |      ├── pgvector (embeddings)
    |      └── RAG pipeline (retrieval)
    |
    v
Drizzle ORM
    |
    v
PostgreSQL + pgvector
```

## LLM Provider Abstraction

The AI layer uses Vercel AI SDK's provider pattern so dev and prod use identical application code:

```typescript
// src/lib/ai/provider.ts
import { anthropic } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const ollama = createOpenAICompatible({
  name: 'ollama',
  baseURL: 'http://localhost:11434/v1',
});

export function getModel(task: 'fast' | 'standard' | 'complex' = 'standard') {
  const isDev = process.env.NODE_ENV === 'development';

  if (isDev) {
    // Free local models — no API key, no cost
    return ollama.chatModel('llama3.3:8b');
  }

  // Production — direct Claude API
  const models = {
    fast: anthropic('claude-haiku-4-5-20251001'),
    standard: anthropic('claude-sonnet-4-6-20260320'),
    complex: anthropic('claude-opus-4-6-20260320'),
  } as const;

  return models[task];
}
```

**Usage is identical regardless of provider:**
```typescript
import { generateText, streamText } from 'ai';
import { getModel } from '@/lib/ai/provider';

// Works with Ollama in dev, Claude in prod — zero code changes
const result = await streamText({
  model: getModel('standard'),
  messages: [{ role: 'user', content: 'Hello JARVIS' }],
});
```

**Environment Variables:**
```bash
# .env.local (dev) — no ANTHROPIC_API_KEY needed!
NODE_ENV=development

# .env.production — only key needed for prod
ANTHROPIC_API_KEY=sk-ant-...
```

## Core Modules
- **UI/Graphics Engine:** Interactive JARVIS-style interface with motion and visual feedback
- **Conversation Engine:** Natural language processing and context-aware responses
- **Self-Learning Module:** Adaptive behavior based on user interactions and feedback (RAG + pgvector)
- **Auth & Security:** Authentication middleware with role-based access

## Database Schemas
_(To be defined as features are built)_

## Key Design Decisions
- App Router for server-first rendering and streaming
- Drizzle ORM for type-safe database queries
- Zod for runtime validation at all system boundaries
- No default exports — named exports only for better refactoring support
