import { streamText } from 'ai';
import type { ModelMessage } from '@ai-sdk/provider-utils';
import { getModel } from '@/lib/ai/provider';
import { JARVIS_SYSTEM_PROMPT } from '@/lib/ai/system-prompt';

export async function POST(req: Request) {
  const { messages } = await req.json() as {
    messages: Array<{ role: string; content: string }>;
  };

  const modelMessages: ModelMessage[] = messages.map((m) => ({
    role: m.role as 'user' | 'assistant',
    content: m.content,
  }));

  const result = streamText({
    model: getModel('standard'),
    system: JARVIS_SYSTEM_PROMPT,
    messages: modelMessages,
  });

  return result.toTextStreamResponse();
}
