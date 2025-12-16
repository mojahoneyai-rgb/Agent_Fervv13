"""
Dependency Injection Container
Manages singleton instances and service resolution.
"""

class Container:
    _instances = {}

    @classmethod
    def register(cls, interface, instance):
        cls._instances[interface] = instance

    @classmethod
    def get(cls, interface):
        return cls._instances.get(interface)

# Global accessor
def get_service(interface):
    return Container.get(interface)
