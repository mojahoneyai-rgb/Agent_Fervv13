"""
AI Fervv IDE - Clipboard Manager
Advanced clipboard operations with history
"""

import pyperclip

class ClipboardManager:
    """Manages clipboard operations with history"""
    
    def __init__(self, history_size=10):
        self.history = []
        self.history_size = history_size
    
    def copy(self, text):
        """Copy text to clipboard"""
        if text:
            pyperclip.copy(text)
            self._add_to_history(text)
            return True
        return False
    
    def cut(self, text):
        """Cut text (copy and return True for deletion)"""
        if text:
            pyperclip.copy(text)
            self._add_to_history(text)
            return True
        return False
    
    def paste(self):
        """Get text from clipboard"""
        try:
            return pyperclip.paste()
        except:
            return ""
    
    def _add_to_history(self, text):
        """Add to clipboard history"""
        # Remove duplicates
        if text in self.history:
            self.history.remove(text)
        
        # Add to front
        self.history.insert(0, text)
        
        # Limit size
        if len(self.history) > self.history_size:
            self.history = self.history[:self.history_size]
    
    def get_history(self):
        """Get clipboard history"""
        return self.history.copy()
    
    def clear_history(self):
        """Clear clipboard history"""
        self.history = []

class UndoRedoManager:
    """Manages undo/redo operations for text editors"""
    
    def __init__(self, max_stack_size=100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_stack_size = max_stack_size
        self.current_state = ""
    
    def save_state(self, state):
        """Save current state for undo"""
        if state != self.current_state:
            self.undo_stack.append(self.current_state)
            self.redo_stack = []  # Clear redo on new action
            
            # Limit stack size
            if len(self.undo_stack) > self.max_stack_size:
                self.undo_stack.pop(0)
            
            self.current_state = state
    
    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(self.current_state)
            self.current_state = self.undo_stack.pop()
            return self.current_state
        return None
    
    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.current_state)
            self.current_state = self.redo_stack.pop()
            return self.current_state
        return None
    
    def can_undo(self):
        """Check if undo is available"""
        return len(self.undo_stack) > 0
    
    def can_redo(self):
        """Check if redo is available"""
        return len(self.redo_stack) > 0
    
    def clear(self):
        """Clear undo/redo stacks"""
        self.undo_stack = []
        self.redo_stack = []
        self.current_state = ""
