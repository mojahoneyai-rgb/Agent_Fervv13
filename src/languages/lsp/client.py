"""
LSP Client (JSON-RPC)
minimal implementation of the Language Server Protocol client.
"""
import subprocess
import json
import threading
import time

class LSPClient:
    def __init__(self, command, language_id):
        self.command = command
        self.language_id = language_id
        self.process = None
        # RPC state would go here (message IDs, requests map)

    def start(self):
        """Starts the Language Server subprocess."""
        try:
            # shell=True to find command in path easily
            self.process = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            # Start listener thread
            t = threading.Thread(target=self._listen)
            t.daemon = True
            t.start()
            print(f"LSP: Started {self.language_id} server.")
            self.initialize()
            return True
        except Exception as e:
            print(f"LSP: Failed to start {self.language_id}: {e}")
            return False

    def _listen(self):
        """Reads JSON-RPC messages from stdout."""
        while self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                # Parse headers (Content-Length)
                if line.startswith(b'Content-Length: '):
                    length = int(line.split(b': ')[1])
                    self.process.stdout.readline() # Check empty line
                    content = self.process.stdout.read(length)
                    message = json.loads(content)
                    self.handle_message(message)
            except Exception as e:
                pass

    def handle_message(self, message):
        # Dispatch notifications/responses
        # print(f"LSP Message: {message}")
        pass

    def send_notification(self, method, params):
        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._write(msg)

    def send_request(self, method, params, id=1):
        msg = {
            "jsonrpc": "2.0",
            "id": id,
            "method": method,
            "params": params
        }
        self._write(msg)

    def _write(self, msg_dict):
        content = json.dumps(msg_dict)
        header = f"Content-Length: {len(content)}\r\n\r\n"
        data = (header + content).encode('utf-8')
        if self.process and self.process.stdin:
            self.process.stdin.write(data)
            self.process.stdin.flush()

    def initialize(self):
        root = "c:\\Users\\xpini\\Desktop\\AIFervvapp" # Mock root
        self.send_request("initialize", {
            "processId": 1234, # Mock
            "rootUri": f"file://{root}",
            "capabilities": {}
        })

    def did_open(self, file_path, content):
        self.send_notification("textDocument/didOpen", {
            "textDocument": {
                "uri": f"file://{file_path}",
                "languageId": self.language_id,
                "version": 1,
                "text": content
            }
        })
