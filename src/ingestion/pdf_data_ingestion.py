import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv


# Load Environment Variables
load_dotenv()

# Input and output directories
PDF_DIR = "data/pdfs"
CHROMA_DIR = "chromaDB"

def load_all_pdfs(pdf_dir: str):
    docs = []
    for root, _, files in os.walk(pdf_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                path = os.path.join(root, f)
                print(f"[INGEST] File identified: {path}")
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
    return docs

def ingest_pdfs_to_chroma():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    docs = load_all_pdfs(PDF_DIR)
    
    if not docs:
        raise ValueError("No PDFs found in data/pdfs")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    
    chunks = splitter.split_documents(docs)
    
    return chunks, embeddings
    
def create_vector_store(chunks, embeddings):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_store
    
def get_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={"k": 3} 
    )

if __name__ == "__main__":
    chunks, embeddings = ingest_pdfs_to_chroma()
    vector_store = create_vector_store(chunks, embeddings)
    retriever = get_retriever(vector_store)