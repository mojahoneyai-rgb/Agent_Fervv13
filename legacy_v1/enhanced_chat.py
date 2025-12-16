"""
AI Fervv IDE - Enhanced Chat UI
Modern chat interface with animations and interactions
"""

import customtkinter as ctk
from tkinter import Text, END
import datetime

class ChatBubble(ctk.CTkFrame):
    """Single chat message bubble"""
    
    def __init__(self, master, role, message, **kwargs):
        # Choose colors based on role
        if role == "Agent":
            fg_color = "#2d2d2d"
            align = "left"
            icon = "🤖"
            text_color = "#cccccc"
        elif role == "You":
            fg_color = "#1a3a52"
            align = "right"
            icon = "👤"
            text_color = "#e0e0e0"
        else:  # System
            fg_color = "#2a2a1a"
            align = "left"
            icon = "ℹ️"
            text_color = "#dcdcaa"
        
        super().__init__(master, fg_color=fg_color, corner_radius=10, **kwargs)
        
        self.role = role
        self.message = message
        
        # Header with icon and role
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(8, 2))
        
        role_label = ctk.CTkLabel(
            header, 
            text=f"{icon} {role}",
            font=("Segoe UI", 10, "bold"),
            text_color="#569cd6" if role == "Agent" else "#4ec9b0"
        )
        role_label.pack(side="left")
        
        # Timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        time_label = ctk.CTkLabel(
            header,
            text=timestamp,
            font=("Segoe UI", 9),
            text_color="#858585"
        )
        time_label.pack(side="right")
        
        # Message content
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            font=("Segoe UI", 10),
            text_color=text_color,
            wraplength=320,
            justify="left",
            anchor="w"
        )
        self.message_label.pack(fill="x", padx=10, pady=(0, 8))
        
        # Action buttons (appear on hover)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent", height=25)
        
        self.copy_btn = ctk.CTkButton(
            self.actions_frame,
            text="📋",
            width=30,
            height=25,
            fg_color="transparent",
            hover_color="#3e3e3e",
            command=self.copy_message
        )
        self.copy_btn.pack(side="left", padx=2)
        
        if role == "Agent":
            self.thumbs_up = ctk.CTkButton(
                self.actions_frame,
                text="👍",
                width=30,
                height=25,
                fg_color="transparent",
                hover_color="#3e3e3e",
                command=lambda: self.react("👍")
            )
            self.thumbs_up.pack(side="left", padx=2)
            
            self.thumbs_down = ctk.CTkButton(
                self.actions_frame,
                text="👎",
                width=30,
                height=25,
                fg_color="transparent",
                hover_color="#3e3e3e",
                command=lambda: self.react("👎")
            )
            self.thumbs_down.pack(side="left", padx=2)
        
        # Bind hover events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        
        # Initial state
        self.alpha = 0.0
        self.fade_in()
    
    def fade_in(self):
        """Smooth fade-in animation"""
        if self.alpha < 1.0:
            self.alpha += 0.1
            # Can't actually change alpha in CTk, but we can simulate with color
            self.after(20, self.fade_in)
    
    def on_hover(self, event=None):
        """Show actions on hover"""
        self.actions_frame.pack(fill="x", padx=10, pady=(0, 5))
    
    def on_leave(self, event=None):
        """Hide actions when not hovering"""
        self.actions_frame.pack_forget()
    
    def copy_message(self):
        """Copy message to clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(self.message)
            # Show feedback
            self.copy_btn.configure(text="✓")
            self.after(1000, lambda: self.copy_btn.configure(text="📋"))
        except:
            pass
    
    def react(self, reaction):
        """Add reaction to message"""
        print(f"Reacted with {reaction} to: {self.message[:30]}...")

class TypingIndicator(ctk.CTkFrame):
    """Animated typing indicator"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#2d2d2d", corner_radius=10, height=50, **kwargs)
        
        # Icon and text
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True)
        
        ctk.CTkLabel(content, text="🤖", font=("Segoe UI", 14)).pack(side="left", padx=5)
        
        self.dots_label = ctk.CTkLabel(
            content,
            text="●",
            font=("Segoe UI", 16),
            text_color="#569cd6"
        )
        self.dots_label.pack(side="left")
        
        self.dot_count = 0
        self.animate_dots()
    
    def animate_dots(self):
        """Animate typing dots"""
        self.dot_count = (self.dot_count + 1) % 4
        dots = "●" * self.dot_count + "○" * (3 - self.dot_count)
        self.dots_label.configure(text=dots)
        self.after(400, self.animate_dots)

class EnhancedChatPanel(ctk.CTkFrame):
    """Modern chat panel with bubbles and animations"""
    
    def __init__(self, master, agent=None, voice_callback=None, **kwargs):
        super().__init__(master, fg_color="#1e1e1e", **kwargs)
        
        self.agent = agent
        self.voice_callback = voice_callback
        
        # Header
        self.setup_header()
        
        # Chat area
        self.chat_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="#1e1e1e",
            scrollbar_button_color="#3e3e3e"
        )
        self.chat_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Suggestions area
        self.suggestions_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        self.suggestions_frame.pack(fill="x", pady=10)
        
        # Input area
        self.setup_input()
        
        # Typing indicator (hidden by default)
        self.typing_indicator = None
        
        # Show initial suggestions
        if self.agent:
            self.show_suggestions()
    
    def setup_header(self):
        """Create animated header"""
        header = ctk.CTkFrame(self, height=50, fg_color="#252526")
        header.pack(fill="x", padx=5, pady=(5, 0))
        
        # Title with animation
        title = ctk.CTkLabel(
            header,
            text="🤖 AI Copilot",
            font=("Segoe UI", 14, "bold"),
            text_color="#569cd6"
        )
        title.pack(side="left", padx=15, pady=10)
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            header,
            text="●",
            font=("Segoe UI", 20),
            text_color="#4ec9b0"  # Green = ready
        )
        self.status_indicator.pack(side="right", padx=10)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            header,
            text="⚙️",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#3e3e3e"
        )
        settings_btn.pack(side="right", padx=5)
    
    def setup_input(self):
        """Create input area"""
        input_frame = ctk.CTkFrame(self, fg_color="#252526", height=80)
        input_frame.pack(fill="x", padx=5, pady=5)
        input_frame.pack_propagate(False)
        
        # Input field
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask AI anything...",
            height=40,
            font=("Segoe UI", 11),
            border_width=0,
            fg_color="#3e3e3e"
        )
        self.input_entry.pack(fill="x", padx=10, pady=(10, 5))
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        # Buttons
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        send_btn = ctk.CTkButton(
            btn_frame,
            text="Send",
            width=80,
            height=30,
            fg_color="#007ACC",
            hover_color="#005A9E",
            command=self.send_message
        )
        send_btn.pack(side="right")
        
        voice_btn = ctk.CTkButton(
            btn_frame,
            text="🎤",
            width=40,
            height=30,
            fg_color="transparent",
            hover_color="#3e3e3e",
            command=self.voice_callback
        )
        self.voice_btn = voice_btn
        voice_btn.pack(side="right", padx=5)
    
    def add_message(self, role, message):
        """Add message bubble with fade-in"""
        bubble = ChatBubble(self.chat_scroll, role, message)
        bubble.pack(fill="x", pady=5, padx=10)
        
        # Ensure suggestions stay at bottom if re-added, but normally bubbles added above
        # Actually bubbles are packed, suggestions are frame packed at init.
        # We should repack suggestions to be at bottom if needed, or insert bubbles before suggestions.
        # For simplicity, we'll let bubbles stack and keep suggestions at top or hide them.
        # Let's hide suggestions when chat starts.
        if role == "You":
            self.suggestions_frame.pack_forget()
        
        # Auto-scroll to bottom
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
        
        return bubble
    
    def show_typing(self):
        """Show typing indicator"""
        if not self.typing_indicator:
            self.typing_indicator = TypingIndicator(self.chat_scroll)
            self.typing_indicator.pack(fill="x", pady=5, padx=10)
            self.chat_scroll._parent_canvas.yview_moveto(1.0)
    
    def hide_typing(self):
        """Hide typing indicator"""
        if self.typing_indicator:
            self.typing_indicator.destroy()
            self.typing_indicator = None
    
    def send_message(self):
        """Send user message"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        # Clear input
        self.input_entry.delete(0, END)
        
        # Add user message
        self.add_message("You", message)
        
        # Show typing
        self.show_typing()
        
        # Call actual AI
        if self.agent:
            import threading
            def run_ai():
                response = self.agent.generate_response(message)
                self.after(0, lambda: self.receive_response(response))
            
            threading.Thread(target=run_ai, daemon=True).start()
        else:
            self.after(1000, lambda: self.receive_response("Agent not connected."))
    
    def receive_response(self, response):
        """Receive AI response"""
        self.hide_typing()
        self.add_message("Agent", response)
    
    def set_status(self, status_color):
        """Update status indicator color"""
        self.status_indicator.configure(text_color=status_color)

    def show_suggestions(self):
        """Show personalized project suggestions"""
        for w in self.suggestions_frame.winfo_children(): w.destroy()
        
        ctk.CTkLabel(self.suggestions_frame, text="Suggested Actions:", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=10)
        
        suggestions = [
            "Analyze project structure",
            "Refactor current file",
            "Generate documentation",
            "Check for bugs"
        ]
        
        for sugg in suggestions:
            btn = ctk.CTkButton(
                self.suggestions_frame,
                text=sugg,
                height=24,
                fg_color="#2d2d2d",
                hover_color="#3e3e3e",
                anchor="w",
                command=lambda s=sugg: self.use_suggestion(s)
            )
            btn.pack(fill="x", padx=10, pady=2)
            
    def use_suggestion(self, text):
        self.input_entry.insert(0, text)
        self.send_message()

    def set_voice_active(self, active):
        if hasattr(self, 'voice_btn'):
            if active:
                self.voice_btn.configure(fg_color="#c42b1c", hover_color="#a02015") # Red when active
            else:
                self.voice_btn.configure(fg_color="transparent", hover_color="#3e3e3e")
