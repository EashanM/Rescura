# rescura/agents/base_agent.py
from langchain.agents import AgentExecutor, Tool
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from typing import List, Optional

class BaseRescuraAgent:
    def __init__(self, retriever, system_prompt: str):
        self.llm = ChatGroq(
            temperature=0.2,
            model_name="llama3-70b-8192",
            max_tokens=1024
        )
        self.retriever = retriever
        self.system_prompt = system_prompt
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Tool]:
        return [
            Tool(
                name="KnowledgeBase",
                func=self._retrieve_context,
                description="Access first aid manuals and disaster guidelines"
            )
        ]

    def _retrieve_context(self, query: str) -> str:
        return "\n".join([doc.page_content for doc in self.retriever.get_relevant_documents(query)])

    def create_agent_executor(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        
        return AgentExecutor(
            agent=self._create_agent_type(),
            tools=self.tools,
            prompt=prompt,
            verbose=True
        )

    def _create_agent_type(self):
        raise NotImplementedError("Subclasses must implement this method")
