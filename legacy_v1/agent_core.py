"""
Agent Core Architecture for AI Fervv
Handles the multi-core "consciousness" of the agent.
"""

from agent_memory import agent_memory
from plugin_interface import AgentPlugin
import importlib
import os
import sys

class AgentCore:
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.memory = agent_memory
        self.plugins = {}
        self.cores = {
            "LOGIC": LogicCore(self),
            "CREATIVE": CreativeCore(self),
            "CODING": CodingCore(self)
        }
        self.active_core = "LOGIC"
        
        # Load plugins
        self.load_plugins()
        
    def load_plugins(self):
        """Discover and load plugins"""
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)
            
        sys.path.append(os.path.dirname(__file__))
        
        # In a real scenario, we would iterate files in plugins/
        # For now, we initialize an empty registry
        print("Plugins system initialized")

    def switch_core(self, core_name):
        """Switch active consciousness core"""
        if core_name in self.cores:
            self.active_core = core_name
            return True
        return False
        
    def process(self, user_input, context=None):
        """Process input through the active core"""
        # 1. Update Memory
        self.memory.remember("user", user_input, context)
        
        # 2. Select Core based on intent (simplified)
        if "code" in user_input.lower() or "function" in user_input.lower() or "def " in user_input:
            self.switch_core("CODING")
        elif "design" in user_input.lower() or "idea" in user_input.lower():
            self.switch_core("CREATIVE")
        else:
            self.switch_core("LOGIC")
            
        # 3. Core Processing
        core = self.cores[self.active_core]
        response = core.think(user_input, context)
        
        # 4. Save Response to Memory
        self.memory.remember("assistant", response, {"core": self.active_core})
        
        return response

class BaseCore:
    def __init__(self, brain):
        self.brain = brain
        
    def think(self, input_text, context):
        raise NotImplementedError

class LogicCore(BaseCore):
    """Handles general reasoning and conversation"""
    def think(self, input_text, context):
        # Enhance prompt with memory
        memories = self.brain.memory.recall(limit=3)
        memory_context = "\n".join([f"{m['role']}: {m['content']}" for m in memories])
        
        system_prompt = f"""You are the LOGIC CORE of AI Fervv.
Analysis and reasoning are your strengths.
        
Recent Memory:
{memory_context}
"""
        # Delegate to main agent for actual generation settings
        return self.brain.agent.generate_with_core(input_text, system_prompt)

class CreativeCore(BaseCore):
    """Handles design, ideas, and creative writing"""
    def think(self, input_text, context):
        system_prompt = """You are the CREATIVE CORE of AI Fervv.
Imagination, design, and UI/UX are your strengths.
Thinking outside the box is your primary directive.
"""
        return self.brain.agent.generate_with_core(input_text, system_prompt)

class CodingCore(BaseCore):
    """Handles implementation and technical details"""
    def think(self, input_text, context):
        system_prompt = """You are the CODING CORE of AI Fervv.
Precision, efficiency, and clean architecture are your strengths.
Always output production-ready code.
"""
        return self.brain.agent.generate_with_core(input_text, system_prompt)

    def analyze_error(self, error_text):
        """Analyze traceback and suggest fix"""
        prompt = f"""ANALYSIS REQUIRED:
The user encountered the following error:
```
{error_text}
```
Explain the cause briefly and provide the corrected code or command to fix it. 
If it requires installing a package, output: [[EXEC: pip install ...]]
If it requires code changes, output the full file content inside [[CREATE: filename]]...[[/CREATE]] if possible.
"""
        return self.brain.agent.generate_with_core(prompt, "You are the DEBUGGING SYSTEM. Fix the code.")
