from django.contrib import admin
from .models import Model, Agent, SystemPrompt, SystemPromptCategory

admin.site.register(Model)
admin.site.register(Agent)
admin.site.register(SystemPrompt)
admin.site.register(SystemPromptCategory)
