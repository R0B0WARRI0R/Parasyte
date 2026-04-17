# PARASYTE - ESPECIFICACION TECNICA

## Objetivo
Crear un agente autonomo basado en LFM que controle Chrome DevTools via CDP para tareas de debugging, profiling y automation.

---

## 1. INTERFACES

### 1.1 CDP Interface

**Connection**: WebSocket a `ws://localhost:9222`

```typescript
interface CDPConnection {
  wsUrl: string;           // "ws://localhost:9222"
  targetId?: string;       // Tab especifico
  sessionId?: string;     // CDP session activa
}
```

**Comandos basicos a soportar**:

```typescript
// Navigation
interface PageCommands {
  "Page.navigate": { url: string };
  "Page.reload": { ignoreCache?: boolean };
  "Page.setViewportEnabled": { enabled: boolean };
}

// DOM
interface DOMCommands {
  "DOM.getDocument": {};
  "DOM.querySelector": { selector: string; nodeId?: number };
  "DOM.querySelectorAll": { selector: string; nodeId?: number };
  "DOM.setOuterHTML": { nodeId: number; outerHTML: string };
  "DOM.getBoxModel": { nodeId: number };
  "DOM.getAttributes": { nodeId: number };
}

// Runtime
interface RuntimeCommands {
  "Runtime.evaluate": { expression: string; returnByValue?: boolean };
  "Runtime.callFunctionOn": { 
    functionDeclaration: string; 
    objectId?: string;
    arguments?: RemoteObject[];
  };
  "Runtime.getProperties": { objectId: string; ownProperties?: boolean };
}

// Debugger
interface DebuggerCommands {
  "Debugger.enable": {};
  "Debugger.disable": {};
  "Debugger.setBreakpoint": { location: Location };
  "Debugger.stepOver": {};
  "Debugger.stepInto": {};
  "Debugger.stepOut": {};
  "Debugger.resume": {};
}

// Network
interface NetworkCommands {
  "Network.enable": {};
  "Network.disable": {};
  "Network.getResponseBody": { requestId: string };
  "Network.setRequestInterception": { patterns: RequestPattern[] };
}

// Memory
interface MemoryCommands {
  "Memory.getDOMCounters": {};
  "HeapProfiler.takeHeapSnapshot": {};
  "HeapProfiler.startTracking": {};
  "HeapProfiler.stopTracking": {};
}

// Profiler
interface ProfilerCommands {
  "Profiler.start": {};
  "Profiler.stop": {};
  "Profiler.enable": {};
  "Profiler.disable": {};
  "Profiler.getBestEffortCoverage": {};
}
```

### 1.2 LFM Interface

**Modelo**: LFM 2.5-1.2B-Instruct

```typescript
interface LFMConfig {
  modelPath: string;          // Path a GGUF
  contextLength: number;       // 4096 default
  threads: number;            // Num threads CPU
  gpuLayers?: number;         // Layers en GPU (0 = CPU only)
  nBatch: number;             // Batch size
  ropeFreqBase: number;       // RoPE base
  ropeFreqScale: number;      // RoPE scale
}
```

**Prompts de entrada**:

```typescript
interface ParasytePrompt {
  task: string;               // Tarea en lenguaje natural
  context?: {
    pageUrl: string;
    recentCommands: CDPCommand[];
    errors: string[];
  };
  mode: "analyze" | "act" | "debug";
}
```

---

## 2. MODULOS

### 2.1 parasyte-core

```typescript
// src/core/adapter.ts
export class CDPAdapter {
  private commands: Map<string, CDPCommand>;
  
  // Mapea intenciones a comandos
  intentionToCommand(intent: string): CDPCommand[];
  
  // Valida outputs de CDP
  validateResponse(cmd: string, response: any): boolean;
}

// src/core/lfm-bridge.ts
export class LFMBridge {
  private lfm: LLModexecutor;
  
  // Ejecuta prompts en LFM
  async query(prompt: ParasytePrompt): Promise<string>;
  
  // Streaming de tokens
  async *stream(prompt: ParasytePrompt): AsyncGenerator<string>;
}

// src/core/cdp-connector.ts
export class CDPConnector {
  private ws: WebSocket;
  private pending: Map<number, Promise<any>>;
  
  // Conectar a Chrome
  async connect(url: string): Promise<void>;
  
  // Enviar comando
  async send(cmd: CDPCommand): Promise<CDPResponse>;
  
  // Escuchar eventos
  on(event: string, callback: (data: any) => void): void;
}
```

### 2.2 parasyte-tools

```typescript
// src/tools/navigation.ts
export const NavigationTools = {
  goto: (url: string) => CDPCommand<"Page.navigate">,
  reload: (options?: { ignoreCache?: boolean }) => ...,
  back: () => ...,
  forward: () => ...,
};

// src/tools/dom.ts
export const DOMTools = {
  query: (selector: string) => ...,
  queryAll: (selector: string) => ...,
  getAttribute: (nodeId: number, name: string) => ...,
  setAttribute: (nodeId: number, name: string, value: string) => ...,
  innerHTML: (nodeId: number, html: string) => ...,
  click: (nodeId: number) => ...,
};

// src/tools/debugger.ts
export const DebuggerTools = {
  setBreakpoint: (url: string, line: number) => ...,
  stepOver: () => ...,
  stepInto: () => ...,
  evaluate: (expr: string) => ...,
};

// src/tools/memory.ts
export const MemoryTools = {
  takeSnapshot: () => ...,
  compareSnapshots: (snapshot1: string, snapshot2: string) => ...,
  getCounters: () => ...,
};

// src/tools/network.ts
export const NetworkTools = {
  enable: () => ...,
  getRequest: (id: string) => ...,
  getResponse: (id: string) => ...,
};
```

### 2.3 parasyte-agents

```typescript
// src/agents/debugger-agent.ts
export class DebuggerAgent {
  // Analiza y reporta errores
  async analyzeErrors(): Promise<ErrorReport>;
  
  // Ejecuta debugging commands
  async setBreakpoint(url: string, line: number): Promise<void>;
  
  // Step-by-step execution
  async stepThrough(): Promise<void>;
}

// src/agents/memory-agent.ts
export class MemoryAgent {
  // Detecta memory leaks
  async detectLeaks(): Promise<LeakReport>;
  
  // Toma snapshots
  async snapshot(label: string): Promise<string>;
  
  // Compara snapshots
  async compare(before: string, after: string): Promise<Diff>;
}

// src/agents/network-agent.ts
export class NetworkAgent {
  // Analiza requests
  async analyzeRequests(): Promise<NetworkReport>;
  
  // Detecta bottlenecks
  async findBottlenecks(): Promise<Bottleneck[]>;
}

// src/agents/react-agent.ts
export class ReactAgent {
  // Inspecciona componentes
  async inspectComponent(name: string): Promise<ComponentInfo>;
  
  // Analiza state
  async analyzeState(): Promise<StateAnalysis>;
}
```

---

## 3. API PUBLICA

### 3.1 REST API (Opcional)

```typescript
// POST /api/query
interface QueryRequest {
  task: string;
  context?: {
    tabId?: string;
    pageUrl?: string;
  };
  mode?: "analyze" | "act" | "debug";
}

// GET /api/snapshot/:tabId
// GET /api/memory/:tabId
// GET /api/network/:tabId
```

### 3.2 CLI

```bash
parasyte "find memory leaks"
parasyte "debug this React component"
parasyte --tab 123 "analyze network requests"
```

### 3.3 Browser Extension

```typescript
// popup.html - Interface de usuario
// background.ts - Service worker con LFM
// content.ts - Inyeccion en paginas
```

---

## 4. SCHEMA DE DATOS

### 4.1 Tab State

```typescript
interface TabState {
  id: string;
  url: string;
  title: string;
  debuggerEnabled: boolean;
  networkEnabled: boolean;
  memorySnapshots: Snapshot[];
  breakpoints: Breakpoint[];
  consoleMessages: ConsoleMessage[];
}
```

### 4.2 Memory Report

```typescript
interface MemoryReport {
  timestamp: Date;
  jsHeapSize: number;
  nodes: number;
  listeners: number;
  comparisons?: {
    before: string;
    after: string;
    leaks: Leak[];
  };
}
```

### 4.3 Error Report

```typescript
interface ErrorReport {
  timestamp: Date;
  errors: {
    message: string;
    stack: string;
    line: number;
    column: number;
    url: string;
  }[];
  suggestions?: string[];
}
```

---

## 5. ERRORES Y MANEJO

### 5.1 CDP Errors

```typescript
enum CDPErrorCode {
  INVALID_REQUEST = -32700,
  METHOD_NOT_FOUND = -32601,
  INVALID_PARAMS = -32602,
  INTERNAL_ERROR = -32603,
  // Browser-specific
  PAGE_CRASHED = -32000,
  TIMEOUT = -32001,
}
```

### 5.2 Retry Logic

```typescript
async function executeWithRetry(
  cmd: CDPCommand,
  maxRetries: number = 3
): Promise<CDPResponse> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await cdp.send(cmd);
    } catch (e) {
      if (e.code === CDPErrorCode.TIMEOUT) {
        await delay(1000 * (i + 1));
        continue;
      }
      throw e;
    }
  }
  throw new Error(`Max retries exceeded`);
}
```

---

## 6. SEGURIDAD

### 6.1 Allowed Commands

```typescript
const ALLOWED_COMMANDS = [
  // Navigation
  "Page.navigate",
  "Page.reload",
  
  // DOM read-only (escritura requiere confirmacion)
  "DOM.getDocument",
  "DOM.querySelector",
  "DOM.querySelectorAll",
  "DOM.getBoxModel",
  
  // Runtime (solo lectura por defecto)
  "Runtime.evaluate",
  "Runtime.callFunctionOn",
  
  // Debugger
  "Debugger.*",
  
  // Memory
  "Memory.*",
  "HeapProfiler.*",
  
  // Network
  "Network.getResponseBody",
];

// Comandos bloqueados
const BLOCKED_COMMANDS = [
  "Emulation.setDeviceMetricsOverride",  // Podria abusar
  "Page.setDownloadBehavior",              // Descargas
  "Browser.*",                             // Control de browser
];
```

### 6.2 Permission Levels

```typescript
enum PermissionLevel {
  READ_ONLY = "read",       // Solo lectura
  DIAGNOSTIC = "diagnostic", // Debugging + profiling
  FULL = "full",           // Control completo (peligroso)
}
```

---

## 7. DEPLOYMENT

### 7.1 Local (Desarrollo)

```bash
# 1. Chrome con remote debugging
chrome --remote-debugging-port=9222

# 2. Iniciar parasyte
python parasyte.py --cdp ws://localhost:9222 --lfm ./models/lfm-2.5-1.2b.q4k.gguf

# 3. CLI interactivo
parasyte> analyze memory
```

### 7.2 Browser Extension

```bash
# Build extension
npm run build:extension

# Extension incluye:
# - LFM cuantizado (GGUF)
# - CDP bridge
# - WASM para inference
```

### 7.3 Edge Device

```bash
# Raspberry Pi / Mobile
python parasyte.py --lfm ./models/lfm-2.5-1.2b.q8.gguf --threads 4
```

---

## 8. TESTS

```typescript
// tests/cdp-connector.test.ts
describe("CDPConnector", () => {
  it("connects to Chrome", async () => {
    const connector = new CDPConnector();
    await connector.connect("ws://localhost:9222");
    expect(connector.isConnected()).toBe(true);
  });
  
  it("sends commands", async () => {
    const result = await connector.send({
      method: "Page.navigate",
      params: { url: "about:blank" }
    });
    expect(result.success).toBe(true);
  });
});

// tests/adapter.test.ts
describe("CDPAdapter", () => {
  it("maps memory check intent", () => {
    const adapter = new CDPAdapter();
    const commands = adapter.intentionToCommand("check memory");
    expect(commands).toContainEqual(
      expect.objectContaining({ method: "Memory.getDOMCounters" })
    );
  });
});
```

---

## 9. DEPENDENCIAS

```json
{
  "dependencies": {
    "playwright": "^1.50.0",
    "ws": "^8.16.0",
    "llama.cpp": "latest"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "vitest": "^1.2.0",
    "esbuild": "^0.20.0"
  }
}
```

---

## 10. VERSIONES

- **v0.1**: Prototype - Conexion basica CDP
- **v0.2**: Con LFM basico
- **v0.3**: Feedback loop
- **v1.0**: Release inicial
