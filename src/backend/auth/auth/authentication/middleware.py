from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
import time


class UpdateLastRequestMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        current_time = timezone.now()

        if request.user.is_authenticated:
            # Usuarios autenticados
            last_request_time = request.user.last_request

            if last_request_time:
                time_diff = (current_time - last_request_time).total_seconds()

                # Si la diferencia de tiempo es menor a 5 segundos, lanza una excepción
                if time_diff < 5:
                    return JsonResponse(
                        "Las peticiones son demasiado frecuentes. Intenta de nuevo más tarde.",
                        status=429,
                    )

            # Si todo está bien, actualiza el campo 'last_request' a la hora actual
            request.user.last_request = current_time
            request.user.save(update_fields=["last_request"])

        else:
            last_request_time = request.session.get("last_request")

            if last_request_time:
                last_request_time = timezone.datetime.fromisoformat(last_request_time)
                time_diff = (current_time - last_request_time).total_seconds()

                if time_diff < 5:
                    return JsonResponse(
                        "Las peticiones son demasiado frecuentes. Intenta de nuevo más tarde, you are hacker or bot",
                        status=429,
                    )
            request.session["last_request"] = current_time.isoformat()

        return None


RATE_LIMIT = 100  # Límite de peticiones permitidas por IP
TIME_WINDOW = 60  # Tiempo en segundos (p. ej., 60 segundos = 1 minuto)
BLOCK_TIME = 600  # Bloqueo de 10 minutos (600 segundos)


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request) -> JsonResponse | None:
        client_ip = self.get_client_ip(request)

        # Comprobar si la IP está bloqueada
        if cache.get(f"blocked:{client_ip}"):
            return JsonResponse(
                {
                    "error": "Estás bloqueado temporalmente por hacer demasiadas peticiones. Intenta de nuevo más tarde."
                },
                status=429,
            )

        # Controlar la tasa de peticiones
        request_count, first_request_time = cache.get(client_ip, (0, time.time()))

        current_time = time.time()
        time_elapsed = current_time - first_request_time

        if time_elapsed < TIME_WINDOW:
            request_count += 1
        else:
            request_count = 1
            first_request_time = current_time

        if request_count > RATE_LIMIT:
            cache.set(f"blocked:{client_ip}", True, BLOCK_TIME)
            return JsonResponse(
                {
                    "error": "Has excedido el límite de peticiones. Estás bloqueado por 10 minutos."
                },
                status=429,
            )
        cache.set(client_ip, (request_count, first_request_time), TIME_WINDOW)

    def get_client_ip(self, request) -> str:
        # Extraer la IP del cliente del encabezado HTTP o del propio request
        x_forwarded_for: str = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip: str = x_forwarded_for.split(",")[0]
        else:
            ip: str = request.META.get("REMOTE_ADDR")
        return ip
