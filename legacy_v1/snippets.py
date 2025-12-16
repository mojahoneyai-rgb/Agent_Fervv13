"""
AI Fervv IDE - Code Snippets System
Predefined code snippets for rapid development
"""

SNIPPETS = {
    "python": {
        "main": {
            "name": "Python Main",
            "code": '''if __name__ == "__main__":
    pass''',
            "description": "Standard Python main block"
        },
        "class": {
            "name": "Class Definition",
            "code": '''class ClassName:
    def __init__(self):
        pass
    
    def method(self):
        pass''',
            "description": "Basic class template"
        },
        "func": {
            "name": "Function",
            "code": '''def function_name(param):
    """Docstring"""
    return None''',
            "description": "Function with docstring"
        },
        "try": {
            "name": "Try-Except",
            "code": '''try:
    # code
    pass
except Exception as e:
    print(f"Error: {e}")''',
            "description": "Try-except block"
        },
        "flask": {
            "name": "Flask App",
            "code": '''from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)''',
            "description": "Basic Flask application"
        },
        "tkinter": {
            "name": "Tkinter Window",
            "code": '''import tkinter as tk

root = tk.Tk()
root.title("Window Title")
root.geometry("800x600")

# Your widgets here

root.mainloop()''',
            "description": "Basic Tkinter window"
        }
    },
    
    "javascript": {
        "func": {
            "name": "Function",
            "code": '''function functionName(params) {
    // code
    return value;
}''',
            "description": "Standard function"
        },
        "arrow": {
            "name": "Arrow Function",
            "code": '''const functionName = (params) => {
    // code
    return value;
};''',
            "description": "ES6 arrow function"
        },
        "class": {
            "name": "Class",
            "code": '''class ClassName {
    constructor() {
        // initialization
    }
    
    method() {
        // code
    }
}''',
            "description": "ES6 class"
        },
        "async": {
            "name": "Async Function",
            "code": '''async function fetchData() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}''',
            "description": "Async/await pattern"
        },
        "react": {
            "name": "React Component",
            "code": '''import React from 'react';

const ComponentName = () => {
    return (
        <div>
            {/* content */}
        </div>
    );
};

export default ComponentName;''',
            "description": "React functional component"
        }
    },
    
    "html": {
        "html5": {
            "name": "HTML5 Template",
            "code": '''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Title</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <script src="script.js"></script>
</body>
</html>''',
            "description": "Complete HTML5 template"
        },
        "form": {
            "name": "Form",
            "code": '''<form action="" method="post">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    
    <button type="submit">Submit</button>
</form>''',
            "description": "Basic form structure"
        },
        "table": {
            "name": "Table",
            "code": '''<table>
    <thead>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>''',
            "description": "HTML table"
        }
    },
    
    "css": {
        "flex": {
            "name": "Flexbox Container",
            "code": '''.container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}''',
            "description": "Flexbox layout"
        },
        "grid": {
            "name": "Grid Container",
            "code": '''.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}''',
            "description": "CSS Grid layout"
        },
        "animation": {
            "name": "Animation",
            "code": '''@keyframes animationName {
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.animated {
    animation: animationName 0.3s ease-in-out;
}''',
            "description": "CSS animation"
        }
    }
}

class SnippetManager:
    def __init__(self):
        self.snippets = SNIPPETS
        self.custom_snippets = {}
    
    def get_snippets_for_language(self, language):
        """Get all snippets for a specific language"""
        lang = language.lower()
        snippets = {}
        
        if lang in self.snippets:
            snippets.update(self.snippets[lang])
        
        if lang in self.custom_snippets:
            snippets.update(self.custom_snippets[lang])
        
        return snippets
    
    def get_snippet(self, language, snippet_id):
        """Get specific snippet"""
        lang = language.lower()
        
        if lang in self.snippets and snippet_id in self.snippets[lang]:
            return self.snippets[lang][snippet_id]
        
        if lang in self.custom_snippets and snippet_id in self.custom_snippets[lang]:
            return self.custom_snippets[lang][snippet_id]
        
        return None
    
    def add_custom_snippet(self, language, snippet_id, name, code, description=""):
        """Add custom snippet"""
        lang = language.lower()
        
        if lang not in self.custom_snippets:
            self.custom_snippets[lang] = {}
        
        self.custom_snippets[lang][snippet_id] = {
            "name": name,
            "code": code,
            "description": description
        }
        return True
    
    def search_snippets(self, query):
        """Search snippets by name or description"""
        results = []
        query = query.lower()
        
        for lang, snippets in self.snippets.items():
            for snip_id, snip_data in snippets.items():
                if (query in snip_data["name"].lower() or 
                    query in snip_data["description"].lower()):
                    results.append({
                        "language": lang,
                        "id": snip_id,
                        "data": snip_data
                    })
        
        return results
