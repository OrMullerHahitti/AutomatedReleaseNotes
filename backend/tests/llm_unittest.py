import unittest
from unittest.mock import patch
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.services.azure_authentication_client import authenticate_openai

class TestLLMService(unittest.TestCase):

    @classmethod
    @patch('backend.app.services.azure_authentication_client.authenticate_openai')
    def setUpClass(cls, mock_auth):
        mock_auth.return_value.api_key = 'test_api_key'
        cls.api_key = authenticate_openai().api_key
        cls.service = AzureDevOpsService(cls.api_key)

    @patch('backend.app.services.azure_devops_services.AzureDevOpsService.__init__', return_value=None)
    def test_llm_service_initialization_with_authenticated_key(self, mock_init):
        mock_init.assert_called_once_with('test_api_key')

    # Add other tests here that use self.servic@patch('backend.app.services.azure_devops_services.AzureDevOpsService.some_method')
    def test_some_other_functionality(self, mock_some_method):
        # Use self.api_key and self.service in your test
        result = self.service.some_method()
        mock_some_method.assert_called_once()
        # Add assertions based on the expected behaviore