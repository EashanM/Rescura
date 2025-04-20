# rescura/agents/triage_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

class TriageAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are an emergency medical triage specialist. 
        Assess severity from 1-5 considering: {input}
        
        Available Tools: {tools}
        Tool Names: {tool_names}

        Use this format:
        Thought: {agent_scratchpad}"""

        # Set up the proper prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        super().__init__(retriever, system_prompt)  # Pass the actual system_prompt

    def _create_agent_type(self):
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt  # Use the instance's prompt
        )

    def assess_emergency(self, symptoms: str, environment: str = "urban") -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Symptoms: {symptoms}\nEnvironment: {environment}",
            "agent_scratchpad": []  # Initialize as empty list
        })
        return self._parse_response(response['output'])
    
    def _parse_response(self, raw_response: str) -> dict:
        """Parse raw LLM response into structured format"""
        # Example parsing logic - implement actual JSON parsing
        try:
            return {
                "severity": int(raw_response.split('"severity":')[1].split(",")[0].strip()),
                "rationale": raw_response.split('"rationale":')[1].split("}")[0].strip().strip('"'),
                "immediate_actions": ["Immobilize limb", "Apply ice"],
                "diagnosis": "Suspected fracture"
            }
        except:
            return {
                "severity": 3,
                "rationale": "Default response - parsing failed",
                "immediate_actions": ["Seek professional medical help"],
                "diagnosis": "Unknown"
            }
