# rescura/retrieval/build_index.py
import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_documents(directory: Path) -> list:
    """Load and split PDF documents from a directory"""
    documents = []
    
    if not directory.exists():
        logger.warning(f"Directory {directory} does not exist, skipping...")
        return documents

    for pdf_file in directory.glob("*.pdf"):
        try:
            logger.info(f"Processing {pdf_file.name}...")
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            logger.error(f"Failed to process {pdf_file}: {str(e)}")
    
    return documents

def process_documents() -> list:
    """Process all documents from data directories"""
    base_dir = Path("data")
    directories = [
        base_dir / "first_aid_manuals",
        base_dir / "disaster_guides",
        base_dir / "wilderness_guides"
    ]
    
    all_docs = []
    for directory in directories:
        logger.info(f"Loading documents from {directory}...")
        docs = load_documents(directory)
        all_docs.extend(docs)
        logger.info(f"Loaded {len(docs)} documents from {directory}")
    
    if not all_docs:
        logger.warning("No documents found in any directories!")
        return []
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return text_splitter.split_documents(all_docs)

def build_and_save_index(chunks: list):
    """Build FAISS index and save to disk"""
    if not chunks:
        logger.error("No document chunks to process!")
        return
    
    logger.info("Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"}  # Use "cuda" if you have GPU
    )
    
    logger.info("Building FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    output_dir = Path("data/faiss_index")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving index to {output_dir}...")
    vector_store.save_local(str(output_dir))
    logger.info("Index built and saved successfully!")

if __name__ == "__main__":
    logger.info("Starting FAISS index generation...")
    chunks = process_documents()
    
    if chunks:
        logger.info(f"Processing {len(chunks)} document chunks")
        build_and_save_index(chunks)
    else:
        logger.error("No documents processed, exiting...")
