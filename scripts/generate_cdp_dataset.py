# ========================================
# PARASYTE - CDP Expert Training Dataset
# ========================================
# Generate 1000+ CDP training examples
# Format: JSONL for efficient training
# ========================================

import json
import random

# CDP Commands organized by category
CDP_COMMANDS = {
    "navigation": [
        {"command": "Page.navigate", "params": {"url": "string"}, "description": "Navega a una URL"},
        {"command": "Page.reload", "params": {"ignoreCache": "boolean"}, "description": "Recarga la pagina"},
        {"command": "Page.bringToFront", "params": {}, "description": "Trae la pagina al frente"},
        {"command": "Target.createTarget", "params": {"url": "string"}, "description": "Crea nueva pestana"},
        {"command": "Target.closeTarget", "params": {"targetId": "string"}, "description": "Cierra pestana"},
        {"command": "Target.attachToTarget", "params": {"targetId": "string"}, "description": "Conecta a pestana"},
        {"command": "Page.setViewportDimensions", "params": {"width": "int", "height": "int"}, "description": "Cambia tamano viewport"},
    ],
    "dom": [
        {"command": "DOM.getDocument", "params": {}, "description": "Obtiene documento completo"},
        {"command": "DOM.querySelector", "params": {"selector": "string", "nodeId": "int"}, "description": "Busca elemento CSS"},
        {"command": "DOM.querySelectorAll", "params": {"selector": "string", "nodeId": "int"}, "description": "Busca todos elementos"},
        {"command": "DOM.getOuterHTML", "params": {"nodeId": "int"}, "description": "HTML externo"},
        {"command": "DOM.setOuterHTML", "params": {"nodeId": "int", "outerHTML": "string"}, "description": "Reemplaza HTML"},
        {"command": "DOM.getBoxModel", "params": {"nodeId": "int"}, "description": "Tamano y posicion"},
        {"command": "DOM.getAttributes", "params": {"nodeId": "int"}, "description": "Lista atributos"},
        {"command": "DOM.setAttributeValue", "params": {"nodeId": "int", "name": "string", "value": "string"}, "description": "Cambia atributo"},
        {"command": "DOM.removeAttribute", "params": {"nodeId": "int", "name": "string"}, "description": "Elimina atributo"},
        {"command": "DOM.requestChildNodes", "params": {"nodeId": "int"}, "description": "Carga hijos"},
        {"command": "DOM.scrollIntoViewIfNeeded", "params": {"nodeId": "int"}, "description": "Scrollea a elemento"},
    ],
    "runtime": [
        {"command": "Runtime.evaluate", "params": {"expression": "string", "returnByValue": "boolean"}, "description": "Ejecuta JS"},
        {"command": "Runtime.callFunctionOn", "params": {"functionDeclaration": "string", "objectId": "string"}, "description": "Llama funcion en objeto"},
        {"command": "Runtime.getProperties", "params": {"objectId": "string", "ownProperties": "boolean"}, "description": "Propiedades de objeto"},
        {"command": "Runtime.releaseObject", "params": {"objectId": "string"}, "description": "Libera referencia"},
        {"command": "Runtime.releaseObjectGroup", "params": {"objectGroup": "string"}, "description": "Libera grupo"},
        {"command": "Runtime.discardConsoleEntries", "params": {}, "description": "Limpia consola"},
        {"command": "Runtime.runIfWaitingForDebugger", "params": {}, "description": "Continua si esperando debugger"},
    ],
    "debugger": [
        {"command": "Debugger.enable", "params": {}, "description": "Activa debugger"},
        {"command": "Debugger.disable", "params": {}, "description": "Desactiva debugger"},
        {"command": "Debugger.setBreakpointByUrl", "params": {"url": "string", "lineNumber": "int"}, "description": "Breakpoint por URL"},
        {"command": "Debugger.setBreakpoint", "params": {"location": {"scriptId": "string", "lineNumber": "int"}}, "description": "Breakpoint exacto"},
        {"command": "Debugger.removeBreakpoint", "params": {"breakpointId": "string"}, "description": "Elimina breakpoint"},
        {"command": "Debugger.stepOver", "params": {}, "description": "Avanza un paso"},
        {"command": "Debugger.stepInto", "params": {}, "description": "Entra en funcion"},
        {"command": "Debugger.stepOut", "params": {}, "description": "Sale de funcion"},
        {"command": "Debugger.resume", "params": {}, "description": "Continua ejecucion"},
        {"command": "Debugger.pause", "params": {}, "description": "Pausa ejecucion"},
        {"command": "Debugger.getScriptSource", "params": {"scriptId": "string"}, "description": "Codigo fuente de script"},
        {"command": "Debugger.evaluateOnCallFrame", "params": {"callFrameId": "string", "expression": "string"}, "description": "Evalua en frame"},
    ],
    "memory": [
        {"command": "Memory.getDOMCounters", "params": {}, "description": "Contadores DOM"},
        {"command": "HeapProfiler.takeHeapSnapshot", "params": {}, "description": "Snapshot heap"},
        {"command": "HeapProfiler.startTracking", "params": {}, "description": "Inicia tracking"},
        {"command": "HeapProfiler.stopTracking", "params": {}, "description": "Detiene tracking"},
        {"command": "HeapProfiler.collectGarbage", "params": {}, "description": "Fuerza garbage collection"},
        {"command": "HeapProfiler.getHeapObjectId", "params": {"objectId": "string"}, "description": "ID de objeto heap"},
        {"command": "HeapProfiler.getObjectByHeapObjectId", "params": {"heapObjectId": "string"}, "description": "Objeto por ID"},
    ],
    "network": [
        {"command": "Network.enable", "params": {}, "description": "Activa monitoreo red"},
        {"command": "Network.disable", "params": {}, "description": "Desactiva monitoreo red"},
        {"command": "Network.getAllRequests", "params": {}, "description": "Todos los requests"},
        {"command": "Network.getRequestByRequestId", "params": {"requestId": "string"}, "description": "Request por ID"},
        {"command": "Network.getResponseBody", "params": {"requestId": "string"}, "description": "Body de respuesta"},
        {"command": "Network.getRequestBody", "params": {"requestId": "string"}, "description": "Body de request"},
        {"command": "Network.setRequestInterception", "params": {"patterns": [{"urlPattern": "string"}]}, "description": "Intercepta requests"},
        {"command": "Network.clearBrowserCache", "params": {}, "description": "Limpia cache"},
        {"command": "Network.clearBrowserCookies", "params": {}, "description": "Limpia cookies"},
        {"command": "Network.setCacheDisabled", "params": {"cacheDisabled": "boolean"}, "description": "Desactiva cache"},
        {"command": "Network.setCookie", "params": {"name": "string", "value": "string", "url": "string"}, "description": "Anade cookie"},
    ],
    "console": [
        {"command": "Log.enable", "params": {}, "description": "Activa log console"},
        {"command": "Log.disable", "params": {}, "description": "Desactiva log console"},
        {"command": "Console.enable", "params": {}, "description": "Activa consola"},
        {"command": "Console.disable", "params": {}, "description": "Desactiva consola"},
        {"command": "Console.clearMessages", "params": {}, "description": "Limpia mensajes"},
    ],
    "performance": [
        {"command": "Profiler.enable", "params": {}, "description": "Activa profiler"},
        {"command": "Profiler.disable", "params": {}, "description": "Desactiva profiler"},
        {"command": "Profiler.start", "params": {}, "description": "Inicia profiling"},
        {"command": "Profiler.stop", "params": {}, "description": "Detiene profiling"},
        {"command": "Performance.enable", "params": {}, "description": "Activa performance"},
        {"command": "Performance.disable", "params": {}, "description": "Desactiva performance"},
        {"command": "Performance.getMetrics", "params": {}, "description": "Obtiene metricas"},
        {"command": "PerformanceStartTrace", "params": {}, "description": "Inicia tracing"},
        {"command": "PerformanceStopTrace", "params": {}, "description": "Detiene tracing"},
    ],
    "security": [
        {"command": "Security.enable", "params": {}, "description": "Activa security"},
        {"command": "Security.disable", "params": {}, "description": "Desactiva security"},
        {"command": "Security.setIgnoreCertificateErrors", "params": {"ignore": "boolean"}, "description": "Ignora cert errors"},
    ],
    "emulation": [
        {"command": "Emulation.setDeviceMetricsOverride", "params": {"width": "int", "height": "int"}, "description": "Override dimensiones"},
        {"command": "Emulation.setTouchEmulationEnabled", "params": {"enabled": "boolean"}, "description": "Touch emulation"},
        {"command": "Emulation.setLocaleOverride", "params": {"locale": "string"}, "description": "Override locale"},
    ],
    "accessibility": [
        {"command": "Accessibility.getFullAXTree", "params": {}, "description": "Arbol AX completo"},
        {"command": "Accessibility.getPartialAXTree", "params": {"nodesToParse": []}, "description": "Arbol AX parcial"},
        {"command": "Accessibility.getAXNodeAndAncestors", "params": {"nodeId": "int"}, "description": "Nodo AX con ancestros"},
    ],
}

# Instructions templates for each category
INSTRUCTION_TEMPLATES = {
    "navigation": [
        "Ve a {url}",
        "Abre {url} en una nueva pestana",
        "Recarga esta pagina",
        "Recarga sin usar cache",
        "Cierra la pestana actual",
        "Abre about:blank",
        "Cambia el tamano de la ventana a {width}x{height}",
    ],
    "dom": [
        "Encuentra el elemento {selector}",
        "Cuantos elementos {selector} hay?",
        "Dame el HTML del elemento {selector}",
        "Cambia el HTML del elemento {selector}",
        "Cual es el tamano del elemento {selector}?",
        "Que atributos tiene {selector}?",
        "Anade el atributo {name}={value} a {selector}",
        "Elimina el atributo {name} de {selector}",
        "Haz scroll hasta {selector}",
        "Cuantos nodos DOM hay?",
    ],
    "runtime": [
        "Ejecuta {expression}",
        "Llama la funcion {function} en el objeto",
        "Cuales son las propiedades de {object}?",
        "Libera el objeto {objectId}",
        "Libera todos los objetos del grupo {group}",
        "Limpia las entradas de consola",
        "Continua si hay debugger esperando",
    ],
    "debugger": [
        "Activa el debugger",
        "Desactiva el debugger",
        "Pon un breakpoint en {url2} linea {line}",
        "Pon un breakpoint condicional en linea {line}",
        "Elimina el breakpoint {breakpointId}",
        "Avanza un paso",
        "Entra en la siguiente funcion",
        "Sale de la funcion actual",
        "Continua la ejecucion",
        "Pausa la ejecucion",
        "Dame el codigo fuente del script {scriptId}",
        "Evalua {expression} en el call frame actual",
    ],
    "memory": [
        "Cuanta memoria usa JavaScript?",
        "Cuantos nodos DOM hay?",
        "Toma un snapshot del heap",
        "Inicia tracking de memoria",
        "Deten tracking de memoria",
        "Fuerza garbage collection",
        "Obtener ID del objeto {objectId}",
        "Cual es el objeto con ID {heapId}?",
    ],
    "network": [
        "Activa monitoreo de red",
        "Desactiva monitoreo de red",
        "Lista todos los requests",
        "Dame el request {requestId}",
        "Cual fue el body de la respuesta?",
        "Cual fue el body del request?",
        "Intercepta todos los requests a {pattern}",
        "Limpia el cache del navegador",
        "Limpia todas las cookies",
        "Desactiva el cache",
        "Anade una cookie {name}={value}",
    ],
    "console": [
        "Activa monitoreo de consola",
        "Desactiva monitoreo de consola",
        "Limpia todos los mensajes de consola",
    ],
    "performance": [
        "Activa el profiler de CPU",
        "Inicia el profiling",
        "Deten el profiling",
        "Que metricas de performance hay?",
        "Inicia el tracing",
        "Deten el tracing",
    ],
    "security": [
        "Activa el panel de seguridad",
        "Ignora los errores de certificado",
    ],
    "emulation": [
        "Simula dispositivo {width}x{height}",
        "Activa emulacion tactil",
        "Cambia el locale a {locale}",
    ],
    "accessibility": [
        "Dame el arbol de accesibilidad completo",
        "Que elementos accesibles hay?",
    ],
}

# Response templates
RESPONSE_TEMPLATES = {
    "Memory.getDOMCounters": [
        "Heap: {heap} bytes, Nodos: {nodes}, Listeners: {listeners}",
        "JSHeap: {heap} bytes usado de {total}",
    ],
    "DOM.querySelector": [
        "Encontrado: nodeId {nodeId}",
        "Elemento con selector {selector}: {nodeId}",
    ],
    "HeapProfiler.takeHeapSnapshot": [
        "Snapshot capturado. Tamano: {size}",
        "Heap snapshot listo para analisis",
    ],
    "Runtime.evaluate": [
        "Resultado: {result}",
        "{expression} = {result}",
    ],
    "Network.enable": [
        "Monitoreo de red activado",
        "Todos los requests seran capturados",
    ],
    "Debugger.enable": [
        "Debugger activado",
        "Breakpoints disponibles",
    ],
    "Profiler.start": [
        "Profiling iniciado",
        "Grabando metricas de CPU",
    ],
}

def generate_examples(count=1000):
    """Generate training examples"""
    examples = []
    example_id = 1
    
    categories = list(CDP_COMMANDS.keys())
    
    while len(examples) < count:
        for category in categories:
            if len(examples) >= count:
                break
            
            commands = CDP_COMMANDS[category]
            templates = INSTRUCTION_TEMPLATES[category]
            
            for cmd in commands:
                if len(examples) >= count:
                    break
                    
                # Generate variations
                for _ in range(3):  # 3 variations per command
                    if len(examples) >= count:
                        break
                    
                    # Fill template
                    template = random.choice(templates)
                    
                    # Replace placeholders
                    params = {}
                    instruction = template
                    
                    replacements = {
                        "url": random.choice(["https://google.com", "https://github.com", "https://perplexity.ai"]),
                        "selector": random.choice(["body", "div", "button", "input", "#main", ".container", "a", "form"]),
                        "width": random.choice([375, 768, 1024, 1920]),
                        "height": random.choice([667, 1024, 1080]),
                        "expression": random.choice(["document.title", "window.location.href", "document.cookie", "localStorage.length", "navigator.userAgent"]),
                        "function": random.choice(["click()", "submit()", "focus()", "blur()"]),
                        "object": random.choice(["element", "window", "document", "console"]),
                        "objectId": "obj_123",
                        "group": random.choice(["temp", "session", "cache"]),
                        "line": str(random.randint(1, 100)),
                        "breakpointId": "bp_" + str(random.randint(1, 100)),
                        "url2": "app.js",
                        "scriptId": "script_123",
                        "requestId": "req_123",
                        "pattern": random.choice(["api/*", "/api/*", "*.json"]),
                        "name": random.choice(["class", "id", "data-test"]),
                        "value": random.choice(["active", "test", "true"]),
                        "heapId": "heap_123",
                        "locale": random.choice(["en-US", "es-ES", "fr-FR"]),
                        "heap": str(random.randint(1000000, 50000000)),
                        "nodes": str(random.randint(100, 5000)),
                        "listeners": str(random.randint(10, 500)),
                        "total": str(random.randint(50000000, 100000000)),
                        "size": str(random.randint(1000000, 10000000)),
                        "result": '"test"',
                        "nodeId": str(random.randint(1, 1000)),
                    }
                    
                    for key, val in replacements.items():
                        if f'{{{key}}}' in instruction:
                            instruction = instruction.replace(f'{{{key}}}', str(val))
                            if key in ['url', 'url2', 'pattern']:
                                params[key] = val
                            elif key in ['width', 'height', 'line']:
                                params[key] = int(val)
                    
                    # Build params (simplified)
                    final_params = {}
                    for param_name, param_type in cmd["params"].items():
                        if param_name in params:
                            final_params[param_name] = params[param_name]
                        elif param_type == "string":
                            final_params[param_name] = f"{{{param_name}}}"
                        elif param_type == "boolean":
                            final_params[param_name] = True
                        elif param_type == "int":
                            final_params[param_name] = 100
                    
                    # Generate response example
                    response_template = random.choice(RESPONSE_TEMPLATES.get(cmd["command"], [cmd["description"]]))
                    response = response_template.format(**replacements)
                    
                    example = {
                        "id": example_id,
                        "category": category,
                        "instruction": instruction,
                        "cdp_command": cmd["command"],
                        "cdp_params": final_params,
                        "context": f"Esta usando Chrome DevTools Protocol para {cmd['description']}",
                        "response_example": response,
                    }
                    
                    examples.append(example)
                    example_id += 1
    
    return examples

# Generate dataset
print("Generating CDP training dataset...")
dataset = generate_examples(1000)
print(f"Generated {len(dataset)} examples")

# Save as JSONL
with open('D:/Parasyte/data/cdp_training_dataset.jsonl', 'w', encoding='utf-8') as f:
    for ex in dataset:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Saved to D:/Parasyte/data/cdp_training_dataset.jsonl")

# Also save pretty JSON
with open('D:/Parasyte/data/cdp_training_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"Saved to D:/Parasyte/data/cdp_training_dataset.json")

# Statistics
categories = {}
for ex in dataset:
    cat = ex['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\nDataset statistics:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
