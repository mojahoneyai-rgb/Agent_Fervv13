"""
Memory Service
Stores and retrieves knowledge for the AI Agent using a simple persistent JSON store.
Future upgrades: Vector Database implementation.
"""
import json
import os
from datetime import datetime

class MemoryService:
    def __init__(self, storage_file="ai_memory.json"):
        self.storage_file = storage_file
        self.memory = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except Exception:
                self.memory = []

    def _save_memory(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

    def remember(self, query, answer, source="unknown"):
        """Store a new piece of information."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer": answer,
            "source": source
        }
        self.memory.append(entry)
        self._save_memory()

    def search(self, query):
        """Simple keyword search in memory."""
        results = []
        query_terms = query.lower().split()
        for entry in self.memory:
            content = (entry["query"] + " " + entry["answer"]).lower()
            if any(term in content for term in query_terms):
                results.append(entry)
        return results

    def get_context_string(self, query, limit=3):
        """Get formatted context for LLM prompt."""
        matches = self.search(query)
        # Simple ranking: most recent first
        matches.sort(key=lambda x: x["timestamp"], reverse=True)
        
        if not matches:
            return ""
            
        context = "[[MEMORY_CONTEXT]]\n"
        for i, m in enumerate(matches[:limit]):
            context += f"Fact {i+1}: {m['answer']} (Source: {m['source']})\n"
        context += "[[/MEMORY_CONTEXT]]\n"
        return context
