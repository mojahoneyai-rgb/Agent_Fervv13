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
        """Execute Chain-of-Thought processing with Memory and Web Search"""
        from src.services.memory_service import MemoryService
        
        # Initialize Memory
        if not hasattr(self, 'memory'):
            self.memory = MemoryService()

        # 1. Check Memory
        memory_context = self.memory.get_context_string(user_input)
        
        # 2. Enhanced Prompt
        thought_prompt = f"""
        You are an advanced AI Agent with access to persistent memory and web search.
        
        User Request: {user_input}
        
        Using Memory Context:
        {memory_context}
        
        First, Analyze if you have enough information to answer. 
        If you are missing critical information about recent events or specific libraries, 
        you should request a SEARCH.
        
        Output one of two formats:
        
        Format 1 (If you need to search):
        [[SEARCH: <query>]]
        
        Format 2 (If you can answer):
        [[THOUGHT]]
        ...your reasoning...
        [[/THOUGHT]]
        [[ANSWER]]
        ...your final response...
        [[/ANSWER]]
        """
        
        # 3. Initial AI Call
        initial_response = self.ai.generate_raw(thought_prompt, system_prompt="You are a smart autonomous agent.")
        
        # 4. Handle Search Intent
        if "[[SEARCH:" in initial_response:
            try:
                # Extract query
                start = initial_response.find("[[SEARCH:") + 9
                end = initial_response.find("]]", start)
                search_query = initial_response[start:end].strip()
                
                # Perform Search
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    results = list(ddgs.text(search_query, max_results=3))
                    
                search_summary = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                
                # Learn (Save to memory)
                self.memory.remember(search_query, search_summary, source="web_search")
                
                # Re-prompt with new knowledge
                final_prompt = f"""
                User Request: {user_input}
                
                New Information found via Search ({search_query}):
                {search_summary}
                
                Memory Context:
                {memory_context}
                
                Now provide a comprehensive answer.
                """
                return self.ai.generate_raw(final_prompt, system_prompt="You are an expert AI with access to real-time data.")
                
            except Exception as e:
                return f"I tried to search for '{search_query}' but failed: {str(e)}. Here is what I know: {initial_response}"

        return initial_response

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
