import asyncio
from graph import graph
from dotenv import load_dotenv

from mcp.client.sse import sse_client
from mcp import ClientSession

# Load Environment Variables
load_dotenv()
import httpx
_orig_request = httpx.AsyncClient.request

async def _patched_request(self, method, url, *args, **kwargs):
    # ensure follow_redirects is set so 307 → /messages/ works
    kwargs.setdefault("follow_redirects", True)
    return await _orig_request(self, method, url, *args, **kwargs)

httpx.AsyncClient.request = _patched_request


# async def main():
#     mcp_server_url = "http://localhost:3333/sse"
#     print("[DEBUG] Starting main()")

    
#     async with sse_client(url = mcp_server_url) as (in_stream, out_stream):
#         print("[DEBUG] SSE connected")

#         async with ClientSession(in_stream, out_stream) as session:
#             print("[DEBUG] MCP session created")
#             await session.initialize()
#             print("[MAIN] Connection Established with MCP Server.", session.serverInfo.name)
                
#             tools_response = await session.list_tools()
#             tools = tools_response.tools
#             tools_desc = "\n".join(
#                     f"- {t.name}: {t.description}"
#                     for t in tools
#             )
    
#             print("[MAIN] Tools Description:\n", tools_desc)
                
#             graph = build_graph(session, tools_desc)
                
#             thread_id = "mcp-test-1"
    
#             await chat_in_loop(graph, thread_id)
                
    
    
    
    
    
    
    
    
    
    

async def chat_in_loop(thread_id: str = "mcp-test-1"):
    """
    Multi-turn CLI chat loop.
    """
    print("\nAgentic RAG: Planner - Executor - Synthesizer")
    print(f"Using thread_id = {thread_id!r}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit", "stop"}:
            print("Goodbye!")
            break

        print("\n[DEBUG] ===== Invoking graph for this turn =====")

        result = await graph.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            },
        )

        print("[DEBUG] ===== Graph invocation finished =====\n")

        final_reply = result["messages"][-1].content
        print("Assistant:", final_reply, "\n")


# asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(chat_in_loop())