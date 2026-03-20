'use client';

import { useChat } from '@ai-sdk/react';
import { useState, useRef, useEffect, type FormEvent } from 'react';

export function Chat() {
  const { messages, sendMessage, status, error } = useChat();
  const [input, setInput] = useState('');
  const [mounted, setMounted] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const isLoading = status === 'streaming' || status === 'submitted';

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    const text = input;
    setInput('');
    await sendMessage({ text });
  };

  if (!mounted) return null;

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="border-b border-cyan-900/30 px-6 py-4 flex items-center gap-3">
        <div className="h-3 w-3 rounded-full bg-cyan-400 animate-pulse" />
        <h1 className="text-cyan-400 text-lg tracking-widest uppercase">
          Jarvis
        </h1>
        <span className="text-zinc-600 text-sm ml-auto">
          Chaos Universe v0.1
        </span>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-cyan-400/20 text-6xl mb-4">&#9678;</div>
            <p className="text-zinc-500 text-lg">
              Good evening. How may I assist you?
            </p>
            <p className="text-zinc-700 text-sm mt-2">
              JARVIS is online. All systems nominal.
            </p>
          </div>
        )}

        {messages.map((message) => {
          const text = message.parts
            ?.filter((p) => p.type === 'text')
            .map((p) => p.text)
            .join('') ?? '';

          return (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-2xl rounded-lg px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                  message.role === 'user'
                    ? 'bg-zinc-800 text-zinc-100 border border-zinc-700'
                    : 'bg-cyan-950/30 text-cyan-100 border border-cyan-900/40'
                }`}
              >
                {message.role === 'assistant' && (
                  <span className="text-cyan-500 text-xs uppercase tracking-wider block mb-1">
                    Jarvis
                  </span>
                )}
                {text}
              </div>
            </div>
          );
        })}

        {isLoading && messages[messages.length - 1]?.role === 'user' && (
          <div className="flex justify-start">
            <div className="bg-cyan-950/30 border border-cyan-900/40 rounded-lg px-4 py-3">
              <span className="text-cyan-500 text-xs uppercase tracking-wider block mb-1">
                Jarvis
              </span>
              <span className="text-cyan-400 animate-pulse">Processing...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-950/30 border border-red-800/40 rounded-lg px-4 py-3 text-red-400 text-sm">
            Connection error: {error.message}
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={onSubmit} className="border-t border-cyan-900/30 px-6 py-4">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Speak, and I shall assist..."
            className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-cyan-700 focus:ring-1 focus:ring-cyan-700 text-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-cyan-900/50 border border-cyan-700 text-cyan-400 px-6 py-3 rounded-lg text-sm uppercase tracking-wider hover:bg-cyan-800/50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
