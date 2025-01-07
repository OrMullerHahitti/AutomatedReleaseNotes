
import asyncio
from backend.app.services.azure_devops_services import AzureDevOpsService
from backend.app.utils.config import *

from pathlib import Path

async def test1():
    azure_test = AzureDevOpsService()
    # sprints_test = await azure_test.fetch_sprints()
    work_items_test = await azure_test.fetch_work_items("Sprint 56")


asyncio.run(test1())




# baseurl = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/{azure_devops_team}/_apis/work/teamsettings/iterations'
# async def get_iterations():
#     response = await make_request(url=baseurl, method='GET', headers=authentication_headers_azure)
#     return response.json()
# async def display_iterations_raw():
#     try:
#         data = await get_iterations()
#         print(json.dumps(data, indent=2))  # Pretty print the JSON
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# asyncio.run(display_iterations_raw())
# TEST FETCH_SPRINTS


