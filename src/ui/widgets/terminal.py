"""
Terminal Widget
Allows execution of system commands (Node, Python, AHK) within the IDE.
"""
import customtkinter as ctk
import subprocess
import threading
import tkinter as tk

class Terminal(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # UI
        self.output_area = ctk.CTkTextbox(self, font=("Consolas", 12), fg_color="#1e1e1e", text_color="#cccccc")
        self.output_area.pack(fill="both", expand=True)
        
        self.input_field = ctk.CTkEntry(self, font=("Consolas", 12), fg_color="#252526")
        self.input_field.pack(fill="x", padx=2, pady=2)
        self.input_field.bind("<Return>", self.run_command)
        
        self.write_output("AI Fervv Terminal v1.0\nReady.\n")

    def run_command(self, event=None):
        cmd = self.input_field.get()
        self.input_field.delete(0, "end")
        self.write_output(f"> {cmd}\n")
        
        if cmd.strip() == "clear":
            self.output_area.configure(state="normal")
            self.output_area.delete("1.0", "end")
            self.output_area.configure(state="disabled")
            return

        # Run in thread
        t = threading.Thread(target=self._exec, args=(cmd,))
        t.daemon = True
        t.start()

    def _exec(self, cmd):
        try:
            # shell=True required for some commands, ignore security for local user app
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if stdout:
                self.write_output(stdout)
            if stderr:
                self.write_output(stderr) # Usually in red logic
        except Exception as e:
            self.write_output(f"Error: {e}\n")

    def write_output(self, text):
        def _write():
            self.output_area.configure(state="normal")
            self.output_area.insert("end", text)
            self.output_area.see("end")
            self.output_area.configure(state="disabled")
        self.after(0, _write)
