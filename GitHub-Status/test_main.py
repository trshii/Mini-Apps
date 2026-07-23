# pyright: strict

import unittest
import requests
from unittest.mock import MagicMock, patch
from typing import Any
from main import StatusController, StatusModel, StatusView, ComponentStatus

class TestStatusController(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_model = MagicMock(spec=StatusModel)
        self.mock_view = MagicMock(spec=StatusView)
        self.controller = StatusController(self.mock_model, self.mock_view)
        
    def test_run_success(self) -> None:
        fake_components = [
            ComponentStatus(name="API Requests", status="operational"),
            ComponentStatus(name="Issues", status="degraded_performance")
        ]
        
        self.mock_model.get_github_status.return_value = fake_components
        
        self.controller.run()
        
        self.mock_model.get_github_status.assert_called_once()
        self.mock_view.display_status.assert_called_once_with(fake_components)
        self.mock_view.display_error.assert_not_called()
        
    def test_run_network_failure(self) -> None:
        """Verify that a RequestException is caught and passed to display_error."""
        # 1. Arrange: Force the model to raise a network exception using side_effect
        fake_error = requests.exceptions.ConnectionError("Simulated offline error")
        self.mock_model.get_github_status.side_effect = fake_error

        # 2. Act: Run the controller
        self.controller.run()

        # 3. Assert: Ensure the error was caught and sent to the view's error handler
        self.mock_model.get_github_status.assert_called_once()
        self.mock_view.display_error.assert_called_once_with(fake_error)
        self.mock_view.display_status.assert_not_called()
        
class TestStatusModel(unittest.TestCase):
    """Tests for the Model, intercepting requests.get to test JSON parsing and filtering."""

    @patch("main.requests.get")
    def test_get_github_status_filtering(self, mock_get: MagicMock) -> None:
        """Verify that dummy 'Visit...' components and empty names are filtered out."""
        # 1. Arrange: Create a fake JSON response simulating GitHub's raw API
        fake_json_payload: dict[str, Any] = {
            "page": {"name": "GitHub"},
            "components": [
                {"name": "Visit www.githubstatus.com for more info", "status": "operational"},
                {"name": "", "status": "operational"},  # Should be ignored (empty name)
                {"name": "Git Operations", "status": "operational"},
                {"name": "GitHub Actions", "status": "partial_outage"}
            ]
        }

        # Set up the mock response object
        mock_response = MagicMock()
        mock_response.json.return_value = fake_json_payload
        mock_get.return_value = mock_response

        # 2. Act: Call the model method
        model = StatusModel()
        results = model.get_github_status()

        # 3. Assert: We should only get 2 DTOs back; the "Visit..." and empty name must be gone
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, "Git Operations")
        self.assertTrue(results[0].is_operational)
        self.assertEqual(results[1].name, "GitHub Actions")
        self.assertFalse(results[1].is_operational)
        
        # Ensure raise_for_status was called on our mock response
        mock_response.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()