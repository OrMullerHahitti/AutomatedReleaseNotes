# app/tests/test_azure_devops_api.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.azure_devops_services import AzureDevOpsService

@pytest.fixture
def azure_devops_service():
    return AzureDevOpsService()

@pytest.mark.asyncio
async def test_fetch_commits(azure_devops_service):
    with patch('app.services.azure_devops_services.make_request', new_callable=AsyncMock) as mock_make_request:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'value': [{'commitId': '123'}, {'commitId': '456'}]
        }
        mock_make_request.return_value = mock_response

        work_items = await azure_devops_service.fetch_commits('2023-01-01', '2023-01-31')
        assert len(work_items) == 2
        assert work_items[0]['commitId'] == '123'
        assert work_items[1]['commitId'] == '456'

@pytest.mark.asyncio
async def test_fetch_work_items_linked_to_commits():
    with patch('app.services.azure_devops_services.make_request', new_callable=AsyncMock) as mock_make_request:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'value': [{'id': '1'}, {'id': '2'}]
        }
        mock_make_request.return_value = mock_response

        from app.services.azure_devops_services import fetch_work_items_linked_to_commits
        work_items = await fetch_work_items_linked_to_commits('org', 'proj', ['123', '456'])
        assert len(work_items) == 2
        assert work_items[0]['id'] == '1'
        assert work_items[1]['id'] == '2'