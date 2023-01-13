from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from example.health.checks import checks_conf


class ServiceHealthCheckError(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class HealthView(APIView):
    """Health check view."""

    @staticmethod
    def check_all() -> dict[str, str]:
        """Runs all health checks.

        :return: dict with errors
        """
        errors = {}
        for check in checks_conf.all_checks:
            try:
                check()
            except Exception as exc:
                errors[check.__name__] = str(exc)

        return errors

    def get(self, request) -> Response:
        """Returns information about application health."""
        if errors := self.check_all():
            raise ServiceHealthCheckError(detail=errors)

        return Response('ok')
