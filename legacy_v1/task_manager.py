"""
AI Fervv IDE - Task Manager
Project task management and tracking
"""

import json
import os
from datetime import datetime
from enum import Enum

class TaskPriority(Enum):
    LOW = ("Low", "#4ec9b0")
    MEDIUM = ("Medium", "#dcdcaa")
    HIGH = ("High", "#f48771")

class TaskStatus(Enum):
    TODO = ("To Do", "#6a9955")
    IN_PROGRESS = ("In Progress", "#569cd6")
    DONE = ("Done", "#4ec9b0")

class Task:
    """Individual task"""
    
    def __init__(self, title, description="", priority=TaskPriority.MEDIUM, 
                 due_date=None, tags=None):
        self.id = datetime.now().timestamp()
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.TODO
        self.due_date = due_date
        self.tags = tags or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.completed_at = None
    
    def mark_done(self):
        """Mark task as done"""
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def mark_in_progress(self):
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()
    
    def mark_todo(self):
        """Mark task as todo"""
        self.status = TaskStatus.TODO
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        task = cls(data["title"], data.get("description", ""))
        task.id = data["id"]
        task.priority = TaskPriority[data["priority"]]
        task.status = TaskStatus[data["status"]]
        task.tags = data.get("tags", [])
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])
        
        if data.get("due_date"):
            task.due_date = datetime.fromisoformat(data["due_date"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        
        return task

class TaskManager:
    """Manages project tasks"""
    
    def __init__(self, project_path=None):
        self.tasks = []
        self.project_path = project_path
        self.tasks_file = None
        
        if project_path:
            self.tasks_file = os.path.join(project_path, ".fervv_tasks.json")
            self.load_tasks()
    
    def add_task(self, title, description="", priority=TaskPriority.MEDIUM, 
                 due_date=None, tags=None):
        """Add new task"""
        task = Task(title, description, priority, due_date, tags)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def remove_task(self, task_id):
        """Remove task by ID"""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()
    
    def get_task(self, task_id):
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status):
        """Get tasks by status"""
        return [t for t in self.tasks if t.status == status]
    
    def get_tasks_by_priority(self, priority):
        """Get tasks by priority"""
        return [t for t in self.tasks if t.priority == priority]
    
    def get_tasks_by_tag(self, tag):
        """Get tasks by tag"""
        return [t for t in self.tasks if tag in t.tags]
    
    def search_tasks(self, query):
        """Search tasks by title or description"""
        query = query.lower()
        return [t for t in self.tasks 
                if query in t.title.lower() or query in t.description.lower()]
    
    def get_statistics(self):
        """Get task statistics"""
        total = len(self.tasks)
        done = len(self.get_tasks_by_status(TaskStatus.DONE))
        in_progress = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        todo = len(self.get_tasks_by_status(TaskStatus.TODO))
        
        return {
            "total": total,
            "done": done,
            "in_progress": in_progress,
            "todo": todo,
            "completion_rate": (done / total * 100) if total > 0 else 0
        }
    
    def save_tasks(self):
        """Save tasks to file"""
        if self.tasks_file:
            try:
                data = [task.to_dict() for task in self.tasks]
                with open(self.tasks_file, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from file"""
        if self.tasks_file and os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
            except Exception as e:
                print(f"Error loading tasks: {e}")
    
    def export_to_markdown(self):
        """Export tasks to markdown format"""
        md = "# Project Tasks\n\n"
        
        for status in TaskStatus:
            tasks = self.get_tasks_by_status(status)
            if tasks:
                md += f"## {status.value[0]}\n\n"
                for task in tasks:
                    checkbox = "[x]" if status == TaskStatus.DONE else "[ ]"
                    md += f"- {checkbox} **{task.title}**"
                    if task.priority == TaskPriority.HIGH:
                        md += " 🔴"
                    md += "\n"
                    if task.description:
                        md += f"  - {task.description}\n"
                    if task.tags:
                        md += f"  - Tags: {', '.join(task.tags)}\n"
                    md += "\n"
        
        stats = self.get_statistics()
        md += f"\n---\n\n**Statistics:** {stats['done']}/{stats['total']} completed ({stats['completion_rate']:.1f}%)\n"
        
        return md
