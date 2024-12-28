from typing import List
from fastapi import HTTPException
from app.utils.requests import make_request
from base_service import BasePlatform
import base_service
#TODO: perhaps write Authentication function. there will be 3 auth in total
#TODO: get a TOKEN for AUTH
class AzureDevOpsService(BasePlatform):
    async def fetch_commits(self, start_date: str, end_date: str) -> List[Commit]:
        base_url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository}/commits'
        headers = {
            'Authorization': 'Basic <PAT>'  # Replace with your Azure DevOps Personal Access Token (encoded as base64)
        }
        params = {
            'searchCriteria.itemVersionVersion': start_date,
            'searchCriteria.itemVersionEndDate': end_date,
        }

        try:
            # Use the utility function for the GET request
            # TODO: make_request ignores "params" , handle it
            response = await make_request(url=base_url, method='POST', headers=headers, data=params)
            commits = response.json()

            # Extract commit ids
            commit_ids = [commit['commitId'] for commit in commits.get('value', [])]

            # Get the work items linked to these commits
            work_items = await fetch_work_items_linked_to_commits(organization, project, commit_ids)
            return work_items

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch work items: {str(e)}")

    async def fetch_work_items(self) -> List[dict]:
        pass

    async def fetch_sprints(self) -> List[Sprint]:

        pass
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

