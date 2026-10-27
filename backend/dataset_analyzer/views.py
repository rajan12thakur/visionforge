from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataset_analyzer.services.annotation_validator import (
validate_yolo_annotation,
)


@api_view(["GET"])
def dataset_module_health(request):
    """Return the operational status of the dataset analysis module."""
    return Response(
        {
            "module": "Dataset Quality Analyzer",
            "service": "VisionForge API",
            "status": "healthy",
            "timestamp": timezone.now().isoformat(),
        },
        status=status.HTTP_200_OK,
    )





@api_view(["POST"])
def validate_annotations(request):
    content = request.data.get("content")
    num_classes = request.data.get("num_classes")

    if not isinstance(content, str):
        return Response(
            {"error": "'content' must be a string."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(num_classes, bool) or not isinstance(num_classes, int):
        return Response(
            {"error": "'num_classes' must be an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if num_classes <= 0:
        return Response(
            {"error": "'num_classes' must be greater than zero."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    result = validate_yolo_annotation(
        content=content,
        num_classes=num_classes,
    )

    return Response(result, status=status.HTTP_200_OK)