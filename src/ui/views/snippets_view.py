"""
Snippets View
Code snippets library panel.
"""
import customtkinter as ctk

# Built-in snippets
SNIPPETS = {
    "python": {
        "def function": "def function_name(args):\n    pass",
        "class": "class ClassName:\n    def __init__(self):\n        pass",
        "if __main__": 'if __name__ == "__main__":\n    main()',
        "try/except": "try:\n    pass\nexcept Exception as e:\n    print(e)",
        "for loop": "for i in range(10):\n    print(i)",
        "list comprehension": "[x for x in items if condition]",
    },
    "javascript": {
        "function": "function name(params) {\n    \n}",
        "arrow function": "const name = (params) => {\n    \n}",
        "async function": "async function name() {\n    const result = await fetch(url);\n}",
        "class": "class ClassName {\n    constructor() {\n    }\n}",
    },
    "html": {
        "html5": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Title</title>\n</head>\n<body>\n    \n</body>\n</html>",
        "div": '<div class="container">\n    \n</div>',
        "link css": '<link rel="stylesheet" href="style.css">',
    },
    "css": {
        "flexbox": ".container {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n}",
        "grid": ".container {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n}",
    }
}

class SnippetsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Header
        ctk.CTkLabel(self, text="CODE SNIPPETS", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=10)
        
        # Language selector
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(lang_frame, text="Language:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.lang_var = ctk.StringVar(value="python")
        ctk.CTkOptionMenu(
            lang_frame, 
            values=list(SNIPPETS.keys()), 
            variable=self.lang_var, 
            command=self.refresh_snippets,
            width=120
        ).pack(side="left", padx=2)
        
        # Snippets List
        self.snippet_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.snippet_list.pack(fill="both", expand=True)
        
        self.refresh_snippets()

    def refresh_snippets(self, *args):
        # Clear existing
        for widget in self.snippet_list.winfo_children():
            widget.destroy()
        
        lang = self.lang_var.get()
        snippets = SNIPPETS.get(lang, {})
        
        for name, code in snippets.items():
            card = ctk.CTkFrame(self.snippet_list, fg_color="#2d2d2d", corner_radius=5)
            card.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(card, text=name, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=4)
            
            preview = code[:50] + "..." if len(code) > 50 else code
            ctk.CTkLabel(card, text=preview.split("\n")[0], text_color="gray", font=("Consolas", 10)).pack(anchor="w", padx=8)
            
            ctk.CTkButton(
                card, 
                text="Insert", 
                width=50, 
                height=20, 
                fg_color="#0e639c",
                command=lambda c=code: self._insert_snippet(c)
            ).pack(anchor="e", padx=5, pady=5)

    def _insert_snippet(self, code):
        from src.core.event_bus import global_event_bus
        global_event_bus.publish("insert_snippet", code)
