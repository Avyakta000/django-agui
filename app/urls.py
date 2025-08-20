from django.urls import path
from .copilotkit_integration import copilotkit_handler
from django.views.decorators.csrf import csrf_exempt
from .sdk import sdk

urlpatterns = [
    # copilotkit endpoints
    path(
        "copilotkit/<path:path>", 
        csrf_exempt(copilotkit_handler), 
        name="copilotkit-path"
    ),
]
