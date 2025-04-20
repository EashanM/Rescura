# rescura/agents/base_agent.py
from langchain.agents import AgentExecutor, Tool
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

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
        """Define tools available to all agents"""
        return [
            Tool(
                name="MedicalKnowledgeRetrieval",
                func=self._retrieve_context,
                description="Access medical manuals and first aid guidelines"
            )
        ]

    def _retrieve_context(self, query: str) -> ToolMessage:
        """Return tool responses as proper ToolMessage objects"""
        docs = self.retriever.get_relevant_documents(query)
        return ToolMessage(
            content="\n".join([doc.page_content for doc in docs]),
            tool_call_id="context_retrieval_123"  # Unique ID for tracking
        )

    def create_agent_executor(self) -> AgentExecutor:
        return AgentExecutor(
        agent=self._create_agent_type(),
        tools=self.tools,
        prompt=self.prompt.partial(
            tools="\n".join([f"{t.name}: {t.description}" for t in self.tools]),
            tool_names=", ".join([t.name for t in self.tools])
        ),
        verbose=True
    )

    def _create_agent_type(self):
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")
