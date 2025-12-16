"""
AI Fervv IDE - Streaming AI & Enhanced Context
Real-time streaming responses with project awareness
"""

import os
import json
from pathlib import Path

class ProjectContext:
    """Enhanced context manager for project understanding"""
    
    def __init__(self, project_root=None):
        self.project_root = project_root
        self.file_cache = {}
        self.structure = {}
        self.dependencies = []
        
    def analyze_project(self):
        """Analyze project structure"""
        if not self.project_root or not os.path.exists(self.project_root):
            return
        
        self.structure = self._build_tree(self.project_root)
        self.dependencies = self._find_dependencies()
    
    def _build_tree(self, path, max_depth=3, current_depth=0):
        """Build project tree"""
        if current_depth > max_depth:
            return {}
        
        tree = {}
        try:
            for item in os.listdir(path):
                if item.startswith('.'):
                    continue
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    tree[item] = self._build_tree(full_path, max_depth, current_depth + 1)
                else:
                    tree[item] = "file"
        except:
            pass
        return tree
    
    def _find_dependencies(self):
        """Find project dependencies"""
        deps = []
        
        # Check requirements.txt
        req_file = os.path.join(self.project_root, "requirements.txt")
        if os.path.exists(req_file):
            try:
                with open(req_file, 'r') as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except:
                pass
        
        # Check package.json
        pkg_file = os.path.join(self.project_root, "package.json")
        if os.path.exists(pkg_file):
            try:
                with open(pkg_file, 'r') as f:
                    pkg = json.load(f)
                    deps.extend(pkg.get('dependencies', {}).keys())
            except:
                pass
        
        return deps
    
    def get_file_content(self, filepath):
        """Get cached or fresh file content"""
        if filepath in self.file_cache:
            return self.file_cache[filepath]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.file_cache[filepath] = content
                return content
        except:
            return None
    
    def get_context_summary(self):
        """Get project context summary"""
        summary = {
            "project_root": self.project_root,
            "file_count": self._count_files(self.structure),
            "dependencies": len(self.dependencies),
            "structure": self._structure_summary(self.structure)
        }
        return summary
    
    def _count_files(self, tree):
        """Count files in tree"""
        count = 0
        for key, value in tree.items():
            if value == "file":
                count += 1
            elif isinstance(value, dict):
                count += self._count_files(value)
        return count
    
    def _structure_summary(self, tree, prefix=""):
        """Get structure as string"""
        lines = []
        for key, value in sorted(tree.items())[:10]:  # Limit to 10 items
            if value == "file":
                lines.append(f"{prefix}📄 {key}")
            elif isinstance(value, dict):
                lines.append(f"{prefix}📁 {key}/")
        return "\n".join(lines)

class StreamingAI:
    """Streaming AI response handler"""
    
    def __init__(self, api_client, context_manager):
        self.api_client = api_client
        self.context = context_manager
        self.is_streaming = False
        self.current_response = ""
    
    async def stream_response(self, prompt, callback=None):
        """Stream AI response token by token"""
        self.is_streaming = True
        self.current_response = ""
        
        try:
            # Add context to prompt
            context_info = self._build_context_prompt()
            full_prompt = f"{context_info}\n\nUser: {prompt}"
            
            # Simulate streaming (in real impl would use API streaming)
            # For now, chunk the response
            response = await self._get_ai_response(full_prompt)
            
            for i in range(0, len(response), 10):
                if not self.is_streaming:
                    break
                    
                chunk = response[i:i+10]
                self.current_response += chunk
                
                if callback:
                    callback(chunk, self.current_response)
                
                # Small delay to simulate streaming  
                await self._sleep(0.05)
            
        except Exception as e:
            if callback:
                callback("", f"Error: {str(e)}")
        finally:
            self.is_streaming = False
    
    def cancel_streaming(self):
        """Cancel current stream"""
        self.is_streaming = False
    
    def _build_context_prompt(self):
        """Build context for AI"""
        if not self.context.project_root:
            return ""
        
        ctx = self.context.get_context_summary()
        return f"""Project Context:
- Root: {ctx['project_root']}
- Files: {ctx['file_count']}
- Dependencies: {ctx['dependencies']}
"""
    
    async def _get_ai_response(self, prompt):
        """Get AI response"""
        # This would use the actual API in real implementation
        # For now, return a simulated response
        return "This is a simulated streaming response. In real implementation, this would come from the AI API with actual streaming."
    
    async def _sleep(self, seconds):
        """Async sleep"""
        import asyncio
        await asyncio.sleep(seconds)
