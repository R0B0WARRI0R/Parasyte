# PARASYTE - ARQUITECTURA TECNICA

## Resumen Ejecutivo

Parasyte es un sistema autonomo basado en Liquid Foundation Models (LFMs) que se conecta al Chrome DevTools Protocol (CDP) para controlar el navegador de forma inteligente. El concepto central es que el LFM funciona como un "parasito" que infecta DevTools y lo controla con minima modificacion propia.

---

## 1. ARQUITECTURA GENERAL

```
┌──────────────────────────────────────────────────────────────────────┐
│                           PARASYTE                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐      │
│  │     LFM      │────▶│   Adapter   │────▶│    CDP Bridge    │      │
│  │   (cerebro)  │     │   Layer     │     │    (ejecutor)    │      │
│  └──────────────┘     └──────────────┘     └──────────────────┘      │
│         │                    │                       │                 │
│         │                    │                       ▼                 │
│         │                    │            ┌──────────────────┐        │
│         │                    │            │   Chrome con     │        │
│         │                    │            │   Remote Debug   │        │
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

## 2. COMPONENTES

### 2.1 LFM Core

**Modelo base**: LFM 2.5-1.2B (Liquid AI)
- 1.2B parametros
- Optimizado para edge inference
- GGUF disponible para CPU inference
- Arquitectura hibrida: LIV + Attention

**Por que LFM:**
- Baja latencia (<10ms/token en edge)
- Adaptacion en inferencia
- Eficiencia energetica 10x vs transformers
- Escalamiento lineal

### 2.2 Adapter Layer

Capa de traduccion que mapea outputs del LLM a comandos CDP.

```typescript
interface CDPAdapter {
  // Input: intenciones del LFM
  // Output: comandos CDP ejecutables
  
  mapIntention(intent: string): CDPCommand;
  validateOutput(output: any): boolean;
  retryOnFailure(command: CDPCommand): CDPCommand;
}
```

**Objetivo**: Minima modificacion al LFM - solo el adapter se entrena.

### 2.3 CDP Bridge

Traductor bidireccional entre LFM y Chrome DevTools.

```
LFM Output ──▶ CDPCommand ──▶ Chrome
             │
             ▼
Chrome Event ──▶ LFM Input
```

**Endpoints principales**:
- `ws://localhost:9222` - Remote debugging
- `Target.createTarget` - Crear nuevas paginas
- `Target.attachToTarget` - Conectar a paginas existentes

### 2.4 Tool Set CDP

Conjunto de herramientas CDP disponibles:

| Categoria | Herramientas |
|-----------|--------------|
| **Navigation** | Page.navigate, Page.reload, Target.createTarget |
| **DOM** | DOM.getDocument, DOM.querySelector, DOM.setOuterHTML |
| **Runtime** | Runtime.evaluate, Runtime.callFunctionOn |
| **Debugger** | Debugger.setBreakpoint, Debugger.stepOver |
| **Network** | Network.enable, Network.setRequestInterception |
| **Memory** | HeapProfiler.takeSnapshot, Memory.getDOMCounters |
| **Profiler** | Profiler.start, Profiler.stop, Performance.getMetrics |

---

## 3. FLUJO DE OPERACION

```
1. USER INPUT
   "¿Hay memory leaks en esta pagina?"

2. LFM PROCESSING
   Analiza la pregunta → Detecta intencion

3. INTENTION MAPPING
   "memory_leak_detection" → [comandos CDP]

4. CDP EXECUTION
   ┌─ Memory.getDOMCounters
   ├─ HeapProfiler.takeSnapshot
   ├─ HeapProfiler.takeSnapshot (2do)
   └─ HeapProfiler.compareSnapshots

5. RESULT PARSING
   CDP responses → Parsed data

6. LFM ANALYSIS
   Analiza resultados → Genera diagnostico

7. USER OUTPUT
   "Se detectaron 3 objetos detached DOM..."
```

---

## 4. MODOS DE OPERACION

### 4.1 Modo Directo (Supervisado)
```
Usuario → LFM → Adapter → CDP → DevTools → Resultado
                                        ↓
                                   Usuario
```
- Usuario mantiene control
- LFM solo asiste/analiza
- Para debugging rapido

### 4.2 Modo Autonomo
```
LFM → Adapter → CDP → DevTools → Feedback → LFM
  ↑                                              │
  └────────────── loop continuo ─────────────────┘
```
- LFM opera sin supervision
- Auto-correction basada en resultados
- Para tareas de larga duracion

### 4.3 Modo Parasyte (Objetivo Final)
```
┌─────────────────────────────────────────────┐
│                                             │
│  LFM "infecta" DevTools                    │
│  Se adhiere via CDP                        │
│  Opera el navegador                        │
│  Se adapta segun feedback                  │
│                                             │
│  El LFM NO necesita ser reentrenado        │
│  Solo el adapter aprende                    │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 5. CAPAS DE SEGURIDAD

### 5.1 Isolation
- CDP commands en execution world aislado
- No acceso a recursos del sistema
- Permissions granulares

### 5.2 Validation
- Comandos CDP validados antes de ejecutar
- Lista blanca de comandos permitidos
- Timeout en operaciones

### 5.3 Audit
- Log de todos los comandos ejecutados
- Diff de cambios en DOM
- Historial de acciones

---

## 6. COMPARATIVA CON COMPETIDORES

| Aspecto | Operator (OpenAI) | Computer Use (Claude) | PARASYTE |
|---------|-------------------|---------------------|---------|
| **Modelo** | GPT-4o | Claude 3.5 Sonnet | LFM |
| **Protocolo** | API propietaria | API propietaria | CDP abierto |
| **Latencia** | Alta | Media | Baja |
| **Edge** | No | No | Si |
| **Control** | Screenshot/VNC | Virtual desktop | DevTools directo |
| **Debugging** | No nativo | Limitado | Nativo CDP |
| **Costo** | $200/mo | Claude API | Local |

---

## 7. ROADMAP

### Fase 1: Prototype (Semana 1-2)
- [ ] Conectar LFM basico a CDP
- [ ] Implementar adapter simple
- [ ] Probar comandos basicos (navigate, evaluate)

### Fase 2: Capabilities (Semana 3-4)
- [ ] Soporte para debugging commands
- [ ] Memory profiling basico
- [ ] Network monitoring

### Fase 3: Autonomy (Semana 5-6)
- [ ] Feedback loop implementado
- [ ] Self-correction
- [ ] Multi-step task execution

### Fase 4: Optimization (Semana 7-8)
- [ ] Fine-tune adapter
- [ ] Performance optimization
- [ ] Edge deployment (browser extension)

---

## 8. REFERENCIAS

- CDP Protocol: https://chromedevtools.github.io/devtools-protocol/
- LFM Models: https://liquid.ai/
- Open-source LFM: https://github.com/kyegomez/LFM
- Chrome DevTools MCP: chrome-devtools-mcp (npm)
