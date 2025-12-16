"""
AI Service & Reasoning Engine
Handles interaction with OpenAI, Gemini, and implements "Chain-of-Thought".
"""
import threading
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from src.core.container import get_service

class ReasoningEngine:
    def __init__(self, ai_service):
        self.ai = ai_service

    def think(self, user_input, context=None):
        """Execute Chain-of-Thought processing"""
        # 1. Thought Generation
        thought_prompt = f"""
        Analyze the following user request. 
        Determine the intent (coding, explanation, system command).
        Formulate a plan.
        
        User Request: {user_input}
        
        Output format:
        [[THOUGHT]]
        ...analysis...
        [[/THOUGHT]]
        [[PLAN]]
        ...steps...
        [[/PLAN]]
        """
        # In a real "1000x" system, we'd run this against a fast model (e.g., gpt-3.5-turbo)
        # For now, we simulate or execute if desired.
        
        # 2. Execution
        response = self.ai.generate_raw(user_input, system_prompt="You are an expert AI.")
        return response

class AIService:
    def __init__(self):
        self.provider = "openai"
        self.openai_client = None
        self.gemini_model = None
        self.reasoning = ReasoningEngine(self)

    def initialize(self):
        config = get_service("ConfigService")
        self.provider = config.get("provider", "openai")
        self._init_provider()

    def _init_provider(self):
        config = get_service("ConfigService")
        if self.provider == "openai":
            key = config.get("openai_key")
            if key and OpenAI:
                self.openai_client = OpenAI(api_key=key)
        elif self.provider == "gemini":
            key = config.get("gemini_key")
            if key and genai:
                genai.configure(api_key=key)
                model_name = config.get("gemini_model", "gemini-pro")
                self.gemini_model = genai.GenerativeModel(model_name)

    def switch_provider(self, provider):
        self.provider = provider
        self._init_provider()

    from src.core.event_bus import global_event_bus

    def generate_async(self, prompt, system_prompt=""):
        """Non-blocking generation"""
        thread = threading.Thread(target=self._run_async, args=(prompt, system_prompt))
        thread.daemon = True
        thread.start()

    def _run_async(self, prompt, system_prompt=""):
        response = self.generate(prompt, system_prompt)
        global_event_bus.publish("ai_response_ready", response)

    def generate(self, prompt, system_prompt=""):
        """High-level generate method (invokes Reasoning/CoT)"""
        return self.reasoning.think(prompt)

    def generate_raw(self, prompt, system_prompt=""):
        """Direct API call"""
        if self.provider == "openai" and self.openai_client:
            try:
                config = get_service("ConfigService")
                model = config.get("openai_model", "gpt-4o")
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI Error: {e}"
                
        elif self.provider == "gemini" and self.gemini_model:
            try:
                full_prompt = system_prompt + "\n\n" + prompt
                response = self.gemini_model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                return f"Gemini Error: {e}"
        
        return "AI Provider not configured or unavailable."
