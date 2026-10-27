from rest_framework import status
from rest_framework.test import APITestCase


class DatasetModuleHealthTests(APITestCase):
    def test_health_endpoint_returns_200(self):
        response = self.client.get("/api/v1/datasets/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_endpoint_returns_expected_payload(self):
        response = self.client.get("/api/v1/datasets/health/")

        self.assertEqual(
            response.data["module"],
            "Dataset Quality Analyzer",
        )
        self.assertEqual(
            response.data["service"],
            "VisionForge API",
        )
        self.assertEqual(response.data["status"], "healthy")