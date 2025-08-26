"""
CopilotKit Agents Package

This package contains different specialized agent implementations that use
the shared runtime tools and models from apps.agents.runtime.
"""

from .general import general_graph
from .research import research_graph
from .medical import medical_graph

__all__ = [
    "general_graph",
    "research_graph", 
    "medical_graph"
]
