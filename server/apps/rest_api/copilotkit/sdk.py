from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from .agents import general_graph, research_graph, medical_graph


sdk = CopilotKitRemoteEndpoint(
    agents=lambda context: [
        LangGraphAgent(
            name="general_assistant",
            description="General-purpose assistant for everyday tasks and information queries.",
            graph=general_graph,
        ),
        LangGraphAgent(
            name="research_assistant",
            description="Specialized research assistant for gathering and analyzing information.",
            graph=research_graph,
        ),
        LangGraphAgent(
            name="medical_assistant",
            description="Medical information assistant (provides general info only, not medical advice).",
            graph=medical_graph,
        ),
    ],
)


