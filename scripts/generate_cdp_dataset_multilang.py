#!/usr/bin/env python3
"""
PARASYTE - Multi-language CDP Training Dataset Generator

Genera dataset con instrucciones en MULTIPLES IDIOMAS mapeando al mismo comando CDP.
El modelo aprende la semantica universal de DevTools.
"""

import json
import random
from typing import Dict, List, Any, Tuple

# ============================================
# MULTI-LANGUAGE INSTRUCTION TEMPLATES
# ============================================
# Each command has instructions in multiple languages
# that map to the same CDP command

CDP_COMMANDS = {
    # NAVIGATION
    "Page.navigate": {
        "description": "Navigate to a URL",
        "templates": {
            "en": ["Go to {url}", "Navigate to {url}", "Visit {url}", "Open {url}", "Load {url}"],
            "es": ["Ve a {url}", "Navega a {url}", "Ir a {url}", "Visitar {url}", "Abre {url}"],
            "fr": ["Aller a {url}", "Naviguer vers {url}", "Visiter {url}", "Ouvrir {url}"],
            "de": ["Gehe zu {url}", "Navigiere zu {url}", "Oeffne {url}"],
            "zh": ["Dakai {url}", "Zhuan dao {url}", "Fangwen {url}"],
        },
        "param": lambda: {"url": random.choice(URLS)},
    },
    
    "Page.reload": {
        "description": "Reload the current page",
        "templates": {
            "en": ["Reload the page", "Refresh the page", "Reload without cache", "Refresh ignoring cache"],
            "es": ["Recarga la pagina", "Refresca la pagina", "Recarga sin cache", "Refresca ignorando cache"],
            "fr": ["Recharger la page", "Actualiser la page", "Recharger sans cache"],
            "de": ["Seite neu laden", "Aktualisieren", "Neu laden ohne Cache"],
            "zh": ["Chongxin jiazai ye mian", "Shuaxin", "Wuxu huancun chongxin jiazai"],
        },
        "param": lambda: {"ignoreCache": random.random() > 0.5},
    },
    
    "Target.createTarget": {
        "description": "Create a new tab/window",
        "templates": {
            "en": ["Open a new tab", "Create new tab with {url}", "Open {url} in new tab", "New window with {url}"],
            "es": ["Abre una nueva pestana", "Nueva pestana con {url}", "Abre {url} en pestana nueva", "Nueva ventana con {url}"],
            "fr": ["Ouvrir un nouvel onglet", "Nouvel onglet avec {url}", "Onglet pour {url}"],
            "de": ["Neuen Tab oeffnen", "Neuer Tab mit {url}", "Neues Fenster mit {url}"],
            "zh": ["Dakai xin biaoqian", "Xin biaoqian fangwen {url}"],
        },
        "param": lambda: {"url": random.choice(URLS)},
    },
    
    "Target.closeTarget": {
        "description": "Close current tab",
        "templates": {
            "en": ["Close the current tab", "Close this tab", "Close the window"],
            "es": ["Cierra la pestana actual", "Cierra esta pestana", "Cierra la ventana"],
            "fr": ["Fermer l'onglet actuel", "Fermer cet onglet", "Fermer la fenetre"],
            "de": ["Aktuellen Tab schliessen", "Tab schliessen", "Fenster schliessen"],
            "zh": ["Guanbi dangqian biaoqian", "Guanbi biaoqian", "Guanbi chuangkou"],
        },
        "param": lambda: {"targetId": "{{TARGET_ID}}"},
    },
    
    "Page.bringToFront": {
        "description": "Bring page to foreground",
        "templates": {
            "en": ["Bring to front", "Focus this tab", "Activate this tab", "Show this tab"],
            "es": ["Trae al frente", "Enfoca esta pestana", "Activa esta pestana", "Muestra esta pestana"],
            "fr": ["Mettre au premier plan", "Activer cet onglet", "Afficher cet onglet"],
            "de": ["In den Vordergrund bringen", "Fokus auf diesen Tab", "Tab aktivieren"],
            "zh": ["Zhi qian mian", "Jihuo biaoqian", "Xianshi biaoqian"],
        },
        "param": lambda: {},
    },
    
    "Emulation.setDeviceMetricsOverride": {
        "description": "Set viewport dimensions",
        "templates": {
            "en": ["Set viewport to {w}x{h}", "Change window size to {w}x{h}", "Resize to {w}x{h}", "Set screen size {w}x{h}"],
            "es": ["Cambia tamano a {w}x{h}", "Establece viewport a {w}x{h}", "Redimensiona a {w}x{h}", "Tamano de pantalla {w}x{h}"],
            "fr": ["Definir la taille a {w}x{h}", "Changer la taille de la fenetre a {w}x{h}", "Redimensionner a {w}x{h}"],
            "de": ["Fenster auf {w}x{h} setzen", "Groesse aendern auf {w}x{h}", "Bildschirmgroesse {w}x{h}"],
            "zh": ["Shezhi shiping wei {w}x{h}", "Gengai chuangkou da xiao wei {w}x{h}"],
        },
        "param": lambda: random.choice(DIMENSIONS),
    },
    
    # DOM
    "DOM.querySelector": {
        "description": "Find element by CSS selector",
        "templates": {
            "en": ["Find element {sel}", "Query selector {sel}", "Get element {sel}", "Locate {sel}"],
            "es": ["Encuentra elemento {sel}", "Busca elemento {sel}", "Consulta {sel}", "Localiza {sel}"],
            "fr": ["Trouver l'element {sel}", "Rechercher {sel}", "Element {sel}"],
            "de": ["Element finden {sel}", "Suche {sel}", "Lokalisieren {sel}"],
            "zh": ["Zhhao {sel} yuansu", "Chaxun {sel}", "Dingwei {sel}"],
        },
        "param": lambda: {"selector": random.choice(SELECTORS)},
    },
    
    "DOM.querySelectorAll": {
        "description": "Find all matching elements",
        "templates": {
            "en": ["Count {sel} elements", "How many {sel}?", "List all {sel}", "Find all {sel} elements"],
            "es": ["Cuantos elementos {sel}?", "Cuenta {sel}", "Lista todos {sel}", "Encuentra todos {sel}"],
            "fr": ["Compter les elements {sel}", "Combien de {sel}?", "Tous les {sel}"],
            "de": ["Wie viele {sel}?", "Zaehle {sel}", "Alle {sel} finden"],
            "zh": ["You duo shao {sel}?", "Jisu {sel} shuliang", "Sousuo suoyou {sel}"],
        },
        "param": lambda: {"selector": random.choice(SELECTORS)},
    },
    
    "DOM.getOuterHTML": {
        "description": "Get element HTML",
        "templates": {
            "en": ["Get HTML of {sel}", "What is the HTML of {sel}?", "Show outer HTML of {sel}"],
            "es": ["Dame el HTML de {sel}", "Cual es el HTML de {sel}?", "HTML externo de {sel}"],
            "fr": ["Donne le HTML de {sel}", "Quel est le HTML de {sel}?"],
            "de": ["HTML von {sel} abrufen", "Was ist das HTML von {sel}?"],
            "zh": ["Huode {sel} de HTML", "{sel} de HTML neirong"],
        },
        "param": lambda: {"nodeId": random.randint(1, 1000)},
    },
    
    "DOM.getBoxModel": {
        "description": "Get element dimensions and position",
        "templates": {
            "en": ["Get size of {sel}", "What are the dimensions of {sel}?", "Position of {sel}", "Bounding box of {sel}"],
            "es": ["Cual es el tamano de {sel}?", "Posicion de {sel}", "Tamano del elemento {sel}", "Caja delimitadora de {sel}"],
            "fr": ["Taille de {sel}?", "Position de {sel}", "Dimensions de {sel}"],
            "de": ["Groesse von {sel}", "Position von {sel}", "Abmessungen von {sel}"],
            "zh": ["{sel} de da xiao", "{sel} de weizhi", "{sel} de chicun"],
        },
        "param": lambda: {"nodeId": random.randint(1, 1000)},
    },
    
    "DOM.setAttributeValue": {
        "description": "Set element attribute",
        "templates": {
            "en": ["Set {attr}={val} on {sel}", "Add {attr} attribute to {sel}", "Set attribute {attr} to {val}"],
            "es": ["Anade {attr}={val} a {sel}", "Establece {attr}={val} en {sel}", "Agrega atributo {attr} a {sel}"],
            "fr": ["Definir {attr}={val} sur {sel}", "Ajouter {attr} a {sel}"],
            "de": ["Setze {attr}={val} auf {sel}", "Attribut {attr} zu {sel} hinzufuegen"],
            "zh": ["Shezhi {sel} de shuxing {attr} wei {val}"],
        },
        "param": lambda: {"nodeId": random.randint(1, 1000), "name": random.choice(ATTR_NAMES), "value": random.choice(ATTR_VALUES)},
    },
    
    # RUNTIME
    "Runtime.evaluate": {
        "description": "Execute JavaScript",
        "templates": {
            "en": [
                "Execute {expr}",
                "Run JavaScript: {expr}",
                "Evaluate {expr}",
                "What is {expr}?",
                "Get page title",
                "What is the current URL?",
                "Get cookies",
                "Get localStorage",
                "Get scroll position",
                "How many listeners?",
                "Is page loaded?",
                "What is the user agent?",
                "How many images?",
                "Check for accessibility",
            ],
            "es": [
                "Ejecuta {expr}",
                "Corre JavaScript: {expr}",
                "Evalua {expr}",
                "Cual es {expr}?",
                "Cual es el titulo de la pagina?",
                "Cual es la URL actual?",
                "Dame las cookies",
                "Dame el localStorage",
                "Posicion del scroll?",
                "Cuantos listeners?",
                "Esta la pagina cargada?",
                "Cual es el user agent?",
                "Cuantas imagenes hay?",
                "Verifica accesibilidad",
            ],
            "fr": [
                "Executer {expr}",
                "Lancer JavaScript: {expr}",
                "Evaluer {expr}",
                "Quel est {expr}?",
            ],
            "de": [
                "Fuehre {expr} aus",
                "JavaScript ausfuehren: {expr}",
                "Berechne {expr}",
            ],
            "zh": [
                "Zhixing {expr}",
                "Yunxing JavaScript: {expr}",
                "Pinggu {expr}",
            ],
        },
        "param": lambda: {"expression": random.choice(EXPRESSIONS), "returnByValue": True},
    },
    
    # DEBUGGER
    "Debugger.enable": {
        "description": "Enable JavaScript debugger",
        "templates": {
            "en": ["Enable debugger", "Turn on debugger", "Activate debugging"],
            "es": ["Activa el debugger", "Activa depuracion", "Activar modo debug"],
            "fr": ["Activer le debogueur", "Activer le mode debug"],
            "de": ["Debugger aktivieren", "Debugging einschalten"],
            "zh": ["Qiyong tiaoshi", "Kaishi tiaoshi moshi"],
        },
        "param": lambda: {},
    },
    
    "Debugger.disable": {
        "description": "Disable debugger",
        "templates": {
            "en": ["Disable debugger", "Turn off debugger"],
            "es": ["Desactiva el debugger", "Desactiva depuracion"],
            "fr": ["Desactiver le debogueur"],
            "de": ["Debugger deaktivieren"],
            "zh": ["Ting yong tiaoshi"],
        },
        "param": lambda: {},
    },
    
    "Debugger.setBreakpointByUrl": {
        "description": "Set breakpoint in script",
        "templates": {
            "en": ["Set breakpoint in {script} at line {line}", "Breakpoint at {script}:{line}", "Pause at {script} line {line}"],
            "es": ["Pon breakpoint en {script} linea {line}", "Pausa en {script}:{line}", "Breakpoint en {script} linea {line}"],
            "fr": ["Definir breakpoint dans {script} ligne {line}", "Pause a {script}:{line}"],
            "de": ["Breakpoint in {script} Zeile {line}", "Pause bei {script}:{line}"],
            "zh": ["Zai {script} di {line} hang shezhi duandian"],
        },
        "param": lambda: {"url": random.choice(SCRIPTS), "lineNumber": random.randint(1, 200)},
    },
    
    "Debugger.stepOver": {
        "description": "Step over next line",
        "templates": {
            "en": ["Step over", "Next line", "Step to next statement", "Continue to next line"],
            "es": ["Avanza un paso", "Siguiente linea", "Continua a la siguiente", "Step over"],
            "fr": ["Passer a la ligne suivante", "Avancer d'un pas"],
            "de": ["Naechste Zeile", "Darueber steppen"],
            "zh": ["Tiaoguo xing", "Xia yi hang"],
        },
        "param": lambda: {},
    },
    
    "Debugger.stepInto": {
        "description": "Step into function",
        "templates": {
            "en": ["Step into", "Enter function", "Go into next call", "Step inside"],
            "es": ["Entra en la funcion", "Step into", "Adentrate en la llamada", "Entra en"],
            "fr": ["Entrer dans la fonction", "Step into"],
            "de": ["In Funktion gehen", "Step into"],
            "zh": ["Jinru hanshu", "Tiaoru"],
        },
        "param": lambda: {},
    },
    
    "Debugger.stepOut": {
        "description": "Step out of function",
        "templates": {
            "en": ["Step out", "Exit function", "Return from function", "Go out of current function"],
            "es": ["Sale de la funcion", "Step out", "Sal de la funcion actual", "Regresa de la funcion"],
            "fr": ["Sortir de la fonction", "Step out"],
            "de": ["Aus Funktion heraus", "Step out"],
            "zh": ["Tiaochu hanshu", "Li kai hanshu"],
        },
        "param": lambda: {},
    },
    
    "Debugger.resume": {
        "description": "Resume execution",
        "templates": {
            "en": ["Resume", "Continue execution", "Run to next breakpoint", "Continue"],
            "es": ["Continua", "Reanuda la ejecucion", "Continua hasta el proximo breakpoint"],
            "fr": ["Reprendre", "Continuer l'execution"],
            "de": ["Fortsetzen", "Ausfuehrung fortsetzen"],
            "zh": ["Jixu zhixing", "Huifu"],
        },
        "param": lambda: {},
    },
    
    "Debugger.pause": {
        "description": "Pause execution",
        "templates": {
            "en": ["Pause", "Pause execution", "Break", "Suspend execution"],
            "es": ["Pausa", "Pausa la ejecucion", "Detener ejecucion", "Interrumpir"],
            "fr": ["Pause", "Suspendre l'execution"],
            "de": ["Pausieren", "Ausfuehrung pausieren"],
            "zh": ["Zanting", "Zanting zhixing"],
        },
        "param": lambda: {},
    },
    
    # MEMORY
    "Memory.getDOMCounters": {
        "description": "Get DOM memory counters",
        "templates": {
            "en": ["How much memory is JavaScript using?", "Memory usage?", "DOM counters", "Memory stats"],
            "es": ["Cuanta memoria usa JavaScript?", "Uso de memoria?", "Contadores DOM", "Estadisticas de memoria"],
            "fr": ["Combien de memoire utilise JavaScript?", "Utilisation memoire?"],
            "de": ["Wie viel Speicher nutzt JavaScript?", "Speichernutzung?"],
            "zh": ["JavaScript shiyong duo shao neicun?", "Neicun shiyong qingkuang"],
        },
        "param": lambda: {},
    },
    
    "HeapProfiler.takeHeapSnapshot": {
        "description": "Take heap memory snapshot",
        "templates": {
            "en": ["Take heap snapshot", "Memory snapshot", "Capture heap state", "Snapshot the heap"],
            "es": ["Toma snapshot del heap", "Instantanea de memoria", "Captura estado del heap", "Snapshot del heap"],
            "fr": ["Prendre un instantane du heap", "Snapshot memoire"],
            "de": ["Heap-Snapshot erstellen", "Speicher-Snapshot"],
            "zh": ["Pai zhao dui neicun", "Neicun kuai Zhao"],
        },
        "param": lambda: {},
    },
    
    "HeapProfiler.collectGarbage": {
        "description": "Force garbage collection",
        "templates": {
            "en": ["Force garbage collection", "Run GC", "Collect garbage", "Clean up memory"],
            "es": ["Fuerza garbage collection", "Ejecuta GC", "Recoge basura", "Limpia memoria"],
            "fr": ["Forcer le garbage collection", "Executer GC"],
            "de": ["Garbage Collection erzwingen", "GC ausfuehren"],
            "zh": ["Qiangzhi laji huishou", "Zhixing GC"],
        },
        "param": lambda: {},
    },
    
    # NETWORK
    "Network.enable": {
        "description": "Enable network monitoring",
        "templates": {
            "en": ["Enable network monitoring", "Monitor network requests", "Start network tracking", "Capture network traffic"],
            "es": ["Activa monitoreo de red", "Monitorea las peticiones de red", "Inicia seguimiento de red", "Captura trafico de red"],
            "fr": ["Activer la surveillance reseau", "Surveiller les requetes"],
            "de": ["Netzwerkueberwachung aktivieren", "Netzwerk-Tracking starten"],
            "zh": ["Qiyong wangluo jiandu", "Kaiqi wangluo genzong"],
        },
        "param": lambda: {},
    },
    
    "Network.disable": {
        "description": "Disable network monitoring",
        "templates": {
            "en": ["Disable network monitoring", "Stop network tracking"],
            "es": ["Desactiva monitoreo de red", "Detener seguimiento de red"],
            "fr": ["Desactiver la surveillance reseau"],
            "de": ["Netzwerkueberwachung deaktivieren"],
            "zh": ["Ting yong wangluo jiandu"],
        },
        "param": lambda: {},
    },
    
    "Network.getAllRequests": {
        "description": "Get all network requests",
        "templates": {
            "en": ["List all requests", "Show network requests", "What requests were made?", "All HTTP requests"],
            "es": ["Lista todos los requests", "Muestra peticiones de red", "Que requests se hicieron?", "Todos los HTTP"],
            "fr": ["Lister toutes les requetes", "Afficher les requetes reseau"],
            "de": ["Alle Requests auflisten", "Netzwerkanfragen anzeigen"],
            "zh": ["Liebiao suoyou qingqiu", "Xianshi wangluo qingqiu"],
        },
        "param": lambda: {},
    },
    
    "Network.clearBrowserCache": {
        "description": "Clear browser cache",
        "templates": {
            "en": ["Clear browser cache", "Clear cache", "Delete cache", "Empty cache"],
            "es": ["Limpia el cache del navegador", "Borra cache", "Elimina cache", "Vaciar cache"],
            "fr": ["Vider le cache du navigateur", "Effacer le cache"],
            "de": ["Browser-Cache leeren", "Cache loeschen"],
            "zh": ["Qingchu liulanqi huancun", "Qingchu huancun"],
        },
        "param": lambda: {},
    },
    
    "Network.clearBrowserCookies": {
        "description": "Clear browser cookies",
        "templates": {
            "en": ["Clear cookies", "Delete cookies", "Remove cookies", "Clear browser cookies"],
            "es": ["Limpia las cookies", "Borra cookies", "Elimina cookies", "Limpia cookies del navegador"],
            "fr": ["Effacer les cookies", "Supprimer les cookies"],
            "de": ["Cookies loeschen", "Browser-Cookies entfernen"],
            "zh": ["Qingchu cookies", "Shanchu cookies"],
        },
        "param": lambda: {},
    },
    
    # PERFORMANCE
    "Profiler.enable": {
        "description": "Enable CPU profiler",
        "templates": {
            "en": ["Enable CPU profiler", "Turn on profiler", "Activate performance profiling"],
            "es": ["Activa el profiler de CPU", "Activar profiling", "Activa rendimiento"],
            "fr": ["Activer le profileur CPU", "Activer le profiling"],
            "de": ["CPU-Profiler aktivieren", "Profiling einschalten"],
            "zh": ["Qiyong CPU jianceqi", "Qidong jiance"],
        },
        "param": lambda: {},
    },
    
    "Profiler.start": {
        "description": "Start profiling",
        "templates": {
            "en": ["Start profiling", "Begin recording", "Start capturing performance", "Record performance"],
            "es": ["Comienza el profiling", "Inicia grabacion", "Comienza a capturar rendimiento", "Graba performance"],
            "fr": ["Demarrer le profiling", "Commencer l'enregistrement"],
            "de": ["Profiling starten", "Aufzeichnung beginnen"],
            "zh": ["Kaishi jiance", "Kaishi luxiang"],
        },
        "param": lambda: {},
    },
    
    "Profiler.stop": {
        "description": "Stop profiling",
        "templates": {
            "en": ["Stop profiling", "Stop recording", "End profiling", "Capture profile data"],
            "es": ["Deten el profiling", "Detener grabacion", "Termina profiling", "Captura datos de perfil"],
            "fr": ["Arreter le profiling", "Arreter l'enregistrement"],
            "de": ["Profiling stoppen", "Aufzeichnung beenden"],
            "zh": ["Ting zhi jiance", "Jieshu luxiang"],
        },
        "param": lambda: {},
    },
    
    "Performance.getMetrics": {
        "description": "Get performance metrics",
        "templates": {
            "en": ["Get performance metrics", "What are the performance metrics?", "Performance stats", "Show metrics"],
            "es": ["Dame las metricas de performance", "Cuales son las metricas?", "Estadisticas de rendimiento", "Muestra metricas"],
            "fr": ["Obtenir les metriques de performance", "Statistiques de performance"],
            "de": ["Leistungsmetriken abrufen", "Performance-Statistiken"],
            "zh": ["Huode jixiao zhishu", "Xingneng zhibiao"],
        },
        "param": lambda: {},
    },
    
    # CONSOLE
    "Log.enable": {
        "description": "Enable console monitoring",
        "templates": {
            "en": ["Enable console monitoring", "Monitor console", "Watch console logs", "Capture console output"],
            "es": ["Activa monitoreo de consola", "Monitorea la consola", "Observa logs de consola", "Captura salida de consola"],
            "fr": ["Activer la surveillance de la console", "Surveiller la console"],
            "de": ["Konsolenueberwachung aktivieren", "Console beobachten"],
            "zh": ["Qiyong Konsol jiance", "Jiance Konsol shuchu"],
        },
        "param": lambda: {},
    },
}

# Data for template filling
URLS = [
    "https://perplexity.ai",
    "https://google.com",
    "https://github.com",
    "https://twitter.com",
    "https://youtube.com",
    "https://wikipedia.org",
    "https://reddit.com",
    "https://stackoverflow.com",
]

SELECTORS = [
    "body", "div", "button", "input", "form", "a", "span", "p",
    "#main", "#app", "#container", "#header", "#footer",
    ".container", ".content", ".wrapper", ".nav",
    "[data-test]", "[role='button']", "nav", "header",
]

DIMENSIONS = [
    {"width": 375, "height": 667},   # iPhone
    {"width": 768, "height": 1024},  # iPad
    {"width": 1440, "height": 900},  # Laptop
    {"width": 1920, "height": 1080}, # Desktop
]

SCRIPTS = ["app.js", "index.js", "main.js", "bundle.js", "script.js", "vendor.js"]

ATTR_NAMES = ["disabled", "readonly", "checked", "class", "id", "data-test", "aria-label", "style"]
ATTR_VALUES = ["true", "active", "test", "enabled", "disabled", "selected"]

EXPRESSIONS = [
    "document.title",
    "window.location.href",
    "document.cookie",
    "JSON.stringify(localStorage)",
    "{x: window.scrollX, y: window.scrollY}",
    "getEventListeners(document).length",
    "document.readyState",
    "navigator.userAgent",
    "document.querySelectorAll('img').length",
    "document.querySelectorAll('[aria-label]').length",
]


def fill_template(template: str, cmd: str) -> str:
    """Fill template with random values"""
    result = template
    
    if "{url}" in result:
        result = result.replace("{url}", random.choice(URLS))
    
    if "{sel}" in result:
        result = result.replace("{sel}", random.choice(SELECTORS))
    
    if "{w}" in result and "{h}" in result:
        dim = random.choice(DIMENSIONS)
        result = result.replace("{w}", str(dim["width"])).replace("{h}", str(dim["height"]))
    
    if "{script}" in result:
        result = result.replace("{script}", random.choice(SCRIPTS))
    
    if "{line}" in result:
        result = result.replace("{line}", str(random.randint(1, 200)))
    
    if "{attr}" in result:
        result = result.replace("{attr}", random.choice(ATTR_NAMES))
    
    if "{val}" in result:
        result = result.replace("{val}", random.choice(ATTR_VALUES))
    
    if "{expr}" in result:
        result = result.replace("{expr}", random.choice(EXPRESSIONS))
    
    return result


def generate_dataset(count: int = 1000) -> List[Dict]:
    """Generate multi-language training dataset"""
    dataset = []
    example_id = 1
    
    # Flatten all commands and their templates
    all_examples = []
    
    for cmd, cmd_data in CDP_COMMANDS.items():
        description = cmd_data["description"]
        templates_by_lang = cmd_data["templates"]
        param_func = cmd_data["param"]
        
        # Collect all templates across all languages
        for lang, templates in templates_by_lang.items():
            for template in templates:
                instruction = fill_template(template, cmd)
                params = param_func()
                
                all_examples.append({
                    "instruction": instruction,
                    "language": lang,
                    "cdp_command": cmd,
                    "cdp_params": params,
                    "description": description,
                })
    
    # Generate dataset by sampling from all_examples
    for _ in range(count):
        base = random.choice(all_examples)
        
        dataset.append({
            "id": example_id,
            "instruction": base["instruction"],
            "language": base["language"],
            "category": get_category_from_command(base["cdp_command"]),
            "cdp_command": base["cdp_command"],
            "cdp_params": base["cdp_params"],
            "context": f"Using Chrome DevTools Protocol: {base['description']}",
            "response_example": f"Command {base['cdp_command']} executed successfully",
        })
        
        example_id += 1
    
    return dataset


def get_category_from_command(cmd: str) -> str:
    """Infer category from command name"""
    if cmd.startswith("Page.") or cmd.startswith("Target."):
        return "navigation"
    elif cmd.startswith("DOM."):
        return "dom"
    elif cmd.startswith("Runtime."):
        return "runtime"
    elif cmd.startswith("Debugger."):
        return "debugger"
    elif cmd.startswith("Memory.") or cmd.startswith("HeapProfiler."):
        return "memory"
    elif cmd.startswith("Network."):
        return "network"
    elif cmd.startswith("Profiler.") or cmd.startswith("Performance"):
        return "performance"
    elif cmd.startswith("Log.") or cmd.startswith("Console."):
        return "console"
    else:
        return "other"


def main():
    print("=" * 60)
    print("PARASYTE - Multi-language CDP Training Dataset")
    print("=" * 60)
    
    print("\nGenerating dataset with instructions in 5 languages...")
    dataset = generate_dataset(1000)
    print(f"Generated {len(dataset)} examples")
    
    # Language distribution
    langs = {}
    for ex in dataset:
        lang = ex["language"]
        langs[lang] = langs.get(lang, 0) + 1
    
    print("\nLanguage distribution:")
    for lang, count in sorted(langs.items(), key=lambda x: -x[1]):
        lang_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "zh": "Chinese"}
        print(f"  {lang_names.get(lang, lang)}: {count} ({count/len(dataset)*100:.1f}%)")
    
    # Category distribution
    cats = {}
    for ex in dataset:
        cat = ex["category"]
        cats[cat] = cats.get(cat, 0) + 1
    
    print("\nCategory distribution:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Save
    output_dir = "D:/Parasyte/data"
    
    with open(f"{output_dir}/cdp_training_multilang.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    with open(f"{output_dir}/cdp_training_multilang.jsonl", "w", encoding="utf-8") as f:
        for ex in dataset:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    
    print(f"\nSaved to {output_dir}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
