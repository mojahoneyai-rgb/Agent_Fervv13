"""
Tasks View
Task management panel.
"""
import customtkinter as ctk
from datetime import datetime

class TasksView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tasks = []
        
        # Header
        ctk.CTkLabel(self, text="TASK MANAGER ✅", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=10)
        
        # Actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(actions, text="➕ Add Task", width=100, height=24, command=self.add_task_dialog).pack(side="left", padx=2)
        
        # Task List
        self.task_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.task_list.pack(fill="both", expand=True)
        
        # Stats
        self.stats_label = ctk.CTkLabel(self, text="Tasks: 0/0", font=("Segoe UI", 10), text_color="gray")
        self.stats_label.pack(pady=5)
        
        self.refresh_tasks()

    def add_task_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter task description:", title="Add Task")
        task_text = dialog.get_input()
        if task_text and task_text.strip():
            self.tasks.append({
                "text": task_text,
                "done": False,
                "created": datetime.now().strftime("%H:%M")
            })
            self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.task_list.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            ctk.CTkLabel(self.task_list, text="No tasks yet", text_color="gray").pack(pady=10)
        
        for i, task in enumerate(self.tasks):
            card = ctk.CTkFrame(self.task_list, fg_color="#2d2d2d", corner_radius=5)
            card.pack(fill="x", pady=2, padx=5)
            
            # Checkbox
            var = ctk.BooleanVar(value=task["done"])
            cb = ctk.CTkCheckBox(
                card, 
                text=task["text"], 
                variable=var,
                command=lambda idx=i, v=var: self._toggle_task(idx, v)
            )
            cb.pack(side="left", padx=5, pady=5)
            
            # Time
            ctk.CTkLabel(card, text=task["created"], text_color="gray", font=("Segoe UI", 9)).pack(side="right", padx=5)
        
        # Update stats
        done = sum(1 for t in self.tasks if t["done"])
        total = len(self.tasks)
        self.stats_label.configure(text=f"Tasks: {done}/{total}")

    def _toggle_task(self, idx, var):
        self.tasks[idx]["done"] = var.get()
        self.refresh_tasks()
