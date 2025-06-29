# langgraph_agent.py

from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import calendar_tools
@tool
def schedule_meeting_tool(input: str) -> str:
    """Schedule a meeting via Google Calendar"""
    return calendar_tools.create_event()
def tool_step(state):
    print("Tool running with:", state)
    input_str = state["input"]
    output = schedule_meeting_tool.invoke(input_str)
    return {"output": output}
workflow = StateGraph(dict)
workflow.add_node("run_tool", tool_step)
workflow.set_entry_point("run_tool")
workflow.set_finish_point("run_tool")
app = workflow.compile()
def run_agent(prompt: str) -> str:
    result = app.invoke({"input": prompt}, RunnableConfig())
    return result["output"]
