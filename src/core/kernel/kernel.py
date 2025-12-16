"""
Micro-Kernel Core
Manages the lifecycle of the IDE.
"""
import importlib
import inspect
from src.core.interfaces.extension import IExtension
from src.core.event_bus import global_event_bus

class Kernel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Kernel, cls).__new__(cls)
            cls._instance.extensions = {}
            cls._instance.services = {}
            # Default logger is print
            cls._instance.log = print
            print("🌌 Galactic Kernel Initialized")
        return cls._instance

    def load_extension(self, module_path):
        """Dynamically loads an extension module."""
        try:
            module = importlib.import_module(module_path)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, IExtension) and obj is not IExtension:
                    extension = obj()
                    extension.on_load(self)
                    self.extensions[name] = extension
                    print(f"Loaded Extension: {name}")
                    return True
        except Exception as e:
            print(f"Failed to load extension {module_path}: {e}")
            return False

    def register_service(self, interface, instance):
        """Registers a core service available to all extensions."""
        self.services[interface] = instance
        global_event_bus.publish("service_registered", interface)

    def get_service(self, interface):
        """Retrieves a registered service."""
        return self.services.get(interface)

    def shutdown(self):
        """Gracefully unloads all extensions."""
        for name, ext in self.extensions.items():
            try:
                ext.on_unload()
            except Exception as e:
                print(f"Error unloading {name}: {e}")
        self.extensions.clear()

# Global Kernel Accessor
kernel = Kernel()
