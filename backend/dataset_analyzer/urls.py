from django.urls import path

from .views import dataset_module_health, validate_annotations

app_name = "dataset_analyzer"

urlpatterns = [
    path("health/", dataset_module_health, name="health"),
    path("validate-annotations/",validate_annotations,name="validate-annotations",
),
]