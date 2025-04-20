# rescura/agents/treatment_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_tool_calling_agent

class TreatmentAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are a certified first aid instructor. Provide step-by-step instructions for {emergency_type} 
        considering resources: {resources} and environment: {environment}."""
        super().__init__(retriever, system_prompt)

    def _create_agent_type(self):
        return create_tool_calling_agent(self.llm, self.tools, self.prompt)

    def generate_treatment_plan(self, emergency_type: str, context: dict) -> str:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Emergency: {emergency_type}\nContext: {context}"
        })
        return response['output']
