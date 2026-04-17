# PARASYTE

> Un LFM que "parasia" Chrome DevTools para control autonomo del navegador

## Concepto

```
+----------------------------------------------------------+
|                     PARASYTE                              |
|                                                           |
|  El LFM "infecta" DevTools como un virus                 |
|  Se modifica mnimamente para controlar                   |
|  el navegador de forma autonoma                            |
|                                                           |
+----------------------------------------------------------+
```

## Analoga biologica

| Virus | Parasyte |
|-------|----------|
| Se adhiere a receptores | Se conecta via CDP |
| Inyecta material genetico | Envia comandos |
| La celula ejecuta | DevTools opera |
| Replicacion/modificacion | Auto-mejora continua |

## Objetivo

Crear un agente autonomo que controle DevTools para:
- Depuracion automatica
- Profiling de rendimiento
- Deteccion de memory leaks
- Analisis de red
- Manipulacion inteligente del DOM

## Estructura del proyecto

```
Parasyte/
  src/                    # Codigo fuente
  data/                   # Datasets de entrenamiento
  notebooks/              # Jupyter notebooks para training
  scripts/                # Scripts utilitarios
  docs/                   # Documentacion tecnica
```

## Quick Start

### 1. Entrenar modelo

```bash
# Abrir en Google Colab
# notebooks/parasyte_lfm_training.ipynb
```

### 2. Exportar a GGUF

```bash
# notebooks/export_gguf.ipynb
```

### 3. Usar con Parasyte

```python
from parasyte import ParasyteAgent

agent = ParasyteAgent()
await agent.initialize()

# Pregunta en lenguaje natural
resultado = await agent.execute_task("Hay memory leaks?")
```

## Tecnologias

- **LFM**: Liquid Foundation Models (Liquid AI)
- **CDP**: Chrome DevTools Protocol
- **Target**: Chrome/Chromium con remote debugging

## Estado

- [x] Investigacion profunda completa
- [x] Dataset CDP generado (500 ejemplos, 98% precision de mapeo)
- [x] Prototipo basico de CDP bridge
- [x] Notebooks de entrenamiento
- [ ] Fine-tuning real del modelo
- [ ] Integration con Perplexity
- [ ] Modo autonomo completo

## Comandos CDP soportados

| Categoria | Comandos |
|-----------|----------|
| Navigation | Page.navigate, Page.reload, Target.createTarget |
| DOM | DOM.querySelector, DOM.getBoxModel, DOM.setOuterHTML |
| Runtime | Runtime.evaluate, Runtime.callFunctionOn |
| Debugger | Debugger.enable, Debugger.setBreakpoint, Debugger.stepOver |
| Network | Network.enable, Network.getAllRequests |
| Memory | Memory.getDOMCounters, HeapProfiler.takeHeapSnapshot |
| Performance | Profiler.start, Profiler.stop, Performance.getMetrics |

## Comparacion con alternativas

| Aspecto | Operator (OpenAI) | Computer Use (Claude) | PARASYTE |
|---------|-------------------|----------------------|----------|
| **Modelo** | GPT-4o | Claude 3.5 Sonnet | LFM |
| **Protocolo** | API propietaria | API propietaria | CDP abierto |
| **Latencia** | Alta | Media | Baja |
| **Edge** | No | No | Si |
| **Control** | Screenshot/VNC | Virtual desktop | DevTools nativo |
| **Debugging** | No nativo | Limitado | CDP nativo |
| **Costo** | $200/mes | API Claude | Local |

## Recursos

- [CDP Protocol Reference](https://chromedevtools.github.io/devtools-protocol/)
- [Liquid AI LFMs](https://liquid.ai/)
- [Unsoth - Fast Fine-tuning](https://github.com/unslothai/unsloth)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

## Licencia

MIT
