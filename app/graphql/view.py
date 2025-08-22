from __future__ import annotations

from typing import Any, Dict

from strawberry.django.views import AsyncGraphQLView


class GraphQLView(AsyncGraphQLView):
    async def get_context(self, request, response) -> Dict[str, Any]:
        # Ensure resolvers can access request, user and auth_claims consistently
        return {
            "request": request,
            "user": getattr(request, "user", None),
            "auth_claims": getattr(request, "auth_claims", None),
            "response": response,
        }


