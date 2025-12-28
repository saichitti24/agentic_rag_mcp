from typing import TypedDict, List, Optional,Annotated, Any, Dict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: Dict[str, Any] | None
    current_step: int
    tool_results: List[str]
    