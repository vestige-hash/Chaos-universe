import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  ANTHROPIC_API_KEY: z.string().min(1).optional(),
  DATABASE_URL: z.string().url().optional(),
  OLLAMA_BASE_URL: z.string().url().default('http://localhost:11434/v1'),
  OLLAMA_MODEL: z.string().default('llama3.3:8b'),
});

type Env = z.infer<typeof envSchema>;

let _env: Env | null = null;

function validateEnv(): Env {
  const parsed = envSchema.safeParse(process.env);

  if (!parsed.success) {
    console.error('Invalid environment variables:', parsed.error.flatten().fieldErrors);
    throw new Error('Invalid environment variables');
  }

  // In production, ANTHROPIC_API_KEY is required at runtime (not build time)
  if (
    parsed.data.NODE_ENV === 'production' &&
    !parsed.data.ANTHROPIC_API_KEY &&
    !process.env.NEXT_PHASE
  ) {
    throw new Error('ANTHROPIC_API_KEY is required in production');
  }

  return parsed.data;
}

// Lazy — validates on first access, not at import time
export function getEnv(): Env {
  if (!_env) {
    _env = validateEnv();
  }
  return _env;
}
