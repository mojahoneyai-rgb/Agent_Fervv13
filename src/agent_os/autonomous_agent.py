"""
Autonomous Agent
The breakdown of the AI into a Kernel-aware entity.
"""
from src.agent_os.tools import AgentTools
from src.core.kernel.kernel import kernel

class AutonomousAgent:
    def __init__(self, ai_service):
        self.ai = ai_service
        self.tools = AgentTools()

    def think_and_act(self, goal):
        """
        The Core Loop:
        1. Think (Plan)
        2. Act (Tool Call)
        3. Observe (Result)
        4. Loop
        """
        # 1. Construct System Prompt with Tool Definitions
        tool_defs = self.tools.get_tool_definitions()
        system_prompt = f"""
        You are an Autonomous AI Developer.
        You have access to the following Kernel Tools:
        {tool_defs}
        
        To use a tool, output a block like:
        [[TOOL_CALL]]
        name: tool_name
        args: {{ "arg": "value" }}
        [[/TOOL_CALL]]
        
        Goal: {goal}
        """
        
        # 2. Get AI Response
        response = self.ai.generate_raw(goal, system_prompt=system_prompt)
        
        # 3. Parse Tool Call (Simple Parser)
        if "[[TOOL_CALL]]" in response:
            try:
                block = response.split("[[TOOL_CALL]]")[1].split("[[/TOOL_CALL]]")[0].strip()
                # Extremely naive parsing for demo purposes
                # In production we'd use JSON parsing or a robust regex
                lines = block.split("\n")
                tool_name = lines[0].split(":")[1].strip()
                # args parsing todo
                
                # Execute (Mock)
                return f"Agent attempted to call {tool_name}. (Parsing Logic Pending)"
            except:
                return "Agent failed to parse tool call."
        
        return response

