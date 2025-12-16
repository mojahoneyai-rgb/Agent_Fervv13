"""
Virtual File System (VFS)
Abstracts file access to allow memory/local/remote operations.
"""
import os
from src.core.interfaces.extension import IExtension
from src.core.event_bus import global_event_bus

class VirtualFileSystem(IExtension):
    def __init__(self):
        self.mounts = {} # Point -> Provider
        
    def on_load(self, kernel):
        kernel.register_service("VFS", self)
        print("VFS Mounted")

    def on_unload(self):
        pass

    def read(self, uri):
        """Reads file content from URI."""
        # Simple local implementation for now, expandable to mock:// or ssh://
        if uri.startswith("file://"):
            path = uri.replace("file://", "")
        else:
            path = uri
            
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def write(self, uri, content):
        """Writes content to URI."""
        if uri.startswith("file://"):
            path = uri.replace("file://", "")
        else:
            path = uri
            
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            global_event_bus.publish("vfs_write", uri)
            return True
        except Exception as e:
            print(f"VFS Write Error: {e}")
            return False

    def list(self, uri):
        """Lists directory content."""
        if uri.startswith("file://"):
            path = uri.replace("file://", "")
        else:
            path = uri
            
        if os.path.isdir(path):
            return os.listdir(path)
        return []
