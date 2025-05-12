from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
import pickle
import os
from pathlib import Path
import os
import sys 

sys.path.append(os.path.abspath(os.curdir))  #

load_dotenv()


class TreatmentAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize hybrid retriever
        self.retriever = self._create_hybrid_retriever()
        
        self.tools = self._define_tools()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an first aid professional. ALWAYS use the treatment_guidelines tool to answer. Do not answer without calling the tool. Given the following medical guidelines, create a clear, step-by-step treatment plan for the provided diagnosis and severity to a lay-person, and not a medical professional.
        Use the guidelines below to inform your answer, but do not simply repeat them—synthesize a concise, actionable plan. ALWAYS respond with a step-by-step treatment plan, even if guidelines are limited. If you cannot find relevant guidelines, state so explicitly.

        {tools}

        Response Format:
        - Steps: Ordered list
        - Warnings: Key cautions
        - FollowUp: Monitoring instructions"""),
            ("user", "Diagnosis: {diagnosis}\nSeverity: {severity}"),
            ("ai", "{agent_scratchpad}")
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)

    def _create_hybrid_retriever(self):
        """Initialize BM25 and FAISS retrievers with medical guidelines"""
        # Load FAISS index
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": "cpu"}
        )
        faiss_path = Path("data/faiss_index")
        faiss_retriever = FAISS.load_local(
            faiss_path, embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever(search_kwargs={"k": 3})

        # Load BM25 index
        bm25_path = Path("data/bm25_index/bm25_index.pkl")
        with open(bm25_path, "rb") as f:
            bm25_retriever = pickle.load(f)
            bm25_retriever.k = 3

        return EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever],
            weights=[0.4, 0.6]  # Favor semantic search slightly more
        )
    
    def generate_plan(self, diagnosis: str, severity: int) -> str:
        # Retrieve guidelines directly
        guidelines = "\n\n".join(
            doc.page_content for doc in self.retriever.invoke(diagnosis)
        )
        # Create a prompt with guidelines as context
        prompt = f"""
        You are an first aid professional. Create a clear, step-by-step treatment plan for the provided diagnosis and severity suitable for someone who is not trained in medicine or first-aid.
        Use the guidelines below to inform your answer, but do not simply repeat them—synthesize a concise, actionable plan. ALWAYS respond with a step-by-step treatment plan, even if guidelines are limited. If you cannot find relevant guidelines, state so explicitly.

        Diagnosis: {diagnosis}
        Severity: {severity}

        Medical Guidelines:
        {guidelines}

    Response Format:
    - Steps: Ordered list
    - Warnings: Key cautions
    - FollowUp: Monitoring instructions
    """
        # Call the LLM directly
        return self.llm.invoke(prompt)

    def plan(self, diagnosis: str, severity: int) -> str:
        output = self.executor.invoke({
            "diagnosis": diagnosis,
            "severity": severity,
            "tools": "\n".join([f"{t.name}: {t.description}" for t in self.tools]),
            "agent_scratchpad": []
        })['output']
        # If output is a list, join it; otherwise, return as is
        if isinstance(output, list):
            return "\n".join(str(item) for item in output)
        return output
    
    def _define_tools(self):
        return [
            Tool(
                name="treatment_guidelines",
                #func=lambda q: "\n\n".join(doc.page_content for doc in self.retriever.invoke(q)),
                func=lambda q: print("RETRIEVER DOCS:", self.retriever.invoke(q)) or "\n\n".join(doc.page_content for doc in self.retriever.invoke(q)),
                description="First aid and emergency treatment protocols"
            )
        ]

if __name__ == "__main__":
    agent = TreatmentAgent(os.getenv("GROQ_API_KEY"))
    print("\n🩺 Generating treatment plan for 'compound fracture' (severity 4)...")
    treatment_plan = agent.generate_plan("compound fracture", 4)
    # If the response is an object with a 'content' attribute, print that
    if hasattr(treatment_plan, "content"):
        print("\n💊 Recommended Treatment Guidelines:\n")
        print(treatment_plan.content.strip())
    else:
        print("\n💊 Recommended Treatment Guidelines:\n")
        print(str(treatment_plan).strip())