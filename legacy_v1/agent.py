import os
from openai import OpenAI

# Try importing Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI not installed. Install with: pip install google-generativeai")

from ai_settings import ai_settings
from agent_core import AgentCore

class AI_Fervv:
    def __init__(self):
        """Initialize AI with configurable provider and Brain"""
        self.provider = ai_settings.get_provider()
        self.client = None
        self.gemini_model = None
        
        # Initialize Brain (Multi-Core + Memory)
        print("Initializing AI Brain...")
        self.brain = AgentCore(self)
        
        # Initialize based on provider
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "gemini":
            self._init_gemini()
        
        # Setup base system prompt
        self._setup_system_prompt()
        
    def _init_openai(self):
        """Initialize OpenAI client"""
        api_key = ai_settings.get_api_key("openai")
        
        if not api_key:
            print("WARNING: No OpenAI API key configured")
            print("Set it in Settings > AI Configuration")
            self.client = None
            return
        
        try:
            self.client = OpenAI(api_key=api_key)
            print("Connected to OpenAI API")
        except Exception as e:
            print(f"Error connecting to OpenAI: {e}")
            self.client = None
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        if not GEMINI_AVAILABLE:
            print("ERROR: Google Generative AI not installed")
            return
        
        api_key = ai_settings.get_api_key("gemini")
        
        if not api_key:
            print("WARNING: No Gemini API key configured")
            print("Set it in Settings > AI Configuration")
            return
        
        try:
            genai.configure(api_key=api_key)
            model_name = ai_settings.get_model("gemini")
            self.gemini_model = genai.GenerativeModel(model_name)
            self.client = True  # Just flag that it's configured
            print(f"Connected to Google Gemini API ({model_name})")
        except Exception as e:
            print(f"Error connecting to Gemini: {e}")
            self.gemini_model = None
    
    def _setup_system_prompt(self):
        """Setup system prompt"""
        user_home = os.path.expanduser("~")
        desktop_path = os.path.join(user_home, "Desktop")
        
        self.base_prompt = f"""You are AI Fervv, an elite software engineer and system architect.
Your goal is to actively create and modify code.

ENVIRONMENT:
- User: {os.path.basename(user_home)}
- Desktop: {desktop_path}
- Home: {user_home}

TOOLS (use in responses):
[[CREATE:filename.ext]]
...file content...
[[/CREATE]]

[[EXEC:command]]

[[REFACTOR:filename.ext]]
...refactored code...
[[/REFACTOR]]

Write clean, well-commented code following best practices.
"""

    def generate_response(self, user_input, context=None):
        """Generate AI response using the Brain (AgentCore)"""
        if not self.client and not self.gemini_model:
            return "ERROR: No AI provider configured. Please set API key in Settings."
        
        # The Brain decides which core to use and how to process
        return self.brain.process(user_input, context)

    def generate_with_core(self, user_input, core_system_prompt):
        """Called by AgentCore to generate actual text using the provider"""
        
        # Combine base prompt with core personality
        full_system = self.base_prompt + "\n\n" + core_system_prompt
        
        try:
            if self.provider == "openai":
                return self._generate_openai(user_input, full_system)
            elif self.provider == "gemini":
                return self._generate_gemini(user_input, full_system)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_openai(self, user_input, system_prompt):
        """Generate response using OpenAI"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        completion = self.client.chat.completions.create(
            model=ai_settings.get_model("openai"),
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )
        
        return completion.choices[0].message.content
    
    def _generate_gemini(self, user_input, system_prompt):
        """Generate response using Google Gemini"""
        full_prompt = system_prompt + "\n\n" + user_input
        response = self.gemini_model.generate_content(full_prompt)
        return response.text
    
    def switch_provider(self, provider):
        """Switch AI provider"""
        if provider in ["openai", "gemini"]:
            self.provider = provider
            ai_settings.set_provider(provider)
            if provider == "openai":
                self._init_openai()
            else:
                self._init_gemini()
            return True
        return False

if __name__ == "__main__":
    print("AI Fervv Agent Test Mode")
    agent = AI_Fervv()
    while True:
        try:
            user_text = input("\nYou: ")
            if user_text.lower() in ['exit', 'quit']:
                break
            print(f"AI: {agent.generate_response(user_text)}")
        except KeyboardInterrupt:
            break