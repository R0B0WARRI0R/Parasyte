#!/usr/bin/env python3
"""
PARASYTE - Prototype Demo

Verifies that LFM can control DevTools via CDP.
Run from D:\Parasyte\src\
"""

from playwright.sync_api import sync_playwright

class ParasyteDemo:
    def __init__(self):
        self.browser = None
        self.page = None
        self.cdp = None
        
    def connect(self):
        """Connect to Chrome via CDP"""
        self.browser = sync_playwright().start().chromium.connect_over_cdp('http://localhost:9222')
        context = self.browser.contexts[0]
        
        # Find Perplexity page
        for page in context.pages:
            if 'perplexity' in page.url.lower():
                self.page = page
                break
        
        if not self.page:
            self.page = context.pages[0]
        
        self.cdp = context.new_cdp_session(self.page)
        self.cdp.send('Runtime.enable')
        self.cdp.send('Log.enable')
        
        print(f"[PARASYTE] Connected to: {self.page.url[:60]}...")
    
    def get_page_info(self):
        """Get basic page info"""
        title = self.cdp.send('Runtime.evaluate', {
            'expression': 'document.title',
            'returnByValue': True
        })['result']['value']
        return title
    
    def check_memory(self):
        """Check memory usage"""
        return self.cdp.send('Memory.getDOMCounters')
    
    def analyze_dom(self):
        """Analyze DOM structure"""
        doc = self.cdp.send('DOM.getDocument')
        root_id = doc['root']['nodeId']
        
        elements = self.cdp.send('Runtime.evaluate', {
            'expression': 'document.querySelectorAll("*").length',
            'returnByValue': True
        })['result']['value']
        
        return {
            'root_node': root_id,
            'total_elements': elements
        }
    
    def detect_frameworks(self):
        """Detect JS frameworks"""
        frameworks = []
        
        # React
        react = self.cdp.send('Runtime.evaluate', {
            'expression': 'typeof window.__REACT_DEVTOOLS_GLOBAL_HOOK__',
            'returnByValue': True
        })['result']['value']
        if react != 'undefined':
            frameworks.append('React')
        
        # Vue
        vue = self.cdp.send('Runtime.evaluate', {
            'expression': 'typeof window.__VUE_DEVTOOLS_GLOBAL_HOOK__',
            'returnByValue': True
        })['result']['value']
        if vue != 'undefined':
            frameworks.append('Vue')
        
        # Angular
        ng = self.cdp.send('Runtime.evaluate', {
            'expression': 'typeof window.ng',
            'returnByValue': True
        })['result']['value']
        if ng != 'undefined':
            frameworks.append('Angular')
        
        return frameworks

    def run(self):
        """Run demo"""
        print("=" * 60)
        print("PARASYTE - LFM Parasiting Chrome DevTools")
        print("=" * 60)
        
        self.connect()
        
        print(f"\nPage Title: {self.get_page_info()}")
        print(f"Memory: {self.check_memory()}")
        
        dom = self.analyze_dom()
        print(f"DOM: {dom['total_elements']} elements (root node {dom['root_node']})")
        
        fw = self.detect_frameworks()
        print(f"Frameworks detected: {fw or 'None'}")
        
        print("\n" + "=" * 60)
        print("Concept verified: LFM CAN control DevTools via CDP")
        print("=" * 60)

if __name__ == "__main__":
    demo = ParasyteDemo()
    demo.run()
