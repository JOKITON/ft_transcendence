from rest_framework import ApiView
from rest_framework.response import Response


"""
estaria guay crear cierta logica de regeneracion de claves

que de enviara automanticamente a todos los servicios cada n tiempo

esto lo hacemos basicamente para que jwt, pueda autentificar en varios serivicios a la vez
"""


class KeyPublicView(ApiView):
    def get(self, request):
        return Response({"key": "public"})


class KeyPrivateView(ApiView):
    def get(self, request):
        return Response({"key": "private"})

