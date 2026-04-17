# PARASYTE - COMPLETE RESEARCH

> 20 topics researched via Perplexity Deep Research

---

## RESEARCH COMPLETED

| # | Topic | Summary |
|---|-------|---------|
| 1 | LFM Architecture | LFMs use CfC (closed-form continuous-time) + ODEs for continuous time |
| 2 | CDP Protocol | JSON-RPC over WebSocket, domains: Page, Runtime, DOM, Network, Debugger, Memory, Profiler |
| 3 | LLM DevTools Integration | Chrome already integrates Gemini; MCP server public preview; Skyvern, Browser Run automate with CDP |
| 4 | Autonomous Debugging | AGDebugger for multi-agent; Self-Debugging in LLMs; Maxim AI tracing |
| 5 | LFM API Access | LFM2.5-1.2B available on HuggingFace GGUF; OpenRouter has compatible endpoint |
| 6 | Neuron Dynamics | CTNNs with ODEs dZ/dt = f(z,t,theta); CfC eliminates numerical solvers (10-100x speedup) |
| 7 | Puppeteer Playwright CDP | Both expose CDP via `createCDPSession()`; Puppeteer faster, Playwright multi-browser |
| 8 | Edge Deployment LFM | GGUF quantization; 2x speedup prefill/decode; browser extension viable with bundling |
| 9 | Model Injection Control | Legitimate extensions like CLANKER (Gemini 2.0); man-in-the-prompt risks |
| 10 | Liquid Neural Network Code | kyegomez/LFM in PyTorch; IGITUGraz/LSM for NEST; LTCtutorial Jupyter notebooks |
| 11 | WebDriver Protocol | W3C standard; Selenium 4 supports full WebDriver; Remote WebDriver via Grid |
| 12 | Chrome Extension Architecture | MV3 with service workers; no remotely hosted code; new Scripting API |
| 13 | Memory Profiling Tools | Heap snapshots, allocation timeline, sampling; detached DOM detection |
| 14 | Network Analysis Tools | Waterfall view, timing breakdown, throttling, filtering; Performance panel integration |
| 15 | React Vue Debugging | React DevTools, Vue DevTools, Angular DevTools; component trees + state inspection |
| 16 | CDP DOM Commands | querySelector, resolveNode, setOuterHTML; Runtime.evaluate + callFunctionOn |
| 17 | Profiler API | chrome.devtools.performance API; CPU flame graphs; V8 Inspector .cpuprofile |
| 18 | Security Isolation | Sandbox renderer; CSP policies; granular extension permissions |
| 19 | Competitive Landscape | Operator (OpenAI), Computer Use (Claude), browser-use, Nanobrowser, Skyvern |
| 20 | Future Architecture | WebGPU default in browsers 2025; WebNN API; on-device LLM at 60fps |

---

## KEY FINDINGS

### 1. CDP is the Perfect Hook
- Mature and complete protocol
- Supports all necessary use cases
- Google is already integrating AI in DevTools

### 2. LFM is Ideal for Edge/Browser
- Latency <10ms/token
- 10x less energy than transformers
- GGUF for CPU inference
- Inference-time adaptation

### 3. Competition Exists But Gap Remains
- Operator and Computer Use are proprietary and expensive
- browser-use is open-source but limited
- None combine LFM + Native DevTools

### 4. "Parasyte" Concept is Unique
- Not just another browser automation agent
- It's a model that "attaches" and controls
- Minimal modification (only adapter layer)

---

## CONCLUSIONS

1. **Technically viable**: CDP + LFM = native DevTools control
2. **Unique in market**: Nobody is doing LFM + DevTools
3. **Edge deployment possible**: Quantized GGUF runs in browser extension
4. **Security manageable**: Allowlist of commands, granular permissions
5. **Clear roadmap**: Prototype -> Capabilities -> Autonomy -> Optimization

---

## NEXT STEPS

- [ ] Functional prototype with basic LFM
- [ ] Adapter layer for CDP commands
- [ ] Implemented feedback loop
- [ ] Fine-tune on CDP commands
- [ ] Browser extension build

---

## DOCUMENTATION

- `research_notes.txt` - Complete research (20 sections)
- `docs/architecture.md` - System architecture
- `docs/technical-spec.md` - Detailed technical specification
- `src/parasyte.py` - Python prototype
- `src/parasyte_demo.py` - Demo that verifies the concept
