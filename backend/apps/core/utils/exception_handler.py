from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        return response

    logger.exception(f"Unhandled exception: {exc}")
    return Response(
        {"error": "Internal server error", "detail": str(exc) if context.get("request") and context["request"].user and context["request"].user.is_superuser else None},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
