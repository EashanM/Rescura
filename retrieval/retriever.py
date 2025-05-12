# rescura/retrieval/retriever.py
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

class RescuraRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.vector_store = FAISS.load_local(
            "data/faiss_index", 
            self.embeddings,
            allow_dangerous_deserialization=True  
        )
    
    def get_relevant_documents(self, query: str, k=3):
        return self.vector_store.similarity_search(query, k=k)
    
    @classmethod
    def build_index(cls, pdf_directory: str):
        loaders = [PyPDFLoader(pdf) for pdf in Path(pdf_directory).glob("*.pdf")]
        docs = [doc for loader in loaders for doc in loader.load()]
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        chunks = splitter.split_documents(docs)
        vector_store = FAISS.from_documents(chunks, cls().embeddings)
        vector_store.save_local("data/faiss_index")
