
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





azure_test = AzureDevOpsService(auth_headers=authentication_headers_azure)
work_items_test = asyncio.run(azure_test.fetch_work_items("Sprint 55"))
print("\n\n\n\n")
for workItem in work_items_test:
    print(workItem)






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


