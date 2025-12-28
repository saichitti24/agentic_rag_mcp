from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

from zoneinfo import ZoneInfo
from fastapi import FastAPI

import requests
from starlette.applications import Starlette
from starlette.routing import Route, Mount




# Load Environment Variables
load_dotenv()

CHROMA_DIR = "chromaDB"

def load_chroma_retriever(k: int = 3):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )

    return vector_store.as_retriever(
        search_kwargs={"k": k}
    )



# Create FastMCP server
mcp = FastMCP("agentic-rag-mcp")




retriever = load_chroma_retriever(k=3)
google = GoogleSearchAPIWrapper()


@mcp.tool()
async def local_rag(query: str) -> str:
    """
    Perform a local retrieval augmented generation (RAG) using a vector store retriever,
    if the user query is related to personal choices, preferences or specific knowledge related to movies, technical concepts technical concepts related to computer science, technology, software engineering etc.
    and return the top 3 relevant documents with formatted results.
    
    """
    
    try:
        result_docs = retriever.invoke(query)
        if not result_docs:
            return "[LOCAL RAG] No results."
           
           
        final_parsed_result_docs = "[LOCAL RAG]\n" + "\n\n".join(doc.page_content for doc in result_docs)
        return final_parsed_result_docs
        
         
    except Exception as e:
        return f"[LOCAL RAG ERROR] {e}"
    
       

@mcp.tool()
async def google_search(query:str) -> str:
    """
    Perform a Google Search when the user query is related to a general fact and not present in the local knowledge base,
    and return the top 5 results formatted with title, snippet, and URL.
    
    """
    try:
        results = google.results(query, num_results=5)
        if not results:
            return "[GOOGLE SEARCH] No results found."
            
        
        
        lines = []
        for r in results:
            lines.append(
                f"TITLE: {r.get('title')}\n"
                f"SNIPPET: {r.get('snippet')}\n"
                f"URL: {r.get('link')}\n"
                    "---"
            )
            
        final_parsed_results = "[GOOGLE SEARCH]\n" + "\n".join(lines)
            
    except Exception as e:
        return f"[GOOGLE SEARCH] Error during search: {e}"
    
        
    return final_parsed_results
    


transport = SseServerTransport("/messages/")
        
async def handle_sse(request):
    # Prepare bidirectional streams over SSE
    async with transport.connect_sse(
        request.scope,
        request.receive,
        request._send
    ) as (in_stream, out_stream):
        # Run the MCP server: read JSON-RPC from in_stream, write replies to out_stream
        await mcp._mcp_server.run(
            in_stream,
            out_stream,
            mcp._mcp_server.create_initialization_options()
        )
        
sse_app = Starlette(
    routes=[
        Route("/sse", handle_sse, methods=["GET"]),
        # Note the trailing slash to avoid 307 redirects
        Mount("/messages/", app=transport.handle_post_message)
    ]
)


app = FastAPI()
app.mount("/", sse_app)

@app.get("/health")
def read_root():
    return {"message": "MCP SSE Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)

