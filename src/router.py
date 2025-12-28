from state import State
from typing import TypedDict, List, Optional,Annotated, Any, Dict

def route_after_executor(state: State) -> str:
    """If there are more steps, go back to executor; else go to synthesizer."""
    plan = state.get("plan") or {}
    steps: List[Dict[str, Any]] = plan.get("steps", [])
    idx = state.get("current_step", 0)

    if idx < len(steps):
        print(f"[ROUTER] More steps remaining ({idx}/{len(steps)}). Looping Executor.")
        return "executor"
    else:
        print(f"[ROUTER] All steps done ({idx}/{len(steps)}). Going to Synthesizer.")
        return "synthesizer"
    
def route_from_planner(state: State) -> str:
    """If there is at least one non-no_tool step, go executor; else go synthesizer."""
    plan = state.get("plan") or {}
    steps: List[Dict[str, Any]] = plan.get("steps", [])
    has_real_tool = any(s["action"] != "no_tool" for s in steps)

    if has_real_tool:
        print("[ROUTER] Plan includes tool steps. Going to Executor.")
        return "executor"
    else:
        print("[ROUTER] Plan has no external tools. Going directly to Synthesizer.")
        return "synthesizer"