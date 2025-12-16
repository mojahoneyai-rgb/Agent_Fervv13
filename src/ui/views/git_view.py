"""
Git View
Source control integration panel.
"""
import customtkinter as ctk
import subprocess
import os
from src.core.container import get_service

class GitView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_svc = get_service("FileService")
        
        # Header
        ctk.CTkLabel(self, text="SOURCE CONTROL", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=10)
        
        # Actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(actions, text="Init Repo", width=80, height=24, command=self.git_init).pack(side="left", padx=2)
        ctk.CTkButton(actions, text="Refresh", width=60, height=24, command=self.refresh_status).pack(side="left", padx=2)
        
        # Status List
        self.status_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.status_list.pack(fill="both", expand=True, pady=5)
        
        # Commit Section
        commit_frame = ctk.CTkFrame(self, fg_color="transparent")
        commit_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(commit_frame, text="Commit:", font=("Segoe UI", 10)).pack(anchor="w")
        self.commit_msg = ctk.CTkEntry(commit_frame, placeholder_text="Commit message...")
        self.commit_msg.pack(fill="x", pady=2)
        
        btn_frame = ctk.CTkFrame(commit_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=2)
        ctk.CTkButton(btn_frame, text="Commit", width=70, height=24, command=self.git_commit).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Push", width=60, height=24, command=self.git_push).pack(side="left", padx=2)
        
        self.refresh_status()

    def _run_git(self, args):
        """Run git command and return output"""
        try:
            cwd = self.file_svc.current_folder if self.file_svc else os.getcwd()
            result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    def git_init(self):
        output = self._run_git(["init"])
        self._show_output(output)
        self.refresh_status()

    def refresh_status(self):
        # Clear existing
        for widget in self.status_list.winfo_children():
            widget.destroy()
        
        output = self._run_git(["status", "--porcelain"])
        if not output.strip():
            ctk.CTkLabel(self.status_list, text="No changes", text_color="gray").pack(anchor="w", padx=5)
            return
            
        for line in output.strip().split("\n"):
            if line:
                status = line[:2]
                filename = line[3:]
                color = "#4ec9b0" if "A" in status or "M" in status else "#f14c4c"
                ctk.CTkLabel(self.status_list, text=f"{status} {filename}", text_color=color).pack(anchor="w", padx=5)

    def git_commit(self):
        msg = self.commit_msg.get()
        if not msg.strip():
            return
        self._run_git(["add", "-A"])
        output = self._run_git(["commit", "-m", msg])
        self._show_output(output)
        self.commit_msg.delete(0, "end")
        self.refresh_status()

    def git_push(self):
        output = self._run_git(["push"])
        self._show_output(output)

    def _show_output(self, text):
        # Simple notification - could be improved
        print(f"[Git] {text}")
