"""
General Assistant Agent

A general-purpose assistant for everyday tasks and information queries.
"""

from langgraph.graph import StateGraph, END
from langgraph.types import RunnableConfig
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from ..runtime.model import get_llm
from ..runtime.schema import AgentState
from ..runtime.tools.datetime_tool import get_current_datetime
from ..runtime.tools.web_search import search_web


def get_general_tools():
    """Get tools for general assistance tasks."""
    return [get_current_datetime, search_web]


async def general_node(state: AgentState, config: RunnableConfig):
    """Handle general assistance tasks and determine next actions."""
    tools = get_general_tools()
    model_name = state.get("model", "gpt-4o") or "gpt-4o"
    llm = get_llm(model_name).bind_tools(tools, parallel_tool_calls=False)
    
    system_message = """You are a helpful general assistant that can help with various tasks.
    
    Your capabilities:
    - Search the web for current information
    - Provide current date/time context
    - Answer general knowledge questions
    - Help with everyday tasks and queries
    
    Be friendly, helpful, and provide accurate information."""
    
    messages = state.messages if hasattr(state, 'messages') else state.get("messages", [])
    response = await llm.ainvoke([SystemMessage(content=system_message), *messages], config=config)
    
    # Update state with new message
    new_state = {**state}
    if "messages" not in new_state:
        new_state["messages"] = []
    new_state["messages"].append(response)
    
    return new_state


# Build the general agent graph
general_graph_builder = StateGraph(AgentState)

# Add nodes
general_graph_builder.add_node("general", general_node)
general_graph_builder.add_node("tools", ToolNode(get_general_tools()))

# Add edges
general_graph_builder.set_entry_point("general")
general_graph_builder.add_conditional_edges(
    "general",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
general_graph_builder.add_edge("tools", "general")

# Compile the graph
general_graph = general_graph_builder.compile(
    checkpointer=MemorySaver(),
)
