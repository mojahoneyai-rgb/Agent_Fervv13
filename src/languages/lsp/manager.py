"""
LSP Manager
Manages LSP clients for different languages.
"""
from src.languages.lsp.client import LSPClient

class LSPManager:
    def __init__(self):
        self.clients = {} # lang_id -> client
        self.configs = {
            "python": "pyright-langserver --stdio",
            "javascript": "typescript-language-server --stdio",
            "html": "vscode-html-language-server --stdio"
        }

    def start_server(self, lang_id):
        if lang_id in self.clients:
            return self.clients[lang_id]
            
        cmd = self.configs.get(lang_id)
        if cmd:
            client = LSPClient(cmd, lang_id)
            if client.start():
                self.clients[lang_id] = client
                return client
        return None

    def notify_open(self, lang_id, file_path, content):
        client = self.start_server(lang_id)
        if client:
            client.did_open(file_path, content)
