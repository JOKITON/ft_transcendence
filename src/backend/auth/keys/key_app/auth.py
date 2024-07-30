from django.http import HttpResponse
from django.views import View


class PublicKeyView(View):
    def get(self, request):
        try:
            with open("/keys/secrets/jwt_auth_public.pem", "r") as f:
                public_key = f.read()
            return HttpResponse(public_key, content_type="text/plain")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


class PrivateKeyView(View):
    def get(self, request):
        try:
            with open("/keys/secrets/jwt_auth_private.pem", "r") as f:
                private_key = f.read()
            return HttpResponse(private_key, content_type="text/plain")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
