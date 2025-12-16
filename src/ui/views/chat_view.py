"""
Chat View
The interface for the AI Co-Pilot.
"""
import customtkinter as ctk
import threading
from src.core.kernel.kernel import kernel
from src.core.event_bus import global_event_bus

class ChatView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.ai_service = kernel.get_service("AIService")
        
        # Main Layout: Stack vertically with pack
        # 1. Chat History (Top, expands)
        self.chat_display = ctk.CTkTextbox(
            self, 
            font=("Segoe UI", 13), 
            wrap="word", 
            state="disabled",
            fg_color="transparent", # Match background for cleaner look? or keep distinct
            activate_scrollbars=True
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        # 2. Input Container (Bottom, fixed height)
        self.input_frame = ctk.CTkFrame(self, height=60, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Grid inside Input Frame for precise alignment
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_field = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Ask AI Fervv...",
            height=35,
            font=("Segoe UI", 12)
        )
        self.input_field.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)
        
        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="➤", 
            width=40, 
            height=35,
            command=self.send_message,
            fg_color="#0e639c",
            hover_color="#1177bb"
        )
        self.send_btn.grid(row=0, column=1, sticky="e")
        
        self.append_message("System", "AI Fervv is ready. 🧠")

    def send_message(self, event=None):
        prompt = self.input_field.get()
        if not prompt.strip():
            return
            
        self.input_field.delete(0, "end")
        self.append_message("You", prompt)
        
        # Run async
        threading.Thread(target=self._generate_response, args=(prompt,), daemon=True).start()

    def _generate_response(self, prompt):
        try:
            # Show "Thinking..."
            # Using after to ensure thread safety for UI updates
            self.after(0, lambda: self.append_message("AI", "Thinking... 💭"))
            
            if self.ai_service:
                response = self.ai_service.generate_raw(prompt) 
            else:
                response = "Error: AIService not available."
                
            self.after(0, lambda: self._update_last_ai_message(response))
            
        except Exception as e:
            self.after(0, lambda: self.append_message("System", f"Error: {e}"))

    def append_message(self, sender, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n[{sender}]: {text}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _update_last_ai_message(self, text):
        # Naive update: just append for now, simpler than managing replace ranges in basic text widget
        self.chat_display.configure(state="normal")
        # Remove "Thinking..." (basic hack: remove last line)
        # For robustness we'll just append the real answer
        self.chat_display.insert("end", f"\n[AI]: {text}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
