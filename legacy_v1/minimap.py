"""
AI Fervv IDE - Code Minimap
VS Code-style minimap for code overview
"""

import customtkinter as ctk
from tkinter import Canvas

class CodeMinimap(ctk.CTkFrame):
    """Minimap showing code overview"""
    
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, width=100, fg_color="#1e1e1e", **kwargs)
        
        self.text_widget = text_widget
        self.pack_propagate(False)
        
        # Canvas for minimap
        self.canvas = Canvas(
            self, 
            width=90, 
            bg="#1e1e1e", 
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Update timer
        self.update_minimap()
    
    def update_minimap(self):
        """Update minimap display"""
        if not self.text_widget:
            return
        
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Get text content
            content = self.text_widget.get("1.0", "end-1c")
            lines = content.split('\n')
            
            # Calculate minimap dimensions
            canvas_height = self.canvas.winfo_height()
            if canvas_height < 10:
                canvas_height = 400
            
            canvas_width = 90
            line_height = max(1, canvas_height / max(len(lines), 1))
            
            # Draw lines
            for i, line in enumerate(lines):
                y = i * line_height
                
                # Determine line color based on content
                if line.strip():
                    # Has content
                    intensity = min(len(line.strip()) * 3, 100)
                    color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
                    
                    # Draw line representation
                    line_width = min(len(line.strip()) * 2, canvas_width)
                    self.canvas.create_rectangle(
                        0, y, line_width, y + line_height,
                        fill=color, outline=""
                    )
            
            # Draw viewport indicator
            try:
                visible_start = self.text_widget.yview()[0]
                visible_end = self.text_widget.yview()[1]
                
                viewport_start = visible_start * canvas_height
                viewport_height = (visible_end - visible_start) * canvas_height
                
                # Semi-transparent viewport box
                self.canvas.create_rectangle(
                    0, viewport_start,
                    canvas_width, viewport_start + viewport_height,
                    outline="#569cd6", width=1, fill="", stipple="gray50"
                )
            except:
                pass
            
            # Schedule next update
            self.after(1000, self.update_minimap)
            
        except Exception as e:
            print(f"Minimap update error: {e}")
            self.after(1000, self.update_minimap)
    
    def on_click(self, event):
        """Handle click on minimap"""
        if not self.text_widget:
            return
        
        # Calculate line number
        canvas_height = self.canvas.winfo_height()
        click_ratio = event.y / canvas_height
        
        # Scroll to that position
        self.text_widget.yview_moveto(click_ratio)
    
    def on_drag(self, event):
        """Handle drag on minimap"""
        self.on_click(event)
