
import asyncio
from state import State
from typing import TypedDict, List, Optional,Annotated, Any, Dict
from mcp.client.sse import sse_client
from mcp import ClientSession

import httpx
_orig_request = httpx.AsyncClient.request

async def _patched_request(self, method, url, *args, **kwargs):
    # ensure follow_redirects is set so 307 → /messages/ works
    kwargs.setdefault("follow_redirects", True)
    return await _orig_request(self, method, url, *args, **kwargs)

httpx.AsyncClient.request = _patched_request




async def executor_node(state: State) -> State:
    
    print("[EXECUTOR NODE] ")
    plan = state.get("plan") or {}
    steps: List[Dict[str, Any]] = plan.get("steps", [])
    idx = state.get("current_step", 0)

    if idx >= len(steps):
        return state

    step = steps[idx]
    action = step["action"]
    tool_input = step.get("input", "")

    

    if action == "no_tool":
        result = "[NO TOOL USED] No external call; rely on conversation context."
    else:
        print("[EXECUTOR NODE] Calling tool:", action, "with input:", tool_input)
        
        mcp_server_url = "http://localhost:8100/sse"
        print("[EXECUTOR] Starting CONNECTION()")


        
        async with sse_client(url = mcp_server_url) as (in_stream, out_stream):
            print("[EXECUTOR] SSE connected")
            async with ClientSession(in_stream, out_stream) as session:
                print("[EXECUTOR] MCP session created")
                await session.initialize()
                response = await session.call_tool(action, {"query": tool_input})
                
                
                result = response.content[0].text
                
                
        
        state["tool_results"].append(result)
        state["current_step"] = idx + 1
            
        
        return state
        
        
        
        
        
        

    

    