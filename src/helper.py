import json
from datetime import datetime
from typing import Any, Dict, List
from state import State



def load_prompt(path:str) -> str:
    """Load prompt text from file."""
    with open(path, 'r', encoding="utf-8") as file:
        return file.read()
    
def latest_user_message(state: State) -> str:
    """Get latest user message content."""
    for msg in reversed(state["messages"]):
        if hasattr(msg, "type") and msg.type == "human":
            return msg.content
        if isinstance(msg, dict) and msg.get("role") == "user":
            return msg.get("content", "")
    last = state["messages"][-1]
    return getattr(last, "content", last.get("content", ""))

def parse_raw_llm_output(raw: str, fallback: dict) -> dict:
    parsed_llm_output: Dict[str, Any]
    try:
        raw_stripped = raw.strip()
        if raw_stripped.startswith("```"):
            raw_stripped = raw_stripped.strip("`")
            # After stripping backticks, might have "json\n{...}"
            if raw_stripped.lstrip().lower().startswith("json"):
                raw_stripped = raw_stripped.split("\n", 1)[1]
        parsed_llm_output = json.loads(raw_stripped)
        return parsed_llm_output
    except Exception as e:
        return fallback
    
def normalize_planner_output(plan: dict) -> dict:
    if "steps" not in plan:
        return {"steps": []}
    return plan