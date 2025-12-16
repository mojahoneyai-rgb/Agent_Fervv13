"""
Agent Tools
The set of capabilities the Autonomous Agent can use to manipulate the environment.
"""
import subprocess
from src.core.kernel.kernel import kernel

class AgentTools:
    def __init__(self):
        self.vfs = kernel.get_service("VFS")

    def read_file(self, path):
        """Reads a file from the VFS."""
        content = self.vfs.read(path)
        if content is None:
            return f"Error: File {path} not found."
        return content

    def write_file(self, path, content):
        """Writes content to a file via VFS."""
        if self.vfs.write(path, content):
            return f"Success: Wrote to {path}"
        return f"Error: Failed to write to {path}"

    def list_files(self, path="."):
        """Lists files in a directory."""
        files = self.vfs.list(path)
        return str(files)

    def execute_command(self, command):
        """Executes a shell command."""
        try:
            # Security: In a real app we'd sandbox this.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Execution Error: {e}"

    def get_tool_definitions(self):
        """Returns the schema for the AI to understand these tools."""
        return [
            {
                "name": "read_file",
                "description": "Read content of a file",
                "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}
            },
            {
                "name": "write_file",
                "description": "Write content to a file",
                "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}}
            },
            {
                "name": "execute_command",
                "description": "Run a shell command",
                "parameters": {"type": "object", "properties": {"command": {"type": "string"}}}
            }
        ]
