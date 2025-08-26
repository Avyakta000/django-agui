from langgraph.graph import MessagesState
from typing import Optional, List
from langchain_core.messages import BaseMessage


class AgentState(MessagesState):
    """Agent state that extends MessagesState for proper tool handling."""
    model: Optional[str] = "gpt-4o"
    status: Optional[str] = None
    
    @property
    def messages(self) -> List[BaseMessage]:
        """Get messages from the state."""
        return self.get("messages", [])
    
    def add_message(self, message: BaseMessage):
        """Add a message to the state."""
        if "messages" not in self:
            self["messages"] = []
        self["messages"].append(message)
