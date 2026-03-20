# Chaos Universe — Technology Stack Analysis

> Full skills audit for building a self-learning AI assistant that surpasses Jarvis.

---

## LAYER 1: CORE INTELLIGENCE (The Brain)

### 1.1 Claude API (Anthropic) — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | LLM API with best-in-class tool use, long context (200K), and agentic capabilities |
| **Pros** | Superior instruction following, native tool/function calling, Claude Agent SDK for agentic workflows, excellent code generation, strong safety/alignment |
| **Cons** | No fine-tuning available, no free tier for API, closed-source |
| **Cost** | Haiku 4.5: $1/$5 per MTok, Sonnet 4.6: $3/$15, Opus 4.6: $5/$25 |
| **Risk** | Vendor lock-in; API rate limits during traffic spikes |
| **Fit** | 9/10 — Best tool-use and agentic reasoning for a JARVIS-style assistant |

### 1.2 OpenAI GPT-5.2

| Attribute | Detail |
|-----------|--------|
| **What** | Latest OpenAI flagship with top reasoning and agentic performance |
| **Pros** | Massive ecosystem, Realtime API for voice, function calling, GPT-5.2 strong on benchmarks |
| **Cons** | More expensive output tokens ($14/MTok), inconsistent instruction following vs Claude |
| **Cost** | GPT-5.2: $1.75/$14 per MTok; GPT-4.1-mini: much cheaper for simple tasks |
| **Risk** | Rapid deprecation cycles (GPT-4o already deprecated) |
| **Fit** | 8/10 — Strong alternative, better Realtime API for voice |

### 1.3 Google Gemini 2.5/3.x

| Attribute | Detail |
|-----------|--------|
| **What** | Google's multimodal LLM with 1M token context and free tier |
| **Pros** | Generous free tier (6 models free), 1M context window, cheapest per-token pricing, built-in Google Search grounding, native image generation |
| **Cons** | Weaker agentic behavior, less reliable tool use, 2.0 models being deprecated June 2026 |
| **Cost** | Gemini 2.5 Flash: $0.30/$2.50; Gemini 2.5 Pro: $1.25/$10; Free tier: generous |
| **Risk** | Rapid deprecation; weaker for complex multi-step tasks |
| **Fit** | 7/10 — Great as a secondary/cheap model for simple tasks and multimodal input |

### 1.4 Open-Source LLMs (Llama 4, Mistral, Qwen)

| Attribute | Detail |
|-----------|--------|
| **What** | Self-hosted models for privacy, cost control, and customization |
| **Pros** | Free to run, full data privacy, fine-tunable, no rate limits |
| **Cons** | Llama 4 Maverick needs 350GB+ VRAM even quantized, significant DevOps overhead, weaker than commercial APIs |
| **Cost** | Free (software), but GPU hardware: $2-10K/mo for capable setups |
| **Risk** | Massive infrastructure burden; models lag behind commercial offerings |
| **Fit** | 5/10 — Not recommended for v1; revisit when project scales |

**RECOMMENDATION:** **Claude API via OpenRouter** as primary brain, **Gemini Flash Lite** as cheap secondary. OpenRouter provides multi-model access through a single API key with automatic failover.

---

## LAYER 1.5: API GATEWAY — OPENROUTER — RECOMMENDED

> **Why OpenRouter?** Single API key for 300+ models, automatic failover (Anthropic -> Bedrock -> Vertex), pass-through pricing with no per-token markup. You already have access.

### OpenRouter Overview

| Attribute | Detail |
|-----------|--------|
| **What** | Unified API gateway for 300+ LLM models from all major providers |
| **Pricing** | Pass-through (same as provider) + 5.5% fee on credit purchases (min $0.80) |
| **Streaming** | Full SSE support; `stream: true` with cancellation support |
| **Tool Use** | Full function calling / tool use with Claude models (OpenAI-format `tools` param) |
| **STT/TTS** | Not available — use self-hosted solutions (see Layer 4) |
| **Rate Limits** | No OpenRouter-enforced limits on paid models; only upstream provider limits apply |

### Claude Models on OpenRouter

| Model | Input/MTok | Output/MTok | Context | Best For |
|-------|-----------|-------------|---------|----------|
| **Claude Opus 4.6** | $5.00 | $25.00 | 1M | Complex reasoning, architecture decisions |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | 1M | Standard tasks, tool use, coding |
| **Claude Haiku 4.5** | ~$1.00 | ~$5.00 | 200K | Lightweight tasks, classification |

### Cheap Models for Task Routing

| Model | Input/MTok | Output/MTok | Use Case |
|-------|-----------|-------------|----------|
| **Gemini 2.0 Flash Lite** | $0.075 | $0.30 | Ultra-cheap classification, routing |
| **DeepSeek V3.2** | $0.25 | $0.38 | ~90% of GPT-5.4 at 1/50th cost |
| **Free models** (DeepSeek R1, Llama 3.3 70B) | $0 | $0 | Development/testing (rate-limited) |

### TypeScript Integration

| Package | Purpose |
|---------|---------|
| **`@openrouter/sdk`** | Official SDK — direct control, Zod schemas for tool calls, streaming |
| **`@openrouter/ai-sdk-provider`** | Vercel AI SDK provider — best for Next.js integration |
| **OpenAI SDK compat** | Use standard `openai` npm package with base URL `https://openrouter.ai/api/v1` |

### Recommended Routing Chain

```
User Query -> Classifier (Gemini Flash Lite: $0.075/MTok)
  ├── Simple task -> Claude Haiku 4.5 ($1/MTok)
  ├── Standard task -> Claude Sonnet 4.6 ($3/MTok)
  └── Complex reasoning -> Claude Opus 4.6 ($5/MTok)
```

### OpenRouter vs Anthropic Direct

| Factor | OpenRouter | Anthropic Direct |
|--------|-----------|-----------------|
| **Multi-model** | 300+ models, one key | Claude only |
| **Failover** | Automatic across providers | Build yourself |
| **Latency** | +50-70ms routing overhead | Lowest possible |
| **Features** | Normalized to OpenAI format | Full Anthropic features day-one |
| **Best for** | Multi-model routing (our use case) | Claude-only apps needing bleeding-edge features |

**VERDICT:** OpenRouter is the right choice — we need multi-model routing for cost optimization, and the 50-70ms overhead is negligible for an AI assistant.

---

## LAYER 2: AGENTIC FRAMEWORK (The Nervous System)

### 2.1 Claude Agent SDK — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Anthropic's official SDK for building multi-step AI agents |
| **Pros** | Native Claude integration, built for tool use and agentic loops, TypeScript support |
| **Cons** | Newer ecosystem, Claude-specific |
| **Cost** | Free (SDK); pay for API usage |
| **Risk** | Tied to Anthropic ecosystem |
| **Fit** | 9/10 — Purpose-built for what we're building |

### 2.2 LangChain / LangGraph

| Attribute | Detail |
|-----------|--------|
| **What** | Most popular framework for chaining LLM calls, RAG, and agent workflows |
| **Pros** | Huge ecosystem, model-agnostic, LangGraph for stateful agents, strong community |
| **Cons** | Over-abstracted, heavy dependency tree, frequent breaking changes, "framework lock-in" |
| **Cost** | Free (open-source); LangSmith observability: $39/user/mo |
| **Risk** | Abstraction overhead; hard to debug when things go wrong |
| **Fit** | 6/10 — Useful for RAG pipelines, but avoid for core agent logic |

### 2.3 Vercel AI SDK

| Attribute | Detail |
|-----------|--------|
| **What** | Streaming-first AI SDK built for Next.js with multi-provider support |
| **Pros** | Native Next.js/React integration, streaming UI components, model-agnostic, TypeScript-first |
| **Cons** | Vercel-centric, less mature for complex agent workflows |
| **Cost** | Free (open-source) |
| **Risk** | Less capable for complex multi-agent orchestration |
| **Fit** | 8/10 — Excellent for the UI layer and streaming responses |

**RECOMMENDATION:** **Claude Agent SDK** for core agent logic + **Vercel AI SDK** for streaming UI integration. Avoid LangChain as primary framework.

---

## LAYER 3: MEMORY & SELF-LEARNING (The Hippocampus)

### 3.1 pgvector (PostgreSQL Extension) — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Vector similarity search directly in PostgreSQL |
| **Pros** | No new infrastructure (uses existing PostgreSQL), works with Drizzle ORM, HNSW indexing, simple |
| **Cons** | Slower than dedicated vector DBs at extreme scale (10M+ vectors), limited filtering options |
| **Cost** | Free (open-source extension) |
| **Risk** | Performance ceiling at very large scale |
| **Fit** | 9/10 — Perfect fit since we're already on PostgreSQL |

### 3.2 Pinecone

| Attribute | Detail |
|-----------|--------|
| **What** | Managed vector database purpose-built for AI applications |
| **Pros** | Fast at scale, serverless option, managed infrastructure, metadata filtering |
| **Cons** | Vendor lock-in, costs scale with storage, another service to manage |
| **Cost** | Free tier: 5M vectors; Starter: ~$70/mo; scales with usage |
| **Risk** | Cost escalation; external dependency |
| **Fit** | 7/10 — Consider if pgvector hits performance limits |

### 3.3 RAG Pipeline (Retrieval-Augmented Generation)

| Attribute | Detail |
|-----------|--------|
| **What** | Pattern for grounding AI responses in user-specific knowledge |
| **Pros** | Enables personalization without fine-tuning, works with any LLM, updateable in real-time |
| **Cons** | Requires good chunking strategy, embedding quality matters, retrieval can miss context |
| **Cost** | Embedding costs: ~$0.10/MTok (OpenAI), free with local models |
| **Risk** | Poor retrieval = hallucination; requires ongoing tuning |
| **Fit** | 10/10 — Essential for self-learning; this is how JARVIS "remembers" |

### 3.4 Knowledge Graphs (Neo4j / in-PostgreSQL)

| Attribute | Detail |
|-----------|--------|
| **What** | Structured relationship mapping between entities the AI learns about |
| **Pros** | Superior for relationship queries, reasoning chains, "connecting dots" |
| **Cons** | Complex to implement, requires schema design upfront |
| **Cost** | Neo4j free tier available; or use PostgreSQL recursive CTEs |
| **Risk** | Over-engineering for v1 |
| **Fit** | 6/10 — Add in v2 for advanced reasoning |

**RECOMMENDATION:** **pgvector** for vector storage + **RAG pipeline** for self-learning from day one. Add Pinecone or knowledge graphs later if needed.

---

## LAYER 4: VOICE INTERFACE (The Mouth & Ears) — FREE & OPEN-SOURCE

> **Strategy shift:** Free, self-hosted voice stack using open-source GitHub projects.
> Paid services (Deepgram, ElevenLabs) remain as optional premium upgrades.

### 4.1 SPEECH-TO-TEXT (STT) — FREE OPTIONS

#### 4.1a Transformers.js + Whisper (Browser) — RECOMMENDED FOR MVP

| Attribute | Detail |
|-----------|--------|
| **What** | Hugging Face's Whisper models running in-browser via WebAssembly/WebGPU |
| **GitHub** | [huggingface/transformers.js](https://github.com/huggingface/transformers.js) — ~14k stars |
| **License** | Apache-2.0 |
| **Languages** | 99+ (Whisper multilingual models) |
| **Runs in** | Browser (client-side) and Node.js |
| **npm** | `@huggingface/transformers` (v3.x) |
| **Accuracy** | Same as Whisper model used; tiny = lower, small/medium = near-commercial |
| **Cost** | **$0 — completely free** |
| **Fit** | 9/10 — Zero server costs, privacy-first, offline-capable |

**Integration:**
```typescript
// Client component with "use client"
import { pipeline } from '@huggingface/transformers';
const transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny.en');
const result = await transcriber(audioBuffer);
```

#### 4.1b Moonshine JS (Browser, Ultra-Fast)

| Attribute | Detail |
|-----------|--------|
| **What** | Purpose-built on-device STT with built-in VAD and streaming |
| **GitHub** | [moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine) — ~3k stars |
| **License** | MIT |
| **Languages** | English (primary) |
| **Runs in** | Browser (on-device, 26MB model) |
| **npm** | `@moonshine-ai/moonshine-js` |
| **Speed** | 5x faster than Whisper for short segments; bounded time-to-first-token |
| **Cost** | **$0** |
| **Fit** | 8/10 — Best for real-time voice commands; English-only limitation |

#### 4.1c faster-whisper (Server, Production) — RECOMMENDED FOR PRODUCTION

| Attribute | Detail |
|-----------|--------|
| **What** | Optimized Whisper via CTranslate2; 4x faster, less memory, 8-bit quantization |
| **GitHub** | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) — ~22k stars |
| **License** | MIT |
| **Languages** | 99+ |
| **Runs on** | Server (Python, Docker) |
| **Accuracy** | Large-v3: 2.7% WER (near human-level 4-6.8% WER) |
| **Ecosystem** | Speaches (OpenAI-compatible API server), WhisperLive (real-time WebSocket streaming) |
| **Cost** | **$0** (self-hosted) |
| **Fit** | 10/10 — Deploy via Docker, call from Next.js API routes using OpenAI SDK format |

#### 4.1d sherpa-onnx (Native Node.js, No Python)

| Attribute | Detail |
|-----------|--------|
| **What** | ONNX-based ASR with native Node.js addon — runs directly in Next.js API routes |
| **GitHub** | [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) — ~10.7k stars |
| **License** | Apache-2.0 |
| **Languages** | Multiple models available |
| **npm** | `sherpa-onnx` |
| **Features** | Streaming + non-streaming ASR, VAD, speaker diarization, TTS (all-in-one) |
| **Cost** | **$0** |
| **Fit** | 8/10 — No Python dependency; installs as npm package |

#### 4.1e whisper.cpp (Server, Maximum Performance)

| Attribute | Detail |
|-----------|--------|
| **What** | C/C++ port of Whisper; 2-10x faster than Python; CUDA/Vulkan/Metal GPU support |
| **GitHub** | [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) — ~48k stars |
| **License** | MIT |
| **WASM** | Browser build available; built-in real-time stream mode |
| **Cost** | **$0** |
| **Fit** | 8/10 — Best raw performance on CPU; call as subprocess from Node.js |

#### 4.1f Web Speech API (Browser Fallback)

| Attribute | Detail |
|-----------|--------|
| **What** | Built-in browser speech recognition |
| **Pros** | Zero setup, no downloads, instant |
| **Cons** | Chrome-only reliable, sends audio to Google servers, no custom vocabulary |
| **Cost** | **$0** |
| **Fit** | 4/10 — Prototype/fallback only |

### 4.2 TEXT-TO-SPEECH (TTS) — FREE OPTIONS

#### 4.2a Kokoro TTS (Browser + Server) — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | High-quality neural TTS that runs in browser via ONNX and on server |
| **GitHub** | [hexgrad/kokoro](https://github.com/hexgrad/kokoro) — ~14k stars |
| **License** | Apache-2.0 |
| **Quality** | Near-commercial quality; ranked #1 on open-source TTS leaderboards |
| **Speed** | Real-time factor ~10-35x (generates speech 10-35x faster than real-time) |
| **Languages** | English, Japanese, Chinese, Korean, French, and more |
| **Runs in** | Browser (ONNX.js / kokoro-js), Server (Python), or via sherpa-onnx |
| **npm** | `kokoro-js` (browser/Node.js ONNX runtime) |
| **Cost** | **$0** |
| **Fit** | 10/10 — Best free TTS; runs in browser = zero server cost for TTS |

**Integration:**
```typescript
// Browser: kokoro-js with ONNX runtime
import { KokoroTTS } from 'kokoro-js';
const tts = await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX');
const audio = await tts.generate('Hello, I am your JARVIS assistant.', { voice: 'af_heart' });
```

#### 4.2b Piper TTS (Server, Lightning Fast)

| Attribute | Detail |
|-----------|--------|
| **What** | Lightweight C++ TTS optimized for speed; runs on Raspberry Pi |
| **GitHub** | [rhasspy/piper](https://github.com/rhasspy/piper) — ~8k stars |
| **License** | MIT |
| **Quality** | Good; natural for a lightweight model; many voice options |
| **Speed** | Ultra-fast synthesis; sub-100ms on modern hardware |
| **Languages** | 30+ languages with pre-trained voices |
| **Cost** | **$0** |
| **Fit** | 8/10 — Best for low-latency server-side TTS; no GPU needed |

#### 4.2c Fish Speech (Server, Voice Cloning)

| Attribute | Detail |
|-----------|--------|
| **What** | Zero-shot voice cloning TTS — clone any voice from ~15 seconds of audio |
| **GitHub** | [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) — ~20k stars |
| **License** | Apache-2.0 |
| **Quality** | Very high; convincing voice cloning |
| **Languages** | English, Chinese, Japanese, Korean, and more |
| **Features** | Voice cloning from 15s sample, emotional expression, streaming support |
| **Cost** | **$0** (self-hosted) |
| **Fit** | 9/10 — Create a custom JARVIS voice for free |

#### 4.2d Bark (Server, Expressive)

| Attribute | Detail |
|-----------|--------|
| **What** | Suno's transformer-based TTS with non-speech sounds (laughter, music, effects) |
| **GitHub** | [suno-ai/bark](https://github.com/suno-ai/bark) — ~38k stars |
| **License** | MIT |
| **Quality** | Very natural with emotional expression; can generate music and sound effects |
| **Speed** | Slower (not real-time without GPU); ~2-5s for a sentence on GPU |
| **Languages** | 13+ languages |
| **Cost** | **$0** |
| **Fit** | 7/10 — Great expressiveness but too slow for real-time assistant responses |

#### 4.2e OpenVoice (Voice Cloning)

| Attribute | Detail |
|-----------|--------|
| **What** | Instant voice cloning with fine-grained style control |
| **GitHub** | [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) — ~31k stars |
| **License** | MIT |
| **Features** | Clone voice from short audio, control emotion/accent/rhythm/pauses independently |
| **Cost** | **$0** |
| **Fit** | 8/10 — Best granular control over voice style; good for creating the JARVIS persona |

#### 4.2f MeloTTS (Multilingual, Fast)

| Attribute | Detail |
|-----------|--------|
| **What** | High-quality multilingual TTS by MyShell |
| **GitHub** | [myshell-ai/MeloTTS](https://github.com/myshell-ai/MeloTTS) — ~5k stars |
| **License** | MIT |
| **Speed** | Real-time on CPU; very fast |
| **Languages** | English, Chinese, Japanese, Korean, Spanish, French |
| **Cost** | **$0** |
| **Fit** | 7/10 — Good multilingual option; less expressive than Kokoro |

#### 4.2g Web Speech API (Browser Fallback)

| Attribute | Detail |
|-----------|--------|
| **What** | Built-in browser speech synthesis |
| **Pros** | Zero setup, many voices on modern OS |
| **Cons** | Robotic quality, no custom voices, inconsistent across browsers |
| **Cost** | **$0** |
| **Fit** | 3/10 — Emergency fallback only; not JARVIS-quality |

### 4.3 PREMIUM VOICE OPTIONS (Optional Upgrades)

| Service | Type | Cost | When to Use |
|---------|------|------|-------------|
| **Deepgram Nova-3** | STT | ~$0.35/hr streaming | If self-hosted STT latency is insufficient |
| **ElevenLabs** | TTS | $5-330/mo | If you want the absolute best voice quality |
| **OpenAI Whisper API** | STT | $0.006/min | Quick cloud fallback |

### 4.4 STT + TTS RECOMMENDATION

**MVP (Zero Cost):**
- **STT:** Transformers.js + Whisper in browser (client-side, free)
- **TTS:** Kokoro TTS via kokoro-js in browser (client-side, free)
- Total voice cost: **$0/mo**

**Production (Zero Cost, Server-Enhanced):**
- **STT:** faster-whisper via Docker (OpenAI-compatible API) + Moonshine JS for instant browser-side VAD
- **TTS:** Kokoro TTS server + Fish Speech for custom JARVIS voice cloning
- Total voice cost: **$0/mo** (just server hosting)

**Hybrid (Best Quality):**
- **STT:** faster-whisper primary + Deepgram Nova-3 fallback
- **TTS:** Fish Speech custom JARVIS voice + ElevenLabs for premium quality
- Total voice cost: **~$50-150/mo**

---

## LAYER 5: GRAPHICS & MOTION (The Face)

### 5.1 React Three Fiber (R3F) + Three.js — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | React renderer for Three.js — declarative 3D graphics in JSX |
| **Pros** | React-native workflow, massive ecosystem (@react-three/drei, postprocessing, uikit), proven with Next.js 15, holographic effects via custom GLSL shaders |
| **Cons** | Learning curve for 3D/shaders, performance tuning needed, SSR requires careful handling |
| **Cost** | Free (open-source) |
| **Risk** | 3D performance on low-end devices; hydration issues with Next.js App Router |
| **Fit** | 10/10 — This IS the JARVIS HUD technology |

### 5.2 Framer Motion — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Production-ready animation library for React |
| **Pros** | Declarative API, layout animations, gesture support, exit animations, spring physics |
| **Cons** | Bundle size (~30KB), not designed for 3D |
| **Cost** | Free (open-source) |
| **Risk** | Minimal; very stable library |
| **Fit** | 9/10 — Perfect for UI transitions, panels sliding in/out, JARVIS-style reveals |

### 5.3 GSAP (GreenSock)

| Attribute | Detail |
|-----------|--------|
| **What** | Industry-standard animation engine with timeline sequencing |
| **Pros** | Most powerful timeline control, ScrollTrigger, works everywhere, butter-smooth |
| **Cons** | Commercial license required for SaaS ($200+/yr), imperative API (less React-friendly) |
| **Cost** | Free for personal; Business: $200/yr; SaaS: Custom pricing |
| **Risk** | Licensing cost; imperative style conflicts with React patterns |
| **Fit** | 7/10 — Powerful but Framer Motion covers most needs in React |

### 5.4 Spline

| Attribute | Detail |
|-----------|--------|
| **What** | Browser-based 3D design tool with React export |
| **Pros** | Visual design workflow (no code for 3D modeling), React component export, real-time collaboration |
| **Cons** | Less control than R3F, runtime performance concerns, dependency on Spline service |
| **Cost** | Free tier available; Pro: ~$9-18/mo |
| **Risk** | Vendor dependency for 3D assets |
| **Fit** | 6/10 — Good for rapid prototyping 3D assets, but R3F for production |

### 5.5 Data Visualization (D3.js / Recharts / Nivo)

| Attribute | Detail |
|-----------|--------|
| **What** | Libraries for real-time data dashboards and overlays |
| **Pros** | D3: unlimited customization; Recharts: simple React charts; Nivo: beautiful defaults |
| **Cons** | D3 has steep learning curve; Recharts limited for custom viz |
| **Cost** | All free (open-source) |
| **Risk** | Minimal |
| **Fit** | 8/10 — Nivo or Recharts for dashboards, D3 for custom HUD elements |

**RECOMMENDATION:** **React Three Fiber** for 3D HUD + **Framer Motion** for 2D animations + **Nivo/Recharts** for data viz. Use Spline only for rapid 3D asset prototyping.

---

## LAYER 6: REAL-TIME & STREAMING (The Blood Flow)

### 6.1 Server-Sent Events (SSE) — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | One-way server-to-client streaming over HTTP |
| **Pros** | Native browser support, works with Next.js Route Handlers, perfect for LLM token streaming, no extra dependencies |
| **Cons** | One-directional only, limited to ~6 connections per domain in HTTP/1.1 |
| **Cost** | Free (built into HTTP) |
| **Risk** | Minimal; proven pattern for AI streaming |
| **Fit** | 9/10 — Standard for LLM response streaming |

### 6.2 Socket.io / WebSockets

| Attribute | Detail |
|-----------|--------|
| **What** | Bidirectional real-time communication |
| **Pros** | True bidirectional, events, rooms, fallback handling |
| **Cons** | Requires separate server/infrastructure (doesn't work natively on Vercel), more complex |
| **Cost** | Free (open-source); infrastructure cost varies |
| **Risk** | Hosting complexity on serverless platforms |
| **Fit** | 7/10 — Needed for voice streaming and real-time collaboration, but SSE covers most AI streaming |

### 6.3 Ably

| Attribute | Detail |
|-----------|--------|
| **What** | Managed real-time messaging with global edge network |
| **Pros** | Exactly-once delivery, message history, state recovery, 6M msgs/mo free, scales well |
| **Cons** | External dependency, costs at scale |
| **Cost** | Free: 6M msgs/mo; Pay-as-you-go after that |
| **Risk** | Vendor dependency |
| **Fit** | 7/10 — Consider if you need mission-critical real-time features beyond SSE |

**RECOMMENDATION:** **SSE** for LLM streaming (built-in, free). Add **WebSockets** only if bidirectional real-time features (voice, collaboration) require it.

---

## LAYER 7: INFRASTRUCTURE (The Skeleton)

### 7.1 Authentication: Clerk — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Drop-in auth with pre-built UI components for Next.js |
| **Pros** | Beautiful UI out of box, Next.js App Router support, social login, MFA, organizations |
| **Cons** | Vendor lock-in, more expensive than DIY |
| **Cost** | Free: 10K MAU; Pro: $25/mo + $0.02/MAU |
| **Risk** | Vendor dependency; cost at scale |
| **Fit** | 8/10 — Fastest path to secure auth |

### 7.2 Deployment: Vercel — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Native hosting platform for Next.js with edge network |
| **Pros** | Zero-config Next.js deployment, edge functions, preview deployments, serverless scaling |
| **Cons** | Expensive at scale, function execution time limits (can hit limits with AI workloads) |
| **Cost** | Free tier: hobby; Pro: $20/mo/member; Enterprise: custom |
| **Risk** | Serverless timeout limits (60s default) for long AI operations |
| **Fit** | 8/10 — Best DX for Next.js; pair with background job service for long tasks |

### 7.3 Background Jobs: Trigger.dev — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | Background job engine with no timeouts, built for AI workloads |
| **Pros** | No execution time limits, per-run pricing, atomic versioning, system packages (ffmpeg etc.) |
| **Cons** | Runs on their infrastructure (not your server) |
| **Cost** | $20/mo base + per-run pricing |
| **Risk** | External compute dependency |
| **Fit** | 9/10 — Solves Vercel's timeout problem for AI agents |

### 7.4 Observability: Helicone — RECOMMENDED

| Attribute | Detail |
|-----------|--------|
| **What** | LLM observability with built-in caching and cost tracking |
| **Pros** | 1-line integration (proxy URL change), 100K requests/mo free, cost tracking, caching saves 20-30% on API costs, open-source |
| **Cons** | Less deep tracing than LangSmith for complex chains |
| **Cost** | Free: 100K req/mo; $25/mo flat after that |
| **Risk** | Minimal — open-source fallback available |
| **Fit** | 9/10 — Essential for tracking AI costs and performance |

### 7.5 Database: PostgreSQL + Drizzle ORM (Already Chosen)

| Attribute | Detail |
|-----------|--------|
| **What** | Type-safe ORM with PostgreSQL |
| **Pros** | Best TypeScript DX, SQL-like syntax, lightweight, migrations |
| **Cons** | Smaller ecosystem than Prisma |
| **Cost** | Free (Drizzle); DB hosting: Neon free tier, Supabase free tier, or Railway ~$5/mo |
| **Risk** | Minimal |
| **Fit** | 10/10 — Already in the stack; great choice |

---

## COST SUMMARY

### Monthly Budget Estimates (Updated with Free Voice Stack)

| Tier | Components | Est. Monthly Cost |
|------|-----------|-------------------|
| **MVP / Solo Dev** | Claude Haiku via OpenRouter + pgvector + Kokoro TTS (browser) + Transformers.js Whisper (browser) + Vercel Free + Helicone Free | **$10-30/mo** |
| **Beta Launch** | Claude Sonnet via OpenRouter + faster-whisper (Docker) + Kokoro TTS (server) + Fish Speech voice clone + Vercel Pro + Clerk Free | **$50-150/mo** |
| **Production** | Claude Opus via OpenRouter + Gemini routing + faster-whisper + Kokoro/Fish Speech + Vercel Pro + Trigger.dev + Clerk Pro + Helicone | **$200-600/mo** |
| **Scale** | Multi-model routing + Deepgram/ElevenLabs premium fallback + custom infrastructure | **$800-2,500+/mo** |

> **Key insight:** Free voice stack saves $100-300/mo compared to previous Deepgram + ElevenLabs recommendation.

---

## RECOMMENDED STACK (Final Verdict)

| Layer | Technology | Why |
|-------|-----------|-----|
| **Intelligence** | Claude Opus/Sonnet 4.6 (primary brain) | Best reasoning, tool use, and agentic behavior |
| **API Gateway** | OpenRouter | Multi-model routing, single API key, automatic failover |
| **Cheap Tasks** | Gemini Flash Lite via OpenRouter ($0.075/MTok) | 40x cheaper than Opus for classification/routing |
| **Agent Framework** | Claude Agent SDK + Vercel AI SDK | Native tool use + streaming UI |
| **Memory** | pgvector + RAG pipeline | Zero new infrastructure |
| **Voice (STT)** | Transformers.js Whisper (browser) + faster-whisper (server) | **Free**, 99+ languages, near-human accuracy |
| **Voice (TTS)** | Kokoro TTS (browser/server) + Fish Speech (voice cloning) | **Free**, near-commercial quality, custom JARVIS voice |
| **3D Graphics** | React Three Fiber + @react-three/drei | Holographic HUD in React |
| **2D Animation** | Framer Motion | Smooth UI transitions |
| **Data Viz** | Nivo / Recharts | Dashboard overlays |
| **Streaming** | SSE (built-in) | Free, native, proven |
| **Auth** | Clerk | Fastest secure auth |
| **Hosting** | Vercel | Native Next.js platform |
| **Background Jobs** | Trigger.dev | No-timeout AI processing |
| **Observability** | Helicone | Cost tracking + caching |
| **Database** | PostgreSQL + Drizzle ORM | Already chosen; excellent |

---

## TOP RISKS

| Risk | Severity | Mitigation |
|------|----------|------------|
| **API costs spiral** | HIGH | Use Helicone caching, Gemini Flash for simple tasks, token budgets per user |
| **Voice latency > 500ms** | MEDIUM | Deepgram + ElevenLabs Flash pipeline, edge deployment, pre-buffer responses |
| **3D performance on mobile** | MEDIUM | Progressive enhancement: 2D fallback for low-end devices, LOD system |
| **Vendor lock-in** | MEDIUM | Abstract LLM calls behind service layer; use Vercel AI SDK for model-agnostic code |
| **Scope creep** | HIGH | Build in layers: text-only v1 -> voice v2 -> 3D HUD v3 |

---

## IMPLEMENTATION PHASES

**Phase 1 — Text Brain (Weeks 1-4):** Next.js + Claude API + pgvector + Drizzle + Clerk + basic chat UI
**Phase 2 — Self-Learning (Weeks 5-8):** RAG pipeline + conversation memory + user preference learning
**Phase 3 — Voice (Weeks 9-12):** Deepgram STT + ElevenLabs TTS + streaming voice pipeline
**Phase 4 — JARVIS HUD (Weeks 13-18):** React Three Fiber 3D interface + Framer Motion + data viz dashboards
**Phase 5 — Agent Mode (Weeks 19-24):** Multi-tool agents + background tasks + proactive suggestions
