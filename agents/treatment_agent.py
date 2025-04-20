from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()


class TreatmentAgent:
    def __init__(self, retriever, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="llama3-70b-8192", 
            api_key=groq_api_key
        )
        self.retriever = retriever
        self.tools = self._define_tools()
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an emergency physician. Create treatment plan.
            Available Tools: {tools}
            
            Response Format:
            - Steps: Ordered list
            - Warnings: Key cautions
            - FollowUp: Monitoring instructions"""),
            ("user", "Diagnosis: {diagnosis}\nSeverity: {severity}")
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def _define_tools(self):
        return [{
            "name": "treatment_guidelines",
            "func": lambda q: self.retriever.similarity_search(q, k=3),
            "description": "First aid and emergency treatment protocols"
        }]

    def plan(self, diagnosis: str, severity: int) -> str:
        return self.executor.invoke({
            "diagnosis": diagnosis,
            "severity": severity
        })['output']
