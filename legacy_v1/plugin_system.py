"""
AI Fervv IDE - Plugin System
Extensibility system for custom plugins
"""

import os
import json
import importlib.util

class Plugin:
    """Base plugin class"""
    
    def __init__(self, ide_instance):
        self.ide = ide_instance
        self.name = "BasePlugin"
        self.version = "1.0"
        self.description = "Base plugin"
    
    def activate(self):
        """Called when plugin is activated"""
        pass
    
    def deactivate(self):
        """Called when plugin is deactivated"""
        pass
    
    def on_file_open(self, file_path):
        """Called when a file is opened"""
        pass
    
    def on_file_save(self, file_path):
        """Called when a file is saved"""
        pass

class PluginManager:
    """Manages IDE plugins"""
    
    def __init__(self, ide_instance):
        self.ide = ide_instance
        self.plugins = {}  # name -> plugin instance
        self.active_plugins = set()
        self.plugins_dir = "plugins"
        
        # Create plugins directory
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
    
    def discover_plugins(self):
        """Discover available plugins"""
        discovered = []
        
        if not os.path.exists(self.plugins_dir):
            return discovered
        
        for item in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, item)
            
            # Check for plugin.json manifest
            manifest_path = os.path.join(plugin_path, "plugin.json")
            if os.path.isdir(plugin_path) and os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    discovered.append({
                        "name": manifest.get("name", item),
                        "version": manifest.get("version", "1.0"),
                        "description": manifest.get("description", ""),
                        "main": manifest.get("main", "plugin.py"),
                        "path": plugin_path
                    })
                except Exception as e:
                    print(f"Error loading plugin {item}: {e}")
        
        return discovered
    
    def load_plugin(self, plugin_info):
        """Load a plugin"""
        try:
            main_file = os.path.join(plugin_info["path"], plugin_info["main"])
            
            if not os.path.exists(main_file):
                return False
            
            # Load module
            spec = importlib.util.spec_from_file_location(
                plugin_info["name"], main_file
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin class (should inherit from Plugin)
            if hasattr(module, "IDEPlugin"):
                plugin_instance = module.IDEPlugin(self.ide)
                self.plugins[plugin_info["name"]] = plugin_instance
                return True
            
        except Exception as e:
            print(f"Error loading plugin {plugin_info['name']}: {e}")
        
        return False
    
    def activate_plugin(self, plugin_name):
        """Activate a plugin"""
        if plugin_name in self.plugins and plugin_name not in self.active_plugins:
            try:
                self.plugins[plugin_name].activate()
                self.active_plugins.add(plugin_name)
                return True
            except Exception as e:
                print(f"Error activating plugin {plugin_name}: {e}")
        return False
    
    def deactivate_plugin(self, plugin_name):
        """Deactivate a plugin"""
        if plugin_name in self.active_plugins:
            try:
                self.plugins[plugin_name].deactivate()
                self.active_plugins.remove(plugin_name)
                return True
            except Exception as e:
                print(f"Error deactivating plugin {plugin_name}: {e}")
        return False
    
    def trigger_event(self, event_name, *args, **kwargs):
        """Trigger event on all active plugins"""
        for plugin_name in self.active_plugins:
            plugin = self.plugins[plugin_name]
            if hasattr(plugin, event_name):
                try:
                    getattr(plugin, event_name)(*args, **kwargs)
                except Exception as e:
                    print(f"Plugin {plugin_name} event error: {e}")

# Built-in plugins

class PrettierPlugin(Plugin):
    """Code formatting plugin"""
    
    def __init__(self, ide_instance):
        super().__init__(ide_instance)
        self.name = "Prettier"
        self.version = "1.0"
        self.description = "Code formatting"
    
    def activate(self):
        print("Prettier plugin activated")
    
    def format_code(self, code, language):
        """Format code (basic implementation)"""
        # In real implementation, would use prettier or similar
        return code

class LiveServerPlugin(Plugin):
    """Live preview server plugin"""
    
    def __init__(self, ide_instance):
        super().__init__(ide_instance)
        self.name = "Live Server"
        self.version = "1.0"
        self.description = "Live HTML preview"
        self.server = None
    
    def activate(self):
        print("Live Server plugin activated")
    
    def start_server(self, port=5500):
        """Start live server"""
        # In real implementation, would start HTTP server
        print(f"Live server would start on port {port}")
