from django.urls import path
from .views.health import HealthView
from .views.echo import EchoView
from .views.langgraph_agui import agui_langgraph_handler
from .copilotkit.endpoints import copilotkit_handler


urlpatterns = [
    path('health', HealthView.as_view(), name='health'),
    path('echo', EchoView.as_view(), name='echo'),
    path('langgraph-agent', agui_langgraph_handler, name='agui-no-slash'),
    
    # CopilotKit endpoints
    path('copilotkit/<path:path>', copilotkit_handler, name='copilotkit-path'),
    path('copilotkit/', copilotkit_handler, name='copilotkit-root'),
]

