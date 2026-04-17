#!/usr/bin/env python3
"""
PARASYTE - CDP Training Dataset Generator v2

Genera dataset de entrenamiento con mapeo SEMANTICO correcto.
"""

import json
import random
from typing import Dict, List, Any, Tuple

# Mapeo semantico simple: instruction keywords -> CDP command + params builder
NAVIGATION_MAP = [
    (["ve a", "navega a", "ir a", "visitar"], lambda m: ("Page.navigate", {"url": extract_url(m)})),
    (["recarga", "refresca", "reload"], lambda m: ("Page.reload", {"ignoreCache": "cache" in m.lower()})),
    (["nueva pestana", "nueva tab", "nueva ventana"], lambda m: ("Target.createTarget", {"url": extract_url(m) or "about:blank"})),
    (["cierra", "cerrar pestana"], lambda m: ("Target.closeTarget", {"targetId": "{{TARGET_ID}}"})),
    (["trae", "frente", "enfoca", "activa"], lambda m: ("Page.bringToFront", {})),
    (["tamano", "tamanio", "dimension", "viewport"], lambda m: ("Emulation.setDeviceMetricsOverride", extract_dimensions(m))),
]

DOM_MAP = [
    (["encuentra", "busca", "localiza", "selecciona", "elemento"], lambda m: ("DOM.querySelector", {"selector": extract_selector(m)})),
    (["cuantos", "numero de", "count", "lista todos", "cuantas"], lambda m: ("DOM.querySelectorAll", {"selector": extract_selector(m)})),
    (["html", "innerhtml", "outerhtml", "contenido"], lambda m: ("DOM.getOuterHTML", {"nodeId": extract_nodeid(m)})),
    (["atributos", "propiedades del elemento"], lambda m: ("DOM.getAttributes", {"nodeId": extract_nodeid(m)})),
    (["anade", "agrega", "set atributo", "disabled al"], lambda m: ("DOM.setAttributeValue", {"nodeId": extract_nodeid(m), "name": extract_attr_name(m), "value": extract_attr_value(m)})),
    (["posicion", "bounding", "tamano del elemento", "tamanio del elemento"], lambda m: ("DOM.getBoxModel", {"nodeId": extract_nodeid(m)})),
]

RUNTIME_MAP = [
    (["ejecuta", "evalua", "corre", "run", "execute"], lambda m: ("Runtime.evaluate", {"expression": extract_expression(m), "returnByValue": True})),
    (["titulo", "title de la pagina"], lambda m: ("Runtime.evaluate", {"expression": "document.title", "returnByValue": True})),
    (["url actual", "direccion actual"], lambda m: ("Runtime.evaluate", {"expression": "window.location.href", "returnByValue": True})),
    (["cookies"], lambda m: ("Runtime.evaluate", {"expression": "document.cookie", "returnByValue": True})),
    (["localstorage", "sessionstorage", "storage"], lambda m: ("Runtime.evaluate", {"expression": extract_storage_expr(m.lower()), "returnByValue": True})),
    (["scroll", "desplazamiento"], lambda m: ("Runtime.evaluate", {"expression": "{x: window.scrollX, y: window.scrollY}", "returnByValue": True})),
    (["listeners", "eventos"], lambda m: ("Runtime.evaluate", {"expression": "getEventListeners(document).length", "returnByValue": True})),
    (["cargada", "ready"], lambda m: ("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})),
    (["react", "vue", "framework"], lambda m: ("Runtime.evaluate", {"expression": "Object.keys(window).filter(k => k.includes('react') || k.includes('vue')).join(', ')", "returnByValue": True})),
    (["simula", "click", "presiona"], lambda m: ("Runtime.evaluate", {"expression": "document.querySelector('{{selector}}').click()", "returnByValue": True})),
    (["escribe", "type"], lambda m: ("Runtime.evaluate", {"expression": "document.querySelector('{{selector}}').value = '{{text}}'", "returnByValue": True})),
    (["user agent"], lambda m: ("Runtime.evaluate", {"expression": "navigator.userAgent", "returnByValue": True})),
    (["imagenes"], lambda m: ("Runtime.evaluate", {"expression": "document.querySelectorAll('img').length", "returnByValue": True})),
    (["aria-label", "accesible"], lambda m: ("Runtime.evaluate", {"expression": "document.querySelectorAll('[aria-label]').length", "returnByValue": True})),
]

DEBUGGER_MAP = [
    (["activa debugger", "habilita debugger", "enable debugger"], lambda m: ("Debugger.enable", {})),
    (["desactiva debugger", "disable debugger"], lambda m: ("Debugger.disable", {})),
    (["breakpoint", "para aqui", "pausa en"], lambda m: ("Debugger.setBreakpointByUrl", {"url": extract_script(m), "lineNumber": extract_line(m)})),
    (["step over", "avanza", "siguiente"], lambda m: ("Debugger.stepOver", {})),
    (["step into", "entra", "dentro"], lambda m: ("Debugger.stepInto", {})),
    (["step out", "sale", "fuera"], lambda m: ("Debugger.stepOut", {})),
    (["resume", "reanuda", "continua"], lambda m: ("Debugger.resume", {})),
    (["pausa", "pause", "detener ejecucion"], lambda m: ("Debugger.pause", {})),
]

MEMORY_MAP = [
    (["memoria", "ram"], lambda m: ("Memory.getDOMCounters", {})),
    (["snapshot", "heap snapshot", "instantanea"], lambda m: ("HeapProfiler.takeHeapSnapshot", {})),
    (["gc", "garbage", "recoge basura"], lambda m: ("HeapProfiler.collectGarbage", {})),
    (["leak", "fuga"], lambda m: ("HeapProfiler.takeHeapSnapshot", {})),
]

NETWORK_MAP = [
    (["activa red", "enable network", "monitorear red", "monitoreo de red"], lambda m: ("Network.enable", {})),
    (["desactiva red", "disable network"], lambda m: ("Network.disable", {})),
    (["requests", "peticiones", "endpoints", "trafico"], lambda m: ("Network.getAllRequests", {})),
    (["intercepta", "interception", "bloquea"], lambda m: ("Network.setRequestInterception", {"patterns": [{"urlPattern": extract_pattern(m)}]})),
    (["clear cache", "limpia cache", "borra cache"], lambda m: ("Network.clearBrowserCache", {})),
    (["clear cookies", "limpia cookies", "borra cookies"], lambda m: ("Network.clearBrowserCookies", {})),
    (["response body", "respuesta", "body de la respuesta"], lambda m: ("Network.getResponseBody", {"requestId": "{{REQUEST_ID}}"})),
]

PERFORMANCE_MAP = [
    (["profiler", "profiling", "cpu"], lambda m: ("Profiler.enable", {})),
    (["start", "comienza", "grabar"], lambda m: ("Profiler.start", {})),
    (["stop", "deten", "terminar"], lambda m: ("Profiler.stop", {})),
    (["metricas", "metrics"], lambda m: ("Performance.getMetrics", {})),
]

CONSOLE_MAP = [
    (["consola", "console logs", "monitoreo de consola"], lambda m: ("Log.enable", {})),
    (["errores en consola", "errores de javascript", "hay errores", "hay memory"], lambda m: ("Runtime.evaluate", {"expression": "window.__errors?.length || 0", "returnByValue": True})),
]

CATEGORY_MAPS = {
    "navigation": NAVIGATION_MAP,
    "dom": DOM_MAP,
    "runtime": RUNTIME_MAP,
    "debugger": DEBUGGER_MAP,
    "memory": MEMORY_MAP,
    "network": NETWORK_MAP,
    "performance": PERFORMANCE_MAP,
    "console": CONSOLE_MAP,
}

URLS = ["https://perplexity.ai", "https://google.com", "https://github.com", "https://twitter.com", "https://youtube.com"]
SELECTORS = ["body", "div", "button", "input", "form", "a", "span", "#main", ".container", "#app", "[data-test]", "nav"]
SCRIPTS = ["app.js", "index.js", "main.js", "bundle.js", "script.js"]

def extract_url(text: str) -> str:
    import re
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return random.choice(URLS)

def extract_selector(text: str) -> str:
    import re
    id_match = re.search(r'#(\w+)', text)
    if id_match:
        return f"#{id_match.group(1)}"
    class_match = re.search(r'\.(\w+)', text)
    if class_match:
        return f".{class_match.group(1)}"
    for sel in SELECTORS:
        if sel.lower() in text.lower():
            return sel
    return random.choice(SELECTORS)

def extract_nodeid(text: str) -> int:
    import re
    match = re.search(r'node[_-]?id[:\s=]*(\d+)', text, re.I)
    if match:
        return int(match.group(1))
    return random.randint(1, 1000)

def extract_script(text: str) -> str:
    import re
    for script in SCRIPTS:
        if script in text.lower():
            return script
    match = re.search(r'([\w-]+\.js)', text, re.I)
    if match:
        return match.group(1)
    return random.choice(SCRIPTS)

def extract_line(text: str) -> int:
    import re
    match = re.search(r'line[:\s]*(\d+)', text, re.I)
    if match:
        return int(match.group(1))
    match = re.search(r':(\d+)$', text)
    if match:
        return int(match.group(1))
    return random.randint(1, 200)

def extract_expression(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["titulo", "title"]):
        return "document.title"
    elif "url" in text_lower or "location" in text_lower:
        return "window.location.href"
    elif "cookie" in text_lower:
        return "document.cookie"
    elif "local" in text_lower or "storage" in text_lower:
        return "Object.keys(localStorage)"
    elif "nodos" in text_lower or "nodes" in text_lower:
        return "document.querySelectorAll('*').length"
    elif "scroll" in text_lower:
        return "{x: window.scrollX, y: window.scrollY}"
    return random.choice(["document.title", "window.location.href", "document.readyState"])

def extract_storage_expr(text: str) -> str:
    if "local" in text:
        return "JSON.stringify(localStorage)"
    elif "session" in text:
        return "JSON.stringify(sessionStorage)"
    return "Object.keys(localStorage)"

def extract_dimensions(text: str) -> dict:
    import re
    match = re.search(r'(\d+)\s*[xX×]\s*(\d+)', text)
    if match:
        return {"width": int(match.group(1)), "height": int(match.group(2))}
    presets = [{"width": 375, "height": 667}, {"width": 768, "height": 1024}, {"width": 1920, "height": 1080}]
    return random.choice(presets)

def extract_pattern(text: str) -> str:
    patterns = ["api/*", "/api/*", "*.json", "*.js", "*.css"]
    for p in patterns:
        if p.replace("*", "") in text.lower():
            return p
    return random.choice(patterns)

def extract_attr_name(text: str) -> str:
    names = ["disabled", "readonly", "checked", "class", "id", "data-test", "aria-label"]
    for name in names:
        if name in text.lower():
            return name
    return random.choice(names)

def extract_attr_value(text: str) -> str:
    import re
    match = re.search(r'=\s*["\']?([^"\'\s,]+)["\']?', text)
    if match:
        return match.group(1)
    return random.choice(["true", "active", "test", "enabled"])

def find_command(instruction: str, category: str) -> Tuple[str, dict]:
    """Find CDP command for instruction"""
    instruction_lower = instruction.lower()
    
    # Try category-specific maps first
    if category in CATEGORY_MAPS:
        for keywords, cmd_builder in CATEGORY_MAPS[category]:
            if any(kw in instruction_lower for kw in keywords):
                return cmd_builder(instruction)
    
    # Try all categories
    for cat, mappings in CATEGORY_MAPS.items():
        for keywords, cmd_builder in mappings:
            if any(kw in instruction_lower for kw in keywords):
                return cmd_builder(instruction)
    
    # Default
    return "Runtime.evaluate", {"expression": instruction, "returnByValue": True}

def get_response(command: str) -> str:
    responses = {
        "Page.navigate": "Pagina cargada",
        "Page.reload": "Pagina recargada",
        "Target.createTarget": "Nueva pestana creada",
        "Target.closeTarget": "Pestana cerrada",
        "Page.bringToFront": "Pagina traida al frente",
        "Emulation.setDeviceMetricsOverride": "Viewport modificado",
        "DOM.querySelector": "Elemento encontrado",
        "DOM.querySelectorAll": "Elementos encontrados",
        "DOM.getOuterHTML": "HTML obtenido",
        "DOM.getAttributes": "Atributos listados",
        "DOM.setAttributeValue": "Atributo modificado",
        "DOM.getBoxModel": "Box model obtenido",
        "Runtime.evaluate": "Resultado obtenido",
        "Debugger.enable": "Debugger activado",
        "Debugger.disable": "Debugger desactivado",
        "Debugger.setBreakpointByUrl": "Breakpoint establecido",
        "Debugger.stepOver": "Avanzado un paso",
        "Debugger.stepInto": "Entrado en funcion",
        "Debugger.stepOut": "Salido de funcion",
        "Debugger.resume": "Ejecucion reanudada",
        "Debugger.pause": "Ejecucion pausada",
        "Memory.getDOMCounters": "Contadores de memoria",
        "HeapProfiler.takeHeapSnapshot": "Snapshot capturado",
        "HeapProfiler.collectGarbage": "GC ejecutado",
        "Network.enable": "Red habilitada",
        "Network.disable": "Red deshabilitada",
        "Network.getAllRequests": "Requests listados",
        "Network.setRequestInterception": "Interceptacion configurada",
        "Network.clearBrowserCache": "Cache limpiado",
        "Network.clearBrowserCookies": "Cookies limpiadas",
        "Network.getResponseBody": "Body obtenido",
        "Profiler.enable": "Profiler activado",
        "Profiler.start": "Profiling iniciado",
        "Profiler.stop": "Profiling detenido",
        "Performance.getMetrics": "Metricas obtenidas",
        "Log.enable": "Consola habilitada",
    }
    return responses.get(command, "Comando ejecutado")

def generate_examples() -> List[Dict]:
    """Base instruction examples"""
    return [
        {"instruction": "Ve a perplexity.ai", "category": "navigation"},
        {"instruction": "Navega a google.com", "category": "navigation"},
        {"instruction": "Recarga la pagina sin usar cache", "category": "navigation"},
        {"instruction": "Cierra la pestana actual", "category": "navigation"},
        {"instruction": "Abre una nueva pestana con github.com", "category": "navigation"},
        {"instruction": "Trae la pestana al frente", "category": "navigation"},
        {"instruction": "Cambia el tamano a 1920x1080", "category": "navigation"},
        {"instruction": "Encuentra el elemento button", "category": "dom"},
        {"instruction": "Cuantos elementos div hay?", "category": "dom"},
        {"instruction": "Dame el HTML del elemento #main", "category": "dom"},
        {"instruction": "Que atributos tiene el elemento body?", "category": "dom"},
        {"instruction": "Anade disabled al boton submit", "category": "dom"},
        {"instruction": "Cual es el tamano del elemento #container?", "category": "dom"},
        {"instruction": "Ejecuta document.title", "category": "runtime"},
        {"instruction": "Cual es el titulo de la pagina?", "category": "runtime"},
        {"instruction": "Dame la URL actual", "category": "runtime"},
        {"instruction": "Que cookies hay en este sitio?", "category": "runtime"},
        {"instruction": "Lista las claves de localStorage", "category": "runtime"},
        {"instruction": "Cual es la posicion del scroll?", "category": "runtime"},
        {"instruction": "Activa el debugger", "category": "debugger"},
        {"instruction": "Pon un breakpoint en app.js linea 42", "category": "debugger"},
        {"instruction": "Avanza un paso", "category": "debugger"},
        {"instruction": "Entra en la siguiente funcion", "category": "debugger"},
        {"instruction": "Sale de la funcion actual", "category": "debugger"},
        {"instruction": "Continua la ejecucion", "category": "debugger"},
        {"instruction": "Pausa la ejecucion", "category": "debugger"},
        {"instruction": "Cuanta memoria usa JavaScript?", "category": "memory"},
        {"instruction": "Toma un snapshot del heap", "category": "memory"},
        {"instruction": "Hay memory leaks?", "category": "memory"},
        {"instruction": "Fuerza garbage collection", "category": "memory"},
        {"instruction": "Activa el monitoreo de red", "category": "network"},
        {"instruction": "Lista todos los requests", "category": "network"},
        {"instruction": "Intercepta las peticiones a /api/*", "category": "network"},
        {"instruction": "Limpia el cache", "category": "network"},
        {"instruction": "Limpia las cookies", "category": "network"},
        {"instruction": "Activa el profiler de CPU", "category": "performance"},
        {"instruction": "Comienza el profiling", "category": "performance"},
        {"instruction": "Deten el profiling", "category": "performance"},
        {"instruction": "Que metricas de performance hay?", "category": "performance"},
        {"instruction": "Activa el monitoreo de consola", "category": "console"},
        {"instruction": "Hay errores en consola?", "category": "console"},
        {"instruction": "Cuantos errores hay?", "category": "console"},
        {"instruction": "Verifica si hay errores de JavaScript", "category": "console"},
        {"instruction": "Cuantos listeners hay en el documento?", "category": "runtime"},
        {"instruction": "Esta la pagina completamente cargada?", "category": "runtime"},
        {"instruction": "Que version de React usa esta app?", "category": "runtime"},
        {"instruction": "Simula un click en el menu", "category": "runtime"},
        {"instruction": "Escribe 'test' en el campo username", "category": "runtime"},
        {"instruction": "Cual es el user agent?", "category": "runtime"},
        {"instruction": "Hay elementos con aria-label?", "category": "runtime"},
        {"instruction": "Cuantas imagenes tiene la pagina?", "category": "runtime"},
    ]

def generate_dataset(count: int = 500) -> List[Dict]:
    """Generate training dataset"""
    dataset = []
    examples = generate_examples()
    
    for i in range(count):
        base = random.choice(examples)
        instruction = base["instruction"]
        category = base["category"]
        
        command, params = find_command(instruction, category)
        response = get_response(command)
        
        dataset.append({
            "id": i + 1,
            "category": category,
            "instruction": instruction,
            "cdp_command": command,
            "cdp_params": params,
            "context": f"Usando Chrome DevTools Protocol para analisis de {category}",
            "response_example": response,
        })
    
    return dataset

def main():
    print("=" * 60)
    print("PARASYTE - CDP Training Dataset Generator v2")
    print("=" * 60)
    
    print("\nGenerando dataset con mapeo semantico correcto...")
    dataset = generate_dataset(500)
    print(f"Generados {len(dataset)} ejemplos")
    
    # Save
    with open("D:/Parasyte/data/cdp_training_v2.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    with open("D:/Parasyte/data/cdp_training_v2.jsonl", "w", encoding="utf-8") as f:
        for ex in dataset:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    
    print("Guardado en D:/Parasyte/data/")
    
    # Stats
    categories = {}
    commands = {}
    for ex in dataset:
        categories[ex["category"]] = categories.get(ex["category"], 0) + 1
        commands[ex["cdp_command"]] = commands.get(ex["cdp_command"], 0) + 1
    
    print(f"\nCategorias: {len(categories)}")
    print(f"Comandos unicos: {len(commands)}")
    
    print("\nPor categoria:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    print("\nTop comandos:")
    for cmd, count in sorted(commands.items(), key=lambda x: -x[1])[:10]:
        print(f"  {cmd}: {count}")
    
    print("\n" + "=" * 60)
    print("Dataset generado exitosamente!")
    print("=" * 60)

if __name__ == "__main__":
    main()
