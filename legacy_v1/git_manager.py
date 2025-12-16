"""
AI Fervv IDE - Git Integration
Git repository management and operations
"""

import subprocess
import os

class GitManager:
    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
    
    def set_repo_path(self, path):
        """Set repository path"""
        self.repo_path = path
    
    def run_git_command(self, command):
        """Execute git command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    def is_git_repo(self):
        """Check if current directory is a git repository"""
        result = self.run_git_command("git rev-parse --git-dir")
        return result["success"]
    
    def init_repo(self):
        """Initialize new git repository"""
        return self.run_git_command("git init")
    
    def get_status(self):
        """Get repository status"""
        result = self.run_git_command("git status --porcelain")
        if not result["success"]:
            return None
        
        files = {"modified": [], "untracked": [], "staged": []}
        
        for line in result["output"].split("\n"):
            if not line:
                continue
            
            status = line[:2]
            filename = line[3:].strip()
            
            if status == "??":
                files["untracked"].append(filename)
            elif status[0] in ["M", "A", "D"]:
                files["staged"].append(filename)
            elif status[1] in ["M", "D"]:
                files["modified"].append(filename)
        
        return files
    
    def add_file(self, filepath):
        """Stage file for commit"""
        return self.run_git_command(f'git add "{filepath}"')
    
    def add_all(self):
        """Stage all changes"""
        return self.run_git_command("git add .")
    
    def commit(self, message):
        """Commit staged changes"""
        return self.run_git_command(f'git commit -m "{message}"')
    
    def get_branches(self):
        """Get list of branches"""
        result = self.run_git_command("git branch")
        if not result["success"]:
            return []
        
        branches = []
        for line in result["output"].split("\n"):
            if line:
                branch = line.strip().replace("* ", "")
                branches.append(branch)
        
        return branches
    
    def get_current_branch(self):
        """Get current branch name"""
        result = self.run_git_command("git branch --show-current")
        if result["success"]:
            return result["output"].strip()
        return None
    
    def create_branch(self, branch_name):
        """Create new branch"""
        return self.run_git_command(f"git branch {branch_name}")
    
    def checkout_branch(self, branch_name):
        """Switch to different branch"""
        return self.run_git_command(f"git checkout {branch_name}")
    
    def push(self, remote="origin", branch=None):
        """Push commits to remote"""
        if not branch:
            branch = self.get_current_branch()
        return self.run_git_command(f"git push {remote} {branch}")
    
    def pull(self, remote="origin", branch=None):
        """Pull changes from remote"""
        if not branch:
            branch = self.get_current_branch()
        return self.run_git_command(f"git pull {remote} {branch}")
    
    def get_log(self, count=10):
        """Get commit history"""
        result = self.run_git_command(f"git log --oneline -n {count}")
        if not result["success"]:
            return []
        
        commits = []
        for line in result["output"].split("\n"):
            if line:
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1]
                    })
        
        return commits
    
    def get_diff(self, filepath=None):
        """Get diff of changes"""
        cmd = "git diff"
        if filepath:
            cmd += f' "{filepath}"'
        return self.run_git_command(cmd)
    
    def get_remote_url(self):
        """Get remote repository URL"""
        result = self.run_git_command("git remote get-url origin")
        if result["success"]:
            return result["output"].strip()
        return None
    
    def add_remote(self, url, name="origin"):
        """Add remote repository"""
        return self.run_git_command(f"git remote add {name} {url}")
