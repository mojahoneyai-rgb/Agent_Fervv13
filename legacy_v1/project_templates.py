"""
AI Fervv IDE - Project Templates
Quick project scaffolding and templates
"""

import os

class ProjectTemplate:
    def __init__(self, name, description, files):
        self.name = name
        self.description = description
        self.files = files  # Dict of {path: content}

TEMPLATES = {
    "python_basic": ProjectTemplate(
        "Python Basic",
        "Basic Python project with main file",
        {
            "main.py": '''"""
Main application file
"""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''',
            "README.md": '''# Python Project

## Description
Your project description here

## Usage
```bash
python main.py
```
''',
            "requirements.txt": ''''''
        }
    ),
    
    "flask_webapp": ProjectTemplate(
        "Flask Web App",
        "Flask web application with templates",
        {
            "app.py": '''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({"status": "success", "data": data})
    return jsonify({"message": "GET request received"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''',
            "templates/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Welcome to Flask</h1>
    <div id="content"></div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
''',
            "static/style.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

h1 {
    color: white;
    text-align: center;
}
''',
            "static/script.js": '''console.log("Flask app loaded");

// Fetch data example
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data));
''',
            "requirements.txt": '''Flask==3.0.0
''',
            "README.md": '''# Flask Web Application

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
python app.py
```
'''
        }
    ),
    
    "html_css_js": ProjectTemplate(
        "HTML/CSS/JS Website",
        "Modern responsive website template",
        {
            "index.html": '''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo">Logo</h1>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>
    
    <section class="hero" id="home">
        <div class="container">
            <h2 class="hero-title">Welcome to Modern Web</h2>
            <p class="hero-subtitle">Beautiful, Responsive, Modern</p>
            <button class="cta-button">Get Started</button>
        </div>
    </section>
    
    <section class="features" id="about">
        <div class="container">
            <h2>Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>Fast</h3>
                    <p>Lightning fast performance</p>
                </div>
                <div class="feature-card">
                    <h3>Responsive</h3>
                    <p>Works on all devices</p>
                </div>
                <div class="feature-card">
                    <h3>Modern</h3>
                    <p>Latest web technologies</p>
                </div>
            </div>
        </div>
    </section>
    
    <script src="script.js"></script>
</body>
</html>
''',
            "style.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --dark: #1e293b;
    --light: #f1f5f9;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--dark);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar */
.navbar {
    background: var(--dark);
    color: white;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary);
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 100px 0;
    text-align: center;
}

.hero-title {
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease-out;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    animation: fadeInUp 0.8s ease-out 0.2s backwards;
}

.cta-button {
    background: white;
    color: var(--primary);
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    animation: fadeInUp 0.8s ease-out 0.4s backwards;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Features */
.features {
    padding: 80px 0;
    background: var(--light);
}

.features h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
''',
            "script.js": '''// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Button interaction
document.querySelector('.cta-button').addEventListener('click', () => {
    alert('Welcome! Start building something amazing!');
});

console.log('Website loaded successfully!');
'''
        }
    ),
    
    "react_app": ProjectTemplate(
        "React Application",
        "React app with modern setup",
        {
            "README.md": '''# React Application

## Setup
```bash
npx create-react-app .
npm start
```

This is a starter template. Run the commands above to initialize.
''',
            "src/App.js": '''import React, { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Application</h1>
        <p>Count: {count}</p>
        <button onClick={() => setCount(count + 1)}>
          Increment
        </button>
      </header>
    </div>
  );
}

export default App;
''',
            "src/App.css": '''.App {
  text-align: center;
}

.App-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

button {
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  transform: scale(1.05);
}
'''
        }
    )
}

class TemplateManager:
    def __init__(self):
        self.templates = TEMPLATES
    
    def get_all_templates(self):
        """Get list of all available templates"""
        return {key: {"name": tmpl.name, "description": tmpl.description} 
                for key, tmpl in self.templates.items()}
    
    def create_project(self, template_key, destination_path):
        """Create project from template"""
        if template_key not in self.templates:
            return False, "Template not found"
        
        template = self.templates[template_key]
        
        try:
            # Create destination directory
            os.makedirs(destination_path, exist_ok=True)
            
            # Create all files
            for file_path, content in template.files.items():
                full_path = os.path.join(destination_path, file_path)
                
                # Create subdirectories if needed
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Write file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True, f"Project created successfully at {destination_path}"
        
        except Exception as e:
            return False, f"Error creating project: {str(e)}"
