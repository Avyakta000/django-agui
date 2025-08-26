"""
Medical Assistant Agent

A specialized agent for medical information and health-related queries.
Note: This agent provides general information only and is not a substitute for professional medical advice.
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


def get_medical_tools():
    """Get tools specific to medical information tasks."""
    return [get_current_datetime, search_web]


async def medical_node(state: AgentState, config: RunnableConfig):
    """Handle medical information queries and determine next actions."""
    tools = get_medical_tools()
    model_name = state.get("model", "gpt-4o") or "gpt-4o"
    llm = get_llm(model_name).bind_tools(tools, parallel_tool_calls=False)
    
    system_message = """You are a medical information assistant that provides general health information.
    
    IMPORTANT DISCLAIMERS:
    - You provide general information only
    - You are NOT a substitute for professional medical advice
    - Always recommend consulting healthcare professionals for medical decisions
    - Never provide diagnosis or treatment recommendations
    
    Your capabilities:
    - Search for general health information
    - Provide current date/time context
    - Explain medical concepts in simple terms
    - Direct users to reliable health resources
    
    Always include appropriate medical disclaimers in your responses."""
    
    messages = state.messages if hasattr(state, 'messages') else state.get("messages", [])
    response = await llm.ainvoke([SystemMessage(content=system_message), *messages], config=config)
    
    # Update state with new message
    new_state = {**state}
    if "messages" not in new_state:
        new_state["messages"] = []
    new_state["messages"].append(response)
    
    return new_state


# Build the medical agent graph
medical_graph_builder = StateGraph(AgentState)

# Add nodes
medical_graph_builder.add_node("medical", medical_node)
medical_graph_builder.add_node("tools", ToolNode(get_medical_tools()))

# Add edges
medical_graph_builder.set_entry_point("medical")
medical_graph_builder.add_conditional_edges(
    "medical",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
medical_graph_builder.add_edge("tools", "medical")

# Compile the graph
medical_graph = medical_graph_builder.compile(
    checkpointer=MemorySaver(),
)
