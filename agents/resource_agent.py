# rescura/agents/resource_agent.py
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()



class ResourceAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="llama3-8b-8192",
            api_key=groq_api_key
        )
        
        self.tools = self._define_tools()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a medical resource coordinator. Find:
            - Hospitals
            - Pharmacies
            - Emergency services
            
            Response Format:
            - Name
            - Address
            - Distance
            - Contact"""),
            ("user", "Location: {location}\nResource: {resource_type}")
        ])
        
        self.agent = create_structured_chat_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def _define_tools(self):
        return [{
            "name": "geo_search",
            "func": lambda loc: ["Hospital A (1mi)", "Clinic B (2mi)"],  # Replace with real API
            "description": "Find locations near coordinates/address"
        }]

    def find(self, resource_type: str, location: str) -> list:
        return self.executor.invoke({
            "resource_type": resource_type,
            "location": location
        })['output']