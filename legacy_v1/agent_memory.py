"""
Episodic Memory System (EMS) for AI Fervv Agent
Handles long-term memory storage using compressed JSON.
"""

import json
import gzip
import os
import time
from datetime import datetime

class AgentMemory:
    def __init__(self, memory_file="agent_memory.json.gz"):
        self.memory_file = memory_file
        self.short_term_memory = []
        self.long_term_memory = self.load_memory()
        
    def load_memory(self):
        """Load long-term memory from compressed file"""
        if os.path.exists(self.memory_file):
            try:
                with gzip.open(self.memory_file, 'rt', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return {"episodes": [], "facts": {}, "project_stats": {}}
        return {"episodes": [], "facts": {}, "project_stats": {}}
    
    def save_memory(self):
        """Save memory to compressed file"""
        try:
            with gzip.open(self.memory_file, 'wt', encoding='utf-8') as f:
                json.dump(self.long_term_memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
            
    def remember(self, role, content, context=None):
        """Add a new memory trace"""
        timestamp = datetime.now().isoformat()
        trace = {
            "timestamp": timestamp,
            "role": role,
            "content": content,
            "context": context or {}
        }
        self.short_term_memory.append(trace)
        
        # Add to episodes if it's significant (simplified logic)
        if len(content) > 50 or role == "user":
            self.long_term_memory["episodes"].append(trace)
            
            # Keep episodes limited
            if len(self.long_term_memory["episodes"]) > 1000:
                self.long_term_memory["episodes"] = self.long_term_memory["episodes"][-1000:]
                
            self.save_memory()
            
    def recall(self, query=None, limit=5):
        """Recall relevant memories"""
        # Simple recent memory recall for now
        # Future: Implement vector similarity search
        return self.long_term_memory["episodes"][-limit:]
    
    def learn_fact(self, key, value):
        """Store a specific fact"""
        self.long_term_memory["facts"][key] = value
        self.save_memory()
        
    def get_fact(self, key):
        """Retrieve a specific fact"""
        return self.long_term_memory["facts"].get(key)
        
    def update_project_stats(self, project_name, stats):
        """Update statistics for a project"""
        self.long_term_memory["project_stats"][project_name] = stats
        self.save_memory()

# Global memory instance
agent_memory = AgentMemory()
