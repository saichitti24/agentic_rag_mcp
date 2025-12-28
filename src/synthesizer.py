from langchain_core.messages import SystemMessage, HumanMessage
from helper import load_prompt, latest_user_message
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from state import State

# Load Environment Variables
load_dotenv()


synthesizer = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

synthesizer_prompt = load_prompt("src/prompts/synthesizer.txt")

def synthesizer_node(state: State) -> State:
    
    user_query = latest_user_message(state)
    
    plan = state.get("plan") or {}
    steps = plan.get("steps", [])
    tool_results = state.get("tool_results", [])
    
    # Build a readable summary for the LLM
    steps_with_results = []
    for idx, step in enumerate(steps):
        result_text = tool_results[idx] if idx < len(tool_results) else ""
        steps_with_results.append(
            f"Step {idx+1}: action={step['action']}, input={step['input']}\n"
            f"  description: {step.get('description','')}\n"
            f"  result: {result_text[:500]}\n"
        )

    planning_trace = "\n".join(steps_with_results) if steps_with_results else "No external steps were executed."
    
    messages = [
        SystemMessage(content=synthesizer_prompt),
    ] + state["messages"] + [
        HumanMessage(content=f"User query: {user_query}"),
        HumanMessage(content=f"Planning & tool execution trace:\n{planning_trace}")
    ]
    
    answer = synthesizer.invoke(messages).content
    
    state["messages"] = add_messages(
        state["messages"],
        {"role": "assistant", "content": answer},
    )
    
    state["plan"] = None
    state["tool_results"] = []
    state["current_step"] = 0

    return state