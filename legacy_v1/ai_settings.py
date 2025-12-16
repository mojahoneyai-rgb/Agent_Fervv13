"""
AI Provider Settings Manager
Handles OpenAI and Google Gemini API configurations
"""

import json
import os

class AISettings:
    """Manage AI provider settings"""
    
    def __init__(self, settings_file="ai_settings.json"):
        self.settings_file = settings_file
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default settings
        return {
            "provider": "openai",  # or "gemini"
            "openai_key": "",
            "gemini_key": "",
            "model": "gpt-4o-mini"
        }
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_provider(self):
        """Get current AI provider"""
        return self.settings.get("provider", "openai")
    
    def set_provider(self, provider):
        """Set AI provider (openai or gemini)"""
        if provider in ["openai", "gemini"]:
            self.settings["provider"] = provider
            self.save_settings()
            return True
        return False
    
    def get_api_key(self, provider=None):
        """Get API key for provider"""
        if provider is None:
            provider = self.get_provider()
        
        key = self.settings.get(f"{provider}_key", "")
        
        # Fallback to environment variable
        if not key:
            if provider == "openai":
                key = os.environ.get("OPENAI_API_KEY", "")
            elif provider == "gemini":
                key = os.environ.get("GOOGLE_API_KEY", "")
        
        return key
    
    def set_api_key(self, provider, key):
        """Set API key for provider"""
        if provider in ["openai", "gemini"]:
            self.settings[f"{provider}_key"] = key
            self.save_settings()
            return True
        return False
    
    def get_model(self, provider=None):
        """Get model for specific provider"""
        if provider is None:
            provider = self.get_provider()
            
        if provider == "openai":
            return self.settings.get("openai_model", "gpt-4o-mini")
        elif provider == "gemini":
            return self.settings.get("gemini_model", "gemini-pro")
        return "gpt-4o-mini"
    
    def set_model(self, provider, model):
        """Set model for provider"""
        if provider in ["openai", "gemini"]:
            self.settings[f"{provider}_model"] = model
            self.save_settings()

# Global settings instance
ai_settings = AISettings()
