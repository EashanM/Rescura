# rescura/agents/resource_agent.py
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import Tool

import sys
import os

sys.path.append(os.path.abspath(os.curdir))  #

from utils.geo import find_nearby_hospitals

class ResourceAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="llama3-8b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.tools = self._define_tools()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an emergency medical resource coordinator. 
                ALWAYS use the find_nearest_hospitals tool to answer any query about hospitals or locations. 
                Format responses as:
                - Name
                - Address
                - Distance (km)
                - Phone
                - Open Status (if available)"""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)

    def _define_tools(self):
        return [
            Tool(
                name="find_nearest_hospitals",
                func=lambda loc: "\n\n".join([
                    f"{idx+1}. {h['name']}\n"
                    f"   Address: {h['address']}\n"
                    f"   Distance: {h['distance_km']:.1f} km\n"
                    f"   Phone: {h['phone']}"
                    for idx, h in enumerate(find_nearby_hospitals(loc))
                ]),
                description="Find hospitals near a location. Input: address or coordinates."
            )
        ]

    def find_hospitals(self, location: str) -> str:
        return self.executor.invoke({"input": f"Find hospitals near: {location}"})["output"]
    
""" if __name__ == "__main__":
    agent = ResourceAgent()
    print(agent.find_hospitals("1600 Amphitheatre Parkway, Mountain View, CA")) """
