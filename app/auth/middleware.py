from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from .google import verify_google_id_token, GoogleTokenError


@dataclass
class AuthenticatedUser:
    id: str
    email: str
    is_authenticated: bool = True


class GoogleBearerAuthMiddleware(MiddlewareMixin):
    """
    Authenticate requests using a Google ID token provided as a Bearer token.

    - Expected header: Authorization: Bearer <id_token>
    - On success, attaches `request.user` with minimal fields and `request.auth_claims`.
    - On failure, leaves `request.user` as AnonymousUser.
    """

    def process_request(self, request):
        authorization: Optional[str] = request.META.get("HTTP_AUTHORIZATION")
        if not authorization or not authorization.startswith("Bearer "):
            request.user = getattr(request, "user", AnonymousUser())
            return None

        token = authorization.split(" ", 1)[1].strip()
        if not token:
            request.user = getattr(request, "user", AnonymousUser())
            return None

        try:
            info = verify_google_id_token(token)
        except GoogleTokenError as exc:
            print(f"[auth] google token verification failed: {exc}")
            request.user = getattr(request, "user", AnonymousUser())
            return None

        # Attach a lightweight user object; optionally map to Django users later
        request.user = AuthenticatedUser(id=info.sub, email=info.email, is_authenticated=True)
        request.auth_claims = {
            "sub": info.sub,
            "email": info.email,
            "email_verified": info.email_verified,
            "name": info.name,
            "picture": info.picture,
            "provider": "google",
        }
        print(f"[auth] authenticated: {info.email} (sub={info.sub})")
        return None


