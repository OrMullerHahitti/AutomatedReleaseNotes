
import asyncio
import base64
from email.policy import default
import json
from app.utils.config import *
from app.utils.requests import make_request
from app.services.azure_devops_services import *
from typing import List


# baseurl = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/{azure_devops_team}/_apis/work/teamsettings/iterations'
# async def get_iterations():
#     response = await make_request(url=baseurl, method='GET', headers=authentication_headers)
#     return response.json()
# async def display_iterations_raw():
#     try:
#         data = await get_iterations()
#         print(json.dumps(data, indent=2))  # Pretty print the JSON
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# asyncio.run(display_iterations_raw())


# TEST FETCH_SPRINTS
service = AzureDevOpsService()
sprints = asyncio.run(service.fetch_sprints())
for sprint in sprints:
        print(f"Sprint ID: {sprint.id}, Name: {sprint.name}, Start Date: {sprint.start_date}, End Date: {sprint.finish_date}")






# Sprints API Dcoumentation:
# https://learn.microsoft.com/en-us/rest/api/azure/devops/work/iterations/list?view=azure-devops-rest-7.1&tabs=HTTP
# Run this version for raw data


