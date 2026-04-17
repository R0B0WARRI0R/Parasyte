# PARASYTE - TECHNICAL ARCHITECTURE

## Executive Summary

Parasyte is an autonomous system based on Liquid Foundation Models (LFMs) that connects to Chrome DevTools Protocol (CDP) to control the browser intelligently. The central concept is that the LFM functions as a "parasite" that infects DevTools and controls it with minimal self-modification.

---

## 1. HIGH-LEVEL ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────────────┐
│                           PARASYTE                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐      │
│  │     LFM      │────▶│   Adapter   │────▶│    CDP Bridge    │      │
│  │   (brain)    │     │   Layer     │     │   (executor)     │      │
│  └──────────────┘     └──────────────┘     └──────────────────┘      │
│         │                    │                       │                 │
│         │                    │                       ▼                 │
│         │                    │            ┌──────────────────┐        │
│         │                    │            │   Chrome with     │        │
│         │                    │            │   Remote Debug    │        │
│         │                    │            └──────────────────┘        │
│         │                    │                                        │
│         ▼                    ▼                                        │
│  ┌──────────────┐     ┌──────────────┐                                 │
│  │   Feedback  │◀────│    Tools    │                                 │
│  │    Loop     │     │   CDP API    │                                 │
│  └──────────────┘     └──────────────┘                                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. COMPONENTS

### 2.1 LFM Core

**Base model**: LFM 2.5-1.2B (Liquid AI)
- 1.2B parameters
- Optimized for edge inference
- GGUF available for CPU inference
- Hybrid architecture: LIV + Attention

**Why LFM:**
- Low latency (<10ms/token on edge)
- Inference-time adaptation
- 10x energy efficiency vs transformers
- Linear scaling

### 2.2 Adapter Layer

Translation layer mapping LLM outputs to CDP commands.

```typescript
interface CDPAdapter {
  mapIntention(intent: string): CDPCommand;
  validateOutput(output: any): boolean;
  retryOnFailure(command: CDPCommand): CDPCommand;
}
```

**Goal**: Minimal LFM modification - only the adapter is trained.

### 2.3 CDP Bridge

Bidirectional translator between LFM and Chrome DevTools.

```
LFM Output ──▶ CDPCommand ──▶ Chrome
             │
             ▼
Chrome Event ──▶ LFM Input
```

**Main endpoints**:
- `ws://localhost:9222` - Remote debugging
- `Target.createTarget` - Create new tabs
- `Target.attachToTarget` - Connect to existing tabs

### 2.4 CDP Tool Set

Available tool set:

| Category | Tools |
|----------|-------|
| **Navigation** | Page.navigate, Page.reload, Target.createTarget |
| **DOM** | DOM.getDocument, DOM.querySelector, DOM.setOuterHTML |
| **Runtime** | Runtime.evaluate, Runtime.callFunctionOn |
| **Debugger** | Debugger.setBreakpoint, Debugger.stepOver |
| **Network** | Network.enable, Network.setRequestInterception |
| **Memory** | HeapProfiler.takeSnapshot, Memory.getDOMCounters |
| **Profiler** | Profiler.start, Profiler.stop, Performance.getMetrics |

---

## 3. OPERATION FLOW

```
1. USER INPUT
   "Are there memory leaks on this page?"

2. LFM PROCESSING
   Analyzes question → Detects intention

3. INTENTION MAPPING
   "memory_leak_detection" → [CDP commands]

4. CDP EXECUTION
   ┌─ Memory.getDOMCounters
   ├─ HeapProfiler.takeSnapshot
   ├─ HeapProfiler.takeSnapshot (2nd)
   └─ HeapProfiler.compareSnapshots

5. RESULT PARSING
   CDP responses → Parsed data

6. LFM ANALYSIS
   Analyzes results → Generates diagnosis

7. USER OUTPUT
   "Detected 3 detached DOM objects..."
```

---

## 4. OPERATION MODES

### 4.1 Direct Mode (Supervised)
```
User → LFM → Adapter → CDP → DevTools → Result
                                        ↓
                                   User
```
- User maintains control
- LFM only assists/analyzes
- For quick debugging

### 4.2 Autonomous Mode
```
LFM → Adapter → CDP → DevTools → Feedback → LFM
  ↑                                              │
  └────────────── continuous loop ───────────────┘
```
- LFM operates without supervision
- Self-correction based on results
- For long-running tasks

### 4.3 Parasyte Mode (End Goal)
```
┌─────────────────────────────────────────────┐
│                                             │
│  LFM "infects" DevTools                    │
│  Attaches via CDP                         │
│  Operates the browser                     │
│  Adapts based on feedback                 │
│                                             │
│  LFM DOES NOT need retraining             │
│  Only the adapter learns                   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 5. SECURITY LAYERS

### 5.1 Isolation
- CDP commands in isolated execution world
- No system resource access
- Granular permissions

### 5.2 Validation
- CDP commands validated before execution
- Allowlist of permitted commands
- Timeout on operations

### 5.3 Audit
- Log of all executed commands
- Diff of DOM changes
- Action history

---

## 6. COMPETITOR COMPARISON

| Aspect | Operator (OpenAI) | Computer Use (Claude) | PARASYTE |
|--------|-------------------|----------------------|----------|
| **Model** | GPT-4o | Claude 3.5 Sonnet | LFM |
| **Protocol** | Proprietary API | Proprietary API | Open CDP |
| **Latency** | High | Medium | Low |
| **Edge** | No | No | Yes |
| **Control** | Screenshot/VNC | Virtual desktop | Native DevTools |
| **Debugging** | Not native | Limited | Native CDP |
| **Cost** | $200/mo | Claude API | Local |

---

## 7. ROADMAP

### Phase 1: Prototype (Week 1-2)
- [ ] Connect basic LFM to CDP
- [ ] Implement simple adapter
- [ ] Test basic commands (navigate, evaluate)

### Phase 2: Capabilities (Week 3-4)
- [ ] Support for debugging commands
- [ ] Basic memory profiling
- [ ] Network monitoring

### Phase 3: Autonomy (Week 5-6)
- [ ] Feedback loop implemented
- [ ] Self-correction
- [ ] Multi-step task execution

### Phase 4: Optimization (Week 7-8)
- [ ] Fine-tune adapter
- [ ] Performance optimization
- [ ] Edge deployment (browser extension)

---

## 8. REFERENCES

- CDP Protocol: https://chromedevtools.github.io/devtools-protocol/
- LFM Models: https://liquid.ai/
- Open-source LFM: https://github.com/kyegomez/LFM
- Chrome DevTools MCP: chrome-devtools-mcp (npm)
