"""
Extension Interface
All components in the Galactic Architecture must implement this.
"""
from abc import ABC, abstractmethod

class IExtension(ABC):
    @abstractmethod
    def on_load(self, kernel):
        """Called when the extension is loaded."""
        pass

    @abstractmethod
    def on_unload(self):
        """Called when the extension is unloaded."""
        pass
