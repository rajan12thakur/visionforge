from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def health_check(request):
    """
    Return the operational status of the VisionForge API.
    """
    return Response(
        {
            "service": "VisionForge API",
            "status": "healthy",
            "timestamp": timezone.now().isoformat(),
        },
        status=status.HTTP_200_OK,
    )