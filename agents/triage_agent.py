from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage
import json
import re
from dotenv import load_dotenv

load_dotenv()


class TriageAgent:
    def __init__(self, retriever, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0.2,
            model_name="llama3-70b-8192",
            api_key=groq_api_key
        )
        self.retriever = retriever
        self.tools = self._define_tools()
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an emergency medical triage specialist. Assess severity from 1-5.
            Available Tools: {tools}
            Tool Names: {tool_names}
            
            Use format:
            Thought: {agent_scratchpad}
            Final Answer: JSON with 'severity' (1-5) and 'rationale'"""),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def _define_tools(self):
        return [{
            "name": "medical_guidelines",
            "func": lambda q: [doc.page_content for doc in self.retriever.invoke(q)],
            "description": "Access medical guidelines and protocols"
        }]

    def assess(self, symptoms: str) -> dict:
        response = self.executor.invoke({
            "input": f"Symptoms: {symptoms}",
            "agent_scratchpad": []
        })
        return self._parse_response(response['output'])

    def _parse_response(self, raw: str) -> dict:
        try:
            json_str = re.search(r'\{.*?\}', raw, re.DOTALL).group()
            return json.loads(json_str)
        except (AttributeError, json.JSONDecodeError):
            return {"error": "Failed to parse response", "raw": raw}
