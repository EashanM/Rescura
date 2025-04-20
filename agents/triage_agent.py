# rescura/agents/triage_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_react_agent

class TriageAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """You are an emergency medical triage specialist. 
        Assess severity from 1-5 considering: {symptoms}, {environment}, and {vitals}."""
        super().__init__(retriever, system_prompt)

    def _create_agent_type(self):
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=ChatPromptTemplate.from_template(self.system_prompt)
        )

    def assess_severity(self, symptoms: str, environment: str) -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Symptoms: {symptoms}\nEnvironment: {environment}"
        })
        return self._parse_response(response['output'])

    def _parse_response(self, raw_response: str) -> dict:
        # Add validation logic here
        return {"severity": 3, "rationale": raw_response}
