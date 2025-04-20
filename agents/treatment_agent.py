# rescura/agents/treatment_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class TreatmentAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are a certified first aid instructor. Provide step-by-step instructions for {emergency_type} 
        considering resources: {resources} and environment: {environment}."""

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])

        super().__init__(retriever, system_prompt)

    def _create_agent_type(self):
        return create_tool_calling_agent(self.llm, self.tools, self.prompt)

    def generate_treatment_plan(self, emergency_type: str, context: dict) -> str:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Emergency: {emergency_type}\nContext: {context}",
            "emergency_type": emergency_type,
            "environment": context.get("environment", ""),
            "resources": context.get("resources", ""),
            "agent_scratchpad": []
        })
        
        return response['output']
