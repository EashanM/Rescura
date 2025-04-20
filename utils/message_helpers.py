from langchain_core.messages import AIMessage, ToolMessage
from typing import List, Tuple

def format_scratchpad(intermediate_steps: List[Tuple]) -> List:
    """Convert agent steps to proper message sequence"""
    formatted = []
    for action, observation in intermediate_steps:
        formatted.append(AIMessage(
            content=action.log,
            additional_kwargs={
                "tool_calls": [{
                    "id": action.tool_call_id,
                    "function": {
                        "name": action.tool,
                        "arguments": action.tool_input
                    }
                }]
            }
        ))
        formatted.append(ToolMessage(
            content=str(observation),
            tool_call_id=action.tool_call_id
        ))
    return formatted
