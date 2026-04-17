# PARASYTE - INVESTIGACION COMPLETA

> 20 topicos investigados via Perplexity Deep Research

---

## INVESTIGACION REALIZADA

| # | Topico | Resumen |
|---|--------|---------|
| 1 | LFM Architecture | LFMs usan CfC (closed-form continuous-time) + ODEs para tiempo continuo |
| 2 | CDP Protocol | JSON-RPC sobre WebSocket, dominios: Page, Runtime, DOM, Network, Debugger, Memory, Profiler |
| 3 | LLM DevTools Integration | Chrome ya integra Gemini; MCP server公开preview; Skyvern, Browser Run automatizan con CDP |
| 4 | Autonomous Debugging | AGDebugger para multi-agent; Self-Debugging en LLMs; Maxim AI tracing |
| 5 | LFM API Access | LFM2.5-1.2B disponible en HuggingFace GGUF; OpenRouter tiene endpoint compatible |
| 6 | Neuron Dynamics | CTNNs con ODEs dZ/dt = f(z,t,theta); CfC elimina solvers numericos (10-100x speedup) |
| 7 | Puppeteer Playwright CDP | Ambos exponen CDP via `createCDPSession()`; Puppeteer mas rapo, Playwright multi-browser |
| 8 | Edge Deployment LFM | GGUF quantization; 2x speedup prefill/decode; browser extension viable con bundling |
| 9 | Model Injection Control | Extensions legitimas como CLANKER (Gemini 2.0); riesgos de man-in-the-prompt |
| 10 | Liquid Neural Network Code | kyegomez/LFM en PyTorch; IGITUGraz/LSM para NEST; LTCtutorial Jupyter notebooks |
| 11 | WebDriver Protocol | W3C standard; Selenium 4 soporta full WebDriver; Remote WebDriver via Grid |
| 12 | Chrome Extension Architecture | MV3 con service workers; no remotely hosted code; Scripting API nuevo |
| 13 | Memory Profiling Tools | Heap snapshots, allocation timeline, sampling; deteccion de detached DOM |
| 14 | Network Analysis Tools | Waterfall view, timing breakdown, throttling, filtering; Performance panel integration |
| 15 | React Vue Debugging | React DevTools, Vue DevTools, Angular DevTools; componente trees + state inspection |
| 16 | CDP DOM Commands | querySelector, resolveNode, setOuterHTML; Runtime.evaluate + callFunctionOn |
| 17 | Profiler API | chrome.devtools.performance API; CPU flame graphs; V8 Inspector .cpuprofile |
| 18 | Security Isolation | Sandbox renderer; CSP policies; extension permissions granular |
| 19 | Competitive Landscape | Operator (OpenAI), Computer Use (Claude), browser-use, Nanobrowser, Skyvern |
| 20 | Future Architecture | WebGPU default en browsers 2025; WebNN API; on-device LLM a 60fps |

---

## HALLAZGOS CLAVE

### 1. CDP es el enganche perfecto
- Protocolo maduro y completo
- Soporta todos los casos de uso necesarios
- Google ya esta integrando AI en DevTools

### 2. LFM es ideal para edge/browser
- Latencia <10ms/token
- 10x menos energia que transformers
- GGUF para CPU inference
- Adaptacion en inferencia

### 3. Competencia existe pero hay gap
- Operator y Computer Use son propietarios y caros
- browser-use es open-source pero limitado
- Ninguno combina LFM + DevTools nativo

### 4. El concepto "Parasyte" es unico
- No es un agente mas de browser automation
- Es un modelo que se "adhiere" y controla
- Modificacion minima (solo adapter layer)

---

## CONCLUSIONES

1. **Tecnicamente viable**: CDP + LFM = control nativo de DevTools
2. **Unico en el mercado**: Nadie esta haciendo LFM + DevTools
3. **Edge deployment posible**: GGUF quantizado corre en browser extension
4. **Seguridad manejable**: Lista blanca de comandos, permissions granulares
5. **Roadmap claro**: Prototype -> Capabilities -> Autonomy -> Optimization

---

## PROXIMOS PASOS

- [ ] Prototype funcional con LFM basico
- [ ] Adapter layer para CDP commands
- [ ] Feedback loop implementado
- [ ] Fine-tune en comandos CDP
- [ ] Browser extension build

---

## DOCUMENTACION

- `research_notes.txt` - Investigacion completa (20 secciones)
- `docs/architecture.md` - Arquitectura del sistema
- `docs/technical-spec.md` - Especificacion tecnica detallada
- `src/parasyte.py` - Prototype Python
- `src/parasyte_demo.py` - Demo que verifica el concepto
