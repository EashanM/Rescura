# rescura/agents/resource_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_openai_tools_agent

class ResourceAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are an emergency resource coordinator. Find {resource_type} 
        in {location} considering {alerts}."""
        super().__init__(retriever, system_prompt)
        self.tools += [
            # Add API tools here
        ]

    def _create_agent_type(self):
        return create_openai_tools_agent(self.llm, self.tools, self.prompt)

    def find_resources(self, resource_type: str, location: str) -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Resource: {resource_type}\nLocation: {location}"
        })
        return response['output']
