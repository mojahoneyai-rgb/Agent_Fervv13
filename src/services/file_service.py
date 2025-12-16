"""
File Service
Handles file system operations safely.
"""
import os
from src.core.event_bus import global_event_bus

class FileService:
    def __init__(self):
        self.current_file = None
        
    def read_file(self, path):
        """Reads content from a file."""
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.current_file = path
            return content
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return None

    def write_file(self, path, content):
        """Writes content to a file."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = path
            global_event_bus.publish("file_saved", path)
            return True
        except Exception as e:
            print(f"Error writing file {path}: {e}")
            return False

    def list_files(self, path):
        """List files and directories in path."""
        try:
            entries = os.scandir(path)
            # define sort order: directories first, then files
            dirs = []
            files = []
            for entry in entries:
                if entry.name.startswith('.') or entry.name == '__pycache__':
                    continue
                if entry.is_dir():
                    dirs.append(entry.name)
                else:
                    files.append(entry.name)
            
            dirs.sort()
            files.sort()
            return dirs, files
        except Exception as e:
            print(f"Error listing directory {path}: {e}")
            return [], []

    def get_current_file(self):
        return self.current_file
