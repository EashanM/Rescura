# rescura/agents/prevention_agent.py
from .base_agent import BaseRescuraAgent
from langchain.agents import create_json_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class PreventionAgent(BaseRescuraAgent):
    def __init__(self, retriever):
        system_prompt = """
        You are a preventive medicine expert. Suggest risk mitigation strategies for {incident_type} in {environment} considering {history}.
        ALWAYS respond ONLY with a single JSON object in the following format:

        {
        "primary_prevention": [ ... ],
        "secondary_prevention": [ ... ],
        "tertiary_prevention": [ ... ],
        "references": [ ... ]
        }
        Do not include any explanations or markdown, only the JSON object.
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\nAvailable Tools: {tools}\nTool Names: {tool_names}"),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])

        super().__init__(retriever, system_prompt)

    def _create_agent_type(self):
        return create_json_chat_agent(self.llm, self.tools, self.prompt)

    def suggest_prevention(self, incident_type: str, environment: str) -> dict:
        agent_executor = self.create_agent_executor()
        response = agent_executor.invoke({
            "input": f"Incident: {incident_type}\nEnvironment: {environment}",
            "incident_type": incident_type,
            "environment": environment,
            "history": "",
            "tools": "\n".join([f"{t.name}: {t.description}" for t in self.tools]),
            "tool_names": ", ".join([t.name for t in self.tools]),
            "agent_scratchpad": []
        })
        return response['output']
