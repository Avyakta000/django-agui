import json
from django.http import JsonResponse
from django.views import View


class EchoView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode()) if request.body else {}
        except Exception:
            payload = {"_parse_error": True}
        return JsonResponse({"echo": payload})

