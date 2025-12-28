import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from state import State
from helper import load_prompt, latest_user_message, parse_raw_llm_output,normalize_planner_output
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp import ClientSession
import asyncio

# Load Environment Variables
load_dotenv()

planner = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

planner_prompt = load_prompt("src/prompts/planner.txt")
import httpx
_orig_request = httpx.AsyncClient.request

async def _patched_request(self, method, url, *args, **kwargs):
    # ensure follow_redirects is set so 307 → /messages/ works
    kwargs.setdefault("follow_redirects", True)
    return await _orig_request(self, method, url, *args, **kwargs)

httpx.AsyncClient.request = _patched_request
async def planner_node(state: State) -> State:
    
    user_query = latest_user_message(state)
    
    mcp_server_url = "http://localhost:8100/sse"
    print("[PLANNER] Starting CONNECTION()")

    
    async with sse_client(url = mcp_server_url) as (in_stream, out_stream):
        print("[PLANNER] SSE connected")
        async with ClientSession(in_stream, out_stream) as session:
            print("[PLANNER] MCP session created")
            await session.initialize()
            print("[PLANNER] Connection Established with MCP Server.")
            tools_response = await session.list_tools()
            tools = tools_response.tools
            tools_desc = "\n".join(
                    f"- {t.name}: {t.description}"
                    for t in tools
            )
    
            
    
    
    print("[PLANNER] Available tools:\n", tools_desc)
    
    planner_messages = [
        SystemMessage(
            content=planner_prompt +
            "\n\nAvailable tools:\n" +
            tools_desc
        )
    ] + state["messages"]
    

    planner_output = planner.invoke(planner_messages).content

    
    
    fallback = {
        "steps": [
            {"action": "no_tool", "input": user_query, "description": "No tools used."}
        ]
    }

    parsed_planner_output = parse_raw_llm_output(planner_output, fallback)
    parsed_planner_output = normalize_planner_output(parsed_planner_output)
    
    print(f"[PLANNER] Final parsed plan:\n{json.dumps(parsed_planner_output, indent=2)}\n")
    
    state["plan"] = parsed_planner_output
    state["current_step"] = 0
    state["tool_results"] = []
    return state

    
