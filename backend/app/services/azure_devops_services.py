from typing import List
from fastapi import HTTPException
from app.utils.requests import make_request
from app.models.models import *
from app.utils.config import *
from app.services.base_service import BasePlatform
from datetime import datetime
import json



class AzureDevOpsService(BasePlatform):


    # async def fetch_commits(self, start_date: str, end_date: str) -> List[Commit]:
    #     base_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/_apis/git/repositories/{azure_devops_repo}/commits'
    #
    #     params = {
    #         'searchCriteria.itemVersionVersion': start_date,
    #         'searchCriteria.itemVersionEndDate': end_date,
    #     }
    #
    #     try:
    #         response = await make_request(url=self.base_url, method='POST', headers=authentication_headers, data=params)
    #         commits = response.json()
    #
    #         # Extract commit ids
    #         commit_ids = [commit['commitId'] for commit in commits.get('value', [])]
    #
    #         # Get the work items linked to these commits
    #         work_items = await fetch_work_items_linked_to_commits(azure_devops_org, azure_devops_project, commit_ids)
    #         return work_items
    #
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Failed to fetch work items: {str(e)}")


    async def fetch_work_items(self, sprint_name: str) -> List[WorkItem]:
        try:

            # Step 1: Extract the work item ids relevant to the input sprint

            # Define WIQL query to fetch all work items for the sprint
            wiql_query = {
                "query": f"""
                    SELECT [System.Id], [System.WorkItemType]
                    FROM WorkItems
                    WHERE [System.IterationPath] = '{azure_devops_project}\\{azure_devops_iteration_team}\\{sprint_name}'
                    AND [System.TeamProject] = '{azure_devops_project}'
                    ORDER BY [System.WorkItemType]
                """
            }

            # URL to run the WIQL query
            wiql_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/_apis/wit/wiql?api-version=7.1'

            # Make the request to the WIQL API
            wiql_response = await make_request(url=wiql_url, method='POST', headers=self.auth_headers, data=wiql_query)
            wiql_json_response = wiql_response.json()

            # Fetch the work item identifiers
            work_item_ids = [item['id'] for item in wiql_json_response['workItems']]



            # Step 2: Fetch the detailed work items information
            work_item_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/_apis/wit/workitems?ids={",".join(map(str, work_item_ids))}&api-version=7.1'
            work_item_response = await make_request(url=work_item_url, method='GET', headers=self.auth_headers)
            work_item_data = work_item_response.json()
            print(json.dumps(work_item_data, indent=2))

            # Step 3: Map the response to the WorkItem model
            work_items = []
            for work_item in work_item_data['value']:
                id = str(work_item['id'])
                title = work_item['fields']['System.Title']
                type = work_item['fields']['System.WorkItemType']
                state = work_item['fields']['System.State']
                description = work_item['fields'].get('System.Description', '')

                # Append the work item to the list
                work_items.append(WorkItem(id=id, title=title, type=type, state=state, description=description))

            return work_items


        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch workItems: {str(e)}")


    async def fetch_sprints(self) -> List[Sprint]:
        base_url = f'https://dev.azure.com/{azure_devops_org}/{azure_devops_project}/{azure_devops_team}/_apis/work/teamsettings/iterations?api-version=7.1'
        try:
            response = await make_request(url=base_url, method='GET', headers=self.auth_headers)
            sprints_data = response.json()

            # Extract sprints and map them to the Sprint model
            sprints = []
            for sprint in sprints_data.get("value", {}):
                sprint_id = sprint.get("id")
                sprint_name = sprint.get("name")
                start_date_str = sprint.get("attributes", {}).get("startDate")
                finish_date_str = sprint.get("attributes", {}).get("finishDate")

                # Convert the start and finish dates from string to datetime.date
                start_date = None
                finish_date = None
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                if finish_date_str:
                    finish_date = datetime.strptime(finish_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

                # Create a Sprint model and append to the list
                sprint = Sprint(
                    id=sprint_id,
                    name=sprint_name,
                    start_date=start_date,
                    finish_date=finish_date
                )
                sprints.append(sprint)

            return sprints


        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch sprints: {str(e)}")

# Function to authenticate and interact with Azure DevOps API


# Function to get work items linked to the commits
# TODO: hcange to POST , in order to use WIQL? what is WIQL?
async def fetch_work_items_linked_to_commits(organization: str, project: str, commit_ids: List[str]) -> List[dict]:
    headers = {
        'Authorization': 'Basic <PAT>'  # Replace with your Azure DevOps Personal Access Token (encoded as base64)
    }

    work_items = []
    for commit_id in commit_ids:
        #TODO: DOES THIS API exist?
        commit_work_items_url = f'https://dev.azure.com/{organization}/{project}/_apis/git/commits/{commit_id}/workitems'
        # GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1
        try:
            # Use the utility function for the GET request
            response = await make_request(url=commit_work_items_url, method='GET', headers=headers)
            work_items_data = response.json()
            work_items.extend(work_items_data.get('value', []))
        except Exception as e:
            # Log or handle errors for individual commit IDs
            continue


    return work_items

async def fetch_repositories(organization, project):
    pass

