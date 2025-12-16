"""
Quick Integration Script for All Enhancements
Updates main.py with all new components
"""

import re

def apply_ultimate_enhancements():
    print("🚀 Applying Ultimate Enhancements...")
    
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Add imports
    new_imports = """from enhanced_chat import EnhancedChatPanel, ChatBubble
from streaming_ai import ProjectContext, StreamingAI
"""
    
    if "from enhanced_chat import" not in content:
        content = content.replace(
            "from web_browser import WebBrowser, LivePreview",
            "from web_browser import WebBrowser, LivePreview\n" + new_imports
        )
    
    # 2. Replace AI panel with enhanced chat
    # Find setup_ai_panel method and replace its content
    pattern = r'(def setup_ai_panel\(self\):.*?)(def setup_status_bar|def.*?\(self\):)'
    
    new_ai_panel = '''def setup_ai_panel(self):
        """Enhanced AI panel with modern chat"""
        self.ai_frame = ctk.CTkFrame(self, width=350, fg_color=COLORS("bg_sidebar"), corner_radius=0)
        self.ai_frame.grid(row=1, column=3, sticky="nsew")
        
        # Use enhanced chat
        self.enhanced_chat = EnhancedChatPanel(self.ai_frame)
        self.enhanced_chat.pack(fill="both", expand=True)
        
    '''
    
    # Replace setup_ai_panel
    content = re.sub(
        r'def setup_ai_panel\(self\):.*?(?=\n    def )',
        new_ai_panel,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    # 3. Update send_ai to use streaming
    send_ai_pattern = r'def send_ai\(self, event=None\):.*?threading\.Thread\(target=ai_thread, daemon=True\)\.start\(\)'
    
    new_send_ai = '''def send_ai(self, event=None):
        """Send message to AI with enhanced chat"""
        if hasattr(self, 'enhanced_chat'):
            # Chat handles sending
            self.enhanced_chat.send_message()
        else:
            # Fallback to old method
            user_input = self.ai_input.get().strip()
            if not user_input:
                return
            self.ai_input.delete(0, "end")
            self.chat_append("You", user_input)
            
            def ai_thread():
                try:
                    response = self.agent.generate_response(user_input)
                    self.after(0, lambda: self.chat_append("Agent", response))
                except Exception as e:
                    self.after(0, lambda: self.chat_append("Error", str(e)))
            
            threading.Thread(target=ai_thread, daemon=True).start()'''
    
    content = re.sub(send_ai_pattern, new_send_ai, content, flags=re.DOTALL)
    
    # 4. Initialize context manager
    init_pattern = r'(self\.web_browser = None)'
    new_init = r'\1\n        self.project_context = ProjectContext()\n        self.streaming_ai = None'
    content = re.sub(init_pattern, new_init, content)
    
    # 5. Update title
    content = content.replace(
        'AI Fervv Studio Code - Ultimate Edition Pro',
        'AI Fervv Studio Code - Professional Edition 🚀'
    )
    
    # Write updated content
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ All enhancements applied!")
    return True

if __name__ == "__main__":
    try:
        apply_ultimate_enhancements()
        print("\n✨ Integration Complete!")
        print("Ready to build and test!")
    except Exception as e:
        print(f"❌ Error: {e}")
