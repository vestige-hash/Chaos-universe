import { anthropic } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { getEnv } from '@/lib/env';

export type ModelTier = 'fast' | 'standard' | 'complex';

export function getModel(task: ModelTier = 'standard') {
  const env = getEnv();
  const isDev = env.NODE_ENV === 'development';

  if (isDev) {
    const ollama = createOpenAICompatible({
      name: 'ollama',
      baseURL: env.OLLAMA_BASE_URL,
    });
    // Free local model — no API key, no cost
    return ollama.chatModel(env.OLLAMA_MODEL);
  }

  // Production — direct Claude API
  const models = {
    fast: anthropic('claude-haiku-4-5-20251001'),
    standard: anthropic('claude-sonnet-4-6-20260320'),
    complex: anthropic('claude-opus-4-6-20260320'),
  } as const;

  return models[task];
}
