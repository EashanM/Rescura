from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage
import json
import re
from dotenv import load_dotenv
from langchain.tools import Tool
import os 
import sys 
sys.path.append(os.path.abspath(os.curdir))


load_dotenv()

class TriageAgent:
    def __init__(self, retriever, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.retriever = retriever
        self.tools = self._define_tools()
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an emergency medical triage specialist talking to someone without medical training. Assess severity from 1-5.
        Available Tools: {tools}
        Tool Names: {tool_names}

        If you are NOT confident in your diagnosis, ask a clear, concise follow-up question to get more information from the user. 
        Only provide a final answer (as JSON with 'severity', 'diagnosis', and 'rationale') when you are confident, or it appears that the user is not able to provide more information.
        Furthermore, speed is very important so make sure to ask the most relevant follow-up questions first and to report a final answer as soon as you can.
             
        If you have asked 4 follow-up questions and still lack confidence, make your best clinical judgment and provide a final answer in the required JSON format.

        Use format:
        Thought: {agent_scratchpad}
        If unsure: Question: <your follow-up question>
        If confident: Final Answer: JSON with 'severity' (1-5), 'diagnosis' (short clinical term), and 'rationale'
        """),
            ("user", "{input}"),
            ("ai", "{agent_scratchpad}"),
        ])
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False, handle_parse_errors=True)

    def _define_tools(self):
        return [
            Tool(
                name="medical_guidelines",
                func=lambda q: [doc.page_content for doc in self.retriever.invoke(q)],
                description="Access medical guidelines and protocols"
            )
        ]

    def assess(self, symptoms: str) -> dict:
        try:
            response = self.executor.invoke({
                "input": f"Symptoms: {symptoms}",
                "tools": "\n".join([f"{t.name}: {t.description}" for t in self.tools]),
                "tool_names": ", ".join([t.name for t in self.tools]),
                "agent_scratchpad": []
            })
            return self._parse_response(response['output'])
        except Exception as e:
            # Try to extract a follow-up question from the exception message
            raw = str(e)
            question_match = re.search(r'Question:\s*(.+)', raw)
            if question_match:
                return {"follow_up": question_match.group(1).strip()}
            # Otherwise, return the error
            return {"error": "Agent error", "raw": raw}

    def _parse_response(self, raw: str) -> dict:
        # Check for a follow-up question
        question_match = re.search(r'Question:\s*(.+)', raw)
        if question_match:
            return {"follow_up": question_match.group(1).strip()}
        # Check for a final answer
        final_match = re.search(r'Final Answer:\s*(\{.*?\})', raw, re.DOTALL)
        if final_match:
            try:
                return json.loads(final_match.group(1))
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw": raw}
        # If neither, return the raw output as a message
        return {"message": raw.strip()}

if __name__ == "__main__":
    # Example usage for conversational triage
    retriever = FAISS.load_local("data/faiss_index", None, allow_dangerous_deserialization=True)  # Adjust as needed
    agent = TriageAgent(retriever, groq_api_key="GROQ_API_KEY")
    
    conversation = input("Describe the emergency situation: ").strip()
    followup_count = 0
    while True:
        try:
            result = agent.assess(conversation)
        except Exception as e:
            print("Agent error:", e)
            break
        if "follow_up" in result:
            followup_count += 1
            print("Rescura: " + result["follow_up"])
            user_reply = input("You: ").strip()
            conversation += " " + user_reply
            if followup_count >= 4:
                conversation += (
                    " You have now asked 4 follow-up questions. "
                    "Please provide your best clinical judgment and a final answer in the required JSON format."
                )
        elif "error" in result:
            print("Error:", result["error"])
            print("Raw output:", result.get("raw", ""))
            break
        elif "message" in result:
            print("Rescura:", result["message"])
            break
        else:
            print("\nRescura confident triage result:")
            print(result)
            break