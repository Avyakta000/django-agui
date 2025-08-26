"""
Research Assistant Agent

A specialized agent for research tasks using web search and data analysis tools.
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


def get_research_tools():
    """Get tools specific to research tasks."""
    return [get_current_datetime, search_web]


async def research_node(state: AgentState, config: RunnableConfig):
    """Handle research operations and determine next actions."""
    tools = get_research_tools()
    model_name = state.get("model", "gpt-4o") or "gpt-4o"
    llm = get_llm(model_name).bind_tools(tools, parallel_tool_calls=False)
    
    system_message = """You are a research assistant specialized in gathering and analyzing information.
    
    Your capabilities:
    - Search the web for current information
    - Provide current date/time context
    - Analyze and synthesize research findings
    - Present information in a clear, organized manner
    
    Always cite your sources when possible and provide accurate, up-to-date information."""
    
    messages = state.messages if hasattr(state, 'messages') else state.get("messages", [])
    response = await llm.ainvoke([SystemMessage(content=system_message), *messages], config=config)
    
    # Update state with new message
    new_state = {**state}
    if "messages" not in new_state:
        new_state["messages"] = []
    new_state["messages"].append(response)
    
    return new_state


# Build the research agent graph
research_graph_builder = StateGraph(AgentState)

# Add nodes
research_graph_builder.add_node("research", research_node)
research_graph_builder.add_node("tools", ToolNode(get_research_tools()))

# Add edges
research_graph_builder.set_entry_point("research")
research_graph_builder.add_conditional_edges(
    "research",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
research_graph_builder.add_edge("tools", "research")

# Compile the graph
research_graph = research_graph_builder.compile(
    checkpointer=MemorySaver(),
)
