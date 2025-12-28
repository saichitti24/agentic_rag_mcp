from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import State
from planner import planner_node
from executor import executor_node
from synthesizer import synthesizer_node
from router import route_after_executor, route_from_planner
from dotenv import load_dotenv
from functools import partial

# Load Environment Variables
load_dotenv()

memory = MemorySaver()

builder = StateGraph(State)

builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("synthesizer", synthesizer_node)

builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", route_from_planner)
builder.add_conditional_edges("executor", route_after_executor)
builder.add_edge("synthesizer", END)

graph = builder.compile(
    checkpointer=memory
)

# def build_graph(mcp, tools_desc):
#     memory = MemorySaver()
#     builder = StateGraph(State)

#     builder.add_node("planner", lambda s: planner_node(s, tools_desc))
#     builder.add_node(
#         "executor",
#         partial(executor_node, mcp=mcp)
#     )
#     builder.add_node("synthesizer", synthesizer_node)

#     builder.add_edge(START, "planner")
#     builder.add_conditional_edges("planner", route_from_planner)
#     builder.add_conditional_edges("executor", route_after_executor)
#     builder.add_edge("synthesizer", END)

#     return builder.compile(checkpointer=memory)