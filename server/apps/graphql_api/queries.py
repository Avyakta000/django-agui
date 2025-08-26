
import strawberry
from typing import List
from .types import ModelType, AgentType, SystemPromptType, SystemPromptCategoryType

@strawberry.type
class Query:
    models: List[ModelType] = strawberry.django.field()
    agents: List[AgentType] = strawberry.django.field()
    system_prompts: List[SystemPromptType] = strawberry.django.field()
    system_prompt_categories: List[SystemPromptCategoryType] = strawberry.django.field()
