"""
AI Fervv IDE - AI Status Display System
Real-time visualization of AI agent activities
"""

from enum import Enum
import time

class AgentStatus(Enum):
    """Agent activity states"""
    READY = ("Agent->Gotowy ✅", "#4ec9b0")
    THINKING = ("Agent->Myśli... 🧠", "#569cd6")
    SEARCHING = ("Agent->Szuka... 🔍", "#dcdcaa")
    WRITING = ("Agent->Pisze... ✍️", "#ce9178")
    ANALYZING = ("Agent->Analizuje... 📊", "#c586c0")
    EXECUTING = ("Agent->Wykonuje... ⚡", "#4fc1ff")
    DEBUGGING = ("Agent->Debuguje... 🐛", "#f48771")
    ERROR = ("Agent->Błąd ❌", "#f48771")

class AIStatusManager:
    """Manages AI agent status display and tracking"""
    
    def __init__(self):
        self.current_status = AgentStatus.READY
        self.status_history = []
        self.start_time = None
        self.callbacks = []
    
    def set_status(self, status: AgentStatus, details=""):
        """Update current status"""
        self.current_status = status
        self.start_time = time.time()
        
        # Add to history
        self.status_history.append({
            "status": status,
            "details": details,
            "timestamp": self.start_time
        })
        
        # Notify listeners
        self._notify_callbacks(status, details)
    
    def get_status(self):
        """Get current status"""
        return self.current_status
    
    def get_status_text(self):
        """Get status display text"""
        return self.current_status.value[0]
    
    def get_status_color(self):
        """Get status color"""
        return self.current_status.value[1]
    
    def get_elapsed_time(self):
        """Get time since status change"""
        if self.start_time:
            return time.time() - self.start_time
        return 0
    
    def register_callback(self, callback):
        """Register status change callback"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, status, details):
        """Notify all registered callbacks"""
        for callback in self.callbacks:
            try:
                callback(status, details)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def get_history(self, limit=10):
        """Get recent status history"""
        return self.status_history[-limit:]
    
    def clear_history(self):
        """Clear status history"""
        self.status_history = []

# Global status manager instance
status_manager = AIStatusManager()
