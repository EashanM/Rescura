from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="llama3-70b-8192",  # or "llama3-8b-8192"
    temperature=0.2,
    max_tokens=512
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a first aid assistant."),
    ("user", "How do I treat a snake bite in the wilderness?")
])

response = llm.invoke(prompt.format())
print(response.content)
