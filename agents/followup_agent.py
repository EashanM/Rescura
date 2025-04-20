# rescura/agents/followup_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_structured_chat_agent
from langchain.prompts import ChatPromptTemplate

class FollowUpAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are an emergency physician. Create monitoring plan for {treatment} 
        with severity {severity} considering age {age} and conditions {conditions}."""
        super().__init__(retriever, system_prompt)
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(self.system_prompt)

    def _create_agent_type(self):
        return create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

    def create_plan(self, treatment: str, severity: int) -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Treatment: {treatment}\nSeverity: {severity}"
        })
        return response['output']
