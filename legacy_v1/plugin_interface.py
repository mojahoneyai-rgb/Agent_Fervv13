"""
Plugin Interface for AI Fervv Agent
"""

from abc import ABC, abstractmethod

class AgentPlugin(ABC):
    """Base class for all agent plugins"""
    
    @property
    @abstractmethod
    def name(self):
        """Plugin name"""
        pass
        
    @property
    @abstractmethod
    def description(self):
        """Plugin description"""
        pass
        
    @abstractmethod
    def initialize(self, agent_core):
        """Initialize plugin with agent core"""
        pass
        
    @abstractmethod
    def execute(self, command, **kwargs):
        """Execute plugin command"""
        pass
