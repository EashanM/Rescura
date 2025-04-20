# rescura/agents/prevention_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_json_chat_agent

class PreventionAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are a preventive medicine expert. Suggest risk mitigation strategies for {incident_type} 
        in {environment} considering {history}."""
        super().__init__(retriever, system_prompt)

    def _create_agent_type(self):
        return create_json_chat_agent(self.llm, self.tools, self.prompt)

    def suggest_prevention(self, incident_type: str, environment: str) -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Incident: {incident_type}\nEnvironment: {environment}"
        })
        return response['output']
