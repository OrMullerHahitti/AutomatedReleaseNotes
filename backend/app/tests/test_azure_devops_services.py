
import asyncio
import base64
from email.policy import default
import json
from app.utils.config import *
from app.utils.requests import make_request
from app.services.azure_devops_services import *
from typing import List
from app.models.models import *
from app.utils.requests import *
import pytest



async def test1():
    azure_test = AzureDevOpsService()
    # sprints_test = await azure_test.fetch_sprints()
    work_items_test = await azure_test.fetch_work_items("Sprint 56")


    directory_path = Path(log_directory_path)
    file_path = directory_path/'test.txt'
    with file_path.open('a') as file:
        for item in work_items_test:
            file.write(f"{item.id}\n"
                       f"{item.title}\n"
                       f" {item.description}\n"
                       f"{item.type}\n"
                       f"{item.state}")


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


