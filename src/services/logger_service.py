"""
Universal Logger Service
Structured JSON logging with GZIP compression and rotation.
"""
import json
import time
import os
import gzip
import threading
import traceback
from datetime import datetime
from src.core.kernel.kernel import kernel

class UniversalLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        self.current_log_file = os.path.join(log_dir, f"session_{int(time.time())}.jsonl")
        self.lock = threading.Lock()
        
        # Start compression thread
        self.running = True
        self.compressor_thread = threading.Thread(target=self._compression_worker)
        self.compressor_thread.daemon = True
        self.compressor_thread.start()

    def log(self, level, message, context=None):
        """Logs a structured event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "context": context or {},
            "trace_id": self._get_trace_id()
        }
        
        entry = json.dumps(event)
        
        # Write to file
        with self.lock:
            with open(self.current_log_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        
        # Also print to console for dev (optional)
        # print(f"[{level}] {message}")

    def info(self, message, **kwargs):
        self.log("INFO", message, kwargs)

    def error(self, message, exc_info=None, **kwargs):
        if exc_info:
            kwargs['exception'] = traceback.format_exc()
        self.log("ERROR", message, kwargs)

    def _get_trace_id(self):
        # Placeholder for telemetry context
        return "trace-000"

    def _compression_worker(self):
        """Compresses old logs in the background."""
        while self.running:
            time.sleep(60) # Check every minute
            self._compress_old_logs()

    def _compress_old_logs(self):
        # Simple rotation logic: compress everything except current
        for f in os.listdir(self.log_dir):
            full_path = os.path.join(self.log_dir, f)
            if f.endswith(".jsonl") and full_path != self.current_log_file:
                try:
                    with open(full_path, 'rb') as f_in:
                        with gzip.open(full_path + '.gz', 'wb') as f_out:
                            import shutil
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(full_path)
                    print(f"Compressed log: {f}")
                except Exception as e:
                    print(f"Compression failed for {f}: {e}")

    def on_unload(self):
        self.running = False
        kernel.log("Logger shutting down.")

# Integration with Kernel
def setup_logger(kernel_instance):
    logger = UniversalLogger()
    kernel_instance.register_service("Logger", logger)
    # Monkey patch kernel print/log
    kernel_instance.log = logger.info
    return logger
