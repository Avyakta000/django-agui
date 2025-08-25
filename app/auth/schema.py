from __future__ import annotations

from typing import Optional

import strawberry
from strawberry.types import Info

from app.graphql.permissions import IsAuthenticated
from app.auth.types import Me

@strawberry.type
class AuthQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: Info) -> Me:
        user = info.context["user"]
        claims = info.context.get("auth_claims") or {}
        print("[auth.me] claims:", claims)
        return Me(
            id=getattr(user, "id", ""),
            email=getattr(user, "email", ""),
            email_verified=bool(claims.get("email_verified", False)),
            name=claims.get("name"),
            picture=claims.get("picture"),
        )


