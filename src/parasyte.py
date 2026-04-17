#!/usr/bin/env python3
"""
PARASYTE - LFM Control for Chrome DevTools

Prototype que demuestra el concepto de un LFM controlando DevTools via CDP.
"""

import asyncio
import json
import os
import sys
from typing import Any, Optional
from dataclasses import dataclass

# Load Perplexity cookies for authentication (future use)
COOKIES_PATH = os.path.expanduser("~").replace("\\", "/") + "/perplexity_cookies.json"

@dataclass
class CDPMessage:
    """CDP message structure"""
    id: int
    method: str
    params: dict = None
    session_id: str = None

class ParasyteCDP:
    """Chrome DevTools Protocol connector"""
    
    def __init__(self, ws_url: str = "ws://localhost:9222"):
        self.ws_url = ws_url
        self.ws = None
        self.msg_id = 0
        self.pending: dict[int, asyncio.Future] = {}
        
    async def connect(self):
        """Connect to Chrome via WebSocket"""
        import websockets
        
        try:
            self.ws = await websockets.connect(self.ws_url)
            print(f"[PARASYTE] Connected to {self.ws_url}")
            
            # Start listening for events
            asyncio.create_task(self._listen())
            return True
            
        except Exception as e:
            print(f"[PARASYTE] Connection failed: {e}")
            print(f"[PARASYTE] Ensure Chrome is running with: --remote-debugging-port=9222")
            return False
    
    async def _listen(self):
        """Listen for CDP events and responses"""
        async for msg in self.ws:
            data = json.loads(msg)
            
            if "id" in data:
                # Response to our request
                msg_id = data["id"]
                if msg_id in self.pending:
                    future = self.pending.pop(msg_id)
                    if "result" in data:
                        future.set_result(data["result"])
                    else:
                        future.set_exception(Exception(data.get("error", {}).get("message", "Unknown error")))
            else:
                # Event
                self._handle_event(data.get("method"), data.get("params", {}))
    
    def _handle_event(self, method: str, params: dict):
        """Handle incoming CDP events"""
        # Console messages
        if method == "Runtime.consoleAPICalled":
            msg_type = params.get("type", "log")
            args = [a.get("value", "") for a in params.get("args", [])]
            print(f"[CONSOLE:{msg_type}] {' '.join(args)}")
        
        # Page events
        elif method == "Page.loadEventFired":
            print(f"[PAGE] Load event: {params.get('timestamp')}")
        
        elif method == "Page.frameStartedLoading":
            print(f"[PAGE] Frame loading: {params.get('frameId', '')[:20]}...")
        
        # Exceptions
        elif method == "Runtime.exceptionThrown":
            print(f"[EXCEPTION] {params.get('exceptionDetails', {}).get('exception', {}).get('description', '')}")
    
    async def send(self, method: str, params: dict = None) -> Any:
        """Send CDP command and wait for response"""
        if not self.ws:
            raise Exception("Not connected")
        
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method}
        if params:
            msg["params"] = params
        
        future = asyncio.get_event_loop().create_future()
        self.pending[self.msg_id] = future
        
        await self.ws.send(json.dumps(msg))
        return await future
    
    async def close(self):
        """Close connection"""
        if self.ws:
            await self.ws.close()

class ParasyteLFM:
    """
    LFM Bridge - Simplified prototype
    
    This is a placeholder. Real implementation would use:
    - llama.cpp bindings for LFM 2.5
    - GGUF model loading
    - Proper token generation
    
    For now, demonstrates the interface.
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model = None
        self.loaded = False
        
    def load(self):
        """Load LFM model"""
        # In production: load GGUF via llama.cpp
        print(f"[LFM] Loading model from {self.model_path or 'default'}")
        print(f"[LFM] Note: This is a placeholder. Real implementation needs llama.cpp bindings")
        self.loaded = True
        
    async def query(self, prompt: str) -> str:
        """Generate response to prompt"""
        if not self.loaded:
            self.load()
        
        # Simulate LFM response based on intent
        prompt_lower = prompt.lower()
        
        if "memory" in prompt_lower or "leak" in prompt_lower:
            return self._handle_memory_intent(prompt)
        elif "network" in prompt_lower or "request" in prompt_lower:
            return self._handle_network_intent(prompt)
        elif "dom" in prompt_lower or "element" in prompt_lower:
            return self._handle_dom_intent(prompt)
        elif "debug" in prompt_lower or "error" in prompt_lower:
            return self._handle_debug_intent(prompt)
        else:
            return f"Parasyte understands: {prompt}\n\nSimulated response for general query."
    
    def _handle_memory_intent(self, prompt: str) -> str:
        """Handle memory-related intents"""
        return """
Parasyte Memory Analysis:
1. Execute Memory.getDOMCounters
2. Take HeapSnapshot (before)
3. Perform actions
4. Take HeapSnapshot (after)
5. Compare for leaks

CDP Commands to execute:
- Memory.getDOMCounters
- HeapProfiler.takeHeapSnapshot
- HeapProfiler.takeHeapSnapshot (second)
- HeapProfiler.compareHeapSnapshots
"""
    
    def _handle_network_intent(self, prompt: str) -> str:
        """Handle network-related intents"""
        return """
Parasyte Network Analysis:
1. Enable Network tracking
2. Execute page actions
3. Capture all requests
4. Analyze timing and headers

CDP Commands to execute:
- Network.enable
- Network.setRequestInterception
- Network.getRequests
- Network.getResponseBody
"""
    
    def _handle_dom_intent(self, prompt: str) -> str:
        """Handle DOM-related intents"""
        return """
Parasyte DOM Analysis:
1. Get document structure
2. Query specific elements
3. Analyze attributes
4. Check for accessibility

CDP Commands to execute:
- DOM.getDocument
- DOM.querySelector
- DOM.getBoxModel
- Runtime.evaluate
"""
    
    def _handle_debug_intent(self, prompt: str) -> str:
        """Handle debug-related intents"""
        return """
Parasyte Debug Mode:
1. Enable debugger
2. Set breakpoint at location
3. Execute step-by-step
4. Capture variable state

CDP Commands to execute:
- Debugger.enable
- Debugger.setBreakpoint
- Debugger.stepOver
- Runtime.getProperties
"""

class ParasyteAgent:
    """
    Main Parasyte Agent
    
    Orchestrates LFM + CDP for autonomous browser control.
    """
    
    def __init__(self, cdp_url: str = "ws://localhost:9222", lfm_path: str = None):
        self.cdp = ParasyteCDP(cdp_url)
        self.lfm = ParasyteLFM(lfm_path)
        self.tab_id: Optional[str] = None
        
    async def initialize(self):
        """Initialize connections"""
        # Connect to Chrome
        if not await self.cdp.connect():
            return False
        
        # List available targets (tabs)
        result = await self.cdp.send("Target.getTargets")
        targets = result.get("targetInfos", [])
        
        if not targets:
            print("[PARASYTE] No tabs found")
            return False
        
        # Use first tab or create new one
        self.tab_id = targets[0].get("targetId")
        print(f"[PARASYTE] Using tab: {self.tab_id}")
        
        # Attach to target
        attach_result = await self.cdp.send("Target.attachToTarget", {
            "targetId": self.tab_id,
            "flatten": True
        })
        self.session_id = attach_result.get("sessionId")
        print(f"[PARASYTE] Session ID: {self.session_id}")
        
        # Load LFM
        self.lfm.load()
        
        return True
    
    async def execute_task(self, task: str):
        """Execute a task given in natural language"""
        print(f"\n[PARASYTE] Task: {task}")
        print("-" * 50)
        
        # Get LFM interpretation
        plan = await self.lfm.query(task)
        print(f"[LFM PLAN]\n{plan}")
        print("-" * 50)
        
        # Execute CDP commands based on plan
        if "memory" in task.lower() or "heap" in task.lower():
            await self._memory_operation(task)
        elif "network" in task.lower() or "request" in task.lower():
            await self._network_operation(task)
        elif "dom" in task.lower():
            await self._dom_operation(task)
        else:
            await self._general_operation(task)
        
        print("-" * 50)
    
    async def _memory_operation(self, task: str):
        """Execute memory-related CDP commands"""
        print("\n[EXEC] Memory operation...")
        
        try:
            # Get DOM counters
            counters = await self.cdp.send("Memory.getDOMCounters")
            print(f"[RESULT] DOM Counters: {counters}")
            
            # Take heap snapshot
            await self.cdp.send("HeapProfiler.takeHeapSnapshot")
            print("[RESULT] Heap snapshot taken")
            
        except Exception as e:
            print(f"[ERROR] {e}")
    
    async def _network_operation(self, task: str):
        """Execute network-related CDP commands"""
        print("\n[EXEC] Network operation...")
        
        try:
            # Enable network tracking
            await self.cdp.send("Network.enable")
            print("[RESULT] Network tracking enabled")
            
            # Get all requests
            result = await self.cdp.send("Network.getAllRequests")
            requests = result.get("requests", [])
            print(f"[RESULT] Found {len(requests)} requests")
            
        except Exception as e:
            print(f"[ERROR] {e}")
    
    async def _dom_operation(self, task: str):
        """Execute DOM-related CDP commands"""
        print("\n[EXEC] DOM operation...")
        
        try:
            # Get document
            doc = await self.cdp.send("DOM.getDocument")
            print(f"[RESULT] Document retrieved, root node: {doc.get('root', {}).get('nodeId')}")
            
            # Get box model for body
            body_result = await self.cdp.send("DOM.getDocument")
            node_id = body_result.get("root", {}).get("nodeId", 1)
            print(f"[RESULT] Root node ID: {node_id}")
            
        except Exception as e:
            print(f"[ERROR] {e}")
    
    async def _general_operation(self, task: str):
        """Execute general CDP commands"""
        print("\n[EXEC] General operation...")
        
        try:
            # Evaluate some JS
            result = await self.cdp.send("Runtime.evaluate", {
                "expression": "document.title",
                "returnByValue": True
            })
            print(f"[RESULT] Page title: {result.get('result', {}).get('value')}")
            
        except Exception as e:
            print(f"[ERROR] {e}")
    
    async def close(self):
        """Clean up connections"""
        await self.cdp.close()
        print("[PARASYTE] Disconnected")

async def main():
    """Main entry point"""
    print("=" * 60)
    print("PARASYTE - LFM Parasiting Chrome DevTools")
    print("=" * 60)
    
    # Initialize Parasyte
    parasyte = ParasyteAgent()
    
    if not await parasyte.initialize():
        print("\n[SETUP] To enable Chrome debugging:")
        print("  1. Close all Chrome windows")
        print("  2. Run: chrome --remote-debugging-port=9222")
        print("  3. Open Perplexity and log in")
        print("  4. Run this script again")
        return
    
    print("\n[PARASYTE] Ready! Examples:")
    print("  - 'check for memory leaks'")
    print("  - 'analyze network requests'")
    print("  - 'inspect the DOM'")
    print("  - 'debug JavaScript errors'")
    print("  - 'quit' to exit\n")
    
    # Interactive loop
    while True:
        try:
            task = input("parasyte> ").strip()
            
            if not task:
                continue
            
            if task.lower() in ["quit", "exit", "q"]:
                break
            
            await parasyte.execute_task(task)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[ERROR] {e}")
    
    await parasyte.close()
    print("\n[PARASYTE] Goodbye!")

if __name__ == "__main__":
    # Check for websockets
    try:
        import websockets
    except ImportError:
        print("Installing websockets...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
        import websockets
    
    asyncio.run(main())
