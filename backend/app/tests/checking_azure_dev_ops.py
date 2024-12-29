
import asyncio
import base64
from email.policy import default
import json
from app.utils.config import *
from app.utils.requests import make_request
#from app.services.azure_devops_services import *
from typing import List
from app.models.models import *
from app.utils.requests import *


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




async def fetch_work_items(sprint_id: str) -> List[WorkItem]:

    # Construct the WIQL query to fetch completed work items within the date range
#     wiql_query = f"""
#     SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State], [System.Description], [System.ClosedDate]
#     FROM WorkItems
#     WHERE [System.TeamProject] = '{azure_devops_project}'
#     AND [System.IterationPath]= '{sprint_id}'  -- Filter by sprint
#     ORDER BY [System.ClosedDate] DESC
# """


    base_url = (f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/{azure_devops_team}/_apis/work/teamsettings/iterations/{sprint_id}/workitems?api-version=7.1)'

    # Step 1: Execute the WIQL query
    response = await make_request(url=base_url, method='POST', headers=authentication_headers_azure, data={'query': wiql_query})
    wiql_data = response.json()
    return wiql_data


data = asyncio.run(fetch_work_items("Sprint 57"))


# Sprints API Dcoumentation:
# https://learn.microsoft.com/en-us/rest/api/azure/devops/work/iterations/list?view=azure-devops-rest-7.1&tabs=HTTP
# Run this version for raw data


