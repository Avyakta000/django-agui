import strawberry
from typing import List
from . import models

@strawberry.django.type(models.Model)
class ModelType:
    id: strawberry.ID
    name: str
    value: str
    is_active: bool

@strawberry.django.type(models.Agent)
class AgentType:
    id: strawberry.ID
    name: str
    is_active: bool
    models: List[ModelType]

@strawberry.django.type(models.SystemPromptCategory)
class SystemPromptCategoryType:
    id: strawberry.ID
    name: str
    is_active: bool

@strawberry.django.type(models.SystemPrompt)
class SystemPromptType:
    id: strawberry.ID
    name: str
    value: str
    is_active: bool
    categories: List[SystemPromptCategoryType]
    agents: List[AgentType]
